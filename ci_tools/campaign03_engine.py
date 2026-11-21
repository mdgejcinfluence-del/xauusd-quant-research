"""CAMPAGNE 3 - cartographie causale impulsions/consolidations (descriptif).
Dictionnaire gele seq185-186 (sha256 76490c40...), comparaisons gelees seq189.
Seuils toujours causaux (passe seul, barre courante exclue); variables
d'instantane closes a l'instantane; issues strictement apres l'instantane."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback, bisect
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign03'); ROOT.mkdir(parents=True, exist_ok=True)
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)
SEED = 20261113

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
def sess(h): return 'ASIE' if h < 8 else ('LONDRES' if h < 13 else ('NEWYORK' if h < 21 else 'NUIT'))

CHARGER_STATS = {'chargees': 0, 'attendues': 0}
def charger():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    CHARGER_STATS['attendues'] = len(parts)
    print('C3 ALL', len(parts), 'partitions attendues', flush=True)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute("SET threads=2")
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts: groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    frames, api, username = [], None, None
    for batch, ps in groups.items():
        localdir = None
        tok = os.environ.get('KAGGLE_API_TOKEN', '')
        if tok:
            try:
                import requests, zipfile, io
                url = f'https://www.kaggle.com/api/v1/datasets/download/shalom5123/{batch}'
                r = None
                for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None), ({}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
                    r = requests.get(url, headers=hdrs, auth=auth, timeout=600)
                    print('direct Kaggle', batch, r.status_code, flush=True)
                    if r.status_code == 200: break
                if r is not None and r.status_code == 200:
                    localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True); pathlib.Path(localdir).mkdir(parents=True)
                    zipfile.ZipFile(io.BytesIO(r.content)).extractall(localdir)
                    print('direct Kaggle OK', batch, len(list(pathlib.Path(localdir).glob('*'))), flush=True)
            except Exception as e:
                print('direct Kaggle KO', str(e)[:100], flush=True); localdir = None
        if localdir is None and batch != 'DRIVE' and os.environ.get('KAGGLE_API_TOKEN'):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi(); api.authenticate(); username = 'shalom5123'
                localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True)
                for _try in range(2):
                    try:
                        api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True); break
                    except Exception:
                        if _try == 1: raise
                        time.sleep(30)
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
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b); CHARGER_STATS['chargees'] += 1
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C3 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives causales (testees par campaign03_temporal_tests.py) ----------
def causal_quantile_series(ts_ns, values, window_ns, q, min_count):
    """Version effective : fenetre [t-window, t), exclusion de la barre courante."""
    from collections import deque
    n = len(values); out = np.full(n, np.nan); cnt = np.zeros(n, dtype=int)
    dq = deque(); srt = []
    for i in range(n):
        t = int(ts_ns[i])
        while dq and dq[0][0] < t - window_ns:
            _, v = dq.popleft()
            j = bisect.bisect_left(srt, v)
            if j < len(srt) and srt[j] == v: srt.pop(j)
        cnt[i] = len(srt)
        if len(srt) >= min_count:
            pos = q * (len(srt) - 1); lo = int(np.floor(pos)); hi = min(lo + 1, len(srt) - 1)
            out[i] = srt[lo] + (srt[hi] - srt[lo]) * (pos - lo)
        dq.append((t, float(values[i]))); bisect.insort(srt, float(values[i]))
    return out, cnt

def causal_past_median(ts_ns, values, window_ns, min_count):
    """Mediane des valeurs PASSEES dans [t-window, t) (exclut la courante)."""
    q50, cnt = causal_quantile_series(ts_ns, values, window_ns, 0.5, min_count)
    return q50, cnt

def classify_trajectory(sens, origin, A_bp, H, L, C, start, end):
    """Classes exclusives du gel seq189 sur (T0, T0+60min] = barres start+1..end.
    Retourne (classe, t50, t100, t_ext, exc_opp_bp, censure)."""
    if end <= start: return 'CENSUREE', None, None, None, 0.0, True
    seg_h, seg_l = H[start + 1:end + 1], L[start + 1:end + 1]
    # position signee (bp, sens de l'impulsion) des extremes
    if sens == 1:
        fav = (seg_h - origin) / origin * 10000; adv = (seg_l - origin) / origin * 10000
    else:
        fav = (origin - seg_l) / origin * 10000; adv = (origin - seg_h) / origin * 10000
    t50 = t100 = t_ext = None
    for j in range(len(seg_h)):
        if t50 is None and adv[j] <= A_bp * 0.5: t50 = j + 1
        if t100 is None and adv[j] <= 0.0: t100 = j + 1
        if t_ext is None and fav[j] >= 2 * A_bp: t_ext = j + 1
    exc_opp = float(max(0.0, -adv.min())) if len(adv) else 0.0
    complete = (end - start) >= 1  # la censure est decidee par l'appelant (fenetre tronquee)
    if t100 is not None and (t_ext is None or t100 < t_ext):
        cls = 'RETOURNEMENT' if exc_opp >= 0.5 * A_bp else 'RETRACEMENT_COMPLET'
    elif t_ext is not None and (t100 is None or t_ext < t100):
        cls = 'CONTINUATION'  # le decoupage <=30/>30 min est applique par l'appelant (unites en barres)
    elif t50 is not None:
        cls = 'RETRACEMENT_PARTIEL'
    else:
        cls = 'STAGNATION'
    return cls, t50, t100, t_ext, exc_opp, False

# ---------- agregation ----------
def agreger(bars_m1, minutes):
    b = bars_m1.copy()
    b['bucket'] = b.ts.dt.floor(f'{minutes}min')
    g = b.groupby('bucket').agg(o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last'), sp=('sp', 'median'), n=('c', 'size')).reset_index().rename(columns={'bucket': 'ts'})
    return g[g.n >= minutes].drop(columns='n').reset_index(drop=True)  # barres completes uniquement

SNAPS = [0, 1, 3, 6, 12]
def famille_imp(bars, fam, minutes):
    bars = bars.reset_index(drop=True)
    bars['date'] = bars.ts.dt.date
    C = bars.c.values; H = bars.h.values; L = bars.l.values
    rets = np.concatenate([[0.0], np.diff(np.log(C))]) * 10000
    bars['r'] = rets
    ts_ns = bars.ts.values.astype('datetime64[ns]').astype(np.int64)
    thr, cnt = causal_quantile_series(ts_ns, np.abs(rets), 60 * 24 * 3600 * 10**9, 0.90, 2000)
    bars['seuil_q90_bp'] = thr; bars['hist_n'] = cnt
    trig_idx = np.where((np.abs(rets) >= thr) & ~np.isnan(thr))[0]
    # amplitudes causales passees (mediane des declenchements des 60 jours passes, min 30)
    trig_times = ts_ns[trig_idx] if len(trig_idx) else np.array([], dtype=np.int64)
    trig_amps = np.abs(rets[trig_idx]) if len(trig_idx) else np.array([])
    past_med, past_n = causal_past_median(trig_times, trig_amps, 60 * 24 * 3600 * 10**9, 30) if len(trig_idx) else (np.array([]), np.array([]))
    pastmed_of = {int(t): (m, n) for t, m, n in zip(trig_idx, past_med, past_n)}
    day_bounds = {}
    for d, idx in bars.groupby('date').indices.items(): day_bounds[d] = (int(idx.min()), int(idx.max()))
    bars_per_60 = int(60 / minutes)
    episodes, snaps = [], []
    prev_end60 = -1
    for ti, i in enumerate(trig_idx):
        if i == 0: continue
        d = bars.date.iloc[i]; d0, d1 = day_bounds[d]
        sens = 1 if rets[i] > 0 else -1
        origin = float(C[i - 1]); A = float(abs(rets[i]))
        chevauche = 1 if i <= prev_end60 else 0
        prev_end60 = max(prev_end60, i + bars_per_60)
        end60 = min(i + bars_per_60, d1)
        fenetre_complete = (i + bars_per_60) <= d1
        cls, t50, t100, t_ext, exc_opp, _ = classify_trajectory(sens, origin, A, H, L, C, i, end60)
        if cls == 'CONTINUATION' and t_ext is not None:
            cls = 'CONTINUATION' if (t_ext * minutes) <= 30 else 'EXTENSION_TARDIVE'
        if not fenetre_complete and cls == 'STAGNATION' and t50 is None and t100 is None and t_ext is None:
            cls = 'CENSUREE'
        pm, pn = pastmed_of.get(int(i), (np.nan, 0))
        groupe_amp = 'NON_CLASSE' if (pn < 30 or np.isnan(pm)) else ('BAS' if A < pm else 'HAUT')
        base = {'famille': fam, 'date': str(d), 'ts_t0': str(bars.ts.iloc[i]), 'grappe': str(d),
                'direction': 'HAUSSE' if sens == 1 else 'BAISSE', 'session': sess(int(bars.ts.iloc[i].hour)),
                'regime': REG.get(d, 'NON_CLASSE'), 'ere': era(d), 'amplitude_initiale_bp': A,
                'seuil_q90_bp': float(thr[i]), 'groupe_amplitude_causal': groupe_amp,
                'chevauchement': chevauche, 'trajectoire_60min': cls,
                't50_barres': t50, 't100_barres': t100, 't_ext_barres': t_ext,
                'excursion_opposee_bp': exc_opp, 'fenetre_60_complete': bool(fenetre_complete)}
        episodes.append(base)
        # instantanes
        seg_rets = rets
        for s in SNAPS:
            k = i + s
            if k > d1: 
                snaps.append({**base, 'snapshot_barres': s, 'censure_snapshot': 1}); continue
            j0 = i
            if sens == 1:
                cumpeak = np.maximum.accumulate(H[j0:k + 1]); retr_j = cumpeak - L[j0:k + 1]
                pos = (C[k] - origin) / origin * 10000; range_cum = H[j0:k + 1].max() - L[j0:k + 1].min()
            else:
                cumpeak = np.minimum.accumulate(L[j0:k + 1]); retr_j = H[j0:k + 1] - cumpeak
                pos = (origin - C[k]) / origin * 10000; range_cum = H[j0:k + 1].max() - L[j0:k + 1].min()
            retr_max = float(retr_j.max() / origin * 10000) if k >= j0 else 0.0
            row = {**base, 'snapshot_barres': s, 'censure_snapshot': 0,
                   'amplitude_cumulee_bp': float(pos), 'position_bp': float(pos),
                   'retracement_max_jusqua_bp': retr_max,
                   'retracement_max_jusqua_pctA': float(retr_max / A * 100) if A > 0 else np.nan,
                   'vol_realisee_bp': float(np.std(seg_rets[j0:k + 1])) if k > j0 else 0.0,
                   'spread_median_bp': float(bars.sp.iloc[k]), 'amplitude_parcourue_bp': float(range_cum / origin * 10000)}
            # issues strictement apres k, sur (k, k+60min], bornees fin de journee et a T0+... fenetre propre a l'instantane
            e2 = min(k + bars_per_60, d1)
            if e2 > k:
                if sens == 1:
                    fav2 = (H[k + 1:e2 + 1] - origin) / origin * 10000; adv2 = (L[k + 1:e2 + 1] - origin) / origin * 10000
                else:
                    fav2 = (origin - L[k + 1:e2 + 1]) / origin * 10000; adv2 = (origin - H[k + 1:e2 + 1]) / origin * 10000
                pos_avant = float(pos)
                row['retracement_ulterior_bp'] = float(max(0.0, pos_avant - adv2.min()))
                row['retracement_ulterior_pctA'] = float(max(0.0, pos_avant - adv2.min()) / A * 100) if A > 0 else np.nan
                row['extension_supplementaire_bp'] = float(max(0.0, fav2.max() - max(pos_avant, A)))
                row['retr_complet_apres_snapshot'] = float(adv2.min() <= 0)
            else:
                row.update({'retracement_ulterior_bp': np.nan, 'retracement_ulterior_pctA': np.nan, 'extension_supplementaire_bp': np.nan, 'retr_complet_apres_snapshot': np.nan})
            for hm in (15, 30, 60):
                pas = int(hm / minutes); t = k + pas
                if t <= d1:
                    row[f'position_plus{hm}_bp'] = float(((C[t] - origin) if sens == 1 else (origin - C[t])) / origin * 10000)
                else: row[f'position_plus{hm}_bp'] = np.nan
            snaps.append(row)
    return pd.DataFrame(episodes), pd.DataFrame(snaps), int((bars.hist_n < 2000).sum())

def famille_cons(bars_m1):
    b = bars_m1.reset_index(drop=True)
    b['date'] = b.ts.dt.date
    b['range_bp'] = (b.h - b.l) / b.c * 10000
    dates = sorted(b.date.unique())
    day_idx = {d: (int(v.min()), int(v.max())) for d, v in b.groupby('date').indices.items()}
    # seuil causal par journee : 0,5 x mediane poolee des ranges des 5 journees precedentes
    seuil_jour, med_jour = {}, {}
    ranges_par_jour = {d: b.range_bp.values[day_idx[d][0]:day_idx[d][1] + 1] for d in dates}
    for di, d in enumerate(dates):
        if di == 0: continue
        prev = dates[max(0, di - 5):di]
        pool = np.concatenate([ranges_par_jour[p] for p in prev]) if prev else np.array([])
        if len(pool) >= 1000:
            med_jour[d] = float(np.median(pool)); seuil_jour[d] = 0.5 * med_jour[d]
    episodes, snaps = [], []
    H = b.h.values; L = b.l.values; C = b.c.values; R = b.range_bp.values
    for d in dates:
        if d not in seuil_jour: continue
        d0, d1 = day_idx[d]; thr = seuil_jour[d]
        calme = R[d0:d1 + 1] <= thr
        run = 0; run_start = None; active_until_noncalm = False
        i = d0
        while i <= d1:
            if calme[i - d0]:
                if run == 0: run_start = i
                run += 1
                if run == 6 and not active_until_noncalm:
                    f = i  # formation a la cloture de la 6e barre calme
                    active_until_noncalm = True
                    rf_h, rf_l = float(H[run_start:f + 1].max()), float(L[run_start:f + 1].min())
                    range_form = (rf_h - rf_l) / C[f] * 10000
                    # sortie : premiere barre apres f
                    sortie_type, sidx = 'CENSUREE', None
                    cum_h, cum_l = rf_h, rf_l
                    e_lim = min(f + 120, d1)
                    for j in range(f + 1, e_lim + 1):
                        rj = (H[j] - L[j]) / C[j] * 10000
                        if rj > 2 * range_form: sortie_type, sidx = 'BARRE_RANGE', j; break
                        if C[j] > cum_h or C[j] < cum_l: sortie_type, sidx = 'CLOTURE_HORS_RANGE', j; break
                        cum_h, cum_l = max(cum_h, H[j]), min(cum_l, L[j])
                    duree = int((sidx - run_start + 1)) if sidx is not None else int(e_lim - run_start + 1)
                    mid = (rf_h + rf_l) / 2
                    ep = {'famille': 'CONS', 'date': str(d), 'ts_t0': str(b.ts.iloc[f]), 'grappe': str(d),
                          'session': sess(int(b.ts.iloc[f].hour)), 'regime': REG.get(d, 'NON_CLASSE'), 'ere': era(d),
                          'range_formation_bp': float(range_form), 'seuil_calme_bp': float(thr),
                          'mediane_ranges_5j_bp': float(med_jour[d]), 'type_sortie': sortie_type,
                          'duree_consolidation_min': duree, 'censuree': float(sortie_type == 'CENSUREE')}
                    # issues post-sortie (ou post-censure a titre descriptif, fenetre apres l'instant de reference)
                    ref = sidx if sidx is not None else e_lim
                    e2 = min(ref + 60, d1)
                    if e2 > ref:
                        ep['range_post_sortie_60_bp'] = float((H[ref + 1:e2 + 1].max() - L[ref + 1:e2 + 1].min()) / C[ref] * 10000)
                        sens_sortie = 1 if C[ref] >= mid else -1
                        if sens_sortie == 1:
                            ep['excursion_sens_sortie_bp'] = float((H[ref + 1:e2 + 1].max() - C[ref]) / C[ref] * 10000)
                            ep['excursion_opposee_bp'] = float((C[ref] - L[ref + 1:e2 + 1].min()) / C[ref] * 10000)
                        else:
                            ep['excursion_sens_sortie_bp'] = float((C[ref] - L[ref + 1:e2 + 1].min()) / C[ref] * 10000)
                            ep['excursion_opposee_bp'] = float((H[ref + 1:e2 + 1].max() - C[ref]) / C[ref] * 10000)
                    else:
                        ep.update({'range_post_sortie_60_bp': np.nan, 'excursion_sens_sortie_bp': np.nan, 'excursion_opposee_bp': np.nan})
                    for hm in (15, 30, 60):
                        t = ref + hm
                        ep[f'position_plus{hm}_bp'] = float((C[t] - mid) / mid * 10000) if t <= d1 else np.nan
                    episodes.append(ep)
                    for s in (0, 3, 6, 12):
                        k = min(f + s, d1)
                        rcum = (H[run_start:k + 1].max() - L[run_start:k + 1].min()) / C[k] * 10000
                        snaps.append({**ep, 'snapshot_min': s, 'duree_ecoulee_min': int(k - run_start + 1),
                                      'range_cumule_bp': float(rcum),
                                      'position_dans_range': float((C[k] - L[run_start:k + 1].min()) / (H[run_start:k + 1].max() - L[run_start:k + 1].min())) if H[run_start:k + 1].max() > L[run_start:k + 1].min() else 0.5,
                                      'ratio_compression': float(rcum / med_jour[d]) if med_jour[d] > 0 else np.nan,
                                      'vol_realisee_bp': float(np.std(np.diff(np.log(C[run_start:k + 1])) * 10000)) if k > run_start else 0.0,
                                      'spread_median_bp': float(b.sp.iloc[k]),
                                      'sortie_avant_snapshot': float(sidx is not None and sidx <= k)})
            else:
                run = 0; run_start = None; active_until_noncalm = False
            i += 1
    return pd.DataFrame(episodes), pd.DataFrame(snaps), len([d for d in dates if d not in seuil_jour])

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date
    journees = int(bars.date.nunique())
    print('C3 barres M1', len(bars), 'journees', journees, flush=True)
    m5 = agreger(bars, 5); m15 = agreger(bars, 15)
    e5, s5, amor5 = famille_imp(m5, 'IMP-M5', 5)
    e15, s15, amor15 = famille_imp(m15, 'IMP-M15', 15)
    ec, sc, amorc = famille_cons(bars)
    # groupe formation causal CONS (C3-09) : mediane des ranges de formation des 60 jours passes (min 30)
    if len(ec):
        ec = ec.sort_values('ts_t0').reset_index(drop=True)
        med, nn = causal_past_median(pd.to_datetime(ec.ts_t0).values.astype('datetime64[ns]').astype(np.int64), ec.range_formation_bp.values, 60 * 24 * 3600 * 10**9, 30)
        ec['groupe_range_formation'] = ['NON_CLASSE' if (n < 30 or np.isnan(m)) else ('BAS' if v < m else 'HAUT') for v, m, n in zip(ec.range_formation_bp.values, med, nn)]
        if len(sc): sc = sc.merge(ec[['ts_t0', 'groupe_range_formation']], on='ts_t0', how='left', suffixes=('', '_y'))
    for df_, nom in [(e5, 'CAMPAIGN_03_EPISODES_IMP_M5.csv.gz'), (e15, 'CAMPAIGN_03_EPISODES_IMP_M15.csv.gz'), (ec, 'CAMPAIGN_03_EPISODES_CONS.csv.gz')]:
        df_.round(4).to_csv(ROOT / nom, index=False, compression='gzip')
    pd.concat([s5.assign(unite='barres_M5'), s15.assign(unite='barres_M15')], ignore_index=True).round(4).to_csv(ROOT / 'CAMPAIGN_03_SNAPSHOTS_IMP.csv.gz', index=False, compression='gzip')
    sc.round(4).to_csv(ROOT / 'CAMPAIGN_03_SNAPSHOTS_CONS.csv.gz', index=False, compression='gzip')
    tailles = {str(p): p.stat().st_size for p in sorted(ROOT.glob('CAMPAIGN_03_*.csv.gz'))}
    print('C3 tailles fichiers', tailles, flush=True)
    cov = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
           'barres_m1': int(len(bars)), 'barres_m5': int(len(m5)), 'barres_m15': int(len(m15)), 'journees': journees,
           'episodes_imp_m5': int(len(e5)), 'episodes_imp_m15': int(len(e15)), 'episodes_cons': int(len(ec)),
           'amorcage_imp_m5_barres_sans_historique': int(amor5), 'amorcage_imp_m15_barres_sans_historique': int(amor15),
           'cons_journees_sans_seuil': int(amorc),
           'chevauchements_imp_m5': int(e5.chevauchement.sum()) if len(e5) else 0,
           'chevauchements_imp_m15': int(e15.chevauchement.sum()) if len(e15) else 0}
    (ROOT / 'C3_COVERAGE.json').write_text(json.dumps(cov, indent=1))
    print('C3 TERMINE', cov, flush=True)

if __name__ == '__main__': main()
