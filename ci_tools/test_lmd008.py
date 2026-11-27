#!/usr/bin/env python3
"""Tests LMD-008 (executes)."""
import hashlib, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/LOSS_MECHANISM_DIAGNOSIS_008'
SRC = R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

V1 = pd.read_csv(SRC / 'BACKTEST_V1_RESULTS.csv'); V2 = pd.read_csv(SRC / 'BACKTEST_V2_F2_RESULTS.csv')
t('01 baseline seq475 inchangee (4107/-30.40 ; 3275/-33.24)',
  len(V1) == 4107 and abs(V1.pnl_net_usd_S0.sum() + 30.40) < 0.05 and len(V2) == 3275 and abs(V2.pnl_net_usd_S0.sum() + 33.24) < 0.05)
t('02 deficit concentre en 3 positions (V1 < -30 ; V2 < -25)',
  V1[V1.nb_positions == 3].pnl_net_usd_S0.sum() < -30 and V2[V2.nb_positions == 3].pnl_net_usd_S0.sum() < -25)
F = pd.read_csv(OUT / 'BASKET_LOSS_FORENSICS.csv')
t('03 forensique complete: 7382 paniers avec MFE/MAE', len(F) == 7382 and F.MFE_bp_vs_pwa_final.notna().all() and F.MAE_bp_vs_pwa_final.notna().all())
t('04 aucun panier en octobre (GAP respecte)', not F.mois_cloture.eq('2026-10').any())
cfg = __import__('json').loads((SRC / 'FROZEN_ENGINE_CONFIGS.json').read_text())
t('05 moteurs geles inchanges (hashes)',
  hashlib.sha256((R / 'ci_tools/colorful_replay.py').read_bytes()).hexdigest() == cfg['moteurs']['V1']['sha256'] and
  hashlib.sha256((R / 'ci_tools/colorful_replay_v2.py').read_bytes()).hexdigest() == cfg['moteurs']['V2-F2']['sha256'])
need = ['LOSS_DIAGNOSIS_EXECUTIVE_REPORT.md','BASKET_LOSS_FORENSICS.csv','OPEN_BASKET_CHRONOLOGY.csv','REINFORCEMENT_IMPACT.csv','ENTRY_FORWARD_ANALYSIS.csv','COST_DECOMPOSITION.csv','LOSS_ATTRIBUTION.csv','V1_V2_COMPARISON.csv','DATA_COVERAGE_AND_LIMITATIONS.md','TEST_REPORT.md']
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('06 10 livrables presents + chaine valide', all((OUT / f).exists() for f in need) and verify()[0])
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
