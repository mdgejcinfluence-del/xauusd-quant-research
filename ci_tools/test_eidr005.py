#!/usr/bin/env python3
"""Tests EIDR-005 (executes)."""
import pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/EXIT_INTELLIGENCE_005'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
T=pd.read_csv(OUT/'EXIT_EVENT_HIGH_RESOLUTION_ANALYSIS.csv')
t('01 cinq evenements de sortie analyses', len(T)==5)
import ast
def ecart(cell):
    try: return ast.literal_eval(cell)[1]
    except Exception: return None
e=[ecart(T.R_PWA.iloc[i]) for i in range(5)]
t('02 premier retour PWA toujours trop tot (ecarts < 0)', all(x is not None and x<0 for x in e))
C=pd.read_csv(OUT/'COUNTERFACTUAL_EXIT_COMPARISON.csv')
t('03 premiers passages classes REFUTED, famille etat+persistance CANDIDATE', (C[C.regle.str.startswith('R_')].statut.eq('REFUTED')).all() and C.iloc[-1].statut=='CANDIDATE')
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
t('04 chaine valide, moteurs geles intouches', verify()[0])
t('05 21 livrables presents', len([f for f in ['MASTER_EXIT_INTELLIGENCE_REPORT.md','FIVE_BASKET_EXIT_RECONSTRUCTION.csv','EXIT_EVENT_HIGH_RESOLUTION_ANALYSIS.csv','LOCAL_HIGH_SIGNATURE_ANALYSIS.md','EXIT_HYPOTHESIS_REGISTER.csv','EXIT_DECISION_FUNCTION_SPECIFICATION.md','RECOVERY_EXIT_MECHANISM.md','IMMEDIATE_CAPTURE_EXIT_MECHANISM.md','PATIENCE_ENGINE_SPECIFICATION.md','POSITION_SIZING_AND_INVENTORY_CONSTRAINTS.md','HIDDEN_STATE_VARIABLE_ANALYSIS.md','INVERSE_PARAMETER_IDENTIFICATION.csv','CAUSAL_EXIT_ENGINE_SPECIFICATION.md','COUNTERFACTUAL_EXIT_COMPARISON.csv','COMPLETE_DYNAMIC_SYSTEM_ARCHITECTURE.md','EXIT_FIDELITY_SCORECARD.csv','ECONOMIC_PERFORMANCE_COMPARISON.csv','RISK_AND_FAILURE_ANALYSIS.md','UNIDENTIFIED_EXIT_PARAMETERS.md','FINAL_STRATEGY_RECONSTRUCTION.md','TECHNICAL_TEST_REPORT.md'] if (OUT/f).exists()])==21)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
