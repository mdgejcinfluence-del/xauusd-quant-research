#!/usr/bin/env python3
"""RE-ENTRY-003 — collecteur d'instantanes publics HFM (Colorful drops 99001292).
Acces public ordinaire uniquement: AUCUN contournement anti-robot, aucun identifiant.
Modes:
  fetch    : GET public de la page strategy-view -> instantane immuable JSON (SHA-256).
             Si le site repond 403, l echec est journalise tel quel (jamais masque).
  ingest F : ingere un contenu de page deja obtenu licitement (HTML ou texte rendu).
  baskets  : deduplication (cle composite), regroupement en paniers justifie, tableau de suivi.
Chaque instantane est immuable; les transactions dedupliquees vivent dans TRANSACTIONS.csv."""
import hashlib, json, pathlib, re, sys
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
BASE = R / 'research' / 'RE-ENTRY-003'
URL = 'https://www.hfm.com/int/en/copy-trading/strategy-view?account=99001292'
PROVIDER = '99001292'
LIGNE = re.compile(r'(XAUUSDc)\s*\|\s*(Buy|Sell)\s*\|\s*([\d.]+)\s*\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*(-?[\d.]+)')

def extraire(texte):
    return [{'symbole': m.group(1), 'sens': m.group(2), 'volume': float(m.group(3)),
             'ouverture_affichee': m.group(4), 'cloture_affichee': m.group(5),
             'profit_affiche': float(m.group(6))} for m in LIGNE.finditer(texte)]

def cle(t):
    return '|'.join([t['symbole'], t['sens'], str(t['volume']), t['ouverture_affichee'],
                     t['cloture_affichee'], str(t['profit_affiche'])])

def enregistrer(texte, mode):
    tx = extraire(texte)
    snap = {'provider_id': PROVIDER, 'url_source': URL, 'collecte_utc': pd.Timestamp.now(tz='UTC').isoformat(),
            'mode_acces': mode, 'transactions_visibles': tx,
            'sha256_contenu': hashlib.sha256(texte.encode()).hexdigest()}
    nom = f"snapshot_{snap['collecte_utc'][:19].replace(':','').replace('T','_')}.json"
    (BASE / 'snapshots' / nom).write_text(json.dumps(snap, indent=1, ensure_ascii=False))
    print(nom, len(tx), 'transactions visibles')
    return snap

def mode_fetch():
    import requests
    try:
        r = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 META-ALPHA-research'}, timeout=60)
        if r.status_code != 200:
            print(f'ACCES_REFUSE_HTTP_{r.status_code}: echec journalise, aucune tentative de contournement.')
            (BASE / 'snapshots' / f"ECHEC_{pd.Timestamp.now(tz='UTC'):%Y%m%d_%H%M%S}.json").write_text(
                json.dumps({'http': r.status_code, 'collecte_utc': pd.Timestamp.now(tz='UTC').isoformat()}, indent=1))
            return
        enregistrer(r.text, 'fetch_public_http_200')
    except Exception as e:
        print(f'ECHEC_RESEAU: {type(e).__name__}: {e}')

def mode_ingest(fichier):
    enregistrer(pathlib.Path(fichier).read_text(errors='replace'), f'ingest_fichier_licite:{pathlib.Path(fichier).name}')

def mode_baskets():
    snaps = sorted((BASE / 'snapshots').glob('snapshot_*.json'))
    vues, compteur = {}, 0
    for f in snaps:
        s = json.loads(f.read_text()); compteur += 1
        for t in s['transactions_visibles']:
            vues.setdefault(cle(t), {**t, 'premier_instantane': f.name})
    T = pd.DataFrame(vues.values()).sort_values('ouverture_affichee').reset_index(drop=True)
    # Regroupement justifie: clotures a <=3 s les unes des autres ET ouverture post-cloture du panier precedent (3 s)
    paniers, courant, derniere_clot = [], [], None
    for _, t in T.iterrows():
        ouv, clo = pd.Timestamp(t.ouverture_affichee), pd.Timestamp(t.cloture_affichee)
        if courant and derniere_clot is not None and ouv > derniere_clot + pd.Timedelta(seconds=3):
            paniers.append(courant); courant = []
        courant.append(t); derniere_clot = clo if derniere_clot is None else max(derniere_clot, clo)
    if courant: paniers.append(courant)
    lignes = []
    for i, p in enumerate(paniers, 1):
        lignes.append({'panier': f'P{i:03d}', 'positions': len(p),
                       'volumes': ' / '.join(str(t.volume) for t in p),
                       'debut_affiche': min(t.ouverture_affichee for t in p),
                       'fin_affichee': max(t.cloture_affichee for t in p),
                       'profit_total_affiche': round(sum(t.profit_affiche for t in p), 2),
                       'regroupement': 'clotures groupees <=3 s, ouvertures sequentielles',
                       'statut_reconstruction': 'EN_ATTENTE_COTATIONS'})
    B = pd.DataFrame(lignes)
    T.to_csv(BASE / 'TRANSACTIONS.csv', index=False); B.to_csv(BASE / 'PANIERS.csv', index=False)
    suivi = {'instantanes': compteur, 'transactions_distinctes': int(len(T)),
             'paniers_identifies': int(len(B)),
             'gagnants': int((B.profit_total_affiche > 0).sum()), 'perdants': int((B.profit_total_affiche < 0).sum())}
    (BASE / 'SUIVI.json').write_text(json.dumps(suivi, indent=1)); print(json.dumps(suivi, indent=1))

if __name__ == '__main__':
    m = sys.argv[1] if len(sys.argv) > 1 else 'baskets'
    {'fetch': mode_fetch, 'baskets': mode_baskets,
     'ingest': lambda: mode_ingest(sys.argv[2])}[m]()
