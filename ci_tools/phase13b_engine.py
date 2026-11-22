#!/usr/bin/env python3
"""PHASE 13-B - Evaluation economique exploratoire IS du signal H1.

Contrat gele: PHASE13A1_EXECUTION_CONTRACT_V2.json (seq330).
Modes:
  lot     (env P13B_BATCH): telecharge UN batch Kaggle IS prive, reconstruit
          les barres M1 Bid/Ask (meme agregation que phase10_engine.charger,
          + horodatages exacts du premier/dernier tick de chaque minute) et
          extrait, pour les evenements candidats dont la fenetre d'entree
          intersecte les partitions du lot, le premier tick strictement
          posterieur a t_decision. Sorties: P13B_BARS_<batch>.csv.gz et
          P13B_TICKS_<batch>.csv dans reports/meta_alpha/phase13/.
  analyse : fusionne les 8 lots, applique le modele H1 gele aux seuls
          evenements F10-01 EVALUATION etiquetes (543), applique la regle
          p_M1 > M0 gele, l'entree tick causale, la sortie de cloture de
          fenetre 8 bougies H1, les scenarios S0/S1/S2, et ecrit les
          livrables PHASE13B_*.

Holdout 2020-2026: jamais monte, liste, lu ni accede (filtre IS_END repris
de phase10_engine: partitions IS uniquement). Aucune optimisation.
Grille de verdict (fixee avant resultats, seq331):
  POSITIVE  : moyenne evenement > 0 ET moyenne grappe > 0 ET mediane
              evenement > 0 sous S0, S1 et S2, conditions d'arret respectees.
  NEGATIVE  : moyenne evenement < 0 ET moyenne grappe < 0 sous S0, S1, S2.
  NON_MESURABLE si conditions d'arret franchies; sinon INCONCLUSIVE.
"""
import glob
import io
import json
import os
import pathlib
import shutil
import sys
import zipfile

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R13 = ROOT / 'reports/meta_alpha/phase13'
R12 = ROOT / 'reports/meta_alpha/phase12'
IS_END = pd.Timestamp('2020-01-20 09:36:27')  # borne IS historique (phase10)
M0 = 0.7591463414634146
SCEN = {'S0': 0.0, 'S1': 0.5, 'S2': 1.0}


