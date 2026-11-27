#!/usr/bin/env python3
"""Tests STRATEGY-DISCOVERY-001 (executes, pas annonces)."""
import hashlib, json, pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/STRATEGY_DISCOVERY_001'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
t('01 V1 gele intact', json.loads((OUT/'V2_DATA_CONTRACT.json').read_text())['reference_V1_gelee']['sha256_colorful_replay.py']==hashlib.sha256((R/'ci_tools/colorful_replay.py').read_bytes()).hexdigest())
C=pd.read_csv(OUT/'MODEL_COMPARISON_V1_V2.csv')
t('02 comparaison V1/V2 produite sur memes donnees', set(C.modele)=={'V1','V2_F2'} and C.paniers.iloc[0]==379)
B=pd.read_csv(OUT/'NOV_BASKET_TRAJECTORIES.csv')
t('03 trajectoires nov. = 379 paniers reconcilies', len(B)==379)
r=json.loads((OUT/'DIAGNOSTIC_RESUME.json').read_text())
t('04 contrefactuel: sous-ensemble evalue et censure documentee', r['cf_evalues']==14 and r['nov_3pos']==140)
reg=pd.read_csv(OUT/'STRATEGY_HYPOTHESIS_REGISTER.csv')
t('05 registre: statuts autorises seulement', set(reg.statut) <= {'PROPOSED','SUPPORTED','REFUTED','NOT_TESTABLE','NEEDS_INDEPENDENT_VALIDATION','CAUSAL_EFFECT_NOT_IDENTIFIED'})
t('06 hypotheses refutees conservees (S5-S7)', (reg[reg.id.isin(['S5','S6','S7'])].statut=='REFUTED').all())
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
t('07 chaine registre valide', verify()[0])
t('08 livrables presents', all((OUT/f).exists() for f in ['STRATEGY_DISCOVERY_FINAL_REPORT.md','V2_STRATEGY_SPECIFICATION.md','V2_DATA_CONTRACT.json','INDEPENDENT_VALIDATION_PLAN.md','UNRESOLVED_QUESTIONS.md']))
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
