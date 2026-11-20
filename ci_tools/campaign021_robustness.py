"""CAMPAGNE 2.1 - robustesse A/B, famille R gelee seq167. Descriptif seul."""
import numpy as np, pandas as pd, pathlib
rng = np.random.default_rng(20261113)
OUT = pathlib.Path('reports/meta_alpha/campaign02_1'); OUT.mkdir(parents=True, exist_ok=True)
E = pd.read_csv('reports/meta_alpha/campaign01/CAMPAIGN_01_EVENTS_RAW.csv')
NB = 2000

def by(pv):
    pv = np.asarray(pv, float); m = len(pv); order = np.argsort(pv); c = np.sum(1 / np.arange(1, m + 1))
    adj = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        val = min(prev, pv[order[i]] * m * c / (i + 1)); adj[order[i]] = min(val, 1.0); prev = adj[order[i]]
    return adj

def terc(df, col):
    out = pd.Series(index=df.index, dtype=object)
    for _, idx in df.groupby('ere').groups.items():
        r = df.loc[idx, col].rank(pct=True)
        out.loc[idx] = pd.cut(r, [0, 1/3, 2/3, 1.0001], labels=['BAS', 'MOYEN', 'HAUT'])
    return out

def quart(df, col):
    out = pd.Series(index=df.index, dtype=object)
    for _, idx in df.groupby('ere').groups.items():
        r = df.loc[idx, col].rank(pct=True)
        out.loc[idx] = pd.cut(r, [0, .25, .5, .75, 1.0001], labels=['Q1', 'Q2', 'Q3', 'Q4'])
    return out

def boot(A_df, B_df, val, kind):
    def arr(d):
        g = {}
        for c, v in zip(d.grappe, d[val]):
            if pd.notna(v): g.setdefault(c, []).append(v)
        return [np.array(x, float) for x in g.values()]
    A, B = arr(A_df), arr(B_df)
    def stat(gs, k):
        if k == 'prop': return sum(a.sum() for a in gs) / sum(len(a) for a in gs)
        return float(np.median(np.concatenate(gs)))
    sa, sb = stat(A, kind), stat(B, kind); obs = sa - sb if kind == 'prop' else sa / sb
    reps = []
    for _ in range(NB):
        ra = [A[i] for i in rng.integers(0, len(A), len(A))]; rb = [B[i] for i in rng.integers(0, len(B), len(B))]
        reps.append(stat(ra, kind) - stat(rb, kind) if kind == 'prop' else stat(ra, kind) / stat(rb, kind))
    reps = np.array(reps); z = reps if kind == 'prop' else np.log(reps)
    p = min(1.0, 2 * min(float(np.mean(z <= 0)), float(np.mean(z >= 0))))
    return obs, float(np.quantile(reps, .025)), float(np.quantile(reps, .975)), p, sa, sb, len(A), len(B)

dep = E[E.famille == 'EV2_DEPASSEMENT'].copy()
dep['reintegre'] = dep.delai_reintegration_min.notna().astype(float)
dep['prof_t'] = terc(dep, 'profondeur_bp'); dep['prof_q'] = quart(dep, 'profondeur_bp')
dep['prof_med'] = dep.groupby('ere', group_keys=False).apply(lambda d: (d.profondeur_bp > d.profondeur_bp.median()).map({True: 'HAUT', False: 'BAS'}), include_groups=False)
cas_ids = set(E[E.famille == 'EV3_CASSURE'].grappe)
dep['cassure_initiale'] = dep.grappe.isin(cas_ids).astype(float)
cas = E[E.famille == 'EV3_CASSURE'].copy(); ret = E[E.famille == 'EV3_RETEST'].copy()
ret['prof_t'] = terc(ret, 'profondeur_bp'); ret['prof_q'] = quart(ret, 'profondeur_bp')
ret['delai_t'] = terc(ret, 'delai_retour_test_min')
cas['reteste'] = cas.grappe.isin(set(ret.grappe)).astype(float)
cas['reintegre'] = cas.delai_reintegration_min.notna().astype(float)

