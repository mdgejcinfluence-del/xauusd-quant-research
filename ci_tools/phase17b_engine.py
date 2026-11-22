#!/usr/bin/env python3
"""PHASE 17-B - Labels economiques B08/B09 et modeles M2 (exploratoire IS).
lot: premier tick d'entree et extremes de liquidation pour les evenements
filtres M1 de tous les segments (apprentissage/calibration/evaluation).
analyse: labels S2 (+S0/S1), features gelees, M0_ECON, seuils P_BE,
regressions logistiques (implementation gelee Phase 12-B importee),
evaluations calibration et evaluation. Holdout jamais accede."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R12 = ROOT / 'reports/meta_alpha/phase12'
R13 = ROOT / 'reports/meta_alpha/phase13'
R14 = ROOT / 'reports/meta_alpha/phase14'
R17 = ROOT / 'reports/meta_alpha/phase17'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
M0_M1 = 0.7591463414634146
SCEN = {'S0': 0.0, 'S1': 0.5, 'S2': 1.0}
CONTRATS = {'B08': (1.5, 1.0), 'B09': (1.5, 1.5)}
VARS = ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN',
        'MFE_A_TREINT_BP', 'NB_TOUCHES_P0_AVANT_TREINT', 'ATR14_H1', 'SPREAD_DECISION_BP']
SESSIONS = ['LONDON', 'LONDON_NY_OVERLAP', 'NY_AFTERNOON', 'NIGHT_OTHER']

def population():
    F = pd.read_csv(R12 / 'PHASE12B_FEATURES.csv')
    P = json.loads((R12 / 'PHASE12C1_MODEL_PARAMETERS.json').read_text())
    d = F[(F.famille == 'F10-01') & (F.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1']))].copy()
    z = np.full(len(d), float(P['intercept']))
    for var, beta in P['coefficients'].items():
        if var.startswith('SESSION_REINTEGRATION='):
            z = z + beta * (d.SESSION_REINTEGRATION == var.split('=', 1)[1]).astype(float).values
        else:
            z = z + beta * d[var].astype(float).values
    d['p_M1_filtre'] = 1 / (1 + np.exp(-np.clip(z, -35, 35)))
    d = d[d.p_M1_filtre > M0_M1].copy()
    P11 = pd.read_csv(ROOT / 'reports/meta_alpha/phase11/PHASE11C_EVENT_PATHS.csv',
                      usecols=['event_id', 'direction'])
    d = d.merge(P11, on='event_id', validate='one_to_one')
    d['t_decision'] = pd.to_datetime(d.t_reintegration)
    d['fin'] = pd.to_datetime(d.fin_fenetre_observation)
    return d

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
    batch = os.environ['P17_BATCH']
    E = population()
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
        cand = E[(E.t_decision < pmax) & (E.fin > pmin)]
        for r in cand.itertuples():
            liq = 'bid' if r.direction == 1 else 'ask'
            q = f"""WITH s AS (SELECT timestamp_utc AS ts, bid, ask, {liq} AS liq FROM read_parquet('{local}')
                    WHERE timestamp_utc > '{r.t_decision}' AND timestamp_utc <= '{r.fin}' ORDER BY timestamp_utc),
                    w AS (SELECT *, max(liq) OVER (ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmax,
                            min(liq) OVER (ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS pmin,
                            lag(ts) OVER (ORDER BY ts) AS pts FROM s)
                    SELECT ts, bid, ask, liq, pts, pmax, pmin FROM w
                    WHERE pmax IS NULL OR liq > pmax OR liq < pmin OR (pts IS NOT NULL AND epoch(ts) - epoch(pts) > 300)"""
            w = con.execute(q).df()
            if not len(w): continue
            w['ts'] = pd.to_datetime(w.ts).dt.tz_localize(None)
            for t in w[w.pts.notna() & ((w.ts - pd.to_datetime(w.pts, format='mixed').dt.tz_localize(None)).dt.total_seconds() > 300)].itertuples():
                rows.append({'event_id': r.event_id, 'kind': 'HOLE', 'ts': str(pd.Timestamp(t.pts).tz_localize(None)), 'ts2': str(t.ts), 'liq': np.nan, 'bid': np.nan, 'ask': np.nan})
            for t in w[(w.pmax.isna()) | (w.liq > w.pmax) | (w.liq < w.pmin)].itertuples():
                rows.append({'event_id': r.event_id, 'kind': 'EXTREME', 'ts': str(t.ts), 'ts2': '', 'liq': float(t.liq), 'bid': float(t.bid), 'ask': float(t.ask)})
            rows.append({'event_id': r.event_id, 'kind': 'BOUND', 'ts': str(w.ts.iloc[0]), 'ts2': str(w.ts.iloc[-1]), 'liq': float(len(w)), 'bid': np.nan, 'ask': np.nan})
            lt = w.iloc[-1]
            rows.append({'event_id': r.event_id, 'kind': 'LAST', 'ts': str(lt.ts), 'ts2': '', 'liq': float(lt.liq), 'bid': float(lt.bid), 'ask': float(lt.ask)})
        print('P17 part', p['name'], flush=True)
    R17.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows, columns=['event_id', 'kind', 'ts', 'ts2', 'liq', 'bid', 'ask']).to_csv(R17 / f'P17_PATH_{batch}.csv', index=False)
    print('P17 lot termine', batch, len(rows), flush=True)

def charger_barres():
    bars = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz')))])
    bars['ts'] = pd.to_datetime(bars.ts)
    if bars.ts.dt.tz is not None: bars['ts'] = bars.ts.dt.tz_localize(None)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

def atr_et_spread(E, bars):
    bars = bars.copy(); bars['heure'] = bars.ts.dt.floor('h')
    H = bars.groupby('heure').agg(h=('mh', 'max'), l=('ml', 'min'), c=('mc', 'last')).reset_index()
    pc = H.c.shift(1)
    H['tr'] = np.maximum(H.h - H.l, np.maximum((H.h - pc).abs(), (H.l - pc).abs()))
    atr = np.full(len(H), np.nan)
    if len(H) > 14:
        atr[14] = H.tr.iloc[1:15].mean()
        for i in range(15, len(H)): atr[i] = (13 * atr[i - 1] + H.tr.iloc[i]) / 14
    H['atr'] = atr; H['cloture'] = H.heure + pd.Timedelta(hours=1)
    A = H[['cloture', 'atr']].dropna().reset_index(drop=True)
    B = bars.set_index('ts')
    out_atr, out_sp = {}, {}
    for r in E.itertuples():
        sel = A[A.cloture <= r.t_decision]
        out_atr[r.event_id] = float(sel.atr.iloc[-1]) if len(sel) else np.nan
        m = r.t_decision - pd.Timedelta(minutes=1)
        out_sp[r.event_id] = float(B.loc[m, 'sp']) if m in B.index else np.nan
    return out_atr, out_sp

def remplir(direction, pe, ps, s):
    if direction == 1: a, b = pe * (1 + s / 10000), ps * (1 - s / 10000)
    else: a, b = pe * (1 - s / 10000), ps * (1 + s / 10000)
    return float(direction * np.log(b / a) * 10000)

def mode_analyse():
    sys.path.insert(0, str(ROOT / 'ci_tools'))
    from phase12b_engine import logistique_irls, metriques, calibration
    E = population().reset_index(drop=True)
    bars = charger_barres()
    atr, spread = atr_et_spread(E, bars)
    E['ATR14_H1'] = E.event_id.map(atr); E['SPREAD_DECISION_BP'] = E.event_id.map(spread)
    # chemins tick
    P = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R17 / 'P17_PATH_*.csv')))])
    P['ts'] = pd.to_datetime(P.ts, format='mixed')
    chemins, inter = {}, {}
    for eid, d in P.groupby('event_id'):
        ext = d[d.kind == 'EXTREME'].drop_duplicates(['ts', 'liq']).sort_values('ts')
        recs, cmax, cmin = [], -np.inf, np.inf
        for t in ext.itertuples():
            if t.liq > cmax or t.liq < cmin: recs.append(t); cmax = max(cmax, t.liq); cmin = min(cmin, t.liq)
        chemins[eid] = recs
        lasts = d[d.kind == 'LAST'].sort_values('ts')
        inter[eid] = {'dernier_prix': (float(lasts.liq.iloc[-1]), lasts.ts.iloc[-1]) if len(lasts) else (np.nan, pd.NaT)}
        trous = d[d.kind == 'HOLE']; bounds = d[d.kind == 'BOUND']
        inter[eid].update({'premier_trou': pd.to_datetime(trous.ts, format='mixed').min() if len(trous) else pd.NaT,
                      'dernier_tick': pd.to_datetime(bounds.ts2, format='mixed').max() if len(bounds) else pd.NaT})
    T14 = pd.read_csv(R14 / 'PHASE14_TRIPLE_BARRIER_EVENTS.csv')
    # ---- labels par contrat
    labels = {}
    for contrat, (tpm, slm) in CONTRATS.items():
        rows = []
        for r in E.itertuples():
            eid = r.event_id; recs = chemins.get(eid, [])
            base = {'event_id': eid, 'grappe_id': r.grappe_id, 'ensemble': r.ensemble, 'direction': int(r.direction),
                    't_decision': str(r.t_decision), 'contrat': contrat}
            if not recs or not recs[0].ts < r.t_decision + pd.Timedelta(seconds=60):
                base.update(statut_entree='NON_EXECUTION', statut_label='NON_EXECUTION'); rows.append(base); continue
            t0 = recs[0]; entree = float(t0.ask if r.direction == 1 else t0.bid)
            a = r.ATR14_H1
            if not np.isfinite(a):
                base.update(statut_entree='EXECUTE', statut_label='UNAVAILABLE_ATR'); rows.append(base); continue
            hit = None
            for t in recs:
                fav = r.direction * (t.liq - entree)
                if fav >= tpm * a: hit = ('TP_FIRST', t); break
                if fav <= -slm * a: hit = ('SL_FIRST', t); break
            interruption = inter[eid]['premier_trou']; dt_ = inter[eid]['dernier_tick']
            cand_i = [x for x in (interruption if pd.notna(interruption) else None,
                                  dt_ if pd.notna(dt_) and dt_ < r.fin else None) if x is not None]
            interruption = min(cand_i) if cand_i else pd.NaT
            complet = str(r.statut_disponibilite) == 'EXTRAIT_BORNE_OK' and pd.notna(r.fin)
            # completude economique: sortie verticale determinable si la trajectoire tick atteint fin
            atteint_fin = pd.notna(dt_) and dt_ >= r.fin - pd.Timedelta(minutes=1)
            if hit is not None and (not pd.notna(interruption) or hit[1].ts < interruption or atteint_fin):
                statut, prix_s, ts_s = hit[0], float(hit[1].liq), hit[1].ts
            elif atteint_fin:
                # sortie verticale: dernier tick de liquidation disponible avant l echeance
                lp, lts = inter[eid]['dernier_prix']
                statut, prix_s, ts_s = 'VERTICAL_FIRST', float(lp), lts
            else:
                statut, prix_s, ts_s = 'CENSORED', np.nan, pd.NaT
            base.update(statut_entree='EXECUTE', timestamp_entree=str(t0.ts), prix_entree=entree,
                        mecanisme=statut, timestamp_sortie=str(ts_s), prix_sortie=prix_s)
            if statut in ('TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'):
                for scen, s in SCEN.items(): base[f'PL_{scen}_bp'] = remplir(r.direction, entree, prix_s, s)
                base['Y_ECON'] = int(base['PL_S2_bp'] > 0)
                base['statut_label'] = 'ETIQUETE'
            else:
                base['statut_label'] = statut
            rows.append(base)
        labels[contrat] = pd.DataFrame(rows)
    # reconciliation evaluation vs Phase 14 (resultats S2 deja geles)
    recon = {}
    for contrat in CONTRATS:
        lab = labels[contrat]
        ev = lab[(lab.ensemble == 'EVALUATION') & (lab.statut_label == 'ETIQUETE')]
        ref = T14[(T14.normalisation == 'B_ATR14_H1') & (T14.configuration == contrat) & (T14.scenario == 'S2')]
        ref = ref[ref.statut.isin(['TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'])].set_index('event_id')
        communs = [e for e in ev.event_id if e in ref.index]
        ecarts = [abs(ev.set_index('event_id').loc[e, 'PL_S2_bp'] - ref.loc[e, 'resultat_bp']) for e in communs]
        recon[contrat] = {'communs': len(communs), 'ecart_max_bp': float(max(ecarts)) if ecarts else None,
                          'conforme': bool(ecarts and max(ecarts) < 1e-6)}
    # ---- features, entrainement, evaluation par contrat
    resultats = {'phase': '17-B', 'qualification': 'HISTORIQUE EXPLORATOIRE - POPULATION DEJA ETUDIEE',
                 'reconciliation_evaluation_phase14': recon, 'contrats': {}}
    decisions_rows = []
    for contrat in CONTRATS:
        lab = labels[contrat]
        lab.to_csv(R17 / f'PHASE17B_LABELS_{contrat}.csv', index=False)
        F = E[['event_id', 'grappe_id', 'ensemble', 'SESSION_REINTEGRATION'] + VARS[:4]].copy()
        F['ATR14_H1'] = F.event_id.map(atr); F['SPREAD_DECISION_BP'] = F.event_id.map(spread)
        F = F.merge(lab[['event_id', 'Y_ECON', 'statut_label', 'mecanisme']], on='event_id', how='left')
        F.to_csv(R17 / f'PHASE17B_FEATURES_{contrat}.csv', index=False)
        def matrice(dd):
            Xs = [dd[VARS].astype(float).values]
            cats = [(dd.SESSION_REINTEGRATION == s).astype(float).values.reshape(-1, 1) for s in SESSIONS]
            return np.hstack(Xs + cats)
        app = F[(F.ensemble == 'APPRENTISSAGE') & (F.statut_label == 'ETIQUETE')].dropna(subset=VARS)
        cal = F[(F.ensemble == 'CALIBRATION') & (F.statut_label == 'ETIQUETE')].dropna(subset=VARS)
        ev = F[(F.ensemble == 'EVALUATION') & (F.statut_label == 'ETIQUETE')].dropna(subset=VARS)
        lab_app = lab[(lab.ensemble == 'APPRENTISSAGE') & (lab.statut_label == 'ETIQUETE')]
        pl = lab_app.PL_S2_bp
        G = float(pl[pl > 0].mean()) if (pl > 0).any() else np.nan
        L = float(-pl[pl <= 0].mean()) if (pl <= 0).any() else np.nan
        p_be = float(L / (G + L)) if np.isfinite(G) and np.isfinite(L) and (G + L) > 0 else np.nan
        m0 = float(app.Y_ECON.mean()) if len(app) else np.nan
        info = {'contrat': contrat, 'effectifs': {}, 'M0_ECON': m0, 'G_bp': G, 'L_bp': L, 'P_BE': p_be}
        for nom, dd in (('APPRENTISSAGE', app), ('CALIBRATION', cal), ('EVALUATION', ev)):
            info['effectifs'][nom] = {'n_etiquetes': int(len(dd)), 'positifs': int(dd.Y_ECON.sum()),
                                      'minorite': int(min(dd.Y_ECON.sum(), len(dd) - dd.Y_ECON.sum())) if len(dd) else 0}
        crit = all(info['effectifs'][s]['n_etiquetes'] >= 100 and info['effectifs'][s]['minorite'] >= 50
                   for s in ('APPRENTISSAGE', 'EVALUATION'))
        if not crit or not np.isfinite(p_be):
            info['verdict'] = 'M2_NON_EVALUABLE'
            resultats['contrats'][contrat] = info
            continue
        beta, predire = logistique_irls(matrice(app), app.Y_ECON.values.astype(float))
        params = {'contrat': contrat, 'modele': 'regression logistique (implementation gelee phase12b_engine.logistique_irls, IRLS tol 1e-10, 200 iter., ridge numerique 1e-8)',
                  'ordre_variables': ['INTERCEPT'] + VARS + [f'SESSION_REINTEGRATION={s}' for s in SESSIONS],
                  'intercept': float(beta[0]), 'coefficients': {v: float(b) for v, b in zip(VARS + [f'SESSION_REINTEGRATION={s}' for s in SESSIONS], beta[1:])},
                  'M0_ECON': m0, 'G_bp': G, 'L_bp': L, 'P_BE': p_be,
                  'n_apprentissage': int(len(app)), 'etiquette': 'NET_OF_SPREAD_AND_HYPOTHETICAL_S2_SLIPPAGE_BEFORE_COMMISSION'}
        (R17 / f'PHASE17B_M2_{contrat}_PARAMETERS.json').write_text(json.dumps(params, indent=1, ensure_ascii=False))
        evals = {}
        for nom, dd in (('CALIBRATION', cal), ('EVALUATION', ev)):
            y = dd.Y_ECON.values.astype(float); p = predire(matrice(dd))
            m2 = metriques(y, p); m0m = metriques(y, np.full(len(dd), m0))
            retenus = p > p_be
            lab_dd = lab.set_index('event_id').loc[dd.event_id]
            pl_ev = lab_dd.PL_S2_bp.values
            evals[nom] = {'M0_ECON': m0m, 'M2': m2, 'calibration_M2': calibration(y, p),
                          'couverture_decisions': float(retenus.mean()),
                          'proportion_rejetees': float(1 - retenus.mean()),
                          'esperance_realisee_retenues_bp': float(pl_ev[retenus].mean()) if retenus.any() else None,
                          'precision_decisions': float(y[retenus].mean()) if retenus.any() else None,
                          'frequence_labels_positifs': float(y.mean())}
            if nom == 'EVALUATION':
                for eid, q, dec, yy, pp in zip(dd.event_id, p, retenus, y, pl_ev):
                    decisions_rows.append({'event_id': eid, 'contrat': contrat, 'q_M2': float(q), 'P_BE': p_be,
                                           'decision': 'EXPOSITION' if dec else 'REJET', 'Y_ECON_realise': int(yy),
                                           'PL_S2_bp': float(pp), 'mecanisme': lab_dd.loc[eid, 'mecanisme']})
        info['evaluations'] = evals
        amel = evals['EVALUATION']['M2']['brier'] < evals['EVALUATION']['M0_ECON']['brier'] and \
               evals['EVALUATION']['M2']['log_loss'] < evals['EVALUATION']['M0_ECON']['log_loss']
        info['verdict'] = 'M2_PREDICTIVE_ECONOMIC_SIGNAL_SUPPORTED_HISTORICALLY' if amel else 'M2_NO_ECONOMIC_PREDICTIVE_IMPROVEMENT'
        resultats['contrats'][contrat] = info
    pd.DataFrame(decisions_rows).to_csv(R17 / 'PHASE17B_ECONOMIC_DECISIONS.csv', index=False)
    ev_rows = []
    for contrat, info in resultats['contrats'].items():
        for seg, eff in info['effectifs'].items():
            row = {'contrat': contrat, 'segment': seg, **eff, 'M0_ECON': info['M0_ECON'], 'P_BE': info['P_BE'],
                   'verdict': info['verdict']}
            if 'evaluations' in info and seg in info['evaluations']:
                e = info['evaluations'][seg]
                row.update({'brier_M0': e['M0_ECON']['brier'], 'brier_M2': e['M2']['brier'],
                            'logloss_M0': e['M0_ECON']['log_loss'], 'logloss_M2': e['M2']['log_loss'],
                            'auc_M2': e['M2']['auc'], 'couverture': e['couverture_decisions'],
                            'esperance_retenues_bp': e['esperance_realisee_retenues_bp']})
            ev_rows.append(row)
    pd.DataFrame(ev_rows).to_csv(R17 / 'PHASE17B_MODEL_EVALUATION.csv', index=False)
    audit_f = {'variables': {v: {'borne': 'disponible a t_decision (12-B pour les 5 variables M1; ATR derniere H1 cloturee; spread minute se terminant a t_decision)',
                                 'manquants_apprentissage': int(F[v].isna().sum()) if False else None} for v in VARS},
               'p_M1': 'EXCLU des variables (filtre primaire gele uniquement)',
               'implementation_M2': 'logistique_irls du code gele ci_tools/phase12b_engine.py importe tel quel (IRLS tol 1e-10, 200 iter., ridge 1e-8, variables brutes, reference ASIA)',
               'aucune_variable_future': True}
    (R17 / 'PHASE17B_FEATURE_AUDIT.json').write_text(json.dumps(audit_f, indent=1, ensure_ascii=False))
    audit_l = {'reconciliation_evaluation_phase14': recon,
               'regles': 'censures/NON_EXECUTION/UNAVAILABLE jamais etiquetes; mecanismes conserves; scenario primaire S2',
               'effectifs_par_contrat': {c: labels[c].groupby(['ensemble', 'statut_label']).size().to_dict() for c in CONTRATS}}
    (R17 / 'PHASE17B_LABEL_AUDIT.json').write_text(json.dumps(audit_l, indent=1, ensure_ascii=False, default=str))
    (R17 / 'PHASE17B_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False, default=str))
    print(json.dumps({'recon': recon, 'verdicts': {c: i['verdict'] for c, i in resultats['contrats'].items()}}, indent=1, default=str), flush=True)
    print('P17 analyse terminee', flush=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
