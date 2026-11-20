"""CAMPAGNE 1.1 - EV4, EV7, OUVERTURES (definitions litterales du dictionnaire seq157).
Descriptif seul, aucun PnL. Reutilise le chargement tick de la campagne 1."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign01_1'); ROOT.mkdir(parents=True, exist_ok=True)
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)
def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

f3 = pd.read_csv('reports/meta_alpha/phase2/f3_har/F3_DAILY_PRED.csv').dropna(subset=['pred_har'])
f3['date'] = pd.to_datetime(f3.day.astype(str)).dt.tz_localize(None).dt.date
q1, q2 = f3.pred_har.quantile([1/3, 2/3]).values
REG = {r.date: ('BAS' if r.pred_har <= q1 else ('HAUT' if r.pred_har > q2 else 'MOYEN')) for r in f3.itertuples()}
def era(d): return '2010_2013' if d.year <= 2013 else ('2014_2016' if d.year <= 2016 else '2017_2020')

def charger():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute("SET threads=2")
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts: groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    frames, api, username = [], None, None
    for batch, ps in groups.items():
        localdir = None
        if batch != 'DRIVE' and os.environ.get('KAGGLE_API_TOKEN'):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi(); api.authenticate(); username = api.config_values.get('username')
                localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True)
                api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True)
            except Exception as e:
                print('Kaggle KO repli Drive', str(e)[:80], flush=True); localdir = None
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if not pathlib.Path(local).exists():
                if not dl_drive(p.get('drive_id', ''), local, p.get('file_bytes', -1)): continue
            try:
                q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts, arg_min(mid, timestamp_utc) AS o,
                        max(mid) AS h, min(mid) AS l, arg_max(mid, timestamp_utc) AS c, median((ask-bid)/mid*10000) AS sp
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b)
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C1.1 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

OPENS = {'ASIE': 0, 'LONDRES': 8, 'NEWYORK': 13}
def main():
    bars = charger(); bars['date'] = bars.ts.dt.date; bars['heure'] = bars.ts.dt.hour
    jours = {d: g.reset_index(drop=True) for d, g in bars.groupby('date')}; dates = sorted(jours)
    day_ranges = {d: float((g.h.max() - g.l.min()) / g.o.iloc[0] * 10000) for d, g in jours.items() if len(g) >= 300}
    P95_JOUR = float(np.quantile(list(day_ranges.values()), 0.95))
    ev4, ev7, opens = [], [], []
    ranges60_hist = []
    for di, d in enumerate(dates):
        g = jours[d]
        if len(g) < 300: continue
        reg, er = REG.get(d, 'NON_CLASSE'), era(d)
        # EV4: range 60 min glissant vs seuil causal (5 jours precedents)
        r60 = np.array([float((g.h.iloc[max(0, i - 59):i + 1].max() - g.l.iloc[max(0, i - 59):i + 1].min()) / g.c.iloc[i] * 10000) for i in range(len(g))])
        if len(ranges60_hist) >= 200:
            thr = 0.6 * float(np.median(ranges60_hist[-5 * 1440:])) if ranges60_hist else np.nan
            if np.isfinite(thr):
                i = 60
                while i < len(g):
                    if r60[i] < thr:
                        j = i
                        while j < len(g) and r60[j] < thr and j - i < 240: j += 1
                        duree = j - i
                        w = g.iloc[j:j + 60]
                        exp_range = float((w.h.max() - w.l.min()) / g.c.iloc[j] * 10000) if len(w) else np.nan
                        ev4.append({'date': str(d), 'regime': reg, 'ere': er, 'session': 'ASIE' if g.ts.iloc[i].hour < 8 else ('LONDRES' if g.ts.iloc[i].hour < 13 else ('NEWYORK' if g.ts.iloc[i].hour < 21 else 'NUIT')),
                                    'duree_compression_min': int(duree), 'range_comprime_bp': float(r60[i]), 'seuil_bp': float(thr),
                                    'expansion_range_60_suivantes_bp': exp_range, 'expansion_1_5x': float(exp_range >= 1.5 * r60[i]) if np.isfinite(exp_range) else np.nan,
                                    'spread_event': float(g.sp.iloc[i])})
                        i = j
                    else: i += 1
        ranges60_hist.extend(r60[::10].tolist())
        # EV7: journee extreme + formation des extremes hebdomadaires
        if day_ranges.get(d, 0) > P95_JOUR:
            ev7.append({'date': str(d), 'regime': reg, 'ere': er, 'range_jour_bp': day_ranges[d], 'jour_semaine': int(pd.Timestamp(d).dayofweek),
                        'heure_formation_haut': int(g.loc[g.h.idxmax(), 'ts'].hour), 'heure_formation_bas': int(g.loc[g.l.idxmin(), 'ts'].hour)})
        # Ouvertures de sessions
        for nom, h0 in OPENS.items():
            w = g[(g.ts.dt.hour >= h0 - 1) & (g.ts.dt.hour < h0 + 1)]
            avant = w[w.ts.dt.hour == h0 - 1].tail(30); apres = w[w.ts.dt.hour == h0]
            if len(avant) < 10 or len(apres) < 30: continue
            p0 = float(apres.o.iloc[0]); r5 = float((apres.iloc[:5].h.max() - apres.iloc[:5].l.min()) / p0 * 10000)
            r60 = float((apres.h.max() - apres.l.min()) / p0 * 10000)
            cum = np.maximum.accumulate(apres.h.values) - np.minimum.accumulate(apres.l.values)
            vitesse = int(np.argmax(cum >= 0.5 * cum[-1])) if cum[-1] > 0 else np.nan
            opens.append({'ouverture': nom, 'heure_utc': h0, 'date': str(d), 'regime': reg, 'ere': er,
                          'spread_avant_med_bp': float(avant.sp.median()), 'spread_apres_med_bp': float(apres.sp.median()),
                          'range_5min_bp': r5, 'range_60min_bp': r60, 'vitesse_50pct_range_min': vitesse,
                          'mouvement_extreme_5min': float(r5 > 20), 'n_barres_apres': int(len(apres))})
    E4, E7, O = pd.DataFrame(ev4), pd.DataFrame(ev7), pd.DataFrame(opens)
    rows = []
    for fam, X in [('EV4_COMPRESSION', E4), ('EV7_JOURNEES_EXTREMES', E7)]:
        if not len(X): continue
        rows.append({'famille': fam, 'n': int(len(X)), 'journees': int(X.date.nunique())})
    pd.DataFrame(rows).to_csv(ROOT / 'CAMPAIGN_01_1_EVENT_METRICS.csv', index=False)
    E4.to_csv(ROOT / 'EV4_EVENTS.csv', index=False); E7.to_csv(ROOT / 'EV7_EVENTS.csv', index=False)
    O.to_csv(ROOT / 'CAMPAIGN_01_1_SESSION_OPENINGS.csv', index=False)
    (ROOT / 'C11_COVERAGE.json').write_text(json.dumps({'EV4': int(len(E4)), 'EV7': int(len(E7)), 'ouvertures': int(len(O)), 'P95_range_jour_bp': P95_JOUR}))
    print('C1.1 TERMINE', len(E4), len(E7), len(O))

if __name__ == '__main__': main()
