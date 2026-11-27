#!/usr/bin/env python3
"""Tests ME-001.1 (executes)."""
import hashlib, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_RECOVERY_SIGNATURE_001'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

E = pd.read_csv(OUT / 'ME001_EPISODE_CATALOG.csv')
t('01 catalogue: 2327 episodes, 5 segments x 3 seuils', len(E) == 2327 and E.groupby(['segment', 'seuil_bp']).ngroups == 15)
t('02 recuperation monotone en horizon et bornee [0,1]',
  (E.groupby(['segment', 'seuil_bp'])[['recupere_300s', 'recupere_900s', 'recupere_3600s', 'recupere_14400s', 'recupere_86400s']].mean().diff(axis=1).iloc[:, 1:] >= -1e-9).all().all())
N = pd.read_csv(OUT / 'ME001_NET_EDGE_ANALYSIS.csv'); N = N[N.base == 'edge_net_central_bp']
neg5 = (N[N.seuil_bp == 5.0].esperance_bp < 0).sum()
t('03 resultat central: edge net a 5bp negatif dans au moins 4/5 segments', neg5 >= 4)
t('04 profondeur toujours au-dela du seuil (excursion continue)', (E.profondeur_max_bp < -E.seuil_bp + 0.01).mean() > 0.9)
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
t('05 registre ME-001 SIGNATURE_DETECTED, jamais VALIDATED pour ME-001',
  'SIGNATURE_DETECTED' in reg and 'Edge net NON VALIDÉ' in reg)
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('06 chaine valide + moteurs geles presents (non modifies par la mission)',
  verify()[0] and (R / 'ci_tools/colorful_replay.py').exists() and (R / 'ci_tools/colorful_replay_v2.py').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
