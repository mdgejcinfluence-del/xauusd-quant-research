"""Démonstration du dispatcher : enchainer des sessions temporaires SANS navigateur.

Ce script ne pousse rien sur Kaggle (dry_run=True par défaut). Il montre
exactement ce que le dispatcher ferait : planifier -> générer -> pousser ->
attendre -> récupérer -> replanifier.

    python scripts/demo_dispatch.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src_helper import build_corpus  # noqa: E402
from metaalpha.dispatch import autonomy_loop, build_kernel_dir, plan_units  # noqa: E402
from metaalpha.remote import LocalRemote  # noqa: E402


def main() -> int:
    ws = Path("/tmp/metaalpha_dispatch_demo")
    if ws.exists():
        shutil.rmtree(ws)
    root = build_corpus(ws / "drive", n_parts=10, rows=1500)

    print("=" * 76)
    print("DISPATCHER META ALPHA — sessions temporaires, aucun navigateur")
    print("=" * 76)

    # 1) Génération d'un kernel réellement poussable
    kdir = build_kernel_dir(
        ws / "kernel", kernel_id="owner/meta-alpha-segment",
        phase="PHASE_2_ANALYTICAL", n_units=40, segment_minutes=210,
        git_url="https://github.com/owner/meta-alpha-research.git",
    )
    meta = json.loads((kdir / "kernel-metadata.json").read_text())
    print("\n[1] KERNEL GÉNÉRÉ (prêt pour `kaggle kernels push`)")
    for k in ("id", "title", "kernel_type", "is_private", "enable_gpu", "enable_internet"):
        print(f"    {k:<16} = {meta[k]}")
    print(f"    fichiers         = {sorted(p.name for p in kdir.iterdir())}")

    # 2) La boucle autonome : 3 segments de 4 unités
    units = [f"part_{i:06d}" for i in range(1, 11)]
    print("\n[2] BOUCLE AUTONOME — 10 unités, 4 par segment, 3 segments demandés")
    import os
    os.environ["METAALPHA_LOCAL_ROOT"] = str(root)   # état lu depuis le backend local
    result = autonomy_loop(
        kernel_id="owner/meta-alpha-segment",
        phase="PHASE_2_ANALYTICAL",
        units_all=units,
        done=set(),
        n_units=4,
        run_root=ws / "runs",
        segment_minutes=210,
        max_segments=3,
        git_url="https://github.com/owner/meta-alpha-research.git",
        dry_run=True,          # aucun appel réseau : on montre le plan
    )

    for seg in result["segments"]:
        if "units_planned" in seg:
            print(f"    segment {seg['segment']} : {seg['units_planned']} unités "
                  f"({seg['first_unit']} → {seg['last_unit']}) push_ok={seg['push_ok']}")
        elif "state" in seg:
            print(f"    segment {seg.get('segment')} : {seg['state']}")
    print("    rappel : en dry-run rien n'est publié sur le backend distant,")
    print("             donc l'état n'avance pas et le lot est volontairement identique.")
    print("             En réel, le garde-fou NO_PROGRESS_STOP arrêterait la boucle.")

    # 3) Preuve de la propriété qui compte : un segment perdu ne crée ni doublon ni trou
    print("\n[3] PROPRIÉTÉ CLÉ — perte d'un segment")
    done = {"part_000001", "part_000002", "part_000003", "part_000004"}
    print(f"    4 unités validées sur Drive, le kernel meurt pendant les 5-8")
    rep = plan_units(units, done, 4)
    print(f"    après replanification, le lot suivant est : {rep}")
    print("    => aucune unité rejouée, aucune unité sautée : la session est jetable")

    # 4) Ce qu'il faudrait changer pour passer en réel
    print("\n[4] PASSAGE EN RÉEL (2 lignes à changer)")
    print("    - dry_run=True  ->  False")
    print("    - renseigner KAGGLE_USERNAME / KAGGLE_KEY + GDRIVE_SA_JSON dans les secrets")
    print("\n    Aucun GPU. Aucun navigateur. Aucune session à maintenir ouverte.")
    print("    Les fichiers générés sont dans :", ws / "kernel")
    return 0


if __name__ == "__main__":
    sys.exit(main())
