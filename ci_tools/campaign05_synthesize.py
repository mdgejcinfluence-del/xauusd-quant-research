"""CAMPAGNE 5 - synthese descriptive. Bootstrap par grappes-journees
(semaines pour C5-09), 2000 replicats, graine 20261113; BY separes par
famille (F-E, F-F). Aucune hypothese ajoutee."""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign05')
RNG = np.random.default_rng(20261113)
B = 2000

def boot_cluster(dfA, dfB, col, kind, cluster='date'):
    def by(df):
        return [g[col].dropna().values for _, g in df.groupby(cluster)]
    da, db = by(dfA), by(dfB)
    da = [x for x in da if len(x)]; db = [x for x in db if len(x)]
    if not da or not db: return (np.nan,) * 5 + (0, 0, 0, 0)
    va, vb = np.concatenate(da), np.concatenate(db)
    ea = np.mean(va) if kind == 'prop' else np.median(va)
    eb = np.mean(vb) if kind == 'prop' else np.median(vb)
    stat = (ea - eb) if kind == 'prop' else (ea / eb if eb != 0 else np.nan)
    diffs = []
    for _ in range(B):
        sa = np.concatenate([da[i] for i in RNG.integers(0, len(da), len(da))])
        sb = np.concatenate([db[i] for i in RNG.integers(0, len(db), len(db))])
        if kind == 'prop': diffs.append(np.mean(sa) - np.mean(sb))
        else:
            mb = np.median(sb); diffs.append(np.median(sa) / mb if mb != 0 else np.nan)
    diffs = np.array(diffs, float); diffs = diffs[~np.isnan(diffs)]
    if kind == 'prop':
        lo, hi = np.percentile(diffs, [2.5, 97.5]); p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    else:
        lo, hi = np.percentile(np.log(diffs[diffs > 0]), [2.5, 97.5]); lo, hi = float(np.exp(lo)), float(np.exp(hi))
        p = 2 * min((np.log(diffs[diffs > 0]) <= 0).mean(), (np.log(diffs[diffs > 0]) >= 0).mean())
    return stat, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), int(len(va)), int(len(vb)), int(len(da)), int(len(db))

def BY(pvals):
    p = np.asarray(pvals, float); m = len(p); H = sum(1 / i for i in range(1, m + 1))
    o = np.argsort(p); q = p[o] * m * H / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1.0)
    return out

META = [
 ('C5-01', 'F-E', 'med', "Amplitude ouverture 30 min (bp), LONDRES vs ASIE", 'ratio'),
 ('C5-02', 'F-E', 'prop', "P(poursuite +30 min), transition NEWYORK vs LONDRES", 'points'),
 ('C5-03', 'F-E', 'med', "Amplitude premiere heure Asie (bp), CONTINUITE vs TROU_INTRA_SEMAINE", 'ratio'),
 ('C5-04', 'F-E', 'med', "Amplitude ouverture Londres 30 min (bp), lundi vs vendredi", 'ratio'),
 ('C5-05', 'F-E', 'med', "Spread median 15 premieres minutes (bp), NEWYORK vs LONDRES", 'ratio'),
 ('C5-06', 'F-F', 'prop', "P(premiere atteinte reelle identifiable disponible avant 08:00), HAUT vs BAS", 'points'),
 ('C5-07', 'F-F', 'med', "Extension +60 min apres premiere atteinte reelle (bp), HAUT vs BAS", 'ratio'),
 ('C5-08', 'F-F', 'med', "Retracement +60 min (bp), atteintes disponibles avant 13:00 vs des 13:00", 'ratio'),
 ('C5-09', 'F-F', 'prop', "P(premiere atteinte hebdomadaire reelle disponible avant mercredi 00:00), HAUT vs BAS", 'points'),
 ('C5-10', 'F-F', 'prop', "P(journee CONTENUE ETABLIE), ere 2010-13 vs 2017-20", 'points')]

