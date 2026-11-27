#!/usr/bin/env python3
"""Tests ME-001.3 (executes)."""
import pathlib, sys
import pandas as pd, numpy as np
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_ENTRY_RISK_003'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

F = pd.read_csv(OUT / 'ME001_PRE_ENTRY_RISK_FEATURES.csv')
A = F[F.vol15_bp.notna()]
t('01 fait mathematique: esperance invariante par exposition constante (x2)',
  abs((2 * A.edge_baseline_bp).mean() - 2 * A.edge_baseline_bp.mean()) < 1e-9 and abs(A.edge_baseline_bp.mean()) > 0)
P = pd.read_csv(OUT / 'ME001_EXPOSURE_POLICY_COMPARISON.csv').set_index(['groupe', 'politique'])
t('02 P2 > P0 en PF dans les deux groupes',
  all(P.loc[(g, 'P2 exclusion vol>Q75 decouverte'), 'PF'] > P.loc[(g, 'P0 constante'), 'PF'] for g in ('decouverte', 'validation')))
t('03 P2 ameliore ES95 vs P0 dans les deux groupes',
  all(P.loc[(g, 'P2 exclusion vol>Q75 decouverte'), 'ES95_bp'] > P.loc[(g, 'P0 constante'), 'ES95_bp'] for g in ('decouverte', 'validation')))
t('04 episodes extremes conserves (profondeur min <= -500bp)', F.profondeur_max_bp.min() <= -500)
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('05 registre SIGNATURE_DETECTED + chaine valide + moteurs geles presents',
  'SIGNATURE_DETECTED' in reg and verify()[0] and (R / 'ci_tools/colorful_replay.py').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
