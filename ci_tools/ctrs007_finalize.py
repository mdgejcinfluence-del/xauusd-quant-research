#!/usr/bin/env python3
"""CTRS-007: data contract + manifest (hashes) generation."""
import hashlib, json, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/COMPLETE_TRADING_SYSTEM_RECONSTRUCTION_007'
mods = ['MARKET_STATE_ENGINE','ENTRY_SIGNAL_ENGINE','ENTRY_PERMISSION_ENGINE','POSITION_SIZING_ENGINE',
        'REINFORCEMENT_ENGINE','INVENTORY_ENGINE','WEIGHTED_AVERAGE_ENGINE','RECOVERY_STATE_ENGINE',
        'EXIT_PERMISSION_ENGINE','EXIT_EXECUTION_ENGINE','RISK_CONTROL_ENGINE','ECONOMIC_ACCOUNTING_ENGINE']
levels = {'MARKET_STATE_ENGINE':'STRONGLY_SUPPORTED (calcul)','ENTRY_SIGNAL_ENGINE':'CANDIDATE (H3)',
 'ENTRY_PERMISSION_ENGINE':'CANDIDATE (F2)','POSITION_SIZING_ENGINE':'NOT_IDENTIFIED (famille bornee)',
 'REINFORCEMENT_ENGINE':'STRONGLY_SUPPORTED (intervalles observes)','INVENTORY_ENGINE':'STRONGLY_SUPPORTED (mecanique)',
 'WEIGHTED_AVERAGE_ENGINE':'DEMONTRE (arithmetique)','RECOVERY_STATE_ENGINE':'STRONGLY_SUPPORTED (description)',
 'EXIT_PERMISSION_ENGINE':'NOT_IDENTIFIED (3 familles equivalentes)','EXIT_EXECUTION_ENGINE':'NOT_IDENTIFIED (horloges non separables)',
 'RISK_CONTROL_ENGINE':'NOT_IDENTIFIED (aucun stop observe)','ECONOMIC_ACCOUNTING_ENGINE':'DEMONTRE pour nos moteurs (negatif)'}
contract = {'version':'CTRS-007','modules':[{'nom':m,'niveau_identification':levels[m],
  'entrees':['ticks passes','etat panier courant'],'sorties':['etat/decisions horodatees'],
  'parametres':'voir registre CTRS-007; aucun parametre invente pour les modules NOT_IDENTIFIED'} for m in mods],
  'invariants':['aucun look-ahead','spread compte une fois','reel/simule separes','parametres traces']}
(OUT/'FULL_SYSTEM_DATA_CONTRACT.json').write_text(json.dumps(contract,indent=1,ensure_ascii=False))
man = {}
for f in sorted(OUT.iterdir()):
    if f.is_file() and f.name != 'MANIFEST_SHA256.json':
        man[f.name] = {'taille': f.stat().st_size, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()}
(OUT/'MANIFEST_SHA256.json').write_text(json.dumps(man, indent=1))
print('modules:', len(mods), '| fichiers manifestes:', len(man))
