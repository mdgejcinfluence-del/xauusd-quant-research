"""PHASE 12-C.2 - confirmation independante H1 sur holdout 2020-2026.
Autorisation seq318. Protocoles geles 12-A (580c39b1...) et 12-C.
Mode 'bars' (P12C2_ETAPE=bars): telecharge les partitions tick du lot
(P12C2_PARTS='debut-fin', identifiants Drive de l'inventaire deja
commite), agrege en barres M1 Mid/Bid/Ask par la requete historique
Phase 10, ecrit P12C2_BARS_<lot>.csv.gz. Les partitions 282-283
(2019-11/2020-01) servent uniquement de contexte au detecteur causal;
aucun evenement IS n'entre dans la population de confirmation.
Mode 'analyse': detection F10-01 par le detecteur historique cible
(evenements_tf, amendement seq289), clustering par la fonction
historique composantes (combine IS+holdout pour detecter les grappes
mixtes, sans nouveau clustering), anatomie par analyser_event gele
(Phase 11-C), variables bornees par features_bornees gele (Phase
12-B), modele gele charge depuis PHASE12C1_MODEL_PARAMETERS.json
(aucun reentrainement), M0 gele 0,7591463414634146. Evaluation
unique terminale, criteres 100/50 et verdicts du preenregistrement
12-C."""
import glob, hashlib, json, os, pathlib, subprocess, sys, time
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')

ROOT12 = pathlib.Path('reports/meta_alpha/phase12'); ROOT12.mkdir(parents=True, exist_ok=True)
FRONTIERE = pd.Timestamp('2020-01-01')
M0_GELE = 0.7591463414634146

def sha256_fichier(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# ---------------- mode bars ----------------
def mode_bars():
    import duckdb
    lot = os.environ.get('P12C2_LOT', 'lot')
    debut, fin = [int(x) for x in os.environ['P12C2_PARTS'].split('-')]
    inv = {p['name']: p for p in json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']}
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute("SET threads=2")
    frames, provenance = [], []
    for n in range(debut, fin + 1):
        nom = f'part_{n:06d}.parquet'; p = inv[nom]; local = f'/tmp/{nom}'
        ok = False
        for tentative in range(2):
            r = subprocess.run(['gdown', '-q', '--output', local, p['drive_id']])
            if r.returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == p['file_bytes']:
                ok = True; break
            print('P12C2 telechargement a reessayer', nom, tentative, flush=True); time.sleep(20 * (tentative + 1))
        if not ok: raise RuntimeError(f'telechargement Drive impossible: {nom}')
        h = sha256_fichier(local)
        q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts,
                arg_min(bid, timestamp_utc) AS bo, max(bid) AS bh, min(bid) AS bl, arg_max(bid, timestamp_utc) AS bc,
                arg_min(ask, timestamp_utc) AS ao, max(ask) AS ah, min(ask) AS al, arg_max(ask, timestamp_utc) AS ac,
                arg_min(mid, timestamp_utc) AS mo, max(mid) AS mh, min(mid) AS ml, arg_max(mid, timestamp_utc) AS mc,
                median((ask-bid)/mid)*10000 AS sp
                FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
        b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None)
        frames.append(b); provenance.append({'partition': nom, 'sha256': h, 'octets': p['file_bytes'], 'barres_m1': int(len(b))})
        pathlib.Path(local).unlink()
        print('P12C2', lot, nom, len(b), 'barres M1', flush=True)
    bars = pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)
    bars.round(6).to_csv(ROOT12 / f'P12C2_BARS_{lot}.csv.gz', index=False, compression='gzip')
    (ROOT12 / f'P12C2_PROVENANCE_{lot}.json').write_text(json.dumps(
        {'lot': lot, 'partitions': provenance, 'barres_m1_total': int(len(bars))}, indent=1))
    print(json.dumps({'lot': lot, 'partitions': len(provenance), 'barres_m1': int(len(bars))}), flush=True)

