"""PHASE 12-C.2-R2 - sonde d'acces au dossier Drive partage (seq322).
Lecture seule: enumeration du dossier (sans telechargement), comparaison
des noms/identifiants aux 66 entrees du manifeste gele, test de contenu
sur UN fichier (le plus petit: telechargement reel, taille, PAR1 debut/fin,
SHA-256 a la reception), controle des six datasets Kaggle de destination
(existence, fichiers). Aucun secret ni identifiant de dossier consigne
dans la sortie."""
import csv, hashlib, json, os, pathlib, subprocess

ROOT12 = pathlib.Path('reports/meta_alpha/phase12')
FOLDER = os.environ['DRIVE_FOLDER_ID']

def sha256_fichier(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 22), b''): h.update(ch)
    return h.hexdigest()

def main():
    man = {r['fichier_source']: r for r in csv.DictReader(open(ROOT12 / 'PHASE12C2_HOLDOUT_TRANSFER_MANIFEST.csv'))}
    assert len(man) == 66
    rep = {'phase': '12-C.2-R2', 'etape': 'sonde', 'manifeste_lignes': 66}
    import gdown
    fichiers = gdown.download_folder(id=FOLDER, output='/tmp/probe_list', skip_download=True, quiet=True)
    entrees = [{'nom': pathlib.Path(f.path).name, 'id': f.id} for f in (fichiers or [])]
    rep['dossier_accessible'] = len(entrees) > 0
    rep['fichiers_enumeres'] = len(entrees)
    noms = sorted(e['nom'] for e in entrees if e['nom'].endswith('.parquet'))
    rep['parquet_enumeres'] = len(noms)
    rep['noms_conformes_manifeste'] = noms == sorted(man.keys())
    rep['manquants'] = sorted(set(man) - set(noms))[:5]
    rep['supplementaires'] = sorted(set(noms) - set(man))[:5]
    par_nom = {e['nom']: e['id'] for e in entrees}
    rep['ids_correspondent_au_manifeste'] = all(par_nom.get(n) == man[n]['reference_source_drive_id'] for n in man if n in par_nom)
    rep['ids_differents'] = [n for n in man if n in par_nom and par_nom[n] != man[n]['reference_source_drive_id']][:5]
    # test de contenu reel sur le plus petit fichier du manifeste present dans le dossier
    candidat = min((man[n] for n in noms if n in man), key=lambda r: int(r['taille_attendue_octets']), default=None)
    if candidat:
        local = f"/tmp/{candidat['fichier_source']}"
        rc = subprocess.run(['gdown', '-q', '--output', local, par_nom[candidat['fichier_source']]]).returncode
        recu = pathlib.Path(local)
        if rc == 0 and recu.exists():
            with open(local, 'rb') as f: tete = f.read(4)
            with open(local, 'rb') as f:
                f.seek(-4, 2); queue = f.read(4)
            rep['test_contenu'] = {'fichier': candidat['fichier_source'], 'taille_recue': recu.stat().st_size,
                                   'taille_attendue': int(candidat['taille_attendue_octets']),
                                   'taille_ok': recu.stat().st_size == int(candidat['taille_attendue_octets']),
                                   'par1_debut': tete == b'PAR1', 'par1_fin': queue == b'PAR1',
                                   'sha256_reception': sha256_fichier(local)}
            recu.unlink()
        else:
            rep['test_contenu'] = {'fichier': candidat['fichier_source'], 'echec_telechargement': True, 'code_retour': rc}
    # destinations Kaggle: existence et contenu actuel
    dests = {}
    for i in range(1, 7):
        ref = f'shalom5123/xauusd-ho-b{i:02d}'
        r = subprocess.run(['kaggle', 'datasets', 'files', ref], capture_output=True, text=True, timeout=120)
        dests[ref] = {'existe': r.returncode == 0, 'sortie': (r.stdout or r.stderr)[-400:]}
    rep['destinations_kaggle'] = dests
    (ROOT12 / 'PHASE12C2R2_PROBE.json').write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    print(json.dumps(rep, indent=1, ensure_ascii=False)[:4000], flush=True)

if __name__ == '__main__':
    main()
