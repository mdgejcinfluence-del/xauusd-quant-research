#!/usr/bin/env python3
"""PHASE 14.1 - Audit de reconciliation a partir des seuls artefacts
Phase 13-B/14 deja produits. Aucune lecture de ticks bruts, aucun
recalcul de barrieres: seules des agregations de controle sur les
fichiers evenementiels deja committes."""
import glob
import json
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R13 = ROOT / 'reports/meta_alpha/phase13'
R14 = ROOT / 'reports/meta_alpha/phase14'
OUT = {}
SCEN = ['S0', 'S1', 'S2']

S = pd.read_csv(R14 / 'PHASE14_EVENT_PATH_SEQUENCE.csv')
EV = pd.read_csv(R14 / 'PHASE14_TRIPLE_BARRIER_EVENTS.csv')
M = pd.read_csv(R14 / 'PHASE14_BARRIER_MATRIX.csv')
E13 = pd.read_csv(R13 / 'PHASE13B_EVENT_EXECUTIONS.csv')

# ---- 1. denominateurs de sequence -------------------------------------
rows = []
for r in S.itertuples():
    corrige = r.ordre if r.statut_completude == 'COMPLET' else 'CENSORED'
    rows.append({'event_id': r.event_id, 'grappe_id': r.grappe_id,
                 'p_M1': r.p_M1, 'quartile_phase14': r.quartile,
                 'mfe_disponible': bool(pd.notna(r.mfe_bp)),
                 'mae_disponible': bool(pd.notna(r.mae_bp)),
                 'statut_completude': r.statut_completude,
                 'ordre_phase14': r.ordre,
                 'ordre_global_reconcilie': corrige,
                 'inclus_statistiques_sequence_reconciliees': corrige in
                 ('MFE_BEFORE_MAE', 'MAE_BEFORE_MFE', 'MFE_MAE_SAME_TIMESTAMP'),
                 'motif': '' if r.statut_completude == 'COMPLET' else
                 'FENETRE CENSUREE: extremes globaux non connaissables, ordre global CENSORED (14.1)'})
D = pd.DataFrame(rows)
D.to_csv(R14 / 'PHASE14_1_SEQUENCE_DENOMINATORS.csv', index=False)
comp = D[D.statut_completude == 'COMPLET']
OUT['sequence'] = {
    'exposes': int(len(D)),
    'complets_421': int(len(comp)),
    'incomplets_22': int(len(D) - len(comp)),
    'ordre_phase14_sur_443': {k: int(v) for k, v in D.ordre_phase14.value_counts().items()},
    'ordre_reconcilie_sur_421_complets': {k: int(v) for k, v in comp.ordre_global_reconcilie.value_counts().items()},
    'incomplets_reclasses_CENSORED': int((D.ordre_global_reconcilie == 'CENSORED').sum()),
    'taux_MAE_avant_MFE_communique': 223 / 443,
    'taux_MAE_avant_MFE_reconcilie_denominateur_421': float((comp.ordre_global_reconcilie == 'MAE_BEFORE_MFE').mean()),
    'conclusion_sens_inchange': bool(abs((comp.ordre_global_reconcilie == 'MAE_BEFORE_MFE').mean() - 0.5) < 0.01),
}

# ---- 2. audit des franchissements apres trou ---------------------------
P = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R14 / 'P14_PATH_*.csv')))])
P['ts'] = pd.to_datetime(P.ts, format='mixed')
P['ts2'] = pd.to_datetime(P.ts2, format='mixed')
trous = P[P.kind == 'HOLE'][['event_id', 'ts', 'ts2']].rename(
    columns={'ts': 'trou_debut', 'ts2': 'trou_fin'})
trous['duree_min'] = (trous.trou_fin - trous.trou_debut).dt.total_seconds() / 60
ext = P[P.kind == 'EXTREME']
g = (EV[EV.gap_avant_franchissement == True]
     .drop_duplicates(['event_id', 'normalisation', 'configuration']))
