#!/usr/bin/env python3
"""PHASE 18-B - Extraction controlee des six variables causales validees en 18-A.
Formules gelees: reports/meta_alpha/phase18/PHASE18A_CANDIDATE_VARIABLES.csv.
lot: variables tick (QUOTE_UPDATE_RATE_5M, MAX_QUOTE_GAP_15M, SPREAD_TREND_5M)
sur partitions IS du lot, fenetres closes a t_decision (aucun tick > t_decision).
analyse: variables barres depuis P13B_BARS committes + assemblage + audits.
Aucun entrainement, aucun label, aucun resultat economique. Holdout jamais accede."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R13 = ROOT / 'reports/meta_alpha/phase13'
R17 = ROOT / 'reports/meta_alpha/phase17'
R18 = ROOT / 'reports/meta_alpha/phase18'
IS_END = pd.Timestamp('2020-01-20 09:36:27')

def evenements():
    lab = pd.read_csv(R17 / 'PHASE17B_LABELS_B08.csv',
                      usecols=['event_id', 'grappe_id', 'ensemble', 't_decision'])
    lab['t_decision'] = pd.to_datetime(lab.t_decision)
    return lab

def telecharger_batch(batch):
    tok = os.environ['KAGGLE_API_TOKEN']
    import requests
    url = f'https://www.kaggle.com/api/v1/datasets/download/shalom5123/{batch}'
    r = None
    for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None), ({}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
        r = requests.get(url, headers=hdrs, auth=auth, timeout=900)
        print('Kaggle', batch, r.status_code, flush=True)
        if r.status_code == 200: break
    if r is None or r.status_code != 200: raise RuntimeError('Kaggle KO ' + batch)
    dd = pathlib.Path('/tmp/kbatch'); shutil.rmtree(dd, ignore_errors=True); dd.mkdir(parents=True)
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(dd)
    return dd

def mode_lot():
    import duckdb
    batch = os.environ['P18_BATCH']
    E = evenements()
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute('SET threads=2')
    # evenements dont t_decision est contenu dans une partition locale
    spans = [(pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None),
              pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None), p['name']) for p in parts]
    def contient(t):
        return any(a <= t <= b for a, b, _ in spans)
    E = E[E.t_decision.map(contient)].copy()
    print('P18 lot', batch, len(parts), 'partitions,', len(E), 'evenements affectes', flush=True)
    rows = []
    for r in E.itertuples():
        t1 = r.t_decision - pd.Timedelta(minutes=15)
        frames = []
        for a, b, name in spans:
            if b < t1 or a > r.t_decision: continue
            local = localdir / name
            if not local.exists(): continue
            q = f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet('{local}')
                    WHERE timestamp_utc >= '{t1}' AND timestamp_utc <= '{r.t_decision}' ORDER BY timestamp_utc"""
            frames.append(con.execute(q).df())
        if frames:
            w = pd.concat(frames)
            w['ts'] = pd.to_datetime(w.ts, format='mixed').dt.tz_localize(None)
            w = w.sort_values('ts').drop_duplicates('ts')
        else:
            w = pd.DataFrame(columns=['ts', 'bid', 'ask'])
        rec = {'event_id': r.event_id, 'source_batch': batch, 'N_QUOTES_15M': int(len(w))}
        if len(w):
            w5 = w[w.ts >= r.t_decision - pd.Timedelta(minutes=5)]
            rec['QUOTE_UPDATE_RATE_5M'] = float(len(w5) / 5.0)
            rec['MAX_QUOTE_GAP_15M'] = float(w.ts.diff().dt.total_seconds().max()) if len(w) > 1 else np.nan
            sp = (w.ask - w.bid) / ((w.ask + w.bid) / 2) * 10000
            recent = sp[w.ts >= r.t_decision - pd.Timedelta(seconds=60)]
            avant = sp[(w.ts >= r.t_decision - pd.Timedelta(minutes=5)) & (w.ts < r.t_decision - pd.Timedelta(seconds=60))]
            rec['SPREAD_TREND_5M'] = float(recent.median() - avant.median()) if len(recent) and len(avant) else np.nan
            rec['N_QUOTES_5M'] = int(len(w5))
        rows.append(rec)
    R18.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(R18 / f'P18_TICKFEAT_{batch}.csv', index=False)
    print('P18 lot termine', batch, len(rows), flush=True)

