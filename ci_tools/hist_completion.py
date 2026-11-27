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

def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    man_p = SORTIE / 'COMPLETION_MANIFEST.json'
    man = json.loads(man_p.read_text()) if man_p.exists() else {'heures': {}, 'lots': {}}
    par_mois = {}
    for h in pd.date_range(DEBUT, FIN, freq='h'):
        cle = str(h)
        if man['heures'].get(cle, {}).get('statut') == 'OK': continue
        df = telecharger_heure(h)
        if df is None or len(df) == 0:
            if h < pd.Timestamp.now(tz='UTC').tz_localize(None) - pd.Timedelta(hours=48):
                man['heures'][cle] = {'statut': 'VIDE_ANCIEN_FIGE', 'ticks': 0}
            continue
        q = qualite(df)
        man['heures'][cle] = {'statut': 'OK', 'ticks': q['ticks'],
                              'bid_lt_ask_violations': q['bid_lt_ask_violations']}
        par_mois.setdefault(f"{h.year}-{h.month:02d}", []).append(df)
    for mois, morceaux in par_mois.items():
        neuf = pd.concat(morceaux)
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

if __name__ == '__main__':
    main()
