#!/usr/bin/env python3
"""Tests AESR-002 (executes)."""
import json, pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/AUTONOMOUS_ECONOMIC_RECONSTRUCTION_002'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
res=json.loads((OUT/'MECHANISM_RESULTS.json').read_text())
t('01 E1 simulees: n=379 reconcilie', res['E1_simulees']['fwd300s']['n']==379)
t('02 signal sans avantage directionnel franc (|moy|<2bp)', abs(res['E1_simulees']['fwd300s']['moyenne_bp'])<2)
t('03 paniers reels longs sous l eau (>75% pour A/B/C)', all(res['E2_reelles'][k]['part_temps_sous_prix_entree_pct']>75 for k in 'ABC'))
t('04 esperance profil recalculee = +6.01', abs(res['E3_profil']['esperance_par_transaction_affichee_jpy']-6.01)<0.05)
reg=pd.read_csv(OUT/'COMPETING_MECHANISM_REGISTER.csv')
t('05 mecanismes concurrents avec statuts', len(reg)>=6 and 'REFUTED' in set(reg.statut.str.strip().str[:7]))
t('06 aucune affirmation market-making (NOT_IDENTIFIED)', (reg[reg.mecanisme.str.contains('Market making')].statut.str.contains('NOT_IDENTIFIED')).all())
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
import hashlib
t('07 chaine valide et moteurs geles intacts', verify()[0])
t('08 15 livrables presents', len([f for f in ['MASTER_RESEARCH_REPORT.md','ECONOMIC_MECHANISM_ANALYSIS.md','COMPETING_MECHANISM_REGISTER.csv','DYNAMIC_SYSTEM_RECONSTRUCTION.md','INVENTORY_AND_RISK_ANALYSIS.md','MARKET_MICROSTRUCTURE_LIMITATIONS.md','ENTRY_AND_EXIT_IDENTIFICATION.md','MODEL_FAMILY_COMPARISON.csv','RECONSTRUCTED_STRATEGY_SPECIFICATION.md','REPLAY_AND_FIDELITY_REPORT.md','ECONOMIC_PERFORMANCE_REPORT.md','ROBUSTNESS_AND_STRESS_TESTS.md','META_ALPHA_MULTI_TRADER_ARCHITECTURE.md','UNRESOLVED_IDENTIFICATION_PROBLEMS.md','FINAL_EVIDENCE_AND_VALIDATION_STATUS.md'] if (OUT/f).exists()])==15)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
