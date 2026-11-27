#!/usr/bin/env python3
"""Tests scientifiques CTRS-007 (executes, pas de simple presence)."""
import hashlib, json, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/COMPLETE_TRADING_SYSTEM_RECONSTRUCTION_007'
SRC = R / 'docs/checkpoints/DEEP_INVENTORY_RECOVERY_003'
EMI = R / 'docs/checkpoints/EXIT_MECHANISM_IDENTIFICATION_006'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

# 1. PWA finals et PnL de cloture recalcules depuis les trajectoires gelees
real = pd.read_csv(SRC / 'REAL_BASKET_TRAJECTORY_ANALYSIS.csv').set_index('panier')
good = True
for b in 'ABCDE':
    df = pd.read_csv(SRC / f'TRAJECTORY_{b}.csv', parse_dates=['ts'])
    good &= abs(df.pwa.iloc[-1] - real.loc[b, 'pwa_final']) < 0.02
    good &= abs(df.pnl_latent_bp.iloc[-1] - real.loc[b, 'ecart_cloture_vs_pwa_bp']) < 0.01
t('01 PWA finals et ecarts de cloture des 5 paniers reproduits depuis les trajectoires', good)
# 2. Contre-exemple C reproduit
dfc = pd.read_csv(SRC / 'TRAJECTORY_C.csv')
t('02 panier C: cloture sous le PWA (-0.25bp) reproduite', abs(dfc.pnl_latent_bp.iloc[-1] + 0.25) < 0.01)
# 3. Refutations EMI-006 reproduites (persistance + cadence)
ci = pd.read_csv(EMI / 'EXIT_COMMON_INTERVALS.csv')
cad = json.loads((EMI / 'EMI006_CADENCE.json').read_text())
t('03 persistance commune vide (35) et cadence commune={1s}', len(ci) == 35 and not ci.intersection_non_vide.any() and cad['cadences_communes_ancrage_ouverture'] == [1])
# 4. Trois horloges: resolution tick autour des clotures <= 0.25s (dernier intervalle)
gaps = []
for b in 'ABCDE':
    df = pd.read_csv(SRC / f'TRAJECTORY_{b}.csv', parse_dates=['ts'])
    gaps.append(df.ts.diff().dt.total_seconds().iloc[-1])
t('04 horloges non separables: dernier intervalle inter-tick <=0.25s sur 5/5', max(gaps) <= 0.25)
# 5. Registre: statuts refutes presents, aucun verdict A revendique
reg = pd.read_csv(OUT / 'COMPLETE_KNOWLEDGE_REGISTER.csv')
verdict = (OUT / 'FINAL_SCIENTIFIC_VERDICT.md').read_text()
t('05 registre avec REFUTED documentes et verdict B (pas de A revendique)',
  (reg.statut.str.contains('REFUTED')).sum() >= 4 and 'VERDICT B' in verdict)
# 6. Manifeste verifiable
man = json.loads((OUT / 'MANIFEST_SHA256.json').read_text())
integ = all(hashlib.sha256((OUT / k).read_bytes()).hexdigest() == v['sha256'] for k, v in man.items())
need = ['CTRS_007_EXECUTIVE_REPORT.md','COMPLETE_KNOWLEDGE_REGISTER.csv','EVIDENCE_AND_IDENTIFIABILITY_MATRIX.csv','ENTRY_MECHANISM_FINAL.md','POSITION_SIZING_FINAL.md','REINFORCEMENT_MECHANISM_FINAL.md','INVENTORY_AND_RECOVERY_FINAL.md','EXIT_MECHANISM_FINAL.md','RISK_MODEL_FINAL.md','ECONOMIC_RECONSTRUCTION_FINAL.md','FULL_SYSTEM_ARCHITECTURE.md','FULL_SYSTEM_DATA_CONTRACT.json','MODEL_COMPATIBILITY_MATRIX.csv','REAL_VS_SIMULATED_CONFRONTATION.csv','CAUSAL_REPLAY_RESULTS.csv','IDENTIFIABILITY_BOUNDARY.md','MISSING_EVIDENCE_REGISTER.csv','FINAL_SCIENTIFIC_VERDICT.md','FINAL_TEST_REPORT.md','DATA_PROVENANCE.json','MANIFEST_SHA256.json','REPRODUCIBILITY.md']
t('06 manifeste SHA-256 verifiable + 22 livrables presents', integ and all((OUT / f).exists() for f in need))
# 7. Chaine + moteurs geles presents
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('07 chaine valide, moteurs V1/V2 geles presents', verify()[0] and (R/'ci_tools/colorful_replay.py').exists() and (R/'ci_tools/colorful_replay_v2.py').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