def candidats():
    """Population primaire preenregistree: F10-01, EVALUATION, etiquetes."""
    F = pd.read_csv(R12 / 'PHASE12B_FEATURES.csv')
    d = F[(F.famille == 'F10-01') & (F.ensemble == 'EVALUATION') &
          (F.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1']))].copy()
    paths = pd.read_csv(ROOT / 'reports/meta_alpha/phase11/PHASE11C_EVENT_PATHS.csv',
                        usecols=['event_id', 'direction'])
    d = d.merge(paths, on='event_id', how='left', validate='one_to_one')
    assert d.direction.notna().all(), 'direction manquante'
    assert len(d) == 543, f'population attendue 543, obtenu {len(d)}'
    d['t_decision'] = pd.to_datetime(d.t_reintegration)
    d['fin_fenetre'] = pd.to_datetime(d.fin_fenetre_observation)
    return d


def probabilites(d):
    """Application deterministe du modele gele PHASE12C1 (aucune estimation)."""
    P = json.loads((R12 / 'PHASE12C1_MODEL_PARAMETERS.json').read_text())
    z = np.full(len(d), float(P['intercept']))
    for var, beta in P['coefficients'].items():
        if var.startswith('SESSION_REINTEGRATION='):
            sess = var.split('=', 1)[1]
            z = z + beta * (d.SESSION_REINTEGRATION == sess).astype(float).values
        else:
            z = z + beta * d[var].astype(float).values
    z = np.clip(z, -35, 35)
    return 1.0 / (1.0 + np.exp(-z))


# ---------------------------------------------------------------- lots CI
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
    batch = os.environ['P13B_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json')
                     .read_text())['partitions']
    kstate = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json')
                        .read_text())
    batchof = {n: i['batch'] for n, i in kstate['uploaded'].items()}
    parts = [p for p in inv
             if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00'))
             .tz_localize(None) <= IS_END and batchof.get(p['name']) == batch]
    print('P13B lot', batch, len(parts), 'partitions IS', flush=True)
    cand = candidats()
    localdir = telecharger_batch(batch)
    con = duckdb.connect()
    con.execute("SET memory_limit='5GB'")
    con.execute('SET threads=2')
    bars_frames, tick_rows = [], []
    for p in parts:
        local = localdir / p['name']
        if not local.exists():
            print('absente', p['name'], flush=True)
            continue
        q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts,
                arg_min(bid, timestamp_utc) AS bo, max(bid) AS bh, min(bid) AS bl,
                arg_max(bid, timestamp_utc) AS bc,
                arg_min(ask, timestamp_utc) AS ao, max(ask) AS ah, min(ask) AS al,
                arg_max(ask, timestamp_utc) AS ac,
                arg_min(mid, timestamp_utc) AS mo, max(mid) AS mh, min(mid) AS ml,
                arg_max(mid, timestamp_utc) AS mc,
                median((ask-bid)/mid)*10000 AS sp,
                arg_min(timestamp_utc, timestamp_utc) AS first_tick_ts,
                arg_max(timestamp_utc, timestamp_utc) AS last_tick_ts
                FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
        b = con.execute(q).df()
        bars_frames.append(b)
        # premier tick strictement posterieur a t_decision (< +60 s)
        pmin = pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None)
        pmax = pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None)
        ev = cand[(cand.t_decision < pmax) &
                  (cand.t_decision + pd.Timedelta(seconds=60) > pmin)]
        for r in ev.itertuples():
            qq = f"""SELECT timestamp_utc, bid, ask FROM read_parquet('{local}')
                     WHERE timestamp_utc > '{r.t_decision}' AND
                           timestamp_utc < '{r.t_decision + pd.Timedelta(seconds=60)}'
                     ORDER BY timestamp_utc LIMIT 1"""
            t = con.execute(qq).df()
            if len(t):
                tick_rows.append({'event_id': r.event_id,
                                  'quote_timestamp': str(t.timestamp_utc.iloc[0]),
                                  'bid': float(t.bid.iloc[0]),
                                  'ask': float(t.ask.iloc[0]),
                                  'partition': p['name']})
        print('P13B part', p['name'], flush=True)
    bars = pd.concat(bars_frames).drop_duplicates('ts').sort_values('ts')
    R13.mkdir(parents=True, exist_ok=True)
    bars.round(6).to_csv(R13 / f'P13B_BARS_{batch}.csv.gz', index=False,
                         compression='gzip')
    pd.DataFrame(tick_rows, columns=['event_id', 'quote_timestamp', 'bid', 'ask', 'partition']).to_csv(R13 / f'P13B_TICKS_{batch}.csv', index=False)
    print('P13B lot termine', batch, len(bars), 'barres,',
          len(tick_rows), 'ticks entree', flush=True)


# ---------------------------------------------------------------- analyse
def stats_ret(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if not len(x):
        return {}
    q = np.quantile(x, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95])
    return {'n': int(len(x)), 'moyenne': float(x.mean()), 'mediane': float(q[3]),
            'p1': float(q[0]), 'p5': float(q[1]), 'p25': float(q[2]),
            'p75': float(q[4]), 'p95': float(q[5]),
            'part_positifs': float((x > 0).mean()), 'part_negatifs': float((x < 0).mean()),
            'perte_maximale': float(x.min()), 'gain_maximal': float(x.max())}


