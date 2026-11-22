"""PHASE 11-C - anatomie descriptive des grands mouvements H1/H4.
Protocole PHASE 11-A gele (sha256 fdfb04ed...), autorisation seq305.
Populations fermees F10-01 (3107 admissibles) et F10-03 (660), identifiants
PHASE 11-B.1 (aucun nouveau clustering). Trajectoires Mid depuis les barres
M1 IS; aucune rentabilite, aucune p-value. Bootstrap grappes descriptif
2000 repetitions, graine 20261122."""
import glob, json, os, pathlib, sys
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase10_engine import construire_barres

ROOT = pathlib.Path('reports/meta_alpha/phase11'); ROOT.mkdir(parents=True, exist_ok=True)
SESSIONS = [(0, 'ASIA'), (8, 'LONDON'), (13, 'LONDON_NY_OVERLAP'), (17, 'NY_AFTERNOON'), (21, 'NIGHT_OTHER')]

def session_de(h):
    for borne, nom in reversed(SESSIONS):
        if h >= borne: return nom
    return 'ASIA'

def fermeture_reguliere(fin_precedente):
    return fin_precedente.hour >= 20 or fin_precedente.weekday() >= 4

def charger_barres():
    dossier = os.environ.get('BARS_DIR', 'bars_artifacts')
    fs = sorted(glob.glob(f'{dossier}/**/P10_BARS_*.csv.gz', recursive=True))
    if len(fs) < 8: raise RuntimeError(f'integrite lots: {len(fs)}/8 fichiers de barres')
    bars = pd.concat([pd.read_csv(f) for f in fs])
    bars['ts'] = pd.to_datetime(bars.ts)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True), len(fs)

