#!/usr/bin/env python3
"""Tests mission fondatrice 009: gouvernance presente, garde-fou demontre, registre sain."""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[1]
G = R / 'docs/governance'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

files = ['META_ALPHA_CONSTITUTION.md', 'META_ALPHA_RESEARCH_DOCTRINE.md', 'META_ALPHA_DRIFT_GUARD.md',
         'META_ALPHA_MODEL_REGISTRY.md', 'META_ALPHA_DECISION_LOG.md', 'META_ALPHA_FOUNDATION_STATUS.md']
t('01 six fichiers de gouvernance presents', all((G / f).exists() for f in files))
const = (G / 'META_ALPHA_CONSTITUTION.md').read_text()
t('02 constitution: modele economique comme unite + trois questions + interdictions',
  'modèle économique' in const and 'QUEL MODÈLE ÉCONOMIQUE' in const.upper() and 'Interdictions absolues' in const)
guard = (G / 'META_ALPHA_DRIFT_GUARD.md').read_text()
t('03 garde-fou: 4 controles et 4 niveaux presents',
  all(k in guard for k in ('Contrôle A', 'Contrôle B', 'Contrôle C', 'Contrôle D', 'VERT', 'JAUNE', 'ORANGE', 'ROUGE')))
t('04 garde-fou demontre sur exemples classes (VERT, ORANGE, ROUGE au moins)',
  guard.count('**VERT**') >= 1 and guard.count('**ORANGE') >= 1 and guard.count('**ROUGE**') >= 1)
reg = (G / 'META_ALPHA_MODEL_REGISTRY.md').read_text()
t('05 registre: ME-001 non valide, V1/V2 rejetes comme exploitations',
  'ME-001' in reg and 'HYPOTHESIS' in reg and 'REJECTED comme' in reg and 'VALIDATED' not in reg.split('ME-001')[1].split('##')[0].replace('NON VALIDÉ', '').replace('non validé', ''))
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('06 chaine valide et moteurs geles presents', verify()[0] and (R / 'ci_tools/colorful_replay.py').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
