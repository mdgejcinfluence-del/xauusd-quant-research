#!/usr/bin/env python3
"""PHASE 14-B - Anatomie MFE/MAE et trois barrieres (exploratoire IS).

Preenregistrement gele: reports/meta_alpha/phase14/ (seq334). Aucune
configuration, aucun seuil, aucun multiplicateur hors grille gelee.
Modes:
  lot     (env P14_BATCH): pour chaque partition IS du batch, extrait pour
          les 443 evenements exposes 13-B dont la fenetre intersecte la
          partition: les ticks de liquidation atteignant un nouvel extreme
          courant dans le morceau, les trous de cotation (> 5 min) et les
          bornes du morceau. Sortie: P14_PATH_<batch>.csv.
  analyse : fusionne les morceaux, reconstruit l'ordre MFE/MAE, les
          quartiles de confiance (p_M1 seul), l'ATR14_H1 Wilder (H1 Mid,
          bougies cloturees a t_decision), puis les 18 configurations de
          barrieres x 3 scenarios et ecrit les livrables PHASE14_*.
Holdout 2020-2026: jamais accede (filtre IS_END historique).
"""
import glob
import io
import json
import os
import pathlib
import shutil
import zipfile
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R13 = ROOT / 'reports/meta_alpha/phase13'
R12 = ROOT / 'reports/meta_alpha/phase12'
R14 = ROOT / 'reports/meta_alpha/phase14'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
M0 = 0.7591463414634146
SCEN = {'S0': 0.0, 'S1': 0.5, 'S2': 1.0}
GRID = [(f'B{i:02d}', tp, sl) for i, (tp, sl) in enumerate(
    [(0.5, 0.5), (0.5, 1.0), (0.5, 1.5), (1.0, 0.5), (1.0, 1.0),
     (1.0, 1.5), (1.5, 0.5), (1.5, 1.0), (1.5, 1.5)], start=1)]
