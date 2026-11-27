#!/usr/bin/env python3
"""HISTORICAL-DATA-COMPLETION — completement Dukascopy 2026-10-01 -> 2026-11-26.
Reutilise edge02_dukascopy.telecharger_heure (.bi5 Bid/Ask ms UTC, DUKASCOPY_PRIMARY).
Idempotent: manifeste par heure; vide recent jamais fige; aucun tick reconstruit.
Sortie: parquet mensuel normalise /tmp + manifeste committe; publication Kaggle privee
(dataset distinct, jamais d ecrasement des 348 partitions certifiees)."""
import hashlib, json, pathlib, sys
import pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from edge02_dukascopy import telecharger_heure, qualite

RACINE = pathlib.Path(__file__).resolve().parents[1]
SORTIE = RACINE / 'research' / 'HISTORICAL-DATA-COMPLETION'
DEBUT, FIN = '2026-10-01T00:00', '2026-11-26T23:00'

def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def main(debut=DEBUT, fin=FIN):
    SORTIE.mkdir(parents=True, exist_ok=True)
    man_p = SORTIE / 'COMPLETION_MANIFEST.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'heures': {}, 'lots': {}}
    # les 'vides anciens' d un run parallele peuvent etre des 503 transitoires (rate-limit):
    # jamais figes dans cette mission, toujours re-essayes
    man['heures'] = {k: v for k, v in man['heures'].items() if v.get('statut') != 'VIDE_ANCIEN_FIGE'}
    par_mois = {}
    heures = [h for h in pd.date_range(DEBUT, FIN, freq='h')
              if man['heures'].get(str(h), {}).get('statut') != 'OK']
    from concurrent.futures import ThreadPoolExecutor
    def travail(h):
        import time
        for essai in range(2):
            df = telecharger_heure(h)
            if df is not None and len(df): return h, df
            time.sleep(3 * (essai + 1))
        return h, None
    with ThreadPoolExecutor(max_workers=1) as ex:
        for h, df in ex.map(travail, heures):
            cle = str(h)
            if df is None or len(df) == 0:
                man['heures'][cle] = {'statut': 'ECHEC_OU_VIDE_A_REESSAYER', 'ticks': 0}
                continue
            q = qualite(df)
            man['heures'][cle] = {'statut': 'OK', 'ticks': q['ticks'],
                                  'bid_lt_ask_violations': q['bid_lt_ask_violations']}
            par_mois.setdefault(f"{h.year}-{h.month:02d}", []).append(df)
    for mois, morceaux in par_mois.items():
        neuf = pd.concat(morceaux)
        mois = f"{mois}_lot{pd.Timestamp(debut).strftime('%m%d')}-{pd.Timestamp(fin).strftime('%m%d')}"  # lot hebdomadaire distinct, jamais d ecrasement mensuel
        neuf['source'] = 'DUKASCOPY_PRIMARY'; neuf['spread'] = neuf.ask - neuf.bid
        neuf = neuf.drop_duplicates('ts').sort_values('ts')
        f = pathlib.Path(f'/tmp/duka_completion_{mois}.parquet'); neuf.to_parquet(f, index=False)
        man['lots'][mois] = {'fichier_tmp': str(f), 'sha256': sha(f), 'ticks': int(len(neuf)),
                             'debut': str(neuf.ts.iloc[0]), 'fin': str(neuf.ts.iloc[-1]),
                             'bid_ask_100pc': bool((neuf.bid < neuf.ask).all())}
        print(mois, len(neuf), 'ticks', man['lots'][mois]['sha256'][:12])
    man_p.write_text(json.dumps(man, indent=1))
    print('heures OK:', sum(1 for v in man['heures'].values() if v['statut'] == 'OK'),
          '/ suivies:', len(man['heures']))


def mode_echantillon():
    """Diagnostic: 8 heures reperees, requetes sequentielles avec codes HTTP explicites."""
    import urllib.request, urllib.error
    heures = ['2026-10-01T10:00','2026-10-05T10:00','2026-10-12T10:00','2026-10-20T10:00',
              '2026-11-02T10:00','2026-11-10T10:00','2026-11-17T10:00','2026-11-25T10:00']
    res = {}
    for hs in heures:
        h = pd.Timestamp(hs)
        u = f'https://datafeed.dukascopy.com/datafeed/XAUUSD/{h.year}/{h.month-1:02d}/{h.day:02d}/{h.hour:02d}h_ticks.bi5'
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 META-ALPHA-research'}), timeout=60) as r:
                corps = r.read()
            df = telecharger_heure(h)
            res[hs] = {'http': r.status, 'octets': len(corps), 'ticks': 0 if df is None else int(len(df))}
        except urllib.error.HTTPError as e:
            res[hs] = {'http': e.code, 'octets': 0, 'ticks': 0}
        except Exception as e:
            res[hs] = {'erreur': f'{type(e).__name__}: {e}'}
        print(hs, res[hs])
    (SORTIE / 'ECHantillon.json'.replace('ECH','ECH')).write_text(json.dumps(res, indent=1))

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'echantillon': mode_echantillon()
    elif len(sys.argv) > 2: main(sys.argv[1], sys.argv[2])
    else: main()
