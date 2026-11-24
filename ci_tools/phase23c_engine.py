#!/usr/bin/env python3
"""PHASE 23-C - Anatomie temporelle des reactions FOMC + candidat fige.
EXPLORATORY_POST_HOC. 73 evenements + 73 temoins 23-B = DEVELOPPEMENT uniquement.
Regles figees AVANT calcul (seq388):
- P0 = dernier Mid strictement avant t0; non validable si age P0 > 300 s.
- Points de reference: premier Mid reel a/after t0+{5,15,30,45,60,120,240} min; retard
  conserve; point non validable si retard > 300 s.
- INITIAL_REACTION_BP = 10000*ln(P15/P0); direction = signe (0 = neutre, aucune decision).
- Decision a t0+15 min; entree: LONG premier Ask strictement apres l'instant de decision,
  SHORT premier Bid; delai maximal 60 s sinon NON_EXECUTION.
- Sorties: t0+60 et t0+240 min (premier Bid/Ask reel a/after la cible, retard <= 300 s).
- Comptabilite 19-B: spread integre une fois; slippage S0=0, S1=0,5, S2=1 bp/cote (S2 principal).
- Excursions post-15 mesurees uniquement sur ticks strictement apres t0+15 min.
Aucun seuil, stop, TP, modele. Holdout interdit."""
import io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R23 = ROOT / 'reports/meta_alpha/phase23'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
NS = 10**9
POINTS = [5, 15, 30, 45, 60, 120, 240]


