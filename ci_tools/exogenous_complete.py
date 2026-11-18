"""PACK EXOGENE - COMPLETION (seq103). INGENIERIE SEULE, 0 analyse.
C1: calendrier macro point-in-time ALFRED (vintages), available_at = vintage + heure de
publication ET convertie date par date via America/New_York (DST) - jamais de decalage fixe.
C2: DFII10, GVZCLS + DGS10/DGS2 officiels FRED (les proxys Yahoo seq102 restent au manifeste).
C3: GLD/IAU clos (consigne au manifeste, aucun substitut).
La cle FRED_API_KEY vient de l'environnement CI: jamais affichee, jamais loguee.
Prerequis dans le meme job: exogenous_collect.py a regenere les dossiers v1 (data_is, /tmp/pack_*)."""
import io, json, os, re, time, hashlib, pathlib, datetime as dt
import pandas as pd, requests
from zoneinfo import ZoneInfo

OUT = pathlib.Path('reports/meta_alpha/exogenous')
IS_END = pd.Timestamp('2020-01-20 09:36:27', tz='UTC')
OOS_END = pd.Timestamp('2023-12-31 23:59:59', tz='UTC')
KEY = os.environ.get('FRED_API_KEY', '').strip()
def sanitize(x):
    return re.sub(r'api_key=[^&\s\'\"]+', 'api_key=REDACTED', str(x))
API = 'https://api.stlouisfed.org/fred'
NY = ZoneInfo('America/New_York')
LOG = []
def log(m): print(m, flush=True); LOG.append(m)
def sha(b): return hashlib.sha256(b).hexdigest()
if not KEY:
    log('FRED_API_KEY ABSENTE de l environnement: collecte FRED impossible (fail-closed, rien fabrique)')

def api_get(path, params, essais=5):
    params = dict(params); params['api_key'] = KEY; params['file_type'] = 'json'
    last = None
    for i in range(essais):
        try:
            r = requests.get(f'{API}{path}', params=params, timeout=60,
                             headers={'User-Agent': 'META ALPHA data engineering'})
            if r.status_code == 429:
                time.sleep(20 * (i + 1)); continue
            if r.status_code >= 400:
                try: msg = r.json().get('error_message', r.text[:150])
                except Exception: msg = r.text[:150]
                raise ValueError(f'FRED HTTP {r.status_code}: {sanitize(msg)}')
            return r.json()
        except Exception as e:
            last = e; log(f'retry {i+1} {path}: {type(e).__name__}'); time.sleep(10 * (2 ** i))
    raise last

def dispo(vintage: dt.date, heure: int, minute: int = 0) -> pd.Timestamp:
    """vintage_date + heure de publication ET -> UTC, conversion DST date par date."""
    local = dt.datetime(vintage.year, vintage.month, vintage.day, heure, minute, tzinfo=NY)
    return pd.Timestamp(local).tz_convert('UTC')

H_PUB = {'PAYEMS': (8, 30), 'UNRATE': (8, 30), 'CPIAUCSL': (8, 30), 'CPIAUCNS': (8, 30),
         'PCEPI': (8, 30), 'PCEPILFE': (8, 30), 'GDP': (8, 30), 'ICSA': (8, 30),
         'DFEDTARU': (14, 0), 'DFEDTARL': (14, 0), 'FEDFUNDS': (14, 0)}
frames, meta = {}, {}

def pit_series(sid):
    """ALFRED natif: un appel toutes-vintages; chaque ligne = une VERSION d'observation,
    vintage_date = realtime_start (date d'apparition de cette version). Point-in-time exact,
    sans requeter l'historique complet a chaque vintage (run2: timeout 300 min, consigne)."""
    h, mnt = H_PUB[sid]
    rows = []
    for an in range(2009, dt.date.today().year + 1):
        fin = min(dt.date(an, 12, 31), dt.date.today()).isoformat()
        offset = 0
        while True:
            o = api_get('/series/observations', {'series_id': sid, 'realtime_start': f'{an}-01-01',
                                                 'realtime_end': fin, 'observation_start': '2009-01-01',
                                                 'limit': 100000, 'offset': offset})
            obs = o.get('observations', [])
            for ob in obs:
                if ob['value'] != '.':
                    v = dt.date.fromisoformat(ob['realtime_start'])
                    rows.append((ob['date'], str(v), dispo(v, h, mnt), float(ob['value'])))
            offset += len(obs)
            if len(obs) < 100000: break
            time.sleep(0.55)
        log(f'{sid}: millesime {an} traite (cumule {len(rows)} versions)')
    return pd.DataFrame(rows, columns=['reference_date', 'vintage_date', 'available_at_utc', 'value']).drop_duplicates()

