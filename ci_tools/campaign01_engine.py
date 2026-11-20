"""CAMPAGNE 1 - EVENEMENTS STRUCTURELS DESCRIPTIFS (dictionnaire gele seq157).
Aucun PnL, aucune entree de trade: anatomie d'evenements (pendant vs apres)."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign01'); ROOT.mkdir(parents=True, exist_ok=True)
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
            print('C1 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    bars = pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)
    return bars

def futurs(g, i, prix_ref):
    """Amplitudes futures (range) 1/5/15/30/60 min apres l'index i (descriptif)."""
    out = {}
    for H in [1, 5, 15, 30, 60]:
        w = g.iloc[i + 1:i + 1 + H]
        out[f'amp_futur_{H}'] = float((w.h.max() - w.l.min()) / prix_ref * 10000) if len(w) else np.nan
    return out

def main():
    bars = charger()
    bars['date'] = bars.ts.dt.date; bars['heure'] = bars.ts.dt.hour
    # seuil impulsion M5 poole (descriptif declare au dictionnaire)
    b5 = bars.set_index('ts').resample('5min').agg(o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last')).dropna().reset_index()
    b5['r'] = (b5.c / b5.c.shift(1) - 1) * 10000
    P90_M5 = float(b5.r.abs().quantile(0.9)); MED_AMP_M1 = float((bars.h - bars.l).median())
    ev = []
    jours = {d: g.reset_index(drop=True) for d, g in bars.groupby('date')}
    dates = sorted(jours)
    ranges60_trailing = []
    for di, d in enumerate(dates):
        g = jours[d]; reg = REG.get(d, 'NON_CLASSE'); er = era(d)
        if len(g) < 300: continue
        asia = g[g.heure < 8]
        niveaux = {}
        if len(asia) >= 60: niveaux['ASIE'] = (float(asia.h.max()), float(asia.l.min()))
        if di > 0 and len(jours[dates[di - 1]]) >= 300:
            pv = jours[dates[di - 1]]; niveaux['VEILLE'] = (float(pv.h.max()), float(pv.l.min()))
        # EV1 extremes de session/journee
        for nom, gg in [('JOUR', g)] + [(s, g[g.heure.between(a, b - 1)]) for s, a, b in [('ASIE', 0, 8), ('LONDRES', 8, 13), ('NEWYORK', 13, 21)]]:
            if len(gg) < 30: continue
            ev.append({'famille': 'EV1_EXTREMES', 'contexte': nom, 'session': sess(int(gg.ts.iloc[0].hour)), 'regime': reg, 'ere': er,
                       'date': str(d), 'grappe': f'{d}|{nom}', 'heure_formation_haut': float(gg.ts.iloc[int(gg.h.idxmax() - gg.index[0])].hour) if False else float(gg.loc[gg.h.idxmax(), 'ts'].hour),
                       'heure_formation_bas': float(gg.loc[gg.l.idxmin(), 'ts'].hour), 'spread_event': float(gg.sp.median())})
        if not niveaux: continue
        w = g[g.heure >= 8].reset_index(drop=True)
        for src, (hi, lo) in niveaux.items():
            for cote, L, sens in [('HAUT', hi, 1), ('BAS', lo, -1)]:
                depasse = (w.c > L) if sens == 1 else (w.c < L)
                idx = np.where(depasse.values)[0]
                for i in idx:
                    if i > 0 and depasse.values[i - 1]: continue  # debut de depassement seulement
                    fen = w.iloc[i:i + 61]
                    prof = float(((fen.h.max() - L) if sens == 1 else (L - fen.l.min())) / L * 10000)
                    reint = np.where(((fen.c < L) if sens == 1 else (fen.c > L)).values)[0]
                    delai = int(reint[0]) if len(reint) else np.nan
                    base = {'contexte': src, 'session': sess(int(w.ts.iloc[i].hour)), 'regime': reg, 'ere': er, 'date': str(d),
                            'grappe': f'{d}|{src}|{cote}', 'spread_event': float(w.sp.iloc[i]), 'profondeur_bp': prof, 'delai_reintegration_min': delai}
                    ev.append({'famille': 'EV2_DEPASSEMENT', **base, **futurs(w, i, L)})
                    if len(reint):
                        ev.append({'famille': 'EV2_REINTEGRATION', **base, **futurs(w, i + int(delai), L)})
                    # EV3 cassure +5bp puis retest
                    buf = L * 5 / 10000
                    if (w.c.iloc[i] > L + buf) if sens == 1 else (w.c.iloc[i] < L - buf):
                        ev.append({'famille': 'EV3_CASSURE', **base})
                        for j in range(i + 1, min(i + 61, len(w))):
                            touche = (w.l.iloc[j] <= L * 1.0005 and w.c.iloc[j] > L) if sens == 1 else (w.h.iloc[j] >= L * 0.9995 and w.c.iloc[j] < L)
                            if touche:
                                encore = (w.c.iloc[min(j + 60, len(w) - 1)] > L) if sens == 1 else (w.c.iloc[min(j + 60, len(w) - 1)] < L)
                                ev.append({'famille': 'EV3_RETEST', **base, 'delai_retour_test_min': j - i, 'encore_au_dela_60': float(encore), **futurs(w, j, L)}); break
        # EV5 impulsions M5 du jour
        g5 = b5[b5.ts.dt.date == d]
        for k in range(1, len(g5)):
            r = g5.r.iloc[k]
            if abs(r) >= P90_M5:
                seg = g5.r.iloc[k + 1:k + 13]
                adv = -np.sign(r) * np.cumsum(seg.values) if len(seg) else np.array([])
                ev.append({'famille': 'EV5_IMPULSION', 'contexte': 'M5', 'session': sess(int(g5.ts.iloc[k].hour)), 'regime': reg, 'ere': er,
                           'date': str(d), 'grappe': f'{d}|IMP', 'spread_event': np.nan, 'amplitude_impulsion_bp': float(abs(r)),
                           'retracement_max_pct': float(adv.max() / abs(r) * 100) if len(adv) else np.nan,
                           'retour_50': float((adv >= 0.5 * abs(r)).any()) if len(adv) else np.nan,
                           'retour_100': float((adv >= abs(r)).any()) if len(adv) else np.nan})
        # EV6 consolidations M1 >= 6 barres sous mediane d'amplitude
        amp = (g.h - g.l).values; run = 0
        for i, a in enumerate(amp):
            if a < MED_AMP_M1: run += 1
            else:
                if run >= 6:
                    w60 = g.iloc[i:i + 60]
                    ev.append({'famille': 'EV6_CONSOLIDATION', 'contexte': 'M1', 'session': sess(int(g.ts.iloc[max(i - run, 0)].hour)), 'regime': reg, 'ere': er,
                               'date': str(d), 'grappe': f'{d}|CONS', 'spread_event': float(g.sp.iloc[i - 1]), 'duree_barres': int(run),
                               'range_suivant_60_bp': float((w60.h.max() - w60.l.min()) / g.c.iloc[i - 1] * 10000) if len(w60) else np.nan})
                run = 0
    E = pd.DataFrame(ev); E.to_csv(ROOT / 'CAMPAIGN_01_EVENTS_RAW.csv', index=False)
    # syntheses: famille x contexte (global/session/regime/ere)
    rows = []
    for (fam, dim, val), x in [(k1, 'GLOBAL', 'TOUT') for k1 in E.famille.unique()] + \
                              [(f, 'SESSION', v) for f in E.famille.unique() for v in ['ASIE', 'LONDRES', 'NEWYORK', 'NUIT']] + \
                              [(f, 'REGIME', v) for f in E.famille.unique() for v in ['BAS', 'MOYEN', 'HAUT']] + \
                              [(f, 'ERE', v) for f in E.famille.unique() for v in ['2010_2013', '2014_2016', '2017_2020']]:
        xx = E[E.famille == fam] if dim == 'GLOBAL' else E[(E.famille == fam) & (E[dict(SESSION='session', REGIME='regime', ERE='ere')[dim]] == val)]
        if not len(xx): continue
        row = {'famille': fam, 'dimension': dim, 'valeur': val, 'n_evenements': int(len(xx)), 'n_grappes': int(xx.grappe.nunique()),
               'n_journees': int(xx.date.nunique()), 'statut': 'RENSEIGNEE' if (len(xx) >= 200 and xx.grappe.nunique() >= 100) else 'NON CONCLUANTE - effectifs'}
        for col in ['profondeur_bp', 'delai_reintegration_min', 'duree_barres', 'retracement_max_pct', 'amplitude_impulsion_bp', 'spread_event', 'amp_futur_60', 'range_suivant_60_bp']:
            if col in xx: row[f'{col}_med'] = round(float(xx[col].median()), 3)
        for col in ['encore_au_dela_60', 'retour_50', 'retour_100']:
            if col in xx: row[f'{col}_freq'] = round(float(xx[col].mean()), 3)
        rows.append(row)
    pd.DataFrame(rows).to_csv(ROOT / 'CAMPAIGN_01_EVENT_METRICS.csv', index=False)
    pd.DataFrame(rows).to_csv(ROOT / 'CAMPAIGN_01_CONDITIONAL_COMPARISONS.csv', index=False)
    (ROOT / 'C1_COVERAGE.json').write_text(json.dumps({'evenements_bruts': int(len(E)), 'familles': E.famille.value_counts().to_dict(), 'P90_M5_bp': P90_M5, 'mediane_amp_M1': MED_AMP_M1}))
    print('CAMPAGNE 1 CALCUL TERMINE', len(E))

if __name__ == '__main__': main()
