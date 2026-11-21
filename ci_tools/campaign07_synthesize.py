"""CAMPAGNE 7 - synthese descriptive F-I. Protocole gele V1 (seq250).
Bootstrap grappes-journees 2000 replicats graine 20261113; BY famille de
cinq a m=5 FIXE; controle de composition deterministe sans p ajoutee."""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign07')
RNG = np.random.default_rng(20261113)
B = 2000

def clus(df, col):
    return [g[col].dropna().values.astype(float) for _, g in df.groupby('date')]

def boot_prop(a, b, col):
    def sommes(df):
        g = df.groupby('date')[col].agg(['sum', 'count'])
        return g['sum'].values.astype(float), g['count'].values.astype(float)
    sa, na_ = sommes(a); sb, nb_ = sommes(b)
    na, nb = int(na_.sum()), int(nb_.sum())
    if len(sa) == 0 or len(sb) == 0: return (np.nan,) * 4 + (na, nb, len(sa), len(sb))
    stat = float(sa.sum() / na_.sum() - sb.sum() / nb_.sum())
    ia = RNG.integers(0, len(sa), (B, len(sa))); ib = RNG.integers(0, len(sb), (B, len(sb)))
    ma = sa[ia].sum(axis=1) / na_[ia].sum(axis=1); mb = sb[ib].sum(axis=1) / nb_[ib].sum(axis=1)
    diffs = ma - mb
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return stat, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), na, nb, len(sa), len(sb)

def boot_ratio(a, b, col):
    ca, cb = clus(a, col), clus(b, col)
    ca = [x for x in ca if len(x)]; cb = [x for x in cb if len(x)]
    na, nb = int(sum(map(len, ca))), int(sum(map(len, cb)))
    if not ca or not cb: return (np.nan,) * 4 + (na, nb, len(ca), len(cb))
    ma, mb = np.median(np.concatenate(ca)), np.median(np.concatenate(cb))
    stat = float(ma / mb) if mb != 0 else np.nan
    rats = []
    for _ in range(B):
        sa = np.concatenate([ca[i] for i in RNG.integers(0, len(ca), len(ca))])
        sb = np.concatenate([cb[i] for i in RNG.integers(0, len(cb), len(cb))])
        m2 = np.median(sb); rats.append(np.median(sa) / m2 if m2 != 0 else np.nan)
    rats = np.array(rats, float); rats = rats[rats > 0]
    lo, hi = np.exp(np.percentile(np.log(rats), [2.5, 97.5]))
    p = 2 * min((np.log(rats) <= 0).mean(), (np.log(rats) >= 0).mean())
    return stat, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), na, nb, len(ca), len(cb)

