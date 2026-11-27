#!/usr/bin/env python3
"""Tests BACKTEST-2026-001 (executes)."""
import hashlib, json, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

cfg = json.loads((OUT / 'FROZEN_ENGINE_CONFIGS.json').read_text())
t('01 hashes des moteurs geles inchanges',
  hashlib.sha256((R / 'ci_tools/colorful_replay.py').read_bytes()).hexdigest() == cfg['moteurs']['V1']['sha256'] and
  hashlib.sha256((R / 'ci_tools/colorful_replay_v2.py').read_bytes()).hexdigest() == cfg['moteurs']['V2-F2']['sha256'])
V1 = pd.read_csv(OUT / 'BACKTEST_V1_RESULTS.csv'); V2 = pd.read_csv(OUT / 'BACKTEST_V2_F2_RESULTS.csv')
t('02 reconciliation novembre V1 (379 paniers, -0.432 seq455)',
  len(V1[V1.mois_cloture == '2026-11']) == 379 and abs(V1[V1.mois_cloture == '2026-11'].pnl_net_usd_S0.sum() + 0.432) < 0.01)
t('03 reconciliation novembre V2 (230 paniers, -0.930 seq459)',
  len(V2[V2.mois_cloture == '2026-11']) == 230 and abs(V2[V2.mois_cloture == '2026-11'].pnl_net_usd_S0.sum() + 0.930) < 0.01)
t('04 reconciliation janv-sept V1 (3728 paniers, -29.97 seq457) et V2 CI negatif',
  len(V1[V1.mois_cloture < '2026-11']) == 3728 and abs(V1[V1.mois_cloture < '2026-11'].pnl_net_usd_S0.sum() + 29.97) < 0.05 and
  V2[V2.mois_cloture < '2026-11'].pnl_net_usd_S0.sum() < 0)
mo = pd.read_csv(OUT / 'MONTHLY_PERFORMANCE_COMPARISON.csv')
s1 = mo[mo.moteur == 'V1'].resultat_net_S0.sum(skipna=True); s2 = mo[mo.moteur == 'V2-F2'].resultat_net_S0.sum(skipna=True)
t('05 coherence mensuel = global (V1 et V2)',
  abs(s1 - V1.pnl_net_usd_S0.sum()) < 0.05 and abs(s2 - V2.pnl_net_usd_S0.sum()) < 0.05)
gaps = pd.read_csv(OUT / 'DATA_GAPS_2026.csv')
t('06 octobre declare GAP et aucun panier en octobre',
  (gaps.gap.str.contains('octobre')).any() and not (V1.mois_cloture == '2026-10').any() and not (V2.mois_cloture == '2026-10').any())
man_ok = (OUT / 'chart_equity_drawdown.png').exists()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('07 chaine valide + graphique equity/drawdown present', verify()[0] and man_ok)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
