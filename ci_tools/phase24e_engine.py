#!/usr/bin/env python3
"""PHASE 24-E - Trajectoire economique jusqu'au premier passage du label M15.
EXPLORATORY_POST_HOC (seq398). Diagnostic FIRST_LABEL_PASSAGE_EXIT_DIAGNOSTIC:
liquidation au premier prix executable strictement apres la cloture M15 confirmant
le label (delai <= 60 s sinon FIRST_PASSAGE_EXIT_NONEXECUTABLE). Aucun stop/TP.
Entrees et sorties 8h reprises de Phase 24-D. Holdout interdit."""
import io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R = ROOT / 'reports/meta_alpha'; R24 = R / 'phase24'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
NS = 10**9; GRAINE = 2127; NBOOT = 10000


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


def charge_selection():
    C = pd.read_parquet(R24 / 'PHASE24E_FIRST_PASSAGE_CATALOG.parquet')
    D = pd.read_parquet(R24 / 'PHASE24D_EVENT_PNL_RESULTS.parquet')
    C = C[(C.split == 'EVALUATION') & (C.FROZEN_SELECTION_STATUS == 'SELECTIONNE') &
          (C.LABEL_FIRST_PASSAGE_STATUS == 'REALISE')]
    return C.merge(D[['event_id', 'direction', 'prix_entree', 't_decision']], on='event_id', how='inner', suffixes=('', '_24d'))