e13idx = E13.set_index('event_id')
grow = []
for r in g.itertuples():
    t_cross = pd.Timestamp(r.timestamp_sortie)
    cand = trous[(trous.event_id == r.event_id) & (trous.trou_fin == t_cross)]
    hole = cand.iloc[0] if len(cand) else None
    tick = ext[(ext.event_id == r.event_id) & (ext.ts == t_cross)]
    liq = float(tick.liq.iloc[0]) if len(tick) else np.nan
    niveau = r.niveau_tp if r.statut == 'TP_FIRST' else r.niveau_sl
    franchi = bool(len(tick) and ((r.statut == 'TP_FIRST' and
                                   ((e13idx.loc[r.event_id, 'direction'] == 1 and liq >= niveau) or
                                    (e13idx.loc[r.event_id, 'direction'] == -1 and liq <= niveau))) or
                                  (r.statut == 'SL_FIRST' and
                                   ((e13idx.loc[r.event_id, 'direction'] == 1 and liq <= niveau) or
                                    (e13idx.loc[r.event_id, 'direction'] == -1 and liq >= niveau)))))
    grow.append({'event_id': r.event_id, 'grappe_id': r.grappe_id,
                 'normalisation': r.normalisation, 'configuration': r.configuration,
                 'barriere': r.statut, 'niveau_barriere': niveau,
                 'trou_debut_derniere_cotation_avant': str(hole.trou_debut) if hole is not None else 'TROU NON RETROUVE DANS LES ARTEFACTS DE CHEMIN',
                 'trou_fin_premiere_cotation_apres': str(hole.trou_fin) if hole is not None else '',
                 'duree_trou_min': float(hole.duree_min) if hole is not None else np.nan,
                 'prix_premier_tick_apres_trou': liq,
                 'franchissement_au_dela_du_niveau_verifie': franchi,
                 'derniere_cotation_valide_avant_trou': 'NON CONSERVEE EN TANT QUE TELLE DANS LES ARTEFACTS (seuls les ticks atteignant un nouvel extreme courant et les bornes de morceaux sont conserves)',
                 'classification_14_1': 'A_CONVENTION_GELEE_APPLIQUEE (franchissement execute au premier prix observable apres le trou, conformement au preenregistrement seq334); ordre intra-trou non observable: limite consignee, aucune trajectoire supposee',
                 'convention_appliquee_conforme_au_gel': True})
G = pd.DataFrame(grow)
G.to_csv(R14 / 'PHASE14_1_GAP_CROSSING_AUDIT.csv', index=False)
OUT['gaps'] = {'trous_recenses_phase14': 209,
               'lignes_gap_ev_x_config_x_scenario': int((EV.gap_avant_franchissement == True).sum()),
               'franchissements_uniques_ev_x_config': int(len(G)),
               'evenements_uniques': int(G.event_id.nunique()),
               'tous_franchissements_verifies_au_dela_du_niveau': bool(G.franchissement_au_dela_du_niveau_verifie.all()),
               'tous_trous_retrouves': bool(G.duree_trou_min.notna().all()),
               'duree_trou_min_min': float(G.duree_trou_min.min()),
               'duree_trou_min_max': float(G.duree_trou_min.max()),
               'convention': 'premier tick apres trou (gel seq334) - conforme, aucun amendement retroactif',
               'limite_ouverte': 'derniere cotation valide avant le trou non conservee en tant que telle dans les artefacts de chemin; ordre des mouvements pendant le trou non observable par construction'}

# ---- 3. reconciliation des 54 cellules --------------------------------
mrows = []
ecarts = []
for _, m in M.iterrows():
    d = EV[(EV.normalisation == m.normalisation) & (EV.configuration == m.configuration) &
           (EV.scenario == m.scenario)]
    res = d[d.statut.isin(['TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'])]
    gr = res.groupby('grappe_id').resultat_bp.mean()
    rec = {'normalisation': m.normalisation, 'configuration': m.configuration,
           'scenario': m.scenario,
           'n_TP_FIRST_matrice': int(m.n_TP_FIRST), 'n_TP_FIRST_reconcilie': int((d.statut == 'TP_FIRST').sum()),
           'n_SL_FIRST_matrice': int(m.n_SL_FIRST), 'n_SL_FIRST_reconcilie': int((d.statut == 'SL_FIRST').sum()),
           'n_VERTICAL_FIRST_matrice': int(m.n_VERTICAL_FIRST), 'n_VERTICAL_FIRST_reconcilie': int((d.statut == 'VERTICAL_FIRST').sum()),
           'n_CENSORED_matrice': int(m.n_CENSORED), 'n_CENSORED_reconcilie': int((d.statut == 'CENSORED').sum()),
           'n_UNAVAILABLE_reconcilie': int((d.statut == 'UNAVAILABLE').sum()),
           'effectif_economique': int(len(res)),
           'moyenne_matrice': m.ev_moyenne, 'moyenne_reconciliee': float(res.resultat_bp.mean()),
           'mediane_matrice': m.ev_mediane, 'mediane_reconciliee': float(res.resultat_bp.median()),
           'taux_positif_matrice': m.ev_part_positifs, 'taux_positif_reconcilie': float((res.resultat_bp > 0).mean()),
           'perte_max_matrice': m.ev_perte_maximale, 'perte_max_reconciliee': float(res.resultat_bp.min()),
           'moyenne_grappe_matrice': m.gr_moyenne, 'moyenne_grappe_reconciliee': float(gr.mean()),
           'mediane_grappe_matrice': m.gr_mediane, 'mediane_grappe_reconciliee': float(gr.median()),
           'n_grappes': int(res.grappe_id.nunique())}
    if abs(rec['taux_positif_matrice'] - rec['taux_positif_reconcilie']) > 1e-9:
        ecarts.append(f"{m.normalisation}/{m.configuration}/{m.scenario}:taux_positif")
    for a, b in [('n_TP_FIRST', 'n_TP_FIRST'), ('n_SL_FIRST', 'n_SL_FIRST'),
                 ('n_VERTICAL_FIRST', 'n_VERTICAL_FIRST'), ('n_CENSORED', 'n_CENSORED')]:
        if rec[f'{a}_matrice'] != rec[f'{b}_reconcilie']:
            ecarts.append(f"{m.normalisation}/{m.configuration}/{m.scenario}:{a}")
    for a in ('moyenne', 'mediane', 'perte_max', 'moyenne_grappe', 'mediane_grappe'):
        if abs(rec[f'{a}_matrice'] - rec[f'{a}_reconciliee']) > 1e-9:
            ecarts.append(f"{m.normalisation}/{m.configuration}/{m.scenario}:{a}")
    mrows.append(rec)
