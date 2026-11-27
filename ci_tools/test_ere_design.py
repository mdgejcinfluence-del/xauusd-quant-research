#!/usr/bin/env python3
"""Tests conception ERE: livrables, diagrammes, coherence, aucun travail interdit."""
import pathlib, sys
R = pathlib.Path(__file__).resolve().parents[1]
D = R / 'docs/architecture/META_ALPHA_ERE'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

docs = ['VISION_AND_OBJECTIVES.md','FUNCTIONAL_ARCHITECTURE.md','SCIENTIFIC_ARCHITECTURE.md','KNOWLEDGE_AND_SOURCE_CATALOG.md','HYPOTHESIS_ENGINE_DESIGN.md','AUTONOMOUS_EXPERIMENT_ENGINE.md','MARKET_DATA_DISCOVERY_ENGINE.md','ECONOMIC_IDENTIFICATION_ENGINE.md','INDEPENDENT_STRATEGY_ENGINEERING.md','VALIDATION_AND_PORTFOLIO_ENGINE.md','DATA_CONTRACTS.md','SYSTEM_INTERFACES.md','SECURITY_AND_GOVERNANCE.md','TECHNICAL_ARCHITECTURE.md','IMPLEMENTATION_ROADMAP.md','OPEN_QUESTIONS_AND_DECISIONS.md']
t('01 seize documents de conception presents', all((D / f).exists() for f in docs))
dias = sorted((D / 'diagrams').glob('*.svg'))
t('02 cinq diagrammes SVG presents et valides (balise svg)', len(dias) == 5 and all('<svg' in f.read_text() and '</svg>' in f.read_text() for f in dias))
arch = (D / 'FUNCTIONAL_ARCHITECTURE.md').read_text()
t('03 neuf modules A-I definis', all(f'{m}.' in arch for m in 'ABCDEFGHI'))
road = (D / 'IMPLEMENTATION_ROADMAP.md').read_text()
t('04 aucune implementation demarree: roadmap conditionnee a la validation du fondateur', 'Aucune' in road and 'validation du fondateur' in road)
strat = (D / 'INDEPENDENT_STRATEGY_ENGINEERING.md').read_text()
t('05 porte du module H: aucun modele ne la franchit aujourd hui (ME-001 en attente)', 'aucun modèle ne franchit encore cette porte' in strat)
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('06 chaine valide + moteurs geles presents (non touches)', verify()[0] and (R / 'ci_tools/colorful_replay.py').exists() and (R / 'ci_tools/colorful_replay_v2.py').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