def logbp(a, b): return 10000 * np.log(b / a)


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
    batch = os.environ['P23_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'

    def requete(debut, fin):
        a = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                            WHERE timestamp_utc >= '{debut}' AND timestamp_utc < '{fin}'
                            ORDER BY timestamp_utc""").fetchnumpy()
        return (a['ts'].astype('datetime64[ns]').astype('int64'), a['bid'].astype(float), a['ask'].astype(float))

    cat = pd.read_csv(R23 / 'PHASE23B_OFFICIAL_EVENT_CATALOG.csv', parse_dates=['ts_utc'])
    jours_dispo = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                                  WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    jours_lot = set(pd.to_datetime(jours_dispo).strftime('%Y-%m-%d'))
    cat = cat[cat.ts_utc.dt.strftime('%Y-%m-%d').isin(jours_lot)]
    rows, revisites = [], []
    for jour, gc in cat.groupby(cat.ts_utc.dt.strftime('%Y-%m-%d')):
        debut = (pd.Timestamp(jour) - pd.Timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        fin = (pd.Timestamp(jour) + pd.Timedelta(days=2)).strftime('%Y-%m-%d')
        tt, bid, ask = requete(debut, fin)
        if len(tt) < 100: continue
        mid = (bid + ask) / 2.0
        for r in gc.itertuples():
            t0 = pd.Timestamp(r.ts_utc).value
            i_pre = int(np.searchsorted(tt, t0, side='left') - 1)
            if i_pre < 0: continue
            P0 = float(mid[i_pre]); age_p0 = (t0 - tt[i_pre]) / NS
            row = dict(type=r.type, role=r.role, ts_utc=r.ts_utc, jour=jour,
                       annee=pd.Timestamp(r.ts_utc).year, P0=P0, age_P0_sec=float(age_p0),
                       validable=bool(age_p0 <= 300))
            prix, retards = {}, {}
            for m in POINTS:
                j = int(np.searchsorted(tt, t0 + m * 60 * NS, side='left'))
                if j < len(tt):
                    prix[m] = float(mid[j]); retards[m] = (tt[j] - (t0 + m * 60 * NS)) / NS
                    row[f'P{m}'] = prix[m]; row[f'retard_P{m}_sec'] = float(retards[m])
                else:
                    row[f'P{m}'] = np.nan; row[f'retard_P{m}_sec'] = np.nan
            if 15 not in prix or np.isnan(prix.get(15, np.nan)):
                rows.append(row); continue
            reac = float(logbp(np.array([P0]), np.array([prix[15]]))[0])
            sens = int(np.sign(reac))
            row['reaction_initiale_bp'] = reac; row['direction'] = sens
            # continuations (deux notions separees)
            for h in (60, 240):
                if h in prix and not np.isnan(prix[h]) and sens != 0:
                    row[f'cont_depuis_P0_{h}'] = bool(np.sign(logbp(np.array([P0]), np.array([prix[h]]))[0]) == sens)
                    row[f'cont_apres_15_{h}'] = bool(np.sign(logbp(np.array([prix[15]]), np.array([prix[h]]))[0]) == sens)
                    row[f'depl_term_signe_{h}'] = float(sens * logbp(np.array([prix[15]]), np.array([prix[h]]))[0])
            # revisites de P0 sur (t0, t0+240m]: franchissement observable du Mid
            seg_i = slice(int(np.searchsorted(tt, t0, side='right')), int(np.searchsorted(tt, t0 + 240 * 60 * NS, side='right')))
            seg_t, seg_m = tt[seg_i], mid[seg_i]
            if sens != 0 and len(seg_m):
                cote = np.where(sens > 0, seg_m <= P0, seg_m >= P0)
                passages = int((np.sign(seg_m - P0)[1:] * np.sign(seg_m - P0)[:-1] < 0).sum()) if len(seg_m) > 1 else 0
                row['n_passages_P0_240m'] = passages
                if cote.any():
                    t_rev = (seg_t[cote][0] - t0) / NS / 60.0
                    row['premiere_revisite_min'] = float(t_rev)
                    row['revisite_fenetre'] = '<15m' if t_rev < 15 else ('15-60m' if t_rev < 60 else '60-240m')
                else:
                    row['premiere_revisite_min'] = np.nan; row['revisite_fenetre'] = 'aucune'
                row['cloture_240_au_dela_P0'] = bool(np.sign(prix.get(240, np.nan) - P0) == sens) if 240 in prix else np.nan
                revisites.append(dict(role=r.role, ts_utc=r.ts_utc, direction=sens,
                                      premiere_revisite_min=row.get('premiere_revisite_min'),
                                      fenetre=row.get('revisite_fenetre'), n_passages_P0=passages))
            # excursions post-15 (ticks strictement apres t0+15m)
            i15 = int(np.searchsorted(tt, t0 + 15 * 60 * NS, side='right'))
            for h in (60, 120, 240):
                e = int(np.searchsorted(tt, t0 + h * 60 * NS, side='right'))
                if e <= i15 or sens == 0: continue
                sm, st = mid[i15:e], tt[i15:e]
                signe_relatif = sens * logbp(np.array([prix[15]]), sm)
                row[f'MFE_post15_{h}'] = float(signe_relatif.max()); row[f'MAE_post15_{h}'] = float(-signe_relatif.min())
                row[f't_MFE_{h}_min'] = float((st[int(np.argmax(signe_relatif))] - (t0 + 15 * 60 * NS)) / NS / 60.0)
                row[f't_MAE_{h}_min'] = float((st[int(np.argmin(signe_relatif))] - (t0 + 15 * 60 * NS)) / NS / 60.0)
                row[f'n_retours_P0_post15_{h}'] = int((np.sign(sm - P0)[1:] * np.sign(sm - P0)[:-1] < 0).sum()) if len(sm) > 1 else 0
                row[f'amplitude_conservee_{h}'] = float(sens * logbp(np.array([P0]), np.array([sm[-1]]))[0] / abs(reac)) if reac != 0 else np.nan
            # execution hypothetique: decision t0+15m, entree <= 60 s, sorties 60/240
            t_dec = t0 + 15 * 60 * NS
            if sens != 0:
                ie = int(np.searchsorted(tt, t_dec, side='right'))
                delai_e = (tt[ie] - t_dec) / NS if ie < len(tt) else np.inf
                row['delai_entree_sec'] = float(delai_e)
                if ie < len(tt) and delai_e <= 60:
                    px_e = float(ask[ie]) if sens > 0 else float(bid[ie])
                    for h in (60, 240):
                        cible = t0 + h * 60 * NS
                        jx = int(np.searchsorted(tt, cible, side='left'))
                        if jx < len(tt) and (tt[jx] - cible) / NS <= 300:
                            px_s = float(bid[jx]) if sens > 0 else float(ask[jx])
                            brut = float(sens * logbp(np.array([px_e]), np.array([px_s]))[0])
                            for s_, nom in [(0.0, 'S0'), (0.5, 'S1'), (1.0, 'S2')]:
                                row[f'net_{nom}_{h}'] = brut - 2 * s_
                            row[f'statut_sortie_{h}'] = 'EXECUTE'
                        else:
                            row[f'statut_sortie_{h}'] = 'SORTIE_NON_VALIDABLE'
                else:
                    row['statut_entree'] = 'NON_EXECUTION'
            rows.append(row)
        print('jour traite', jour, flush=True)
    R23.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(R23 / f'P23C_PATH_{batch}.parquet', index=False)
    pd.DataFrame(revisites).to_csv(R23 / f'P23C_REV_{batch}.csv', index=False)
    print('lot termine', batch, len(rows), 'fenetres', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()


def mode_analyse():
    import glob as _g
    P = pd.concat([pd.read_parquet(f) for f in _g.glob(str(R23 / 'P23C_PATH_*.parquet'))])
    P = P.drop_duplicates(['role', 'ts_utc']).sort_values(['ts_utc', 'role'])
    P.to_parquet(R23 / 'PHASE23C_EVENT_PATH_METRICS.parquet', index=False)
    rev = pd.concat([pd.read_csv(f) for f in _g.glob(str(R23 / 'P23C_REV_*.csv'))]).drop_duplicates(['role', 'ts_utc'])
    rev.to_csv(R23 / 'PHASE23C_FIRST_REVISIT_CATALOG.csv', index=False)
    cols = [c for c in P.columns if any(k in c for k in ('MFE_post15', 'MAE_post15', 't_MFE', 't_MAE', 'amplitude_conservee', 'n_retours'))]
    P[['role', 'ts_utc', 'direction', 'reaction_initiale_bp'] + cols].to_parquet(
        R23 / 'PHASE23C_POST_15M_EXCURSION_RESULTS.parquet', index=False)
    lignes = []
    comp = []
    for nom, g0 in [('EVENEMENT', P[P.role == 'EVENEMENT']), ('CONTROLE', P[P.role == 'CONTROLE'])]:
        g = g0[g0.direction != 0]
        d = dict(groupe=nom, n=len(g))
        for h in (60, 240):
            d[f'cont_depuis_P0_{h}'] = float(g[f'cont_depuis_P0_{h}'].mean())
            d[f'cont_apres_15_{h}'] = float(g[f'cont_apres_15_{h}'].mean())
            d[f'MFE_med_{h}'] = float(g[f'MFE_post15_{h}'].median()); d[f'MAE_med_{h}'] = float(g[f'MAE_post15_{h}'].median())
            d[f'depl_term_med_{h}'] = float(g[f'depl_term_signe_{h}'].median())
            d[f'netS2_moy_{h}'] = float(g[f'net_S2_{h}'].mean()); d[f'netS2_med_{h}'] = float(g[f'net_S2_{h}'].median())
            d[f'netS2_sd_{h}'] = float(g[f'net_S2_{h}'].std())
        d['revisite_240 part'] = float((g.revisite_fenetre != 'aucune').mean())
        d['premiere_revisite_mediane_min'] = float(g.premiere_revisite_min.median())
        comp.append(d)
    C = pd.DataFrame(comp); C.to_csv(R23 / 'PHASE23C_EVENT_VS_CONTROL_COMPARISON.csv', index=False)
    ev = C[C.groupe == 'EVENEMENT'].iloc[0]
    stats = dict(n_evt=int(ev.n), cont_apres15_60=float(ev.cont_apres_15_60), cont_apres15_240=float(ev.cont_apres_15_240),
                 netS2_60=float(ev.netS2_moy_60), netS2_240=float(ev.netS2_moy_240),
                 puissance={str(h): int(np.ceil(((1.96 + 0.84) * float(ev[f'netS2_sd_{h}']) / 10) ** 2)) for h in (60, 240)})
    (R23 / '_phase23c_stats.json').write_text(json.dumps(stats, indent=1))
    print(C.round(3).to_string()); print(stats, flush=True)
