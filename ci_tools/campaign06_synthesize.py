"""CAMPAGNE 6 - synthese descriptive F-G. Protocole gele V1.1+V1.2+V1.2.1+V1.2.2.
Bootstrap par grappes 2000 replicats, graine 20261113; BY famille de cinq
a m=5 FIXE (H5=2.283333) meme si une p est NaN; aucune hypothese ajoutee."""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign06')
RNG = np.random.default_rng(20261113)
B = 2000
LN115 = float(np.log(1.15))

def boot_med(a_clusters, b_clusters):
    """a_clusters/b_clusters: liste de tableaux par grappe. Diff de medianes."""
    a = [x for x in a_clusters if len(x)]; b = [x for x in b_clusters if len(x)]
    na = int(sum(len(x) for x in a)); nb = int(sum(len(x) for x in b))
    if not a or not b: return (np.nan,) * 4 + (na, nb, len(a), len(b)) + (np.array([]),)
    va, vb = np.concatenate(a), np.concatenate(b)
    stat = float(np.median(va) - np.median(vb))
    diffs = []
    for _ in range(B):
        sa = np.concatenate([a[i] for i in RNG.integers(0, len(a), len(a))])
        sb = np.concatenate([b[i] for i in RNG.integers(0, len(b), len(b))])
        diffs.append(np.median(sa) - np.median(sb))
    diffs = np.array(diffs)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return stat, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), na, nb, len(a), len(b), diffs

def clusters_par(df, col, grappe):
    return [g[col].dropna().values for _, g in df.groupby(grappe)]

