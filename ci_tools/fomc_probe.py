"""Sonde d'ingenierie: quelles pages officielles federalreserve.gov livrent les dates FOMC pre-2021?"""
import re, requests, pathlib
URLS = [
 'https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm?year=2015',
 'https://www.federalreserve.gov/monetarypolicy/fomcminutes20151216.htm',
 'https://www.federalreserve.gov/newsevents/pressreleases/monetary20151216a.htm',
 'https://www.federalreserve.gov/feeds/press_monetary.xml',
 'https://www.federalreserve.gov/json/calendar.json',
 'https://www.federalreserve.gov/data.json',
 'https://www.federalreserve.gov/monetarypolicy/files/fomc_meeting_calendar_2015.pdf',
 'https://www.federalreserve.gov/monetarypolicy/files/FOMC_Meeting_Calendar_2015.pdf',
 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
]
OUTL=[]
def emit(x): print(x, flush=True); OUTL.append(str(x))
for u in URLS:
    try:
        r = requests.get(u, timeout=60, headers={'User-Agent': 'Mozilla/5.0 (META ALPHA data engineering)'})
        t = r.text
        emit(f'== {u}\n   statut={r.status_code} len={len(t)} type={r.headers.get("content-type")}')
        for pat in [r'fomcminutes20\d{6}', r'monetary20\d{6}[a-z]\.htm', r'FOMC Meeting', r'December 15[-–]16']:
            emit(f'   motif {pat}: {len(re.findall(pat, t))}')
        emit('   extrait: ' + re.sub(r'\s+', ' ', t[:300]))
    except Exception as e:
        emit(f'== {u}\n   ECHEC {type(e).__name__} {str(e)[:120]}')
emit('SONDE TERMINEE')
pathlib.Path('reports/meta_alpha/exogenous/FOMC_PROBE.txt').write_text('\n'.join(OUTL))

# --- profondeur FOMC dans calendar.json ---
import json as _json, collections as _c
try:
    r = requests.get('https://www.federalreserve.gov/json/calendar.json', timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
    evs = _json.loads(r.text).get('events', [])
    emit(f'calendar.json: {len(evs)} evenements, cles={list(evs[0]) if evs else []}')
    fomc = [e for e in evs if 'FOMC' in str(e.get('description','')) or 'FOMC' in str(e.get('title',''))]
    emit(f'evenements FOMC: {len(fomc)}')
    def annee(e): return str(e.get('start_date', e.get('date','')))[:4]
    emit(f'par annee: {dict(sorted(_c.Counter(annee(e) for e in fomc).items()))}')
    for e in fomc[:3] + fomc[-3:]: emit(f"exemple: {e}")
except Exception as e:
    emit(f'calendar ECHEC {type(e).__name__} {str(e)[:120]}')
emit('SONDE2 TERMINEE')
pathlib.Path('reports/meta_alpha/exogenous/FOMC_PROBE.txt').write_text('\n'.join(OUTL))

# --- sonde3: dates fomcminutes dans fomccalendars + calendar decode ---
try:
    h = requests.get('https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm', timeout=60, headers={'User-Agent': 'Mozilla/5.0'}).text
    ds = sorted(set(re.findall(r'fomcminutes(20\d\d)(\d\d)(\d\d)\.htm', h)))
    emit(f'calendars: {len(ds)} dates minutes, de {ds[0]} a {ds[-1]}')
    ms = sorted(set(re.findall(r'monetary(20\d\d)(\d\d)(\d\d)[a-z]\.htm', h)))
    emit(f'calendars: {len(ms)} dates communiques, de {ms[0]} a {ms[-1]}')
except Exception as e: emit(f'sonde3a ECHEC {e}')
try:
    r = requests.get('https://www.federalreserve.gov/json/calendar.json', timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
    evs = _json.loads(r.content.decode('utf-8-sig')).get('events', [])
    fomc = [e for e in evs if 'FOMC' in str(e.get('description','')) or 'FOMC' in str(e.get('event_type','')) or 'FOMC' in str(e.get('title',''))]
    emit(f'calendar: {len(evs)} evts, FOMC={len(fomc)}')
    for e in fomc[:2] + fomc[-2:]: emit(f'ex: {e}')
    dates = sorted(str(e.get('start_date',''))[:10] for e in fomc)
    emit(f'calendar FOMC dates: {dates[:3]} ... {dates[-3:]}' if dates else 'calendar FOMC: aucune date')
except Exception as e: emit(f'sonde3b ECHEC {type(e).__name__} {str(e)[:120]}')
emit('SONDE3 TERMINEE')
pathlib.Path('reports/meta_alpha/exogenous/FOMC_PROBE.txt').write_text('\n'.join(OUTL))

# --- sonde4: couverture calendar FOMC Meeting + liens minutes 2015 ---
try:
    r = requests.get('https://www.federalreserve.gov/json/calendar.json', timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
    evs = _json.loads(r.content.decode('utf-8-sig')).get('events', [])
    mtg = [e for e in evs if e.get('title') == 'FOMC Meeting']
    mois = [e.get('month','') for e in mtg if e.get('month')]
    emit(f'FOMC Meeting: {len(mtg)}; mois min={min(mois)} max={max(mois)}')
    emit(f'par annee reunion: {dict(sorted(_c.Counter(m[:4] for m in mois).items()))}')
except Exception as e: emit(f'sonde4a ECHEC {e}')
try:
    h = requests.get('https://www.federalreserve.gov/monetarypolicy/fomcminutes20151216.htm', timeout=60, headers={'User-Agent': 'Mozilla/5.0'}).text
    lf = sorted(set(re.findall(r'fomcminutes(20[0-9]{6})[.]htm', h)))
    lm = sorted(set(re.findall(r'monetary(20[0-9]{6})[a-z][.]htm', h)))
    emit('minutes 20151216 liens fomcminutes: ' + str(lf))
    emit('minutes 20151216 liens monetary: ' + str(lm))
except Exception as e: emit(f'sonde4b ECHEC {e}')
emit('SONDE4 TERMINEE')
pathlib.Path('reports/meta_alpha/exogenous/FOMC_PROBE.txt').write_text('\n'.join(OUTL))

# --- sonde5: structure des liens de la page archives historiques ---
try:
    h = requests.get('https://www.federalreserve.gov/monetarypolicy/fomc_historical_year.htm?year=2015', timeout=60, headers={'User-Agent': 'Mozilla/5.0'}).text
    hrefs = sorted(set(re.findall(r'href="([^"]+)"', h)))
    sel = [x for x in hrefs if any(k in x.lower() for k in ['fomc', 'minutes', 'calendar', 'monetary'])]
    emit('archives hrefs pertinents (' + str(len(sel)) + '):')
    for x in sel[:40]: emit('  ' + x)
    txt = re.sub(r'<[^>]+>', ' ', h); txt = re.sub(r'\s+', ' ', txt)
    i = txt.lower().find('historical')
    emit('texte autour de historical: ' + txt[max(0,i-100):i+400])
except Exception as e: emit('sonde5 ECHEC ' + type(e).__name__ + ' ' + str(e)[:100])
emit('SONDE5 TERMINEE')
pathlib.Path('reports/meta_alpha/exogenous/FOMC_PROBE.txt').write_text('\n'.join(OUTL))
