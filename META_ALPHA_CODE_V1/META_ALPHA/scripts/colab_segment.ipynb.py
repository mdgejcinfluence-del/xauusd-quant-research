# Notebook de démarrage pour Colab / Kaggle
#
# Objectif : lancer un SEGMENT de travail reproductible de ≤ 3 h 30 sur le
# corpus certifié, avec checkpoints sur Drive et reprise automatique.
#
# ⚠ Ce notebook n'est PAS un service 24/24. Il exécute un segment puis
#   s'arrête. La reprise se fait en le relançant (ou via le worker/watchdog).
#
# Utilisation :
#   1. Exécuter la cellule 0 (installation + montage Drive)
#   2. Exécuter la cellule 1 (préflight) — lecture seule, ne modifie rien
#   3. Exécuter la cellule 2 pour traiter un segment
#
# ---------------------------------------------------------------------------
# CELLULE 0 — installation
# ---------------------------------------------------------------------------
# !git clone https://github.com/<VOUS>/meta-alpha-research.git
# %cd meta-alpha-research
# !pip install -q -r requirements.txt
# from google.colab import drive
# drive.mount('/content/drive')
# import os
# os.environ['METAALPHA_ROOT'] = '/content/drive/MyDrive/META_ALPHA_XAUUSD_DGP'

# ---------------------------------------------------------------------------
# CELLULE 1 — préflight (LECTURE SEULE, aucune écriture hors RESEARCH_V1_*)
# ---------------------------------------------------------------------------
# import os, sys
# sys.path.insert(0, '/content/meta-alpha-research')
# from metaalpha.preflight import run_preflight
# rep = run_preflight(os.environ['METAALPHA_ROOT'], sample='part_000001.parquet')
# print(rep['status'])
# print('partitions :', rep['partitions'])
# print('blocages  :', rep['blocking'])
# assert rep['status'].startswith('PREFLIGHT_OK'), "NE PAS CONTINUER : conflit de base"

# ---------------------------------------------------------------------------
# CELLULE 2 — un segment de travail (reprend où le précédent s'est arrêté)
# ---------------------------------------------------------------------------
# import os, sys
# sys.path.insert(0, '/content/meta-alpha-research')
# from pathlib import Path
# from metaalpha.config import Config, sha256_file
# from metaalpha.fs import Storage
# from metaalpha.orchestrator import Orchestrator
# from scripts.demo_end_to_end import unit_fn   # à remplacer par la vraie unité de phase
#
# root = os.environ['METAALPHA_ROOT']
# storage = Storage.open(root)
# cfg = Config.load('/content/meta-alpha-research/config/execution_config.json')
#
# parts = sorted(p.stem for p in (Path(root)/'01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS').glob('*.parquet'))
# # SEGMENT : on ne prend que ce qui n'est pas encore fait -> reprise naturelle
# from metaalpha.checkpoints import UnitKey, is_valid
# ch = sha256_file(Path(root)/'04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json')
# todo = [u for u in parts if not is_valid(storage, UnitKey('PHASE_2_ANALYTICAL', u, ch, '', ''))]
# print(f"{len(todo)} unités restantes sur {len(parts)}")
#
# orch = Orchestrator(storage, cfg, phase='PHASE_2_ANALYTICAL',
#                     unit_fn=unit_fn('PHASE_2_ANALYTICAL'),
#                     max_runtime_seconds=3*3600 + 1800)   # 3 h 30 : sous le plafond Colab/Kaggle
# out = orch.run(todo, input_hash_for=lambda u: ch + '#' + u)
# print(out.status, out.units_executed, 'exécutées,', out.units_skipped, 'sautées')
# # Si status == BLOCKED_WITH_RESUME : relancer simplement cette cellule.

# ---------------------------------------------------------------------------
# CELLULE 3 — benchmark réel (obligatoire avant toute extrapolation)
# ---------------------------------------------------------------------------
# !python -m metaalpha.bench \
#     --partitions-dir "/content/drive/MyDrive/META_ALPHA_XAUUSD_DGP/01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS" \
#     --n 3 --threads 2 --memory-limit 4GB \
#     --out "/content/drive/MyDrive/META_ALPHA_XAUUSD_DGP/RESEARCH_V1_XAUUSD_TICK_ONLY/40_REPORTS/BENCHMARK_REPORT.json"

# ---------------------------------------------------------------------------
# CELLULE 4 — rapport de fin de segment + heartbeat
# ---------------------------------------------------------------------------
# import json
# print(json.dumps(storage.read_json('00_GOVERNANCE/state.json'), indent=2))
