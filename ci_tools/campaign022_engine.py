"""CAMPAGNE 2.2 - reconstruction temporelle causale des depassements/cassures.
Instantanes T0/+1/+3/+5: variables connues jusqu'a l'instant; issues strictement apres."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign02_2'); ROOT.mkdir(parents=True, exist_ok=True)
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
def sess(h): return 'ASIE' if h < 8 else ('LONDRES' if h < 13 else ('NEWYORK' if h < 21 else 'NUIT'))

BATCH = os.environ.get('C22_BATCH', 'xauusd-is-b01')
def charger():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    parts = [p for p in parts if batchof.get(p['name'], 'DRIVE') == BATCH]
    print('LOT', BATCH, len(parts), 'partitions', flush=True)
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
                    api = KaggleApi(); api.authenticate(); username = 'shalom5123'  # proprietaire reel des datasets (VERIFY.json), config_values renvoyait un nom court -> 403
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
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b)
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C2.2 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

SNAPS = [0, 1, 3, 5]
def main():
    bars = charger(); bars['date'] = bars.ts.dt.date; bars['heure'] = bars.ts.dt.hour
    jours = {d: g.reset_index(drop=True) for d, g in bars.groupby('date')}; dates = sorted(jours)
    if len(dates) < 200:
        (ROOT / f'ERROR_{BATCH}.txt').write_text(f'COUVERTURE INSUFFISANTE LOT {BATCH}: {len(dates)} journees (<200)')
        raise RuntimeError(f'couverture insuffisante lot {BATCH}: {len(dates)} journees')
    over, brk = [], []
    for di, d in enumerate(dates):
        g = jours[d]
        if len(g) < 300: continue
        reg, er = REG.get(d, 'NON_CLASSE'), era(d)
        asia = g[g.heure < 8]; niveaux = {}
        if len(asia) >= 60: niveaux['ASIE'] = (float(asia.h.max()), float(asia.l.min()))
        if di > 0 and len(jours[dates[di - 1]]) >= 300:
            pv = jours[dates[di - 1]]; niveaux['VEILLE'] = (float(pv.h.max()), float(pv.l.min()))
        if not niveaux: continue
        w = g[g.heure >= 8].reset_index(drop=True)
        C, H, Lc, SP = w.c.values, w.h.values, w.l.values, w.sp.values
        rets = np.concatenate([[0.0], np.diff(np.log(C))]) * 10000
        for src, (hi, lo) in niveaux.items():
            for cote, L, sens in [('HAUT', hi, 1), ('BAS', lo, -1)]:
                dep = (C > L) if sens == 1 else (C < L)
                for i in np.where(dep)[0]:
                    if i > 0 and dep[i - 1]: continue
                    gid = f'{d}|{src}|{cote}'; fin = min(i + 60, len(w) - 1)
                    prof60 = float(((H[i:fin + 1].max() - L) if sens == 1 else (L - Lc[i:fin + 1].min())) / L * 10000)
                    reint_idx = np.where(((C[i:fin + 1] < L) if sens == 1 else (C[i:fin + 1] > L)))[0]
                    delai_reint = int(reint_idx[0]) if len(reint_idx) else None
                    cassure = (C[i] > L + L * 5 / 10000) if sens == 1 else (C[i] < L - L * 5 / 10000)
                    j_ret, inval = None, None
                    if cassure:
                        for j in range(i + 1, min(i + 61, len(w))):
                            touche = (Lc[j] <= L * 1.0005 and C[j] > L) if sens == 1 else (H[j] >= L * 0.9995 and C[j] < L)
                            if touche: j_ret = j; break
                        if j_ret is not None:
                            ri = np.where(((C[j_ret:fin + 1] < L) if sens == 1 else (C[j_ret:fin + 1] > L)))[0]
                            inval = int(ri[0]) if len(ri) else None
                    for s in SNAPS:
                        k = min(i + s, fin)
                        seg_h, seg_l = H[i:k + 1], Lc[i:k + 1]
                        prof_max = float(((seg_h.max() - L) if sens == 1 else (L - seg_l.min())) / L * 10000)
                        pos = float((C[k] - L) * sens / L * 10000)
                        duree = int(np.sum(dep[i:k + 1]))
                        vol = float(np.std(rets[i:k + 1])) if k > i else 0.0
                        base = {'date': str(d), 'grappe': gid, 'niveau': src, 'cote': cote, 'session': sess(int(w.ts.iloc[i].hour)),
                                'regime': reg, 'ere': er, 'snapshot_min': s, 'profondeur_initiale_bp': float((C[i] - L) * sens / L * 10000),
                                'prof_max_jusqua_bp': prof_max, 'prof60_retrospective_bp': prof60, 'position_bp': pos,
                                'duree_au_dela_min': duree, 'vol_realisee_bp': vol, 'spread_bp': float(SP[k]),
                                'amplitude_parcourue_bp': float((seg_h.max() - seg_l.min()) / L * 10000)}
                        # issues strictement apres k, bornees a i+60
                        apres = slice(k + 1, fin + 1)
                        if k < fin:
                            futur_c = C[apres]
                            ri2 = np.where(((futur_c < L) if sens == 1 else (futur_c > L)))[0]
                            base['reintegration_ulterior'] = float(len(ri2) > 0)
                            base['temps_restant_reint_min'] = float(ri2[0] + 1) if len(ri2) else np.nan
                            exc_fav = float(((H[apres].max() - C[k]) if sens == 1 else (C[k] - Lc[apres].min())) / L * 10000)
                            exc_adv = float(((C[k] - Lc[apres].min()) if sens == 1 else (H[apres].max() - C[k])) / L * 10000)
                            base['extension_supplementaire_bp'] = float(max(0.0, ((H[apres].max() - L) if sens == 1 else (L - Lc[apres].min())) / L * 10000 - prof_max))
                            base['excursion_favorable_bp'] = exc_fav; base['excursion_adverse_bp'] = exc_adv
                        else:
                            base.update({'reintegration_ulterior': np.nan, 'temps_restant_reint_min': np.nan, 'extension_supplementaire_bp': np.nan, 'excursion_favorable_bp': np.nan, 'excursion_adverse_bp': np.nan})
                        for h in (15, 30, 60):
                            t = k + h
                            base[f'position_plus{h}_bp'] = float((C[t] - L) * sens / L * 10000) if t <= fin else np.nan
                        base['censure_60'] = float(delai_reint is None)
                        over.append(base)
                        if cassure:
                            b = dict(base); b['delai_retest_min'] = (j_ret - i) if j_ret is not None else np.nan
                            b['retest_confirme'] = float(j_ret is not None)
                            brk.append(b)
                            if j_ret is not None and s == 0:
                                b = dict(b); b['snapshot_min'] = 'RETEST'
                                rk = j_ret
                                b['prof_max_jusqua_bp'] = float(((H[i:rk + 1].max() - L) if sens == 1 else (L - Lc[i:rk + 1].min())) / L * 10000)
                                b['position_bp'] = float((C[rk] - L) * sens / L * 10000)
                                b['invalidee_apres_retest'] = float(inval is not None)
                                for h in (15, 30, 60):
                                    t = rk + h
                                    b[f'position_plus{h}_bp'] = float((C[t] - L) * sens / L * 10000) if t <= fin + 60 and t < len(w) else np.nan
                            brk.append(b)
    O, B = pd.DataFrame(over), pd.DataFrame(brk)
    O.to_csv(ROOT / 'CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv', index=False)
    B.to_csv(ROOT / 'CAMPAIGN_02_2_BREAKOUT_TIMELINE.csv', index=False)
    (ROOT / 'C22_COVERAGE.json').write_text(json.dumps({'overshoot_rows': int(len(O)), 'episodes': int(O.grappe.count() and O[O.snapshot_min.astype(str) == '0'].shape[0]), 'breakout_rows': int(len(B))}))
    print('C2.2 TERMINE', len(O), len(B))

if __name__ == '__main__': main()