def analyser_event(ev_row, tf_bars, trig_idx, M, minutes_tf):
    """M: arrays M1 (ts_min, mo, mh, ml, mc). Retourne dict de mesures."""
    d = int(ev_row.sens); t0 = pd.Timestamp(ev_row.t_signal)
    trig = tf_bars.iloc[trig_idx]
    P0 = float(trig.mc)
    ts_min, mo, mh, ml, mc = M
    t0min = int(t0.value // 60_000_000_000)
    # --- barres de trajectoire et censure ---
    chemin, motif_censure = [], 'COMPLETE'
    fin_prec = t0
    for k in range(1, 9):
        j = trig_idx + k
        if j >= len(tf_bars): motif_censure = 'FIN_COUVERTURE'; break
        b = tf_bars.iloc[j]
        ecart = (b.debut - fin_prec) / pd.Timedelta(minutes=1)
        if ecart > minutes_tf and not fermeture_reguliere(fin_prec):
            motif_censure = 'LACUNE_ANORMALE'; break
        chemin.append(b); fin_prec = b.fin
    horizon = len(chemin)
    R = {'t0': str(t0), 'P0': P0, 'direction': d, 'horizon_atteint': horizon,
         'statut_censure': 'COMPLETE' if horizon == 8 else motif_censure,
         'session_declenchement': session_de(t0.hour)}
    if horizon == 0:
        return R
    fin_fenetre = chemin[-1].fin
    i0 = int(np.searchsorted(ts_min, t0min))
    i1 = int(np.searchsorted(ts_min, int(fin_fenetre.value // 60_000_000_000)))
    s_mh, s_ml, s_mc, s_ts = mh[i0:i1], ml[i0:i1], mc[i0:i1], ts_min[i0:i1]
    if len(s_mc) == 0:
        R['statut_censure'] = 'DONNEES_M1_ABSENTES'; R['horizon_atteint'] = 0; return R
    R['temps_marche_minutes'] = int(len(s_mc))
    R['temps_calendaire_minutes'] = int((fin_fenetre - t0) / pd.Timedelta(minutes=1))
    y = d * 10000 * np.log(s_mc / P0)  # clotures M1 orientees (bp)
    if d > 0:
        fav_px = np.maximum.accumulate(s_mh); adv_px = np.minimum.accumulate(s_ml)
        fav_bp = 10000 * np.log(fav_px / P0); adv_bp = 10000 * np.log(P0 / adv_px)
        extreme_decl = float(trig.mh)
    else:
        fav_px = np.minimum.accumulate(s_ml); adv_px = np.maximum.accumulate(s_mh)
        fav_bp = 10000 * np.log(P0 / fav_px); adv_bp = 10000 * np.log(adv_px / P0)
        extreme_decl = float(trig.ml)
    # bornes de fin de chaque bougie de trajectoire (en minutes)
    fins = [int(b.fin.value // 60_000_000_000) for b in chemin]
    for k in range(1, 9):
        if k <= horizon:
            ik = int(np.searchsorted(s_ts, fins[k - 1]))
            R[f'mfe_{k}'] = float(max(0.0, fav_bp[:ik].max())) if ik else 0.0
            R[f'mae_{k}'] = float(max(0.0, adv_bp[:ik].max())) if ik else 0.0
            R[f'disp_{k}'] = float(y[ik - 1]) if ik else np.nan
        else:
            R[f'mfe_{k}'] = np.nan; R[f'mae_{k}'] = np.nan; R[f'disp_{k}'] = np.nan
    def minute_iso(idx):
        return str(pd.Timestamp(s_ts[idx], unit='m')) if 0 <= idx < len(s_ts) else None
    imfe = int(np.argmax(fav_bp)); imae = int(np.argmax(adv_bp))
    R['mfe_max_bp'] = float(fav_bp[imfe]); R['mae_max_bp'] = float(adv_bp[imae])
    R['mfe_extreme_minute_start_utc'] = minute_iso(imfe); R['mae_extreme_minute_start_utc'] = minute_iso(imae)
    R['mfe_extreme_available_at_utc'] = str(pd.Timestamp(s_ts[imfe], unit='m') + pd.Timedelta(minutes=1)) if len(s_ts) else None
    R['mae_extreme_available_at_utc'] = str(pd.Timestamp(s_ts[imae], unit='m') + pd.Timedelta(minutes=1)) if len(s_ts) else None
    R['extreme_timestamp_resolution'] = 'M1'
    R['session_mfe'] = session_de(pd.Timestamp(s_ts[imfe], unit='m').hour) if len(s_ts) else None
    R['session_mae'] = session_de(pd.Timestamp(s_ts[imae], unit='m').hour) if len(s_ts) else None
    # --- extension confirmee, repli (clotures), reprise ---
    best = np.maximum.accumulate(y)
    ext_idx = np.where(y > 0)[0]
    extension = len(ext_idx) > 0
    R['extension_confirmee'] = int(extension)
    repli_start, best_avant_repli = None, None
    if extension:
        for mIdx in range(len(y)):
            if best[mIdx] > 0 and y[mIdx] < best[mIdx]:
                repli_start, best_avant_repli = mIdx, float(best[mIdx]); break
    R['repli_present'] = int(repli_start is not None)
    # repli depuis l'extreme favorable (extrema, minute du sommet exclue pour ne pas inventer d'ordre intraminute)
    profondeur, i_repli_ext, i_sommet = 0.0, None, None
    if d > 0:
        sommet = np.maximum.accumulate(s_mh)
        for mIdx in range(1, len(y)):
            prof = 10000 * np.log(sommet[mIdx - 1] / s_ml[mIdx])
            if prof > profondeur: profondeur, i_repli_ext, i_sommet = float(prof), mIdx, int(np.argmax(s_mh[:mIdx]))
    else:
        creux = np.minimum.accumulate(s_ml)
        for mIdx in range(1, len(y)):
            prof = 10000 * np.log(s_mh[mIdx] / creux[mIdx - 1])
            if prof > profondeur: profondeur, i_repli_ext, i_sommet = float(prof), mIdx, int(np.argmax(-s_ml[:mIdx]))
    R['repli_profondeur_max_bp'] = profondeur
    R['repli_extreme_minute_start_utc'] = minute_iso(i_repli_ext) if i_repli_ext is not None else None
    R['repli_duree_minutes'] = int(s_ts[i_repli_ext] - s_ts[i_sommet]) if (i_repli_ext is not None and i_sommet is not None) else None
    R['session_repli'] = session_de(pd.Timestamp(s_ts[i_repli_ext], unit='m').hour) if i_repli_ext is not None else None
    # ordre intraminute indetermine: sommet favorable et extreme de repli dans la meme minute (calcul inclusif)
    intra = False
    if i_repli_ext is not None and i_sommet is not None and s_ts[i_repli_ext] == s_ts[i_sommet]: intra = True
    R['intra_minute_order_unknown'] = int(intra)
    if repli_start is not None:
        R['repli_debut_minute_start_utc'] = minute_iso(repli_start)
        apres = np.where(y[repli_start + 1:] > best_avant_repli)[0]
        R['reprise_apres_repli'] = int(len(apres) > 0)
        R['reprise_minute_start_utc'] = minute_iso(repli_start + 1 + int(apres[0])) if len(apres) else None
    else:
        R['reprise_apres_repli'] = 0; R['reprise_minute_start_utc'] = None; R['repli_debut_minute_start_utc'] = None
    R['session_reprise'] = session_de(pd.Timestamp(R['reprise_minute_start_utc']).hour) if R['reprise_minute_start_utc'] else None
    # --- touche et reintegration de P0 ---
    touche = np.where(adv_bp > 0)[0]
    R['touche_P0'] = int(len(touche) > 0)
    R['touche_delai_minutes'] = int(s_ts[touche[0]] - t0min) if len(touche) else None
    R['touche_minute_start_utc'] = minute_iso(int(touche[0])) if len(touche) else None
    R['session_touche'] = session_de(pd.Timestamp(s_ts[touche[0]], unit='m').hour) if len(touche) else None
    reint, best_avant_reint = None, None
    if extension:
        premier_ext = int(ext_idx[0])
        cand = np.where(y[premier_ext + 1:] < 0)[0]
        if len(cand):
            reint = premier_ext + 1 + int(cand[0]); best_avant_reint = float(best[reint])
    R['reintegration_confirmee'] = int(reint is not None)
    R['reintegration_delai_minutes'] = int(s_ts[reint] - t0min) if reint is not None else None
    R['reintegration_minute_start_utc'] = minute_iso(reint) if reint is not None else None
    R['session_reintegration'] = session_de(pd.Timestamp(s_ts[reint], unit='m').hour) if reint is not None else None
    R['retour_immediat'] = int(reint is not None and s_ts[reint] < fins[0]) if (reint is not None and fins) else 0
    if extension:
        seg = y[int(ext_idx[0]):]
        R['nb_retours'] = int(np.sum((seg[:-1] >= 0) & (seg[1:] < 0))) if len(seg) > 1 else 0
    else:
        R['nb_retours'] = 0
    reprise_post_reint = False
    if reint is not None:
        reprise_post_reint = bool(np.any(y[reint + 1:] > best_avant_reint))
    R['reprise_apres_reintegration'] = int(reprise_post_reint)
    # --- retracement de la bougie declencheuse (jamais plafonne) ---
    corps = d * 10000 * np.log(float(trig.mc) / float(trig.mo))
    R['corps_declencheur_bp'] = float(corps)
    R['range_declencheur_bp'] = float(10000 * np.log(float(trig.mh) / float(trig.ml)))
    if d > 0: recul_depuis_decl = 10000 * np.log(extreme_decl / s_ml)
    else: recul_depuis_decl = 10000 * np.log(s_mh / extreme_decl)
    R['recul_depuis_extreme_declencheur_bp'] = float(np.max(recul_depuis_decl)) if len(s_mc) else 0.0
    R['fraction_corps_reprise'] = float(R['recul_depuis_extreme_declencheur_bp'] / corps) if corps > 0 else np.nan
    R['repli_relatif_extension_pct'] = float(100 * profondeur / fav_bp[-1]) if fav_bp[-1] > 0 else np.nan
    R['repli_distance_P0_bp'] = float(y[i_repli_ext]) if i_repli_ext is not None else np.nan
    # composition temporelle de la bougie declencheuse (minutes par session)
    debut_trig = trig.debut
    masque_trig = (ts_min >= int(debut_trig.value // 60_000_000_000)) & (ts_min < t0min)
    heures_trig = pd.to_datetime(ts_min[masque_trig], unit='m').hour
    compo = {nom: int((heures_trig.map(session_de) == nom).sum()) for _, nom in SESSIONS}
    R['composition_declencheuse_minutes'] = json.dumps(compo)
    # --- archetype (hierarchie gelee) ---
    if horizon < 8:
        R['archetype'] = 'CENSURE'
    elif intra and (repli_start is not None or reint is not None):
        R['archetype'] = 'AMBIGU_INTRA_MINUTE'
    elif not extension:
        R['archetype'] = 'AUCUNE_EXTENSION_CONFIRMEE'
    elif reint is not None:
        R['archetype'] = 'REINTEGRATION_PUIS_REPRISE' if reprise_post_reint else 'FAUX_DEPART_REINTEGRE_SANS_REPRISE'
    elif repli_start is not None:
        R['archetype'] = 'REPLI_PUIS_CONTINUATION' if R['reprise_apres_repli'] else 'REPLI_SANS_REPRISE'
    else:
        R['archetype'] = 'CONTINUATION_SANS_REPLI_CONFIRME'
    return R

def q(vals, noms=('mediane', 'p25', 'p75', 'p90')):
    v = pd.Series(vals, dtype=float).dropna()
    if not len(v): return {n: None for n in noms} | {'n': 0}
    qq = {'mediane': 0.5, 'p25': 0.25, 'p75': 0.75, 'p90': 0.9, 'p95': 0.95}
    return {n: float(v.quantile(qq[n])) for n in noms} | {'n': int(len(v))}

def bootstrap_grappes(P, fam, graine=20261122, nb=2000):
    rng = np.random.default_rng(graine)
    d = P[P.famille == fam]
    groupes = [g for _, g in d.groupby('grappe_id')]
    def stats(ech):
        e = pd.concat(ech) if ech else d.iloc[0:0]
        return {'mfe_8_mediane': float(e.mfe_8.median()) if len(e) else np.nan,
                'mae_8_mediane': float(e.mae_8.median()) if len(e) else np.nan,
                'disp_8_mediane': float(e.disp_8.median()) if len(e) else np.nan}
    obs = stats(groupes)
    dist = {k: [] for k in obs}
    idx = rng.integers(0, len(groupes), size=(nb, len(groupes)))
    for b in range(nb):
        s = stats([groupes[i] for i in idx[b]])
        for k in dist: dist[k].append(s[k])
    return {k: {'observe': obs[k], 'ic95_bas': float(np.nanpercentile(dist[k], 2.5)), 'ic95_haut': float(np.nanpercentile(dist[k], 97.5))} for k in obs}

def main():
    bars, nb_lots = charger_barres()
    ev = pd.read_csv('reports/meta_alpha/phase10/PHASE10_EVENTS_CIBLE.csv.gz')
    carte = pd.read_csv(ROOT / 'PHASE11B_EVENT_CLUSTER_MAP.csv')
    ev['cle'] = [f"{f}|{tf}|{t}|{int(s):+d}" for f, tf, t, s in zip(ev.famille, ev.timeframe, ev.t_signal, ev.sens)]
    adm = ev[(ev.entree_eligible == 1) & (ev.fenetre_complete == 1)].merge(
        carte[['cle_composite_source', 'event_id', 'grappe_id']], left_on='cle', right_on='cle_composite_source', how='left')
    assert adm.event_id.notna().all() and len(adm) == 3767, f"jointure carte: {len(adm)} lignes, {adm.event_id.isna().sum()} sans identifiant"
    M = (bars.ts.values.astype('datetime64[ns]').astype('int64') // 60_000_000_000,
         bars.mo.values, bars.mh.values, bars.ml.values, bars.mc.values)
    chemins = []
    resumes_tf = {}
    for fam, minutes in [('F10-01', 60), ('F10-03', 240)]:
        tf = construire_barres(bars, minutes)
        resumes_tf[fam] = int(len(tf))
        fin_index = {pd.Timestamp(f): i for i, f in enumerate(tf.fin)}
        sous = adm[adm.famille == fam]
        for _, row in sous.iterrows():
            trig_idx = fin_index.get(pd.Timestamp(row.t_signal))
            if trig_idx is None:
                chemins.append({'event_id': row.event_id, 'grappe_id': row.grappe_id, 'famille': fam,
                                'timeframe': row.timeframe, 't0': row.t_signal, 'direction': int(row.sens),
                                'horizon_atteint': 0, 'statut_censure': 'BOUGIE_DECLENCHEUSE INTROUVABLE', 'archetype': 'CENSURE'})
                continue
            R = analyser_event(row, tf, trig_idx, M, minutes)
            R.update({'event_id': row.event_id, 'grappe_id': row.grappe_id, 'famille': fam, 'timeframe': row.timeframe})
            chemins.append(R)
        print('P11C', fam, 'evenements traites', len(sous), flush=True)
    P = pd.DataFrame(chemins)
    P.to_csv(ROOT / 'PHASE11C_EVENT_PATHS.csv', index=False)
    synthese(P, ev, nb_lots, resumes_tf)

def synthese(P, ev, nb_lots, resumes_tf):
    resultats = {'statut_execution': 'TERMINE', 'lots_barres': nb_lots, 'barres_tf': resumes_tf,
                 'populations': {}, 'anomalies': [], 'reproductibilite': 'moteur deterministe (aucun hasard hors bootstrap a graine fixee 20261122)'}
    horizons, archetypes, sessions, couverture = [], [], [], []
    for fam in ('F10-01', 'F10-03'):
        d = P[P.famille == fam]
        dcomplet = d[d.horizon_atteint == 8]
        resultats['populations'][fam] = {'admissibles_analyses': int(len(d)), 'trajectoires_completes': int(len(dcomplet)),
                                         'censurees': int(len(d) - len(dcomplet)),
                                         'bootstrap_grappes_t8': bootstrap_grappes(dcomplet, fam) if len(dcomplet) else {}}
        for k in range(1, 9):
            sous = d[d.horizon_atteint >= k]
            ligne = {'famille': fam, 'timeframe': d.timeframe.iloc[0], 'horizon': k, 'n_evenements': int(len(sous))}
            for mesure in ('mfe', 'mae', 'disp'):
                col = f'{mesure}_{k}'
                ligne[f'{mesure}_evenement'] = json.dumps(q(sous[col]))
                par_grappe = sous.groupby('grappe_id')[col].median()
                ligne[f'{mesure}_grappe'] = json.dumps(q(par_grappe))
            ligne['proportion_nouveau_mfe'] = float((sous[f'mfe_{k}'] > sous[f'mfe_{k-1}']).mean()) if k > 1 and len(sous) else None
            ligne['proportion_aggravation_mae'] = float((sous[f'mae_{k}'] > sous[f'mae_{k-1}']).mean()) if k > 1 and len(sous) else None
            horizons.append(ligne)
            couverture.append({'famille': fam, 'horizon': k, 'n_disponibles': int(len(sous)),
                               'n_censurees_avant_horizon': int(len(d) - len(sous))})
        for arch, n in d.archetype.value_counts().items():
            archetypes.append({'famille': fam, 'archetype': arch, 'n': int(n), 'proportion': float(n / len(d)), 'denominateur': int(len(d))})
        for sess, g in d.groupby('session_declenchement'):
            sessions.append({'famille': fam, 'type_session': 'DECLENCHEMENT', 'session': sess, 'n': int(len(g)),
                             'mfe_8_mediane': float(g.mfe_8.median()), 'mae_8_mediane': float(g.mae_8.median()),
                             'part_reintegration': float(g.reintegration_confirmee.mean()), 'part_reprise_post_reintegration': float(g.reprise_apres_reintegration.mean())})
        for champ, nom in [('session_mfe', 'MFE'), ('session_mae', 'MAE'), ('session_repli', 'REPLI'), ('session_touche', 'TOUCHE'),
                           ('session_reintegration', 'REINTEGRATION'), ('session_reprise', 'REPRISE')]:
            for sess, n in d[champ].dropna().value_counts().items():
                sessions.append({'famille': fam, 'type_session': f'REALISATION_{nom}', 'session': sess, 'n': int(n),
                                 'mfe_8_mediane': None, 'mae_8_mediane': None, 'part_reintegration': None, 'part_reprise_post_reintegration': None})
        cov = d.statut_censure.value_counts()
        resultats['populations'][fam]['censures'] = {k: int(v) for k, v in cov.items()}
    # chevauchement descriptif H1 dans les episodes H4 (declencheuse + fenetre d'observation 32 h)
    h1 = P[P.famille == 'F10-01']; h4 = P[P.famille == 'F10-03']
    if len(h1) and len(h4):
        debuts = np.sort(pd.to_datetime(h4.t0).values.astype('datetime64[ns]').astype('int64') // 60_000_000_000 - 240)
        fins = debuts + 240 + 32 * 60
        t_h1 = pd.to_datetime(h1.t0).values.astype('datetime64[ns]').astype('int64') // 60_000_000_000
        pos = np.searchsorted(debuts, t_h1, side='right') - 1
        dedans = (pos >= 0) & (t_h1 <= fins[np.maximum(pos, 0)])
        resultats['chevauchement_H1_dans_episodes_H4'] = {'evenements_H1_concernes': int(dedans.sum()), 'total_H1': int(len(h1)),
                                                           'definition': 't0 H1 dans [debut de la bougie declencheuse H4, t0 H4 + 32 h]', 'interpretation': 'descriptif uniquement, aucune causalite'}
    pd.DataFrame(horizons).to_csv(ROOT / 'PHASE11C_HORIZON_METRICS.csv', index=False)
    pd.DataFrame(archetypes).to_csv(ROOT / 'PHASE11C_ARCHETYPES.csv', index=False)
    pd.DataFrame(sessions).to_csv(ROOT / 'PHASE11C_SESSION_ANATOMY.csv', index=False)
    pd.DataFrame(couverture).to_csv(ROOT / 'PHASE11C_COVERAGE_CENSORING.csv', index=False)
    (ROOT / 'PHASE11C_RESULTS.json').write_text(json.dumps(resultats, indent=1, default=str))
    print(json.dumps(resultats, indent=1, default=str)[:4000], flush=True)

if __name__ == '__main__': main()