def mode_analyse():
    d = candidats().reset_index(drop=True)
    d['p_M1'] = probabilites(d)
    # controle de reproduction des metriques predictives 12-B (non economique)
    y = d.RESUMPTION.values.astype(float)
    pc = np.clip(d.p_M1.values, 1e-15, 1 - 1e-15)
    ctrl = {'brier_M1_evaluation': float(np.mean((pc - y) ** 2)),
            'attendues_12B': {'brier': 0.16538954947396367, 'log_loss': 0.5468387473824291},
            'log_loss_M1_evaluation': float(-np.mean(y * np.log(pc) + (1 - y) * np.log(1 - pc)))}
    ctrl['reproduction_conforme'] = bool(
        abs(ctrl['brier_M1_evaluation'] - ctrl['attendues_12B']['brier']) < 1e-9 and
        abs(ctrl['log_loss_M1_evaluation'] - ctrl['attendues_12B']['log_loss']) < 1e-9)
    print('controle reproduction 12-B:', ctrl, flush=True)

    bars = pd.concat([pd.read_csv(f) for f in
                      sorted(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz')))])
    assert bars.ts.nunique() >= 0 and len(glob.glob(str(R13 / 'P13B_BARS_*.csv.gz'))) == 8, '8 lots requis'
    bars['ts'] = pd.to_datetime(bars.ts)
    bars = bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True)
    B = bars.set_index('ts')
    tick_frames = []
    for f in sorted(glob.glob(str(R13 / 'P13B_TICKS_*.csv'))):
        try:
            tf = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            continue
        if len(tf):
            tick_frames.append(tf)
    ticks = pd.concat(tick_frames)
    ticks['quote_timestamp'] = pd.to_datetime(ticks.quote_timestamp).dt.tz_localize(None)
    ticks = (ticks.sort_values('quote_timestamp')
             .drop_duplicates('event_id', keep='first').set_index('event_id'))

    d['expose'] = d.p_M1 > M0
    lignes = []
    for r in d.itertuples():
        L = {'event_id': r.event_id, 'grappe_id': r.grappe_id, 'famille': 'F10-01',
             'timeframe': 'H1', 'direction': int(r.direction),
             't_decision': str(r.t_decision), 'p_M1': float(r.p_M1),
             'decision_exposition': 'EXPOSITION' if r.expose else 'SANS_EXPOSITION',
             'statut_entree': '', 'timestamp_entree': '', 'prix_entree': np.nan,
             'cote_entree': '', 'statut_sortie': '', 'timestamp_sortie': '',
             'prix_sortie': np.nan, 'cote_sortie': '',
             'duree_exposition_min': np.nan, 'mfe_bp': np.nan, 'mae_bp': np.nan,
             'statut_completude': '', 'motif': ''}
        if not r.expose:
            L.update(statut_entree='SANS_EXPOSITION', statut_sortie='SANS_EXPOSITION',
                     statut_completude='NON_CONCERNE')
            lignes.append(L)
            continue
        if r.event_id not in ticks.index:
            L.update(statut_entree='NON_EXECUTION', statut_sortie='NON_EXECUTE',
                     statut_completude='NON_EXECUTE',
                     motif='AUCUN_TICK_DANS_FENETRE_60S')
            lignes.append(L)
            continue
        tk = ticks.loc[r.event_id]
        assert r.t_decision < tk.quote_timestamp < r.t_decision + pd.Timedelta(seconds=60)
        long = r.direction == 1
        entree = float(tk.ask if long else tk.bid)
        L.update(statut_entree='EXECUTE', timestamp_entree=str(tk.quote_timestamp),
                 prix_entree=entree, cote_entree='ASK' if long else 'BID')
        minute_sortie = r.fin_fenetre - pd.Timedelta(minutes=1)
        if minute_sortie not in B.index:
            L.update(statut_sortie='SORTIE_INDISPONIBLE', statut_completude='INCOMPLET',
                     motif='MINUTE_SORTIE_ABSENTE')
            lignes.append(L)
            continue
        bs = B.loc[minute_sortie]
        sortie = float(bs.bc if long else bs.ac)
        if not np.isfinite(sortie) or sortie <= 0 or not np.isfinite(bs.sp):
            L.update(statut_sortie='SORTIE_INDISPONIBLE', statut_completude='INCOMPLET',
                     motif='PRIX_OU_SPREAD_SORTIE_NON_FINI')
            lignes.append(L)
            continue
        L.update(statut_sortie='CLOTURE_FENETRE_8H', timestamp_sortie=str(bs.last_tick_ts),
                 prix_sortie=sortie, cote_sortie='BID' if long else 'ASK',
                 duree_exposition_min=float(
                     (pd.Timestamp(bs.last_tick_ts) - tk.quote_timestamp).total_seconds() / 60))
        # excursions aux prix de liquidation (barres M1 issues des ticks)
        chemin = B.loc[r.t_decision:minute_sortie]
        if len(chemin):
            if long:
                mfe = np.log(chemin.bh.max() / entree) * 10000
                mae = -np.log(chemin.bl.min() / entree) * 10000
            else:
                mfe = -np.log(chemin.al.min() / entree) * 10000
                mae = np.log(chemin.ah.max() / entree) * 10000
            L.update(mfe_bp=float(max(mfe, 0.0)), mae_bp=float(max(mae, 0.0)))
        for nom, s in SCEN.items():
            if long:
                pe, ps = entree * (1 + s / 10000), sortie * (1 - s / 10000)
            else:
                pe, ps = entree * (1 - s / 10000), sortie * (1 + s / 10000)
            L[f'resultat_{nom}_bp'] = float(r.direction * np.log(ps / pe) * 10000)
        L['statut_completude'] = 'COMPLET'
        lignes.append(L)
    E = pd.DataFrame(lignes)

    exposes = E[E.decision_exposition == 'EXPOSITION']
    executes = exposes[exposes.statut_entree == 'EXECUTE']
    complets = executes[executes.statut_completude == 'COMPLET']
    n_non_exec = int((exposes.statut_entree == 'NON_EXECUTION').sum())
    taux_non_exec = n_non_exec / len(exposes) if len(exposes) else np.nan
    # spreads non finis: minutes d'entree (barre de t_decision) et de sortie
    sp_tot, sp_nf = 0, 0
    for r in E[E.statut_sortie == 'CLOTURE_FENETRE_8H'].itertuples():
        m_out = pd.Timestamp(r.timestamp_sortie).floor('min')
        for m in (pd.Timestamp(r.t_decision), m_out):
            sp_tot += 1
            if m not in B.index or not np.isfinite(B.loc[m, 'sp']):
                sp_nf += 1
    taux_sp_nf = sp_nf / sp_tot if sp_tot else np.nan

    resultats = {'phase': '13-B', 'qualification': 'NIVEAU 2 - EXPLORATOIRE IS UNIQUEMENT',
                 'etiquette': 'NET_OF_SPREAD_BEFORE_COMMISSION_AND_SLIPPAGE',
                 'controle_reproduction_predictive_12B': ctrl,
                 'population': {'candidats_evaluation': int(len(E)),
                                'exposes_p_superieur_M0': int(len(exposes)),
                                'sans_exposition': int(len(E) - len(exposes)),
                                'executes': int(len(executes)),
                                'non_executions': n_non_exec,
                                'clotures_conformes': int(len(complets)),
                                'trajectoires_incompletes': int(len(executes) - len(complets))},
                 'taux_non_execution': {'numerateur': n_non_exec, 'denominateur': int(len(exposes)),
                                        'taux': float(taux_non_exec), 'seuil': 0.10},
                 'spreads_non_finis': {'numerateur': int(sp_nf), 'denominateur': int(sp_tot),
                                       'taux': float(taux_sp_nf), 'seuil': 0.05},
                 'scenarios': {}}
    for nom in SCEN:
        col = f'resultat_{nom}_bp'
        par_ev = stats_ret(complets[col].values)
        grappe = complets.groupby('grappe_id')[col].mean()
        par_gr = stats_ret(grappe.values)
        resultats['scenarios'][nom] = {'par_evenement': par_ev, 'par_grappe': par_gr,
                                      'mfe': stats_ret(complets.mfe_bp.values),
                                      'mae': stats_ret(complets.mae_bp.values),
                                      'duree_exposition_min': stats_ret(complets.duree_exposition_min.values)}
    # verdict selon grille seq331
    if taux_non_exec > 0.10 or taux_sp_nf > 0.05:
        verdict = 'NON_MESURABLE'
    else:
        pos = all(resultats['scenarios'][s]['par_evenement'].get('moyenne', 0) > 0 and
                  resultats['scenarios'][s]['par_grappe'].get('moyenne', 0) > 0 and
                  resultats['scenarios'][s]['par_evenement'].get('mediane', 0) > 0
                  for s in SCEN)
        neg = all(resultats['scenarios'][s]['par_evenement'].get('moyenne', 0) < 0 and
                  resultats['scenarios'][s]['par_grappe'].get('moyenne', 0) < 0
                  for s in SCEN)
        verdict = ('ECONOMICALLY_POSITIVE_EXPLORATORY_IS' if pos else
                   'ECONOMICALLY_NEGATIVE_EXPLORATORY_IS' if neg else
                   'ECONOMICALLY_INCONCLUSIVE_EXPLORATORY_IS')
    resultats['verdict'] = verdict

    E.to_csv(R13 / 'PHASE13B_EVENT_EXECUTIONS.csv', index=False)
    cov = pd.DataFrame([
        {'etape': 'DETECTES_F10_01_H1_REINTEGRES_TOUS_ENSEMBLES', 'effectif': 2695, 'motif': 'PHASE12B_RESULTS'},
        {'etape': 'CANDIDATS_EVALUATION_PRIMAIRE', 'effectif': int(len(E)), 'motif': 'F10-01 EVALUATION etiquetes 2018-2020, grappes entieres'},
        {'etape': 'SANS_EXPOSITION_P_INFERIEUR_M0', 'effectif': int(len(E) - len(exposes)), 'motif': 'conserves en couverture, aucune position'},
        {'etape': 'EXPOSES', 'effectif': int(len(exposes)), 'motif': 'p_M1 > 0,7591463414634146'},
        {'etape': 'EXECUTES', 'effectif': int(len(executes)), 'motif': 'premier tick dans (t_decision, +60 s)'},
        {'etape': 'NON_EXECUTION', 'effectif': n_non_exec, 'motif': 'AUCUN_TICK_DANS_FENETRE_60S'},
        {'etape': 'CLOTURES_CONFORMES', 'effectif': int(len(complets)), 'motif': 'Bid/Ask cloture derniere minute fenetre 8H'},
        {'etape': 'TRAJECTOIRES_INCOMPLETES', 'effectif': int(len(executes) - len(complets)), 'motif': 'minute/prix/spread de sortie indisponible'},
    ])
    cov.to_csv(R13 / 'PHASE13B_COVERAGE_AND_EXECUTION.csv', index=False)
    lignes_r = []
    for nom in SCEN:
        s = resultats['scenarios'][nom]
        for pond in ('par_evenement', 'par_grappe'):
            lignes_r.append({'famille': 'F10-01', 'timeframe': 'H1', 'scenario': nom,
                             'ponderation': pond, **s[pond],
                             'mfe_mediane': s['mfe'].get('mediane'), 'mfe_p95': s['mfe'].get('p95'),
                             'mae_mediane': s['mae'].get('mediane'), 'mae_p95': s['mae'].get('p95'),
                             'perte_maximale': s[pond].get('perte_maximale'),
                             'taux_non_execution': float(taux_non_exec),
                             'taux_spreads_non_finis': float(taux_sp_nf)})
    pd.DataFrame(lignes_r).to_csv(R13 / 'PHASE13B_RISK_METRICS.csv', index=False)
    (R13 / 'PHASE13B_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False))
    print(json.dumps({'verdict': verdict, 'population': resultats['population'],
                      'taux_non_execution': taux_non_exec, 'taux_spreads_nf': taux_sp_nf}, indent=1), flush=True)
    print('P13B analyse terminee', flush=True)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'analyse'
    if mode == 'lot':
        mode_lot()
    else:
        mode_analyse()