def mode_lot():
    import duckdb
    batch = os.environ['P23_BATCH']
    inv = json.loads((R / 'INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((R / 'kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'
    S = charge_selection()
    S['jour'] = pd.to_datetime(S.t_decision).dt.strftime('%Y-%m-%d')
    jours_dispo = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                                  WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    jl = set(pd.to_datetime(jours_dispo).strftime('%Y-%m-%d'))
    S = S[S.jour.isin(jl)]
    rows = []
    for jour, gc in S.groupby('jour'):
        debut = (pd.Timestamp(jour) - pd.Timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        fin = (pd.Timestamp(jour) + pd.Timedelta(days=4)).strftime('%Y-%m-%d')
        a = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                            WHERE timestamp_utc >= '{debut}' AND timestamp_utc < '{fin}'
                            ORDER BY timestamp_utc""").fetchnumpy()
        if len(a['ts']) < 100: continue
        tt = a['ts'].astype('datetime64[ns]').astype('int64'); bid = a['bid'].astype(float); ask = a['ask'].astype(float)
        for r in gc.itertuples():
            d = int(r.direction); px_e = float(r.prix_entree)
            t_fp = pd.Timestamp(r.LABEL_FIRST_PASSAGE_TIMESTAMP).value
            t_ent = pd.Timestamp(r.t_decision).value
            t_8h = t_ent + 32 * 15 * 60 * NS
            ie = int(np.searchsorted(tt, t_ent, side='right'))
            ix = int(np.searchsorted(tt, t_fp, side='right'))
            rec = dict(event_id=r.event_id, grappe_id=r.grappe_id, semaine_iso=r.semaine_iso, direction=d)
            if ix >= len(tt) or (tt[ix] - t_fp) / NS > 60:
                rec['statut'] = 'FIRST_PASSAGE_EXIT_NONEXECUTABLE'; rows.append(rec); continue
            px_fp = float(bid[ix]) if d > 0 else float(ask[ix])
            rec.update(statut='COMPLET', prix_sortie_FP=px_fp, retard_execution_FP_sec=float((tt[ix] - t_fp) / NS))
            brut = float(d * 10000 * np.log(px_fp / px_e))
            for s_, nom in [(0.0, 'S0'), (0.5, 'S1'), (1.0, 'S2')]:
                rec[f'PNL_FP_{nom}'] = brut - 2 * s_
            seg_t = tt[ie:ix + 1]; seg_p = bid[ie:ix + 1] if d > 0 else ask[ie:ix + 1]
            flott = d * 10000 * np.log(seg_p / px_e)
            rec['MFE_avant_FP_bp'] = float(flott.max()); rec['MAE_avant_FP_bp'] = float(-flott.min())
            dtm = np.diff(seg_t) / NS / 60
            rec['temps_en_gain_min'] = float((dtm[flott[:-1] > 0]).sum()) if len(dtm) else 0.0
            rec['temps_en_perte_min'] = float((dtm[flott[:-1] < 0]).sum()) if len(dtm) else 0.0
            rec['perte_flottante_sup50_avant_FP'] = bool(flott.min() < -50)
            # post-passage jusqu a la cible 8h
            i8 = int(np.searchsorted(tt, t_8h, side='left'))
            if i8 > ix:
                seg2_p = bid[ix:i8 + 1] if d > 0 else ask[ix:i8 + 1]
                f2 = d * 10000 * np.log(seg2_p / px_fp)
                rec['excursion_favorable_post_FP'] = float(f2.max()); rec['excursion_adverse_post_FP'] = float(-f2.min())
            rows.append(rec)
        print('jour traite', jour, flush=True)
    R24.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(R24 / f'P24E_FP_{batch}.parquet', index=False)
    print('lot termine', batch, len(rows), flush=True)


def mode_analyse():
    import glob as _g
    F = pd.concat([pd.read_parquet(f) for f in _g.glob(str(R24 / 'P24E_FP_*.parquet'))]).drop_duplicates('event_id')
    D = pd.read_parquet(R24 / 'PHASE24D_EVENT_PNL_RESULTS.parquet')
    M = F.merge(D[['event_id', 'PNL_S0', 'PNL_S1', 'PNL_S2', 'MFE_bp', 'MAE_bp']], on='event_id', suffixes=('', '_8h'))
    M = M.rename(columns={'PNL_S0': 'PNL_8H_S0', 'PNL_S1': 'PNL_8H_S1', 'PNL_S2': 'PNL_8H_S2',
                          'MFE_bp': 'MFE_8H', 'MAE_bp': 'MAE_8H'})
    M['gain_restitue_S2'] = M.PNL_FP_S2 - M.PNL_8H_S2
    M.to_parquet(R24 / 'PHASE24E_FIRST_PASSAGE_EXIT_RESULTS.parquet', index=False)
    M[['event_id', 'MFE_avant_FP_bp', 'MAE_avant_FP_bp', 'temps_en_gain_min', 'temps_en_perte_min']].to_parquet(
        R24 / 'PHASE24E_PATH_TO_FIRST_PASSAGE.parquet', index=False)
    M[['event_id', 'PNL_FP_S2', 'PNL_8H_S2', 'gain_restitue_S2', 'excursion_favorable_post_FP', 'excursion_adverse_post_FP']].to_parquet(
        R24 / 'PHASE24E_POST_PASSAGE_RESTITUTION.parquet', index=False)
    C = M[M.statut == 'COMPLET'].copy()
    rng = np.random.default_rng(GRAINE)
    groupes = {g: v for g, v in C.groupby('grappe_id')}
    cles = list(groupes.keys())
    diffs = np.empty(NBOOT)
    for i in range(NBOOT):
        idx = np.concatenate([groupes[c].index.values for c in rng.choice(cles, len(cles), replace=True)])
        pos = C.index.get_indexer(idx)
        diffs[i] = (C.PNL_FP_S2.values - C.PNL_8H_S2.values)[pos].mean()
    stats = dict(n_realises=len(C), grappes=int(C.grappe_id.nunique()),
                 PNL_FP_S2_moyen=float(C.PNL_FP_S2.mean()), PNL_FP_S2_mediane=float(C.PNL_FP_S2.median()),
                 PNL_8H_sur_realises_moyen=float(C.PNL_8H_S2.mean()),
                 diff_appariee_moyenne=float((C.PNL_FP_S2 - C.PNL_8H_S2).mean()),
                 IC95_diff=tuple(np.percentile(diffs, [2.5, 97.5])),
                 part_FP_positive=float((C.PNL_FP_S2 > 0).mean()),
                 MAE_avant_FP_P95=float(C.MAE_avant_FP_bp.quantile(.95)),
                 part_perte_flottante_sup50=float(C.perte_flottante_sup50_avant_FP.mean()))
    (R24 / '_phase24e_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(stats, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
