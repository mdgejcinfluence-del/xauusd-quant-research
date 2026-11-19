"""PHASE 9 CARRY - collecte data.binance.vision (funding USDT-M mensuel) + qualification Hyperliquid.
Selection des candidats par profondeur (metrics OI si dispo, sinon volume klines), jamais par le funding.
Sortie brute: reports/meta_alpha/phase9/carry/FUNDING_<SYM>.csv + CARRY_RAW.json (stats descriptives par symbole liste)."""
import io, json, pathlib, zipfile, datetime as dt
import pandas as pd, requests

OUT = pathlib.Path('reports/meta_alpha/phase9/carry'); OUT.mkdir(parents=True, exist_ok=True)
LOG = []
def log(m): print(m, flush=True); LOG.append(str(m))
S = requests.Session(); S.headers.update({'User-Agent': 'Mozilla/5.0 (META ALPHA data engineering)'})
BASE = 'https://data.binance.vision/data/futures/um'

def liste_symboles():
    r = S.get('https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/monthly/fundingRate/', timeout=60)
    import re
    syms = sorted(set(re.findall(r'fundingRate/([A-Z0-9]+USDT)/', r.text)))
    return syms

def telecharge(url):
    r = S.get(url, timeout=60)
    if r.status_code != 200: return None
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content)); n = z.namelist()[0]
        return z.read(n)
    except Exception: return None

def profondeur(sym):
    """OI moyen recent via monthly metrics (dernier mois dispo), repli volume klines."""
    for an, mo in [(2026, 10), (2026, 9), (2025, 12)]:
        raw = telecharge(f'{BASE}/monthly/metrics/{sym}/{sym}-metrics-{an}-{mo:02d}.zip')
        if raw:
            try:
                d = pd.read_csv(io.BytesIO(raw))
                col = [c for c in d.columns if 'open_interest' in c.lower()]
                if col: return float(d[col[0]].astype(float).mean()), 'OI metrics'
            except Exception: pass
    for an, mo in [(2026, 10), (2025, 12)]:
        raw = telecharge(f'{BASE}/monthly/klines/{sym}/1d/{sym}-1d-{an}-{mo:02d}.zip')
        if raw:
            try:
                d = pd.read_csv(io.BytesIO(raw), header=None)
                return float(pd.to_numeric(d[7], errors='coerce').sum()), 'volume quote klines (proxy)'
            except Exception: pass
    return 0.0, 'indisponible'

def funding(sym):
    frames = []
    d = dt.date(2020, 1, 1)
    while d <= dt.date(2026, 11, 1):
        raw = telecharge(f'{BASE}/monthly/fundingRate/{sym}/{sym}-fundingRate-{d.year}-{d.month:02d}.zip')
        if raw:
            try:
                x = pd.read_csv(io.BytesIO(raw))
                frames.append(x)
            except Exception as e: log(f'{sym} {d}: csv illisible {e}')
        d = (d.replace(day=28) + dt.timedelta(days=7)).replace(day=1)
    if not frames: return None
    f = pd.concat(frames).drop_duplicates()
    f.columns = [c.strip() for c in f.columns]
    return f

res = {'genere': str(pd.Timestamp.now(tz='UTC')), 'journal': LOG}
try:
    syms = liste_symboles(); res['symboles_listes'] = len(syms); log(f'{len(syms)} symboles listes')
except Exception as e:
    syms = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'LINKUSDT', 'AVAXUSDT']
    res['symboles_listes'] = f'ECHEC listing ({e}) - repli liste majeure declaree'
    log('listing echoue, repli liste majeure')
profondeurs = {}
for s in syms[:60]:
    p, src = profondeur(s)
    if p > 0: profondeurs[s] = {'valeur': p, 'source': src}
res['profondeurs'] = profondeurs
candidats = [s for s, _ in sorted(profondeurs.items(), key=lambda kv: -kv[1]['valeur'])[:8]]
res['candidats_par_profondeur'] = candidats
log(f'candidats: {candidats}')
for s in candidats:
    f = funding(s)
    if f is None: res[s] = {'statut': 'AUCUN FUNDING'}; continue
    f.to_csv(OUT / f'FUNDING_{s}.csv', index=False)
    res[s] = {'lignes': int(len(f)), 'colonnes': list(f.columns)}
    log(f'{s}: {len(f)} lignes funding')
# Hyperliquid qualification
try:
    r = S.post('https://api.hyperliquid.xyz/info', json={'type': 'fundingHistory', 'coin': 'BTC', 'startTime': 1700000000000}, timeout=30)
    res['hyperliquid'] = {'statut': r.status_code, 'reponse_debut': r.text[:200]}
except Exception as e:
    res['hyperliquid'] = {'statut': f'ECHEC {type(e).__name__} {str(e)[:100]}'}
log(f"hyperliquid: {res['hyperliquid']}")
(OUT / 'CARRY_RAW.json').write_text(json.dumps(res, indent=1, default=str))
print('COLLECTE CARRY TERMINEE')
