"""Exécution d'UN segment borné — le code qui tourne DANS le kernel jetable.

Contraintes absolues, toutes imposées ici :

- durée bornée (arrêt propre AVANT le plafond du runtime hôte) ;
- une unité = 1 partition téléchargée → calculée → publiée → supprimée ;
- reprise : on ne traite que ce qui n'est pas déjà VALID sur Drive ;
- disque local surveillé (Kaggle n'offre que ~20 Go) ;
- aucune écriture hors RESEARCH_V1_* (délégué au Storage) ;
- aucune décision scientifique.

L'unité de calcul elle-même est FOURNIE par la phase (registre humain).
Ici, on ne fait que l'ordonner.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import tempfile
import time
from pathlib import Path

from .checkpoints import UnitKey, is_valid, write as write_ckpt
from .config import Config, code_hash, sha256_file
from .fs import Storage
from .governance import assert_not_killed, load_state, save_state
from .remote import remote_from_env

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config" / "execution_config.json"


def _log(msg: str) -> None:
    print(f"[META ALPHA {dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')}] {msg}", flush=True)


def _free_gb(path: Path) -> float:
    return shutil.disk_usage(path).free / 1e9


def run_segment(
    *,
    phase: str,
    max_units: int = 40,
    segment_minutes: int = 210,
    config_path: str | Path | None = None,
    remote=None,
    unit_fn=None,
    workdir: str | Path | None = None,
    local_root: str | None = None,
) -> dict:
    """Traite jusqu'à `max_units` unités, ou jusqu'à la limite de temps.

    Retourne toujours un statut terminal de la liste autorisée par le kit.
    """
    started = time.time()
    deadline = started + segment_minutes * 60

    cfg = Config.load(config_path or DEFAULT_CONFIG)
    remote = remote or remote_from_env(local_root)
    storage = Storage.open(local_root or "/tmp/meta_alpha_research_zone")
    ch = code_hash()
    tmp_root = Path(workdir or tempfile.mkdtemp(prefix="metaalpha_seg_"))
    tmp_root.mkdir(parents=True, exist_ok=True)

    # ---- 1. inventaire des unités disponibles (source de vérité : Drive)
    parts_rel = cfg.get("paths", "partitions_rel")
    unit_files = [n for n in remote.listdir(parts_rel) if n.endswith(".parquet")]
    if not unit_files:
        return {"status": "BLOCKED_WITH_RESUME", "reason": "aucune partition listée",
                "phase": phase, "resume_from": None}
    _log(f"{len(unit_files)} partitions visibles sur le backend distant")

    input_hash = _certificate_hash(remote, cfg)
    executed = skipped = failed = 0
    errors: list[str] = []
    resume_from = None
    done_ids: list[str] = []

    unit_fn = unit_fn or _default_unit_fn(remote, cfg, phase)

    for name in unit_files:
        uid = name.replace(".parquet", "")
        if executed + skipped >= max_units:
            resume_from = uid
            break
        if time.time() > deadline:
            resume_from = uid
            errors.append("SEGMENT_TIME_LIMIT")
            break
        try:
            assert_not_killed(storage)
        except Exception as exc:
            resume_from = uid
            errors.append(str(exc))
            break

        key = UnitKey(phase=phase, unit_id=uid, input_hash=input_hash,
                      code_hash=ch, config_hash=cfg.sha)
        if is_valid(storage, key):
            skipped += 1
            done_ids.append(uid)
            continue

        # garde-fou disque : seuil absolu ET proportionnel au disque du runtime.
        # Sur un runner de 1 Go comme sur un Kaggle de 20 Go, on ne se lance pas
        # dans une unité qui ferait exploser le disque en cours de route.
        total_gb = shutil.disk_usage(tmp_root).total / 1e9
        need_gb = max(
            float(cfg.get("orchestrator", "min_free_gb", default=2.0)),
            float(cfg.get("orchestrator", "disk_guard_ratio", default=0.15)) * total_gb,
        )
        if _free_gb(tmp_root) < need_gb:
            resume_from = uid
            errors.append("DISK_PRESSURE")
            break

        t0 = time.time()
        local_part = None
        try:
            # 2. télécharger UNE partition seulement
            local_part = remote.download(f"{parts_rel}/{name}", tmp_root / name)
            # 3. calculer et publier l'unité
            rows, out_rel, out_sha = unit_fn(uid, local_part, storage)
            write_ckpt(storage, key, output_rel=out_rel, output_sha=out_sha, rows=rows,
                       elapsed_s=time.time() - t0, runtime="segment", attempts=1)
            # 4. publier le checkpoint et l'artefact sur le backend distant
            _publish(remote, storage, out_rel)
            _publish(remote, storage, key.rel)
            executed += 1
            done_ids.append(uid)
            _log(f"{uid} OK ({rows} lignes, {time.time()-t0:.1f}s)")
        except Exception as exc:
            failed += 1
            errors.append(f"{uid}: {exc}")
            _log(f"{uid} ÉCHEC : {exc}")
            resume_from = uid
        finally:
            # 5. libérer le disque : une session ne stocke rien durablement
            if local_part and local_part.exists():
                local_part.unlink(missing_ok=True)

        if failed and "DETERMINISTIC" in errors[-1]:
            break

    elapsed = time.time() - started
    status = (
        "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"
        if failed == 0 and resume_from is None and executed + skipped >= len(unit_files)
        else ("FAILED_TECHNICAL" if failed else "BLOCKED_WITH_RESUME")
    )

    report = {
        "phase": phase,
        "status": status,
        "units_total_available": len(unit_files),
        "units_executed": executed,
        "units_skipped_from_checkpoint": skipped,
        "units_failed": failed,
        "resume_from": resume_from,
        "elapsed_s": round(elapsed, 2),
        "segment_minutes_budget": segment_minutes,
        "code_hash": ch,
        "config_hash": cfg.sha,
        "errors": errors[:20],
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    _publish_report(remote, storage, phase, report)

    st = load_state(storage)
    st["active_phase"] = phase
    st["phase_status"] = status
    st["last_unit_done"] = done_ids[-1] if done_ids else st.get("last_unit_done")
    save_state(storage, st)
    _publish(remote, storage, "00_GOVERNANCE/state.json")

    shutil.rmtree(tmp_root, ignore_errors=True)
    return report


# ---------------------------------------------------------------------------
def _certificate_hash(remote, cfg: Config) -> str:
    """Hash du certificat hérité : il entre dans la clé de checkpoint."""
    rel = cfg.get("paths", "cert_p2_rel")
    try:
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            p = remote.download(rel, Path(td) / "cert.json")
            return sha256_file(p)
    except Exception:
        return "sha256:UNAVAILABLE"


def _publish(remote, storage: Storage, rel: str) -> None:
    src = storage._resolve_read(rel)
    if src.exists():
        try:
            remote.upload(src, f"{storage.writable_subdir}/{rel}")
        except Exception as exc:
            _log(f"publication distante impossible pour {rel} : {exc}")


def _publish_report(remote, storage: Storage, phase: str, report: dict) -> None:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rel = f"40_REPORTS/{phase}/{stamp}_segment.json"
    storage.write_atomic_json(rel, report)
    _publish(remote, storage, rel)


def _default_unit_fn(remote, cfg: Config, phase: str):
    """Unité de démonstration : agrégat causal par partition.

    ⚠ Ce n'est PAS une formule scientifique. En production, la phase fournit
    son propre `unit_fn` issu d'un Formula Registry humain.
    """
    from .duck import connect

    def _fn(uid: str, local_part: Path, storage: Storage):
        out_rel = f"20_DERIVED/{phase}/{uid}.parquet"
        out_path = storage._resolve_write(out_rel)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with connect(
            memory_limit=cfg.get("duckdb", "memory_limit", default="4GB"),
            threads=int(cfg.get("duckdb", "threads", default=2)),
            temp_dir=cfg.get("duckdb", "temp_dir", default="/tmp/duckdb_spill"),
        ) as con:
            con.execute(
                f"""
                COPY (
                    SELECT date_trunc('day', timestamp) AS day,
                           count(*)                    AS n_ticks,
                           avg(ask - bid)              AS spread_mean_observed,
                           min(timestamp)              AS t_min,
                           max(timestamp)              AS t_max
                    FROM read_parquet('{local_part.as_posix()}')
                    GROUP BY 1 ORDER BY 1
                ) TO '{out_path.as_posix()}' (FORMAT PARQUET)
                """
            )
            rows = con.execute(
                f"SELECT count(*) FROM read_parquet('{out_path.as_posix()}')"
            ).fetchone()[0]
        return int(rows), out_rel, sha256_file(out_path)

    return _fn
