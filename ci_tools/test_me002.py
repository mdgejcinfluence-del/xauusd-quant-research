#!/usr/bin/env python3
"""Tests ME-002.1 (executes)."""
import pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME002_DISLOCATION_001'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
E = pd.read_csv(OUT / 'ME002_EPISODE_CATALOG.csv')
t('01 catalogue: 4272 episodes, decouverte+validation x 3 seuils', len(E) == 4272 and E.groupby(['segment', 'seuil_bp']).ngroups == 15)
N = pd.read_csv(OUT / 'ME002_NET_EDGE_ANALYSIS.csv'); N = N[N.base == 'edge_central_bp']
t('02 resultat central: esperance nette negative dans les 6 combinaisons', (N.groupby(['groupe', 'seuil_bp']).esperance_bp.first() < 0).all())
t('03 phenomene de resorption present (>40% partout)', (E.groupby(['segment', 'seuil_bp']).resorbe.mean() > 0.4).all())
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('04 registre ME-002 REJECTED (forme testee) + chaine valide', 'REJECTED sous la forme testée' in reg and verify()[0])
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