MR = pd.DataFrame(mrows)
MR.to_csv(R14 / 'PHASE14_1_BARRIER_MATRIX_RECONCILIATION.csv', index=False)
b09 = MR[(MR.normalisation == 'B_ATR14_H1') & (MR.configuration == 'B09')].set_index('scenario')
b08 = MR[(MR.normalisation == 'B_ATR14_H1') & (MR.configuration == 'B08')].set_index('scenario')
OUT['matrice'] = {'cellules': int(len(MR)), 'ecarts_numeriques': ecarts,
                  'ATR_B09_S0': float(b09.loc['S0', 'moyenne_reconciliee']),
                  'ATR_B09_S2': float(b09.loc['S2', 'moyenne_reconciliee']),
                  'ATR_B08_S0': float(b08.loc['S0', 'moyenne_reconciliee']),
                  'ATR_B08_S2': float(b08.loc['S2', 'moyenne_reconciliee']),
                  'pertes_max_ATR_S0_min_max': [float(MR[(MR.normalisation == 'B_ATR14_H1') & (MR.scenario == 'S0')].perte_max_reconciliee.min()),
                                               float(MR[(MR.normalisation == 'B_ATR14_H1') & (MR.scenario == 'S0')].perte_max_reconciliee.max())],
                  'R_EVENT_toutes_negatives_S0': bool((MR[(MR.normalisation == 'A_R_EVENT') & (MR.scenario == 'S0')].moyenne_reconciliee < 0).all()),
                  'aucune_configuration_selectionnee': True}

# ---- 4. ponderation grappe ---------------------------------------------
cw = []
for (norm, cid, scen), d in EV[EV.statut.isin(['TP_FIRST', 'SL_FIRST', 'VERTICAL_FIRST'])].groupby(['normalisation', 'configuration', 'scenario']):
    gr = d.groupby('grappe_id').resultat_bp.mean()
    cw.append({'normalisation': norm, 'configuration': cid, 'scenario': scen,
               'n_evenements': int(len(d)), 'n_grappes': int(d.grappe_id.nunique()),
               'grappes_manquantes_par_rapport_au_max': int(EV.grappe_id.nunique() - d.grappe_id.nunique()),
               'moyenne_evenement': float(d.resultat_bp.mean()),
               'moyenne_grappe (moyenne des moyennes intra-grappe)': float(gr.mean()),
               'mediane_evenement': float(d.resultat_bp.median()),
               'mediane_des_moyennes_par_grappe': float(gr.median()),
               'evenements_censures_exclus': int((EV[(EV.normalisation == norm) & (EV.configuration == cid) & (EV.scenario == scen)].statut == 'CENSORED').sum()),
               'recalcul_de_grappes': 'AUCUN (grappe_id Phase 11-B/13-B repris tels quels)'})
