"""CAMPAGNE 4 - regimes et volatilite, cartographie causale descriptive.
Dictionnaire v2 gele seq196 (sha256 0a615c54...), dix comparaisons seq196/200.
Etats a seuils strictement passes; aucune etiquette poolee presentee comme
temps reel; transitions confirmees datees a D=C+2, jamais antidatees."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback, bisect
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign04'); ROOT.mkdir(parents=True, exist_ok=True)
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)

def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

def era(d): return '2010_2013' if d.year <= 2013 else ('2014_2016' if d.year <= 2016 else '2017_2020')
def sess_of_hour(h): return 'ASIE' if h < 8 else ('LONDRES' if h < 13 else ('NEWYORK' if h < 21 else 'NUIT'))
SESSIONS = ['ASIE', 'LONDRES', 'NEWYORK', 'NUIT']

CHARGER_STATS = {'chargees': 0, 'attendues': 0}
def charger():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    CHARGER_STATS['attendues'] = len(parts)
    print('C4 ALL', len(parts), 'partitions attendues', flush=True)
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
            print('C4 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives causales (testees par campaign04_temporal_tests.py) ----------
def causal_quantile_series(ts_ns, values, window_ns, q, min_count):
    """Quantile sur [t-window, t), barre courante exclue."""
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

def tercile_causal(values, window, min_hist):
    """Etiquettes BAS/MOYEN/HAUT vs quantiles des `window` valeurs precedentes
    (jours precedents), valeur courante exclue des seuils."""
    v = pd.Series(values, dtype=float)
    q1 = v.shift(1).rolling(window, min_periods=min_hist).quantile(1/3)
    q2 = v.shift(1).rolling(window, min_periods=min_hist).quantile(2/3)
    out = np.full(len(v), 'NON_CLASSE', dtype=object)
    ok = q1.notna().values
    vv = v.values
    out[ok & (vv <= q1.values)] = 'BAS'
    out[ok & (vv > q2.values)] = 'HAUT'
    out[ok & (vv > q1.values) & (vv <= q2.values)] = 'MOYEN'
    return out, q1.values, q2.values

def episodes_et_transitions(etats):
    """Episodes (runs contigus d'etats classes) et transitions.
    Confirmation D = C+2 (3 journees consecutives), jamais antidatee.
    Une interruption NON_CLASSE clot l'episode sans creer de transition."""
    cls = list(etats)
    eps = []
    i = 0
    while i < len(cls):
        if cls[i] == 'NON_CLASSE': i += 1; continue
        j = i
        while j + 1 < len(cls) and cls[j + 1] == cls[i]: j += 1
        eps.append({'debut': i, 'fin': j, 'etat': cls[i]}); i = j + 1
    trans = []
    for a, b in zip(eps, eps[1:]):
        if b['debut'] != a['fin'] + 1: continue  # NON_CLASSE intercale: pas de transition definie
        C = b['debut']; persistance = b['fin'] - b['debut'] + 1
        confirmee = persistance >= 3
        trav = int(C - a['fin'])
        trans.append({'candidate_idx': C, 'depuis': a['etat'], 'vers': b['etat'],
                      'confirmee': bool(confirmee), 'confirmation_idx': (C + 2) if confirmee else None,
                      'persistance': int(persistance), 'traversee': trav,
                      'vitesse': 'RAPIDE' if trav <= 2 else ('INTERMEDIAIRE' if trav <= 4 else 'PROGRESSIVE')})
    return eps, trans

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date
    bars = bars.sort_values('ts').reset_index(drop=True)
    # rendements M1 internes a chaque journee (premier de la journee exclu)
    bars['r'] = np.log(bars.c).groupby(bars['date']).diff()
    jours = []
    sess_rows = []
    absr_par_jour = {}
    for d, g in bars.groupby('date'):
        r = g.r.dropna().values
        if len(g) < 300:
            jours.append({'date': d, 'utilisable': 0, 'n_barres': len(g)}); absr_par_jour[d] = np.abs(r); continue
        rv = float(np.sqrt(np.sum(r ** 2)) * 10000)
        m2 = np.mean(r ** 2); m3 = np.mean(r ** 3)
        skew = float(m3 / m2 ** 1.5) if m2 > 0 else np.nan
        jours.append({'date': d, 'utilisable': 1, 'n_barres': len(g), 'rv_bp': rv, 'skew': skew,
                      'cloture_fin': float(g.c.iloc[-1]), 'absr': None})
        absr_par_jour[d] = np.abs(r)
        for sname in SESSIONS:
            gs = g[g.ts.dt.hour.map(sess_of_hour) == sname]
            rs = np.log(gs.c).diff().dropna().values
            if len(gs) >= 60 and len(rs) > 0:
                sess_rows.append({'date': d, 'session': sname, 'n_barres': len(gs), 'rv_bp': float(np.sqrt(np.sum(rs ** 2)) * 10000)})
            else:
                sess_rows.append({'date': d, 'session': sname, 'n_barres': len(gs), 'rv_bp': np.nan})
    J = pd.DataFrame(jours)
    dates_all = list(J.date)
    # seuil d'extremes causal par journee: q99 des |r| M1 poolés des 60 journees precedentes (min 20000)
    pos = {d: i for i, d in enumerate(dates_all)}
    seuils_ext = np.full(len(J), np.nan); freq_ext = np.full(len(J), np.nan)
    for i, d in enumerate(dates_all):
        prev = dates_all[max(0, i - 60):i]
        pool = np.concatenate([absr_par_jour[p] for p in prev]) if prev else np.array([])
        if len(pool) >= 20000:
            seuils_ext[i] = np.quantile(pool, 0.99)
            cur = absr_par_jour[d]
            freq_ext[i] = float(np.mean(cur > seuils_ext[i])) if len(cur) else np.nan
    J['seuil_extremes_bp'] = seuils_ext; J['freq_extremes'] = freq_ext
    Ju = J[J.utilisable == 1].reset_index(drop=True).copy()
    Ju['ere'] = [era(d) for d in Ju.date]
    Ju['ret_j_bp'] = np.log(Ju.cloture_fin).diff() * 10000
    Ju['etat_courant'], Ju['q1_rv'], Ju['q2_rv'] = tercile_causal(Ju.rv_bp.values, 60, 40)
    Ju['mediane_rv_60'] = pd.Series(Ju.rv_bp.values).shift(1).rolling(60, min_periods=40).median().values
    Ju['log_ratio_rv_mediane'] = np.log(Ju.rv_bp / Ju.mediane_rv_60)
    Ju['etat_asymetrie'], _, _ = tercile_causal(Ju.skew.values, 60, 40)
    Ju['etat_queue'], _, _ = tercile_causal(Ju.freq_extremes.values, 60, 40)
    lv = np.log(Ju.rv_bp.values)
    vov = pd.Series(lv).rolling(20).std().values
    Ju['vol_de_vol'] = vov
    Ju['etat_vov'], _, _ = tercile_causal(vov, 60, 40)
    # F3: prediction causale, tercile causal roulant 250 (min 60), reference poolee retrospective
    f3 = pd.read_csv('reports/meta_alpha/phase2/f3_har/F3_DAILY_PRED.csv')
    f3['date'] = pd.to_datetime(f3.day.astype(str)).dt.tz_localize(None).dt.date
    f3 = f3.sort_values('date').reset_index(drop=True)
    lab_causal, _, _ = tercile_causal(f3.pred_har.values, 250, 60)
    f3['f3_tercile_causal'] = lab_causal
    pp = f3.pred_har.dropna()
    q1p, q2p = pp.quantile([1/3, 2/3]).values
    f3['f3_tercile_pooled_ref'] = ['NON_CLASSE' if pd.isna(x) else ('BAS' if x <= q1p else ('HAUT' if x > q2p else 'MOYEN')) for x in f3.pred_har]
    Ju = Ju.merge(f3[['date', 'pred_har', 'f3_tercile_causal', 'f3_tercile_pooled_ref']], on='date', how='left')
    Ju['f3_tercile_causal'] = Ju['f3_tercile_causal'].fillna('NON_CLASSE')
    Ju['f3_tercile_pooled_ref'] = Ju['f3_tercile_pooled_ref'].fillna('NON_CLASSE')
    # dispersion intrajournaliere depuis les sessions
    S = pd.DataFrame(sess_rows)
    piv = S.pivot_table(index='date', columns='session', values='rv_bp', aggfunc='first')
    disp, nok = [], []
    for d, row in piv.iterrows():
        v = row.dropna().values
        nok.append(len(v))
        disp.append(float(v.max() / v.min()) if len(v) >= 3 and v.min() > 0 else np.nan)
    D = pd.DataFrame({'date': list(piv.index), 'dispersion': disp, 'n_sessions_ok': nok})
    Ju = Ju.merge(D, on='date', how='left')
    Ju['etat_dispersion'], _, _ = tercile_causal(Ju.dispersion.values, 60, 40)
    # etats de session causaux par session
    S = S.sort_values(['session', 'date'])
    etats_sess = []
    for sname, gs in S.groupby('session'):
        lab, _, _ = tercile_causal(gs.rv_bp.values, 60, 40)
        etats_sess.append(pd.Series(lab, index=gs.index))
    S['etat_session'] = pd.concat(etats_sess).sort_index()
    # impulsions IMP-M5 par journee (definitions campagne 3 gelees)
    mb = bars.copy(); mb['bucket'] = mb.ts.dt.floor('5min')
    m5 = mb.groupby('bucket').agg(o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last'), n=('c', 'size')).reset_index().rename(columns={'bucket': 'ts'})
    m5 = m5[m5.n >= 5].drop(columns='n').reset_index(drop=True)
    C = m5.c.values
    rets5 = np.concatenate([[0.0], np.diff(np.log(C))]) * 10000
    ts_ns = m5.ts.values.astype('datetime64[ns]').astype(np.int64)
    thr5, _ = causal_quantile_series(ts_ns, np.abs(rets5), 60 * 24 * 3600 * 10**9, 0.90, 2000)
    trig = (~np.isnan(thr5)) & (np.abs(rets5) >= thr5)
    m5d = pd.Series(m5.ts.dt.date.values[trig]).value_counts()
    Ju['imp_m5_count'] = Ju.date.map(m5d).fillna(0).astype(int)
    # depassements par journee: bruts campagnes 2.2/2.3 (definitions historiques inchangees, lecture seule)
    try:
        ov = pd.read_csv('reports/meta_alpha/campaign02_2/CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv', usecols=['date', 'snapshot_min'])
        ov = ov[ov.snapshot_min.astype(str) == '0']
        cnt = ov.groupby('date').size()
        Ju['depassements_count'] = [int(cnt.get(str(d), 0)) for d in Ju.date]
    except Exception as e:
        print('depassements indisponibles', str(e)[:80], flush=True); Ju['depassements_count'] = np.nan
    Ju = Ju.drop(columns=[c for c in ['absr'] if c in Ju.columns])
    Ju.round(5).to_csv(ROOT / 'CAMPAIGN_04_DAILY.csv.gz', index=False, compression='gzip')
    S.round(5).to_csv(ROOT / 'CAMPAIGN_04_SESSIONS.csv.gz', index=False, compression='gzip')
    cov = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
           'barres_m1': int(len(bars)), 'journees_presentes': int(len(J)), 'journees_utilisables': int(len(Ju)),
           'journees_non_utilisables': int((J.utilisable == 0).sum()),
           'etat_courant_classes': int((Ju.etat_courant != 'NON_CLASSE').sum()),
           'f3_causal_classes': int((Ju.f3_tercile_causal != 'NON_CLASSE').sum()),
           'sessions_lignes': int(len(S))}
    (ROOT / 'C4_COVERAGE.json').write_text(json.dumps(cov, indent=1))
    print('C4 TERMINE', cov, flush=True)

if __name__ == '__main__': main()
