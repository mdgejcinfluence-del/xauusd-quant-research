"""PHASE 12-C.2-R3 - verification cryptographique 66/66 des datasets Kaggle.
Lecture seule Kaggle (aucune publication), aucun acces Drive.
Compare chaque fichier Kaggle a l'empreinte SOURCE du proprietaire
(SOURCE_SHA256_66_PARTITIONS.json, calculee dans Colab authentifie sur
les originaux) et au manifeste gele. Sorties: inventaire, CSV de
verification ligne par ligne, audit global. Code de sortie 1 si le
verdict n'est pas HOLDOUT_MIGRATION_VERIFIED (empeche toute analyse)."""
import csv, hashlib, io, json, os, pathlib, sys, zipfile
import requests

ROOT12 = pathlib.Path('reports/meta_alpha/phase12')
LOTS = {'b01': (283, 293), 'b02': (294, 304), 'b03': (305, 315), 'b04': (316, 326), 'b05': (327, 337), 'b06': (338, 348)}
TOK = os.environ.get('KAGGLE_API_TOKEN', '')

def telecharger_dataset(ref):
    r = requests.get(f'https://www.kaggle.com/api/v1/datasets/download/{ref}',
                     headers={'Authorization': f'Bearer {TOK}'}, timeout=1800)
    r.raise_for_status()
    return r.content

def metadonnees(ref):
    try:
        r = requests.get(f'https://www.kaggle.com/api/v1/datasets/view/{ref}',
                         headers={'Authorization': f'Bearer {TOK}'}, timeout=120)
        if r.status_code == 200:
            d = r.json()
            return {'ref': ref, 'titre': d.get('title'), 'proprietaire': d.get('ownerName'),
                    'version': d.get('currentVersionNumber'), 'prive': d.get('isPrivate'),
                    'taille_totale': d.get('totalBytes')}
        return {'ref': ref, 'erreur_http': r.status_code}
    except Exception as e:
        return {'ref': ref, 'erreur': f'{type(e).__name__}: {str(e)[:120]}'}

def main():
    man = {r['fichier_source']: r for r in csv.DictReader(open(ROOT12 / 'PHASE12C2_HOLDOUT_TRANSFER_MANIFEST.csv'))}
    assert len(man) == 66
    src = {f['file']: f for f in json.load(open(ROOT12 / 'SOURCE_SHA256_66_PARTITIONS.json'))['files']}
    assert len(src) == 66 and set(src) == set(man)
    inventaire, lignes = [], []
    for lot, (a, b) in LOTS.items():
        ref = f'shalom5123/xauusd-ho-{lot}'
        md = metadonnees(ref); contenu = telecharger_dataset(ref)
        z = zipfile.ZipFile(io.BytesIO(contenu))
        noms = sorted(pathlib.Path(n).name for n in z.namelist() if n.endswith('.parquet'))
        attendus = [f'part_{n:06d}.parquet' for n in range(a, b + 1)]
        inventaire.append(md | {'dataset': ref, 'fichiers_observes': noms, 'fichiers_attendus': attendus,
                                'inventaire_conforme': noms == attendus})
        print('P12C2R3', ref, 'version', md.get('version'), 'prive', md.get('prive'), 'fichiers', len(noms), flush=True)
        for nom in attendus:
            membre = [n for n in z.namelist() if pathlib.Path(n).name == nom]
            if len(membre) != 1:
                lignes.append({'nom': nom, 'dataset': ref, 'version_kaggle': md.get('version'),
                               'taille_source': src[nom]['size_bytes'], 'taille_destination': None,
                               'sha256_source_colab': src[nom]['sha256_source'], 'sha256_kaggle': None,
                               'par1_debut': None, 'par1_fin': None, 'statut_comparaison': 'MANQUANT_OU_DOUBLON'})
                continue
            data = z.read(membre[0])
            h = hashlib.sha256(data).hexdigest()
            lignes.append({'nom': nom, 'dataset': ref, 'version_kaggle': md.get('version'),
                           'taille_source': src[nom]['size_bytes'], 'taille_destination': len(data),
                           'sha256_source_colab': src[nom]['sha256_source'], 'sha256_kaggle': h,
                           'par1_debut': data[:4] == b'PAR1', 'par1_fin': data[-4:] == b'PAR1',
                           'statut_comparaison': 'IDENTIQUE' if (h == src[nom]['sha256_source'] and len(data) == src[nom]['size_bytes'] == int(man[nom]['taille_attendue_octets'])) else 'DIVERGENCE'})
            print('P12C2R3', nom, lignes[-1]['statut_comparaison'], flush=True)
        del contenu
    with open(ROOT12 / 'PHASE12C2_SHA256_VERIFICATION.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys())); w.writeheader(); w.writerows(lignes)
    (ROOT12 / 'PHASE12C2_KAGGLE_INVENTORY.json').write_text(json.dumps(inventaire, indent=1, ensure_ascii=False))
    ok = (len(lignes) == 66 and all(l['statut_comparaison'] == 'IDENTIQUE' for l in lignes)
          and all(i['inventaire_conforme'] for i in inventaire))
    audit = {'phase': '12-C.2-R3', 'verdict_migration': 'HOLDOUT_MIGRATION_VERIFIED' if ok else 'HOLDOUT_MIGRATION_BLOCKED',
             'controle': {'attendus': 66, 'presents_verifies': int(sum(l['statut_comparaison'] == 'IDENTIQUE' for l in lignes)),
                          'manquants_ou_doublons': int(sum(l['statut_comparaison'] == 'MANQUANT_OU_DOUBLON' for l in lignes)),
                          'divergences': int(sum(l['statut_comparaison'] == 'DIVERGENCE' for l in lignes)),
                          'inventaires_datasets_conformes': bool(all(i['inventaire_conforme'] for i in inventaire)),
                          'confidentialite': {i['dataset']: i.get('prive') for i in inventaire},
                          'versions': {i['dataset']: i.get('version') for i in inventaire}},
             'provenance_empreintes_source': 'SOURCE_SHA256_66_PARTITIONS.json (proprietaire, Colab authentifie sur les originaux Drive) sha256 du fichier recu: voir checkpoint; empreintes jamais recalculees depuis la destination pour servir de reference',
             'historique': 'verdicts precedents HOLDOUT_MIGRATION_BLOCKED (seq321, seq323) par indisponibilite des sources; le present controle compare les copies Kaggle aux empreintes source fournies, sans aucun nouvel acces Drive',
             'fichiers_a_problemes': [l for l in lignes if l['statut_comparaison'] != 'IDENTIQUE']}
    (ROOT12 / 'PHASE12C2_HOLDOUT_TRANSFER_AUDIT.json').write_text(json.dumps(audit, indent=1, ensure_ascii=False))
    print(json.dumps(audit, indent=1, ensure_ascii=False)[:3000], flush=True)
    if not ok: sys.exit(1)

if __name__ == '__main__':
    main()
