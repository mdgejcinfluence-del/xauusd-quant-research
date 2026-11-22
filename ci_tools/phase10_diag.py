"""Diagnostic d'acces aux sources IS (aucune donnee exploitee, aucun secret affiche)."""
import json, os, subprocess, sys

def log(*a): print(*a, flush=True)

inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
kstate = json.loads(open('reports/meta_alpha/kaggle_migration/STATE.json').read())
tok = os.environ.get('KAGGLE_API_TOKEN', '')
log('token present:', bool(tok), 'longueur:', len(tok))
try:
    import requests
    url = 'https://www.kaggle.com/api/v1/datasets/download/shalom5123/xauusd-is-b01'
    for nom, hdrs, auth in [('bearer', {'Authorization': f'Bearer {tok}'}, None),
                            ('basic', {}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
        try:
            r = requests.get(url, headers=hdrs, auth=auth, timeout=120, stream=True)
            log('kaggle direct', nom, '->', r.status_code, r.headers.get('content-type'), r.headers.get('content-length'))
            r.close()
        except Exception as e:
            log('kaggle direct', nom, 'ERREUR', str(e)[:200])
except Exception as e:
    log('requests indisponible', str(e)[:200])
try:
    p = [x for x in inv if x.get('drive_id')][0]
    log('test Drive partition:', p['name'], 'taille attendue:', p.get('file_bytes'))
    rc = subprocess.run(['gdown', '-q', '--output', '/tmp/diag_part.parquet', p['drive_id']]).returncode
    ok = os.path.exists('/tmp/diag_part.parquet')
    log('gdown rc:', rc, 'fichier present:', ok, 'taille:', os.path.getsize('/tmp/diag_part.parquet') if ok else None)
except Exception as e:
    log('Drive ERREUR', str(e)[:200])
sys.exit(0)
