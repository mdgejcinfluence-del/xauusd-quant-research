"""L6 — extraction de la matrice, par partition, avec checkpoints durables.

C'est le barreau coûteux de l'échelle. Trois règles le rendent sûr :

1. **Une partition à la fois.** Jamais le corpus entier en mémoire. DuckDB
   écrit le résultat d'une partition, on passe à la suivante.
2. **Checkpoint avant / après.** Une partition terminée est enregistrée avec
   le hash de sa sortie. Relancer ne refait que ce qui manque. Un arrêt de 12 h
   ou une coupure de session ne coûte que la partition en cours.
3. **Aucune variable sans définition.** On n'extrait que les variables
   présentes dans le Variable Registry. Une variable bloquée n'entre pas dans
   la matrice — sinon la matrice contiendrait un paramètre inventé.

Le résultat n'est pas un « résultat scientifique » : c'est une matière première
tracée. Aucune conclusion d'edge ne peut être tirée ici.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any, Iterable

from .fs import Storage
from . import registry

MATRIX_DIR = "11_EXTRACTION/MATRIX"
CHECKPOINT_REL = "11_EXTRACTION/EXTRACTION_CHECKPOINTS_V1.json"


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


# Paramètre attendu par variable, tel qu'écrit par decisions.py.
# Table explicite : si le nom change d'un côté, on veut une erreur bruyante,
# pas un None silencieux.
PARAM_NAME = {
    "ROLL_STD_MID": "N",
    "ROLL_RANGE_MID": "N",
    "MAD_NORM_DEV": "N",
}


def _expr_for(variable_id: str, params: dict[str, Any]) -> str | None:
    """Traduit une variable du Registry en expression SQL.

    Seules les variables dont la sémantique est SANS AMBIGUÏTÉ sont traduites ici.
    Tout le reste lève : on préfère ne pas extraire plutôt qu'extraire faux.
    """
    v = variable_id.upper()

    if v == "MID":
        return "((ask + bid) / 2.0)"
    if v == "SPREAD_ABS":
        return "(ask - bid)"
    if v == "SPREAD_REL":
        return "CASE WHEN (ask + bid) <> 0 THEN (ask - bid) / ((ask + bid) / 2.0) END"
    if v == "RET_TICK":
        return ("((ask + bid) / 2.0) / NULLIF(lag((ask + bid) / 2.0) OVER (ORDER BY t), 0) - 1")

    # --- variables paramétrées : uniquement si le paramètre est EXPLICITE ---
    if v == "ROLL_STD_MID":
        w = params.get(PARAM_NAME["ROLL_STD_MID"])
        n = _as_int(w)
        if n is None:
            raise _MissingParameter(f"ROLL_STD_MID : fenêtre absente ou non entière ({w!r})")
        # Decision proprietaire: ecart-type des RENDEMENTS mid consecutifs
        # r_i = (mid_i - mid_{i-1}) / mid_{i-1}, PAS des niveaux de mid.
        # ret_mid est calcule par l'etage enrichi de extract_partition.
        # Warm-up NULL: il faut N rendements, donc premiere valeur a l'evenement N+1.
        return (f"CASE WHEN row_number() OVER (ORDER BY t) >= {n + 1} THEN "
                f"stddev_samp(ret_mid) OVER (ORDER BY t "
                f"ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW) END")

    if v == "ROLL_RANGE_MID":
        w = params.get(PARAM_NAME["ROLL_RANGE_MID"])
        n = _as_int(w)
        if n is None:
            raise _MissingParameter(f"ROLL_RANGE_MID : fenêtre absente ou non entière ({w!r})")
        return (f"CASE WHEN row_number() OVER (ORDER BY t) >= {n} THEN "
                f"(max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW)"
                f" - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN {n - 1} PRECEDING AND CURRENT ROW)) END")

    if v == "UPDATE_INTENSITY":
        w = params.get("T")
        n = _as_seconds(w)
        if n is None:
            raise _MissingParameter(f"UPDATE_INTENSITY : duree T absente ou non entiere ({w!r})")
        # fenetre temps causale [t-T, t] : RANGE sur le timestamp, passe + present.
        return (f"count(*) OVER (ORDER BY t RANGE BETWEEN INTERVAL {n} SECOND PRECEDING AND CURRENT ROW)")

    if v == "INTERARRIVAL_MEAN":
        w = params.get("N")
        n = _as_int(w)
        if n is None:
            raise _MissingParameter(f"INTERARRIVAL_MEAN : fenetre N absente ou non entiere ({w!r})")
        # moyenne des N derniers inter-arrivees = (t - t[t-N]) / N (somme telescopique exacte).
        # NULL tant que t[t-N] n'existe pas (warm-up NULL, aucune valeur fabriquee).
        return (f"(epoch(t) - epoch(lag(t, {n}) OVER (ORDER BY t))) / {n}.0")

    if v == "RET_H":
        # RET_H_ALIGN_V1 (validee par le proprietaire): RET_H(t) = (MID(t_H)-MID(t))/MID(t),
        # t_H = premier tick a ou apres t+H. Label uniquement, jamais une feature.
        # NULL si aucun tick n'existe avant la fin du segment (horizon incomplet).
        w = params.get("H")
        n = _as_seconds(w)
        if n is None:
            raise _MissingParameter(f"RET_H : horizon H absent ou illisible ({w!r})")
        return (f"(((SELECT b2.mid FROM enriched b2 WHERE b2.t >= e.t + INTERVAL {n} SECOND "
                f"ORDER BY b2.t LIMIT 1) - e.mid) / NULLIF(e.mid, 0))")

    raise _NotTranslatable(f"{variable_id} : pas de traduction SQL certifiée à ce stade")


def _as_seconds(x: Any) -> int | None:
    """Duree proprietaire ('1s', '5s', '30s', '1min') -> secondes entieres."""
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return int(x) if int(x) > 0 else None
    s = str(x).strip().lower()
    try:
        if s.endswith("min"):
            return int(float(s[:-3]) * 60)
        if s.endswith("h"):
            return int(float(s[:-1]) * 3600)
        if s.endswith("s"):
            return int(float(s[:-1]))
        return int(float(s))
    except (TypeError, ValueError):
        return None


class _MissingParameter(RuntimeError):
    """Le registre contient la variable mais pas son paramètre : incohérence."""


class _NotTranslatable(RuntimeError):
    """La variable existe mais sa formule n'est pas encore figée : on n'invente pas."""


def _as_int(x: Any) -> int | None:
    try:
        n = int(str(x).strip())
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def plan_extraction(storage: Storage) -> dict[str, Any]:
    """Décide QUOI extraire, sans rien exécuter.

    Rend la liste des variables extractibles et, séparément, celles qui sont
    refusées avec la raison exacte. C'est la partie qui répond à « l'ingénierie
    fera quoi, concrètement ».
    """
    if not storage.exists(registry.VARIABLE_REGISTRY_REL):
        return {"status": "NO_REGISTRY", "extractible": [], "refused": []}

    reg = storage.read_json(registry.VARIABLE_REGISTRY_REL)
    extractible: list[dict[str, Any]] = []
    refused: list[dict[str, Any]] = []

    for key, var in reg.get("variables", {}).items():
        vid = var.get("variable_id") or key.split("@")[0]
        params = var.get("parameters") or {}
        # Remediation audit: chaque couple (variable, fenetre) est une entree
        # distincte, certifiable separement, sans ecraser les autres fenetres.
        window_key = {"ROLL_STD_MID": "N", "ROLL_RANGE_MID": "N",
                      "UPDATE_INTENSITY": "T", "INTERARRIVAL_MEAN": "N",
                      "RET_H": "H"}.get(vid)
        windows = [None]
        if window_key and isinstance(params.get(window_key), (list, tuple)):
            windows = list(params[window_key])
        for w in windows:
            p_one = dict(params)
            entry_id = vid
            if w is not None:
                p_one[window_key] = w
                entry_id = f"{vid}_{window_key}{w}"
            try:
                expr = _expr_for(vid, p_one)
            except _MissingParameter as exc:
                refused.append({"variable_id": vid, "entry_id": entry_id, "reason": str(exc), "cause": "PARAMETRE_MANQUANT"})
                continue
            except _NotTranslatable as exc:
                refused.append({"variable_id": vid, "entry_id": entry_id, "reason": str(exc), "cause": "FORMULE_NON_CERTIFIEE"})
                continue
            extractible.append({"variable_id": vid, "entry_id": entry_id, "sql": expr, "parameters": p_one,
                                "kind": "label" if vid in ("RET_H", "MFE_H", "MAE_H") else "feature"})

    # Plusieurs versions d'une variable peuvent coexister au registre (v1, v2...):
    # un meme couple (variable, fenetre) ne doit apparaitre qu'une fois dans le plan.
    _seen: dict[str, dict[str, Any]] = {}
    for e in extractible:
        _seen[e.get("entry_id", e["variable_id"])] = e
    extractible = list(_seen.values())
    _seen_r: dict[str, dict[str, Any]] = {}
    for e in refused:
        _seen_r[e.get("entry_id", e["variable_id"])] = e
    refused = list(_seen_r.values())
    return {
        "status": "PLANNED",
        "extractible_total": len(extractible),
        "refused_total": len(refused),
        "extractible": extractible,
        "refused": refused,
    }


def extract_partition(
    parquet_path: str | Path,
    plan: dict[str, Any],
    *,
    out_path: str | Path,
    ts_col: str = "timestamp",
    bid_col: str = "bid",
    ask_col: str = "ask",
    memory_limit: str = "4GB",
    threads: int = 2,
) -> dict[str, Any]:
    """Écrit la matrice d'UNE partition. Retourne les métriques + le hash."""
    from .duck import connect
    from .config import sha256_file

    feats = plan.get("extractible") or []
    if not feats:
        return {"status": "NOTHING_TO_EXTRACT", "reason": "aucune variable extractible"}

    select_list = ",\n        ".join(f"{f['sql']} AS {f.get('entry_id', f['variable_id'])}" for f in feats)
    src = Path(parquet_path).as_posix()
    dst = Path(out_path)
    dst.parent.mkdir(parents=True, exist_ok=True)

    q = f"""
    COPY (
        WITH base AS (
            SELECT "{ts_col}" AS t, "{bid_col}" AS bid, "{ask_col}" AS ask
            FROM read_parquet('{src}')
            ORDER BY "{ts_col}"
        ),
        with_mid AS (
            SELECT t, bid, ask, ((ask + bid) / 2.0) AS mid FROM base
        ),
        enriched AS (
            SELECT t, bid, ask, mid,
                   (mid / NULLIF(lag(mid) OVER (ORDER BY t), 0) - 1) AS ret_mid
            FROM with_mid
        )
        SELECT t, bid, ask,
        {select_list}
        FROM enriched e
    ) TO '{dst.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """

    with connect(memory_limit=memory_limit, threads=threads) as con:
        con.execute(q)
        rows = con.execute(f"SELECT count(*) FROM read_parquet('{dst.as_posix()}')").fetchone()[0]

    return {
        "status": "EXTRACTED",
        "source": str(parquet_path),
        "output": str(dst),
        "rows": int(rows),
        "columns": [f.get("entry_id", f["variable_id"]) for f in feats],
        "sha256": sha256_file(dst),
        "size_bytes": dst.stat().st_size,
    }


