"""PHASE 12-C.2-R - migration controlee holdout Drive -> Kaggle prive.
Autorisation seq320. Modes:
- probe (P12C2R_MODE=probe): verifie la presence des secrets (booleens
  uniquement, jamais de valeurs), l'authentification du compte de
  service Drive et l'acces en metadonnees a la premiere et derniere
  partition; authentification Kaggle. Aucun contenu telecharge.
- lot (P12C2R_MODE=lot, P12C2R_LOT=b01..b06): telecharge les partitions
  du lot via l'API Drive authentifiee par compte de service (jamais
  gdown ni lien anonyme), verifie taille + signature PAR1, calcule le
  SHA-256 source (etabli a ce transfert authentifie: absent de
  l'inventaire historique), cree le dataset Kaggle PRIVE du lot,
  re-telecharge la copie Kaggle et compare les SHA-256 fichier par
  fichier. Aucun fichier de donnees n'est ecrit dans le depot."""
import csv, hashlib, io, json, os, pathlib, subprocess, sys, zipfile

ROOT12 = pathlib.Path('reports/meta_alpha/phase12'); ROOT12.mkdir(parents=True, exist_ok=True)
LOTS = {'b01': (283, 293), 'b02': (294, 304), 'b03': (305, 315), 'b04': (316, 326), 'b05': (327, 337), 'b06': (338, 348)}

def sha256_fichier(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 22), b''): h.update(ch)
    return h.hexdigest()

def manifeste():
    rows = list(csv.DictReader(open(ROOT12 / 'PHASE12C2_HOLDOUT_TRANSFER_MANIFEST.csv')))
    assert len(rows) == 66, len(rows)
    return {r['fichier_source']: r for r in rows}

def drive_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    info = json.loads(os.environ['GDRIVE_SA_JSON'])
    creds = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    return build('drive', 'v3', credentials=creds, cache_discovery=False)

def mode_probe():
    rep = {'mode': 'probe', 'gdrive_sa_present': bool(os.environ.get('GDRIVE_SA_JSON')),
           'gdrive_root_id_present': bool(os.environ.get('GDRIVE_ROOT_FOLDER_ID')),
           'kaggle_api_token_present': bool(os.environ.get('KAGGLE_API_TOKEN')),
           'kaggle_username_present': bool(os.environ.get('KAGGLE_USERNAME')),
           'kaggle_key_present': bool(os.environ.get('KAGGLE_KEY')),
           'sa_auth_ok': False, 'acces_metadonnees': {}, 'kaggle_auth_ok': False}
    man = manifeste()
    if rep['gdrive_sa_present']:
        try:
            svc = drive_service(); rep['sa_auth_ok'] = True
            for nom in ('part_000283.parquet', 'part_000348.parquet'):
                fid = man[nom]['reference_source_drive_id']
                md = svc.files().get(fileId=fid, fields='id,name,size,mimeType').execute()
                rep['acces_metadonnees'][nom] = {'nom_retourne': md.get('name'), 'taille_retournee': md.get('size'),
                                                 'taille_attendue': man[nom]['taille_attendue_octets'],
                                                 'concordance': str(md.get('size')) == str(man[nom]['taille_attendue_octets']) and md.get('name') == nom}
        except Exception as e:
            rep['erreur_sa'] = f'{type(e).__name__}: {str(e)[:200]}'
    if rep['kaggle_api_token_present'] or (rep['kaggle_username_present'] and rep['kaggle_key_present']):
        try:
            import requests
            tok = os.environ.get('KAGGLE_API_TOKEN', '')
            r = requests.get('https://www.kaggle.com/api/v1/datasets/list?user=shalom5123', headers={'Authorization': f'Bearer {tok}'}, timeout=60) if tok else None
            rep['kaggle_auth_ok'] = bool(r is not None and r.status_code == 200)
            rep['kaggle_datasets_visibles'] = [d.get('ref') for d in r.json()][:50] if rep['kaggle_auth_ok'] else []
        except Exception as e:
            rep['erreur_kaggle'] = f'{type(e).__name__}: {str(e)[:200]}'
    (ROOT12 / 'PHASE12C2_PROBE.json').write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    print(json.dumps(rep, indent=1, ensure_ascii=False), flush=True)

def telecharger_drive(svc, fid, local):
    from googleapiclient.http import MediaIoBaseDownload
    req = svc.files().get_media(fileId=fid)
    with open(local, 'wb') as f:
        dl = MediaIoBaseDownload(f, req, chunksize=1 << 23)
        fait = False
        while not fait:
            _, fait = dl.next_chunk()

def kaggle_env():
    env = dict(os.environ)
    return env

