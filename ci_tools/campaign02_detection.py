"""CAMPAGNE 2 - detection conditionnelle descriptive (plan gele seq162-164).
Bootstrap par grappes, BY sur 24 tests. Aucun PnL, aucune direction testee comme signal."""
import numpy as np, pandas as pd, pathlib, json
rng = np.random.default_rng(20261113)
OUT = pathlib.Path('reports/meta_alpha/campaign02'); OUT.mkdir(parents=True, exist_ok=True)
E = pd.read_csv('reports/meta_alpha/campaign01/CAMPAIGN_01_EVENTS_RAW.csv')
E4 = pd.read_csv('reports/meta_alpha/campaign01_1/EV4_EVENTS.csv')
OP = pd.read_csv('reports/meta_alpha/campaign01_1/CAMPAIGN_01_1_SESSION_OPENINGS.csv')
NB = 2000

def tercile_era(df, col):
    out = pd.Series(index=df.index, dtype=object)
    for _, idx in df.groupby('ere').groups.items():
        out.loc[idx] = pd.qcut(df.loc[idx, col], 3, labels=['BAS', 'MOYEN', 'HAUT'], duplicates='drop')
    return out

def cluster_arrays(df, val, cluster):
    groups = {}
    for c, v in zip(df[cluster], df[val]):
        if pd.notna(v): groups.setdefault(c, []).append(v)
    return [np.array(v, dtype=float) for v in groups.values()]

def boot_prop(A, B):
    # A,B: listes d'array par grappe (valeurs 0/1)
    def stat(gs): 
        s = sum(a.sum() for a in gs); n = sum(len(a) for a in gs); return s / n if n else np.nan
    obs = stat(A) - stat(B); reps = []
    for _ in range(NB):
        ra = [A[i] for i in rng.integers(0, len(A), len(A))]; rb = [B[i] for i in rng.integers(0, len(B), len(B))]
        reps.append(stat(ra) - stat(rb))
    reps = np.array(reps); p = min(1.0, 2 * min(float(np.mean(reps <= 0)), float(np.mean(reps >= 0))))
    return obs, float(np.quantile(reps, .025)), float(np.quantile(reps, .975)), float(p), stat(A), stat(B)

def boot_med(A, B):
    def stat(gs): return float(np.median(np.concatenate(gs))) if gs else np.nan
    obs = stat(A) / stat(B); reps = []
    for _ in range(NB):
        ra = [A[i] for i in rng.integers(0, len(A), len(A))]; rb = [B[i] for i in rng.integers(0, len(B), len(B))]
        reps.append(stat(ra) / stat(rb))
    reps = np.array(reps); lr = np.log(reps); p = min(1.0, 2 * min(float(np.mean(lr <= 0)), float(np.mean(lr >= 0))))
    return obs, float(np.quantile(reps, .025)), float(np.quantile(reps, .975)), float(p), stat(A), stat(B)

def by(pv):
    pv = np.asarray(pv, float); m = len(pv); order = np.argsort(pv); c = np.sum(1 / np.arange(1, m + 1))
    adj = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        rank = i + 1; val = min(prev, pv[order[i]] * m * c / rank); adj[order[i]] = min(val, 1.0); prev = adj[order[i]]
    return adj

def prep(df, val, cluster='grappe'):
    d = df.dropna(subset=[val]).copy(); d[val] = d[val].astype(float); return d

tests = []
def add(test, famille, bras, dfA, dfB, val, kind, cluster='grappe', seuil=0.05):
    A = cluster_arrays(prep(dfA, val, cluster), val, cluster); B = cluster_arrays(prep(dfB, val, cluster), val, cluster)
    fn = boot_prop if kind == 'prop' else boot_med
    obs, lo, hi, p, sa, sb = fn(A, B)
    tests.append({'test': test, 'famille': famille, 'comparaison': bras, 'variable': val, 'type': kind,
                  'n_A': int(sum(len(a) for a in A)), 'grappes_A': len(A), 'jours_A': int(dfA.date.nunique()),
                  'n_B': int(sum(len(b) for b in B)), 'grappes_B': len(B), 'jours_B': int(dfB.date.nunique()),
                  'stat_A': round(sa, 4), 'stat_B': round(sb, 4), 'ecart': round(float(obs), 4),
                  'ic95_bas': round(lo, 4), 'ic95_haut': round(hi, 4), 'p_brut': round(p, 5), 'seuil_materiel': seuil})
    print(test, tests[-1], flush=True)

