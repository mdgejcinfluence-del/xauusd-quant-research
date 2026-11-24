"""Phase 21-B : asymetrie directionnelle apres expansion D1 signee.
Artefacts 21-A uniquement. EXPLORATORY_POST_HOC. Aucun modele/strategie/P&L."""
import hashlib
import json
import pathlib

import numpy as np
import pandas as pd

R = pathlib.Path('reports/meta_alpha/phase21')
HS = (1, 2, 3, 5)
GRAINE = 2111
NBOOT = 10000


def groupe(row):
    if row.regime == 'D1_EXPANSION':
        return 'D1_POSITIVE_EXPANSION' if row.BODY_BP > 0 else ('D1_NEGATIVE_EXPANSION' if row.BODY_BP < 0 else 'D1_NEUTRAL_EXPANSION')
    if row.regime == 'D1_NORMAL':
        return 'D1_NORMAL_POSITIVE' if row.BODY_BP > 0 else ('D1_NORMAL_NEGATIVE' if row.BODY_BP < 0 else 'D1_NORMAL_NEUTRAL')
    if row.regime == 'D1_COMPRESSION':
        return 'D1_COMPRESSION_DESCRIPTIF'
    return 'INDETERMINE_CHAUFFE'


def main():
    j = pd.read_parquet(R / 'PHASE21A_D1_BARSET.parquet')
    fwd = pd.read_parquet(R / 'PHASE21A_D1_FORWARD_MFE_MAE.parquet')
    j = j.merge(fwd, on='jour', how='left')
    cat = pd.read_parquet(R / 'PHASE21A_D1_REGIME_CATALOG.parquet')
    j = j.merge(cat[['jour', 'EPISODE_D1_EXPANSION']], on='jour', suffixes=('', '_cat'))
    if 'EPISODE_D1_EXPANSION_cat' in j:
        j['EPISODE_D1_EXPANSION'] = j['EPISODE_D1_EXPANSION_cat']
        j = j.drop(columns='EPISODE_D1_EXPANSION_cat')
    j['groupe'] = j.apply(groupe, axis=1)
    j['signe'] = np.sign(j.BODY_BP)
    j['semaine_iso'] = j.jour.dt.strftime('%G-W%V')

    exp = j[j.regime == 'D1_EXPANSION'].copy()
    # episodes: premiere journee de chaque episode
    exp = exp.sort_values('jour')
    premier = exp.groupby('EPISODE_D1_EXPANSION').jour.transform('min')
    exp['est_premier_episode'] = exp.jour == premier
    catalogue = exp.rename(columns={'EPISODE_D1_EXPANSION': 'D1_EXPANSION_EPISODE_ID'})[
        ['D1_EXPANSION_EPISODE_ID', 'jour', 'groupe', 'BODY_BP', 'RANGE_BP', 'signe',
         'est_premier_episode', 'semaine_iso', 'annee']]
    catalogue.to_parquet(R / 'PHASE21B_EXPANSION_EPISODE_CATALOG.parquet', index=False)

    prim = exp[exp.est_premier_episode].copy()
    rec = []
    for g, gg in j.groupby('groupe'):
        rec.append(dict(groupe=g, n_journees=len(gg), n_semaines_iso=gg.semaine_iso.nunique(),
                        annees=f"{gg.annee.min()}-{gg.annee.max()}"))
    for signe_g, gg in prim.groupby('groupe'):
        rec.append(dict(groupe=signe_g + ' (primaire, 1er jour episode)', n_journees=len(gg),
                        n_semaines_iso=gg.semaine_iso.nunique(), annees=f"{gg.annee.min()}-{gg.annee.max()}"))
    rec.append(dict(groupe='EPISODES_EXPANSION_total', n_journees=int(exp.EPISODE_D1_EXPANSION.nunique()),
                    n_semaines_iso=int(exp.semaine_iso.nunique()), annees=''))
    rec.append(dict(groupe='JOURNEES_EXPANSION_dans_episode_deja_commence',
                    n_journees=int((~exp.est_premier_episode).sum()), n_semaines_iso=int(exp[~exp.est_premier_episode].semaine_iso.nunique()), annees=''))
    pd.DataFrame(rec).to_csv(R / 'PHASE21B_EVENT_COHORT_RECONCILIATION.csv', index=False)

    # chemins futurs: primaire (episodes) + secondaire (toutes expansions) + references normales
    pops = []
    for pop, df in [('PRIMAIRE_EPISODE', prim), ('SECONDAIRE_TOUTES_EXPANSIONS', exp),
                    ('REFERENCE_NORMALE', j[j.regime == 'D1_NORMAL'])]:
        for r in df.itertuples():
            for H in HS:
                term = getattr(r, f'TERMINAL_{H}')
                up, dn = getattr(r, f'UP_{H}'), getattr(r, f'DOWN_{H}')
                fav = up if r.signe > 0 else (dn if r.signe < 0 else np.nan)
                adv = dn if r.signe > 0 else (up if r.signe < 0 else np.nan)
                pops.append(dict(population=pop, jour=r.jour, groupe=r.groupe, signe=int(r.signe),
                                 episode_id=getattr(r, 'EPISODE_D1_EXPANSION', np.nan),
                                 horizon_jours=H, heures_ecoulees=H * 24,
                                 FUTURE_TERMINAL_BP=term, FUTURE_UP_BP=up, FUTURE_DOWN_BP=dn,
                                 DIRECTION_ALIGNED_TERMINAL_BP=r.signe * term if r.signe != 0 else np.nan,
                                 FAVORABLE_EXCURSION_BP=fav, ADVERSE_EXCURSION_BP=adv,
                                 EXCURSION_ASYMMETRY_BP=fav - adv if r.signe != 0 else np.nan,
                                 EXCURSION_ASYMMETRY_RATIO=(fav / adv) if (r.signe != 0 and adv and adv > 0) else np.nan,
                                 MFE_DIR_BP=getattr(r, f'MFE_{H}'), MAE_DIR_BP=getattr(r, f'MAE_{H}'),
                                 semaine_iso=r.semaine_iso, annee=r.annee, censure=False if pd.notna(term) else True))
    paths = pd.DataFrame(pops)
    paths.to_parquet(R / 'PHASE21B_FUTURE_PATHS.parquet', index=False)

    # metriques signees descriptives par groupe/horizon (primaire pour expansions, ref normales entieres)
    met = []
    base = paths[((paths.population == 'PRIMAIRE_EPISODE') | (paths.population == 'REFERENCE_NORMALE'))]
    for (g, H), gg in base.groupby(['groupe', 'horizon_jours']):
        d = gg.dropna(subset=['FUTURE_TERMINAL_BP'])
        if not len(d):
            continue
        al = d.DIRECTION_ALIGNED_TERMINAL_BP
        row = dict(groupe=g, horizon_jours=H, n=len(d), n_semaines_iso=d.semaine_iso.nunique(),
                   terminal_moyenne=d.FUTURE_TERMINAL_BP.mean(), terminal_mediane=d.FUTURE_TERMINAL_BP.median(),
                   aligne_moyenne=al.mean(), aligne_mediane=al.median(),
                   part_continuation=float((al > 0).mean()), part_retournement=float((al < 0).mean()),
                   asymetrie_moyenne=d.EXCURSION_ASYMMETRY_BP.mean(), asymetrie_mediane=d.EXCURSION_ASYMMETRY_BP.median(),
                   MFE_mediane=d.FAVORABLE_EXCURSION_BP.median(), MAE_mediane=d.ADVERSE_EXCURSION_BP.median(),
                   MFE_moins_MAE_mediane=(d.FAVORABLE_EXCURSION_BP - d.ADVERSE_EXCURSION_BP).median())
        for q in (10, 25, 50, 75, 90, 95):
            row[f'TERMINAL_P{q}'] = np.nanpercentile(d.FUTURE_TERMINAL_BP, q)
        for s in (30, 60, 100):
            row[f'part_aligne_sup_{s}bp'] = float((al.abs() > s).mean())
        met.append(row)
    pd.DataFrame(met).to_csv(R / 'PHASE21B_SIGNED_DIRECTIONAL_METRICS.csv', index=False)

    upd = base.groupby(['groupe', 'horizon_jours']).agg(
        n=('FUTURE_TERMINAL_BP', 'count'), UP_mediane=('FUTURE_UP_BP', 'median'), DOWN_mediane=('FUTURE_DOWN_BP', 'median'),
        UP_moyenne=('FUTURE_UP_BP', 'mean'), DOWN_moyenne=('FUTURE_DOWN_BP', 'mean')).reset_index()
    upd.to_csv(R / 'PHASE21B_UP_DOWN_EXCURSION_COMPARISON.csv', index=False)

    # couverture amplitude vs references non verifiees
    cov = []
    for (g, H), gg in base.groupby(['groupe', 'horizon_jours']):
        d = gg.dropna(subset=['FAVORABLE_EXCURSION_BP'])
        for ref in (4.0, 4.5):
            row = dict(groupe=g, horizon_jours=H, reference_bp=ref, statut_reference='REFERENCE_COST_UNVERIFIED', n=len(d),
                       MAE_mediane=d.ADVERSE_EXCURSION_BP.median(), MAE_moyenne=d.ADVERSE_EXCURSION_BP.mean())
            for k in (1, 2, 3, 5):
                row[f'part_MFE_sup_{k}x'] = float((d.FAVORABLE_EXCURSION_BP > k * ref).mean())
            cov.append(row)
    pd.DataFrame(cov).to_csv(R / 'PHASE21B_AMPLITUDE_COST_COVERAGE.csv', index=False)

    # inference: bootstrap par grappes de semaines ISO, population primaire
    rng = np.random.default_rng(GRAINE)
    comparaisons = [('D1_POSITIVE_EXPANSION', 'D1_NORMAL_POSITIVE', 'PRIMAIRE_EPISODE', 'REFERENCE_NORMALE'),
                    ('D1_NEGATIVE_EXPANSION', 'D1_NORMAL_NEGATIVE', 'PRIMAIRE_EPISODE', 'REFERENCE_NORMALE'),
                    ('D1_POSITIVE_EXPANSION', 'D1_NEGATIVE_EXPANSION', 'PRIMAIRE_EPISODE', 'PRIMAIRE_EPISODE')]
    tests = []
    for g1, g2, p1, p2 in comparaisons:
        for H in HS:
            for mesure in ('DIRECTION_ALIGNED_TERMINAL_BP', 'EXCURSION_ASYMMETRY_BP'):
                a = paths[(paths.population == p1) & (paths.groupe == g1) & (paths.horizon_jours == H)].dropna(subset=[mesure])
                b = paths[(paths.population == p2) & (paths.groupe == g2) & (paths.horizon_jours == H)].dropna(subset=[mesure])
                evalue = len(a) >= 50 and len(b) >= 50 and a.semaine_iso.nunique() >= 20 and b.semaine_iso.nunique() >= 20
                effet = a[mesure].mean() - b[mesure].mean() if evalue else np.nan
                p = np.nan; ci = (np.nan, np.nan); med = np.nan
                if evalue:
                    wa, wb = a.semaine_iso.unique(), b.semaine_iso.unique()
                    ga = {w: x[mesure].values for w, x in a.groupby('semaine_iso')}
                    gb = {w: x[mesure].values for w, x in b.groupby('semaine_iso')}
                    boots = np.empty(NBOOT)
                    for i in range(NBOOT):
                        sa = np.concatenate([ga[w] for w in rng.choice(wa, len(wa), replace=True)])
                        sb = np.concatenate([gb[w] for w in rng.choice(wb, len(wb), replace=True)])
                        boots[i] = sa.mean() - sb.mean()
                    p = 2 * min((boots <= 0).mean(), (boots >= 0).mean())
                    ci = tuple(np.percentile(boots, [2.5, 97.5]))
                    med = a[mesure].median() - b[mesure].median()
                tests.append(dict(comparaison=f'{g1} vs {g2}', horizon_jours=H, mesure=mesure,
                                  n_g1=len(a), n_g2=len(b), semaines_g1=a.semaine_iso.nunique(), semaines_g2=b.semaine_iso.nunique(),
                                  effet_moyenne=effet, diff_mediane=med, IC95_bas=ci[0], IC95_haut=ci[1],
                                  p_value=p, statut='EVALUE' if evalue else 'NON_EVALUABLE_INFERENTIAL'))
    T = pd.DataFrame(tests)
    # BH q=0.05 sur tests evalues
    q = np.full(len(T), np.nan)
    idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; ordre = np.argsort(pv); m = len(pv)
        qq = pv[ordre] * m / (np.arange(m) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[ordre])] = np.minimum(qq, 1.0)
    T['q_value_BH'] = q
    T.to_csv(R / 'PHASE21B_MULTIPLE_TEST_CORRECTION.csv', index=False)

    # stabilite temporelle: terminal aligne moyen par periode (primaire)
    stab = []
    for per, m in [('complet', np.ones(len(base), bool)), ('2010-2015', base.annee <= 2015), ('2016-2019', base.annee >= 2016)]:
        for (g, H), gg in base[m].groupby(['groupe', 'horizon_jours']):
            d = gg.dropna(subset=['DIRECTION_ALIGNED_TERMINAL_BP'])
            if len(d):
                stab.append(dict(periode=per, groupe=g, horizon_jours=H, n=len(d),
                                 aligne_moyenne=d.DIRECTION_ALIGNED_TERMINAL_BP.mean(),
                                 aligne_mediane=d.DIRECTION_ALIGNED_TERMINAL_BP.median(),
                                 asymetrie_moyenne=d.EXCURSION_ASYMMETRY_BP.mean()))
    pd.DataFrame(stab).to_csv(R / 'PHASE21B_TEMPORAL_STABILITY.csv', index=False)

    # registre
    reg = []
    for comp, gg in T.groupby('comparaison'):
        ev = gg[gg.statut == 'EVALUE']
        if not len(ev):
            reg.append(dict(comparaison=comp, q_min=np.nan, qualification='D1_SIGNED_PATTERN_NON_EVALUABLE')); continue
        sig = ev[ev.q_value_BH < 0.05]
        if len(sig):
            mesure_sig = ';'.join(sorted(set(sig.mesure)))
            sens = 'positif' if sig.effet_moyenne.mean() > 0 else 'negatif'
            reg.append(dict(comparaison=comp, q_min=float(ev.q_value_BH.min()),
                            qualification=f'EFFET_SIGNIFICATIF_{sens} ({mesure_sig}) - candidat descriptif, jamais un edge'))
        else:
            reg.append(dict(comparaison=comp, q_min=float(ev.q_value_BH.min()),
                            qualification='AUCUN_EFFET_SIGNIFICATIF - amplitude sans direction'))
    pd.DataFrame(reg).to_csv(R / 'PHASE21B_ANOMALY_REGISTRY.csv', index=False)

    (R / 'PHASE21B_CLUSTERED_UNCERTAINTY.md').write_text(
        "# PHASE 21-B — INCERTITUDE PAR GRAPPES\n\n"
        "Bootstrap par grappes de semaines ISO (10 000 replications, graine 2111), population primaire = "
        "premiere journee de chaque episode d'expansion (episodes preserves, jamais scindes). "
        "References normales regroupees par semaine ISO. p percentile bilaterale "
        "`2*min(P(delta<=0), P(delta>=0))`, IC95 percentiles du bootstrap, BH q=0,05 sur 24 tests preenregistres. "
        "Minima: 50 evenements et 20 semaines ISO par groupe sinon NON_EVALUABLE_INFERENTIAL. "
        "Les fenetres futures chevauchantes restent correlees au sein d'une meme semaine; le bootstrap par "
        "grappes hebdomadaires est la methode deja eprouvee (Phases 20-B/21-A). Aucun test IID naif.\n")
    stats = dict(episodes_total=int(exp.EPISODE_D1_EXPANSION.nunique()), journees_expansion=int(len(exp)),
                 primaire={g: int(len(x)) for g, x in prim.groupby('groupe')},
                 n_tests=int(len(T)), n_evalues=int((T.statut == 'EVALUE').sum()),
                 n_q_significatifs=int((T.q_value_BH < .05).sum()))
    print(json.dumps(stats, indent=1, default=str))


if __name__ == '__main__':
    main()