LABELS = {'S0': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE',
          'S1': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_0_5_BP_PER_SIDE',
          'S2': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_1_0_BP_PER_SIDE'}


def evenements():
    E = pd.read_csv(R13 / 'PHASE13B_EVENT_EXECUTIONS.csv')
    E = E[E.decision_exposition == 'EXPOSITION'].copy()
    assert len(E) == 443, f'exposes attendus 443, obtenu {len(E)}'
    F = pd.read_csv(R12 / 'PHASE12B_FEATURES.csv',
                    usecols=['event_id', 'MFE_A_TREINT_BP', 'fin_fenetre_observation'])
    E = E.merge(F, on='event_id', how='left', validate='one_to_one')
    E['t_entree'] = pd.to_datetime(E.timestamp_entree).dt.tz_localize(None)
    E['t_decision_ts'] = pd.to_datetime(E.t_decision)
    E['fin'] = pd.to_datetime(E.fin_fenetre_observation)
    E['t_sortie_13b'] = pd.to_datetime(E.timestamp_sortie, errors='coerce')
    if E.t_sortie_13b.dt.tz is not None:
        E['t_sortie_13b'] = E.t_sortie_13b.dt.tz_localize(None)
    return E


# ------------------------------------------------------------------ lot CI
def telecharger_batch(batch):
    tok = os.environ['KAGGLE_API_TOKEN']
    import requests
    url = f'https://www.kaggle.com/api/v1/datasets/download/shalom5123/{batch}'
    r = None
    for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None),
                       ({}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
        r = requests.get(url, headers=hdrs, auth=auth, timeout=900)
        print('Kaggle', batch, r.status_code, flush=True)
        if r.status_code == 200:
            break
    if r is None or r.status_code != 200:
        raise RuntimeError(f'telechargement Kaggle KO: {batch}')
    localdir = pathlib.Path('/tmp/kbatch')
    shutil.rmtree(localdir, ignore_errors=True)
    localdir.mkdir(parents=True)
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(localdir)
    return localdir


def mode_lot():
    import duckdb
    batch = os.environ['P14_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json')
                     .read_text())['partitions']
    kstate = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json')
                        .read_text())
    batchof = {n: i['batch'] for n, i in kstate['uploaded'].items()}
    parts = [p for p in inv
             if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00'))
             .tz_localize(None) <= IS_END and batchof.get(p['name']) == batch]
    ev = evenements()
    localdir = telecharger_batch(batch)
    con = duckdb.connect()
    con.execute("SET memory_limit='5GB'")
    con.execute('SET threads=2')
    rows = []
    for p in parts:
        local = localdir / p['name']
        if not local.exists():
            continue
        pmin = pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None)
        pmax = pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None)
        cand = ev[(ev.t_entree < pmax) & (ev.fin > pmin)]
        for r in cand.itertuples():
            liq = 'bid' if r.direction == 1 else 'ask'
            base = f"""SELECT timestamp_utc AS ts, bid, ask, {liq} AS liq
                       FROM read_parquet('{local}')
                       WHERE timestamp_utc >= '{r.t_entree}' AND
                             timestamp_utc <= '{r.fin}' ORDER BY timestamp_utc"""
            q = f"""WITH s AS ({base}),
                    w AS (SELECT *, max(liq) OVER (ORDER BY ts ROWS BETWEEN
                                  UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmax,
                                  min(liq) OVER (ORDER BY ts ROWS BETWEEN
                                  UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmin,
                                  lag(ts) OVER (ORDER BY ts) AS pts
                          FROM s)
                    SELECT ts, bid, ask, liq, pts, pmax, pmin FROM w
                    WHERE pmax IS NULL OR liq > pmax OR liq < pmin
                          OR (pts IS NOT NULL AND
                              epoch(ts) - epoch(pts) > 300)"""
            w = con.execute(q).df()
            if not len(w):
                continue
            w['ts'] = pd.to_datetime(w.ts).dt.tz_localize(None)
            trous = w[w.pts.notna() & ((w.ts - pd.to_datetime(w.pts).dt.tz_localize(None)).dt.total_seconds() > 300)]
            for t in trous.itertuples():
                rows.append({'event_id': r.event_id, 'kind': 'HOLE',
                             'ts': str(pd.Timestamp(t.pts).tz_localize(None)),
                             'ts2': str(t.ts), 'liq': np.nan,
                             'bid': np.nan, 'ask': np.nan})
            ext = w[(w.pmax.isna()) | (w.liq > w.pmax) | (w.liq < w.pmin)]
            for t in ext.itertuples():
                rows.append({'event_id': r.event_id, 'kind': 'EXTREME',
                             'ts': str(t.ts), 'ts2': '', 'liq': float(t.liq),
                             'bid': float(t.bid), 'ask': float(t.ask)})
            rows.append({'event_id': r.event_id, 'kind': 'BOUND',
                         'ts': str(w.ts.iloc[0]), 'ts2': str(w.ts.iloc[-1]),
                         'liq': float(len(w)), 'bid': np.nan, 'ask': np.nan})
        print('P14 part', p['name'], flush=True)
    R14.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=['event_id', 'kind', 'ts', 'ts2', 'liq', 'bid', 'ask']) \
        .to_csv(R14 / f'P14_PATH_{batch}.csv', index=False)
    print('P14 lot termine', batch, len(rows), 'lignes', flush=True)


