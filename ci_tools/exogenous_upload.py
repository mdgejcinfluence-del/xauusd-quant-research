"""Upload Kaggle des 3 packs scelles par perimetre + verification noms/tailles (jamais de re-telechargement des scelles)."""
import json, pathlib, time
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate(); user = api.config_values.get('username')
JOBS = {'is': ('xauusd-exogenous-pack-is', pathlib.Path('reports/meta_alpha/exogenous/data_is')),
        'oos': ('xauusd-exogenous-pack-oos', pathlib.Path('/tmp/pack_oos')),
        'holdout': ('xauusd-exogenous-pack-holdout', pathlib.Path('/tmp/pack_holdout'))}
res = {}
for pk, (slug, folder) in JOBS.items():
    files = sorted(folder.glob('*.parquet'))
    if not files: res[pk] = {'statut': 'VIDE - rien a publier'}; continue
    meta_dir = pathlib.Path(f'/tmp/up_{pk}'); meta_dir.mkdir(exist_ok=True)
    for f in files:
        (meta_dir / f.name).write_bytes(f.read_bytes())
    (meta_dir / 'dataset-metadata.json').write_text(json.dumps(
        {'title': slug, 'id': f'{user}/{slug}', 'licenses': [{'name': 'other'}]}))
    try:
        api.dataset_create_new(str(meta_dir), public=False, quiet=True); statut = 'cree'
    except Exception as e:
        try: api.dataset_create_version(str(meta_dir), version_notes='maj pack exogene', quiet=True); statut = 'version maj'
        except Exception as e2: res[pk] = {'statut': f'ECHEC upload: {str(e)[:100]} / {str(e2)[:100]}'}; continue
    # verification noms + tailles (metadonnees uniquement pour les scelles)
    dist = {}
    for essai in range(6):
        try:
            r = api.dataset_list_files(f'{user}/{slug}', page_size=100)
            dist = {f.name: f.total_bytes for f in r.files}
            if len(dist) >= len(files): break
        except Exception: pass
        time.sleep(20)
    local = {f.name: f.stat().st_size for f in files}
    res[pk] = {'dataset': f'{user}/{slug}', 'statut_upload': statut,
               'fichiers_locaux': local, 'fichiers_distants': dist,
               'all_ok': all(dist.get(k) == v for k, v in local.items()),
               'role': 'EXPOSE' if pk == 'is' else 'SCELLE (liste de metadonnees seulement, contenu jamais telecharge)'}
    print(pk, res[pk]['statut_upload'], 'all_ok=', res[pk]['all_ok'], flush=True)
pathlib.Path('reports/meta_alpha/exogenous/VERIFY_KAGGLE.json').write_text(json.dumps(res, indent=1))
print('UPLOAD TERMINE')