rows = []
def add(tid, fam, bras, A, B, val, kind='prop'):
    obs, lo, hi, p, sa, sb, ga, gb = boot(A, B, val, kind)
    rows.append({'test': tid, 'famille': fam, 'comparaison': bras, 'variable': val, 'n_A': len(A), 'n_B': len(B),
                 'grappes_A': ga, 'grappes_B': gb, 'jours_A': int(A.date.nunique()), 'jours_B': int(B.date.nunique()),
                 'stat_A': round(sa, 4), 'stat_B': round(sb, 4), 'ecart': round(float(obs), 4), 'ic95_bas': round(lo, 4), 'ic95_haut': round(hi, 4), 'p_brut': round(p, 5)})
    print(tid, rows[-1], flush=True)

add('R01', 'A', 'cassure initiale observable (+5bp) vs depassement simple', dep[dep.cassure_initiale == 1], dep[dep.cassure_initiale == 0], 'reintegre')
add('R02', 'A', 'profondeur Q1 vs Q4 (sensibilite quartiles)', dep[dep.prof_q == 'Q1'], dep[dep.prof_q == 'Q4'], 'reintegre')
add('R03', 'A', 'profondeur sous vs au-dessus mediane d ere', dep[dep.prof_med == 'BAS'], dep[dep.prof_med == 'HAUT'], 'reintegre')
add('R04', 'A', 'profondeur BAS vs HAUT, session Londres seule', dep[(dep.prof_t == 'BAS') & (dep.session == 'LONDRES')], dep[(dep.prof_t == 'HAUT') & (dep.session == 'LONDRES')], 'reintegre')
add('R05', 'A', 'profondeur BAS vs HAUT, session New York seule', dep[(dep.prof_t == 'BAS') & (dep.session == 'NEWYORK')], dep[(dep.prof_t == 'HAUT') & (dep.session == 'NEWYORK')], 'reintegre')
add('R06', 'A', 'profondeur BAS vs HAUT, regime BAS seul', dep[(dep.prof_t == 'BAS') & (dep.regime == 'BAS')], dep[(dep.prof_t == 'HAUT') & (dep.regime == 'BAS')], 'reintegre')
add('R07', 'A', 'profondeur BAS vs HAUT, regime HAUT seul', dep[(dep.prof_t == 'BAS') & (dep.regime == 'HAUT')], dep[(dep.prof_t == 'HAUT') & (dep.regime == 'HAUT')], 'reintegre')
add('R08', 'A', 'profondeur mediane: censures vs reintegrations <=3 min', dep[dep.reintegre == 0], dep[dep.delai_reintegration_min <= 3], 'profondeur_bp', 'med')
add('R09', 'B', 'encore au-dela par delai retest BAS vs HAUT', ret[ret.delai_t == 'BAS'], ret[ret.delai_t == 'HAUT'], 'encore_au_dela_60')
add('R10', 'B', 'toutes cassures: reintegration, retestees vs non retestees', cas[cas.reteste == 1], cas[cas.reteste == 0], 'reintegre')
add('R11', 'B', 'encore au-dela, Londres vs New York (retests)', ret[ret.session == 'LONDRES'], ret[ret.session == 'NEWYORK'], 'encore_au_dela_60')
add('R12', 'B', 'encore au-dela, profondeur Q1 vs Q4 (sensibilite)', ret[ret.prof_q == 'Q1'], ret[ret.prof_q == 'Q4'], 'encore_au_dela_60')
R = pd.DataFrame(rows); R['p_BY_familleR'] = by(R.p_brut.values).round(5)
R.to_csv(OUT / 'CAMPAIGN_02_1_ROBUSTNESS_TESTS.csv', index=False)