if KEY:
    for sid in H_PUB:
        try:
            d = pit_series(sid)
            if len(d):
                frames[f'macro_{sid.lower()}_pit'] = d
                meta[f'macro_{sid.lower()}_pit'] = {
                    'source': f'ALFRED/FRED API series_id={sid} (vintages point-in-time)', 'frequence': 'panel de vintages',
                    'convention_available_at': f'vintage_date + {H_PUB[sid][0]:02d}:{H_PUB[sid][1]:02d} America/New_York converti UTC date par date (DST)',
                    'lignes': int(len(d)), 'vintages': int(d.vintage_date.nunique()),
                    'plage_reference': [str(d.reference_date.min()), str(d.reference_date.max())],
                    'plage_vintage': [str(d.vintage_date.min()), str(d.vintage_date.max())]}
                log(f'OK macro_{sid.lower()}_pit: {len(d)} obs, {d.vintage_date.nunique()} vintages')
            else:
                meta[f'macro_{sid.lower()}_pit'] = {'source': f'ALFRED {sid}', 'statut': 'AUCUNE DONNEE RENVOYEE'}
        except Exception as e:
            log(f'ECHEC PIT {sid}: {type(e).__name__} {str(e)[:100]}')
            meta[f'macro_{sid.lower()}_pit'] = {'source': f'ALFRED {sid}', 'statut': 'ECHEC COLLECTE', 'motif': sanitize(e)[:200]}
            if sid == 'DFEDTARU' and 'does not exist in ALFRED' in str(e):
                try:
                    o = api_get('/series/observations', {'series_id': sid, 'observation_start': '2009-01-01', 'limit': 100000})
                    rows = [(ob['date'], ob['date'], dispo(dt.date.fromisoformat(ob['date']), 14, 0), float(ob['value']))
                            for ob in o.get('observations', []) if ob['value'] != '.']
                    d = pd.DataFrame(rows, columns=['reference_date', 'vintage_date', 'available_at_utc', 'value']).drop_duplicates()
                    frames[f'macro_{sid.lower()}_pit'] = d
                    meta[f'macro_{sid.lower()}_pit'] = {
                        'source': 'FRED API DFEDTARU (ALFRED: serie absente, message FRED consigne au journal)',
                        'frequence': 'daily (borne cible, change aux decisions)',
                        'convention_available_at': 'jour de decision 14:00 America/New_York converti UTC date par date (DST)',
                        'note_pit': 'serie d evenement de politique monetaire (valeur fixee par le communique FOMC, non revisee); pas de panel de vintages ALFRED disponible',
                        'lignes': int(len(d)), 'plage_reference': [str(d.reference_date.min()), str(d.reference_date.max())]}
                    log(f'OK macro_dfedtaru_pit (repli documente): {len(d)} lignes')
                except Exception as e2:
                    log(f'ECHEC repli DFEDTARU: {type(e2).__name__} {sanitize(e2)[:100]}')
    # C2: series officielles courantes
    for sid, nom in [('DFII10', 'fred_dfii10_officiel'), ('GVZCLS', 'fred_gvz_officiel'),
                     ('DGS10', 'fred_dgs10_officiel'), ('DGS2', 'fred_dgs2_officiel')]:
        try:
            o = api_get('/series/observations', {'series_id': sid, 'observation_start': '2003-01-01', 'limit': 100000})
            rows = [(ob['date'], float(ob['value'])) for ob in o.get('observations', []) if ob['value'] != '.']
            d = pd.DataFrame(rows, columns=['reference_date', 'value'])
            d['available_at_utc'] = pd.to_datetime(d.reference_date, utc=True) + pd.Timedelta(days=1)
            frames[nom] = d[['reference_date', 'available_at_utc', 'value']]
            meta[nom] = {'source': f'FRED API series_id={sid} (officiel, remplace le proxy Yahoo seq102 comme reference primaire)',
                         'frequence': 'daily', 'convention_available_at': 'reference_date + 1 jour 00:00 UTC (conservateur)',
                         'lignes': int(len(d)), 'plage_reference': [str(d.reference_date.min()), str(d.reference_date.max())]}
            log(f'OK {nom}: {len(d)} lignes')
        except Exception as e:
            log(f'ECHEC C2 {sid}: {type(e).__name__} {str(e)[:100]}')
            meta[nom] = {'source': f'FRED {sid}', 'statut': 'ECHEC COLLECTE (manquant documente, aucun proxy reconstruit)', 'motif': sanitize(e)[:200]}

