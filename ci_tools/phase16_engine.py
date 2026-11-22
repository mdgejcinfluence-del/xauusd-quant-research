#!/usr/bin/env python3
"""PHASE 16 - Entree passive E3 (proxy de franchissement, seq342).
lot: ticks de la fenetre (t_decision, t_decision+60s] par partition IS.
analyse: reference, P_limit, franchissement strict, sorties X0/X1/X2."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R13 = ROOT / 'reports/meta_alpha/phase13'
R14 = ROOT / 'reports/meta_alpha/phase14'
R16 = ROOT / 'reports/meta_alpha/phase16'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
SCEN = {'S0': 0.0, 'S1': 0.5, 'S2': 1.0}
LABELS = {'S0': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE',
          'S1': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_0_5_BP_EXIT_SLIPPAGE',
          'S2': 'NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_1_0_BP_EXIT_SLIPPAGE'}
EXITS = {'X0': None, 'X1': (1.5, 1.0), 'X2': (1.5, 1.5)}

def evenements():
    E = pd.read_csv(R13 / 'PHASE13B_EVENT_EXECUTIONS.csv')
    E = E[E.decision_exposition == 'EXPOSITION'].copy()
    assert len(E) == 443
    F = pd.read_csv(ROOT / 'reports/meta_alpha/phase12/PHASE12B_FEATURES.csv',
                    usecols=['event_id', 'fin_fenetre_observation'])
    E = E.merge(F, on='event_id')
    E['t_decision_ts'] = pd.to_datetime(E.t_decision)
    E['t_entree_E0'] = pd.to_datetime(E.timestamp_entree).dt.tz_localize(None)
    E['fin'] = pd.to_datetime(E.fin_fenetre_observation)
    E['t_sortie_13b'] = pd.to_datetime(E.timestamp_sortie, errors='coerce')
    if E.t_sortie_13b.dt.tz is not None:
        E.t_sortie_13b = E.t_sortie_13b.dt.tz_localize(None)
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
    d = pathlib.Path('/tmp/kbatch'); shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(d)
    return d

def mode_lot():
    import duckdb
    batch = os.environ['P16_BATCH']
    E = evenements()
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
        cand = E[(E.t_decision_ts < pmax) & (E.t_decision_ts + pd.Timedelta(seconds=60) > pmin)]
        for r in cand.itertuples():
            q = f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet('{local}')
                    WHERE timestamp_utc > '{r.t_decision_ts}' AND
                          timestamp_utc <= '{r.t_decision_ts + pd.Timedelta(seconds=60)}'
                    ORDER BY timestamp_utc"""
            w = con.execute(q).df()
            for t in w.itertuples():
                rows.append({'event_id': r.event_id, 'ts': str(pd.Timestamp(t.ts).tz_localize(None)),
                             'bid': float(t.bid), 'ask': float(t.ask)})
        print('P16 part', p['name'], flush=True)
    R16.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=['event_id', 'ts', 'bid', 'ask']).to_csv(R16 / f'P16_WIN_{batch}.csv', index=False)
    print('P16 lot termine', batch, len(rows), flush=True)

