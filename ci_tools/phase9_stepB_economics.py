"""PHASE 9 ETAPE B - audit economique descriptif des cinq candidates.
Aucun backtest strategique: esperances brutes Mid descriptives calculees
sur les fichiers d evenements deja valides des campagnes 1-5, moins un
modele de couts explicite (spread OBSERVE a l evenement; commissions et
slippage HYPOTHETIQUES en scenarios). Les estimations Mid ne sont pas
des preuves de remplissage reel."""
import json, pathlib
import numpy as np
import pandas as pd

OUT = pathlib.Path('reports/meta_alpha/phase9_portfolio'); OUT.mkdir(parents=True, exist_ok=True)
M1 = pathlib.Path('reports/meta_alpha')

# Modele de couts commun (aller-retour, en bp). Spread: multiplie le spread observe.
SCENARIOS = {
    'favorable':   {'spread_mult': 1.0, 'commission_bp': 0.0, 'slippage_bp_AR': 0.5},
    'central':     {'spread_mult': 1.0, 'commission_bp': 0.7, 'slippage_bp_AR': 1.0},
    'defavorable': {'spread_mult': 1.5, 'commission_bp': 1.4, 'slippage_bp_AR': 3.0}}

def couts(spread_obs):
    return {k: float(v['spread_mult'] * spread_obs + v['commission_bp'] + v['slippage_bp_AR'])
            for k, v in SCENARIOS.items()}

def bloc(brut, spread_obs, n, jours):
    c = couts(spread_obs)
    return {'n': int(n), 'journees': int(jours), 'frequence_par_an': float(n / max(jours, 1) * 252),
            'esperance_brute_mid_bp': float(brut), 'spread_observe_bp': float(spread_obs),
            'cout_total_bp': c, 'esperance_nette_bp': {k: float(brut - v) for k, v in c.items()},
            'cout_max_supportable_bp': float(brut)}

def med(s): return float(np.nanmedian(s))

# ---------- P9-A: depassements T0, tercile bas de profondeur initiale ----------
T = pd.read_csv(M1 / 'campaign02_2/CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv')
T0 = T[T.snapshot_min.astype(str) == '0'].copy()
q33 = T0.profondeur_initiale_bp.quantile(1 / 3)
A = T0[T0.profondeur_initiale_bp <= q33].copy()
# gain fade (Mid): reintegration -> sortie au niveau (= profondeur initiale);
# sinon position signee a +60 min relative au niveau.
A['gain_fade'] = np.where(A.reintegration_ulterior == 1, A.profondeur_initiale_bp,
                          A.profondeur_initiale_bp - A.position_plus60_bp)
p9a = bloc(A.gain_fade.mean(), med(A.spread_bp), len(A), A.date.nunique())
p9a.update({'seuil_tercile_bas_bp': float(q33), 'profondeur_mediane_bp': med(A.profondeur_initiale_bp),
            'taux_reintegration': float(A.reintegration_ulterior.mean()),
            'delai_reintegration_median_min': med(A.temps_restant_reint_min),
            'gain_median_bp': med(A.gain_fade),
            'par_ere': {}, 'par_session': {}})
for col, key in [('ere', 'par_ere'), ('session', 'par_session')]:
    for v, g in A.groupby(col):
        p9a[key][v] = {'n': int(len(g)), 'brut_bp': float(g.gain_fade.mean()), 'spread_bp': med(g.spread_bp)}

# ---------- P9-B: cassure + retest, entree momentum au retest ----------
B = pd.read_csv(M1 / 'campaign02_2/CAMPAIGN_02_2_BREAKOUT_TIMELINE.csv')
R = B[B.snapshot_min.astype(str) == 'RETEST'].copy()
R['gain_momentum_60'] = R.position_plus60_bp - R.position_bp
p9b = bloc(R.gain_momentum_60.mean(), med(R.spread_bp), len(R), R.date.nunique())
p9b.update({'delai_retest_median_min': med(R.delai_retest_min),
            'encore_au_dela_60': float((R.position_plus60_bp > 0).mean()),
            'gain_median_bp': med(R.gain_momentum_60),
            'position_plus15_med': med(R.position_plus15_bp), 'position_plus30_med': med(R.position_plus30_bp),
            'excursion_adverse_apres_retest': 'NON DISPONIBLE dans les fichiers valides (positions +15/+30/+60 seulement)',
            'par_ere': {v: {'n': int(len(g)), 'brut_bp': float(g.gain_momentum_60.mean()), 'spread_bp': med(g.spread_bp)} for v, g in R.groupby('ere')},
            'par_session': {v: {'n': int(len(g)), 'brut_bp': float(g.gain_momentum_60.mean()), 'spread_bp': med(g.spread_bp)} for v, g in R.groupby('session')}})

