#!/usr/bin/env python3
"""Tests DEEP-REVERSE-001 (executes)."""
import hashlib, pathlib, sys
import pandas as pd
R=pathlib.Path(__file__).resolve().parents[1]; OUT=R/'docs/checkpoints/DEEP_REVERSE_ENGINEERING_001'
ok=[]
def t(n,c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
reg=pd.read_csv(OUT/'COMPLETE_HYPOTHESIS_REGISTER.csv')
t('01 statuts autorises uniquement', set(reg.statut.str.strip()) <= {'OBSERVED','STRONGLY_SUPPORTED','CANDIDATE','NOT_IDENTIFIED','REFUTED','INSUFFICIENT_DATA','INDEPENDENTLY_VALIDATED'})
t('02 aucune regle declaree INDEPENDENTLY_VALIDATED a tort', not (reg.statut.str.strip()=='INDEPENDENTLY_VALIDATED').any())
h=(R/'docs/checkpoints/RE_ENTRY_007/source/myHF _ HFM Broker.html78.html').read_bytes()
t('03 HTML78 archive et empreinte conforme', hashlib.sha256(h).hexdigest()=='2e3a9e19d56cbfa9fe28c7fe275b0af7b7a8f3b579db623fe442c288ebddc210')
import json; pc=json.loads((OUT/'PREV_CANDLE_FEATURES.json').read_text())
t('04 bougie precedente: corps positif pour les 5 entrees reelles', all(v['corps_bp']>0 for v in pc.values()))
t('05 hypotheses refutees conservees', set(reg[reg.statut.str.strip()=='REFUTED'].id) >= {'H-SIZ-01','H-EXT-01','H-EXT-02','H-EXT-03','H-EXT-04'})
sys.path.insert(0,str(R/'ci_tools')); from ledger_chain import verify
t('06 chaine du registre valide; V1/V2 intouches', verify()[0])
t('07 15 livrables presents', len([f for f in ['MASTER_REVERSE_ENGINEERING_REPORT.md','SOURCE_AND_EVIDENCE_REGISTER.csv','COMPLETE_HYPOTHESIS_REGISTER.csv','ENTRY_ENGINE_SPECIFICATION.md','BASKET_MANAGER_SPECIFICATION.md','REINFORCEMENT_ENGINE_SPECIFICATION.md','POSITION_SIZING_SPECIFICATION.md','EXIT_ENGINE_SPECIFICATION.md','RISK_ENGINE_SPECIFICATION.md','COMPLETE_STRATEGY_ARCHITECTURE.md','MODEL_REPRODUCTION_REPORT.md','FIDELITY_SCORECARD.csv','UNRESOLVED_RULES_AND_BLOCKERS.md','INDEPENDENT_VALIDATION_PROTOCOL.md','TECHNICAL_TEST_REPORT.md'] if (OUT/f).exists()])==15)
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