def BY_m5(pvals):
    """BY avec m=5 fixe meme si certaines p sont NaN (publiees NaN)."""
    p = np.asarray(pvals, float); H5 = sum(1 / i for i in range(1, 6))
    ok = ~np.isnan(p); out = np.full(len(p), np.nan)
    if ok.sum() == 0: return out
    pv = p[ok]; o = np.argsort(pv); q = pv[o] * 5 * H5 / (np.arange(len(pv)) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    tmp = np.empty(len(pv)); tmp[o] = np.minimum(q, 1.0); out[ok] = tmp
    return out

META = [
 ('C6-01', "Persistance: ER_j selon classe de j-1 (DIRECTIONNELLE vs OSCILLANTE)", 'ER', 0.05),
 ('C6-02', "ER selon amplitude (tercile haut vs bas de A_bp, retrospectif)", 'ER', 0.05),
 ('C6-03', "ER lundi vs vendredi", 'ER', 0.05),
 ('C6-04', "Point median tau (min) selon signe de Delta_seg (+ vs -)", 'tau', 30.0),
 ('C6-05', "ER ere 2010-2013 vs 2017-2020", 'ER', 0.05)]

def main():
    D = pd.read_csv(ROOT / 'CAMPAIGN_06_DAYS.csv', parse_dates=['date'])
    E = D[D.eligible == 1].copy()
    details = {}
    res = {}
    # ---- C6-01 paires: jours presents successifs, aucun chainage a travers une censure
    D = D.sort_values('date').reset_index(drop=True)
    pairs = []
    for i in range(1, len(D)):
        prev, cur = D.iloc[i - 1], D.iloc[i]
        if prev.eligible == 1 and cur.eligible == 1 and prev.classe_forme in ('DIRECTIONNELLE', 'OSCILLANTE'):
            pairs.append({'date_j': cur.date, 'date_jm1': prev.date, 'semaine_lundi': cur.semaine_lundi,
                          'bras': prev.classe_forme, 'ER_j': cur.ER,
                          'ven_lun': int(cur.jour_semaine == 0 and prev.jour_semaine == 4)})
    P = pd.DataFrame(pairs)
    P.to_csv(ROOT / 'CAMPAIGN_06_PAIRES_C6_01.csv', index=False)
    details['C6-01'] = {'paires_total': int(len(P)), 'ven_lun': int(P.ven_lun.sum()) if len(P) else 0,
                        'semaines': int(P.semaine_lundi.nunique()) if len(P) else 0}
    if len(P):
        a = clusters_par(P[P.bras == 'DIRECTIONNELLE'], 'ER_j', 'semaine_lundi')
        b = clusters_par(P[P.bras == 'OSCILLANTE'], 'ER_j', 'semaine_lundi')
        res['C6-01'] = boot_med(a, b)
        # controle blocs mobiles de 2 semaines consecutives (IC seulement)
        semaines = sorted(P.semaine_lundi.unique())
        par_sem = {s: P[P.semaine_lundi == s] for s in semaines}
        blocs = [(semaines[i], semaines[i + 1]) for i in range(len(semaines) - 1)]
        nblocs_need = int(np.ceil(len(semaines) / 2))
        diffs_b, invalides = [], 0
        for _ in range(B):
            sel = [blocs[i] for i in RNG.integers(0, len(blocs), nblocs_need)] if blocs else []
            fa, fb = [], []
            for bloc in sel:
                for s in bloc:
                    g = par_sem[s]; fa += g[g.bras == 'DIRECTIONNELLE'].ER_j.tolist(); fb += g[g.bras == 'OSCILLANTE'].ER_j.tolist()
            if fa and fb: diffs_b.append(np.median(fa) - np.median(fb))
            else: invalides += 1
        diffs_b = np.array(diffs_b)
        details['C6-01'].update({'n_blocs_2sem': len(blocs), 'replicats_invalides': int(invalides),
                                 'taux_invalides_pct': round(invalides / B * 100, 2),
                                 'ic_blocs': [float(np.percentile(diffs_b, 2.5)), float(np.percentile(diffs_b, 97.5))] if len(diffs_b) else [np.nan, np.nan]})
    else:
        res['C6-01'] = (np.nan,) * 4 + (0, 0, 0, 0) + (np.array([]),)
        details['C6-01'].update({'n_blocs_2sem': 0, 'replicats_invalides': B, 'taux_invalides_pct': 100.0, 'ic_blocs': [np.nan, np.nan]})
    # ---- C6-02 terciles contemporains retrospectifs
    q33, q66 = E.A_bp.quantile(1 / 3), E.A_bp.quantile(2 / 3)
    A2, B2 = E[E.A_bp >= q66], E[E.A_bp <= q33]
    res['C6-02'] = boot_med(clusters_par(A2, 'ER', 'date'), clusters_par(B2, 'ER', 'date'))
    dec = {}
    for nom, g in [('haut', A2), ('bas', B2)]:
        dec[nom] = {'n': int(len(g)), 'ER_med': float(g.ER.median()), 'S_med': float(g.S.median()),
                    'abs_delta_sur_A_med': float(g.abs_delta_seg_sur_A.median()),
                    'L_bp_med': float(g.L_bp.median()), 'A_bp_med': float(g.A_bp.median())}
    dec['terciles_seuils_bp'] = [float(q33), float(q66)]
    dec['ln_ratio_abs_delta_sur_A'] = float(np.log(dec['haut']['abs_delta_sur_A_med'] / dec['bas']['abs_delta_sur_A_med']))
    dec['ln_ratio_S'] = float(np.log(dec['haut']['S_med'] / dec['bas']['S_med']))
    details['C6-02'] = dec
    # ---- C6-03 / C6-04 / C6-05
    res['C6-03'] = boot_med(clusters_par(E[E.jour_semaine == 0], 'ER', 'date'), clusters_par(E[E.jour_semaine == 4], 'ER', 'date'))
    res['C6-04'] = boot_med(clusters_par(E[E.delta_seg_bp >= 5], 'tau_min', 'date'), clusters_par(E[E.delta_seg_bp <= -5], 'tau_min', 'date'))
    res['C6-05'] = boot_med(clusters_par(E[E.ere == '2010_2013'], 'ER', 'date'), clusters_par(E[E.ere == '2017_2020'], 'ER', 'date'))
    for cid in ['C6-02', 'C6-03', 'C6-04', 'C6-05']:
        g = {'C6-02': (A2, B2), 'C6-03': (E[E.jour_semaine == 0], E[E.jour_semaine == 4]),
             'C6-04': (E[E.delta_seg_bp >= 5], E[E.delta_seg_bp <= -5]),
             'C6-05': (E[E.ere == '2010_2013'], E[E.ere == '2017_2020'])}[cid]
        col = 'tau_min' if cid == 'C6-04' else 'ER'
        details[cid] = details.get(cid, {}) | {'mediane_a': float(g[0][col].median()), 'mediane_b': float(g[1][col].median())}
    # ---- tableau, BY m=5 fixe, lectures
    rows = []
    for cid, label, kind, mat in META:
        stat, lo, hi, p, na, nb, ga, gb, _ = res[cid]
        rows.append({'id': cid, 'comparaison': label, 'type': kind, 'statistique_diff_medianes': stat,
                     'ic95_bas': lo, 'ic95_haut': hi, 'p_brute': p, 'n_a': na, 'n_b': nb,
                     'grappes_a': ga, 'grappes_b': gb,
                     'seuil_materiel': '0.05 ER' if kind == 'ER' else '30 min', 'materiel': bool(abs(stat) >= mat) if stat == stat else False})
    comp = pd.DataFrame(rows)
    comp['q_BY_m5'] = BY_m5(comp.p_brute.values)
    def lecture_base(r):
        if (r.n_a == 0 or r.n_b == 0) and r.p_brute != r.p_brute: return 'STRUCTURELLEMENT_NON_EVALUABLE'
        if not (r.n_a >= 200 and r.n_b >= 200 and r.grappes_a >= 100 and r.grappes_b >= 100): return 'NON_ELIGIBLE (effectifs publies)'
        if r.q_BY_m5 < 0.05 and r.materiel: return 'CANDIDATE_J1'
        if r.q_BY_m5 < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture_base, axis=1)
    # ---- C6-01: regle prudente figee (priorite V1.2.1)
    r1 = comp[comp.id == 'C6-01'].iloc[0]; d1 = details['C6-01']; e = r1.statistique_diff_medianes
    icb = d1['ic_blocs']
    if d1['n_blocs_2sem'] < 30 or d1['taux_invalides_pct'] > 5 or e == 0:
        statut_controle = 'CONTROLE_INDETERMINE'
    elif (icb[0] <= 0 <= icb[1]) or (icb[0] * e < 0 and icb[1] * e < 0):
        statut_controle = 'FRAGILE_SIGNE'
    elif r1.lecture == 'CANDIDATE_J1' and min(abs(icb[0]), abs(icb[1])) < 0.05:
        statut_controle = 'FRAGILE_MATERIALITE'
    else:
        statut_controle = 'ROBUSTE'
    details['C6-01']['statut_controle'] = statut_controle
    details['C6-01']['inversion_controle'] = bool(icb[0] * e < 0 and icb[1] * e < 0) if e == e else False
    lec = r1.lecture
    if statut_controle == 'FRAGILE_SIGNE' and lec in ('CANDIDATE_J1', 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'):
        lec = 'NEGATIF (non robuste au controle par blocs)'
    elif statut_controle == 'FRAGILE_MATERIALITE' and lec == 'CANDIDATE_J1':
        lec = 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL (robustesse de materialite non etablie au controle par blocs)'
    elif statut_controle == 'CONTROLE_INDETERMINE' and lec in ('CANDIDATE_J1', 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'):
        lec = 'NON_ELIGIBLE (controle indetermine)'
    comp.loc[comp.id == 'C6-01', 'lecture'] = lec
    details['C6-01']['lecture_avant_controle'] = str(r1.lecture)
    # ---- C6-02: declassement ferme
    r2 = comp[comp.id == 'C6-02'].iloc[0]
    if r2.q_BY_m5 < 0.05 and abs(r2.statistique_diff_medianes) >= 0.05:
        lnA, lnS = details['C6-02']['ln_ratio_abs_delta_sur_A'], details['C6-02']['ln_ratio_S']
        meme_sens = (lnA * r2.statistique_diff_medianes) > 0
        if meme_sens and abs(lnA) > LN115 and abs(lnS) <= LN115:
            comp.loc[comp.id == 'C6-02', 'lecture'] = 'DECLASSE_DEPLACEMENT_RELATIF (pas une forme pure)'
            details['C6-02']['declassement'] = True
        else: details['C6-02']['declassement'] = False
    else: details['C6-02']['declassement'] = False
    comp.round(6).to_csv(ROOT / 'CAMPAIGN_06_COMPARISONS.csv', index=False)
    (ROOT / 'CAMPAIGN_06_DETAILS.json').write_text(json.dumps(details, indent=1, default=str))
    print(comp.to_string(index=False))
    print(json.dumps(details, indent=1, default=str))

if __name__ == '__main__': main()
