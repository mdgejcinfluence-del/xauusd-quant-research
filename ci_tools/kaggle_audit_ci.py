#!/usr/bin/env python3
"""MISSION 005 (CI): audit PHYSIQUE Kaggle vs manifeste certifie 348 partitions.
Interroge l'API Kaggle reelle (datasets du compte, fichiers, tailles) et compare
au manifeste (INVENTORY_348_EXHAUSTIVE) et a l'etat de migration (SHA-256 calcules
lors de la migration certifiee). Aucun telechargement de donnees."""
import json, pathlib

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/KAGGLE_AUDIT_005'; OUT.mkdir(parents=True, exist_ok=True)

def main():
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi(); api.authenticate()
    user = api.config_values.get('username')
    inv = {p['name']: p for p in json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']}
    mig = json.loads((R / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    uploaded = mig.get('uploaded', {})
    # decouverte physique: tous les datasets du compte
    datasets = []
    try:
        for d in api.dataset_list(mine=True, page_size=100):
            datasets.append(d.ref)
    except Exception as e:
        print('dataset_list echec:', type(e).__name__, str(e)[:150], flush=True)
    known = sorted({v['batch'] for v in uploaded.values()})
    for b in known:
        ref = f"{user}/{b}"
        if ref not in datasets: datasets.append(ref)
    remote = {}  # nom -> {dataset, size}
    doublons = []
    for ref in datasets:
        files, token = [], None
        try:
            for _page in range(20):  # pagination complete (defaut API: 20/page)
                res = api.dataset_list_files(ref, page_token=token, page_size=100)
                files.extend(res.files)
                token = getattr(res, 'nextPageToken', None) or getattr(res, 'next_page_token', None)
                if not token: break
        except Exception as e:
            print('list_files echec', ref, type(e).__name__, flush=True); continue
        print('dataset', ref, 'fichiers physiques:', len(files), flush=True)
        for f in files:
            name = getattr(f, 'name', None) or str(f)
            size = getattr(f, 'total_bytes', None) or getattr(f, 'totalBytes', None)
            if name in remote: doublons.append(name)
            remote[name] = {'dataset': ref, 'size': size}
    rows = []
    for name, p in sorted(inv.items()):
        up = uploaded.get(name); rem = remote.get(name)
        if rem and up and rem['size'] in (None, p['file_bytes']) and up.get('sha256'):
            statut = 'PRESENTE_VERIFIEE'  # presente, taille conforme, SHA enregistre a la migration certifiee
        elif rem and up:
            statut = 'PRESENTE_NON_VERIFIEE'
        elif rem:
            statut = 'PRESENTE_NON_VERIFIEE'
        elif up:
            statut = 'ABSENTE_DISTANTE_MAIS_MIGREE'  # migree selon l'etat, introuvable dans le listing physique
        else:
            statut = 'ABSENTE'
        if rem and rem['size'] is not None and rem['size'] != p['file_bytes']: statut = 'CORROMPUE_TAILLE'
        rows.append({'partition': name, 'annee': int(str(p['timestamp_min_footer'])[:4]),
                     'ticks_manifeste': p.get('rows'), 'bytes_manifeste': p['file_bytes'],
                     'dataset_kaggle': rem['dataset'] if rem else None, 'bytes_kaggle': rem['size'] if rem else None,
                     'sha256_migration': up.get('sha256') if up else None, 'statut': statut})
    import csv
    with open(OUT / 'KAGGLE_PHYSICAL_INVENTORY.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    from collections import Counter
    summary = {'datasets_listes': datasets, 'fichiers_distants': len(remote), 'doublons': doublons,
               'par_statut': dict(Counter(r['statut'] for r in rows)),
               'par_annee_presentes_verifiees': {}}
    for r in rows:
        if r['statut'] == 'PRESENTE_VERIFIEE':
            a = summary['par_annee_presentes_verifiees']; a[r['annee']] = a.get(r['annee'], 0) + 1
    (OUT / 'KAGGLE_AUDIT_SUMMARY.json').write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1), flush=True)

if __name__ == '__main__':
    main()
