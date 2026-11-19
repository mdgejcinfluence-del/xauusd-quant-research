"""PHASE 8 - BACKFILL S3 DUKASCOPY IS_NR (ingenierie, 0 essai).
Bougies 1 min BID/ASK quotidiennes (1 fichier/jour/sens), agregees en horaire UTC.
Reprise: un mois deja present dans reports/meta_alpha/nr/s3_hourly/ est saute.
Format bougie Dukascopy: >5i f (timestamp s, open, close, low, high x1000, volume) = 24 octets."""
import io, json, lzma, pathlib, struct, datetime as dt
import pandas as pd, requests

OUT = pathlib.Path('reports/meta_alpha/nr/s3_hourly'); OUT.mkdir(parents=True, exist_ok=True)
LOG = []
def log(m): print(m, flush=True); LOG.append(m)
def fetch(url):
    r = requests.get(url, timeout=90, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code != 200 or len(r.content) < 100: return None
    try: return lzma.decompress(r.content)
    except Exception: return None

def bougies(dec):
    n = len(dec) // 24; rows = []
    for i in range(n):
        t, o, c, lo, hi, v = struct.unpack_from('>5if', dec, i * 24)
        rows.append((t, o / 1000, c / 1000, lo / 1000, hi / 1000, v))
    return rows

def jour(d):
    base = f'https://datafeed.dukascopy.com/datafeed/XAUUSD/{d.year}/{d.month - 1:02d}/{d.day:02d}'
    out = {}
    for sens in ['BID', 'ASK']:
        dec = fetch(f'{base}/{sens}_candles_min_1.bi5')
        if dec is None: return None
        out[sens] = bougies(dec)
    b = pd.DataFrame(out['BID'], columns=['t', 'bo', 'bc', 'bl', 'bh', 'bv'])
    a = pd.DataFrame(out['ASK'], columns=['t', 'ao', 'ac', 'al', 'ah', 'av'])
    m = b.merge(a, on='t'); m['ts'] = pd.to_datetime(m.t, unit='s', utc=True)
    m['spread_bp'] = (m.ac - m.bc) / ((m.ac + m.bc) / 2) * 1e4
    m['heure'] = m.ts.dt.floor('h')
    g = m.groupby('heure').agg(close=('bc', 'last'), spread_med=('spread_bp', 'median'), volume=('bv', 'sum'), n=('t', 'size')).reset_index()
    return g

def main():
    d = dt.date(2020, 1, 1); fin = dt.date(2023, 12, 31)
    mois_courant = None; lignes = []; stats = {'jours_ok': 0, 'jours_vides': 0}
    while d <= fin:
        cle = f'{d.year}-{d.month:02d}'
        if cle != mois_courant:
            if lignes:
                pd.concat(lignes).to_parquet(OUT / f's3_hourly_{mois_courant}.parquet', index=False)
                log(f'mois {mois_courant} ecrit')
            mois_courant = cle; lignes = []
            if (OUT / f's3_hourly_{cle}.parquet').exists():
                log(f'mois {cle} deja present - saute')
                d = (d.replace(day=28) + dt.timedelta(days=7)).replace(day=1); mois_courant = f'{d.year}-{d.month:02d}'
                if (OUT / f's3_hourly_{mois_courant}.parquet').exists(): continue
                # le mois suivant sera traite normalement ci-dessous
        if d.weekday() < 5:
            g = jour(d)
            if g is not None and len(g): lignes.append(g); stats['jours_ok'] += 1
            else: stats['jours_vides'] += 1
        d += dt.timedelta(days=1)
    if lignes: pd.concat(lignes).to_parquet(OUT / f's3_hourly_{mois_courant}.parquet', index=False)
    (OUT / 'BACKFILL_STATE.json').write_text(json.dumps({**stats, 'journal': LOG[-50:]}, indent=1))
    log(f"BACKFILL TERMINE {stats}")
if __name__ == '__main__': main()
