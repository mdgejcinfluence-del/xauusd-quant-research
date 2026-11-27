#!/usr/bin/env python3
"""Tests EMI-006 (exécutés) : moteur causal + résultats d'identifiabilité."""
import json, pathlib, sys
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
R = HERE.parents[2]
sys.path.insert(0, str(HERE))
from EXIT_MECHANISM_ENGINE import ExitEngine

ok = []
def t(n, c):
    ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

# 1. causalité moteur : sur série synthétique, aucune décision avant le seuil
syn = pd.DataFrame({'ts': pd.date_range('2026-01-01', periods=200, freq='100ms'),
                    'mid': 100.0, 'pwa': 100.0,
                    'pnl_latent_bp': [-1.0] * 100 + [1.0] * 100})
log = ExitEngine(family='P', persistence_s=5).run(syn)
exe = log[log.decision == 'EXIT_EXECUTED']
t('01 moteur P: execution seulement apres 5s favorables continues',
  len(exe) == 1 and (exe.ts.iloc[0] - syn.ts.iloc[100]).total_seconds() >= 5)
# 2. invalidation réinitialise le compteur
syn2 = syn.copy(); syn2.loc[120:129, 'pnl_latent_bp'] = -1.0
log2 = ExitEngine(family='P', persistence_s=5).run(syn2)
t('02 invalidation -> STATE_INVALIDATED present et compteur reinitialise',
  (log2.decision == 'STATE_INVALIDATED').any() and
  (log2[log2.decision == 'EXIT_EXECUTED'].ts.iloc[0] - syn2.ts.iloc[130]).total_seconds() >= 5)
# 3. famille U n'autorise jamais d'exécution (mécanisme non identifié)
tr = pd.read_csv(R / 'docs/checkpoints/DEEP_INVENTORY_RECOVERY_003/TRAJECTORY_A.csv', parse_dates=['ts'])
logU = ExitEngine(family='U').run(tr)
t('03 famille U: aucune execution simulee presentee comme reelle',
  not (logU.decision == 'EXIT_EXECUTED').any() and (logU.decision == 'EXIT_NOT_AUTHORIZED').any())
# 4. aucune intersection de persistance commune (grille préenregistrée)
ci = pd.read_csv(HERE / 'EXIT_COMMON_INTERVALS.csv')
t('04 persistance commune: intersection vide sur toute la grille (35 combinaisons)',
  len(ci) == 35 and not ci.intersection_non_vide.any())
# 5. cadence : seule la cadence triviale 1s est commune (ancrage ouverture)
cad = json.loads((HERE / 'EMI006_CADENCE.json').read_text())
t('05 cadence fixe ancree ouverture: commune = {1s} seulement (triviale)',
  cad['cadences_communes_ancrage_ouverture'] == [1])
# 6. C clôture hors état favorable theta=0 (contre-exemple persistance stricte)
rob = pd.read_csv(HERE / 'EXIT_ROBUSTNESS_TESTS.csv')
cflag = rob[(rob.panier == 'C') & (rob.test.str.contains('cloture dans etat'))].valeur.iloc[0]
t('06 panier C: cloture hors etat favorable (theta=0) documentee', str(cflag).lower() == 'false')
# 7. chaînes et livrables
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
need = ['EMI_006_EXECUTIVE_REPORT.md', 'EMI_006_METHODOLOGY.md', 'EXIT_TIMELINE_A_E.csv',
        'EXIT_STATE_TRANSITIONS.csv', 'EXIT_MODEL_COMPARISON.csv', 'EXIT_PARAMETER_COMPATIBILITY.csv',
        'EXIT_IDENTIFIABILITY_MATRIX.csv', 'EXIT_CAUSAL_REPLAY.csv', 'EXIT_FALSE_TRIGGER_ANALYSIS.csv',
        'EXIT_ROBUSTNESS_TESTS.csv', 'EXIT_MECHANISM_ENGINE.py', 'EXIT_ENGINE_TESTS.py',
        'DATA_PROVENANCE.json', 'REPRODUCIBILITY.md', 'FINAL_VERDICT.md']
t('07 chaine valide + 15 livrables obligatoires presents',
  verify()[0] and all((HERE / f).exists() for f in need))
print(f"\n{sum(ok)}/{len(ok)} tests PASS")
sys.exit(0 if all(ok) else 1)