# ------------------------------------------------------------------ analyse
def stats(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        return {}
    q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    return {'n': int(len(x)), 'moyenne': float(x.mean()), 'mediane': float(q[3]),
            'p1': float(q[0]), 'p5': float(q[1]), 'p25': float(q[2]),
            'p75': float(q[4]), 'p95': float(q[5]), 'p99': float(q[6]),
            'part_positifs': float((x > 0).mean()),
            'perte_maximale': float(x.min()), 'gain_maximal': float(x.max())}


def atr_series():
    bars = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz')))])
    bars['ts'] = pd.to_datetime(bars.ts)
    if bars.ts.dt.tz is not None:
        bars['ts'] = bars.ts.dt.tz_localize(None)
    bars = bars.drop_duplicates('ts').sort_values('ts')
    bars['heure'] = bars.ts.dt.floor('h')
    H = bars.groupby('heure').agg(o=('mo', 'first'), h=('mh', 'max'),
                                  l=('ml', 'min'), c=('mc', 'last')).reset_index()
    pc = H.c.shift(1)
    H['tr'] = np.maximum(H.h - H.l,
                         np.maximum((H.h - pc).abs(), (H.l - pc).abs()))
    atr = np.full(len(H), np.nan)
    if len(H) > 14:
        atr[14] = H.tr.iloc[1:15].mean()
        for i in range(15, len(H)):
            atr[i] = (13 * atr[i - 1] + H.tr.iloc[i]) / 14
    H['atr'] = atr
    H['cloture'] = H.heure + pd.Timedelta(hours=1)
    return H[['cloture', 'atr']].dropna()


def mode_analyse():
    E = evenements().reset_index(drop=True)
    # ---- fusion des chemins tick
    frames = []
    for f in sorted(glob.glob(str(R14 / 'P14_PATH_*.csv'))):
        try:
            tf = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            continue
        if len(tf):
            frames.append(tf)
    P = pd.concat(frames)
    P['ts'] = pd.to_datetime(P.ts, format='mixed')
    seq_rows, path = [], {}
    controle_entree = {'verifies': 0, 'divergents': 0}
    for r in E.itertuples():
        d = P[P.event_id == r.event_id]
        ext = (d[d.kind == 'EXTREME'].drop_duplicates(['ts', 'liq'])
               .sort_values('ts').reset_index(drop=True))
        trous = d[d.kind == 'HOLE']
        bounds = d[d.kind == 'BOUND']
        dernier_tick = pd.to_datetime(bounds.ts2, format='mixed').max() if len(bounds) else pd.NaT
        premier_trou = pd.to_datetime(trous.ts).min() if len(trous) else pd.NaT
        # extremes globaux (nouveaux extremes courants sur la sequence fusionnee)
        recs, cmax, cmin = [], -np.inf, np.inf
        for t in ext.itertuples():
            if t.liq > cmax or t.liq < cmin:
                recs.append(t)
                cmax = max(cmax, t.liq)
                cmin = min(cmin, t.liq)
        path[r.event_id] = {'recs': recs, 'trous_fin': set(pd.to_datetime(trous.ts2, format='mixed')) if len(trous) else set(),
                            'premier_trou': premier_trou, 'dernier_tick': dernier_tick}
        if len(recs):
            t0 = recs[0]
            prix_tick = t0.ask if r.direction == 1 else t0.bid
            if abs(prix_tick - r.prix_entree) < 1e-9 and t0.ts == r.t_entree:
                controle_entree['verifies'] += 1
            else:
                controle_entree['divergents'] += 1
        liqs = pd.DataFrame(recs)
        if not len(liqs):
            seq_rows.append({'event_id': r.event_id, 'grappe_id': r.grappe_id,
                             'p_M1': r.p_M1, 'ordre': 'CENSORED',
                             'statut_completude': r.statut_completude})
            continue
        i_max = liqs.liq.idxmax()
        i_min = liqs.liq.idxmin()
        ts_mfe = liqs.loc[i_max, 'ts'] if r.direction == 1 else liqs.loc[i_min, 'ts']
        ts_mae = liqs.loc[i_min, 'ts'] if r.direction == 1 else liqs.loc[i_max, 'ts']
        mfe = max(r.direction * np.log((liqs.liq.max() if r.direction == 1 else liqs.liq.min()) / r.prix_entree) * 10000, 0.0) if r.direction == 1 else max(-np.log(liqs.liq.min() / r.prix_entree) * 10000, 0.0)
        mae = max(-r.direction * np.log((liqs.liq.min() if r.direction == 1 else liqs.liq.max()) / r.prix_entree) * 10000, 0.0) if r.direction == 1 else max(np.log(liqs.liq.max() / r.prix_entree) * 10000, 0.0)
        interruption = premier_trou
        if pd.notna(dernier_tick) and dernier_tick < r.fin:
            interruption = min(interruption, dernier_tick) if pd.notna(interruption) else dernier_tick
        if r.statut_completude == 'INCOMPLET' and pd.notna(interruption) and (ts_mfe > interruption or ts_mae > interruption):
            ordre = 'CENSORED'
        elif ts_mfe < ts_mae:
            ordre = 'MFE_BEFORE_MAE'
        elif ts_mae < ts_mfe:
            ordre = 'MAE_BEFORE_MFE'
        else:
            ordre = 'MFE_MAE_SAME_TIMESTAMP'
        seq_rows.append({'event_id': r.event_id, 'grappe_id': r.grappe_id,
                         'p_M1': float(r.p_M1), 'direction': int(r.direction),
                         'mfe_bp': float(mfe), 'mae_bp': float(mae),
                         'timestamp_mfe': str(ts_mfe), 'timestamp_mae': str(ts_mae),
                         'delai_mfe_s': float((ts_mfe - r.t_entree).total_seconds()),
                         'delai_mae_s': float((ts_mae - r.t_entree).total_seconds()),
                         'delai_entre_extremes_s': float((ts_mae - ts_mfe).total_seconds()),
                         'ordre': ordre, 'statut_completude': r.statut_completude})
    S = pd.DataFrame(seq_rows)
    # ---- quartiles de confiance (p_M1 seul, departage event_id)
    S = S.sort_values(['p_M1', 'event_id']).reset_index(drop=True)
    tailles = [111, 111, 111, 110]
    qlabels, seuils_q, debut = [], {}, 0
    for i, t in enumerate(tailles):
        bloc = S.iloc[debut:debut + t]
        qlabels += [f'Q{i + 1}'] * len(bloc)
        seuils_q[f'Q{i + 1}'] = {'n': int(len(bloc)), 'p_min': float(bloc.p_M1.min()),
                                 'p_max': float(bloc.p_M1.max())}
        debut += t
    S['quartile'] = qlabels
    S = S.sort_values('event_id').reset_index(drop=True)
    S.to_csv(R14 / 'PHASE14_EVENT_PATH_SEQUENCE.csv', index=False)
    seqmap = S.set_index('event_id')

    # ---- ATR a t_decision
    A = atr_series()
    E['ATR14_H1'] = [float(A.atr[A.cloture <= t].iloc[-1]) if (A.cloture <= t).any() else np.nan
                     for t in E.t_decision_ts]

    # ---- barrieres
    grid_rows, ev_rows = [], []
    comp_fixe = {}
    for norm in ('A_R_EVENT', 'B_ATR14_H1'):
        for cid, tpm, slm in GRID:
            for scen, s in SCEN.items():
                res, res_gr, statuts = [], {}, {}
                for r in E.itertuples():
                    eid = r.event_id
                    info = path[eid]
                    recs = info['recs']
                    base = {'event_id': eid, 'grappe_id': r.grappe_id,
                            'normalisation': norm, 'configuration': cid,
                            'tp_mult': tpm, 'sl_mult': slm, 'scenario': scen,
                            'etiquette': LABELS[scen]}
                    echelle = r.MFE_A_TREINT_BP if norm == 'A_R_EVENT' else r.ATR14_H1
                    if not np.isfinite(echelle) or echelle <= 0:
                        base.update(statut='UNAVAILABLE')
                        ev_rows.append(base)
                        statuts['UNAVAILABLE'] = statuts.get('UNAVAILABLE', 0) + 1
                        continue
                    if norm == 'A_R_EVENT':
                        niv_tp = r.prix_entree * np.exp(r.direction * tpm * echelle / 10000)
                        niv_sl = r.prix_entree * np.exp(-r.direction * slm * echelle / 10000)
                    else:
                        niv_tp = r.prix_entree + r.direction * tpm * echelle
                        niv_sl = r.prix_entree - r.direction * slm * echelle
                    base.update(niveau_tp=float(niv_tp), niveau_sl=float(niv_sl),
                                echelle=float(echelle))
                    # premier franchissement dans la sequence d'extremes
                    hit = None
                    for t in recs:
                        fav = r.direction * np.log(t.liq / r.prix_entree) * 10000 if norm == 'A_R_EVENT' else r.direction * (t.liq - r.prix_entree)
                        seuil_tp = tpm * echelle if norm == 'A_R_EVENT' else tpm * echelle
                        seuil_sl = -slm * echelle
                        fav_val = np.log(t.liq / r.prix_entree) * 10000 * r.direction if norm == 'A_R_EVENT' else r.direction * (t.liq - r.prix_entree)
                        if fav_val >= seuil_tp:
                            hit = ('TP_FIRST', t)
                            break
                        if fav_val <= seuil_sl:
                            hit = ('SL_FIRST', t)
                            break
                    interruption = info['premier_trou']
                    if pd.notna(info['dernier_tick']) and info['dernier_tick'] < r.fin:
                        interruption = min(interruption, info['dernier_tick']) if pd.notna(interruption) else info['dernier_tick']
                    if hit is not None and r.statut_completude == 'INCOMPLET' and pd.notna(interruption) and not hit[1].ts < interruption:
                        hit = None
                        force_censure = True
                    else:
                        force_censure = False
                    if hit is not None:
                        statut, t = hit
                        prix_sortie = float(t.liq)
                        ts_sortie = t.ts
                        gap = ts_sortie in info['trous_fin']
                    elif r.statut_completude == 'COMPLET' and not force_censure:
                        statut, prix_sortie, ts_sortie, gap = 'VERTICAL_FIRST', float(r.prix_sortie), r.t_sortie_13b, False
                    else:
                        statut, prix_sortie, ts_sortie, gap = 'CENSORED', np.nan, pd.NaT, False
                    statuts[statut] = statuts.get(statut, 0) + 1
                    base.update(statut=statut, timestamp_sortie=str(ts_sortie),
                                prix_sortie=prix_sortie,
                                gap_avant_franchissement=bool(gap))
                    if statut in ('TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'):
                        if r.direction == 1:
                            pe, ps = r.prix_entree * (1 + s / 10000), prix_sortie * (1 - s / 10000)
                        else:
                            pe, ps = r.prix_entree * (1 - s / 10000), prix_sortie * (1 + s / 10000)
                        val = float(r.direction * np.log(ps / pe) * 10000)
                        base.update(resultat_bp=val,
                                    duree_detention_min=float((ts_sortie - r.t_entree).total_seconds() / 60),
                                    mfe_bp=float(seqmap.loc[eid, 'mfe_bp']),
                                    mae_bp=float(seqmap.loc[eid, 'mae_bp']))
                        res.append((eid, r.grappe_id, val))
                    ev_rows.append(base)
                arr = np.array([v for _, _, v in res], float)
                gr = {}
                for eid, g, v in res:
                    gr.setdefault(g, []).append(v)
                grm = np.array([np.mean(v) for v in gr.values()], float)
                st_ev, st_gr = stats(arr), stats(grm)
                # comparaison sortie fixe 13-B, meme sous-ensemble comparable
                ids = [eid for eid, _, _ in res]
                fixe = E.set_index('event_id').loc[ids, f'resultat_{scen}_bp'] if False else None
                grid_rows.append({'normalisation': norm, 'configuration': cid,
                                  'tp_mult': tpm, 'sl_mult': slm, 'scenario': scen,
                                  'etiquette': LABELS[scen],
                                  'n_TP_FIRST': statuts.get('TP_FIRST', 0),
                                  'n_SL_FIRST': statuts.get('SL_FIRST', 0),
                                  'n_VERTICAL_FIRST': statuts.get('VERTICAL_FIRST', 0),
                                  'n_CENSORED': statuts.get('CENSORED', 0),
                                  'n_UNAVAILABLE': statuts.get('UNAVAILABLE', 0),
                                  'n_ambigus': statuts.get('ORDER_UNRESOLVED', 0) + statuts.get('GAP_CROSSING_UNRESOLVED', 0),
                                  **{f'ev_{k}': v for k, v in st_ev.items()},
                                  **{f'gr_{k}': v for k, v in st_gr.items()}})
                comp_fixe[(norm, cid, scen)] = ids
    EV = pd.DataFrame(ev_rows)
    EV.to_csv(R14 / 'PHASE14_TRIPLE_BARRIER_EVENTS.csv', index=False)
    M = pd.DataFrame(grid_rows)
    # comparaison obligatoire: sortie fixe 13-B sur le meme sous-ensemble
    Eidx = E.set_index('event_id')
    complet_ids = set(E.loc[E.statut_completude == 'COMPLET', 'event_id'])
    comp_rows = []
    for _, m in M.iterrows():
        ids_all = comp_fixe[(m.normalisation, m.configuration, m.scenario)]
        ids = [e for e in ids_all if e in complet_ids]  # meme sous-ensemble comparable (protocole gele section 7)
        sous = EV[(EV.normalisation == m.normalisation) & (EV.configuration == m.configuration) &
                  (EV.scenario == m.scenario) & (EV.event_id.isin(ids))]
        comp = Eidx.loc[ids]
        comp_rows.append({'normalisation': m.normalisation, 'configuration': m.configuration,
                          'scenario': m.scenario, 'n_comparable': len(ids),
                          'barriere_moyenne_ev': float(sous.resultat_bp.mean()),
                          'barriere_mediane_ev': float(sous.resultat_bp.median()),
                          'fixe13B_moyenne_ev': float(comp[f'resultat_{m.scenario}_bp'].mean()),
                          'fixe13B_mediane_ev': float(comp[f'resultat_{m.scenario}_bp'].median()),
                          'barriere_moyenne_gr': float(sous.groupby('grappe_id').resultat_bp.mean().mean()),
                          'fixe13B_moyenne_gr': float(comp.groupby('grappe_id')[f'resultat_{m.scenario}_bp'].mean().mean()),
                          'classes_hors_comparaison_dont_incompletes': int(len(ids_all) - len(ids)),
                          'incompletes_13B_separees': 22})
    CW = pd.DataFrame(comp_rows)
    CW.to_csv(R14 / 'PHASE14_CLUSTER_WEIGHTING.csv', index=False)
    M.to_csv(R14 / 'PHASE14_BARRIER_MATRIX.csv', index=False)

    # ---- analyse par quartile
    conf = []
    for q in ('Q1', 'Q2', 'Q3', 'Q4'):
        bloc = S[S.quartile == q]
        conf.append({'section': 'SEQUENCE', 'quartile': q, 'n': int(len(bloc)),
                     'p_min': float(bloc.p_M1.min()), 'p_max': float(bloc.p_M1.max()),
                     'freq_MFE_BEFORE_MAE': float((bloc.ordre == 'MFE_BEFORE_MAE').mean()),
                     'freq_MAE_BEFORE_MFE': float((bloc.ordre == 'MAE_BEFORE_MFE').mean()),
                     'freq_indetermines': float(bloc.ordre.isin(['MFE_MAE_SAME_TIMESTAMP', 'ORDER_UNRESOLVED', 'CENSORED']).mean()),
                     'mfe_mediane': float(bloc.mfe_bp.median()), 'mae_mediane': float(bloc.mae_bp.median()),
                     'delai_mfe_median_s': float(bloc.delai_mfe_s.median()),
                     'delai_mae_median_s': float(bloc.delai_mae_s.median())})
    EVm = EV.merge(S[['event_id', 'quartile']], on='event_id', how='left')
    for (q, norm, cid, scen), g in EVm[EVm.statut.isin(['TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'])].groupby(['quartile', 'normalisation', 'configuration', 'scenario']):
        conf.append({'section': 'BARRIERES', 'quartile': q, 'normalisation': norm,
                     'configuration': cid, 'scenario': scen, 'n': int(len(g)),
                     'moyenne': float(g.resultat_bp.mean()), 'mediane': float(g.resultat_bp.median()),
                     'part_positifs': float((g.resultat_bp > 0).mean())})
    pd.DataFrame(conf).to_csv(R14 / 'PHASE14_CONFIDENCE_ANALYSIS.csv', index=False)

    ordres = S.ordre.value_counts().to_dict()
    nb_trous = int((P.kind == 'HOLE').sum())
    nb_gap = int(EV.gap_avant_franchissement.sum()) if 'gap_avant_franchissement' in EV else 0
    cov = pd.DataFrame([
        {'element': 'exposes_13B', 'effectif': 443, 'detail': 'cohorte figee'},
        {'element': 'ordres_determines', 'effectif': int(S.ordre.isin(['MFE_BEFORE_MAE', 'MAE_BEFORE_MFE']).sum()), 'detail': str({k: ordres.get(k, 0) for k in ('MFE_BEFORE_MAE', 'MAE_BEFORE_MFE')})},
        {'element': 'MFE_MAE_SAME_TIMESTAMP', 'effectif': int(ordres.get('MFE_MAE_SAME_TIMESTAMP', 0)), 'detail': 'meme horodatage tick, indepartageable'},
        {'element': 'CENSORED_ordre', 'effectif': int(ordres.get('CENSORED', 0)), 'detail': 'incompletes sans extremes certains avant interruption'},
        {'element': 'trous_cotation_>5min', 'effectif': nb_trous, 'detail': 'tous evenements confondus'},
        {'element': 'franchissements_apres_trou', 'effectif': nb_gap, 'detail': 'prix du premier tick suivant le trou utilise'},
        {'element': 'ATR_UNAVAILABLE', 'effectif': int(EV[EV.statut == 'UNAVAILABLE'].event_id.nunique()) if 'statut' in EV else 0, 'detail': 'branche B uniquement'},
        {'element': 'incompletes_13B', 'effectif': 22, 'detail': 'presentees separement; barrieres classees seulement avant premiere interruption'},
        {'element': 'controle_entree_tick_13B', 'effectif': controle_entree['verifies'], 'detail': f"divergents: {controle_entree['divergents']}"},
    ])
    cov.to_csv(R14 / 'PHASE14_COVERAGE_AND_AMBIGUITIES.csv', index=False)

    verdict_anatomie = 'MFE_MAE_SEQUENCE_ANALYZED' if S.ordre.isin(['MFE_BEFORE_MAE', 'MAE_BEFORE_MFE', 'MFE_MAE_SAME_TIMESTAMP']).sum() > 0 else 'SEQUENCE_ANALYSIS_BLOCKED'
    verdict_barrieres = 'BARRIER_MATRIX_COMPLETED_EXPLORATORY_IS' if len(M) == 54 else 'BARRIER_MATRIX_BLOCKED'
    resultats = {'phase': '14-B', 'qualification': 'EXPLORATOIRE_IS - HYPOTHESES POSTERIEURES AUX RESULTATS DE PHASE 13-B',
                 'controle_entree_tick_13B': controle_entree,
                 'ordres': {k: int(v) for k, v in ordres.items()},
                 'quartiles_seuils_p_M1': seuils_q,
                 'sequence_globale': {'mfe_mediane': float(S.mfe_bp.median()),
                                      'mae_mediane': float(S.mae_bp.median()),
                                      'delai_mfe_median_s': float(S.delai_mfe_s.median()),
                                      'delai_mae_median_s': float(S.delai_mae_s.median())},
                 'matrice': M.to_dict('records'),
                 'verdict_anatomie': verdict_anatomie,
                 'verdict_barrieres': verdict_barrieres,
                 'rappel': 'aucune configuration selectionnee; commissions exclues; niveau 3 non autorise'}
    (R14 / 'PHASE14_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False, default=str))
    print(json.dumps({'verdict_anatomie': verdict_anatomie, 'verdict_barrieres': verdict_barrieres,
                      'ordres': ordres, 'controle_entree': controle_entree}, indent=1), flush=True)
    print('P14 analyse terminee', flush=True)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'analyse'
    if mode == 'lot':
        mode_lot()
    else:
        mode_analyse()
