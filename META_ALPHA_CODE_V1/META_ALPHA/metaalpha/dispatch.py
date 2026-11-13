"""Lancement de segments sur un runtime temporaire — SANS navigateur.

Réponse au problème « Colab/Kaggle sont des sessions temporaires » :

    On ne loue pas une session. On loue UNE UNITÉ DE TRAVAIL.

Le cycle complet, entièrement automatisable :

    1. planifier()   : lit l'état sur Drive, choisit les unités restantes
    2. materialiser(): génère un kernel autonome (script .py) + kernel-metadata.json
    3. pousser()     : `kaggle kernels push -p <dir>`  (upload ET exécution)
    4. surveiller()  : `kaggle kernels status` -> QUEUED / RUNNING / COMPLETE / ERROR
    5. recuperer()   : `kaggle kernels output` (rapport, logs)
    6. reprendre()   : si ERROR / COMPLETE partiel -> on repousse le reste

Aucune étape ne nécessite de navigateur. Aucune session n'a besoin de durer.
Si le kernel meurt à 4 h 59, les unités déjà publiées sur Drive sont valides
et la relance reprend exactement à la suivante.

Ce module EXÉCUTE des commandes. Il ne prend aucune décision scientifique.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

KAGGLE_STATUS = {"QUEUED", "RUNNING", "COMPLETE", "ERROR", "CANCEL_ACKNOWLEDGED"}

# Le script poussé est volontairement MINCE : il ne contient aucune logique
# scientifique. Il clone le dépôt (code revu par un humain) puis exécute UN
# segment borné. Le code de calcul vit dans le dépôt, pas dans le kernel.
KERNEL_TEMPLATE = '''# -*- coding: utf-8 -*-
"""Kernel jetable META ALPHA — généré par metaalpha.dispatch.

Rôle unique : exécuter UN segment borné puis s'arrêter.
Ne contient AUCUNE formule scientifique : le code de calcul est cloné depuis
le dépôt (révision épinglée par {git_ref}).

Durée cible : {segment_minutes} min (sous le plafond de 12 h de Kaggle).
"""
import os, sys, subprocess, traceback

SEGMENT_MINUTES = {segment_minutes}
GIT_URL = {git_url!r}
GIT_REF = {git_ref!r}
PHASE = {phase!r}
N_UNITS = {n_units}

def log(msg):
    print(f"[META ALPHA] {{msg}}", flush=True)

def load_secrets():
    """Kaggle Secrets -> variables d'environnement, en mémoire uniquement."""
    try:
        from kaggle_secrets import UserSecretsClient
        c = UserSecretsClient()
        vals = {{}}
        for key in ("GDRIVE_SA_JSON", "GDRIVE_ROOT_FOLDER_ID", "HOLDOUT_SEAL_KEY"):
            try:
                vals[key] = c.get_secret(key)
            except Exception:
                pass
        return vals
    except Exception as exc:
        log(f"secrets indisponibles : {{exc}}")
        return {{}}

def main():
    secrets = load_secrets()
    for k, v in secrets.items():
        if v:
            os.environ[k] = v          # jamais écrit sur disque
    log(f"secrets chargés : {{sorted(k for k,v in secrets.items() if v)}}")

    work = "/tmp/meta_alpha_repo"
    if os.path.isdir(work):
        subprocess.run(["rm", "-rf", work], check=False)
    log(f"clonage du dépôt {{GIT_URL}} @ {{GIT_REF}}")
    subprocess.run(["git", "clone", "--depth", "1", "--branch", GIT_REF, GIT_URL, work], check=True)
    os.chdir(work)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=True)

    sys.path.insert(0, work)
    from metaalpha.segment import run_segment
    result = run_segment(
        phase=PHASE,
        max_units=N_UNITS,
        segment_minutes=SEGMENT_MINUTES,
    )
    log(f"RÉSULTAT: {{json.dumps(result, ensure_ascii=False)}}")
    return 0 if result.get("status") != "FAILED_TECHNICAL" else 1

