#!/usr/bin/env python3
"""Tests DIRR-003 (executes)."""
import pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/DEEP_INVENTORY_RECOVERY_003'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
T=pd.read_csv(OUT/'REAL_BASKET_TRAJECTORY_ANALYSIS.csv')
t('01 cinq paniers reels reconstruits', len(T)==5 and set(T.panier)==set('ABCDE'))
t('02 regimes: 3 recovery / 2 immediats', (T.regime_observe=='INVENTORY_RECOVERY').sum()==3 and (T.regime_observe=='IMMEDIATE').sum()==2)
t('03 paniers recovery majoritairement sous le PWA (>60%)', (T[T.regime_observe=='INVENTORY_RECOVERY'].temps_sous_pwa_pct>60).all())
t('04 trajectoires tick archivees', all((OUT/f'TRAJECTORY_{k}.csv').exists() for k in 'ABCDE'))
C=pd.read_csv(OUT/'COUNTERFACTUAL_SCENARIOS.csv')
t('05 contrefactuels a horizon commun presents', (C.horizon=='cloture reelle (meme instant)').sum()>=5)
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
t('06 chaine valide, moteurs geles intouches (aucune ecriture)', verify()[0])
t('07 18 livrables presents', len([f for f in ['MASTER_DIRR_REPORT.md','REAL_BASKET_TRAJECTORY_ANALYSIS.csv','INVENTORY_STATE_RECONSTRUCTION.md','WEIGHTED_AVERAGE_PRICE_ANALYSIS.md','RECOVERY_MECHANISM_ANALYSIS.md','IMMEDIATE_CAPTURE_ANALYSIS.md','POSITION_SIZING_IDENTIFICATION.md','EXIT_MECHANISM_IDENTIFICATION.md','DYNAMIC_STATE_MACHINE.md','COUNTERFACTUAL_SCENARIOS.csv','TAIL_RISK_AND_EXPOSURE_REPORT.md','DIRR_ARCHITECTURE.md','DIRR_REPLAY_REPORT.md','BEHAVIORAL_FIDELITY_SCORECARD.csv','ECONOMIC_PERFORMANCE_COMPARISON.csv','UNRESOLVED_MECHANISMS.md','FINAL_SCIENTIFIC_CONCLUSIONS.md','TECHNICAL_TEST_REPORT.md'] if (OUT/f).exists()])==18)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
