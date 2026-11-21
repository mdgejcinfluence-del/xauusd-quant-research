"""CAMPAGNE 3 - synthese descriptive (bootstrap journees, BY sur les 12 gelees).
Lit les bruts CI, ne recalcule aucune definition; produit les tableaux livres."""
import pathlib, json
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign03')
RNG = np.random.default_rng(20261113)
B = 2000

def wmedian(vals, w):
    o = np.argsort(vals); v, ww = vals[o], w[o].astype(float)
    cw = np.cumsum(ww); tot = cw[-1]
    return float(v[np.searchsorted(cw, 0.5 * tot)])

def boot_stat(days_vals, kind):
    """days_vals: liste (valeurs array) par journee. Retourne estimateur sur tout."""
    vals = np.concatenate([v for v in days_vals if len(v)])
    return float(np.mean(vals)) if kind == 'prop' else float(np.median(vals))

def bootstrap(days_a, days_b, kind):
    da = [np.asarray(v, float) for v in days_a if len(v)]
    db = [np.asarray(v, float) for v in days_b if len(v)]
    if not da or not db: return np.nan, np.nan, np.nan, np.nan, 0, 0
    est_a, est_b = boot_stat(da, kind), boot_stat(db, kind)
    diffs = []
    all_days = da + db; # resampling separe par bras (grappes du bras)
    for _ in range(B):
        sa = [da[i] for i in RNG.integers(0, len(da), len(da))]
        sb = [db[i] for i in RNG.integers(0, len(db), len(db))]
        va, vb = np.concatenate(sa), np.concatenate(sb)
        diffs.append((np.mean(va) - np.mean(vb)) if kind == 'prop' else (np.median(va) - np.median(vb)))
    diffs = np.array(diffs)
    diff = est_a - est_b
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean()) if diff != 0 else 1.0
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return diff, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), len(da), len(db)

def BY(pvals):
    p = np.asarray(pvals, float); m = len(p); H = sum(1 / i for i in range(1, m + 1))
    o = np.argsort(p); ranked = p[o]; q = ranked * m * H / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1.0)
    return out

def by_days(df, col, mask):
    sub = df[mask & df[col].notna()]
    return [g[col].values for _, g in sub.groupby('date')]

def compare(cid, fam, label, df, col, kind, bras_a, bras_b, mat_kind):
    ma, mb = bras_a(df), bras_b(df)
    da, db = by_days(df, col, ma), by_days(df, col, mb)
    na = int(sum(len(x) for x in da)); nb = int(sum(len(x) for x in db))
    diff, lo, hi, p, ja, jb = bootstrap(da, db, kind)
    va = np.concatenate(da) if da else np.array([]); vb = np.concatenate(db) if db else np.array([])
    ea = float(np.mean(va)) if kind == 'prop' and len(va) else (float(np.median(va)) if len(va) else np.nan)
    eb = float(np.mean(vb)) if kind == 'prop' and len(vb) else (float(np.median(vb)) if len(vb) else np.nan)
    ratio = (ea / eb) if (kind == 'med' and eb not in (0, np.nan) and not np.isnan(eb)) else np.nan
    suf = (na >= 200 and nb >= 200 and ja >= 100 and jb >= 100)
    return {'id': cid, 'famille': fam, 'comparaison': label, 'type': kind, 'n_a': na, 'journees_a': ja,
            'n_b': nb, 'journees_b': jb, 'estim_a': ea, 'estim_b': eb, 'diff_a_moins_b': diff,
            'ic95_bas': lo, 'ic95_haut': hi, 'ratio_medianes': ratio, 'p_brute': p, 'suffisance': bool(suf)}

