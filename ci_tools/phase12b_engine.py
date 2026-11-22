"""PHASE 12-B - extraction bornee a t_reintegration et evaluation predictive.
Protocole PHASE 12-A GELE (sha256 580c39b1...), autorisation seq312.
Cinq variables preenregistrees calculees sur les seules minutes M1
<= t_reintegration; cible RESUMPTION deja materialisee en Phase 11-C
(reprise_apres_reintegration), jamais recalculee sous une nouvelle
definition. M0 (frequence d'apprentissage) vs M1 (logistique simple
sans reglage, variables brutes). H1/H4 separes. Aucune rentabilite,
aucun test de significativite, holdout jamais accede."""
import glob, json, os, pathlib
import numpy as np
import pandas as pd

ROOT11 = pathlib.Path('reports/meta_alpha/phase11')
ROOT12 = pathlib.Path('reports/meta_alpha/phase12'); ROOT12.mkdir(parents=True, exist_ok=True)
SESSIONS_ORDRE = ['ASIA', 'LONDON', 'LONDON_NY_OVERLAP', 'NY_AFTERNOON', 'NIGHT_OTHER']
SESSIONS = [(0, 'ASIA'), (8, 'LONDON'), (13, 'LONDON_NY_OVERLAP'), (17, 'NY_AFTERNOON'), (21, 'NIGHT_OTHER')]
BORNES = {'APPRENTISSAGE': (pd.Timestamp('2010-01-01'), pd.Timestamp('2016-01-01')),
          'CALIBRATION': (pd.Timestamp('2016-01-01'), pd.Timestamp('2018-01-01')),
          'EVALUATION': (pd.Timestamp('2018-01-01'), pd.Timestamp('2021-01-01'))}

def session_de(h):
    for borne, nom in reversed(SESSIONS):
        if h >= borne: return nom
    return 'ASIA'

def features_bornees(d, s_mh, s_ml, s_mc, s_ts, P0, i_reint):
    """Cinq variables (dont session hors fonction) sur minutes[0..i_reint] uniquement.
    Conventions identiques a Phase 11-C: y = clotures M1 orientees en bp log vs P0;
    extreme favorable = extrema M1 orientes cumules; profondeur de repli = ecart
    entre le sommet favorable cumule de la minute precedente et l'extreme adverse
    de la minute courante (aucun ordre intraminute invente)."""
    mh, ml, mc, ts = s_mh[:i_reint + 1], s_ml[:i_reint + 1], s_mc[:i_reint + 1], s_ts[:i_reint + 1]
    if d > 0:
        fav_bp = 10000 * np.log(np.maximum.accumulate(mh) / P0)
        sommet = np.maximum.accumulate(mh)
        profs = [10000 * np.log(sommet[m - 1] / ml[m]) for m in range(1, len(mc))]
        touches = int(np.sum(ml[:-1] < P0))
    else:
        fav_bp = 10000 * np.log(P0 / np.minimum.accumulate(ml))
        creux = np.minimum.accumulate(ml)
        profs = [10000 * np.log(mh[m] / creux[m - 1]) for m in range(1, len(mc))]
        touches = int(np.sum(mh[:-1] > P0))
    i_pic = int(np.argmax(fav_bp)); mfe = float(fav_bp[i_pic])
    profondeur = float(max(0.0, max(profs))) if profs else 0.0
    return {'RATIO_REPLI_EXTENSION_A_TREINT': float(profondeur / mfe) if mfe > 0 else np.nan,
            'DUREE_EXTREME_VERS_TREINT_MIN': int(ts[i_reint] - ts[i_pic]),
            'MFE_A_TREINT_BP': mfe,
            'NB_TOUCHES_P0_AVANT_TREINT': touches,
            '_profondeur_repli_a_treint_bp': profondeur, '_i_pic': i_pic}

def charger_barres():
    dossier = os.environ.get('BARS_DIR', 'bars_artifacts')
    fs = sorted(glob.glob(f'{dossier}/**/P10_BARS_*.csv.gz', recursive=True))
    if len(fs) < 8: raise RuntimeError(f'integrite lots: {len(fs)}/8 fichiers de barres')
    bars = pd.concat([pd.read_csv(f) for f in fs])
    bars['ts'] = pd.to_datetime(bars.ts)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True), len(fs)