def variables_barres(E):
    bars = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz')))])
    bars['ts'] = pd.to_datetime(bars.ts)
    if bars.ts.dt.tz is not None: bars['ts'] = bars.ts.dt.tz_localize(None)
    bars = bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True)
    bars['cloture'] = bars.ts + pd.Timedelta(minutes=1)
    mc = bars.set_index('cloture').mc
    recs = []
    for r in E.itertuples():
        rec = {'event_id': r.event_id}
        for nom, nbar, duree in [('30M', 30, 30), ('60M', 61, 61)]:
            fen = mc[(mc.index <= r.t_decision) & (mc.index > r.t_decision - pd.Timedelta(minutes=duree))]
            ok = len(fen) == nbar and (fen.index.to_series().diff().dropna() == pd.Timedelta(minutes=1)).all()
            if nom == '30M':
                rec['N_BARS_30M'] = int(len(fen))
                rec['RV_MID_30M'] = float(np.log(fen).diff().dropna().std(ddof=1) * 10000) if ok else np.nan
            else:
                rec['N_BARS_60M'] = int(len(fen))
                if ok:
                    d = fen.diff().dropna()
                    rec['PATH_EFFICIENCY_60M'] = float(abs(fen.iloc[-1] - fen.iloc[0]) / d.abs().sum()) if d.abs().sum() > 0 else np.nan
                    sg = np.sign(d.values); rec['REVERSAL_COUNT_60M'] = int(sum(1 for i in range(1, len(sg)) if sg[i] != 0 and sg[i-1] != 0 and sg[i] != sg[i-1]))
                else:
                    rec['PATH_EFFICIENCY_60M'] = np.nan; rec['REVERSAL_COUNT_60M'] = np.nan
        recs.append(rec)
    return pd.DataFrame(recs)

def mode_analyse():
    E = evenements()
    tick = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R18 / 'P18_TICKFEAT_*.csv')))])
    doublons = int(tick.event_id.duplicated().sum())
    tick = tick.drop_duplicates('event_id')
    bar = variables_barres(E)
    out = E.merge(tick, on='event_id', how='left').merge(bar, on='event_id', how='left')
    VARS6 = ['QUOTE_UPDATE_RATE_5M', 'MAX_QUOTE_GAP_15M', 'SPREAD_TREND_5M', 'RV_MID_30M', 'PATH_EFFICIENCY_60M', 'REVERSAL_COUNT_60M']
    out = out[['event_id', 'grappe_id', 'ensemble', 't_decision'] + VARS6 +
              ['N_QUOTES_15M', 'N_QUOTES_5M', 'N_BARS_30M', 'N_BARS_60M', 'source_batch']]
    out.to_parquet(R18 / 'PHASE18B_CAUSAL_FEATURES.parquet', index=False)
    # couverture
    rows = []
    for v in VARS6:
        for ens, g in out.groupby('ensemble'):
            rows.append(dict(variable=v, ensemble=ens, n_attendus=int(len(g)), n_valides=int(g[v].notna().sum()),
                             n_manquants=int(g[v].isna().sum()), couverture=float(g[v].notna().mean()),
                             non_finis=int((~np.isfinite(g[v].dropna())).sum()) if g[v].notna().any() else 0))
    pd.DataFrame(rows).to_csv(R18 / 'PHASE18B_FEATURE_COVERAGE.csv', index=False)
    rec = []
    for ens, g in E.groupby('ensemble'):
        o = out[out.ensemble == ens]
        rec.append(dict(ensemble=ens, evenements_attendus=int(len(g)), retrouves_parquet=int(len(o)),
                        doublons_tick_bruts=doublons if ens == 'APPRENTISSAGE' else 0,
                        sans_lot_tick=int(o.source_batch.isna().sum())))
    pd.DataFrame(rec).to_csv(R18 / 'PHASE18B_EVENT_RECONCILIATION.csv', index=False)
    # redondance descriptive (variables uniquement, aucun resultat economique)
    fea = pd.read_csv(R17 / 'PHASE17B_FEATURES_B08.csv')
    j = out.merge(fea, on=['event_id', 'grappe_id', 'ensemble'], how='inner')
    ANCIENNES = ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN', 'MFE_A_TREINT_BP',
                 'NB_TOUCHES_P0_AVANT_TREINT', 'ATR14_H1', 'SPREAD_DECISION_BP']
    lignes = []
    for v in VARS6:
        for a in ANCIENNES:
            s = j[[v, a]].dropna()
            lignes.append(dict(nouvelle=v, ancienne=a, n=int(len(s)),
                               pearson=float(s[v].corr(s[a])) if len(s) > 2 else None,
                               spearman=float(s[v].rank().corr(s[a].rank())) if len(s) > 2 else None))
    for i, v in enumerate(VARS6):
        for a in VARS6[i + 1:]:
            s = j[[v, a]].dropna()
            lignes.append(dict(nouvelle=v, ancienne=a, n=int(len(s)),
                               pearson=float(s[v].corr(s[a])) if len(s) > 2 else None,
                               spearman=float(s[v].rank().corr(s[a].rank())) if len(s) > 2 else None))
    pd.DataFrame(lignes).to_csv(R18 / 'PHASE18B_REDUNDANCY_MATRIX.csv', index=False)
    print('P18 analyse terminee', len(out), 'evenements; doublons tick:', doublons, flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