def main():
    e5 = pd.read_csv(ROOT / 'CAMPAIGN_03_EPISODES_IMP_M5.csv')
    e15 = pd.read_csv(ROOT / 'CAMPAIGN_03_EPISODES_IMP_M15.csv')
    ec = pd.read_csv(ROOT / 'CAMPAIGN_03_EPISODES_CONS.csv')
    s5 = pd.read_csv(ROOT / 'CAMPAIGN_03_SNAPSHOTS_IMP.csv'); simp = s5.copy()
    for e in (e5, e15): e['retr_complet'] = e.t100_barres.notna().astype(float)
    e5['stagnation'] = (e5.trajectoire_60min == 'STAGNATION').astype(float)
    e15['continuation'] = (e15.trajectoire_60min == 'CONTINUATION').astype(float)
    ec['sortie_barre'] = (ec.type_sortie == 'BARRE_RANGE').astype(float)
    s_m5 = simp[(simp.famille == 'IMP-M5')]; s_m15 = simp[(simp.famille == 'IMP-M15')]
    rows = []
    rows.append(compare('C3-01', 'IMP-M5', 'P(retracement complet) HAUSSE vs BAISSE', e5, 'retr_complet', 'prop', lambda d: d.direction == 'HAUSSE', lambda d: d.direction == 'BAISSE', 'prop'))
    rows.append(compare('C3-02', 'IMP-M5', 'P(retracement complet) LONDRES vs ASIE', e5, 'retr_complet', 'prop', lambda d: d.session == 'LONDRES', lambda d: d.session == 'ASIE', 'prop'))
    rows.append(compare('C3-03', 'IMP-M5', 'Retracement ulterieur apres +12 barres (bp) amplitude BAS vs HAUT', s_m5[s_m5.snapshot_barres == 12], 'retracement_ulterior_bp', 'med', lambda d: d.groupe_amplitude_causal == 'BAS', lambda d: d.groupe_amplitude_causal == 'HAUT', 'med'))
    rows.append(compare('C3-04', 'IMP-M5', 'P(stagnation) regime BAS vs HAUT', e5, 'stagnation', 'prop', lambda d: d.regime == 'BAS', lambda d: d.regime == 'HAUT', 'prop'))
    rows.append(compare('C3-05', 'IMP-M5', 'Retracement ulterieur apres T0 (bp) ere 2010-13 vs 2017-20', s_m5[s_m5.snapshot_barres == 0], 'retracement_ulterior_bp', 'med', lambda d: d.ere == '2010_2013', lambda d: d.ere == '2017_2020', 'med'))
    rows.append(compare('C3-06', 'IMP-M15', 'P(retracement complet) HAUSSE vs BAISSE', e15, 'retr_complet', 'prop', lambda d: d.direction == 'HAUSSE', lambda d: d.direction == 'BAISSE', 'prop'))
    rows.append(compare('C3-07', 'IMP-M15', 'Extension supplementaire apres +12 barres (bp) amplitude BAS vs HAUT', s_m15[s_m15.snapshot_barres == 12], 'extension_supplementaire_bp', 'med', lambda d: d.groupe_amplitude_causal == 'BAS', lambda d: d.groupe_amplitude_causal == 'HAUT', 'med'))
    rows.append(compare('C3-08', 'IMP-M15', 'P(continuation) LONDRES vs ASIE', e15, 'continuation', 'prop', lambda d: d.session == 'LONDRES', lambda d: d.session == 'ASIE', 'prop'))
    rows.append(compare('C3-09', 'CONS', 'P(sortie BARRE_RANGE) range de formation BAS vs HAUT', ec, 'sortie_barre', 'prop', lambda d: d.groupe_range_formation == 'BAS', lambda d: d.groupe_range_formation == 'HAUT', 'prop'))
    rows.append(compare('C3-10', 'CONS', 'Range post-sortie 60min (bp) CLOTURE_HORS_RANGE vs BARRE_RANGE', ec[ec.type_sortie != 'CENSUREE'], 'range_post_sortie_60_bp', 'med', lambda d: d.type_sortie == 'CLOTURE_HORS_RANGE', lambda d: d.type_sortie == 'BARRE_RANGE', 'med'))
    rows.append(compare('C3-11', 'CONS', 'P(censure +120min) LONDRES vs ASIE', ec, 'censuree', 'prop', lambda d: d.session == 'LONDRES', lambda d: d.session == 'ASIE', 'prop'))
    rows.append(compare('C3-12', 'CONS', 'Duree consolidation (min) ere 2010-13 vs 2017-20', ec, 'duree_consolidation_min', 'med', lambda d: d.ere == '2010_2013', lambda d: d.ere == '2017_2020', 'med'))
    comp = pd.DataFrame(rows)
    comp['q_BY'] = BY(comp.p_brute.fillna(1.0).values)
    def lecture(r):
        if not r.suffisance: return 'NON_CONCLUANT (suffisance)'
        mat = (abs(r.diff_a_moins_b) >= 5) if r.type == 'prop' and False else None
        if r.type == 'prop':
            mat_ok = abs(r.diff_a_moins_b) >= 0.05
        else:
            mat_ok = (r.ratio_medianes >= 1.15 or r.ratio_medianes <= 1 / 1.15) if not np.isnan(r.ratio_medianes) else False
        if r.q_BY < 0.05 and mat_ok: return 'CANDIDATE_J1'
        if r.q_BY < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture, axis=1)
    comp.to_csv(ROOT / 'CAMPAIGN_03_COMPARISONS.csv', index=False)
    # coherence par ere (signe) pour comparaisons hors ere
    # statistiques d'instantanes
    stats = []
    for df, fam, unite in [(s_m5, 'IMP-M5', 'barres'), (s_m15, 'IMP-M15', 'barres')]:
        for (snap, ctx_type, ctx), g in list(df.groupby(['snapshot_barres', 'session']).__iter__()) if False else []:
            pass
    def agg(df, fam, snapcol, groupcols, cols):
        out = []
        for keys, g in df.groupby(groupcols):
            r = {'famille': fam, **{c: k for c, k in zip(groupcols, keys if isinstance(keys, tuple) else (keys,))}, 'n': len(g), 'journees': g.date.nunique()}
            for c in cols:
                v = g[c].dropna()
                if len(v): r[f'{c}_med'] = float(v.median()); r[f'{c}_p25'] = float(v.quantile(.25)); r[f'{c}_p75'] = float(v.quantile(.75))
            out.append(r)
        return out
    cols_imp = ['amplitude_cumulee_bp', 'retracement_max_jusqua_bp', 'retracement_ulterior_bp', 'extension_supplementaire_bp', 'vol_realisee_bp']
    rows_s = []
    rows_s += agg(s_m5, 'IMP-M5', 'snapshot_barres', ['snapshot_barres'], cols_imp)
    rows_s += agg(s_m15, 'IMP-M15', 'snapshot_barres', ['snapshot_barres'], cols_imp)
    rows_s += agg(s_m5, 'IMP-M5', 'snapshot_barres', ['snapshot_barres', 'session'], cols_imp)
    rows_s += agg(s_m5, 'IMP-M5', 'snapshot_barres', ['snapshot_barres', 'ere'], cols_imp)
    rows_s += agg(s_m5, 'IMP-M5', 'snapshot_barres', ['snapshot_barres', 'regime'], cols_imp)
    rows_s += agg(s_m15, 'IMP-M15', 'snapshot_barres', ['snapshot_barres', 'session'], cols_imp)
    sc = pd.read_csv(ROOT / 'CAMPAIGN_03_SNAPSHOTS_CONS.csv')
    rows_s += agg(sc, 'CONS', 'snapshot_min', ['snapshot_min'], ['range_cumule_bp', 'position_dans_range', 'ratio_compression', 'vol_realisee_bp'])
    rows_s += agg(sc, 'CONS', 'snapshot_min', ['snapshot_min', 'session'], ['range_cumule_bp', 'ratio_compression'])
    pd.DataFrame(rows_s).to_csv(ROOT / 'CAMPAIGN_03_SNAPSHOT_STATS.csv', index=False)
    # metriques evenements / trajectoires / issues
    met = []
    for df, fam in [(e5, 'IMP-M5'), (e15, 'IMP-M15')]:
        for keys, g in df.groupby('trajectoire_60min'):
            met.append({'famille': fam, 'dimension': 'trajectoire_60min', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(df), 2)})
        for keys, g in df.groupby('session'):
            met.append({'famille': fam, 'dimension': 'session', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(df), 2)})
        for keys, g in df.groupby('ere'):
            met.append({'famille': fam, 'dimension': 'ere', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(df), 2)})
        for keys, g in df.groupby('direction'):
            met.append({'famille': fam, 'dimension': 'direction', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(df), 2)})
    for keys, g in ec.groupby('type_sortie'):
        met.append({'famille': 'CONS', 'dimension': 'type_sortie', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(ec), 2)})
    for keys, g in ec.groupby('session'):
        met.append({'famille': 'CONS', 'dimension': 'session', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(ec), 2)})
    for keys, g in ec.groupby('ere'):
        met.append({'famille': 'CONS', 'dimension': 'ere', 'modalite': keys, 'n': len(g), 'journees': g.date.nunique(), 'part_pct': round(100 * len(g) / len(ec), 2)})
    pd.DataFrame(met).to_csv(ROOT / 'CAMPAIGN_03_EVENT_METRICS.csv', index=False)
    print(comp.to_string(index=False))

if __name__ == '__main__': main()