def run_extraction(
    storage: Storage,
    partitions: Iterable[dict[str, Any]],
    *,
    limit: int | None = None,
) -> dict[str, Any]:
    """Extrait les partitions manquantes, une par une, avec checkpoint durable."""
    plan = plan_extraction(storage)
    if plan["status"] != "PLANNED" or not plan.get("extractible"):
        return {"status": "BLOCKED", "plan": plan,
                "reason": "aucune variable extractible : répondre aux décisions d'abord"}

    ckpt = storage.read_json(CHECKPOINT_REL) if storage.exists(CHECKPOINT_REL) else {
        "schema_version": "1.0", "partitions": {}
    }

    done: list[dict[str, Any]] = []
    skipped: list[str] = []
    errors: list[dict[str, str]] = []

    targets = list(partitions)
    if limit is not None:
        targets = targets[:limit]

    for part in targets:
        pid = part["partition_id"]
        prev = ckpt["partitions"].get(pid)
        if prev and prev.get("status") == "EXTRACTED" and Path(prev["output"]).exists():
            skipped.append(pid)
            continue

        out = storage.root / storage.writable_subdir / MATRIX_DIR / f"{pid}.parquet"
        try:
            res = extract_partition(part["path"], plan, out_path=out)
        except Exception as exc:
            errors.append({"partition_id": pid, "error": f"{type(exc).__name__}: {exc}"})
            ckpt["partitions"][pid] = {"status": "FAILED", "error": str(exc), "utc": _now()}
            storage.write_atomic_json(CHECKPOINT_REL, ckpt)   # checkpoint même en échec
            continue

        ckpt["partitions"][pid] = {**res, "utc": _now()}
        storage.write_atomic_json(CHECKPOINT_REL, ckpt)       # durable, partition par partition
        done.append(res)

    report = {
        "schema_version": "1.0",
        "generated_utc": _now(),
        "plan": plan,
        "extracted_now": len(done),
        "skipped_already_done": len(skipped),
        "failed": len(errors),
        "errors": errors,
        "partitions_done_total": sum(
            1 for v in ckpt["partitions"].values() if v.get("status") == "EXTRACTED"
        ),
        "results": done,
    }
    storage.write_atomic_json("11_EXTRACTION/EXTRACTION_RUN_V1.json", report)
    return report