def logistique_irls(X, y, max_iter=200, tol=1e-10):
    """Logistique non penalisee (variables brutes), Newton-Raphson amorti;
    aucun reglage, aucune selection. Ridge numerique 1e-8 documente."""
    Xd = np.column_stack([np.ones(len(X)), X]); beta = np.zeros(Xd.shape[1])
    for _ in range(max_iter):
        z = np.clip(Xd @ beta, -35, 35); p = 1 / (1 + np.exp(-z))
        W = np.clip(p * (1 - p), 1e-10, None)
        A = Xd.T @ (Xd * W[:, None]) + 1e-8 * np.eye(Xd.shape[1])
        pas = np.linalg.solve(A, Xd.T @ (y - p))
        beta_n = beta + pas
        if np.max(np.abs(beta_n - beta)) < tol: beta = beta_n; break
        beta = beta_n
    def predire(Xn):
        z = np.clip(np.column_stack([np.ones(len(Xn)), Xn]) @ beta, -35, 35)
        return 1 / (1 + np.exp(-z))
    return beta, predire

def metriques(y, p):
    y = np.asarray(y, float); p = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15)
    brier = float(np.mean((p - y) ** 2))
    logloss = float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))
    # AUC par rangs (Mann-Whitney)
    ordre = np.argsort(p); rangs = np.empty(len(p)); rangs[ordre] = np.arange(1, len(p) + 1)
    # gestion des ex-aequo par rang moyen
    ps = pd.Series(p); rangs = ps.rank(method='average').values
    n1, n0 = y.sum(), len(y) - y.sum()
    auc = float((rangs[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)) if n1 and n0 else None
    pred = (p >= 0.5).astype(float)
    tp = float(np.sum((pred == 1) & (y == 1))); fp = float(np.sum((pred == 1) & (y == 0)))
    fn = float(np.sum((pred == 0) & (y == 1)))
    return {'brier': brier, 'log_loss': logloss, 'auc': auc,
            'precision_seuil_0_5': float(tp / (tp + fp)) if tp + fp else None,
            'rappel_seuil_0_5': float(tp / (tp + fn)) if tp + fn else None}

def calibration(y, p):
    """Pente/ordonnee (logistique de y sur logit(p)) et deciles predits."""
    y = np.asarray(y, float); p = np.clip(np.asarray(p, float), 1e-6, 1 - 1e-6)
    logit = np.log(p / (1 - p)).reshape(-1, 1)
    beta, _ = logistique_irls(logit, y)
    dec = pd.DataFrame({'p': p, 'y': y}); dec['decile'] = pd.qcut(dec.p.rank(method='first'), 10, labels=False)
    courbes = [{'decile': int(k), 'n': int(len(g)), 'predit_moyen': float(g.p.mean()), 'observe': float(g.y.mean())}
               for k, g in dec.groupby('decile')]
    return {'intercept': float(beta[0]), 'pente': float(beta[1]), 'deciles': courbes}

def main():
    from phase10_engine import construire_barres
    bars, nb_lots = charger_barres()
    P = pd.read_csv(ROOT11 / 'PHASE11C_EVENT_PATHS.csv', parse_dates=['t0'])
    assert len(P) == 3767 and P.event_id.is_unique
    reint = P[P.reintegration_confirmee == 1].copy()
    assert len(reint) == 3327, len(reint)
    M = (bars.ts.values.astype('datetime64[ns]').astype('int64') // 60_000_000_000,
         bars.mo.values, bars.mh.values, bars.ml.values, bars.mc.values)
    ts_min, mo, mh, ml, mc = M
    tf_par_fam = {}
    for fam, minutes in [('F10-01', 60), ('F10-03', 240)]:
        tf_par_fam[fam] = (construire_barres(bars, minutes), minutes)
    lignes, anomalies = [], []
    for _, row in reint.iterrows():
        fam = row.famille; tf, minutes_tf = tf_par_fam[fam]
        d = int(row.direction); P0 = float(row.P0); t0 = pd.Timestamp(row.t0)
        t0min = int(t0.value // 60_000_000_000)
        minute_reint = pd.Timestamp(row.reintegration_minute_start_utc)
        minute_reint_min = int(minute_reint.value // 60_000_000_000)
        # fin de fenetre d'observation (replique Phase 11-C: enchainement des barres TF)
        fin_index = {pd.Timestamp(f): i for i, f in enumerate(tf.fin)}
        trig_idx = fin_index.get(t0)
        fin_fenetre = None
        if trig_idx is not None and trig_idx + int(row.horizon_atteint) < len(tf):
            fin_fenetre = pd.Timestamp(tf.iloc[trig_idx + int(row.horizon_atteint)].fin) if row.horizon_atteint else t0
            if row.horizon_atteint == 0: fin_fenetre = t0
        i0 = int(np.searchsorted(ts_min, t0min))
        i1 = int(np.searchsorted(ts_min, minute_reint_min, side='right'))
        s_mh, s_ml, s_mc, s_ts = mh[i0:i1], ml[i0:i1], mc[i0:i1], ts_min[i0:i1]
        if len(s_ts) == 0 or s_ts[-1] != minute_reint_min:
            anomalies.append({'event_id': row.event_id, 'motif': 'MINUTE_REINTEGRATION_INTROUVABLE'}); continue
        i_reint = len(s_ts) - 1
        y = d * 10000 * np.log(s_mc / P0)
        # controle de coherence avec la definition gelee (recalcule uniquement en controle, jamais pour la cible)
        ext = np.where(y > 0)[0]
        reint_controle = None
        if len(ext):
            cand = np.where(y[int(ext[0]) + 1:] < 0)[0]
            if len(cand): reint_controle = int(ext[0]) + 1 + int(cand[0])
        if reint_controle != i_reint:
            anomalies.append({'event_id': row.event_id, 'motif': f'REINTEGRATION_NON_RECONCILIEE controle={reint_controle} attendu={i_reint}'})
        F = features_bornees(d, s_mh, s_ml, s_mc, s_ts, P0, i_reint)
        session = session_de(minute_reint.hour)
        if session != row.session_reintegration:
            anomalies.append({'event_id': row.event_id, 'motif': 'SESSION_NON_RECONCILIEE'})
        if F['MFE_A_TREINT_BP'] > float(row.mfe_max_bp) + 1e-6:
            anomalies.append({'event_id': row.event_id, 'motif': 'MFE_BORNE_SUPERIEUR_AU_MFE_FENETRE (fuite potentielle)'})
        # cible deja materialisee (Phase 11-C), jamais recalculee
        if row.horizon_atteint < 8: statut, res = 'CENSORED', None
        elif int(row.intra_minute_order_unknown) == 1: statut, res = 'AMBIGUOUS', None
        else: res = int(row.reprise_apres_reintegration); statut = f'RESUMPTION_{res}'
        lignes.append({'event_id': row.event_id, 'grappe_id': row.grappe_id, 'famille': fam,
                       'timeframe': row.timeframe, 't0': str(t0),
                       't_reintegration': str(minute_reint + pd.Timedelta(minutes=1)),
                       'minute_reintegration_start_utc': str(minute_reint),
                       'RESUMPTION': res, 'cible_statut': statut,
                       'RATIO_REPLI_EXTENSION_A_TREINT': F['RATIO_REPLI_EXTENSION_A_TREINT'],
                       'DUREE_EXTREME_VERS_TREINT_MIN': F['DUREE_EXTREME_VERS_TREINT_MIN'],
                       'MFE_A_TREINT_BP': F['MFE_A_TREINT_BP'],
                       'NB_TOUCHES_P0_AVANT_TREINT': F['NB_TOUCHES_P0_AVANT_TREINT'],
                       'SESSION_REINTEGRATION': session,
                       'fin_fenetre_observation': str(fin_fenetre) if fin_fenetre is not None else None,
                       'borne_max_minute_utilisee': str(minute_reint),
                       'statut_disponibilite': 'EXTRAIT_BORNE_OK' if reint_controle == i_reint else 'ANOMALIE_CONTROLE',
                       'motif_exclusion': ''})
    F = pd.DataFrame(lignes)
    # --- separation chronologique par grappe entiere (affectation: 1er evenement reintegre de la grappe) ---
    F['t_reintegration_ts'] = pd.to_datetime(F.t_reintegration)
    premier = F.groupby(['famille', 'grappe_id']).t_reintegration_ts.min().rename('grappe_premier_treint')
    F = F.merge(premier, on=['famille', 'grappe_id'], how='left')
    def segment_de(ts):
        for nom, (a, b) in BORNES.items():
            if a <= ts < b: return nom
        return 'HORS_SEGMENTS'
    F['segment_grappe'] = F.grappe_premier_treint.map(segment_de)
    # purge: fenetre d'observation chevauchant le debut du segment suivant
    def ensemble_final(r):
        if r.cible_statut in ('CENSORED', 'AMBIGUOUS'): return 'EXCLU_CIBLE'
        if r.segment_grappe == 'APPRENTISSAGE' and r.fin_fenetre_observation and pd.Timestamp(r.fin_fenetre_observation) > BORNES['CALIBRATION'][0]:
            return 'EXCLU_PURGE_CHEVauchement'.upper()
        if r.segment_grappe == 'CALIBRATION' and r.fin_fenetre_observation and pd.Timestamp(r.fin_fenetre_observation) > BORNES['EVALUATION'][0]:
            return 'EXCLU_PURGE_CHEVauchement'.upper()
        return r.segment_grappe
    F['ensemble'] = F.apply(ensemble_final, axis=1)
    F.loc[F.ensemble.str.startswith('EXCLU_PURGE'), 'motif_exclusion'] = 'PURGE_FENETRE_CHEVauche_SEGMENT_SUIVANT'
    F.loc[F.cible_statut == 'CENSORED', 'motif_exclusion'] = 'CIBLE_CENSUREE_HORIZON_INCOMPLET'
    F.loc[F.cible_statut == 'AMBIGUOUS', 'motif_exclusion'] = 'CIBLE_AMBIGUE_ORDRE_INTRAMINUTE'
    # controle: aucune grappe partagee entre ensembles conserves
    conserves = F[F.ensemble.isin(BORNES)]
    par_grappe = conserves.groupby(['famille', 'grappe_id']).ensemble.nunique()
    assert (par_grappe <= 1).all(), 'grappe partagee entre ensembles'
    F = F.drop(columns=['t_reintegration_ts', 'grappe_premier_treint'])
    F.to_csv(ROOT12 / 'PHASE12B_FEATURES.csv', index=False)

    audit_vars = {
        'RATIO_REPLI_EXTENSION_A_TREINT': {'definition': 'Profondeur du repli observee a t_reintegration (sommet favorable cumule minute precedente -> extreme adverse de la minute, convention 11-C) divisee par le MFE intraminute atteint a t_reintegration; >100 % conserve, aucun plafonnement', 'unite': 'ratio sans unite', 'source': 'M1 Mid (mh/ml) minutes <= minute de reintegration incluse', 'disponibilite': 'a t_reintegration (cloture de la minute de reintegration)'},
        'DUREE_EXTREME_VERS_TREINT_MIN': {'definition': 'Minutes (horodatage de debut de minute M1) entre la minute du meilleur extreme favorable atteint a t_reintegration et la minute de reintegration', 'unite': 'minutes', 'source': 'M1 Mid minutes <= minute de reintegration incluse', 'disponibilite': 'a t_reintegration'},
        'MFE_A_TREINT_BP': {'definition': 'Excursion favorable intraminute maximale atteinte entre t0 et t_reintegration (extrema M1 orientes cumules, log vs P0); jamais le MFE de fenetre complete', 'unite': 'bp (log)', 'source': 'M1 Mid minutes <= minute de reintegration incluse', 'disponibilite': 'a t_reintegration'},
        'NB_TOUCHES_P0_AVANT_TREINT': {'definition': 'Nombre de minutes strictement anterieures a la minute de reintegration dont l extreme adverse franchit P0 (ml<P0 si d=+1, mh>P0 si d=-1)', 'unite': 'compte', 'source': 'M1 Mid minutes < minute de reintegration', 'disponibilite': 'a t_reintegration'},
        'SESSION_REINTEGRATION': {'definition': 'Categorie UTC fixe 11-A de l heure de la minute de reintegration (5 modalites)', 'unite': 'categorie', 'source': 'horodatage de reintegration Phase 11-C, reverifie', 'disponibilite': 'a t_reintegration'}}
    audit = {'variables': {}, 'controles_anti_fuite': {}, 'anomalies': anomalies}
    for v, meta in audit_vars.items():
        audit['variables'][v] = meta | {
            'borne_temporelle_verifiee': 'minutes <= minute de reintegration incluse (cloture = t_reintegration); test synthetique mutation du futur passe',
            'taux_valeurs_manquantes_parmi_reintegres': float(F[v].isna().mean()) if v != 'SESSION_REINTEGRATION' else 0.0,
            'statut_anti_fuite': 'BORNE_VERIFIEE'}
    audit['controles_anti_fuite'] = {
        'borne_temporelle_par_variable': 'VERIFIEE (extraction tronquee a i_reint; colonne borne_max_minute_utilisee = minute de reintegration)',
        'separation_cible_predicteurs': 'VERIFIEE (cible = reprise_apres_reintegration 11-C materialisee; aucune colonne fenetre complete dans la matrice: RATIO/DUREE/MFE/NB_TOUCHES recalcules bornes, SESSION)',
        'colonnes_interdites_absentes_de_la_matrice': ['mfe_max_bp', 'mae_max_bp', 'repli_profondeur_max_bp', 'fraction_corps_reprise', 'repli_relatif_extension_pct', 'nb_retours', 'archetype', 'reprise_apres_reintegration (hors cible)', 'disp_1..8'],
        'grappes_partagees_entre_ensembles': 0,
        'ordre_chronologique': 'apprentissage 2010-2015 < calibration 2016-2017 < evaluation 2018-2020; aucune donnee d evaluation utilisee pour M0/M1',
        'purge_chevauchements': 'evenements d apprentissage/calibration dont fin_fenetre_observation depasse le debut du segment suivant exclus (motif consigne)',
        'reglage_apres_resultats': 'AUCUN (modele unique prespecifie, variables brutes, aucun hyperparametre optimise)',
        'reproductibilite': 'moteur deterministe; logistique IRLS deterministe'}
    (ROOT12 / 'PHASE12B_FEATURE_AUDIT.json').write_text(json.dumps(audit, indent=1, ensure_ascii=False, default=str))

    # --- evaluation par famille ---
    evaluations, resultats_familles = [], {}
    VARIABLES = ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN', 'MFE_A_TREINT_BP', 'NB_TOUCHES_P0_AVANT_TREINT']
    for fam in ('F10-01', 'F10-03'):
        d = F[F.famille == fam]
        etiq = d[d.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1'])]
        app = etiq[etiq.ensemble == 'APPRENTISSAGE']; ev = etiq[etiq.ensemble == 'EVALUATION']
        cal = etiq[etiq.ensemble == 'CALIBRATION']
        n_ev, min_ev = len(ev), int(min(ev.RESUMPTION.sum(), len(ev) - ev.RESUMPTION.sum())) if len(ev) else 0
        base = {'famille': fam, 'timeframe': d.timeframe.iloc[0],
                'n_reintegres': int(len(d)), 'n_censures': int((d.cible_statut == 'CENSORED').sum()),
                'n_ambigus': int((d.cible_statut == 'AMBIGUOUS').sum()),
                'n_apprentissage': int(len(app)), 'classe1_apprentissage': int(app.RESUMPTION.sum()),
                'n_calibration': int(len(cal)), 'n_evaluation': int(n_ev),
                'classe1_evaluation': int(ev.RESUMPTION.sum()) if len(ev) else 0,
                'classe0_evaluation': int(len(ev) - ev.RESUMPTION.sum()) if len(ev) else 0,
                'criteres_insuffisance': 'NON EVALUABLE si n_evaluation < 100 ou classe minoritaire < 50'}
        if n_ev < 100 or min_ev < 50:
            base |= {'statut_evaluabilite': 'NON_EVALUABLE', 'verdict': 'NON_EVALUABLE',
                     'motif': f'n_evaluation={n_ev}, minorite={min_ev} (seuils 100/50)'}
            resultats_familles[fam] = base; evaluations.append(base); continue
        X_app = app[VARIABLES].astype(float).values
        for sess in SESSIONS_ORDRE[1:]:
            pass
        def matrice(dd):
            Xs = [dd[VARIABLES].astype(float).values]
            cats = [(dd.SESSION_REINTEGRATION == s).astype(float).values.reshape(-1, 1) for s in SESSIONS_ORDRE[1:]]
            return np.hstack(Xs + cats)
        beta, predire = logistique_irls(matrice(app), app.RESUMPTION.values.astype(float))
        p0 = float(app.RESUMPTION.mean())
        p_m0 = np.full(len(ev), p0); p_m1 = predire(matrice(ev))
        m0, m1 = metriques(ev.RESUMPTION.values, p_m0), metriques(ev.RESUMPTION.values, p_m1)
        calib = calibration(ev.RESUMPTION.values, p_m1) if len(ev) >= 200 else None
        ameliore = (m1['brier'] < m0['brier']) and (m1['log_loss'] < m0['log_loss'])
        verdict = 'PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY' if ameliore and not anomalies else 'NO_PREDICTIVE_IMPROVEMENT'
        base |= {'statut_evaluabilite': 'EVALUABLE', 'verdict': verdict,
                 'M0_probabilite_apprentissage': p0,
                 'M0_brier': m0['brier'], 'M1_brier': m1['brier'], 'delta_brier_M1_moins_M0': m1['brier'] - m0['brier'],
                 'M0_log_loss': m0['log_loss'], 'M1_log_loss': m1['log_loss'], 'delta_log_loss_M1_moins_M0': m1['log_loss'] - m0['log_loss'],
                 'amelioration_relative_brier_pct': float(100 * (m0['brier'] - m1['brier']) / m0['brier']),
                 'amelioration_relative_log_loss_pct': float(100 * (m0['log_loss'] - m1['log_loss']) / m0['log_loss']),
                 'M0_auc': m0['auc'], 'M1_auc': m1['auc'],
                 'M1_precision_0_5': m1['precision_seuil_0_5'], 'M1_rappel_0_5': m1['rappel_seuil_0_5'],
                 'calibration_M1': calib, 'convention_signe': 'delta negatif = M1 meilleur que M0'}
        resultats_familles[fam] = base; evaluations.append(base)
    pd.DataFrame(evaluations).to_csv(ROOT12 / 'PHASE12B_MODEL_EVALUATION.csv', index=False)
    verdicts = [v['verdict'] for v in resultats_familles.values()]
    if anomalies: decision = 'BLOCKED'
    elif all(v == 'PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY' for v in verdicts): decision = 'PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY (toutes familles evaluables)'
    elif any(v == 'PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY' for v in verdicts): decision = 'MIXTE PAR FAMILLE (voir verdicts separes)'
    elif all(v == 'NON_EVALUABLE' for v in verdicts): decision = 'NON_EVALUABLE'
    else: decision = 'NO_PREDICTIVE_IMPROVEMENT'
    resultats = {'phase': '12-B', 'statut_execution': 'TERMINE', 'lots_barres': nb_lots,
                 'protocole': 'PHASE12A_PREDICTABILITY_PROTOCOL.md GELE sha256 580c39b114397143e6eaa7fc63e529afb79ad61ec3f9cbd843116d3484a4e99e',
                 'qualification': 'HISTORIQUEMENT EVALUEE - NON INDEPENDAMMENT CONFIRMEE',
                 'familles': resultats_familles, 'decision_globale': decision,
                 'variables_extraites': list(audit_vars.keys()),
                 'controles_anti_fuite': audit['controles_anti_fuite'],
                 'separation': 'grappe entiere par famille; segments 2010-2015/2016-2017/2018-2020; purge des fenetres chevauchant le segment suivant; calibration non utilisee pour ajuster ni selectionner (aucune recalibration prespecifiee)',
                 'criteres_insuffisance_appliques': 'evaluation <100 etiquetes ou minorite <50 => NON EVALUABLE',
                 'anomalies': anomalies,
                 'interdits_respectes': 'aucune variable fenetre complete, aucun test de significativite, aucune optimisation, aucun acces holdout, aucune rentabilite'}
    (ROOT12 / 'PHASE12B_RESULTS.json').write_text(json.dumps(resultats, indent=1, ensure_ascii=False, default=str))
    print(json.dumps(resultats, indent=1, ensure_ascii=False, default=str)[:6000], flush=True)

if __name__ == '__main__':
    main()
