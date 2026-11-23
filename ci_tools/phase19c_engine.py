#!/usr/bin/env python3
"""PHASE 19-C - Sorties temporelles appariees H8/H16, cohorte d'evaluation 13-B/17-B.
lot: par evenement expose, entree (premier tick > t_decision), sorties premier tick
>= entree+8h et >= entree+16h, extremes de liquidation et temps en perte par horizon.
analyse: P&L via remplir() gele (Phase 19-B verifie), comparaison appariee, bootstrap
par grappe. Aucune barriere, aucun modele. Holdout jamais accede."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R17 = ROOT / 'reports/meta_alpha/phase17'
R19 = ROOT / 'reports/meta_alpha/phase19'
IS_END = pd.Timestamp('2020-01-20 09:36:27')

def population():
    lab = pd.read_csv(R17 / 'PHASE17B_LABELS_B08.csv')
    E = lab[lab.ensemble == 'EVALUATION'][['event_id', 'grappe_id', 'direction', 't_decision',
                                           'timestamp_entree', 'prix_entree', 'statut_entree']].copy()
    E['t_decision'] = pd.to_datetime(E.t_decision)
    return E

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
    batch = os.environ['P19_BATCH']
    E = population()
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute('SET threads=2')
    spans = [(pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None),
              pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None), p['name']) for p in parts]
    E = E[E.t_decision.map(lambda t: any(a <= t <= b for a, b, _ in spans))].copy()
    print('P19 lot', batch, len(parts), 'partitions,', len(E), 'evenements', flush=True)
    rows = []
    for r in E.itertuples():
        liq = 'bid' if r.direction == 1 else 'ask'
        debut = r.t_decision; fin = r.t_decision + pd.Timedelta(hours=20)
        frames = []
        for a, b, name in spans:
            if b < debut or a > fin: continue
            local = localdir / name
            if not local.exists(): continue
            q = f"""SELECT timestamp_utc AS ts, bid, ask, {liq} AS liq FROM read_parquet('{local}')
                    WHERE timestamp_utc > '{debut}' AND timestamp_utc <= '{fin}' ORDER BY timestamp_utc"""
            frames.append(con.execute(q).df())
        if not frames: continue
        w = pd.concat(frames); w['ts'] = pd.to_datetime(w.ts, format='mixed').dt.tz_localize(None)
        w = w.sort_values('ts').drop_duplicates('ts').reset_index(drop=True)
        if not len(w): continue
        t0 = w.iloc[0]; entree = float(t0.ask if r.direction == 1 else t0.bid); te = t0.ts
        rec = {'event_id': r.event_id, 'source_batch': batch, 'ts_entree': str(te), 'prix_entree_calcule': entree,
               'prix_entree_17B': r.prix_entree, 'ts_entree_17B': r.timestamp_entree}
        for H in (8, 16):
            cible = te + pd.Timedelta(hours=H)
            apres = w[w.ts >= cible]
            seg = w[w.ts <= (apres.ts.iloc[0] if len(apres) else w.ts.iloc[-1])]
            rec[f'sortie_disponible_H{H}'] = int(len(apres) > 0)
            if len(apres):
                s = apres.iloc[0]
                rec[f'ts_sortie_H{H}'] = str(s.ts); rec[f'prix_sortie_H{H}'] = float(s.liq)
                rec[f'delai_sortie_s_H{H}'] = float((s.ts - cible).total_seconds())
            pnl = r.direction * (seg.liq - entree)
            rec[f'MFE_H{H}'] = float(pnl.max()); rec[f'MAE_H{H}'] = float(pnl.min())
            durees = seg.ts.diff().dt.total_seconds().shift(-1)
            en_perte = (pnl.iloc[:-1] < 0).values
            rec[f'temps_en_perte_s_H{H}'] = float(np.nansum(durees.iloc[:-1].values[en_perte])) if len(seg) > 1 else 0.0
            rec[f'duree_observee_s_H{H}'] = float((seg.ts.iloc[-1] - te).total_seconds())
        rows.append(rec)
    R19.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=['event_id','source_batch','ts_entree','prix_entree_calcule']).to_csv(R19 / f'P19_HORIZONS_{batch}.csv', index=False) if not rows else pd.DataFrame(rows).to_csv(R19 / f'P19_HORIZONS_{batch}.csv', index=False)
    print('P19 lot termine', batch, len(rows), flush=True)

def remplir(direction, pe, ps, s):
    if direction == 1: a, b = pe * (1 + s / 10000), ps * (1 - s / 10000)
    else: a, b = pe * (1 - s / 10000), ps * (1 + s / 10000)
    return float(direction * np.log(b / a) * 10000)

def mode_analyse():
    E = population()
    H = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R19 / 'P19_HORIZONS_*.csv'))) if pathlib.Path(f).stat().st_size > 50])
    doublons = int(H.event_id.duplicated().sum()); H = H.drop_duplicates('event_id')
    j = E.merge(H, on='event_id', how='left')
    resultats = {}
    for Hh in (8, 16):
        d = j[j[f'sortie_disponible_H{Hh}'] == 1].copy()
        for scen, s in [('S0', 0.0), ('S1', 0.5), ('S2', 1.0)]:
            d[f'PL_{scen}'] = [remplir(int(r.direction), float(r.prix_entree_calcule), float(r[f'prix_sortie_H{Hh}']), s)
                               for r in d.itertuples()]
        d = d.rename(columns={f'ts_sortie_H{Hh}': 'ts_sortie', f'prix_sortie_H{Hh}': 'prix_sortie',
                              f'delai_sortie_s_H{Hh}': 'delai_sortie_s', f'MFE_H{Hh}': 'MFE_prix',
                              f'MAE_H{Hh}': 'MAE_prix', f'temps_en_perte_s_H{Hh}': 'temps_en_perte_s',
                              f'duree_observee_s_H{Hh}': 'duree_observee_s'})
        resultats[Hh] = d
        d[['event_id', 'grappe_id', 'direction', 'ts_entree', 'prix_entree_calcule', 'ts_sortie', 'prix_sortie',
           'delai_sortie_s', 'MFE_prix', 'MAE_prix', 'temps_en_perte_s', 'duree_observee_s',
           'PL_S0', 'PL_S1', 'PL_S2']].to_parquet(R19 / f'PHASE19C_H{Hh}_EVENT_RESULTS.parquet', index=False)
    a, b = resultats[8], resultats[16]
    pair = a[['event_id', 'grappe_id', 'PL_S0', 'PL_S1', 'PL_S2']].merge(
        b[['event_id', 'PL_S0', 'PL_S1', 'PL_S2', 'MAE_prix', 'temps_en_perte_s']], on='event_id', suffixes=('_H8', '_H16'))
    for scen in ['S0', 'S1', 'S2']: pair[f'DELTA_{scen}'] = pair[f'PL_{scen}_H16'] - pair[f'PL_{scen}_H8']
    pair.to_parquet(R19 / 'PHASE19C_PAIRED_COMPARISON.parquet', index=False)
    lignes = []
    for Hh, d in resultats.items():
        for scen in ['S0', 'S1', 'S2']:
            s = d[f'PL_{scen}']
            lignes.append(dict(horizon=f'H{Hh}', scenario=scen, n=int(len(s)), PL_moyen=float(s.mean()),
                               PL_mediane=float(s.median()), part_positifs=float((s > 0).mean()),
                               q25=float(s.quantile(.25)), q75=float(s.quantile(.75)), perte_max=float(s.min())))
    for scen in ['S0', 'S1', 'S2']:
        lignes.append(dict(horizon=f'DELTA_H16-H8_{scen}', scenario=scen, n=int(len(pair)),
                           PL_moyen=float(pair[f'DELTA_{scen}'].mean()), PL_mediane=float(pair[f'DELTA_{scen}'].median()),
                           part_positifs=float((pair[f'DELTA_{scen}'] > 0).mean())))
    pd.DataFrame(lignes).to_csv(R19 / 'PHASE19C_COST_SCENARIO_COMPARISON.csv', index=False)
    # bootstrap par grappe sur DELTA_S2 (graine fixee, reproductible)
    rng = np.random.default_rng(1907)
    grappes = pair.groupby('grappe_id').DELTA_S2.mean()
    vals = grappes.values; boots = []
    for _ in range(2000):
        boots.append(rng.choice(vals, size=len(vals), replace=True).mean())
    stats = dict(n_paires=int(len(pair)), n_grappes=int(len(vals)), delta_moyen_evenements=float(pair.DELTA_S2.mean()),
                 delta_moyen_grappes=float(vals.mean()), ic95_grappes=[float(np.quantile(boots, .025)), float(np.quantile(boots, .975))],
                 part_grappes_delta_positif=float((vals > 0).mean()))
    (R19 / '_phase19c_stats.json').write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1)); print('doublons lots:', doublons)

if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