def main():
    OP = pd.read_csv(ROOT / 'CAMPAIGN_05_OPENINGS.csv.gz')
    ATT = pd.read_csv(ROOT / 'CAMPAIGN_05_ATTEINTES_JOUR.csv.gz')
    WATT = pd.read_csv(ROOT / 'CAMPAIGN_05_ATTEINTES_SEMAINE.csv')
    DFF = pd.read_csv(ROOT / 'CAMPAIGN_05_DAY_FF.csv')
    TOU = pd.read_csv(ROOT / 'CAMPAIGN_05_TOUCHES.csv')
    OPe = OP[OP.eligible == 1]
    res = {}
    def S(cid, a, b, col, kind, cluster='date'):
        res[cid] = boot_cluster(a, b, col, kind, cluster)
    # C5-01
    S('C5-01', OPe[(OPe.session == 'LONDRES') & (OPe.fenetre_30_statut != 'CENSUREE')], OPe[(OPe.session == 'ASIE') & (OPe.fenetre_30_statut != 'CENSUREE')], 'amplitude_30_bp', 'med')
    # C5-02
    T = OPe[OPe.session.isin(['NEWYORK', 'LONDRES']) & OPe.mouvement_pre60_bp.notna() & (OPe.mouvement_pre60_bp.abs() > 0) & (~OPe.issue_30.isin(['CENSURE', 'MOUVEMENT_NUL']))].copy()
    T['poursuite'] = T.issue_30.isin(['POURSUITE_SEULE', 'LES_DEUX']).astype(float)
    S('C5-02', T[T.session == 'NEWYORK'], T[T.session == 'LONDRES'], 'poursuite', 'prop')
    # C5-03
    A3 = OPe[(OPe.session == 'ASIE') & (OPe.fenetre_60_statut != 'CENSUREE')]
    S('C5-03', A3[A3.classe_ancrage_asie == 'CONTINUITE'], A3[A3.classe_ancrage_asie == 'TROU_INTRA_SEMAINE'], 'amplitude_60_bp', 'med')
    # C5-04
    A4 = OPe[(OPe.session == 'LONDRES') & (OPe.fenetre_30_statut != 'CENSUREE')]
    S('C5-04', A4[A4.jour_semaine == 0], A4[A4.jour_semaine == 4], 'amplitude_30_bp', 'med')
    # C5-05
    A5 = OPe[OPe.fenetre_15_statut != 'CENSUREE']
    S('C5-05', A5[A5.session == 'NEWYORK'], A5[A5.session == 'LONDRES'], 'spread_15_bp', 'med')
    # C5-06/07/08 : atteintes reelles identifiables, ordre determine
    if 'ordre_indetermine' not in ATT.columns: ATT['ordre_indetermine'] = 0
    R = ATT[(ATT.statut_atteinte == 'REELLE_IDENTIFIABLE') & (ATT.ordre_indetermine.fillna(0) == 0)].copy()
    R['avant8'] = (R.disponibilite_min < 480).astype(float)
    S('C5-06', R[R.cote == 'HAUT'], R[R.cote == 'BAS'], 'avant8', 'prop')
    R7 = R[R.censure_60 == 0]
    S('C5-07', R7[R7.cote == 'HAUT'], R7[R7.cote == 'BAS'], 'extension_60_bp', 'med')
    R8 = R.copy(); R8['groupe'] = np.where(R8.disponibilite_min < 780, 'A', 'B')
    S('C5-08', R8[R8.groupe == 'A'], R8[R8.groupe == 'B'], 'retracement_60_bp', 'med')
    # C5-09
    W = WATT[WATT.statut_atteinte == 'REELLE_IDENTIFIABLE'].copy()
    W['avant_mercredi_f'] = W.avant_mercredi.astype(float)
    res['C5-09'] = boot_cluster(W[W.cote == 'HAUT'], W[W.cote == 'BAS'], 'avant_mercredi_f', 'prop', cluster='semaine_lundi')
    # C5-10
    touch_dates = set(TOU.date.astype(str)) if len(TOU) else set()
    D = DFF[DFF.ff_usage == 'OK'].copy()
    D['a_evenement'] = ((D.atteinte_haut.fillna(0) + D.atteinte_bas.fillna(0)) > 0) | (D.date.astype(str).isin(touch_dates))
    D['contenue'] = D.contenue_etablie.fillna(0).astype(float)
    Dden = D[(D.contenue_etablie.fillna(0) == 1) | (D.a_evenement)]
    S('C5-10', Dden[Dden.ere == '2010_2013'], Dden[Dden.ere == '2017_2020'], 'contenue', 'prop')
    rows = []
    for cid, fam, kind, label, mat in META:
        stat, lo, hi, p, na, nb, ja, jb = res[cid]
        if mat == 'points': mat_ok = abs(stat) >= 0.05 if stat == stat else False
        else: mat_ok = (stat >= 1.15 or stat <= 1 / 1.15) if stat == stat else False
        rows.append({'id': cid, 'famille': fam, 'comparaison': label, 'type': kind, 'statistique': stat,
                     'ic95_bas': lo, 'ic95_haut': hi, 'p_brute': p, 'n_a': na, 'n_b': nb, 'grappes_a': ja, 'grappes_b': jb,
                     'seuil_materiel': '5 points' if mat == 'points' else 'ratio 1.15 symetrique', 'materiel': bool(mat_ok)})
    comp = pd.DataFrame(rows)
    comp['q_BY_famille'] = np.nan
    for fam, g in comp.groupby('famille'):
        comp.loc[g.index, 'q_BY_famille'] = BY(g.p_brute.values)
    def lecture(r):
        if not (r.n_a >= 200 and r.n_b >= 200 and r.grappes_a >= 100 and r.grappes_b >= 100): return 'NON_ELIGIBLE (effectifs publies)'
        if r.q_BY_famille < 0.05 and r.materiel: return 'CANDIDATE_J1'
        if r.q_BY_famille < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture, axis=1)
    comp.round(5).to_csv(ROOT / 'CAMPAIGN_05_COMPARISONS.csv', index=False)
    print(comp.to_string(index=False))

if __name__ == '__main__': main()
