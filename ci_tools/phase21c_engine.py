"""Phase 21-C : anatomie intrajournaliere D1 (6 tranches H4), premiers passages, nouveaux extremes.
Artefacts 20-A/21-A uniquement. EXPLORATORY_POST_HOC. Aucun modele/strategie/P&L."""
import json
import pathlib

import numpy as np
import pandas as pd

R20 = pathlib.Path('reports/meta_alpha/phase20')
R21 = pathlib.Path('reports/meta_alpha/phase21')
GRAINE = 2113
NBOOT = 10000
SEUILS = (30, 60, 100)


def main():
    h4 = pd.read_parquet(R20 / 'PHASE20A_H4_BARSET.parquet')
    d1 = pd.read_parquet(R21 / 'PHASE21A_D1_BARSET.parquet')
    jours = set(d1.jour)
    h4['jour'] = h4.bar_start.dt.normalize()
    h4 = h4[h4.jour.isin(jours)].sort_values(['jour', 'slot_utc'])
    info_d1 = d1.set_index('jour')

    paths, passages, extremes_events, seq_rows = [], [], [], []
    for jour, g in h4.groupby('jour'):
        g = g.sort_values('slot_utc')
        if len(g) != 6:
            continue
        o = g.open.iloc[0]; clot = g.close.iloc[-1]
        final_range = info_d1.loc[jour, 'RANGE_BP']
        cumh, cuml = o, o
        slot_final_high = slot_final_low = None
        fh = g.high.max(); fl = g.low.min()
        for k, (_, b) in enumerate(g.iterrows(), start=1):
            nh, nl = max(cumh, b.high), min(cuml, b.low)
            up_ext = 10000 * np.log(nh / cumh) if nh > cumh else 0.0
            dn_ext = 10000 * np.log(cuml / nl) if nl < cuml else 0.0
            new_h, new_l = nh > cumh, nl < cuml
            cumh, cuml = nh, nl
            if b.high >= fh and slot_final_high is None: slot_final_high = k
            if b.low <= fl and slot_final_low is None: slot_final_low = k
            crange = 10000 * np.log(cumh / cuml)
            pbody = 10000 * np.log(b.close / o)
            reste = g.iloc[k:]
            if len(reste):
                f_up = 10000 * np.log(reste.high.max() / b.close)
                f_dn = 10000 * np.log(b.close / reste.low.min())
                f_term = 10000 * np.log(clot / b.close)
                ext_meme_h = 10000 * np.log(max(cumh, reste.high.max()) / cumh)
                ext_meme_l = 10000 * np.log(cuml / min(cuml, reste.low.min()))
            else:
                f_up = f_dn = f_term = ext_meme_h = ext_meme_l = np.nan
            cat = ('LES_DEUX' if new_h and new_l else 'NOUVEAU_HIGH' if new_h else 'NOUVEAU_LOW' if new_l else 'AUCUN')
            paths.append(dict(jour=jour, tranche=k, slot_utc=int(b.slot_utc), cloture_utc=b.bar_start + pd.Timedelta(hours=4),
                              CUMULATIVE_HIGH=cumh, CUMULATIVE_LOW=cuml, CUMULATIVE_RANGE_BP=crange,
                              PARTIAL_BODY_BP=pbody, PARTIAL_BODY_EFFICIENCY=pbody / crange if crange > 0 else np.nan,
                              CLOSE_LOCATION_PARTIAL=(b.close - cuml) / (cumh - cuml) if cumh > cuml else np.nan,
                              UPWARD_EXTENSION_BP=up_ext, DOWNWARD_EXTENSION_BP=dn_ext,
                              fraction_range_final=crange / final_range if final_range > 0 else np.nan,
                              nouvel_extreme=cat, TERMINAL_FUTUR_BP=f_term, FUTURE_UP_BP=f_up, FUTURE_DOWN_BP=f_dn,
                              EXT_HIGH_FUTURE_BP=ext_meme_h, EXT_LOW_FUTURE_BP=ext_meme_l,
                              barres_restantes=6 - k, semaine_iso=b.semaine_iso, annee=jour.year,
                              RANGE_FINAL_BP=final_range))
            if cat != 'AUCUN':
                extremes_events.append(dict(jour=jour, tranche=k, type=cat, cloture_utc=b.bar_start + pd.Timedelta(hours=4),
                                            barres_restantes=6 - k, TERMINAL_FUTUR_BP=f_term, FUTURE_UP_BP=f_up, FUTURE_DOWN_BP=f_dn,
                                            EXT_HIGH_FUTURE_BP=ext_meme_h, EXT_LOW_FUTURE_BP=ext_meme_l,
                                            semaine_iso=b.semaine_iso, annee=jour.year))
        ordre = ('HIGH_AVANT_LOW' if slot_final_high < slot_final_low else
                 'LOW_AVANT_HIGH' if slot_final_low < slot_final_high else 'MEME_BARRE_ORDRE_INCONNU')
        seq_rows.append(dict(jour=jour, tranche_high_final=slot_final_high, tranche_low_final=slot_final_low, ordre_extremes_finaux=ordre,
                             RANGE_FINAL_BP=final_range, annee=jour.year))
        # premiers passages
        jp = [p for p in paths if p['jour'] == jour]
        for s in SEUILS:
            hit = next((p for p in jp if p['CUMULATIVE_RANGE_BP'] >= s), None)
            if hit is None:
                passages.append(dict(jour=jour, seuil_bp=s, declenche=False, tranche=None, semaine_iso=jp[0]['semaine_iso'], annee=jour.year))
            else:
                k = hit['tranche']; reste = g.iloc[k:]
                passages.append(dict(jour=jour, seuil_bp=s, declenche=True, tranche=k, cloture_utc=hit['cloture_utc'],
                                     CUMULATIVE_RANGE_BP=hit['CUMULATIVE_RANGE_BP'], PARTIAL_BODY_BP=hit['PARTIAL_BODY_BP'],
                                     PARTIAL_STATE=('PARTIAL_POSITIVE' if hit['PARTIAL_BODY_BP'] > 0 else 'PARTIAL_NEGATIVE' if hit['PARTIAL_BODY_BP'] < 0 else 'PARTIAL_NEUTRAL'),
                                     UPWARD_EXTENSION_BP=hit['UPWARD_EXTENSION_BP'], DOWNWARD_EXTENSION_BP=hit['DOWNWARD_EXTENSION_BP'],
                                     heures_restantes=(6 - k) * 4, RANGE_ADDITIONNEL_BP=final_range - hit['CUMULATIVE_RANGE_BP'],
                                     TERMINAL_FUTUR_BP=hit['TERMINAL_FUTUR_BP'], FUTURE_UP_BP=hit['FUTURE_UP_BP'], FUTURE_DOWN_BP=hit['FUTURE_DOWN_BP'],
                                     premier_slot=(k == 1), semaine_iso=hit['semaine_iso'], annee=jour.year))

    P = pd.DataFrame(paths); PAS = pd.DataFrame(passages); EXT = pd.DataFrame(extremes_events); SEQ = pd.DataFrame(seq_rows)
    P.to_parquet(R21 / 'PHASE21C_DAILY_PATH_CATALOG.parquet', index=False)
    PAS.to_parquet(R21 / 'PHASE21C_FIRST_PASSAGE_CATALOG.parquet', index=False)
    EXT.to_parquet(R21 / 'PHASE21C_NEW_EXTREME_EVENT_CATALOG.parquet', index=False)
    SEQ.to_csv(R21 / 'PHASE21C_INTRADAY_EXTREME_SEQUENCE.csv', index=False)

    agg = P.groupby('tranche').agg(n=('jour', 'count'), range_median=('CUMULATIVE_RANGE_BP', 'median'), range_moyen=('CUMULATIVE_RANGE_BP', 'mean'),
                                   fraction_finale_mediane=('fraction_range_final', 'median'),
                                   ext_high_mediane=('UPWARD_EXTENSION_BP', 'median'), ext_low_mediane=('DOWNWARD_EXTENSION_BP', 'median'),
                                   n_nouveau_high=('UPWARD_EXTENSION_BP', lambda x: int((x > 0).sum())),
                                   n_nouveau_low=('DOWNWARD_EXTENSION_BP', lambda x: int((x > 0).sum()))).reset_index()
    for q in (10, 25, 75, 90, 95, 99):
        agg[f'range_P{q}'] = P.groupby('tranche').CUMULATIVE_RANGE_BP.quantile(q / 100).values
    agg.to_csv(R21 / 'PHASE21C_PARTIAL_RANGE_BY_SLOT.csv', index=False)

    post = PAS[PAS.declenche].copy()
    post.to_parquet(R21 / 'PHASE21C_POST_PASSAGE_EXCURSIONS.parquet', index=False)

    aft = EXT.groupby(['type', 'barres_restantes']).agg(
        n=('jour', 'count'), terminal_median=('TERMINAL_FUTUR_BP', 'median'), up_median=('FUTURE_UP_BP', 'median'),
        down_median=('FUTURE_DOWN_BP', 'median'), ext_high_mediane=('EXT_HIGH_FUTURE_BP', 'median'),
        ext_low_mediane=('EXT_LOW_FUTURE_BP', 'median')).reset_index()
    aft.to_csv(R21 / 'PHASE21C_AFTER_EXTREME_BEHAVIOR.csv', index=False)

    pd_dir = post[post.PARTIAL_STATE.isin(['PARTIAL_POSITIVE', 'PARTIAL_NEGATIVE'])].copy()
    pd_dir['signe'] = np.where(pd_dir.PARTIAL_STATE == 'PARTIAL_POSITIVE', 1, -1)
    pd_dir['TERMINAL_ALIGNE'] = pd_dir.signe * pd_dir.TERMINAL_FUTUR_BP
    pd_dir['FAVORABLE'] = np.where(pd_dir.signe > 0, pd_dir.FUTURE_UP_BP, pd_dir.FUTURE_DOWN_BP)
    pd_dir['ADVERSE'] = np.where(pd_dir.signe > 0, pd_dir.FUTURE_DOWN_BP, pd_dir.FUTURE_UP_BP)
    pd_dir['ASYMETRIE'] = pd_dir.FAVORABLE - pd_dir.ADVERSE
    pd_dir.to_csv(R21 / 'PHASE21C_PARTIAL_DIRECTION_AMPLITUDE.csv', index=False)

    cov = []
    for (s, st), gg in pd_dir.groupby(['seuil_bp', 'PARTIAL_STATE']):
        for ref in (4.0, 4.5):
            row = dict(groupe=f'passage_{s}bp_{st}', reference_bp=ref, statut_reference='REFERENCE_COST_UNVERIFIED', n=len(gg),
                       range_additionnel_median=gg.RANGE_ADDITIONNEL_BP.median(), MAE_mediane=gg.ADVERSE.median())
            for kk in (1, 2, 3, 5):
                row[f'part_MFE_sup_{kk}x'] = float((gg.FAVORABLE > kk * ref).mean())
            for s2 in SEUILS:
                row[f'part_range_add_sup_{s2}bp'] = float((gg.RANGE_ADDITIONNEL_BP > s2).mean())
            cov.append(row)
    pd.DataFrame(cov).to_csv(R21 / 'PHASE21C_AMPLITUDE_COST_COVERAGE.csv', index=False)

    # inference
    rng = np.random.default_rng(GRAINE)

    def boot(a, b, mesure):
        ev = len(a) >= 50 and len(b) >= 50 and a.semaine_iso.nunique() >= 20 and b.semaine_iso.nunique() >= 20
        if not ev:
            return np.nan, np.nan, (np.nan, np.nan), False
        wa, wb = a.semaine_iso.unique(), b.semaine_iso.unique()
        ga = {w: x[mesure].values for w, x in a.groupby('semaine_iso')}
        gb = {w: x[mesure].values for w, x in b.groupby('semaine_iso')}
        boots = np.empty(NBOOT)
        for i in range(NBOOT):
            boots[i] = np.concatenate([ga[w] for w in rng.choice(wa, len(wa), replace=True)]).mean() - \
                       np.concatenate([gb[w] for w in rng.choice(wb, len(wb), replace=True)]).mean()
        p = 2 * min((boots <= 0).mean(), (boots >= 0).mean())
        return a[mesure].mean() - b[mesure].mean(), p, tuple(np.percentile(boots, [2.5, 97.5])), True

    tests = []
    E = EXT[(EXT.tranche >= 2) & (EXT.tranche <= 5)]
    aucun = P[(P.tranche >= 2) & (P.tranche <= 5) & (P.nouvel_extreme == 'AUCUN')]
    groupes = {'NOUVEAU_HIGH': E[E.type == 'NOUVEAU_HIGH'], 'NOUVEAU_LOW': E[E.type == 'NOUVEAU_LOW'], 'AUCUN': aucun}
    for c1, c2 in [('NOUVEAU_HIGH', 'AUCUN'), ('NOUVEAU_LOW', 'AUCUN'), ('NOUVEAU_HIGH', 'NOUVEAU_LOW')]:
        for m in ('TERMINAL_FUTUR_BP', 'FUTURE_UP_BP', 'FUTURE_DOWN_BP'):
            a, b = groupes[c1].dropna(subset=[m]), groupes[c2].dropna(subset=[m])
            eff, p, ci, ev = boot(a, b, m)
            tests.append(dict(comparaison=f'{c1} vs {c2}', mesure=m, n1=len(a), n2=len(b), effet=eff, p_value=p,
                              IC95_bas=ci[0], IC95_haut=ci[1], statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
    for s in (60, 100):
        for m in ('TERMINAL_ALIGNE', 'ASYMETRIE'):
            a = pd_dir[(pd_dir.seuil_bp == s) & (pd_dir.PARTIAL_STATE == 'PARTIAL_POSITIVE')].dropna(subset=[m])
            b = pd_dir[(pd_dir.seuil_bp == s) & (pd_dir.PARTIAL_STATE == 'PARTIAL_NEGATIVE')].dropna(subset=[m])
            eff, p, ci, ev = boot(a, b, m)
            tests.append(dict(comparaison=f'passage{s} PARTIAL_POSITIVE vs PARTIAL_NEGATIVE', mesure=m, n1=len(a), n2=len(b),
                              effet=eff, p_value=p, IC95_bas=ci[0], IC95_haut=ci[1], statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
    a = post[(post.seuil_bp == 60) & (post.tranche <= 2)].dropna(subset=['RANGE_ADDITIONNEL_BP'])
    b = post[(post.seuil_bp == 60) & (post.tranche >= 4)].dropna(subset=['RANGE_ADDITIONNEL_BP'])
    eff, p, ci, ev = boot(a, b, 'RANGE_ADDITIONNEL_BP')
    tests.append(dict(comparaison='passage60 precoce(slot<=2) vs tardif(slot>=4)', mesure='RANGE_ADDITIONNEL_BP', n1=len(a), n2=len(b),
                      effet=eff, p_value=p, IC95_bas=ci[0], IC95_haut=ci[1], statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
    T = pd.DataFrame(tests)
    q = np.full(len(T), np.nan); idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; o = np.argsort(pv); m_ = len(pv)
        qq = pv[o] * m_ / (np.arange(m_) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[o])] = np.minimum(qq, 1)
    T['q_value_BH'] = q
    T.to_csv(R21 / 'PHASE21C_MULTIPLE_TEST_CORRECTION.csv', index=False)

    # stabilite: anatomie par periode + terminal apres nouveau high/low
    stab = []
    for per, m in [('complet', P.annee > 0), ('2010-2015', P.annee <= 2015), ('2016-2019', P.annee >= 2016)]:
        for tr, gg in P[m].groupby('tranche'):
            stab.append(dict(periode=per, type='range_cumule', cle=f'tranche{tr}', n=len(gg), valeur_mediane=gg.CUMULATIVE_RANGE_BP.median(),
                             fraction_finale_mediane=gg.fraction_range_final.median()))
        for t_, gg in EXT[m.loc[EXT.index] if False else (EXT.annee <= 2015 if per == '2010-2015' else EXT.annee >= 2016 if per == '2016-2019' else EXT.annee > 0)].groupby('type'):
            stab.append(dict(periode=per, type=f'terminal_apres_{t_}', cle='', n=len(gg), valeur_mediane=gg.TERMINAL_FUTUR_BP.median(), fraction_finale_mediane=np.nan))
    pd.DataFrame(stab).to_csv(R21 / 'PHASE21C_TEMPORAL_STABILITY.csv', index=False)

    reg = []
    for _, r in T.iterrows():
        if r.statut != 'EVALUE':
            qual = 'INSUFFICIENT_EVIDENCE'
        elif r.q_value_BH < 0.05:
            qual = 'EFFET_SIGNIFICATIF (candidat descriptif, jamais un edge)'
        else:
            qual = 'AUCUN_EFFET_SIGNIFICATIF'
        reg.append(dict(comparaison=r.comparaison, mesure=r.mesure, q_value=r.q_value_BH, qualification=qual))
    pd.DataFrame(reg).to_csv(R21 / 'PHASE21C_ANOMALY_REGISTRY.csv', index=False)
    print(json.dumps(dict(jours=int(P.jour.nunique()), passages_declenches={str(s): int((PAS.seuil_bp.eq(s) & PAS.declenche).sum()) for s in SEUILS},
                          extremes={k: int(len(v)) for k, v in groupes.items()}, n_tests=int(len(T)),
                          n_sig=int((T.q_value_BH < .05).sum())), indent=1))


if __name__ == '__main__':
    main()
