"""PHASE 10 - campagne mouvements capturables H1/H4/D1. Protocole gele
PHASE 10-A (seq283), preflight seq285. Signaux sur clotures Mid causales
(seuils roulants 250 barres, barre courante exclue), mesures de
rentabilite sur prix Bid/Ask (spread dans les prix, jamais soustrait),
entree a l'ouverture de la barre suivant le signal. Corpus IS uniquement
(borne IS_END); holdout jamais accede."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/phase10'); ROOT.mkdir(parents=True, exist_ok=True)
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
    print('P10 ALL', len(parts), 'partitions attendues', flush=True)
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
                q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts,
                        arg_min(bid, timestamp_utc) AS bo, max(bid) AS bh, min(bid) AS bl, arg_max(bid, timestamp_utc) AS bc,
                        arg_min(ask, timestamp_utc) AS ao, max(ask) AS ah, min(ask) AS al, arg_max(ask, timestamp_utc) AS ac,
                        arg_min(mid, timestamp_utc) AS mo, max(mid) AS mh, min(mid) AS ml, arg_max(mid, timestamp_utc) AS mc,
                        median((ask-bid)/mid)*10000 AS sp
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b); CHARGER_STATS['chargees'] += 1
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('P10 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives (testees par phase10_temporal_tests.py) ----------
def seuil_roulant(valeurs_precedentes, q):
    """Quantile causal sur les 250 dernieres valeurs precedentes (courante exclue)."""
    v = np.asarray(valeurs_precedentes, float)[-250:]
    if len(v) < 250: return np.nan
    return float(np.quantile(v, q, method='linear'))

def retour_log(c_prev, c):
    return float(np.log(c / c_prev) * 10000) if c_prev > 0 and c > 0 else np.nan

def fermeture_programmee(fin_signal):
    """fin_signal: Timestamp de fin de la barre de signal. Coupure quotidienne
    (fin ~21h UTC) ou week-end (vendredi soir) consideres fermetures regulieres."""
    return fin_signal.hour == 21 or (fin_signal.weekday() == 4 and fin_signal.hour >= 20) or fin_signal.weekday() >= 5

def construire_barres(bars_m1, minutes, min_frac=0.5):
    """Agrege les barres M1 en barres de timeframe (debut de periode)."""
    b = bars_m1.copy()
    if minutes >= 1440:
        b['per'] = b.ts.dt.floor('D')
    else:
        b['per'] = b.ts.dt.floor(f'{minutes}min')
    g = b.groupby('per')
    out = pd.DataFrame({
        'debut': g.ts.min().index, 'bo': g.bo.first(), 'bh': g.bh.max(), 'bl': g.bl.min(), 'bc': g.bc.last(),
        'ao': g.ao.first(), 'ah': g.ah.max(), 'al': g.al.min(), 'ac': g.ac.last(),
        'mo': g.mo.first(), 'mh': g.mh.max(), 'ml': g.ml.min(), 'mc': g.mc.last(),
        'sp': g.sp.median(), 'n': g.ts.count()}).reset_index(drop=True)
    attendu = 1380 if minutes >= 1440 else minutes
    out = out[out.n >= attendu * min_frac].reset_index(drop=True)
    out['fin'] = out.debut + pd.Timedelta(minutes=minutes)
    out['range_bp'] = (out.mh - out.ml) / out.mc * 10000
    return out

def evenements_tf(tf, nom_tf, minutes):
    """Detecte les evenements d'un timeframe et mesure les sillages executables."""
    n = len(tf)
    debut = tf.debut.values; fin = tf.fin.values
    mc = tf.mc.values.astype(float)
    r = np.full(n, np.nan)
    if minutes >= 1440:
        r[1:] = np.log(mc[1:] / mc[:-1]) * 10000
    else:
        ecart = (tf.debut.diff().dt.total_seconds().values // 60)
        ok = ecart == minutes
        r[1:][ok[1:]] = np.log(mc[1:][ok[1:]] / mc[:-1][ok[1:]]) * 10000
    absr = np.abs(r); rng = tf.range_bp.values.astype(float)
    ev = []
    def mesure(i, sens, fenetre_min, famille):
        # entree: barre suivante (i+1); delai controle par l'ecart a l'ouverture attendue
        if i + 1 >= n: return None
        ecart_entree = (debut[i + 1] - fin[i]) / np.timedelta64(1, 'm')
        elig = (ecart_entree == 0) or fermeture_programmee(pd.Timestamp(fin[i]))
        entree_idx = i + 1
        t_ent = debut[entree_idx]
        cible = t_ent + np.timedelta64(fenetre_min, 'm')
        j = int(np.searchsorted(debut, cible))
        if j >= n or (debut[j] - cible) / np.timedelta64(1, 'm') > fenetre_min: fenetre_ok = False
        else: fenetre_ok = True
        rec = {'famille': famille, 'timeframe': nom_tf, 't_signal': str(pd.Timestamp(fin[i])),
               'ere': era(pd.Timestamp(debut[i]).date()), 'sens': int(sens),
               'spread_bp': float(tf.sp.values[i]), 'entree_eligible': int(elig),
               'fenetre_complete': int(fenetre_ok), 't_entree': str(pd.Timestamp(t_ent)),
               't_sortie': str(pd.Timestamp(debut[j])) if j < n else None}
        if not fenetre_ok: return rec
        w = slice(entree_idx, j)
        if sens > 0:
            e = tf.ao.values[entree_idx]; s_ = tf.bo.values[j]
            fav = (tf.bh.values[w].max() / e - 1) * 10000; adv = (1 - tf.bl.values[w].min() / e) * 10000
        else:
            e = tf.bo.values[entree_idx]; s_ = tf.ao.values[j]
            fav = (1 - tf.al.values[w].min() / e) * 10000; adv = (tf.ah.values[w].max() / e - 1) * 10000
        rec.update({'rendement_signe_bp': float(sens * np.log(s_ / e) * 10000) if sens > 0 else float(-np.log(s_ / e) * 10000),
                    'mae_bp': float(adv), 'mfe_bp': float(fav),
                    'range_fenetre_bp': float((tf.mh.values[w].max() - tf.ml.values[w].min()) / tf.mc.values[entree_idx] * 10000)})
        # rendement signe oriente: pour sens>0 log(sortie/entree); pour sens<0 -log(sortie/entree) avec sortie/entree en prix executes coherents
        rec['rendement_signe_bp'] = float(np.log(s_ / e) * 10000) if sens > 0 else float(-np.log(s_ / e) * 10000)
        return rec
    seuils = {}
    if nom_tf in ('H1', 'H4'):
        fam_ext, fam_brk, fen_brk, nb_ext = (('F10-01', 'F10-02', 4 * 60, 20) if nom_tf == 'H1' else ('F10-03', 'F10-04', 24 * 60, 30))
        for i in range(n):
            th = seuil_roulant(absr[:i], 0.95)
            if np.isfinite(r[i]) and np.isfinite(th) and abs(r[i]) > th:
                rec = mesure(i, int(np.sign(r[i])), minutes, fam_ext)
                if rec: rec['seuil_bp'] = float(th); ev.append(rec)
            if i >= nb_ext:
                hi = tf.mh.values[i - nb_ext:i].max(); lo = tf.ml.values[i - nb_ext:i].min()
                if mc[i] > hi:
                    rec = mesure(i, 1, fen_brk, fam_brk)
                    if rec: ev.append(rec)
                elif mc[i] < lo:
                    rec = mesure(i, -1, fen_brk, fam_brk)
                    if rec: ev.append(rec)
    else:
        for i in range(n):
            th = seuil_roulant(absr[:i], 0.90)
            if np.isfinite(r[i]) and np.isfinite(th) and abs(r[i]) > th:
                rec = mesure(i, int(np.sign(r[i])), 1440, 'F10-05')
                if rec: rec['seuil_bp'] = float(th); ev.append(rec)
            thq = seuil_roulant(rng[:i], 0.25)
            if np.isfinite(thq) and rng[i] < thq:
                med_prec = float(np.median(rng[max(0, i - 250):i])) if i >= 250 else np.nan
                if i + 1 < n and np.isfinite(med_prec):
                    ev.append({'famille': 'F10-06', 'timeframe': 'D1', 't_signal': str(pd.Timestamp(fin[i])),
                               'ere': era(pd.Timestamp(debut[i]).date()), 'sens': 0, 'spread_bp': float(tf.sp.values[i]),
                               'entree_eligible': 1, 'fenetre_complete': 1,
                               't_entree': str(pd.Timestamp(debut[i + 1])), 't_sortie': str(pd.Timestamp(fin[i + 1])),
                               'ratio_range': float(rng[i + 1] / med_prec), 'range_lendemain_bp': float(rng[i + 1]),
                               'mae_bp': np.nan, 'mfe_bp': np.nan, 'rendement_signe_bp': np.nan,
                               'range_fenetre_bp': float(rng[i + 1])})
    return ev

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    all_ev = []
    resume = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
              'barres_m1': int(len(bars)), 'barres_tf': {}}
    for nom_tf, minutes in [('H1', 60), ('H4', 240), ('D1', 1440)]:
        tf = construire_barres(bars, minutes)
        resume['barres_tf'][nom_tf] = int(len(tf))
        ev = evenements_tf(tf, nom_tf, minutes)
        all_ev += ev
        print('P10', nom_tf, 'barres', len(tf), 'evenements', len(ev), flush=True)
    EV = pd.DataFrame(all_ev)
    EV.round(4).to_csv(ROOT / 'PHASE10_EVENTS.csv.gz', index=False, compression='gzip')
    if len(EV):
        resume['evenements_par_famille'] = {k: int(v) for k, v in EV.famille.value_counts().items()}
        resume['entree_eligibles'] = int(EV.entree_eligible.sum()); resume['fenetres_completes'] = int(EV.fenetre_complete.sum())
    (ROOT / 'P10_COVERAGE.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume), flush=True)

if __name__ == '__main__': main()
