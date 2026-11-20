"""CAMPAGNE 0 - MOTEUR DE BASELINES DESCRIPTIVES (dictionnaire gele seq153/154).
Aucune performance, aucun PnL: distributions de reference V1-V12, IS uniquement.
Barres Mid declarees M1/M5/M15/H1 depuis le tick (lac du programme / repli Drive).
Les tableaux bruts par barre restent en memoire CI; seuls les resumes sont committes."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign00'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT / 'STATE.json'
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)
def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

# regime F3: terciles de la vol predite du jour (modele gele, prevision <= j-1 par construction)
f3 = pd.read_csv('reports/meta_alpha/phase2/f3_har/F3_DAILY_PRED.csv').dropna(subset=['pred_har'])
f3['date'] = pd.to_datetime(f3.day.astype(str)).dt.tz_localize(None).dt.date
q1, q2 = f3.pred_har.quantile([1/3, 2/3]).values
REG = {r.date: ('REGIME_BAS' if r.pred_har <= q1 else ('REGIME_HAUT' if r.pred_har > q2 else 'REGIME_MOYEN')) for r in f3.itertuples()}
def era(d): return 'ERE_2010_2013' if d.year <= 2013 else ('ERE_2014_2016' if d.year <= 2016 else 'ERE_2017_2020')
def session(h): return 'ASIE' if h < 8 else ('LONDRES' if h < 13 else ('NEWYORK' if h < 21 else 'NUIT'))

HORIZONS = {'M1': 1, 'M5': 5, 'M15': 15, 'H1': 60}
ACC = {h: {'r': [], 'amp': [], 'eu': [], 'ed': [], 'sp': [], 'day': [], 'sess': [], 'reg': [], 'era': []} for h in HORIZONS}
DAYS_SEEN = set()

def resample(b1, minutes):
    if minutes == 1: return b1
    b = b1.copy(); b['bucket'] = b.ts.dt.floor(f'{minutes}min')
    g = b.groupby('bucket').agg(o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last'), sp=('sp', 'median'), n=('n', 'sum')).reset_index().rename(columns={'bucket': 'ts'})
    return g

def accumuler(bars):
    bars = bars.sort_values('ts').reset_index(drop=True)
    bars['date'] = bars.ts.dt.date
    for hname, minutes in HORIZONS.items():
        b = resample(bars, minutes) if minutes > 1 else bars
        b = b.copy(); b['date'] = b.ts.dt.date
        for d, g in b.groupby('date'):
            if len(g) < 5: continue
            DAYS_SEEN.add(d)
            r = (g.c.values[1:] / g.o.values[1:] - 1) * 10000  # rendement barre: close vs ouverture de la MEME barre? non: voir ci-dessous
            # V1 gele: rendement barre a barre (close/close precedent) au sein du jour
            cc = g.c.values; r = (cc[1:] / cc[:-1] - 1) * 10000
            amp = (g.h.values - g.l.values) / g.o.values * 10000
            eu = (g.h.values - g.o.values) / g.o.values * 10000
            ed = (g.o.values - g.l.values) / g.o.values * 10000
            A = ACC[hname]
            A['r'].append(r.astype(np.float32)); A['amp'].append(amp[1:].astype(np.float32))
            A['eu'].append(eu[1:].astype(np.float32)); A['ed'].append(ed[1:].astype(np.float32))
            A['sp'].append(g.sp.values[1:].astype(np.float32))
            A['day'].append(np.full(len(r), hash(d) % 100000, np.int32))
            A['sess'].append(np.array([session(x) for x in g.ts.dt.hour.values[1:]]))
            A['reg'].append(np.array([REG.get(d, 'NON_CLASSE')] * len(r)))
            A['era'].append(np.array([era(d)] * len(r)))

def main():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    state = json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done': []}
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute("SET threads=2")
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts:
        if p['name'] not in state['done']: groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    api = None; username = None
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
                print('Kaggle KO, repli Drive:', str(e)[:80], flush=True); localdir = None
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if not pathlib.Path(local).exists():
                if not dl_drive(p.get('drive_id', ''), local, p.get('file_bytes', -1)):
                    state.setdefault('skipped', []).append(p['name']); continue
            try:
                q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts,
                        arg_min(mid, timestamp_utc) AS o, max(mid) AS h, min(mid) AS l,
                        arg_max(mid, timestamp_utc) AS c, median((ask-bid)/mid*10000) AS sp, count(*) AS n
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b1 = con.execute(q).df(); b1['ts'] = pd.to_datetime(b1.ts).dt.tz_localize(None)
                accumuler(b1)
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {type(e).__name__} {e}")
            state['done'].append(p['name']); print('C0 part:', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    # ---- synthese des distributions (aucune performance) ----
    rows = []
    def stats_row(var, hname, cell, x, ndays):
        x = np.asarray(x, dtype=float); x = x[np.isfinite(x)]
        if len(x) == 0: return
        concl = 'RENSEIGNEE' if (len(x) >= 1000 and ndays >= 100) else 'NON CONCLUANTE - effectifs insuffisants'
        rows.append({'variable': var, 'horizon': hname, 'cellule': cell, 'n': int(len(x)), 'journees': int(ndays),
                     'moyenne': round(float(x.mean()), 4), 'ecart_type': round(float(x.std()), 4), 'mediane': round(float(np.median(x)), 4),
                     **{f'P{int(q*100)}': round(float(np.quantile(x, q)), 4) for q in [0.5, 0.75, 0.9, 0.95, 0.99]}, 'statut': concl})
    for hname, A in ACC.items():
        if not A['r']: continue
        r = np.concatenate(A['r']); amp = np.concatenate(A['amp']); eu = np.concatenate(A['eu']); ed = np.concatenate(A['ed']); sp = np.concatenate(A['sp'])
        day = np.concatenate(A['day']); sess = np.concatenate(A['sess']); reg = np.concatenate(A['reg']); er = np.concatenate(A['era'])
        cellules = [('GLOBAL', np.ones(len(r), bool))]
        for s in ['ASIE', 'LONDRES', 'NEWYORK', 'NUIT']: cellules.append((f'SESSION_{s}', sess == s))
        for s in ['REGIME_BAS', 'REGIME_MOYEN', 'REGIME_HAUT']: cellules.append((s, reg == s))
        for s in ['ERE_2010_2013', 'ERE_2014_2016', 'ERE_2017_2020']: cellules.append((s, er == s))
        for cname, m in cellules:
            nd = len(np.unique(day[m])) if m.sum() else 0
            stats_row('V1_RENDEMENT_BP', hname, cname, r[m], nd)
            stats_row('V2_AMPLITUDE_BP', hname, cname, amp[m], nd)
            stats_row('V3_EXCURSION_HAUSSE_BP', hname, cname, eu[m], nd)
            stats_row('V4_EXCURSION_BAISSE_BP', hname, cname, ed[m], nd)
            stats_row('V12_SPREAD_BP', hname, cname, sp[m], nd)
            # V6 persistance + V7 retournements (par cellule, paires intra-jour via masque jour)
            stats_row('V11_QUEUE_EXTREME_PCT_|r|>20BP', hname, cname, (np.abs(r[m]) > 20) * 100, nd)
        # V5 vol realisee journaliere (globale + regime/ere du jour)
        uq, inv_idx = np.unique(day, return_inverse=True)
        rv = np.sqrt(np.bincount(inv_idx, weights=r ** 2))
        stats_row('V5_VOL_REALISEE_JOUR_BP', hname, 'GLOBAL', rv, len(uq))
    # V6/V7/V8/V9/V10 depuis les sequences stockees (par jour, jamais inter-jours)
    for hname, A in ACC.items():
        if not A['r']: continue
        r = np.concatenate(A['r']); amp = np.concatenate(A['amp']); day = np.concatenate(A['day'])
        p90 = np.quantile(np.abs(r), 0.9); med_amp = np.median(amp)
        pair_prod, pair_r2, pair_n, sign_changes, sign_pairs = 0.0, 0.0, 0, 0, 0
        retra, cons_durees, ratios_jour = [], [], []
        for d in np.unique(day):
            m = day == d; rr = r[m]; aa = amp[m]
            if len(rr) > 1:
                pair_prod += float(np.sum(rr[1:] * rr[:-1])); pair_r2 += float(np.sum(rr[:-1] ** 2)); pair_n += len(rr) - 1
                sc = rr[1:] * rr[:-1] < 0; sign_changes += int(sc.sum()); sign_pairs += len(sc)
                run = 0
                for a in aa:
                    if a < med_amp: run += 1
                    elif run: cons_durees.append(run); run = 0
                if run: cons_durees.append(run)
                for i in np.where(np.abs(rr) >= p90)[0]:
                    seg = rr[i + 1:i + 13]
                    if len(seg):
                        adv = -np.sign(rr[i]) * np.cumsum(seg)
                        retra.append(float(np.max(np.maximum(adv, 0)) / abs(rr[i]) * 100))
            ratios_jour.append(float(np.median(aa) / med_amp) if len(aa) else np.nan)
        nd = len(np.unique(day))
        stats_row('V6_PERSISTANCE_CORR_LAG1', hname, 'GLOBAL', np.array([pair_prod / pair_r2 if pair_r2 else np.nan]), nd)
        stats_row('V7_RETOURNEMENTS_PCT', hname, 'GLOBAL', np.array([sign_changes / sign_pairs * 100 if sign_pairs else np.nan]), nd)
        stats_row('V8_RETRACEMENT_PCT_IMPULSION', hname, 'GLOBAL', np.array(retra), nd)
        stats_row('V9_CONSOLIDATION_DUREE_BARRES', hname, 'GLOBAL', np.array(cons_durees, dtype=float), nd)
        stats_row('V10_RATIO_AMPLITUDE_JOUR', hname, 'GLOBAL', np.array(ratios_jour), nd)
    out = pd.DataFrame(rows)
    if len(out): out.to_csv(ROOT / 'CAMPAIGN_00_BASELINE_METRICS.csv', index=False)
    else: print('AUCUNE DONNEE ACCUMULEE - CSV existant preserve')
    (ROOT / 'C0_COVERAGE.json').write_text(json.dumps({'partitions_traitees': len(state['done']), 'partitions_sautees': len(state.get('skipped', [])), 'journees_distinctes': len(DAYS_SEEN)}))
    STATE_P.write_text(json.dumps(state)); print('CAMPAGNE 0 CALCUL TERMINE', len(out))

if __name__ == '__main__': main()
