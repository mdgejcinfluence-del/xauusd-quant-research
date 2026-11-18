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
