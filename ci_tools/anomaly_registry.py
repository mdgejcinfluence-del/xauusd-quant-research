"""Registre d'anomalies phenomenologiques (charte: pas d'item K sans 5 mesures).
Une anomalie est DESCRIPTIVE par defaut; elle ne devient 'candidat_predictif' que
par une decision explicite et justifiee, jamais automatiquement.
Champs obligatoires (refus si incomplet): identifiant, partitions sources, periode,
granularite, definition de la mesure, distribution/frequence, conditions
d'apparition, comportement de reference, ecart observe, incertitude/stabilite,
dependances, limites, hashes (code, configuration, donnees)."""
import json, hashlib, pathlib, sys

REQUIRED = ['anomaly_id','partitions_sources','periode','granularite','definition_mesure',
 'distribution_frequence','conditions_apparition','comportement_reference','ecart_observe',
 'incertitude_stabilite','dependances','limites','hash_code','hash_config','hash_donnees']
P = pathlib.Path('reports/meta_alpha/ANOMALY_REGISTRY.json')

def sha(path): return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

def register(a):
    missing=[k for k in REQUIRED if k not in a or a[k] in (None,'')]
    if missing: raise ValueError(f'anomalie refusee, champs manquants: {missing}')
    if a.get('statut') not in ('DESCRIPTIVE','CANDIDAT_PREDICTIF'):
        a['statut']='DESCRIPTIVE'
    d=json.loads(P.read_text()) if P.exists() else {'anomalies':[]}
    if any(x['anomaly_id']==a['anomaly_id'] for x in d['anomalies']):
        raise ValueError(f"identifiant deja present (immuable): {a['anomaly_id']}")
    d['anomalies'].append(a); P.write_text(json.dumps(d,indent=1,ensure_ascii=False))
    return a['anomaly_id']

if __name__=='__main__':
    # auto-test: une anomalie incomplete doit etre refusee, une complete acceptee (fichier temporaire)
    import tempfile, os
    tmp=pathlib.Path(tempfile.mktemp(suffix='.json')); P_orig=P
    globals()['P']=tmp
    try:
        register({'anomaly_id':'TEST-INCOMPLETE'})
        print('ECHEC: anomalie incomplete acceptee'); sys.exit(1)
    except ValueError as e:
        print('refus correct:', e)
    full={k:'x' for k in REQUIRED}; full['anomaly_id']='TEST-COMPLETE'
    register(full); print('acceptation correcte:', full['anomaly_id'], '| statut par defaut DESCRIPTIVE conserve')
    os.remove(tmp)