if __name__ == "__main__":
    import json
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(1)
'''


@dataclass
class DispatchResult:
    ok: bool
    kernel_id: str
    run_dir: str
    command: str
    stdout: str
    dry_run: bool = False


def _run(cmd: list[str], dry_run: bool = False, cwd: str | None = None) -> tuple[int, str]:
    printable = " ".join(cmd)
    if dry_run:
        return 0, f"[dry-run] {printable}"
    env = os.environ.copy()
    # identifiants Kaggle : KAGGLE_USERNAME / KAGGLE_KEY fournis par l'environnement
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def build_kernel_dir(
    out_dir: str | Path,
    *,
    kernel_id: str,
    phase: str,
    n_units: int,
    segment_minutes: int = 210,
    git_url: str = "https://github.com/OWNER/meta-alpha-research.git",
    git_ref: str = "main",
) -> Path:
    """Génère un dossier poussable : kernel-metadata.json + script autonome.

    `kernel_id` doit être « owner/slug ». Le slug doit correspondre au titre
    kagglé (minuscules, tirets) : sinon Kaggle renvoie 403/409.
    """
    if "/" not in kernel_id:
        raise ValueError("kernel_id doit être au format owner/slug")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    slug = kernel_id.split("/", 1)[1]

    script = KERNEL_TEMPLATE.format(
        phase=phase, n_units=n_units, segment_minutes=segment_minutes,
        git_url=git_url, git_ref=git_ref,
    )
    (out / "main.py").write_text(script, encoding="utf-8")

    meta = {
        "id": kernel_id,
        "title": slug,
        "code_file": "main.py",
        "language": "python",
        "kernel_type": "script",          # script : exécution batch, pas d'onglet interactif
        "is_private": True,
        "enable_gpu": False,              # AUCUN GPU : inutile pour ce projet (cf. étude §10.1)
        "enable_internet": True,          # requis : clone du dépôt + API Drive
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
        "model_sources": [],
        "machine_shape": "",
    }
    (out / "kernel-metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out


def push(run_dir: str | Path, *, dry_run: bool = False) -> DispatchResult:
    """Pousse ET exécute. Équivalent d'un `docker run` distant qui rend la main."""
    cmd = ["kaggle", "kernels", "push", "-p", str(run_dir)]
    code, out = _run(cmd, dry_run)
    return DispatchResult(code == 0, "", str(run_dir), " ".join(cmd), out, dry_run)


def status(kernel_id: str, *, dry_run: bool = False) -> tuple[str, str]:
    code, out = _run(["kaggle", "kernels", "status", kernel_id], dry_run)
    for token in KAGGLE_STATUS:
        if token in out.upper():
            return token, out.strip()
    return ("UNKNOWN" if code else "DRY_RUN"), out.strip()


def fetch_output(kernel_id: str, dest: str | Path, *, dry_run: bool = False) -> DispatchResult:
    Path(dest).mkdir(parents=True, exist_ok=True)
    cmd = ["kaggle", "kernels", "output", kernel_id, "-p", str(dest)]
    code, out = _run(cmd, dry_run)
    return DispatchResult(code == 0, kernel_id, str(dest), " ".join(cmd), out, dry_run)


def wait_and_collect(
    kernel_id: str,
    dest: str | Path,
    *,
    poll_seconds: int = 60,
    max_wait_minutes: int = 720,
    dry_run: bool = False,
) -> dict:
    """Attend la fin, récupère la sortie, renvoie un diagnostic exploitable."""
    import time

    start = dt.datetime.now(dt.timezone.utc)
    history: list[dict] = []
    while True:
        st, raw = status(kernel_id, dry_run=dry_run)
        history.append({"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": st})
        if dry_run or st in {"COMPLETE", "ERROR", "CANCEL_ACKNOWLEDGED"}:
            break
        elapsed = (dt.datetime.now(dt.timezone.utc) - start).total_seconds()
        if elapsed > max_wait_minutes * 60:
            st = "TIMEOUT"
            break
        time.sleep(poll_seconds)

    result = {"kernel_id": kernel_id, "final_status": st, "history": history[-20:]}
    if st in {"COMPLETE", "ERROR"} and not dry_run:
        res = fetch_output(kernel_id, dest)
        result["output_ok"] = res.ok
        result["output_dir"] = str(dest)
        log_file = Path(dest) / f"{kernel_id.split('/')[-1]}.log"
        if log_file.exists():
            tail = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-60:]
            result["log_tail"] = tail
    return result


# ---------------------------------------------------------------------------
# Planification : quelles unités restent, et combien par segment ?
# ---------------------------------------------------------------------------
def plan_units(units_all: list[str], done: set[str], n_units: int) -> list[str]:
    """Retourne le prochain lot. PUR : aucune I/O, testable.

    C'est ici que se joue l'autonomie : le lot est recalculé à chaque
    dispatch à partir de l'état réel sur Drive, donc un kernel perdu ne
    provoque ni doublon ni trou.
    """
    remaining = [u for u in units_all if u not in done]
    return remaining[:n_units]


def autonomy_loop(
    *,
    kernel_id: str,
    phase: str,
    units_all: list[str],
    done: set[str],
    n_units: int,
    run_root: str | Path,
    segment_minutes: int = 210,
    max_segments: int = 6,
    git_url: str,
    git_ref: str = "main",
    dry_run: bool = False,
) -> dict:
    """Enchaîne jusqu'à `max_segments` segments. Chaque itération :
    replanifie depuis l'état, pousse, attend, récupère.

    On ne suppose JAMAIS que le segment précédent a tout fait : on relit.
    """
    log: list[dict] = []
    done = set(done)
    for i in range(max_segments):
        done_before = len(done)
        batch = plan_units(units_all, done, n_units)
        if not batch:
            log.append({"segment": i, "state": "ALL_UNITS_DONE"})
            break

        run_dir = Path(run_root) / f"segment_{i:02d}"
        build_kernel_dir(
            run_dir, kernel_id=kernel_id, phase=phase, n_units=len(batch),
            segment_minutes=segment_minutes, git_url=git_url, git_ref=git_ref,
        )
        pushed = push(run_dir, dry_run=dry_run)
        log.append({
            "segment": i, "units_planned": len(batch), "first_unit": batch[0],
            "last_unit": batch[-1], "push_ok": pushed.ok,
        })
        if not pushed.ok:
            log.append({"segment": i, "state": "PUSH_FAILED", "detail": pushed.stdout[-400:]})
            break

        collected = wait_and_collect(
            kernel_id, Path(run_root) / f"segment_{i:02d}_out", dry_run=dry_run
        )
        log.append({"segment": i, "collected": collected})
        if collected["final_status"] not in {"COMPLETE", "DRY_RUN"}:
            # on s'arrête, mais RIEN n'est perdu : la prochaine exécution relira l'état
            log.append({"segment": i, "state": "SEGMENT_UNHEALTHY_STOP"})
            break

        # après chaque segment on RE-DÉRIVE l'état depuis le backend distant
        done |= read_done_from_drive(phase)

        # ANTI-BOUCLE (kit §15.3 : aucune boucle répétitive sans progrès).
        # Si un segment complet n'a fait avancer AUCUNE unité, on s'arrête :
        # continuer consommerait du quota pour rien et masquerait un bug.
        if not dry_run and len(done) <= done_before:
            log.append({
                "segment": i, "state": "NO_PROGRESS_STOP",
                "detail": "aucune unité validée n'a été publiée : arrêt pour ne pas "
                          "consommer de quota inutilement",
            })
            break

    return {
        "segments": log,
        "units_done_total": len(done),
        "units_total": len(units_all),
        "remaining": max(0, len(units_all) - len(done)),
    }


def read_done_from_drive(phase: str, remote=None) -> set[str]:
    """Lit les checkpoints VALIDES sur Drive. Source de vérité unique."""
    from .remote import remote_from_env

    r = remote or remote_from_env()
    try:
        names = r.listdir(f"RESEARCH_V1_XAUUSD_TICK_ONLY/00_GOVERNANCE/checkpoints/{phase}")
    except Exception:
        return set()
    done = set()
    for name in names:
        if not name.endswith(".json"):
            continue
        try:
            ck = r.read_json(
                f"RESEARCH_V1_XAUUSD_TICK_ONLY/00_GOVERNANCE/checkpoints/{phase}/{name}"
            )
            if ck.get("status") == "VALID":
                done.add(ck["unit_id"])
        except Exception:
            continue
    return done


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description="META ALPHA — dispatch de segments")
    ap.add_argument("--phase", required=True)
    ap.add_argument("--kernel-id", required=True, help="owner/slug")
    ap.add_argument("--units", required=True, help="fichier JSON contenant la liste des unités")
    ap.add_argument("--n-units", type=int, default=40)
    ap.add_argument("--segment-minutes", type=int, default=210)
    ap.add_argument("--max-segments", type=int, default=6)
    ap.add_argument("--git-url", required=True)
    ap.add_argument("--git-ref", default="main")
    ap.add_argument("--run-root", default="/tmp/metaalpha_dispatch")
    ap.add_argument("--local-root", default=None, help="pour dériver `done` sans Drive")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    units = json.loads(Path(args.units).read_text(encoding="utf-8"))
    if isinstance(units, dict):
        units = units["units"]

    if args.local_root:
        from .remote import LocalRemote

        done = read_done_from_drive(args.phase, remote=LocalRemote(Path(args.local_root)))
    else:
        done = read_done_from_drive(args.phase)

    result = autonomy_loop(
        kernel_id=args.kernel_id, phase=args.phase, units_all=list(units), done=done,
        n_units=args.n_units, run_root=args.run_root,
        segment_minutes=args.segment_minutes, max_segments=args.max_segments,
        git_url=args.git_url, git_ref=args.git_ref, dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