# ---------- P9-C: fade impulsions IMP-M5 Londres (vs Asie publie) ----------
S = pd.read_csv(M1 / 'campaign03/CAMPAIGN_03_SNAPSHOTS_IMP.csv.gz')
S = S[(S.famille == 'IMP-M5') & (S.censure_snapshot == 0)]
piv = S[S.snapshot_barres.isin([0, 12])].pivot_table(index=['date', 'ts_t0', 'direction'],
        columns='snapshot_barres', values=['position_bp', 'spread_median_bp', 'amplitude_initiale_bp',
        'excursion_opposee_bp', 'session', 'ere', 'chevauchement'], aggfunc='first')
piv.columns = [f'{a}_{b}' for a, b in piv.columns]
piv = piv.reset_index()
piv['gain_fade_60'] = piv.position_bp_0 - piv.position_bp_12  # entree a la cloture T0, sortie +60 min (Mid)
def fade_bloc(g):
    b = bloc(g.gain_fade_60.mean(), med(g.spread_median_bp_0), len(g), g.date.nunique())
    b.update({'amplitude_initiale_med_bp': med(g.amplitude_initiale_bp_0),
              'excursion_opposee_med_bp': med(g.excursion_opposee_bp_0),
              'gain_median_bp': med(g.gain_fade_60),
              'par_ere': {v: {'n': int(len(x)), 'brut_bp': float(x.gain_fade_60.mean()), 'spread_bp': med(x.spread_median_bp_0)} for v, x in g.groupby('ere_0')}})
    return b
p9c = {'Londres': fade_bloc(piv[piv.session_0 == 'LONDRES']), 'ASIE': fade_bloc(piv[piv.session_0 == 'ASIE']),
       'chevauchement_episodes_M5_pct': float(piv.chevauchement_0.mean() * 100)}

# ---------- P9-D: expansion apres consolidation (filtre de volatilite, sans direction) ----------
C = pd.read_csv(M1 / 'campaign03/CAMPAIGN_03_EPISODES_CONS.csv.gz')
C = C[C.censuree == 0].copy()
C['ratio_post'] = C.range_post_sortie_60_bp / C.range_formation_bp
p9d = {}
for grp, g in C.groupby('groupe_range_formation'):
    p9d[str(grp)] = {'n': int(len(g)), 'range_formation_med_bp': med(g.range_formation_bp),
                     'range_post_60_med_bp': med(g.range_post_sortie_60_bp),
                     'freq_sortie_2x': float((g.ratio_post > 2).mean()),
                     'duree_consolidation_med_min': med(g.duree_consolidation_min)}
# reference: range 60 min inconditionnel campagne 1 (EV6 global publie)
p9d['note'] = "Pas d'esperance directionnelle: valeur de filtre seulement. Spread a l'evenement non stocke pour CONS (voir registre des manques)."

# ---------- P9-E: atteintes veille, retracement selon heure de disponibilite ----------
E = pd.read_csv(M1 / 'campaign05/CAMPAIGN_05_ATTEINTES_JOUR.csv.gz')
E = E[(E.statut_atteinte == 'REELLE_IDENTIFIABLE') & (E.ordre_indetermine.fillna(0) == 0) & (E.censure_60 == 0)].copy()
E['avant13'] = E.disponibilite_min < 13 * 60
# mouvement "disponible" descriptif: retracement maximal +60 (sens fade) et extension (sens continuation)
p9e = {}
for lab, g in [('avant_13h', E[E.avant13]), ('des_13h', E[~E.avant13])]:
    p9e[lab] = {'n': int(len(g)), 'retracement_60_med_bp': med(g.retracement_60_bp),
                'extension_60_med_bp': med(g.extension_60_bp), 'position_fin_60_med_bp': med(g.position_fin_60_bp),
                'sessions': g.assign(ses=pd.cut(g.disponibilite_min, [0, 420, 780, 1260, 1440], labels=['S1', 'S2', 'S3', 'S4'])).ses.value_counts(normalize=True).round(3).to_dict(),
                'eres': g.ere.value_counts(normalize=True).round(3).to_dict()}
p9e['spread_proxy'] = "Spread a l'atteinte non stocke en campagne 5; proxy observe campagne 1 (EV2, mediane globale publiee dans CAMPAIGN_01_EVENT_METRICS.csv)."

res = {'modele_couts': SCENARIOS, 'P9-A': p9a, 'P9-B': p9b, 'P9-C': p9c, 'P9-D': p9d, 'P9-E': p9e}
(OUT / 'STEP_B_ECONOMICS.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=1, default=str)[:5200])
