#!/usr/bin/env python3
"""Tests ME-003.1 (executes)."""
import pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME003_IMPULSE_001'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
E = pd.read_csv(OUT / 'ME003_EPISODE_CATALOG.csv')
t('01 catalogue: episodes sur 5 segments x 3 seuils', E.groupby(['segment', 'seuil_bp']).ngroups == 15 and len(E) > 4000)
N = pd.read_csv(OUT / 'ME003_NET_EDGE_ANALYSIS.csv')
t('02 resultat central: esperance negative aux 18 combinaisons (groupe x seuil x horizon)', (N.esperance_bp < 0).all() and len(N) == 18)
t('03 continuation de trajectoire presente (>55% partout)', (E.groupby(['segment', 'seuil_bp']).continuation_1h.mean() > 0.55).all())
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('04 registre ME-003 REJECTED (forme testee) + chaine valide', reg.count('REJECTED sous la forme testée') >= 2 and verify()[0])
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