# ---------------- mode analyse ----------------
def charger_barres():
    dossier = os.environ.get('BARS_DIR', 'bars_artifacts')
    fs = sorted(glob.glob(f'{dossier}/**/P12C2_BARS_*.csv.gz', recursive=True))
    if len(fs) < 8: raise RuntimeError(f'integrite lots: {len(fs)}/8 fichiers de barres')
    bars = pd.concat([pd.read_csv(f) for f in fs])
    bars['ts'] = pd.to_datetime(bars.ts)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True), len(fs)

def mode_analyse():
    from phase10_engine import construire_barres, evenements_tf
    from phase10_synthesize import composantes
    from phase11c_engine import analyser_event
    from phase12b_engine import features_bornees, metriques, calibration, session_de
    params = json.load(open(ROOT12 / 'PHASE12C1_MODEL_PARAMETERS.json'))
    assert sha256_fichier(ROOT12 / 'PHASE12C1_MODEL_PARAMETERS.json') == '1bcb3b706b74fbbd013f6aa7b6c4bccc0580f30a40ef88d8dc2682144c80956e'
    coef = params['coefficients']; intercept = float(params['intercept'])
    bars, nb_lots = charger_barres()
    tf = construire_barres(bars, 60)
    ev_liste, diag = evenements_tf(tf, 'H1', 60, cible=True)
    EV = pd.DataFrame(ev_liste)
    EV['t_signal_ts'] = pd.to_datetime(EV.t_signal)
    detectes_total = len(EV)
    contexte = EV[EV.t_signal_ts < FRONTIERE]
    HO = EV[EV.t_signal_ts >= FRONTIERE].copy()
    adm_mask = (HO.entree_eligible == 1) & (HO.fenetre_complete == 1)
    # clustering combine IS + holdout admissibles (methode historique, aucun nouvel algorithme)
    IS = pd.read_csv('reports/meta_alpha/phase10/PHASE10_EVENTS_CIBLE.csv.gz')
    IS = IS[(IS.famille == 'F10-01') & (IS.entree_eligible == 1) & (IS.fenetre_complete == 1)]
    ho_adm = HO[adm_mask].copy()
    ts0 = np.concatenate([pd.to_datetime(IS.t_signal).values.astype('datetime64[ns]').astype('int64'),
                          pd.to_datetime(ho_adm.t_signal).values.astype('datetime64[ns]').astype('int64')])
    ts1 = np.concatenate([pd.to_datetime(IS.t_sortie).values.astype('datetime64[ns]').astype('int64'),
                          pd.to_datetime(ho_adm.t_sortie).values.astype('datetime64[ns]').astype('int64')])
    g = composantes(ts0, ts1)
    g_is, g_ho = g[:len(IS)], g[len(IS):]
    grappes_mixtes = set(g_is.tolist())
    M = (bars.ts.values.astype('datetime64[ns]').astype('int64') // 60_000_000_000,
         bars.mo.values, bars.mh.values, bars.ml.values, bars.mc.values)
    ts_min, mo, mh, ml, mc = M
    fin_index = {pd.Timestamp(f): i for i, f in enumerate(tf.fin)}
    lignes, exclusions = [], {'CONTEXTE_AVANT_FRONTIERE': int(len(contexte)), 'NON_ADMISSIBLE': int(len(HO) - len(ho_adm)),
                              'GRAPPE_MIXTE_IS_HOLDOUT': 0, 'NON_REINTEGRE': 0, 'CENSORED': 0, 'AMBIGUOUS': 0}
    for k, (_, row) in enumerate(ho_adm.iterrows()):
        eid = 'EV-' + hashlib.sha256(f"F10-01|H1|{row.t_signal}|{int(row.sens):+d}".encode()).hexdigest()
        gid = f'GR-F10-01-HO-{int(g_ho[k]) + 1:05d}'
        base = {'event_id': eid, 'grappe_id': gid, 'timeframe': 'H1', 'famille': 'F10-01', 't0': row.t_signal,
                'direction': int(row.sens), 'periode': 'HOLDOUT_2020+'}
        if int(g_ho[k]) in grappes_mixtes:
            exclusions['GRAPPE_MIXTE_IS_HOLDOUT'] += 1
            lignes.append(base | {'statut_admissibilite': 'EXCLU', 'motif_exclusion': 'GRAPPE_MIXTE_IS_HOLDOUT',
                                  'cible_statut': 'EXCLU', 'RESUMPTION': None, 't_reintegration': None}); continue
        trig_idx = fin_index.get(pd.Timestamp(row.t_signal))
        R = analyser_event(row, tf, trig_idx, M, 60)
        if not R.get('reintegration_confirmee'):
            exclusions['NON_REINTEGRE'] += 1
            lignes.append(base | {'statut_admissibilite': 'ADMISSIBLE', 'motif_exclusion': 'NON_REINTEGRE_HORS_POPULATION_CONDITIONNELLE',
                                  'cible_statut': 'NON_REINTEGRE', 'RESUMPTION': None, 't_reintegration': None,
                                  'horizon_atteint': R.get('horizon_atteint')}); continue
        minute_reint = pd.Timestamp(R['reintegration_minute_start_utc']); t0 = pd.Timestamp(row.t_signal)
        t0min = int(t0.value // 60_000_000_000); mr_min = int(minute_reint.value // 60_000_000_000)
        i0 = int(np.searchsorted(ts_min, t0min)); i1 = int(np.searchsorted(ts_min, mr_min, side='right'))
        F = features_bornees(int(row.sens), mh[i0:i1], ml[i0:i1], mc[i0:i1], ts_min[i0:i1], float(R['P0']), i1 - i0 - 1)
        if R['horizon_atteint'] < 8: statut, res = 'CENSORED', None; exclusions['CENSORED'] += 1
        elif int(R['intra_minute_order_unknown']) == 1: statut, res = 'AMBIGUOUS', None; exclusions['AMBIGUOUS'] += 1
        else: res = int(R['reprise_apres_reintegration']); statut = f'RESUMPTION_{res}'
        lignes.append(base | {'statut_admissibilite': 'ADMISSIBLE', 'motif_exclusion': '' if res is not None else statut,
                              'cible_statut': statut, 'RESUMPTION': res,
                              't_reintegration': str(minute_reint + pd.Timedelta(minutes=1)),
                              'RATIO_REPLI_EXTENSION_A_TREINT': F['RATIO_REPLI_EXTENSION_A_TREINT'],
                              'DUREE_EXTREME_VERS_TREINT_MIN': F['DUREE_EXTREME_VERS_TREINT_MIN'],
                              'MFE_A_TREINT_BP': F['MFE_A_TREINT_BP'],
                              'NB_TOUCHES_P0_AVANT_TREINT': F['NB_TOUCHES_P0_AVANT_TREINT'],
                              'SESSION_REINTEGRATION': session_de(minute_reint.hour),
                              'borne_max_minute_utilisee': str(minute_reint), 'horizon_atteint': R['horizon_atteint']})
    F = pd.DataFrame(lignes)
    F.to_csv(ROOT12 / 'PHASE12C2_HOLDOUT_FEATURES.csv', index=False)
    etiq = F[F.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1'])].copy()
    def proba(r):
        z = intercept + sum(coef[c] * float(r[c]) for c in
              ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN', 'MFE_A_TREINT_BP', 'NB_TOUCHES_P0_AVANT_TREINT']) \
            + sum(coef[f'SESSION_REINTEGRATION={s}'] * (1.0 if r.SESSION_REINTEGRATION == s else 0.0)
                  for s in ['LONDON', 'LONDON_NY_OVERLAP', 'NY_AFTERNOON', 'NIGHT_OTHER'])
        return float(1 / (1 + np.exp(-np.clip(z, -35, 35))))
    if len(etiq):
        etiq['probabilite_M1'] = [proba(r) for _, r in etiq.iterrows()]
        etiq['probabilite_M0'] = M0_GELE
    P = etiq[['event_id', 'grappe_id', 'probabilite_M0', 'probabilite_M1', 'RESUMPTION', 'cible_statut', 't_reintegration']].rename(
        columns={'RESUMPTION': 'cible', 'cible_statut': 'statut'}) if len(etiq) else pd.DataFrame()
    if len(P): P['provenance'] = 'PHASE12C1_MODEL_PARAMETERS.json (seq317); M0 gele seq12-B'
    P.to_csv(ROOT12 / 'PHASE12C2_HOLDOUT_PREDICTIONS.csv', index=False)
    audit = {'variables': {v: {'borne_temporelle_verifiee': 'minutes <= minute de reintegration incluse (features_bornees gele, tronquee a i_reint)',
                               'statut_anti_fuite': 'BORNE_VERIFIEE',
                               'taux_valeurs_manquantes_parmi_reintegres': float(F[v].isna().mean()) if v in F else None}
                           for v in ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN', 'MFE_A_TREINT_BP', 'NB_TOUCHES_P0_AVANT_TREINT', 'SESSION_REINTEGRATION']},
             'controles': {'modele_gele_charge_depuis': 'PHASE12C1_MODEL_PARAMETERS.json sha256 verifie par assertion',
                           'reentrainement': 'AUCUN', 'M0': M0_GELE, 'M0_recalcule_sur_holdout': 'JAMAIS',
                           'colonnes_fenetre_complete_dans_predicteurs': 'AUCUNE', 'grappes_mixtes_exclues': exclusions['GRAPPE_MIXTE_IS_HOLDOUT'],
                           'evaluation_unique_terminale': True},
             'anomalies': []}
    (ROOT12 / 'PHASE12C2_FEATURE_AUDIT.json').write_text(json.dumps(audit, indent=1, ensure_ascii=False))
    n_ev = len(etiq); n1 = int(etiq.RESUMPTION.sum()) if n_ev else 0; mino = min(n1, n_ev - n1) if n_ev else 0
    resultat = {'phase': '12-C.2', 'qualification': 'CONFIRMATION HISTORIQUE HORS IS - NON VALIDATION PROSPECTIVE',
                'detectes_holdout_bruts': int(len(HO)), 'detectes_contexte_avant_frontiere': int(len(contexte)),
                'admissibles_holdout': int(len(ho_adm)), 'exclusions': exclusions,
                'reintegres_etiquetes': n_ev, 'classe1': n1, 'classe0': n_ev - n1,
                'criteres_evaluabilite': {'n_min': 100, 'minorite_min': 50, 'satisfaits': bool(n_ev >= 100 and mino >= 50)},
                'diagnostic_detecteur': diag, 'lots_barres': nb_lots,
                'couverture_barres_m1': {'debut': str(bars.ts.iloc[0]), 'fin': str(bars.ts.iloc[-1]), 'barres': int(len(bars))}}
    if n_ev >= 100 and mino >= 50:
        m0 = metriques(etiq.RESUMPTION.values, etiq.probabilite_M0.values)
        m1 = metriques(etiq.RESUMPTION.values, etiq.probabilite_M1.values)
        cal = calibration(etiq.RESUMPTION.values, etiq.probabilite_M1.values) if n_ev >= 200 else None
        ameliore = m1['brier'] < m0['brier'] and m1['log_loss'] < m0['log_loss']
        resultat |= {'M0': m0, 'M1': m1, 'delta_brier_M1_moins_M0': m1['brier'] - m0['brier'],
                     'delta_log_loss_M1_moins_M0': m1['log_loss'] - m0['log_loss'],
                     'calibration_M1': cal, 'distribution_probabilites_M1': {
                         'min': float(etiq.probabilite_M1.min()), 'p25': float(etiq.probabilite_M1.quantile(.25)),
                         'mediane': float(etiq.probabilite_M1.median()), 'p75': float(etiq.probabilite_M1.quantile(.75)), 'max': float(etiq.probabilite_M1.max())},
                     'verdict': 'CONFIRMED_HISTORICAL_HOLDOUT' if ameliore else 'NO_PREDICTIVE_IMPROVEMENT_HOLDOUT'}
    else:
        resultat['verdict'] = 'NON_EVALUABLE'
    (ROOT12 / 'PHASE12C2_EVALUATION.json').write_text(json.dumps(resultat, indent=1, ensure_ascii=False, default=str))
    print(json.dumps(resultat, indent=1, ensure_ascii=False, default=str)[:5000], flush=True)

if __name__ == '__main__':
    if os.environ.get('P12C2_ETAPE') == 'bars': mode_bars()
    else: mode_analyse()