def BY_m5(pvals):
    p = np.asarray(pvals, float); H5 = sum(1 / i for i in range(1, 6))
    ok = ~np.isnan(p); out = np.full(len(p), np.nan)
    if ok.sum() == 0: return out
    pv = p[ok]; o = np.argsort(pv); q = pv[o] * 5 * H5 / (np.arange(len(pv)) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    tmp = np.empty(len(pv)); tmp[o] = np.minimum(q, 1.0); out[ok] = tmp
    return out

def composition(a, b):
    """Controle gele: eres, sessions, sens, distance initiale, exposition. Aucun test."""
    det = {}
    seuils_depasse = False
    for var in ['ere', 'session', 'cote']:
        pa = a[var].value_counts(normalize=True); pb = b[var].value_counts(normalize=True)
        cats = set(pa.index) | set(pb.index)
        diffs = {str(k): float(abs(pa.get(k, 0) - pb.get(k, 0)) * 100) for k in cats}
        det[f'ecarts_pts_{var}'] = diffs
        if diffs and max(diffs.values()) >= 5.0: seuils_depasse = True
    dmed = float(abs(a.distance_initiale_bp.median() - b.distance_initiale_bp.median()))
    det['ecart_distance_initiale_mediane_bp'] = dmed
    if dmed >= 2.0: seuils_depasse = True
    expo = (len(a) / len(b)) if len(b) else np.nan
    det['ratio_exposition_episodes'] = float(expo)
    if not (0.8695652173913043 <= expo <= 1.15): seuils_depasse = True
    # strates ere x session x cote
    def cnt(df): return df.groupby(['ere', 'session', 'cote']).size()
    ca_, cb_ = cnt(a), cnt(b)
    def part_sans_comparable(df, autre):
        tot = len(df); s = 0
        for (k, v) in df.groupby(['ere', 'session', 'cote']).size().items():
            if autre.get(k, 0) < 30: s += v
        return s / tot if tot else 0.0
    p_ab = part_sans_comparable(a, cb_); p_ba = part_sans_comparable(b, ca_)
    det['part_sans_strate_comparable'] = [float(p_ab), float(p_ba)]
    if dmed > 10.0 or max(p_ab, p_ba) > 0.25: statut = 'NON_EVALUABLE_COMPOSITION'
    elif seuils_depasse: statut = 'SENSIBLE_A_LA_COMPOSITION'
    else: statut = 'CONSERVEE'
    det['statut'] = statut
    return statut, det

def main():
    EP = pd.read_csv(ROOT / 'CAMPAIGN_07_EPISODES.csv.gz')
    details = {}
    prim = EP[(EP.saut == 0) & (EP.simultane == 0)].copy()
    # populations resolues
    def approches_resolues(df):
        r = df[df.terminal.isin(['FRANCHISSEMENT', 'REJET', 'SANS_EFFET'])].copy()
        r['issue'] = (r.terminal == 'FRANCHISSEMENT').astype(float)
        return r
    A = approches_resolues(prim)
    details['populations'] = {
        'episodes_bruts_par_grille': {k: int(v) for k, v in EP.grille.value_counts().items()},
        'saut': int(EP.saut.sum()), 'simultanes': int(EP.simultane.sum()),
        'censures_jour': int((EP.terminal == 'CENSURE_JOUR').sum()),
        'approches_resolues_par_grille': {k: int(v) for k, v in A.grille.value_counts().items()}}
    res = {}
    res['I-01'] = boot_prop(A[A.grille == 'G50'], A[A.grille == 'P50'], 'issue')
    T = prim[(prim.touche == 1) & prim.terminal.isin(['REJET', 'FRANCHISSEMENT', 'SANS_EFFET'])].copy()
    T['issue'] = (T.terminal == 'REJET').astype(float)
    res['I-02'] = boot_prop(T[T.grille == 'G50'], T[T.grille == 'P50'], 'issue')
    F = prim[(prim.franchissement == 1) & (prim.suivi_complet == 1)].copy()
    res['I-03'] = boot_ratio(F[F.grille == 'G50'], F[F.grille == 'P50'], 'distance_post_bp')
    res['I-04'] = boot_prop(A[A.grille == 'R100'], A[A.grille == 'R10'], 'issue')
    # I-05: bootstrap par journees au sein de chaque ere (grilles ensemble)
    def boot_i05():
        cells = {}
        for ere in ['2010_2013', '2017_2020']:
            for g in ['G50', 'P50']:
                cells[(ere, g)] = A[(A.ere == ere) & (A.grille == g)]
        def effet(sample_dates):
            ps = {}
            for (ere, g), df in cells.items():
                sub = df[df.date.isin(sample_dates[ere])]
                ps[(ere, g)] = sub.issue.mean() if len(sub) else np.nan
            return (ps[('2010_2013', 'G50')] - ps[('2010_2013', 'P50')]) - (ps[('2017_2020', 'G50')] - ps[('2017_2020', 'P50')])
        dates = {ere: sorted(A[A.ere == ere].date.unique()) for ere in ['2010_2013', '2017_2020']}
        stat = effet(dates)
        diffs = []
        for _ in range(B):
            sd = {ere: RNG.choice(dates[ere], size=len(dates[ere]), replace=True) for ere in dates}
            # reconstruire avec multiplicites: dupliquer les episodes par tirage
            ps = {}
            for (ere, g), df in cells.items():
                cnt = pd.Series(sd[ere]).value_counts()
                vals = np.concatenate([np.repeat(df[df.date == d].issue.values, 1) for d in []]) if False else None
                sub = df.set_index('date').loc[[d for d in sd[ere] if d in set(df.date)]]
                ps[(ere, g)] = sub.issue.mean() if len(sub) else np.nan
            diffs.append((ps[('2010_2013', 'G50')] - ps[('2010_2013', 'P50')]) - (ps[('2017_2020', 'G50')] - ps[('2017_2020', 'P50')]))
        diffs = np.array(diffs, float)
        lo, hi = np.nanpercentile(diffs, [2.5, 97.5])
        p = 2 * min(np.nanmean(diffs <= 0), np.nanmean(diffs >= 0))
        na = int(len(cells[('2010_2013', 'G50')]) + len(cells[('2010_2013', 'P50')]))
        nb = int(len(cells[('2017_2020', 'G50')]) + len(cells[('2017_2020', 'P50')]))
        ga = int(A[A.ere == '2010_2013'].date.nunique()); gb = int(A[A.ere == '2017_2020'].date.nunique())
        return float(stat), float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), na, nb, ga, gb
    res['I-05'] = boot_i05()
    details['I-05_cellules'] = {f'{e}_{g}': {'n': int(len(A[(A.ere == e) & (A.grille == g)])), 'p_franchissement': float(A[(A.ere == e) & (A.grille == g)].issue.mean())}
                                for e in ['2010_2013', '2014_2016', '2017_2020'] for g in ['G50', 'P50']}
    # controle de composition (aucune p creee)
    compo = {}
    paires = {'I-01': (A[A.grille == 'G50'], A[A.grille == 'P50']),
              'I-02': (T[T.grille == 'G50'], T[T.grille == 'P50']),
              'I-03': (F[F.grille == 'G50'], F[F.grille == 'P50'])}
    for cid, (a, b) in paires.items():
        st, det = composition(a, b); compo[cid] = det; details[f'composition_{cid}'] = det
    # I-05: composition par ere, statut le plus severe
    sts = []
    for ere in ['2010_2013', '2017_2020']:
        st, det = composition(A[(A.ere == ere) & (A.grille == 'G50')], A[(A.ere == ere) & (A.grille == 'P50')])
        sts.append(st); details[f'composition_I-05_{ere}'] = det
    compo['I-05'] = 'NON_EVALUABLE_COMPOSITION' if 'NON_EVALUABLE_COMPOSITION' in sts else ('SENSIBLE_A_LA_COMPOSITION' if 'SENSIBLE_A_LA_COMPOSITION' in sts else 'CONSERVEE')
    details['taux_bruts'] = {
        'I-01': {g: float(A[A.grille == g].issue.mean()) for g in ['G50', 'P50']},
        'I-02': {g: float(T[T.grille == g].issue.mean()) for g in ['G50', 'P50']},
        'I-03_medianes_bp': {g: float(F[F.grille == g].distance_post_bp.median()) for g in ['G50', 'P50']},
        'I-04': {g: float(A[A.grille == g].issue.mean()) for g in ['R100', 'R10']}}
    META = [('I-01', "P(franchissement strict|approche) G50 vs P50", 'points', 0.05),
            ('I-02', "P(rejet|touche) G50 vs P50", 'points', 0.05),
            ('I-03', "Distance post-franchissement (ratio medianes) G50 vs P50", 'ratio', None),
            ('I-04', "P(franchissement|approche) R100 vs R10", 'points', 0.05),
            ('I-05', "Ecart (G50-P50) de P(franchissement): 2010-13 moins 2017-20", 'points', 0.05)]
    rows = []
    for cid, label, kind, mat in META:
        stat, lo, hi, p, na, nb, ga, gb = res[cid]
        if kind == 'points': materiel = bool(abs(stat) >= mat) if stat == stat else False
        else: materiel = bool(stat >= 1.15 or stat <= 1 / 1.15) if stat == stat else False
        rows.append({'id': cid, 'comparaison': label, 'type': kind, 'statistique': stat, 'ic95_bas': lo, 'ic95_haut': hi,
                     'p_brute': p, 'n_a': na, 'n_b': nb, 'grappes_a': ga, 'grappes_b': gb,
                     'seuil_materiel': '5 points' if kind == 'points' else 'ratio 1.15 symetrique', 'materiel': materiel,
                     'composition': compo.get(cid, 'NON_APPLIQUE (anneaux reels)')})
    comp = pd.DataFrame(rows)
    comp['q_BY_m5'] = BY_m5(comp.p_brute.values)
    def lecture(r):
        if (r.n_a == 0 or r.n_b == 0) and r.p_brute != r.p_brute: return 'STRUCTURELLEMENT_NON_EVALUABLE'
        if not (r.n_a >= 200 and r.n_b >= 200 and r.grappes_a >= 100 and r.grappes_b >= 100): return 'NON_ELIGIBLE (effectifs publies)'
        if r.composition == 'NON_EVALUABLE_COMPOSITION': return 'NON_EVALUABLE_COMPOSITION (pas de candidate)'
        if r.q_BY_m5 < 0.05 and r.materiel:
            return 'ASSOCIATION_SENSIBLE_A_LA_COMPOSITION (pas de candidate)' if r.composition == 'SENSIBLE_A_LA_COMPOSITION' else 'CANDIDATE_J1'
        if r.q_BY_m5 < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture, axis=1)
    comp.round(6).to_csv(ROOT / 'CAMPAIGN_07_COMPARISONS.csv', index=False)
    (ROOT / 'CAMPAIGN_07_DETAILS.json').write_text(json.dumps(details, indent=1, default=str))
    print(comp.to_string(index=False))

if __name__ == '__main__': main()
