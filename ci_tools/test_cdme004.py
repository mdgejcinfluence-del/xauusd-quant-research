#!/usr/bin/env python3
"""Tests CDME-004 (executes)."""
import pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/COMPLETE_DECISION_MECHANISM_004'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
T=pd.read_csv(OUT/'EXIT_TRAJECTORY_ANALYSIS.csv')
t('01 fenetres pre-cloture pour les 5 paniers', len(T)==5)
t('02 trait commun: PnL en hausse sur 300s aux 5 clotures', (T.pnl_moins300s_bp>0).all())
t('03 clotures pres du sommet local 300s (>-3bp)', (T.dist_au_sommet300_bp>-3).all())
t('04 A cloture en acceleration (contre-exemple epuisement consigne)', T[T.panier=='A'].pnl_moins30s_bp.iloc[0]>3)
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
t('05 chaine valide, moteurs geles intouches', verify()[0])
t('06 19 livrables presents', len([f for f in ['MASTER_CDME_REPORT.md','EXIT_TRIGGER_DISCOVERY.md','EXIT_TRAJECTORY_ANALYSIS.csv','POSITION_SIZING_IDENTIFICATION.md','POST_ENTRY_REGIME_DISCOVERY.md','PATIENCE_MECHANISM_ANALYSIS.md','RECOVERY_FUNCTION_IDENTIFICATION.md','INITIAL_ENTRY_MECHANISM.md','INVERSE_PARAMETER_IDENTIFICATION.md','COMPETING_MODEL_REGISTER.csv','DYNAMIC_SYSTEM_SPECIFICATION.md','DIRR_004_ARCHITECTURE.md','DIRR_004_REPLAY_REPORT.md','BEHAVIORAL_FIDELITY_COMPARISON.csv','ECONOMIC_PERFORMANCE_COMPARISON.csv','RISK_AND_FAILURE_SCENARIOS.md','UNIDENTIFIED_PARAMETERS.md','FINAL_STRATEGY_RECONSTRUCTION.md','TECHNICAL_TEST_REPORT.md'] if (OUT/f).exists()])==19)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