def stats(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if not len(x): return {}
    q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    return {'n': int(len(x)), 'moyenne': float(x.mean()), 'mediane': float(q[3]), 'p1': float(q[0]),
            'p5': float(q[1]), 'p25': float(q[2]), 'p75': float(q[4]), 'p95': float(q[5]), 'p99': float(q[6]),
            'part_positifs': float((x > 0).mean()), 'perte_maximale': float(x.min()), 'gain_maximal': float(x.max())}

def mode_analyse():
    E = evenements().reset_index(drop=True)
    Eidx = E.set_index('event_id')
    S14 = pd.read_csv(R14 / 'PHASE14_EVENT_PATH_SEQUENCE.csv').set_index('event_id')
    T14 = pd.read_csv(R14 / 'PHASE14_TRIPLE_BARRIER_EVENTS.csv')
    atr = (T14[T14.normalisation == 'B_ATR14_H1'].drop_duplicates('event_id')
           .set_index('event_id').echelle.to_dict())
    # fenetres tick 60 s
    W = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R16 / 'P16_WIN_*.csv')))])
    W['ts'] = pd.to_datetime(W.ts, format='mixed')
    W = W.drop_duplicates(['event_id', 'ts', 'bid', 'ask']).sort_values(['event_id', 'ts'])
    # extremes Phase 14 (franchissements de barrieres apres remplissage)
    P14 = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R14 / 'P14_PATH_*.csv')))])
    recs14, inter14 = {}, {}
    ext = P14[P14.kind == 'EXTREME'].copy(); ext['ts'] = pd.to_datetime(ext.ts, format='mixed')
    for eid, d in ext.groupby('event_id'):
        d = d.drop_duplicates(['ts', 'liq']).sort_values('ts')
        recs, cmax, cmin = [], -np.inf, np.inf
        for t in d.itertuples():
            if t.liq > cmax or t.liq < cmin:
                recs.append(t); cmax = max(cmax, t.liq); cmin = min(cmin, t.liq)
        recs14[eid] = recs
    for eid, d in P14.groupby('event_id'):
        trous = d[d.kind == 'HOLE']; bounds = d[d.kind == 'BOUND']
        inter14[eid] = {'premier_trou': pd.to_datetime(trous.ts, format='mixed').min() if len(trous) else pd.NaT,
                        'dernier_tick': pd.to_datetime(bounds.ts2, format='mixed').max() if len(bounds) else pd.NaT,
                        'trous_fin': set(pd.to_datetime(trous.ts2, format='mixed')) if len(trous) else set()}
    # ticks d'entree 13-B pour controle de la cotation de reference
    TK = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R13 / 'P13B_TICKS_*.csv')))])
    TK['quote_timestamp'] = pd.to_datetime(TK.quote_timestamp, format='mixed').dt.tz_localize(None)
    TK = TK.sort_values('quote_timestamp').drop_duplicates('event_id', keep='first').set_index('event_id')
    entrees, controle_ref = {}, {'conformes': 0, 'divergents': 0, 'sans_cotation': 0}
    audit_gap = {'egalites_observees_non_remplissages': 0, 'remplissages_apres_trou_dans_fenetre': 0}
    for r in E.itertuples():
        w = W[W.event_id == r.event_id]
        if not len(w):
            entrees[r.event_id] = {'statut': 'NO_REFERENCE_QUOTE'}
            controle_ref['sans_cotation'] += 1
            continue
        ref = w.iloc[0]
        if r.event_id in TK.index:
            tk = TK.loc[r.event_id]
            if tk.quote_timestamp == ref.ts and abs(tk.bid - ref.bid) < 1e-9 and abs(tk.ask - ref.ask) < 1e-9:
                controle_ref['conformes'] += 1
            else: controle_ref['divergents'] += 1
        p_limit = (ref.bid + ref.ask) / 2
        d = {'statut': 'NO_FILL', 'ts_ref': ref.ts, 'bid0': float(ref.bid), 'ask0': float(ref.ask),
             'p_limit': float(p_limit), 'spread0_bp': float((ref.ask - ref.bid) / p_limit * 10000),
             'ts_fill': pd.NaT, 'delai_fill_s': np.nan, 'n_ticks_fenetre': int(len(w))}
        apres = w[w.ts > ref.ts]
        cond = (apres.ask < p_limit) if r.direction == 1 else (apres.bid > p_limit)
        egal = (apres.ask == p_limit) if r.direction == 1 else (apres.bid == p_limit)
        audit_gap['egalites_observees_non_remplissages'] += int(egal.sum())
        if cond.any():
            tf = apres[cond].iloc[0]
            d.update(statut='FILL_PROXY', ts_fill=tf.ts,
                     delai_fill_s=float((tf.ts - r.t_decision_ts).total_seconds()))
            if (apres.ts.diff().dt.total_seconds() > 300).any() and tf.ts in set(apres.ts[apres.ts.diff().dt.total_seconds() > 300]):
                audit_gap['remplissages_apres_trou_dans_fenetre'] += 1
        entrees[r.event_id] = d
    # resultats par sortie et scenario
    ev_rows, grid_rows, comp_rows = [], [], []
    for exit_, mult in EXITS.items():
        for scen, s in SCEN.items():
            res, statuts, res_e0comp, rempli_ids = {}, {}, {}, []
            for r in E.itertuples():
                eid = r.event_id; d = entrees[eid]
                base = {'event_id': eid, 'grappe_id': r.grappe_id, 'sortie': exit_, 'scenario': scen, 'etiquette': LABELS[scen]}
                # reference E0 a convention comparable (slippage de sortie seule, prix 13-B)
                if r.statut_completude == 'COMPLET':
                    ps0 = r.prix_sortie * (1 - s / 10000) if r.direction == 1 else r.prix_sortie * (1 + s / 10000)
                    res_e0comp[eid] = float(r.direction * np.log(ps0 / r.prix_entree) * 10000)
                if d['statut'] != 'FILL_PROXY':
                    base['statut'] = d['statut']; statuts[d['statut']] = statuts.get(d['statut'], 0) + 1
                    ev_rows.append(base); continue
                rempli_ids.append(eid)
                entree = d['p_limit']; ts_fill = d['ts_fill']
                a = atr.get(eid, np.nan); hit = None
                if exit_ in ('X1', 'X2'):
                    for t in recs14.get(eid, []):
                        if t.ts < ts_fill: continue
                        fav = r.direction * (t.liq - entree)
                        if fav >= mult[0] * a: hit = ('TP_FIRST', t); break
                        if fav <= -mult[1] * a: hit = ('SL_FIRST', t); break
                    inter = inter14[eid]['premier_trou']; dt_ = inter14[eid]['dernier_tick']
                    cand_i = [x for x in (inter if pd.notna(inter) and inter >= ts_fill else None,
                                          dt_ if pd.notna(dt_) and dt_ < r.fin else None) if x is not None]
                    interruption = min(cand_i) if cand_i else pd.NaT
                    if hit is not None and r.statut_completude == 'INCOMPLET' and pd.notna(interruption) and not hit[1].ts < interruption:
                        hit = None
                if hit is not None:
                    statut, prix_s, ts_s = hit[0], float(hit[1].liq), hit[1].ts
                elif r.statut_completude == 'COMPLET':
                    statut, prix_s, ts_s = 'VERTICAL_FIRST', float(r.prix_sortie), r.t_sortie_13b
                else:
                    statut, prix_s, ts_s = 'CENSORED', np.nan, pd.NaT
                statuts[statut] = statuts.get(statut, 0) + 1
                base.update(statut=statut, timestamp_sortie=str(ts_s), prix_sortie=prix_s,
                            gap_avant_franchissement=bool(hit is not None and hit[1].ts in inter14[eid]['trous_fin']))
                if statut in ('TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'):
                    ps = prix_s * (1 - s / 10000) if r.direction == 1 else prix_s * (1 + s / 10000)
                    val = float(r.direction * np.log(ps / entree) * 10000)
                    fav_arr = [r.direction * np.log(t.liq / entree) * 10000 for t in recs14.get(eid, []) if t.ts >= ts_fill]
                    base.update(resultat_bp=val, duree_detention_min=float((ts_s - ts_fill).total_seconds() / 60),
                                mfe_bp=float(max(max(fav_arr), 0.0)) if fav_arr else np.nan,
                                mae_bp=float(max(-min(fav_arr), 0.0)) if fav_arr else np.nan)
                    res[eid] = val
                ev_rows.append(base)
            arr = np.array(list(res.values()), float)
            gr = pd.Series(res).groupby(Eidx.loc[list(res.keys()), 'grappe_id'].values).mean() if res else pd.Series(dtype=float)
            st_ev = stats(arr)
            coh = np.array([res.get(eid, 0.0) for eid in E.event_id], float)
            coh_e0 = np.array([res_e0comp.get(eid, 0.0) for eid in E.event_id], float)
            sous = [eid for eid in rempli_ids if eid in res and eid in res_e0comp]
            grid_rows.append({'politique': 'E3', 'sortie': exit_, 'scenario': scen, 'etiquette': LABELS[scen],
                              'statut_remplissage': 'QUOTE_CROSSING_PROXY_ONLY', 'opportunites': 443,
                              'remplissages_proxy': int(sum(1 for v in entrees.values() if v['statut'] == 'FILL_PROXY')),
                              'NO_FILL': statuts.get('NO_FILL', 0), 'NO_REFERENCE_QUOTE': statuts.get('NO_REFERENCE_QUOTE', 0),
                              'n_TP_FIRST': statuts.get('TP_FIRST', 0), 'n_SL_FIRST': statuts.get('SL_FIRST', 0),
                              'n_VERTICAL_FIRST': statuts.get('VERTICAL_FIRST', 0), 'n_CENSORED': statuts.get('CENSORED', 0),
                              **{f'ev_{k}': v for k, v in st_ev.items()},
                              'gr_moyenne': float(gr.mean()) if len(gr) else np.nan,
                              'gr_mediane': float(gr.median()) if len(gr) else np.nan, 'n_grappes': int(len(gr)),
                              'cohorte443_moyenne': float(coh.mean()), 'cohorte443_mediane': float(np.median(coh)),
                              'commission_theorique_equilibre_bp': float(st_ev.get('moyenne', np.nan))})
            comp_rows.append({'sortie': exit_, 'scenario': scen, 'n_sous_ensemble_rempli_complet': len(sous),
                              'E3_moyenne_cohorte443': float(coh.mean()), 'E0_comparable_moyenne_cohorte443': float(coh_e0.mean()),
                              'E3_mediane_sous_ensemble': float(np.median([res[e] for e in sous])) if sous else np.nan,
                              'E0_comparable_mediane_sous_ensemble': float(np.median([res_e0comp[e] for e in sous])) if sous else np.nan,
                              'convention_E0': 'prix 13-B, slippage de sortie seule (comparable a E3)'})
    EV = pd.DataFrame(ev_rows); EV.to_csv(R16 / 'PHASE16_ENTRY_EXECUTIONS_DETAIL.csv', index=False)
    M = pd.DataFrame(grid_rows); M.to_csv(R16 / 'PHASE16_EXIT_MATRIX.csv', index=False)
    pd.DataFrame(comp_rows).to_csv(R16 / 'PHASE16_ENTRY_COMPARISON.csv', index=False)
    # evenements d'entree
    erows = []
    for r in E.itertuples():
        d = entrees[r.event_id]
        erows.append({'event_id': r.event_id, 'grappe_id': r.grappe_id, 'direction': int(r.direction),
                      't_decision': str(r.t_decision_ts), 'p_M1': float(r.p_M1),
                      'timestamp_reference': str(d.get('ts_ref', '')), 'Bid_0': d.get('bid0'), 'Ask_0': d.get('ask0'),
                      'spread_initial_bp': d.get('spread0_bp'), 'P_limit': d.get('p_limit'),
                      'timestamp_activation': str(d.get('ts_ref', '')), 'statut_remplissage': d['statut'],
                      'statut_preuve': 'QUOTE_CROSSING_PROXY_ONLY', 'timestamp_franchissement': str(d.get('ts_fill', '')),
                      'delai_franchissement_s': d.get('delai_fill_s'), 'expiration': str(r.t_decision_ts + pd.Timedelta(seconds=60)),
                      'prix_entree_E0': float(r.prix_entree),
                      'amelioration_vs_E0_bp': float(r.direction * np.log(r.prix_entree / d['p_limit']) * 10000) if d['statut'] == 'FILL_PROXY' else np.nan,
                      'n_ticks_fenetre_60s': d.get('n_ticks_fenetre'), 'statut_completude_13B': r.statut_completude})
    ED = pd.DataFrame(erows); ED.to_csv(R16 / 'PHASE16_ENTRY_EVENTS.csv', index=False)
    cw = []
    for _, m in M.iterrows():
        dd = EV[(EV.sortie == m.sortie) & (EV.scenario == m.scenario) & EV.resultat_bp.notna()]
        g = dd.groupby('grappe_id').resultat_bp.mean()
        cw.append({'sortie': m.sortie, 'scenario': m.scenario, 'n_evenements': int(len(dd)), 'n_grappes': int(len(g)),
                   'moyenne_evenement': float(dd.resultat_bp.mean()), 'moyenne_grappe': float(g.mean()),
                   'mediane_evenement': float(dd.resultat_bp.median()), 'mediane_moyennes_par_grappe': float(g.median()),
                   'cohorte443_moyenne': m.cohorte443_moyenne})
    pd.DataFrame(cw).to_csv(R16 / 'PHASE16_CLUSTER_WEIGHTING.csv', index=False)
    filled = ED[ED.statut_remplissage == 'FILL_PROXY']
    cov = pd.DataFrame([
        {'element': 'opportunites_exposees', 'effectif': 443, 'detail': 'cohorte figee'},
        {'element': 'cotations_de_reference_trouvees', 'effectif': int((ED.statut_remplissage != 'NO_REFERENCE_QUOTE').sum()), 'detail': f"controle vs tick 13-B: {controle_ref}"},
        {'element': 'franchissements_proxy', 'effectif': int(len(filled)), 'detail': 'QUOTE_CROSSING_PROXY_ONLY - execution reelle non prouvee'},
        {'element': 'NO_FILL_expiration_60s', 'effectif': int((ED.statut_remplissage == 'NO_FILL').sum()), 'detail': 'ni perte ni gain; conserves dans la cohorte'},
        {'element': 'egalites_strictes_non_comptees', 'effectif': audit_gap['egalites_observees_non_remplissages'], 'detail': 'Ask == P_limit ou Bid == P_limit ne sont pas des franchissements'},
        {'element': 'remplissages_premier_tick_apres_trou_fenetre', 'effectif': audit_gap['remplissages_apres_trou_dans_fenetre'], 'detail': 'trou > 5 min dans la fenetre de 60 s (fermetures)'},
        {'element': 'incompletes_13B', 'effectif': 22, 'detail': 'identifiees; barrieres classees seulement avant premiere interruption, sinon CENSORED'},
        {'element': 'franchissements_barrieres_apres_trou', 'effectif': int(EV.gap_avant_franchissement.sum()) if 'gap_avant_franchissement' in EV else 0, 'detail': 'lignes evenement x cellule; ordre intra-gap jamais suppose (limites 14.1)'}])
    cov.to_csv(R16 / 'PHASE16_FILL_AND_GAP_AUDIT.csv', index=False)
    # verdicts geles
    taux = len(filled) / 443
    verdict_structure = 'PASSIVE_ENTRY_STRUCTURE_IDENTIFIED' if taux >= 0.50 else ('PASSIVE_ENTRY_STRUCTURE_NOT_IDENTIFIED' if taux < 0.25 else 'PASSIVE_ENTRY_ANALYSIS_INCONCLUSIVE')
    C = pd.DataFrame(comp_rows).set_index(['sortie', 'scenario'])
    adv = all(C.loc[('X0', s), 'E3_moyenne_cohorte443'] > C.loc[('X0', s), 'E0_comparable_moyenne_cohorte443'] for s in SCEN) and \
          C.loc[('X0', 'S0'), 'E3_mediane_sous_ensemble'] >= C.loc[('X0', 'S0'), 'E0_comparable_mediane_sous_ensemble']
    notf = all(C.loc[('X0', s), 'E3_moyenne_cohorte443'] <= C.loc[('X0', s), 'E0_comparable_moyenne_cohorte443'] for s in SCEN)
    verdict_eco = 'EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_FOUND' if adv else ('EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_NOT_FOUND' if notf else 'ECONOMICALLY_INCONCLUSIVE')
    resultats = {'phase': '16', 'qualification': 'EXPLORATOIRE IS - QUOTE_CROSSING_PROXY_ONLY',
                 'controle_cotation_reference_vs_13B': controle_ref,
                 'taux_franchissement_proxy': float(taux), 'delai_franchissement_median_s': float(filled.delai_franchissement_s.median()) if len(filled) else None,
                 'amelioration_vs_E0_mediane_bp': float(filled.amelioration_vs_E0_bp.median()) if len(filled) else None,
                 'matrice': M.to_dict('records'), 'comparaison_E0': comp_rows,
                 'verdict_structure': verdict_structure, 'verdict_qualite_execution': 'QUOTE_CROSSING_PROXY_ONLY',
                 'verdict_economie': verdict_eco,
                 'rappel': 'franchissement de cotation seulement; execution reelle non prouvee; aucune strategie'}
    (R16 / 'PHASE16_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False, default=str))
    print(json.dumps({'taux': taux, 'verdicts': [verdict_structure, verdict_eco], 'controle_ref': controle_ref}, indent=1), flush=True)
    print('P16 analyse terminee', flush=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