# ---- FOMC: dates de reunion (source federalreserve.gov) ----
MOIS = {m: i + 1 for i, m in enumerate(['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])}
def fomc_events():
    ev = {}
    urls = ['https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'] + \
           [f'https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm?year={y}' for y in range(2010, 2027)]
    for url in urls:
        try:
            html = requests.get(url, timeout=60, headers={'User-Agent': 'Mozilla/5.0'}).text
            txt = re.sub(r'<[^>]+>', ' ', html); txt = re.sub(r'\s+', ' ', txt)
            for mm in re.finditer(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})[-–](\d{1,2}),?\s+(20\d\d)', txt):
                d2 = dt.date(int(mm.group(4)), MOIS[mm.group(1).lower()], int(mm.group(3)))
                ev[d2] = dt.date(int(mm.group(4)), MOIS[mm.group(1).lower()], int(mm.group(2)))
            for mm in re.finditer(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(20\d\d)', txt):
                d2 = dt.date(int(mm.group(3)), MOIS[mm.group(1).lower()], int(mm.group(2)))
                ev.setdefault(d2, d2)
            annees = sorted(set(re.findall(r'20\d\d', txt)))[:8]
            log(f'FOMC page annees detectees: {annees}')
            for ym in re.finditer(r'(20\d\d) FOMC Meetings(.*?)(?=20\d\d FOMC Meetings|$)', txt):
                an = int(ym.group(1))
                for mm in re.finditer(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})[-–](\d{1,2})', ym.group(2)):
                    d2 = dt.date(an, MOIS[mm.group(1).lower()], int(mm.group(3)))
                    ev[d2] = dt.date(an, MOIS[mm.group(1).lower()], int(mm.group(2)))
            log(f'FOMC source OK: {url[:70]} (cumule {len(ev)} reunions)')
        except Exception as e:
            log(f'FOMC source ECHEC {url[:70]}: {type(e).__name__}')
    rows = [{'reference_date': pd.Timestamp(d2), 'available_at_utc': dispo(d2, 14, 0),
             'event': 'FOMC_statement', 'meeting_start': str(d1), 'meeting_end': str(d2)} for d2, d1 in sorted(ev.items())]
    return pd.DataFrame(rows)

def fomc_events_archives():
    """Dates de reunion pre-2021: liens officiels fomcminutesAAAAMMJJ.htm des pages
    d'archives federalreserve.gov (la date du lien = jour 2 de reunion). Aucune date inventee."""
    ev = {}
    for y in range(2010, 2027):
        for url in [f'https://www.federalreserve.gov/monetarypolicy/fomchistorical{y}.htm',
                    f'https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm?year={y}',
                    f'https://www.federalreserve.gov/monetarypolicy/fomcminutes{y}index.htm']:
            try:
                html = requests.get(url, timeout=60, headers={'User-Agent': 'Mozilla/5.0'}).text
                trouve = 0
                for mm in re.finditer(r'fomcminutes(20\d\d)(\d\d)(\d\d)\.htm', html):
                    d2 = dt.date(int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
                    if d2 not in ev: ev[d2] = d2; trouve += 1
                for mm in re.finditer(r'monetary(20\d\d)(\d\d)(\d\d)[a-z]\.htm', html):
                    d2 = dt.date(int(mm.group(1)), int(mm.group(2)), int(mm.group(3)))
                    if d2 not in ev: ev[d2] = d2; trouve += 1
                log(f'FOMC archives {y}: longueur html={len(html)}')
                log(f'FOMC archives {y} {url[45:75]}: +{trouve} (cumule {len(ev)})')
            except Exception as e:
                log(f'FOMC archives ECHEC {y}: {type(e).__name__}')
    rows = [{'reference_date': pd.Timestamp(d2), 'available_at_utc': dispo(d2, 14, 0),
             'event': 'FOMC_statement', 'meeting_start': '', 'meeting_end': str(d2)} for d2 in sorted(ev)]
    return pd.DataFrame(rows)
def fomc_calendar_json():
    """Calendrier officiel federalreserve.gov/json/calendar.json: evenements 'FOMC Meeting',
    jour 2 = month (AAAA-MM) + days. Source officielle, aucune date inventee."""
    import json as _json
    r = requests.get('https://www.federalreserve.gov/json/calendar.json', timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
    evs = _json.loads(r.content.decode('utf-8-sig')).get('events', [])
    rows = []
    for e in evs:
        if e.get('title') != 'FOMC Meeting': continue
        mth, dys = str(e.get('month', '')), str(e.get('days', ''))
        if len(mth) != 7 or not dys.isdigit(): continue
        d2 = dt.date(int(mth[:4]), int(mth[5:7]), int(dys))
        desc = re.sub(r'<[^>]+>', ' ', str(e.get('description', '')))
        mm = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s*[-\u2013]\s*(?:(January|February|March|April|May|June|July|August|September|October|November|December)\s+)?(\d{1,2})', desc)
        d1 = ''
        if mm:
            m1 = MOIS[mm.group(1).lower()]; j1 = int(mm.group(2))
            y1 = d2.year - (1 if (m1 == 12 and d2.month == 1) else 0)
            d1 = str(dt.date(y1, m1, j1))
        rows.append({'reference_date': pd.Timestamp(d2), 'available_at_utc': dispo(d2, 14, 0),
                     'event': 'FOMC_statement', 'meeting_start': d1, 'meeting_end': str(d2)})
    log(f'FOMC calendar.json: {len(rows)} reunions')
    return pd.DataFrame(rows)

try:
    fe = pd.concat([fomc_events(), fomc_events_archives(), fomc_calendar_json()]).drop_duplicates('reference_date').sort_values('reference_date')
    if len(fe):
        frames['fomc_events'] = fe
        meta['fomc_events'] = {'source': 'federalreserve.gov (calendriers FOMC officiels + json/calendar.json officiel)', 'frequence': 'evenement',
                               'convention_available_at': 'jour 2 de reunion, 14:00 America/New_York converti UTC date par date (DST)',
                               'lignes': int(len(fe)), 'plage_reference': [str(fe.reference_date.min()), str(fe.reference_date.max())]}
        log(f'OK fomc_events: {len(fe)} reunions')
    else:
        meta['fomc_events'] = {'source': 'federalreserve.gov', 'statut': 'NON COLLECTE: aucune date parsee (aucune fabrication)'}
except Exception as e:
    meta['fomc_events'] = {'source': 'federalreserve.gov', 'statut': f'ECHEC {sanitize(e)[:150]}'}

# ---- Integration aux dossiers v1 regeneres + decoupage + VERIFY integral ----
folders = {'is': OUT / 'data_is', 'oos': pathlib.Path('/tmp/pack_oos'), 'holdout': pathlib.Path('/tmp/pack_holdout')}
for pk, d in folders.items(): d.mkdir(parents=True, exist_ok=True)
for nom, df in frames.items():
    df = df.copy()
    df['reference_date'] = pd.to_datetime(df['reference_date'], utc=True)
    df['available_at_utc'] = pd.to_datetime(df['available_at_utc'], utc=True)
    a = df.available_at_utc
    for pk, part in [('is', df[a <= IS_END]), ('oos', df[(a > IS_END) & (a <= OOS_END)]), ('holdout', df[a > OOS_END])]:
        if len(part): part.to_parquet(folders[pk] / f'{nom}.parquet', index=False)
mani_path = OUT / 'MANIFEST.json'
mani = json.loads(mani_path.read_text()) if mani_path.exists() else {}
mani.setdefault('series', {}).update(meta)
mani['completion_seq103'] = {'genere_utc': str(pd.Timestamp.now(tz='UTC')), 'journal': [sanitize(x) for x in LOG],
                             'note_c2': 'versions FRED officielles = reference primaire; proxys Yahoo seq102 conserves et consignes'}
mani['series']['macro_calendrier_pit'] = {'statut': 'SUPERSEDE par la completion seq103 (series macro_*_pit ALFRED ci-dessus)'}
mani['series']['etf_gld_iau_shares'] = {'statut': 'CLOTURE DEFINITIVE (C3, seq104)',
    'motif': 'historique des flux (shares outstanding) non certifiable gratuitement - manquant definitif',
    'interdiction': 'le volume daily GLD existe mais volume != flux: interdiction absolue de l utiliser comme substitut dans toute hypothese future; famille non re-visitable sans source nouvelle certifiable'}
mani_path.write_text(json.dumps(mani, indent=1, default=str))
verify = {}
for pk, d in folders.items():
    files = {f.name: {'sha256': sha(f.read_bytes()), 'taille': f.stat().st_size} for f in sorted(d.glob('*.parquet'))}
    audit = None
    if pk == 'is':
        mx = None
        for fn in files:
            m = pd.read_parquet(d / fn).available_at_utc.max()
            mx = m if mx is None or m > mx else mx
        audit = {'max_available_at_utc_expose': str(mx), 'borne': str(IS_END), 'passe': bool(mx is not None and mx <= IS_END)}
    verify[pk] = {'fichiers': files, 'audit_anti_fuite': audit,
                  'statut': 'EXPOSE' if pk == 'is' else 'SCELLE (upload seul, aucun telechargement par un moteur)'}
    (OUT / f'VERIFY_{pk.upper()}.json').write_text(json.dumps(verify[pk], indent=1, default=str))
log(f"COMPLETION TERMINEE: audit IS passe={verify['is']['audit_anti_fuite']}")
