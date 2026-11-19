"""PHASE 8 - COLLECTEUR CORPUS NR (ingenierie, 0 essai).
S1 Yahoo (GC=F, XAUUSD=X): daily 2020+, horaire 730j, 1min roulant. S2 Swissquote: snapshot spread.
S3 Dukascopy: qualification (telechargement + decompression LZMA d'un fichier horaire).
Sorties: reports/meta_alpha/nr/{MANIFEST_NR.json, data_is/, data_valid/} commitees (IS 2020-2023, VALID 2024);
bruts complets (incl. HOLDOUT 2025+) -> /tmp/nr_lake pour upload Kaggle scelle (jamais re-telecharge).
Append-only cote spreads: le fichier spreads est relu depuis le lake local du job si present, sinon reparti vide (consigne)."""
import io, json, lzma, pathlib, struct, datetime as dt
import pandas as pd, requests

OUT = pathlib.Path('reports/meta_alpha/nr'); (OUT / 'data_is').mkdir(parents=True, exist_ok=True); (OUT / 'data_valid').mkdir(parents=True, exist_ok=True)
LAKE = pathlib.Path('/tmp/nr_lake'); LAKE.mkdir(exist_ok=True)
LOG = []
def log(m): print(m, flush=True); LOG.append(m)
def get(url, timeout=60):
    r = requests.get(url, timeout=timeout, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    r.raise_for_status(); return r.content

def yahoo(sym, rng_, inter):
    raw = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng_}&interval={inter}')
    j = json.loads(raw)['chart']['result'][0]; q = j['indicators']['quote'][0]
    d = pd.DataFrame({'ts': pd.to_datetime(j['timestamp'], unit='s', utc=True),
                      'open': q['open'], 'high': q['high'], 'low': q['low'], 'close': q['close'], 'volume': q.get('volume')})
    return d.dropna(subset=['close'])

def split_save(d, nom):
    d = d.copy(); d['date'] = d.ts.dt.tz_convert('UTC')
    is_ = d[(d.ts >= '2020-01-01') & (d.ts < '2024-01-01')]; va = d[(d.ts >= '2024-01-01') & (d.ts < '2025-01-01')]
    if len(is_): is_.to_parquet(OUT / f'data_is/{nom}.parquet', index=False)
    if len(va): va.to_parquet(OUT / f'data_valid/{nom}.parquet', index=False)
    d.to_parquet(LAKE / f'{nom}_FULL.parquet', index=False)
    return {'fichier': nom, 'lignes': int(len(d)), 'plage': [str(d.ts.min()), str(d.ts.max())],
            'is_nr': int(len(is_)), 'valid_nr': int(len(va)), 'holdout_nr_scele': int((d.ts >= '2025-01-01').sum())}

man = {'genere_utc': str(pd.Timestamp.now(tz='UTC')), 'sources': {}, 'journal': LOG}
for sym, nom in [('GC=F', 'yahoo_gc_daily'), ('XAUUSD=X', 'yahoo_xauusd_daily')]:
    try: man['sources'][nom] = split_save(yahoo(sym, '10y', '1d'), nom); log(f'OK {nom}')
    except Exception as e: man['sources'][nom] = {'statut': f'ECHEC {type(e).__name__} {str(e)[:100]}'}; log(f'ECHEC {nom}: {e}')
for sym, nom in [('GC=F', 'yahoo_gc_hourly'), ('XAUUSD=X', 'yahoo_xauusd_hourly')]:
    try: man['sources'][nom] = split_save(yahoo(sym, '2y', '1h'), nom); log(f'OK {nom}')
    except Exception as e: man['sources'][nom] = {'statut': f'ECHEC {type(e).__name__} {str(e)[:100]}'}; log(f'ECHEC {nom}: {e}')
try:
    d = yahoo('GC=F', '30d', '1m'); d.to_parquet(LAKE / 'yahoo_gc_1min_FULL.parquet', index=False)
    man['sources']['yahoo_gc_1min'] = {'lignes': int(len(d)), 'plage': [str(d.ts.min()), str(d.ts.max())], 'note': 'roulant 30j - lake uniquement'}
    log('OK 1min')
except Exception as e:
    man['sources']['yahoo_gc_1min'] = {'statut': f'ECHEC {type(e).__name__} {str(e)[:100]}'}; log(f'ECHEC 1min: {e}')

# S2 Swissquote snapshot
try:
    raw = get('https://forex-data-feed.swissquote.com/public-quotes/bboquotes/instrument/XAU/USD')
    j = json.loads(raw)
    lignes = []
    def walk(o):
        if isinstance(o, dict):
            if 'bid' in o and 'ask' in o: lignes.append(o)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(j)
    snap = {'ts_utc': str(pd.Timestamp.now(tz='UTC')), 'n_profils': len(lignes),
            'bid_min': min(float(x['bid']) for x in lignes), 'ask_max': max(float(x['ask']) for x in lignes),
            'spread_min_cents': min(float(x['ask']) - float(x['bid']) for x in lignes) * 100}
    sp = LAKE / 'swissquote_spreads.parquet'
    old = pd.read_parquet(sp) if sp.exists() else pd.DataFrame()
    pd.concat([old, pd.DataFrame([snap])]).to_parquet(sp, index=False)
    (OUT / 'SPREADS_SNAPSHOTS.csv').write_text(pd.concat([old, pd.DataFrame([snap])]).to_csv(index=False))
    man['sources']['swissquote_s2'] = snap; log(f'OK S2 spread min {snap["spread_min_cents"]:.0f} cents')
except Exception as e:
    man['sources']['swissquote_s2'] = {'statut': f'ECHEC {type(e).__name__} {str(e)[:100]}'}; log(f'ECHEC S2: {e}')

# S3 Dukascopy qualification: hier, 12h UTC (mois 0-indexe, LZMA .bi5, tick=20 octets)
try:
    hier = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2)
    url = f'https://datafeed.dukascopy.com/datafeed/XAUUSD/{hier.year}/{hier.month - 1:02d}/{hier.day:02d}/12h_ticks.bi5'
    raw = get(url, timeout=120)
    dec = lzma.decompress(raw)
    n = len(dec) // 20
    t0, ask, bid = struct.unpack('>III', dec[:12]) if n else (0, 0, 0)
    man['sources']['dukascopy_s3'] = {'url_test': url, 'octets_compresses': len(raw), 'ticks_decompresses': int(n),
                                      'premier_tick': {'ms_depuis_minuit': int(t0), 'ask_x1000': int(ask), 'bid_x1000': int(bid)},
                                      'statut': 'QUALIFIE' if n > 100 else 'REPONSE PAUVRE'}
    log(f'S3: {n} ticks decompresses')
except Exception as e:
    man['sources']['dukascopy_s3'] = {'statut': f'NON QUALIFIE depuis CI: {type(e).__name__} {str(e)[:120]}'}
    log(f'S3 echec: {e}')
(OUT / 'MANIFEST_NR.json').write_text(json.dumps(man, indent=1, default=str))
log('COLLECTE NR TERMINEE')