# Descriptifs A
descA = []
for dim, col in [('SESSION', 'session'), ('ERE', 'ere'), ('REGIME', 'regime'), ('NIVEAU', 'contexte')]:
    for v, g in dep.groupby(col):
        descA.append({'famille': 'A_DEPASSEMENTS', 'dimension': dim, 'valeur': v, 'n': len(g), 'jours': int(g.date.nunique()), 'grappes': int(g.grappe.nunique()),
                      'prof_med_bp': round(g.profondeur_bp.median(), 2), 'prof_P90_bp': round(g.profondeur_bp.quantile(.9), 2),
                      'taux_reintegration': round(g.reintegre.mean(), 4), 'taux_censure': round(1 - g.reintegre.mean(), 4),
                      'delai_median_reintegres': float(g.delai_reintegration_min.median())})
for v, g in dep[dep.reintegre == 1].groupby(pd.cut(dep[dep.reintegre == 1].delai_reintegration_min, [0, 3, 15, 60], labels=['<=3min', '4-15min', '16-60min'])):
    descA.append({'famille': 'A_DEPASSEMENTS', 'dimension': 'DUREE_AU_DELA', 'valeur': v, 'n': len(g), 'jours': int(g.date.nunique()), 'grappes': int(g.grappe.nunique()),
                  'prof_med_bp': round(g.profondeur_bp.median(), 2), 'prof_P90_bp': round(g.profondeur_bp.quantile(.9), 2), 'taux_reintegration': 1.0, 'taux_censure': 0.0, 'delai_median_reintegres': float(g.delai_reintegration_min.median())})
cens = dep[dep.reintegre == 0]
descA.append({'famille': 'A_DEPASSEMENTS', 'dimension': 'DUREE_AU_DELA', 'valeur': 'CENSURE >60min', 'n': len(cens), 'jours': int(cens.date.nunique()), 'grappes': int(cens.grappe.nunique()),
              'prof_med_bp': round(cens.profondeur_bp.median(), 2), 'prof_P90_bp': round(cens.profondeur_bp.quantile(.9), 2), 'taux_reintegration': 0.0, 'taux_censure': 1.0, 'delai_median_reintegres': np.nan})
pd.DataFrame(descA).to_csv(OUT / 'CAMPAIGN_02_1_OVERSHOOT_ANALYSIS.csv', index=False)

descB = []
for nom, X, val in [('TOUTES_CASSURES', cas, 'reteste'), ('RETESTEES', ret, 'encore_au_dela_60'), ('NON_RETESTEES', cas[cas.reteste == 0], 'reintegre')]:
    descB.append({'famille': 'B_CASSURES', 'dimension': 'SOUS_ENSEMBLE', 'valeur': nom, 'n': len(X), 'jours': int(X.date.nunique()), 'grappes': int(X.grappe.nunique()),
                  'taux_variable': round(X[val].mean(), 4), 'delai_retest_median': float(ret.delai_retour_test_min.median()) if nom != 'NON_RETESTEES' else np.nan,
                  'prof_med_bp': round(X.profondeur_bp.median(), 2)})
for dim, col in [('SESSION', 'session'), ('ERE', 'ere'), ('REGIME', 'regime')]:
    for v, g in ret.groupby(col):
        descB.append({'famille': 'B_CASSURES', 'dimension': dim, 'valeur': v, 'n': len(g), 'jours': int(g.date.nunique()), 'grappes': int(g.grappe.nunique()),
                      'taux_variable': round(g.encore_au_dela_60.mean(), 4), 'delai_retest_median': float(g.delai_retour_test_min.median()), 'prof_med_bp': round(g.profondeur_bp.median(), 2)})
pd.DataFrame(descB).to_csv(OUT / 'CAMPAIGN_02_1_BREAKOUT_ANALYSIS.csv', index=False)
print(R[['test', 'ecart', 'p_BY_familleR']].to_string())
