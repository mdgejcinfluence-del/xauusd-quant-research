"""CAMPAGNE 7 - F-I nombres ronds, descriptif. Protocole gele V1 (seq250,
execution seq251-252). Grilles exogenes G50/P50 (demi-pas), anneaux
R100/R10, placebos P100/P10 descriptifs. Evenements a la cloture des
barres; aucune reconstruction de donnee manquante."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign07'); ROOT.mkdir(parents=True, exist_ok=True)
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
    print('C7 ALL', len(parts), 'partitions attendues', flush=True)
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
            print('C7 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives (testees par campaign07_temporal_tests.py) ----------
def distance_bp(bas, haut, niveau):
    if bas <= niveau <= haut: return 0.0
    return min(abs(bas - niveau), abs(haut - niveau)) / niveau * 10000.0

def est_franchissement(cloture, niveau, par_en_dessous):
    return cloture > niveau if par_en_dessous else cloture < niveau

def session_de(minute):
    h = minute // 60
    return 'ASIE' if h < 8 else ('LONDRES' if h < 13 else ('NEWYORK' if h < 21 else 'NUIT'))

GRILLES = {
    'G50': (50.0, 0.0), 'P50': (50.0, 25.0), 'R100': (100.0, 0.0),
    'R10': (10.0, 0.0), 'P100': (100.0, 25.0), 'P10': (10.0, 5.0)}

def niveaux(grille, pmin, pmax):
    pas, off = GRILLES[grille]
    k0 = int(np.floor((pmin - off) / pas)) - 1; k1 = int(np.ceil((pmax - off) / pas)) + 1
    lv = [off + pas * k for k in range(k0, k1 + 1) if pmin - 60 <= off + pas * k <= pmax + 60]
    if grille == 'R10': lv = [x for x in lv if x % 50 != 0]
    if grille == 'R100': lv = [x for x in lv if x % 100 == 0]
    return lv

def episodes_niveau(ts, day, o, h, l, c, niveau, grille):
    """ts en minutes (int), day = identifiant de jour (int). Retourne les episodes."""
    n = len(ts)
    d = np.where((l <= niveau) & (h >= niveau), 0.0, np.minimum(np.abs(l - niveau), np.abs(h - niveau)))
    dbp = d / niveau * 10000.0
    inband = dbp <= 25.0
    idx = np.where(inband)[0]
    episodes = []
    if len(idx) == 0: return episodes
    starts = []
    last = -10**9
    for i in idx:
        if ts[i] - last > 60: starts.append(int(i))
        last = int(ts[i])
    pas = GRILLES[grille][0]
    for s in starts:
        dend = s
        while dend + 1 < n and day[dend + 1] == day[s]: dend += 1
        prev_close = c[s - 1] if s > 0 else c[s]
        dessous = bool(prev_close < niveau) if prev_close != niveau else bool(c[s] <= niveau)
        touche = franch = rejet = False; t_touch = t_cross = t_term = None; terminal = None
        j = s
        while j <= dend:
            beyond = est_franchissement(c[j], niveau, dessous)
            if not touche and not franch and d[j] > 0 and ((dessous and o[j] > niveau) or ((not dessous) and o[j] < niveau)):
                terminal = 'SAUT'; t_term = j; break
            if beyond and not franch:
                franch = True; t_cross = j; break
            if d[j] == 0 and not touche:
                touche = True; t_touch = j
            if touche and j > t_touch:
                ecart = (niveau - c[j]) if dessous else (c[j] - niveau)
                if ecart / niveau * 10000.0 >= 25.0:
                    rejet = True; terminal = 'REJET'; t_term = j; break
            j += 1
        retour = maintien = False; dist_post = np.nan; suivi_complet = False
        if franch:
            w = [k for k in range(t_cross + 1, min(dend, t_cross + 400) + 1) if ts[k] <= ts[t_cross] + 60]
            mins = set(int(ts[k] - ts[t_cross]) for k in w)
            suivi_complet = all(m in mins for m in range(1, 61))
            if w:
                exc = [(h[k] - niveau) if dessous else (niveau - l[k]) for k in w]
                dist_post = float(max(exc) / niveau * 10000.0)
                for k in w:
                    if (dessous and c[k] < niveau) or ((not dessous) and c[k] > niveau): retour = True; break
                maintien = bool(suivi_complet and not retour)
            terminal = 'FRANCHISSEMENT'
        elif touche and not rejet:
            # fenetre de 60 min apres touche complete sans franchissement ni rejet?
            if ts[dend] - ts[t_touch] >= 60:
                terminal = 'SANS_EFFET'
            else:
                terminal = 'CENSURE_JOUR'
        elif not touche and not franch and terminal is None:
            terminal = 'CENSURE_JOUR'
        # simultane: la barre de contact couvre >=2 niveaux de la grille
        contact = t_touch if t_touch is not None else t_cross
        simultane = False
        if contact is not None:
            off = GRILLES[grille][1]
            simultane = (int(np.floor((h[contact] - off) / pas)) - int(np.floor((l[contact] - off) / pas))) >= 1 and grille in ('G50', 'R10', 'R100')
            if grille == 'R10':  # niveaux reels R10 seulement (hors multiples de 50)
                lv_in = [x for x in np.arange(np.ceil(l[contact] / 10) * 10, h[contact] + 1e-9, 10) if x % 50 != 0]
                simultane = len(lv_in) >= 2
        d0 = dt.datetime.utcfromtimestamp(0)  # placeholder
        episodes.append({'grille': grille, 'niveau': float(niveau), 'idx_approche': int(s),
                         'minute_jour': int(ts[s] % 1440), 'cote': 'DESSOUS' if dessous else 'DESSUS',
                         'distance_initiale_bp': float(dbp[s]), 'touche': int(touche), 'franchissement': int(franch),
                         'saut': int(terminal == 'SAUT'), 'rejet': int(rejet), 'retour': int(retour),
                         'maintien': int(maintien), 'distance_post_bp': dist_post,
                         'suivi_complet': int(suivi_complet), 'terminal': terminal,
                         'simultane': int(simultane), 'delai_touche_min': (int(ts[t_touch] - ts[s]) if t_touch is not None else None),
                         'delai_franch_min': (int(ts[t_cross] - ts[s]) if t_cross is not None else None)})
    return episodes

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date
    ts = (bars.ts - pd.Timestamp('2010-01-01')).dt.total_seconds().values // 60
    ts = ts.astype(np.int64)
    day = bars.date.values
    dates_u = {d: i for i, d in enumerate(sorted(set(bars.date)))}
    day_id = np.array([dates_u[d] for d in day])
    date_str = bars.date.astype(str).values
    o, h, l, c = bars.o.values, bars.h.values, bars.l.values, bars.c.values
    pmin, pmax = float(l.min()), float(h.max())
    all_eps = []
    for grille in GRILLES:
        for nv in niveaux(grille, pmin, pmax):
            eps = episodes_niveau(ts, day_id, o, h, l, c, nv, grille)
            for e in eps:
                e['date'] = date_str[e['idx_approche']]
                e['ere'] = era(dt.date.fromisoformat(e['date']))
                e['session'] = session_de(e['minute_jour'])
                del e['idx_approche']
            all_eps += eps
        print('C7 grille', grille, 'episodes cumules', len(all_eps), flush=True)
    EP = pd.DataFrame(all_eps)
    EP.round(4).to_csv(ROOT / 'CAMPAIGN_07_EPISODES.csv.gz', index=False, compression='gzip')
    resume = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
              'barres_m1': int(len(bars)), 'journees_presentes': int(bars.date.nunique()),
              'episodes_par_grille': {k: int(v) for k, v in EP.grille.value_counts().items()},
              'terminaux': {k: int(v) for k, v in EP.terminal.value_counts().items()}}
    (ROOT / 'C7_COVERAGE.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume), flush=True)

if __name__ == '__main__': main()