dep = E[E.famille == 'EV2_DEPASSEMENT'].copy(); dep['reintegre'] = dep.delai_reintegration_min.notna().astype(float)
dep['censure'] = 1 - dep['reintegre']; dep['prof_t'] = tercile_era(dep, 'profondeur_bp')
add('T01', 'EV2', 'profondeur BAS vs HAUT', dep[dep.prof_t == 'BAS'], dep[dep.prof_t == 'HAUT'], 'reintegre', 'prop')
add('T02', 'EV2', 'ere 2010_2013 vs 2017_2020', dep[dep.ere == '2010_2013'], dep[dep.ere == '2017_2020'], 'reintegre', 'prop')
rei = dep[dep.reintegre == 1]
add('T03', 'EV2', 'delai, profondeur BAS vs HAUT', rei[rei.prof_t == 'BAS'], rei[rei.prof_t == 'HAUT'], 'delai_reintegration_min', 'med', seuil=0.15)
add('T04', 'EV2', 'regime BAS vs HAUT', dep[dep.regime == 'BAS'], dep[dep.regime == 'HAUT'], 'reintegre', 'prop')
add('T05', 'EV2', 'session Londres vs New York', dep[dep.session == 'LONDRES'], dep[dep.session == 'NEWYORK'], 'reintegre', 'prop')
add('T06', 'EV2', 'censure, profondeur BAS vs HAUT', dep[dep.prof_t == 'BAS'], dep[dep.prof_t == 'HAUT'], 'censure', 'prop')
cas = E[E.famille == 'EV3_CASSURE'].copy(); ret = E[E.famille == 'EV3_RETEST'].copy()
cas['reteste'] = cas.grappe.isin(set(ret.grappe)).astype(float)
add('T07', 'EV3', 'retest, regime BAS vs HAUT', cas[cas.regime == 'BAS'], cas[cas.regime == 'HAUT'], 'reteste', 'prop')
add('T08', 'EV3', 'encore au-dela, regime BAS vs HAUT', ret[ret.regime == 'BAS'], ret[ret.regime == 'HAUT'], 'encore_au_dela_60', 'prop')
add('T09', 'EV3', 'encore au-dela, ere 2010_2013 vs 2017_2020', ret[ret.ere == '2010_2013'], ret[ret.ere == '2017_2020'], 'encore_au_dela_60', 'prop')
ret['prof_t'] = tercile_era(ret, 'profondeur_bp')
add('T10', 'EV3', 'encore au-dela, profondeur BAS vs HAUT', ret[ret.prof_t == 'BAS'], ret[ret.prof_t == 'HAUT'], 'encore_au_dela_60', 'prop')
imp = E[E.famille == 'EV5_IMPULSION'].copy()
add('T11', 'EV5', 'retour100, ere 2010_2013 vs 2017_2020', imp[imp.ere == '2010_2013'], imp[imp.ere == '2017_2020'], 'retour_100', 'prop')
add('T12', 'EV5', 'retracement median, regime BAS vs HAUT', imp[imp.regime == 'BAS'], imp[imp.regime == 'HAUT'], 'retracement_max_pct', 'med', seuil=0.15)
add('T13', 'EV5', 'retour100, session ASIE vs NEWYORK', imp[imp.session == 'ASIE'], imp[imp.session == 'NEWYORK'], 'retour_100', 'prop')
cons = E[E.famille == 'EV6_CONSOLIDATION'].copy()
add('T14', 'EV6', 'range suivant, regime BAS vs HAUT', cons[cons.regime == 'BAS'], cons[cons.regime == 'HAUT'], 'range_suivant_60_bp', 'med', seuil=0.15)
add('T15', 'EV6', 'range suivant, ere 2010_2013 vs 2017_2020', cons[cons.ere == '2010_2013'], cons[cons.ere == '2017_2020'], 'range_suivant_60_bp', 'med', seuil=0.15)
E4['duree_long'] = (E4.duree_compression_min > E4.duree_compression_min.median()).astype(int)
add('T16', 'EV4', 'expansion1.5x, regime BAS vs HAUT', E4[E4.regime == 'BAS'], E4[E4.regime == 'HAUT'], 'expansion_1_5x', 'prop', cluster='date')
add('T17', 'EV4', 'range expansion, ere 2010_2013 vs 2017_2020', E4[E4.ere == '2010_2013'], E4[E4.ere == '2017_2020'], 'expansion_range_60_suivantes_bp', 'med', cluster='date', seuil=0.15)
add('T18', 'EV4', 'expansion1.5x, duree courte vs longue', E4[E4.duree_long == 0], E4[E4.duree_long == 1], 'expansion_1_5x', 'prop', cluster='date')
ny = OP[OP.ouverture == 'NEWYORK']; lon = OP[OP.ouverture == 'LONDRES']
add('T19', 'OUVERTURES', 'New York range60, ere 2010_2013 vs 2017_2020', ny[ny.ere == '2010_2013'], ny[ny.ere == '2017_2020'], 'range_60min_bp', 'med', cluster='date', seuil=0.15)
add('T20', 'OUVERTURES', 'New York extremes 5min, regime BAS vs HAUT', ny[ny.regime == 'BAS'], ny[ny.regime == 'HAUT'], 'mouvement_extreme_5min', 'prop', cluster='date')
add('T21', 'OUVERTURES', 'Londres spread apres, ere 2010_2013 vs 2017_2020', lon[lon.ere == '2010_2013'], lon[lon.ere == '2017_2020'], 'spread_apres_med_bp', 'med', cluster='date', seuil=0.15)
ev1 = E[E.famille == 'EV1_EXTREMES'].copy()
a1 = ev1[ev1.contexte == 'ASIE'].copy(); a1['dernier_tiers'] = (a1.heure_formation_haut >= 5.34).astype(float)
n1 = ev1[ev1.contexte == 'NEWYORK'].copy(); n1['dernier_tiers'] = (n1.heure_formation_haut >= 18.34).astype(float)
add('T22', 'EV1', 'extreme haut dernier tiers, ASIE vs NEWYORK', a1, n1, 'dernier_tiers', 'prop', seuil=9)
add('T23', 'EV2', 'spread evenement, reintegres vs censures', rei, dep[dep.reintegre == 0], 'spread_event', 'med', seuil=0.15)
add('T24', 'EV3/EV2', 'amp futur 60, apres retest vs apres reintegration', ret, E[E.famille == 'EV2_REINTEGRATION'], 'amp_futur_60', 'med', seuil=0.15)

R = pd.DataFrame(tests); R['p_BY'] = by(R.p_brut.values).round(5)
def verdict(r):
    if r.test == 'T24': return 'CONTEXTE (biais de selection, jamais anomalie)'
    if r.test == 'T06': return 'LIEN A T01 (complement mecanique)'
    materiel = abs(r.ecart) >= r.seuil_materiel if r.type == 'prop' else (r.ecart >= 1 + r.seuil_materiel or r.ecart <= 1 / (1 + r.seuil_materiel))
    suff = r.n_A >= 200 and r.n_B >= 200 and r.grappes_A >= 100 and r.grappes_B >= 100
    return 'J1_CANDIDATE_NOUVELLE' if (r.p_BY < 0.05 and materiel and suff) else 'NON_CONCLUANT_OU_QUEUE'
R['verdict_plan'] = R.apply(verdict, axis=1)
R.to_csv(OUT / 'CAMPAIGN_02_CONDITIONAL_BASELINES.csv', index=False)
print(R[['test', 'ecart', 'p_brut', 'p_BY', 'verdict_plan']].to_string())
