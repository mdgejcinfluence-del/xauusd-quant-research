#!/usr/bin/env python3
"""Scoring SHADOW hors ligne: applique la regle preenregistree (deadline 120 min)
et la reference 8 h aux evenements reconstruits depuis les cotations collectees.
Aucun ordre. Comptabilite 19-B: spread une fois, S0/S1/S2, S2 principal.
Implementation a completer lors de l'activation (reconstruction M15 identique a
ci_tools/phase24b_engine.py, predictions gelees via coefficients 24-C)."""
import json, pathlib
CONTRAT = json.loads((pathlib.Path(__file__).parents[1] / 'SHADOW_DATA_CONTRACT.json').read_text())
print('Contrat charge:', CONTRAT['contrat'], '| borne:', CONTRAT['borne_prospective_utc'])
print('Statut: PRET, NON ACTIVE (aucune source de flux connectee).')