# ---------------------------------------------------------------------------
# L7 — le contrat : rendre la matrice opposable
# ---------------------------------------------------------------------------
def build_manifest(storage: Storage) -> dict[str, Any]:
    """Scelle la matrice : hash global, lignée, et ce qui reste bloqué.

    Un manifeste n'est pas une décoration : c'est ce qui permet, six mois plus
    tard, de prouver quelle matrice exacte a produit quel résultat — et de
    refuser de comparer deux choses différentes.
    """
    from .config import sha256_text

    if not storage.exists(CHECKPOINT_REL):
        return {"status": "NO_EXTRACTION", "reason": "aucune extraction enregistrée"}

    ckpt = storage.read_json(CHECKPOINT_REL)
    parts = {k: v for k, v in ckpt.get("partitions", {}).items() if v.get("status") == "EXTRACTED"}

    entries = []
    for pid, meta in sorted(parts.items()):
        entries.append({
            "partition_id": pid,
            "source": meta.get("source"),
            "output": meta.get("output"),
            "rows": meta.get("rows"),
            "columns": meta.get("columns"),
            "sha256": meta.get("sha256"),
        })

    var_reg = storage.read_json(registry.VARIABLE_REGISTRY_REL) \
        if storage.exists(registry.VARIABLE_REGISTRY_REL) else {"variables": {}}
    plan = plan_extraction(storage)

    lineage = {
        "variables_used": sorted({c for e in entries for c in (e.get("columns") or [])}),
        "variables_refused": [r["variable_id"] for r in plan.get("refused", [])],
        "registry_sha256": sha256_text(
            str(sorted(var_reg.get("variables", {}).keys()))
        )[:32],
    }

    body = {
        "partitions": entries,
        "lineage": lineage,
        "total_rows": sum(e["rows"] or 0 for e in entries),
    }
    manifest_sha = sha256_text(str(body))[:64]

    manifest = {
        "schema_version": "1.0",
        "generated_utc": _now(),
        **body,
        "manifest_sha256": manifest_sha,
        "honesty": {
            "is_scientific_result": False,
            "note": (
                "Ce manifeste prouve l'intégrité de la matière première, pas "
                "l'existence d'un edge. Le Holdout n'est pas ouvert ici."
            ),
        },
    }
    storage.write_atomic_json("11_EXTRACTION/MANIFEST_V1.json", manifest)
    return manifest
