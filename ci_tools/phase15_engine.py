#!/usr/bin/env python3
"""PHASE 15 - Engineering du point d'entree (exploratoire IS, seq339).
lot: declencheurs E1/E2 depuis les barres M1 committes, ticks d'entree et
extremes de liquidation par partition IS. analyse: matrice 3x3x3."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R11 = ROOT / 'reports/meta_alpha/phase11'
R13 = ROOT / 'reports/meta_alpha/phase13'
R14 = ROOT / 'reports/meta_alpha/phase14'
R15 = ROOT / 'reports/meta_alpha/phase15'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
SCEN = {'S0': 0.0, 'S1': 0.5, 'S2': 1.0}
LABELS = {'S0': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE',
          'S1': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_0_5_BP_PER_SIDE',
          'S2': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_1_0_BP_PER_SIDE'}
EXITS = {'X0': None, 'X1': (1.5, 1.0), 'X2': (1.5, 1.5)}

def evenements():
    E = pd.read_csv(R13 / 'PHASE13B_EVENT_EXECUTIONS.csv')
    E = E[E.decision_exposition == 'EXPOSITION'].copy()
    assert len(E) == 443
    P0 = pd.read_csv(R11 / 'PHASE11C_EVENT_PATHS.csv', usecols=['event_id', 'P0'])
    F = pd.read_csv(ROOT / 'reports/meta_alpha/phase12/PHASE12B_FEATURES.csv',
                    usecols=['event_id', 'fin_fenetre_observation'])
    E = E.merge(P0, on='event_id').merge(F, on='event_id')
    E['t_decision_ts'] = pd.to_datetime(E.t_decision)
    E['t_entree_E0'] = pd.to_datetime(E.timestamp_entree).dt.tz_localize(None)
    E['fin'] = pd.to_datetime(E.fin_fenetre_observation)
    E['t_sortie_13b'] = pd.to_datetime(E.timestamp_sortie, errors='coerce')
    if E.t_sortie_13b.dt.tz is not None:
        E.t_sortie_13b = E.t_sortie_13b.dt.tz_localize(None)
    return E

def charger_barres():
    bars = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz')))])
    bars['ts'] = pd.to_datetime(bars.ts)
    if bars.ts.dt.tz is not None:
        bars['ts'] = bars.ts.dt.tz_localize(None)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

def declencheurs(E, bars):
    B = bars.set_index('ts')
    out = {}
    for r in E.itertuples():
        cand = bars[(bars.ts >= r.t_decision_ts) & (bars.ts + pd.Timedelta(minutes=1) <= r.fin)]
        trig = {}
        hit = cand[r.direction * (cand.mc - r.P0) > 0]
        trig['E1'] = (hit.ts.iloc[0] + pd.Timedelta(minutes=1)) if len(hit) else pd.NaT
        c0bar = B.loc[r.t_decision_ts - pd.Timedelta(minutes=1), 'mc'] if (r.t_decision_ts - pd.Timedelta(minutes=1)) in B.index else np.nan
        ref, run, prev_ts, t2 = c0bar, 0, r.t_decision_ts - pd.Timedelta(minutes=1), pd.NaT
        for c in cand.itertuples():
            adj = (c.ts - prev_ts) == pd.Timedelta(minutes=1)
            prog = adj and pd.notna(ref) and ((r.direction == 1 and c.mc > ref) or (r.direction == -1 and c.mc < ref))
            run = run + 1 if prog else 0
            if run >= 2:
                t2 = c.ts + pd.Timedelta(minutes=1)
                break
            ref, prev_ts = c.mc, c.ts
        trig['E2'] = t2
        out[r.event_id] = trig
    return out

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
    d = pathlib.Path('/tmp/kbatch'); shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(d)
    return d

def mode_lot():
    import duckdb
    batch = os.environ['P15_BATCH']
    E = evenements(); trig = declencheurs(E, charger_barres())
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute('SET threads=2')
    rows = []
    for p in parts:
        local = localdir / p['name']
        if not local.exists(): continue
        pmin = pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None)
        pmax = pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None)
        for r in E.itertuples():
            for pol in ('E1', 'E2'):
                t0 = trig[r.event_id][pol]
                if pd.isna(t0) or not (t0 < pmax and r.fin > pmin): continue
                liq = 'bid' if r.direction == 1 else 'ask'
                q = f"""WITH s AS (SELECT timestamp_utc AS ts, bid, ask, {liq} AS liq FROM read_parquet('{local}')
                        WHERE timestamp_utc > '{t0}' AND timestamp_utc <= '{r.fin}' ORDER BY timestamp_utc),
                        w AS (SELECT *, max(liq) OVER (ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmax,
                                min(liq) OVER (ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmin,
                                lag(ts) OVER (ORDER BY ts) AS pts FROM s)
                        SELECT ts, bid, ask, liq, pts, pmax, pmin FROM w
                        WHERE pmax IS NULL OR liq > pmax OR liq < pmin OR (pts IS NOT NULL AND epoch(ts) - epoch(pts) > 300)"""
                w = con.execute(q).df()
                if not len(w): continue
                w['ts'] = pd.to_datetime(w.ts).dt.tz_localize(None)
                for t in w[w.pts.notna() & ((w.ts - pd.to_datetime(w.pts, format='mixed').dt.tz_localize(None)).dt.total_seconds() > 300)].itertuples():
                    rows.append({'event_id': r.event_id, 'politique': pol, 'kind': 'HOLE', 'ts': str(pd.Timestamp(t.pts).tz_localize(None)), 'ts2': str(t.ts), 'liq': np.nan, 'bid': np.nan, 'ask': np.nan})
                for t in w[(w.pmax.isna()) | (w.liq > w.pmax) | (w.liq < w.pmin)].itertuples():
                    rows.append({'event_id': r.event_id, 'politique': pol, 'kind': 'EXTREME', 'ts': str(t.ts), 'ts2': '', 'liq': float(t.liq), 'bid': float(t.bid), 'ask': float(t.ask)})
                rows.append({'event_id': r.event_id, 'politique': pol, 'kind': 'BOUND', 'ts': str(w.ts.iloc[0]), 'ts2': str(w.ts.iloc[-1]), 'liq': float(len(w)), 'bid': np.nan, 'ask': np.nan})
        print('P15 part', p['name'], flush=True)
    R15.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=['event_id', 'politique', 'kind', 'ts', 'ts2', 'liq', 'bid', 'ask']).to_csv(R15 / f'P15_PATH_{batch}.csv', index=False)
    print('P15 lot termine', batch, len(rows), flush=True)

def stats(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if not len(x): return {}
    q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    return {'n': int(len(x)), 'moyenne': float(x.mean()), 'mediane': float(q[3]), 'p1': float(q[0]),
            'p5': float(q[1]), 'p25': float(q[2]), 'p75': float(q[4]), 'p95': float(q[5]), 'p99': float(q[6]),
            'part_positifs': float((x > 0).mean()), 'perte_maximale': float(x.min()), 'gain_maximal': float(x.max())}

def remplir(direction, prix_entree, prix_sortie, s):
    if direction == 1: pe, ps = prix_entree * (1 + s / 10000), prix_sortie * (1 - s / 10000)
    else: pe, ps = prix_entree * (1 - s / 10000), prix_sortie * (1 + s / 10000)
    return float(direction * np.log(ps / pe) * 10000)

def mode_analyse():
    E = evenements().reset_index(drop=True)
    bars = charger_barres(); B = bars.set_index('ts')
    trig = declencheurs(E, bars)
    S14 = pd.read_csv(R14 / 'PHASE14_EVENT_PATH_SEQUENCE.csv').set_index('event_id')
    T14 = pd.read_csv(R14 / 'PHASE14_TRIPLE_BARRIER_EVENTS.csv')
    atr = (T14[T14.normalisation == 'B_ATR14_H1'].drop_duplicates('event_id')
           .set_index('event_id').echelle.to_dict())
    # chemins Phase 14 (interruptions) et chemins Phase 15 (E1/E2)
    P14 = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R14 / 'P14_PATH_*.csv')))])
    inter14 = {}
    for eid, d in P14.groupby('event_id'):
        trous = d[d.kind == 'HOLE']; bounds = d[d.kind == 'BOUND']
        inter14[eid] = {'premier_trou': pd.to_datetime(trous.ts, format='mixed').min() if len(trous) else pd.NaT,
                        'dernier_tick': pd.to_datetime(bounds.ts2, format='mixed').max() if len(bounds) else pd.NaT,
                        'trous_fin': set(pd.to_datetime(trous.ts2, format='mixed')) if len(trous) else set()}
    frames = []
    for f in sorted(glob.glob(str(R15 / 'P15_PATH_*.csv'))):
        try: tf = pd.read_csv(f)
        except pd.errors.EmptyDataError: continue
        if len(tf): frames.append(tf)
    P = pd.concat(frames); P['ts'] = pd.to_datetime(P.ts, format='mixed')
    chemins = {}
    for (eid, pol), d in P.groupby(['event_id', 'politique']):
        ext = d[d.kind == 'EXTREME'].drop_duplicates(['ts', 'liq']).sort_values('ts')
        recs, cmax, cmin = [], -np.inf, np.inf
        for t in ext.itertuples():
            if t.liq > cmax or t.liq < cmin:
                recs.append(t); cmax = max(cmax, t.liq); cmin = min(cmin, t.liq)
        chemins[(eid, pol)] = recs
    # ---- entrees par politique
    ent = {}
    for r in E.itertuples():
        ent[(r.event_id, 'E0')] = {'statut': 'EXECUTE', 'trig': r.t_decision_ts, 'ts': r.t_entree_E0, 'prix': float(r.prix_entree)}
        for pol in ('E1', 'E2'):
            t0 = trig[r.event_id][pol]
            if pd.isna(t0):
                ent[(r.event_id, pol)] = {'statut': 'NO_ENTRY_TRIGGER', 'trig': t0, 'ts': pd.NaT, 'prix': np.nan}
                continue
            recs = chemins.get((r.event_id, pol), [])
            if not recs or not (t0 < recs[0].ts < t0 + pd.Timedelta(seconds=60)) or recs[0].ts >= r.fin:
                ent[(r.event_id, pol)] = {'statut': 'NON_EXECUTION', 'trig': t0, 'ts': pd.NaT, 'prix': np.nan}
                continue
            t = recs[0]
            ent[(r.event_id, pol)] = {'statut': 'EXECUTE', 'trig': t0, 'ts': t.ts,
                                      'prix': float(t.ask if r.direction == 1 else t.bid)}
    # ---- lignes de chemins (comparaison evenement par evenement)
    prows = []
    for r in E.itertuples():
        e0 = ent[(r.event_id, 'E0')]
        for pol in ('E0', 'E1', 'E2'):
            e = ent[(r.event_id, pol)]
            recs = chemins.get((r.event_id, pol), []) if pol != 'E0' else []
            mfe = mae = np.nan
            if pol == 'E0':
                mfe, mae = float(S14.loc[r.event_id, 'mfe_bp']), float(S14.loc[r.event_id, 'mae_bp'])
            elif e['statut'] == 'EXECUTE' and recs:
                liqs = [t.liq for t in recs if t.ts >= e['ts']]
                if liqs:
                    fav = r.direction * np.log(np.array(liqs) / e['prix']) * 10000
                    mfe, mae = float(max(fav.max(), 0.0)), float(max(-fav.min(), 0.0))
            prows.append({'event_id': r.event_id, 'grappe_id': r.grappe_id, 'direction': int(r.direction),
                          'p_M1': float(r.p_M1), 'quartile': str(S14.loc[r.event_id, 'quartile']),
                          'politique': pol, 'statut_entree': e['statut'],
                          'timestamp_declenchement': str(e['trig']), 'timestamp_entree': str(e['ts']),
                          'prix_entree': e['prix'],
                          'delai_apres_t_decision_min': float((e['ts'] - r.t_decision_ts).total_seconds() / 60) if e['statut'] == 'EXECUTE' else np.nan,
                          'retard_vs_E0_min': float((e['ts'] - e0['ts']).total_seconds() / 60) if e['statut'] == 'EXECUTE' else np.nan,
                          'prix_economise_vs_E0_bp': float(r.direction * np.log(e0['prix'] / e['prix']) * 10000) if e['statut'] == 'EXECUTE' else np.nan,
                          'mfe_apres_entree_bp': mfe, 'mae_apres_entree_bp': mae,
                          'statut_completude_13B': r.statut_completude})
    EP = pd.DataFrame(prows)
    EP.to_csv(R15 / 'PHASE15_ENTRY_PATHS.csv', index=False)
    # ---- matrice entrees x sorties x scenarios
    Eidx = E.set_index('event_id')
    t14idx = {(x.event_id, x.configuration, x.scenario): x for x in T14.itertuples()}
    ev_rows, grid_rows = [], []
    for pol in ('E0', 'E1', 'E2'):
        for exit_, mult in EXITS.items():
            for scen, s in SCEN.items():
                res, statuts = {}, {}
                for r in E.itertuples():
                    eid = r.event_id; e = ent[(eid, pol)]
                    base = {'event_id': eid, 'grappe_id': r.grappe_id, 'politique': pol, 'sortie': exit_,
                            'scenario': scen, 'etiquette': LABELS[scen], 'quartile': str(S14.loc[eid, 'quartile'])}
                    if e['statut'] != 'EXECUTE':
                        base['statut'] = e['statut']; statuts[e['statut']] = statuts.get(e['statut'], 0) + 1
                        ev_rows.append(base); continue
                    if pol == 'E0' and exit_ in ('X1', 'X2'):
                        t = t14idx.get((eid, 'B08' if exit_ == 'X1' else 'B09', scen))
                        if t is None or t.statut not in ('TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'):
                            st = 'CENSORED' if t is not None else 'UNAVAILABLE'
                            base['statut'] = st; statuts[st] = statuts.get(st, 0) + 1; ev_rows.append(base); continue
                        base.update(statut=t.statut, timestamp_sortie=t.timestamp_sortie, prix_sortie=t.prix_sortie,
                                    resultat_bp=float(t.resultat_bp), duree_detention_min=float(t.duree_detention_min),
                                    mfe_bp=float(S14.loc[eid, 'mfe_bp']), mae_bp=float(S14.loc[eid, 'mae_bp']))
                        statuts[t.statut] = statuts.get(t.statut, 0) + 1; res[eid] = float(t.resultat_bp)
                        ev_rows.append(base); continue
                    a = atr.get(eid, np.nan)
                    hit = None
                    if exit_ in ('X1', 'X2') and pol != 'E0':
                        if not np.isfinite(a):
                            base['statut'] = 'UNAVAILABLE'; statuts['UNAVAILABLE'] = statuts.get('UNAVAILABLE', 0) + 1
                            ev_rows.append(base); continue
                        niv_tp = e['prix'] + r.direction * mult[0] * a
                        niv_sl = e['prix'] - r.direction * mult[1] * a
                        for t in chemins.get((eid, pol), []):
                            if t.ts < e['ts']: continue
                            fav = r.direction * (t.liq - e['prix'])
                            if fav >= mult[0] * a: hit = ('TP_FIRST', t); break
                            if fav <= -mult[1] * a: hit = ('SL_FIRST', t); break
                        inter = inter14[eid]['premier_trou']
                        dt_ = inter14[eid]['dernier_tick']
                        interruptions = [x for x in (inter if pd.notna(inter) and inter >= e['ts'] else None,
                                                     dt_ if pd.notna(dt_) and dt_ < r.fin else None) if x is not None]
                        interruption = min(interruptions) if interruptions else pd.NaT
                        if hit is not None and r.statut_completude == 'INCOMPLET' and pd.notna(interruption) and not hit[1].ts < interruption:
                            hit = None
                    recs_p = chemins.get((eid, pol), [])
                    liqs = [t.liq for t in recs_p if t.ts >= e['ts']] if pol != 'E0' else []
                    if pol == 'E0':
                        mfe_p, mae_p = float(S14.loc[eid, 'mfe_bp']), float(S14.loc[eid, 'mae_bp'])
                    elif liqs:
                        fav_arr = r.direction * np.log(np.array(liqs) / e['prix']) * 10000
                        mfe_p, mae_p = float(max(fav_arr.max(), 0.0)), float(max(-fav_arr.min(), 0.0))
                    else: mfe_p = mae_p = np.nan
                    if hit is not None:
                        statut, prix_s, ts_s = hit[0], float(hit[1].liq), hit[1].ts
                    elif exit_ == 'X0' or exit_ in ('X1', 'X2'):
                        if r.statut_completude == 'COMPLET':
                            statut, prix_s, ts_s = 'VERTICAL_FIRST', float(r.prix_sortie), r.t_sortie_13b
                        else:
                            statut, prix_s, ts_s = 'CENSORED', np.nan, pd.NaT
                    base.update(statut=statut, timestamp_sortie=str(ts_s), prix_sortie=prix_s,
                                mfe_bp=mfe_p, mae_bp=mae_p,
                                gap_avant_franchissement=bool(hit is not None and hit[1].ts in inter14[eid]['trous_fin']))
                    statuts[statut] = statuts.get(statut, 0) + 1
                    if statut in ('TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'):
                        val = remplir(r.direction, e['prix'], prix_s, s)
                        base.update(resultat_bp=val, duree_detention_min=float((ts_s - e['ts']).total_seconds() / 60))
                        res[eid] = val
                    ev_rows.append(base)
                arr = np.array(list(res.values()), float)
                grm = EP.groupby('event_id').first()
                gr_vals = pd.Series(res).groupby(Eidx.loc[list(res.keys()), 'grappe_id'].values).mean() if res else pd.Series(dtype=float)
                st_ev, st_gr = stats(arr), stats(gr_vals.values)
                coh = np.array([res.get(eid, 0.0) for eid in E.event_id], float)
                grid_rows.append({'politique': pol, 'sortie': exit_, 'scenario': scen, 'etiquette': LABELS[scen],
                                  'opportunites': 443, 'declenches': int(sum(1 for (eid, p), e in ent.items() if p == pol and e['statut'] != 'NO_ENTRY_TRIGGER')),
                                  'executes': int(len(res) + statuts.get('CENSORED', 0) + statuts.get('UNAVAILABLE', 0)),
                                  'taux_capture': float(len(res) / 443), 'non_decharges_NO_ENTRY_TRIGGER': statuts.get('NO_ENTRY_TRIGGER', 0),
                                  'NON_EXECUTION': statuts.get('NON_EXECUTION', 0),
                                  'n_TP_FIRST': statuts.get('TP_FIRST', 0), 'n_SL_FIRST': statuts.get('SL_FIRST', 0),
                                  'n_VERTICAL_FIRST': statuts.get('VERTICAL_FIRST', 0), 'n_CENSORED': statuts.get('CENSORED', 0),
                                  **{f'ev_{k}': v for k, v in st_ev.items()}, **{f'gr_{k}': v for k, v in st_gr.items()},
                                  'cohorte443_moyenne': float(coh.mean()), 'cohorte443_mediane': float(np.median(coh)),
                                  'mfe_mediane': float(np.nanmedian([x.get('mfe_bp', np.nan) for x in ev_rows if x.get('politique') == pol and x.get('sortie') == exit_ and x.get('scenario') == scen])) if res else np.nan,
                                  'commission_theorique_equilibre_bp': float(st_ev.get('moyenne', np.nan))})
    EV = pd.DataFrame(ev_rows)
    EV.to_csv(R15 / 'PHASE15_ENTRY_EXECUTIONS.csv', index=False)
    M = pd.DataFrame(grid_rows)
    M.to_csv(R15 / 'PHASE15_ENTRY_EXIT_MATRIX.csv', index=False)
    # pondération grappe dediee + confiance + couverture
    cw = []
    for _, m in M.iterrows():
        d = EV[(EV.politique == m.politique) & (EV.sortie == m.sortie) & (EV.scenario == m.scenario) & EV.resultat_bp.notna()]
        g = d.groupby('grappe_id').resultat_bp.mean()
        cw.append({'politique': m.politique, 'sortie': m.sortie, 'scenario': m.scenario, 'n_evenements': int(len(d)),
                   'n_grappes': int(d.grappe_id.nunique()), 'moyenne_evenement': float(d.resultat_bp.mean()),
                   'moyenne_grappe': float(g.mean()), 'mediane_evenement': float(d.resultat_bp.median()),
                   'mediane_moyennes_par_grappe': float(g.median()), 'cohorte443_moyenne': m.cohorte443_moyenne})
    pd.DataFrame(cw).to_csv(R15 / 'PHASE15_CLUSTER_WEIGHTING.csv', index=False)
    conf = []
    for (q, pol, exit_, scen), d in EV.groupby(['quartile', 'politique', 'sortie', 'scenario']):
        res = d[d.resultat_bp.notna()]
        conf.append({'quartile': q, 'politique': pol, 'sortie': exit_, 'scenario': scen,
                     'n_exposes_quartile': int(len(d) / 1), 'n_resultats': int(len(res)),
                     'moyenne_executes': float(res.resultat_bp.mean()) if len(res) else np.nan,
                     'mediane_executes': float(res.resultat_bp.median()) if len(res) else np.nan,
                     'moyenne_cohorte_quartile (non declenches a 0)': float(d.resultat_bp.fillna(0).mean()),
                     'statut': 'DESCRIPTIF UNIQUEMENT - jamais filtre'})
    pd.DataFrame(conf).to_csv(R15 / 'PHASE15_CONFIDENCE_ANALYSIS.csv', index=False)
    cov_rows = []
    for pol in ('E0', 'E1', 'E2'):
        d = EP[EP.politique == pol]
        cov_rows.append({'politique': pol, 'opportunites': 443,
                         'declenches': int((d.statut_entree != 'NO_ENTRY_TRIGGER').sum()),
                         'NO_ENTRY_TRIGGER': int((d.statut_entree == 'NO_ENTRY_TRIGGER').sum()),
                         'NON_EXECUTION': int((d.statut_entree == 'NON_EXECUTION').sum()),
                         'EXECUTE': int((d.statut_entree == 'EXECUTE').sum()),
                         'delai_median_min': float(d.delai_apres_t_decision_min.median()),
                         'prix_economise_median_bp': float(d.prix_economise_vs_E0_bp.median())})
    cov_rows.append({'politique': 'TOUTES', 'opportunites': 443, 'note': '22 trajectoires incompletes 13-B conservees dans les denominateurs; barrieres classees seulement avant premiere interruption (convention Phase 14/14.1); trous documentes dans PHASE14_COVERAGE et P14_PATH; ordre intra-gap jamais suppose'})
    pd.DataFrame(cov_rows).to_csv(R15 / 'PHASE15_COVERAGE_AND_GAPS.csv', index=False)
    # ---- reconciliations de reference
    def cellule(pol, exit_, scen):
        m = M[(M.politique == pol) & (M.sortie == exit_) & (M.scenario == scen)]
        return m.iloc[0] if len(m) else None
    rec = {}
    c = cellule('E0', 'X0', 'S0')
    rec['E0_X0_S0'] = {'moyenne': float(c.ev_moyenne), 'mediane': float(c.ev_mediane),
                       'attendu_13B': {'moyenne': 0.11130282596408449, 'mediane': -0.8917991641155775},
                       'conforme': bool(abs(c.ev_moyenne - 0.11130282596408449) < 1e-9 and abs(c.ev_mediane + 0.8917991641155775) < 1e-9)}
    for exit_, cfg in (('X1', 'B08'), ('X2', 'B09')):
        c = cellule('E0', exit_, 'S0')
        m14 = pd.read_csv(R14 / 'PHASE14_BARRIER_MATRIX.csv')
        ref = m14[(m14.normalisation == 'B_ATR14_H1') & (m14.configuration == cfg) & (m14.scenario == 'S0')].iloc[0]
        rec[f'E0_{exit_}_S0'] = {'moyenne': float(c.ev_moyenne), 'attendu_phase14': float(ref.ev_moyenne),
                                 'conforme': bool(abs(c.ev_moyenne - ref.ev_moyenne) < 1e-9)}
    # ---- anatomie: fenetres relatives (clotures M1 de liquidation, completes)
    fenetres = [(0, 1), (1, 5), (5, 15), (15, 30), (30, 60), (60, 120), (120, 240), (240, 480)]
    anat = []
    comp = E[E.statut_completude == 'COMPLET']
    for a, b in fenetres:
        deps, spreads = [], []
        for r in comp.itertuples():
            w = bars[(bars.ts >= r.t_decision_ts + pd.Timedelta(minutes=a)) & (bars.ts < r.t_decision_ts + pd.Timedelta(minutes=b))]
            if len(w) < 2: continue
            liq_c = w.bc if r.direction == 1 else w.ac
            deps.append(r.direction * np.log(liq_c.iloc[-1] / liq_c.iloc[0]) * 10000)
            spreads.append(w.sp.median())
        anat.append({'fenetre_min': f'{a}-{b}', 'n': len(deps),
                     'deplacement_directionnel_median_bp': float(np.median(deps)) if deps else np.nan,
                     'part_fenetres_positives': float((np.array(deps) > 0).mean()) if deps else np.nan,
                     'spread_median_bp': float(np.median(spreads)) if spreads else np.nan})
    seq = S14.loc[comp.event_id]
    # premier extreme tick et stabilisation (artefacts Phase 14, prix de liquidation)
    ext14 = P14[P14.kind == 'EXTREME'].copy()
    ext14['ts'] = pd.to_datetime(ext14.ts, format='mixed')
    types_premier, delais_stab = {}, {}
    Emap = E.set_index('event_id')
    for eid, d in ext14.groupby('event_id'):
        r = Emap.loc[eid]
        d = d.drop_duplicates(['ts', 'liq']).sort_values('ts')
        recs, cmax, cmin = [], -np.inf, np.inf
        for t in d.itertuples():
            if t.liq > cmax or t.liq < cmin:
                recs.append(t); cmax = max(cmax, t.liq); cmin = min(cmin, t.liq)
        if len(recs) < 2: continue
        t1 = recs[1]
        favorable = (t1.liq >= recs[0].liq) if r.direction == 1 else (t1.liq <= recs[0].liq)
        types_premier[eid] = 'FAVORABLE' if favorable else 'ADVERSE'
        for t in recs[1:]:
            adv = (t.liq < recs[0].liq) if r.direction == 1 else (t.liq > recs[0].liq)
            if adv:
                delais_stab[eid] = (t.ts - r.t_entree_E0).total_seconds() / 60
                break
    comp_ids = set(comp.event_id)
    types_comp = [v for k, v in types_premier.items() if k in comp_ids]
    part_premier = max(pd.Series(types_comp).value_counts(normalize=True)) if types_comp else 0.0
    bornes = [(0, 1), (1, 5), (5, 15), (15, 30), (30, 60), (60, 120), (120, 240), (240, 480)]
    stab_comp = [v for k, v in delais_stab.items() if k in comp_ids]
    parts_fen = [float(np.mean([(a <= v < b) for v in stab_comp])) if stab_comp else 0.0 for a, b in bornes]
    anat_extra = {'premier_extreme_type_dominant_part': float(part_premier),
                  'premier_extreme_types': pd.Series(types_comp).value_counts().to_dict(),
                  'stabilisation_part_max_par_fenetre': float(max(parts_fen)) if parts_fen else 0.0,
                  'stabilisation_parts_par_fenetre': {f'{a}-{b}': float(x) for (a, b), x in zip(bornes, parts_fen)}}
    anat_res_extra = anat_extra
    anat_res = {'fenetres': anat, **anat_extra,
                'ordre_extremes_complets': {k: int(v) for k, v in seq.ordre.value_counts().items()},
                'delai_mfe_median_s': float(seq.delai_mfe_s.median()), 'delai_mae_median_s': float(seq.delai_mae_s.median())}
    # ---- verdicts selon criteres geles (protocole section 6)
    bloque = not all(v['conforme'] for v in rec.values())
    def cohorte(pol, scen):
        return float(cellule(pol, 'X0', scen).cohorte443_moyenne)
    def med_exec(pol, scen):
        return float(cellule(pol, 'X0', scen).ev_mediane)
    if bloque:
        verdict_eco = 'BLOCKED'
    else:
        adv = False; notfound = True
        for pol in ('E1', 'E2'):
            cap = float(cellule(pol, 'X0', 'S0').taux_capture)
            if all(cohorte(pol, s) > cohorte('E0', s) for s in SCEN) and med_exec(pol, 'S0') >= med_exec('E0', 'S0') and cap >= 0.30:
                adv = True
            if not all(cohorte(pol, s) <= cohorte('E0', s) for s in SCEN):
                notfound = False
        verdict_eco = 'EXPLORATORY_ENTRY_ADVANTAGE_FOUND' if adv else ('EXPLORATORY_ENTRY_ADVANTAGE_NOT_FOUND' if notfound else 'ECONOMICALLY_INCONCLUSIVE')
    if bloque:
        verdict_anat = 'ENTRY_ANALYSIS_BLOCKED'
    elif float(part_premier) >= 0.60 or float(max(parts_fen)) >= 0.50:
        verdict_anat = 'ENTRY_STRUCTURE_IDENTIFIED'
    else:
        verdict_anat = 'ENTRY_STRUCTURE_NOT_IDENTIFIED'
    resultats = {'phase': '15', 'qualification': 'EXPLORATOIRE IS - hypotheses posterieures aux Phases 13-B/14',
                 'reconciliations': rec, 'anatomie': anat_res, 'matrice': M.to_dict('records'),
                 'verdict_anatomie': verdict_anat, 'verdict_economie': verdict_eco,
                 'rappel': 'aucune combinaison selectionnee; commissions exclues; cohorte 443 et executes presentes ensemble'}
    (R15 / 'PHASE15_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False, default=str))
    print(json.dumps({'reconciliations': rec, 'verdict_anatomie': verdict_anat, 'verdict_economie': verdict_eco}, indent=1), flush=True)
    print('P15 analyse terminee', flush=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
