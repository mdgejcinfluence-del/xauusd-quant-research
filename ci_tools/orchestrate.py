"""Orchestrateur de continuite: lit les checkpoints, decide la prochaine action
AUTORISEE, la journalise. Ne franchit jamais un gate sensible (Holdout, reel, depense)."""
import json, pathlib, datetime
log = pathlib.Path('reports/meta_alpha/ORCHESTRATION_LOG.md')
def read(p):
    try: return json.loads(pathlib.Path(p).read_text())
    except Exception: return None
p3 = read('reports/meta_alpha/p3/P3_001_RESULTS.json')
p3s = read('reports/meta_alpha/p3/STATE.json')
if p3: action = "P3-001 termine: Arena doit produire le rapport de gate P3 (statistiques, FDR) puis, si criteres satisfaits, preenregistrer P4. Aucune action automatique au-dela."
elif p3s and p3s.get('pass') != 'DONE': action = "P3-001 en cours/interrompu: relancer le workflow p3-001.yml (reprise par STATE.json)."
else: action = "P3-001 non demarre: lancer le workflow p3-001.yml."
stamp = datetime.datetime.utcnow().isoformat()+'Z'
with open(log,'a') as f: f.write(f"\n- {stamp} — {action}\n")
print(action)
