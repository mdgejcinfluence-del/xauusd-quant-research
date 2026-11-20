"""CAMPAGNE 2.3 - sonde d'acces minimale (gelee seq174). Aucun secret affiche."""
import json, os, pathlib, subprocess
OUT = pathlib.Path('reports/meta_alpha/campaign02_3'); OUT.mkdir(parents=True, exist_ok=True)
log = []
tok = os.environ.get('KAGGLE_API_TOKEN', '')
user = os.environ.get('KAGGLE_USERNAME', '')
# 1) Kaggle: listage seul
try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi(); api.authenticate()
    files = api.dataset_list_files('marioadh/xauusd-is-b01').files
    log.append(f'KAGGLE_API_LIST (auth compte + acces dataset + lecture fichiers): OK {len(files)} fichiers; premier={files[0].name if files else None}')
except Exception as e:
    log.append(f'KAGGLE_API_LIST: ECHEC {type(e).__name__} {str(e)[:120]}')
try:
    import requests
    url = 'https://www.kaggle.com/api/v1/datasets/list/marioadh/xauusd-is-b01'
    ok = False
    for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None), ({}, (user, tok))]:
        r = requests.get(url, headers=hdrs, auth=auth, timeout=60)
        log.append(f'KAGGLE_HTTPS_LIST ({ "bearer" if hdrs else "basic" }): HTTP {r.status_code} corps={r.text[:200].replace(chr(10)," ")}')
        if r.status_code == 200: ok = True; break
    log.append(f'KAGGLE_HTTPS_LIST: {"OK" if ok else "ECHEC"}')
except Exception as e:
    log.append(f'KAGGLE_HTTPS_LIST: ECHEC {type(e).__name__} {str(e)[:120]}')
# 2) Drive: une seule partition
inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
batchof = {n: i['batch'] for n, i in kstate['uploaded'].items()}
cand = [p for p in inv if batchof.get(p['name']) == 'xauusd-is-b01']
p0 = sorted(cand, key=lambda p: p['name'])[0]
local = f"/tmp/{p0['name']}"
try:
    rc = subprocess.run(['gdown', '-q', '--output', local, p0.get('drive_id', '')]).returncode
    if pathlib.Path(local).exists():
        sz = pathlib.Path(local).stat().st_size
        log.append(f"DRIVE_1_FICHIER: rc={rc} taille={sz} attendue={p0.get('file_bytes')} {'OK' if sz == p0.get('file_bytes') else 'TAILLE_DIFFERENTE'}")
    else:
        log.append(f'DRIVE_1_FICHIER: rc={rc} fichier absent ECHEC')
except Exception as e:
    log.append(f'DRIVE_1_FICHIER: ECHEC {type(e).__name__} {str(e)[:120]}')
(OUT / 'ACCESS_PROBE.txt').write_text('\n'.join(log) + '\n')
print('\n'.join(log))