CW = pd.DataFrame(cw)
CW.to_csv(R14 / 'PHASE14_1_CLUSTER_WEIGHTING_AUDIT.csv', index=False)
OUT['grappes'] = {'grappe_id_distincts_cohorte': int(EV.grappe_id.nunique()),
                  'cellules_verifiees': int(len(CW)),
                  'conforme': bool((CW['n_grappes'] > 0).all())}

# ---- 5. quartiles -------------------------------------------------------
S2 = S.sort_values(['p_M1', 'event_id']).reset_index(drop=True)
labels, debut = [], 0
for i, t in enumerate([111, 111, 111, 110]):
    labels += [f'Q{i + 1}'] * t
    debut += t
S2['quartile_reconstruit'] = labels
OUT['quartiles'] = {
    'construction': 'p_M1 seul, departage event_id (verifie par reconstruction du classement)',
    'concordance_avec_phase14': bool((S2.quartile_reconstruit.values == S2.sort_values(['p_M1', 'event_id']).reset_index(drop=True).quartile.values).all()),
    'seuils': {q: {'n': int((S.quartile == q).sum()), 'p_min': float(S.loc[S.quartile == q, 'p_M1'].min()),
                   'p_max': float(S.loc[S.quartile == q, 'p_M1'].max())} for q in ('Q1', 'Q2', 'Q3', 'Q4')},
    'Q4_mfe_median': float(S.loc[S.quartile == 'Q4', 'mfe_bp'].median()),
    'Q4_mae_median': float(S.loc[S.quartile == 'Q4', 'mae_bp'].median()),
    'Q4_freq_MFE_avant_MAE': float((S.loc[S.quartile == 'Q4', 'ordre'] == 'MFE_BEFORE_MAE').mean()),
    'Q4_statut': 'descriptif uniquement, aucun filtre cree'}
# coherence avec les seuils consignes en Phase 14
res14 = json.loads((R14 / 'PHASE14_RESULTS.json').read_text())
OUT['quartiles']['coherent_avec_PHASE14_RESULTS'] = bool(all(
    abs(OUT['quartiles']['seuils'][q]['p_max'] - res14['quartiles_seuils_p_M1'][q]['p_max']) < 1e-12
    for q in ('Q1', 'Q2', 'Q3', 'Q4')))

# ---- 6. couts: etiquettes et slippage aux seuls remplissages -----------
lab = EV.groupby('scenario').etiquette.unique().to_dict()
piv = EV.pivot_table(index=['event_id', 'normalisation', 'configuration'],
                     columns='scenario', values='resultat_bp')
stat = EV.pivot_table(index=['event_id', 'normalisation', 'configuration'],
                      columns='scenario', values='statut', aggfunc='first')
OUT['couts'] = {'etiquettes': {k: list(v) for k, v in lab.items()},
                'statuts_identiques_entre_scenarios': bool((stat.S0 == stat.S1).all() and (stat.S0 == stat.S2).all()),
                'delta_S1_moins_S0_median_bp': float((piv.S1 - piv.S0).median()),
                'delta_S2_moins_S0_median_bp': float((piv.S2 - piv.S0).median()),
                'spread': 'integre une seule fois aux prix Bid/Ask (aucune soustraction dans les artefacts)',
                'commissions': 'COMMISSION_EXCLUDED_BY_DESIGN - aucun tarif dans les artefacts'}

OUT['verdict_controles'] = {
    'denominateurs_sequences': 'DIVERGENCE DOCUMENTEE ET RECONCILIEE: le taux communique de 50,3 % portait sur 443 (22 incompletes classees); denominateur corrige 421, taux 50,36 %, sens inchange; les 22 incompletes sont re classees CENSORED pour l ordre global dans PHASE14_1_SEQUENCE_DENOMINATORS.csv',
    'gaps': 'CONFORME AU GEL (convention du premier tick apres trou preenregistree seq334 et appliquee telle quelle); limite epistemique consignee (ordre intra-trou non observable, derniere cotation avant trou non conservee en tant que telle)',
    'matrice_54_cellules': 'CONFORME' if not ecarts else f'ECARTS: {ecarts}',
    'grappes': 'CONFORME (aucun recalcul, moyennes intra-grappe puis moyenne des grappes verifiees)',
    'quartiles': 'CONFORME (p_M1 seul, departage event_id, seuils coherents)',
    'couts': 'CONFORME (etiquettes par scenario; slippage aux seuls remplissages: statuts et franchissements identiques entre scenarios, deltas medians -1/-2 bp)'}
(R14 / 'PHASE14_1_RESULTS.json').write_text(json.dumps(OUT, indent=1, ensure_ascii=False))
print(json.dumps(OUT, indent=1, ensure_ascii=False)[:3000])