def mode_lot():
    lot = os.environ['P12C2R_LOT']; a, b = LOTS[lot]
    dataset_id = f'shalom5123/xauusd-ho-{lot}'
    man = manifeste()
    resultat = {'lot': lot, 'dataset': dataset_id, 'fichiers': [], 'statut': 'EN_COURS'}
    svc = drive_service()
    dossier = pathlib.Path('/tmp/kaggle_upload'); dossier.mkdir(exist_ok=True)
    for n in range(a, b + 1):
        nom = f'part_{n:06d}.parquet'; m = man[nom]; local = str(dossier / nom)
        telecharger_drive(svc, m['reference_source_drive_id'], local)
        taille = pathlib.Path(local).stat().st_size
        entree = {'fichier': nom, 'taille_attendue': int(m['taille_attendue_octets']), 'taille_source': taille,
                  'signature_par1': open(local, 'rb').read(4) == b'PAR1', 'sha256_source': sha256_fichier(local)}
        entree['taille_ok'] = taille == int(m['taille_attendue_octets'])
        resultat['fichiers'].append(entree)
        print('P12C2R', lot, nom, 'source OK', entree['taille_ok'], flush=True)
    if not all(f['taille_ok'] and f['signature_par1'] for f in resultat['fichiers']):
        resultat['statut'] = 'BLOCKED_DIVERGENCE_SOURCE'; _ecrire(resultat); raise RuntimeError('divergence source')
    meta = {'title': f'META ALPHA XAUUSD Holdout 2020-2026 {lot}', 'id': dataset_id,
            'licenses': [{'name': 'CC0-1.0'}], 'isPrivate': True,
            'description': 'Partitions holdout XAUUSD transferees sous controle (Phase 12-C.2-R, seq320). Usage reserve a la confirmation H1 preenregistree.'}
    (dossier / 'dataset-metadata.json').write_text(json.dumps(meta))
    r = subprocess.run(['kaggle', 'datasets', 'create', '-p', str(dossier), '--dir-mode', 'zip'],
                       capture_output=True, text=True, env=kaggle_env(), timeout=3300)
    print('kaggle create rc', r.returncode, (r.stdout or r.stderr)[-500:], flush=True)
    if r.returncode != 0:
        # dataset peut deja exister lors d'une reprise technique avant toute metrique: basculer en nouvelle version
        r = subprocess.run(['kaggle', 'datasets', 'version', '-p', str(dossier), '-m', 'transfert controle 12-C.2-R', '--dir-mode', 'zip'],
                           capture_output=True, text=True, env=kaggle_env(), timeout=3300)
        print('kaggle version rc', r.returncode, (r.stdout or r.stderr)[-500:], flush=True)
        if r.returncode != 0:
            resultat['statut'] = 'BLOCKED_KAGGLE_UPLOAD'; _ecrire(resultat); raise RuntimeError('upload Kaggle impossible')
    # verification: re-telecharger la copie Kaggle et comparer les empreintes
    import requests, time
    tok = os.environ.get('KAGGLE_API_TOKEN', '')
    url = f'https://www.kaggle.com/api/v1/datasets/download/{dataset_id}'
    copie = None
    for tentative in range(6):
        r = requests.get(url, headers={'Authorization': f'Bearer {tok}'}, timeout=1200)
        if r.status_code == 200: copie = r.content; break
        print('attente copie Kaggle', r.status_code, tentative, flush=True); time.sleep(60)
    if copie is None:
        resultat['statut'] = 'BLOCKED_COPIE_KAGGLE_INTROUVABLE'; _ecrire(resultat); raise RuntimeError('copie Kaggle introuvable')
    z = zipfile.ZipFile(io.BytesIO(copie)); noms = [n for n in z.namelist() if n.endswith('.parquet')]
    resultat['fichiers_copie_kaggle'] = sorted(noms)
    for entree in resultat['fichiers']:
        nom = entree['fichier']
        correspondance = [n for n in noms if pathlib.Path(n).name == nom]
        if len(correspondance) != 1:
            entree['sha256_copie_kaggle'] = None; entree['correspondance_sha256'] = False; continue
        data = z.read(correspondance[0])
        entree['sha256_copie_kaggle'] = hashlib.sha256(data).hexdigest()
        entree['taille_copie'] = len(data)
        entree['correspondance_sha256'] = entree['sha256_copie_kaggle'] == entree['sha256_source']
    ok = (len(noms) == len(resultat['fichiers']) and all(f.get('correspondance_sha256') for f in resultat['fichiers']))
    resultat['statut'] = 'LOT_VERIFIE' if ok else 'BLOCKED_DIVERGENCE_COPIE'
    _ecrire(resultat)
    print(json.dumps(resultat, indent=1)[:3000], flush=True)
    if not ok: raise RuntimeError('divergence copie Kaggle')

def _ecrire(resultat):
    (ROOT12 / f"PHASE12C2_TRANSFER_LOT_{resultat['lot']}.json").write_text(json.dumps(resultat, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    if os.environ.get('P12C2R_MODE') == 'probe': mode_probe()
    else: mode_lot()
