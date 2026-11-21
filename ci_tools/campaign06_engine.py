"""CAMPAGNE 6 - F-G forme des trajectoires journalieres, descriptif.
Protocole gele V1.1 + V1.2 + V1.2.1 + V1.2.2 (seq239, execution seq241-242).
Segments continus; L intra-segment uniquement; Delta_seg sur la meme
population que L (ER<=1 par inegalite triangulaire); Delta_jour jamais
en ratio avec L; aucune reconstruction de donnee manquante."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign06'); ROOT.mkdir(parents=True, exist_ok=True)
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

CHARGER_STATS = {'chargees': 0, 'attendues': 0}
def charger():
    import duckdb
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    CHARGER_STATS['attendues'] = len(parts)
    print('C6 ALL', len(parts), 'partitions attendues', flush=True)
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
                        max(mid) AS h, min(mid) AS l, arg_max(mid, timestamp_utc) AS c
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b); CHARGER_STATS['chargees'] += 1
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C6 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives (testees par campaign06_temporal_tests.py) ----------
def segments(minutes):
    """Indices de debut de segment (minutes consecutives, ecart == 1)."""
    minutes = np.asarray(minutes)
    if len(minutes) == 0: return np.array([], dtype=int)
    return np.concatenate([[0], np.where(np.diff(minutes) > 1)[0] + 1]).astype(int)

def classe_forme(delta_seg_bp, er):
    if abs(delta_seg_bp) < 5.0: return 'DEPLACEMENT_FAIBLE'
    if er <= 0.10: return 'OSCILLANTE'
    if er < 0.30: return 'MIXTE'
    return 'DIRECTIONNELLE'

def halte_candidates(gaps, jour_semaine):
    """gaps: liste (premiere_minute_manquante, duree_manquante). B15 option A:
    fenetre UTC fixe debut 21:00-22:00 +/-5 min, duree 45-75, lundi-vendredi."""
    cand = []
    for k, (debut, duree) in enumerate(gaps):
        if jour_semaine < 5 and 1255 <= debut <= 1325 and 45 <= duree <= 75: cand.append(k)
    return cand

def compute_day(minutes, o, h, l, c, jour_semaine=0):
    minutes = np.asarray(minutes, dtype=float); o = np.asarray(o, float); h = np.asarray(h, float)
    l = np.asarray(l, float); c = np.asarray(c, float)
    n = len(minutes); p0 = float(o[0])
    dm = np.diff(minutes); dc = np.diff(c)
    intra = dm == 1
    steps = np.where(intra, np.abs(dc), 0.0)
    L = float(steps.sum())
    seg_start = segments(minutes)
    seg_id = np.zeros(n, dtype=int); seg_id[seg_start[1:]] = 1; seg_id = np.cumsum(seg_id)
    delta_seg = 0.0
    for s in range(seg_id[-1] + 1):
        idx = np.where(seg_id == s)[0]; delta_seg += float(c[idx[-1]] - c[idx[0]])
    gap_idx = np.where(~intra)[0]
    gaps = [(int(minutes[i] + 1), int(dm[i] - 1), float(c[i + 1] - c[i])) for i in gap_idx]  # (debut manquant, duree, saut)
    D = float(sum(abs(g[2]) for g in gaps))
    delta_jour = float(c[-1] - p0)
    A = float(h.max() - l.min())
    bp = lambda x: x / p0 * 10000.0 if p0 else np.nan
    ER = abs(delta_seg) / L if L > 0 else np.nan
    S = L / A if A > 0 else np.nan
    rho = D / (L + D) if (L + D) > 0 else np.nan
    # part directionnelle
    if delta_seg != 0:
        mv = intra & (dc != 0)
        PD = float((np.sign(dc[mv]) == np.sign(delta_seg)).mean()) if mv.any() else np.nan
    else: PD = np.nan
    # point median: premier pas ou le cumule atteint L/2
    tau = np.nan
    if L > 0:
        cum = np.concatenate([[0.0], np.cumsum(steps)])
        k = int(np.argmax(cum[1:] >= L / 2))  # pas aboutissant a la barre k+1
        tau = float(minutes[k + 1])
    # efficiences par moitie (segments internes a chaque moitie)
    def er_moitie(mask):
        mm = minutes[mask]; cc = c[mask]
        if len(cc) < 2: return np.nan
        d2 = np.diff(mm); s2 = np.where(d2 == 1, np.abs(np.diff(cc)), 0.0); L2 = s2.sum()
        if L2 == 0: return np.nan
        st = segments(mm); ds = 0.0
        sid = np.zeros(len(mm), dtype=int); sid[st[1:]] = 1; sid = np.cumsum(sid)
        for s in range(sid[-1] + 1):
            idx = np.where(sid == s)[0]; ds += float(cc[idx[-1]] - cc[idx[0]])
        return abs(ds) / L2
    ER1 = er_moitie(minutes < 720); ER2 = er_moitie(minutes >= 720)
    AS = ER1 - ER2 if (ER1 == ER1 and ER2 == ER2) else np.nan
    # couverture / B15
    cand = halte_candidates([(g[0], g[1]) for g in gaps], jour_semaine)
    if len(cand) == 1:
        classe_halte = 'FRONTIERE_PROGRAMMEE'; front = cand[0]
    elif len(gaps) == 0:
        classe_halte = 'AUCUN_TROU'; front = -1
    else:
        classe_halte = 'HALTE_INDETERMINEE'; front = -1
    sess = [g for k, g in enumerate(gaps) if k != front]
    cumul_sess = int(sum(g[1] for g in sess)); trou_sess_max = int(max([g[1] for g in sess], default=0))
    attendues = n + cumul_sess
    taux = n / attendues * 100 if attendues else np.nan
    trou_max_all = int(max([g[1] for g in gaps], default=0))
    statut_general = 'COMPLETE' if (n >= 1368 and minutes[0] <= 10 and minutes[-1] >= 1430 and trou_max_all <= 30) else ('PARTIELLE' if n >= 300 else 'EXCLUE')
    # statuts de forme: priorite V1.2.2
    if L == 0 and D == 0: statut_forme = 'PLATE_OBSERVEE'
    elif L == 0 and D > 0: statut_forme = 'INDETERMINEE_DISCONTINUITES'
    elif A == 0: statut_forme = 'INCOHERENTE'
    elif L > 0 and rho == rho and rho > 0.5: statut_forme = 'DOMINEE_DISCONTINUITES_OBSERVEES'
    elif taux >= 95.0 and trou_sess_max <= 15 and cumul_sess <= 30: statut_forme = 'ELIGIBLE'
    else: statut_forme = 'CENSUREE_FORME'
    eligible = 1 if statut_forme == 'ELIGIBLE' else 0
    return {'n_barres': n, 'p0': p0, 'delta_seg_bp': bp(delta_seg), 'delta_jour_bp': bp(delta_jour),
            'L_bp': bp(L), 'A_bp': bp(A), 'D_bp': bp(D), 'abs_delta_seg_sur_A': (abs(delta_seg) / A if A > 0 else np.nan),
            'ER': ER, 'S': S, 'rho': rho, 'PD': PD, 'tau_min': tau, 'ER1': ER1, 'ER2': ER2, 'AS': AS,
            'n_segments': int(seg_id[-1] + 1), 'n_trous': len(gaps), 'duree_cumulee_trous_min': int(sum(g[1] for g in gaps)),
            'minutes_attendues': int(attendues), 'minutes_observees': n, 'taux_couverture_pct': taux,
            'trou_session_max_min': trou_sess_max, 'cumul_trous_session_min': cumul_sess,
            'classe_halte': classe_halte, 'statut_general': statut_general, 'statut_forme': statut_forme,
            'eligible': eligible, 'classe_forme': classe_forme(bp(delta_seg), ER) if eligible else None,
            'premiere_minute': int(minutes[0]), 'derniere_minute': int(minutes[-1])}

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date; bars['minute'] = bars.ts.dt.hour * 60 + bars.ts.dt.minute
    rows = []
    for d, g in bars.groupby('date'):
        g = g.sort_values('ts')
        r = compute_day(g.minute.values, g.o.values, g.h.values, g.l.values, g.c.values, int(pd.Timestamp(d).dayofweek))
        r.update({'date': str(d), 'ere': era(d), 'jour_semaine': int(pd.Timestamp(d).dayofweek),
                  'semaine_lundi': str(d - dt.timedelta(days=int(pd.Timestamp(d).dayofweek)))})
        rows.append(r)
        print('C6 jour', d, r['statut_forme'], flush=True)
    D = pd.DataFrame(rows)
    D.round(6).to_csv(ROOT / 'CAMPAIGN_06_DAYS.csv', index=False)
    cov_cols = ['date', 'ere', 'jour_semaine', 'n_barres', 'minutes_attendues', 'minutes_observees', 'taux_couverture_pct',
                'n_trous', 'duree_cumulee_trous_min', 'trou_session_max_min', 'cumul_trous_session_min',
                'classe_halte', 'statut_general', 'statut_forme', 'eligible', 'premiere_minute', 'derniere_minute']
    D[cov_cols].round(4).to_csv(ROOT / 'CAMPAIGN_06_DAY_COVERAGE.csv', index=False)
    resume = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
              'barres_m1': int(len(bars)), 'journees_presentes': int(len(D)),
              'statuts_forme': {k: int(v) for k, v in D.statut_forme.value_counts().items()},
              'classes_halte': {k: int(v) for k, v in D.classe_halte.value_counts().items()},
              'statuts_generaux': {k: int(v) for k, v in D.statut_general.value_counts().items()},
              'classes_forme_eligibles': {k: int(v) for k, v in D[D.eligible == 1].classe_forme.value_counts().items()}}
    (ROOT / 'C6_COVERAGE.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume), flush=True)

if __name__ == '__main__': main()
