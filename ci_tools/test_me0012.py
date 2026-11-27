#!/usr/bin/env python3
"""Tests ME-001.2 (executes)."""
import pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_NONRECOVERY_002'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

E = pd.read_csv(OUT / 'ME001_EPISODE_TRAJECTORIES.csv')
vc = E.raison_fin.value_counts()
t('01 issues coherentes: total = recuperes + 24h + censures',
  len(E) == vc.sum() and set(vc.index) == {'recupere', 'horizon_24h', 'censure_fin_partition'})
t('02 censures jamais classees recuperees ni echecs 24h', (E[E.raison_fin == 'censure_fin_partition'].recupere_24h == False).all())
X = pd.read_csv(OUT / 'ME001_EXIT_FAMILY_COUNTERFACTUALS.csv')
base = X[X.famille.str.startswith('baseline')].set_index('groupe').esperance_bp
others = X[~X.famille.str.startswith('baseline')]
t('03 resultat central: toutes les familles < baseline (decouverte et validation)',
  all(others[others.groupe == g].esperance_bp.max() < base[g] for g in ('decouverte', 'validation')))
D = pd.read_csv(OUT / 'ME001_DETECTION_PERFORMANCE.csv')
t('04 drapeau preenregistre: sensibilite <= 10% partout (refute comme detecteur)', (D.sensibilite <= 0.10).all())
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('05 registre SIGNATURE_DETECTED maintenu + chaine valide', 'SIGNATURE_DETECTED' in reg and verify()[0])
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
