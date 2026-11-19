"""Upload du lake NR complet (incl. HOLDOUT scelle) vers Kaggle prive; verification noms/tailles.
Le HOLDOUT_NR n'est jamais re-telecharge par un moteur: upload seul."""
import json, pathlib, time
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate(); user = api.config_values.get('username')
slug = 'xauusd-nr-corpus'
lake = pathlib.Path('/tmp/nr_lake'); meta = pathlib.Path('/tmp/nr_meta'); meta.mkdir(exist_ok=True)
files = sorted(lake.glob('*.parquet'))
for f in files: (meta / f.name).write_bytes(f.read_bytes())
(meta / 'dataset-metadata.json').write_text(json.dumps({'title': slug, 'id': f'{user}/{slug}', 'licenses': [{'name': 'other'}]}))
try:
    existants = {f.name for f in api.dataset_list_files(f'{user}/{slug}', page_size=100).files}
except Exception: existants = set()
try:
    if existants: api.dataset_create_version(str(meta), version_notes='collecte NR', quiet=True); statut = 'version maj'
    else: api.dataset_create_new(str(meta), public=False, quiet=True); statut = 'cree'
except Exception as e:
    statut = f'ECHEC {str(e)[:120]}'
dist = {}
for _ in range(20):
    try:
        dist = {f.name: f.total_bytes for f in api.dataset_list_files(f'{user}/{slug}', page_size=100).files}
        if all(dist.get(f.name) == f.stat().st_size for f in files): break
    except Exception: pass
    time.sleep(30)
res = {'dataset': f'{user}/{slug}', 'statut': statut, 'fichiers': {f.name: f.stat().st_size for f in files},
       'distants': dist, 'all_ok': all(dist.get(f.name) == f.stat().st_size for f in files),
       'note': 'HOLDOUT_NR (2025+) present dans le lake: upload seul, jamais re-telecharge par un moteur'}
pathlib.Path('reports/meta_alpha/nr/VERIFY_NR_LAKE.json').write_text(json.dumps(res, indent=1))
print(slug, statut, 'all_ok=', res['all_ok'])
