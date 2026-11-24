# -*- coding: utf-8 -*-
"""Phase 21-A: radiographie structurelle D1 depuis les barres H4 certifiees 20-A.
Aucun tick relu, aucun modele, aucun P&L. EXPLORATORY_POST_HOC."""
import json, pathlib
import numpy as np, pandas as pd
R20 = pathlib.Path('reports/meta_alpha/phase20'); R21 = pathlib.Path('reports/meta_alpha/phase21')
GRAINE = 2107

def logbp(a, b): return 10000 * np.log(b / a)

def construire_d1():
    h = pd.read_parquet(R20 / 'PHASE20A_H4_BARSET.parquet')
    h['jour'] = h.bar_start.dt.normalize()
    lignes = []; qualite = []
    for jour, g in h.groupby('jour'):
        # Completude au niveau journee: six barres presentes avec couverture >= 3,5 h.
        # Le critere H4 d'ecart maximal <= 1800 s est inapplicable a la barre de 20:00,
        # qui contient la pause nocturne structurelle du marche (ecart median 3600 s):
        # le trou est signale (trou_intrajournalier), jamais masque. Artefacts 20-A inchanges.
        gc = g[g.couverture_s >= 3.5 * 3600]
        slots_ok = sorted(gc.bar_start.dt.hour.unique())
        complet = len(gc) == 6 and slots_ok == [0, 4, 8, 12, 16, 20]
        qualite.append(dict(jour=jour, n_barres_h4=int(len(g)), n_completes=int(len(gc)), slots_complets=str(slots_ok),
                            trou_intrajournalier=int((g.max_gap_s > 1800).any()) if complet else '',
                            statut='COMPLETE' if complet else 'INCOMPLETE (GAP_CAUSE_UNVERIFIED si cause non etablie)'))
        if not complet: continue
        gc = gc.sort_values('bar_start')
        lignes.append(dict(jour=jour, open=float(gc.open.iloc[0]), high=float(gc.high.max()), low=float(gc.low.min()),
                           close=float(gc.close.iloc[-1]), n_quotes=int(gc.n_quotes.sum()),
                           spread_mediane_barres=float(gc.spread_median_bp.median()),
                           spread_moy_pondere_cotations=float(np.average(gc.spread_mean_bp, weights=gc.n_quotes)),
                           trou_intrajournalier=int((gc.max_gap_s > 1800).any()),
                           sources_h4='|'.join(sorted(set('|'.join(gc.source_batches).split('|'))))))
    d = pd.DataFrame(lignes).sort_values('jour').reset_index(drop=True)
    pd.DataFrame(qualite).to_csv(R21 / 'PHASE21A_D1_DATA_QUALITY.csv', index=False)
    d['BODY_BP'] = logbp(d.open, d.close); d['ABS_BODY_BP'] = d.BODY_BP.abs()
    d['RANGE_BP'] = 10000 * np.log(d.high / d.low)
    prev = d.close.shift(1)
    d['TRUE_RANGE_BP'] = 10000 * np.log(np.maximum(d.high, prev) / np.minimum(d.low, prev))
    d['BODY_EFFICIENCY'] = d.ABS_BODY_BP / d.RANGE_BP
    d['CLOSE_LOCATION'] = (d.close - d.low) / (d.high - d.low)
    d['UPPER_WICK_BP'] = 10000 * np.log(d.high / d[['open', 'close']].max(axis=1))
    d['LOWER_WICK_BP'] = 10000 * np.log(d[['open', 'close']].min(axis=1) / d.low)
    d['WICK_IMBALANCE'] = (d.LOWER_WICK_BP - d.UPPER_WICK_BP) / d.RANGE_BP
    atr = np.full(len(d), np.nan); tr = d.TRUE_RANGE_BP.values
    for i in range(14, len(d)): atr[i] = tr[i - 14:i].mean()
    d['ATR14_D1_PREV'] = atr
    d['BODY_ATR14'] = d.ABS_BODY_BP / atr; d['RANGE_ATR14'] = d.RANGE_BP / atr; d['TRUE_RANGE_ATR14'] = d.TRUE_RANGE_BP / atr
    d['sens'] = np.sign(d.BODY_BP).astype(int)
    d['jour_semaine'] = d.jour.dt.dayofweek; d['mois'] = d.jour.dt.month; d['annee'] = d.jour.dt.year
    d['semaine_iso'] = d.jour.dt.strftime('%G-W%V')
    return d

def forward(d):
    n = len(d); out = pd.DataFrame({'jour': d.jour})
    for H in (1, 2, 3, 5):
        up = np.full(n, np.nan); dn = np.full(n, np.nan); term = np.full(n, np.nan)
        mfe = np.full(n, np.nan); mae = np.full(n, np.nan); tup = np.full(n, np.nan); tdn = np.full(n, np.nan)
        for i in range(n - H):
            c = d.close.values[i]; seg_hi = d.high.values[i + 1:i + H + 1]; seg_lo = d.low.values[i + 1:i + H + 1]
            up[i] = 10000 * np.log(seg_hi.max() / c); dn[i] = -10000 * np.log(seg_lo.min() / c)
            tup[i] = int(np.argmax(seg_hi)) + 1; tdn[i] = int(np.argmin(seg_lo)) + 1
            s = d.sens.values[i]
            if s > 0: mfe[i], mae[i] = up[i], dn[i]
            elif s < 0: mfe[i], mae[i] = dn[i], up[i]
            term[i] = 10000 * np.log(d.close.values[i + H] / c)
        out[f'UP_{H}'] = up; out[f'DOWN_{H}'] = dn; out[f'TERMINAL_{H}'] = term
        out[f'MFE_{H}'] = mfe; out[f'MAE_{H}'] = mae; out[f'T_MFE_jours_{H}'] = np.where(d.sens.values >= 0, tup, tdn)
        out[f'T_MAE_jours_{H}'] = np.where(d.sens.values >= 0, tdn, tup)
    return out

def regimes(d):
    rng = d.RANGE_BP.values; q10 = np.full(len(d), np.nan); q90 = np.full(len(d), np.nan)
    for i in range(250, len(d)):
        q10[i] = np.quantile(rng[i - 250:i], .10); q90[i] = np.quantile(rng[i - 250:i], .90)
    d['Q10_roulant'] = q10; d['Q90_roulant'] = q90
    d['regime'] = np.where(rng <= q10, 'D1_COMPRESSION', np.where(rng >= q90, 'D1_EXPANSION', 'D1_NORMAL'))
    d.loc[~np.isfinite(q10), 'regime'] = 'INDETERMINE_CHAUFFE'
    for etat in ('D1_COMPRESSION', 'D1_EXPANSION'):
        col = f'EPISODE_{etat}'; ids = np.full(len(d), '', dtype=object); cpt = -1
        for i in range(len(d)):
            if d.regime.iloc[i] == etat:
                if i == 0 or d.regime.iloc[i - 1] != etat: cpt += 1
                ids[i] = f'{etat}-{cpt}'
        d[col] = ids
    return d

def p_decalage_semaines(outcomes, masque, rng, n_rep=10000):
    """outcomes/masque: matrices (semaines ISO, 7 jours). Decalage circulaire par
    semaines entieres >= 2 sur l'axe des semaines; p bilaterale."""
    valides = np.isfinite(outcomes)
    obs_m = masque & valides
    if obs_m.sum() == 0: return np.nan
    obs = np.nanmean(outcomes[obs_m]); centre = np.nanmean(outcomes[valides])
    n_sem = outcomes.shape[0]; stats = []
    for _ in range(n_rep):
        k = int(rng.integers(2, max(3, n_sem - 2)))
        dec = np.roll(outcomes, k, axis=0)
        m = masque & np.isfinite(dec)
        if m.sum(): stats.append(np.nanmean(dec[m]))
    stats = np.array(stats)
    return float((np.abs(stats - centre) >= abs(obs - centre)).mean())

def grille_semaine(d, colonne):
    g = d.copy(); g['sem'] = g.jour.dt.strftime('%G-W%V'); g['js'] = g.jour.dt.dayofweek
    piv = g.pivot_table(index='sem', columns='js', values=colonne, aggfunc='first').reindex(columns=range(7))
    return piv

def main():
    d = construire_d1()
    d = regimes(d)
    fw = forward(d)
    d.to_parquet(R21 / 'PHASE21A_D1_BARSET.parquet', index=False)
    fw.to_parquet(R21 / 'PHASE21A_D1_FORWARD_MFE_MAE.parquet', index=False)
    j = d.merge(fw, on='jour')
    j['AMP_FUTURE'] = j.UP_1 + j.DOWN_1
    d[d.regime != 'INDETERMINE_CHAUFFE'][['jour', 'regime', 'EPISODE_D1_COMPRESSION', 'EPISODE_D1_EXPANSION', 'RANGE_BP', 'Q10_roulant', 'Q90_roulant']]\
        .to_parquet(R21 / 'PHASE21A_D1_REGIME_CATALOG.parquet', index=False)
    # distributions
    def dist(nom, s):
        s = pd.Series(s).dropna(); r = dict(mesure=nom, n=int(len(s)), moyenne=float(s.mean()), mediane=float(s.median()),
                                             ecart_type=float(s.std()), mad=float((s - s.median()).abs().median()),
                                             minimum=float(s.min()), maximum=float(s.max()))
        for p in (1, 5, 10, 25, 50, 75, 90, 95, 99): r[f'P{p}'] = float(s.quantile(p / 100))
        for seuil in (30, 60, 100): r[f'part_sup_{seuil}bp'] = float((s > seuil).mean())
        return r
    pd.DataFrame([dist('BODY_BP signe', j.BODY_BP), dist('ABS_BODY_BP', j.ABS_BODY_BP), dist('RANGE_BP', j.RANGE_BP),
                  dist('TRUE_RANGE_BP', j.TRUE_RANGE_BP), dist('BODY_ATR14', j.BODY_ATR14), dist('RANGE_ATR14', j.RANGE_ATR14)])\
        .to_csv(R21 / 'PHASE21A_D1_AMPLITUDE_DISTRIBUTIONS.csv', index=False)
    # autocorrelation
    ac = []
    for nom, s in [('rendements signes', j.BODY_BP), ('rendements absolus', j.ABS_BODY_BP), ('RANGE_BP', j.RANGE_BP),
                   ('TRUE_RANGE_BP', j.TRUE_RANGE_BP), ('direction', j.sens.astype(float))]:
        for lag in (1, 2, 3, 5, 10, 20):
            ac.append(dict(serie=nom, retard_jours=lag, autocorrelation=float(s.reset_index(drop=True).autocorr(lag)),
                           ic95_approx=float(1.96 / np.sqrt(len(s.dropna())))))
    pd.DataFrame(ac).to_csv(R21 / 'PHASE21A_D1_AUTOCORRELATION.csv', index=False)
    # sequences maximales
    lignes = []
    sens = j.sens.values; debut = 0
    for i in range(1, len(j) + 1):
        if i == len(j) or sens[i] == 0 or sens[i] != sens[debut]:
            L = i - debut
            if sens[debut] != 0 and L >= 2:
                g = j.iloc[debut:i]
                ligne = dict(run_id=f'D1RUN-{debut}', longueur=min(L, 5), longueur_exacte=L, direction=int(sens[debut]),
                             jour_fin=g.jour.iloc[-1], amplitude_cumulee_bp=float(g.BODY_BP.sum()),
                             amplitude_moyenne_par_jour=float(g.BODY_BP.mean()))
                for H in (1, 2, 3, 5):
                    ligne[f'TERMINAL_{H}'] = float(sens[debut] * j[f'TERMINAL_{H}'].iloc[i - 1]) if i - 1 + H < len(j) else np.nan
                    ligne[f'MFE_{H}'] = float(j[f'MFE_{H}'].iloc[i - 1]) if i - 1 + H < len(j) else np.nan
                    ligne[f'MAE_{H}'] = float(j[f'MAE_{H}'].iloc[i - 1]) if i - 1 + H < len(j) else np.nan
                lignes.append(ligne)
            debut = i
    pd.DataFrame(lignes).to_csv(R21 / 'PHASE21A_D1_SEQUENCE_ANALYSIS.csv', index=False)
    # cassures
    brk = []
    for i in range(5, len(j)):
        for fam, hi_ref, lo_ref in [('PRECEDENT', j.high.values[i - 1], j.low.values[i - 1]),
                                    ('CINQ_PRECEDENTS', j.high.values[i - 5:i].max(), j.low.values[i - 5:i].min())]:
            for cote, cond_i, cond_c in [('HAUT', j.high.values[i] > hi_ref, j.close.values[i] > hi_ref),
                                         ('BAS', j.low.values[i] < lo_ref, j.close.values[i] < lo_ref)]:
                if cond_i or cond_c:
                    ligne = dict(jour=j.jour.iloc[i], famille=f'CASSURE_{fam}_{cote}', type='CLOTURE_CONFIRMEE' if cond_c else 'INTRABARRE_SEUL',
                                 direction=1 if cote == 'HAUT' else -1)
                    for H in (1, 2, 3, 5):
                        ligne[f'TERMINAL_DIR_{H}'] = float(ligne['direction'] * j[f'TERMINAL_{H}'].iloc[i])
                    brk.append(ligne)
    pd.DataFrame(brk).to_csv(R21 / 'PHASE21A_D1_BREAKOUT_ANALYSIS.csv', index=False)
    # carte temporelle
    lignes = []
    def stats(g, type_, cle):
        return dict(type=type_, cle=str(cle), n=int(len(g)), BODY_moyen=float(g.BODY_BP.mean()), BODY_mediane=float(g.BODY_BP.median()),
                    RANGE_mediane=float(g.RANGE_BP.median()), RANGE_P90=float(g.RANGE_BP.quantile(.9)), RANGE_P95=float(g.RANGE_BP.quantile(.95)),
                    part_sup30=float((g.RANGE_BP > 30).mean()), part_sup60=float((g.RANGE_BP > 60).mean()), part_sup100=float((g.RANGE_BP > 100).mean()),
                    MFE1_mediane=float(g.MFE_1.median()), MAE1_mediane=float(g.MAE_1.median()),
                    statut='DESCRIPTIF' if len(g) >= 50 else 'FAIBLE_EFFECTIF')
    for k, g in j.groupby('jour_semaine'): lignes.append(stats(g, 'JOUR_SEMAINE (0=lundi)', k))
    for k, g in j.groupby('mois'): lignes.append(stats(g, 'MOIS', k))
    for k, g in j.groupby('annee'): lignes.append(stats(g, 'ANNEE', k))
    for k, g in [('2010-2015', j[j.annee <= 2015]), ('2016-2020', j[j.annee >= 2016])]: lignes.append(stats(g, 'SOUS_PERIODE', k))
    pd.DataFrame(lignes).to_csv(R21 / 'PHASE21A_D1_TEMPORAL_MAP.csv', index=False)
    # couverture couts (diagnostic)
    lignes = []
    for mesure, s in [('ABS_BODY_BP', j.ABS_BODY_BP), ('RANGE_BP', j.RANGE_BP), ('MFE_1', j.MFE_1), ('MFE_5', j.MFE_5),
                      ('TERMINAL_ABS_1', j.TERMINAL_1.abs()), ('TERMINAL_ABS_5', j.TERMINAL_5.abs())]:
        for ref in (4.0, 4.5):
            ligne = dict(mesure=mesure, reference_bp=ref, statut_reference='REFERENCE_COST_UNVERIFIED')
            for mult in (1, 2, 3, 5): ligne[f'part_sup_{mult}x'] = float((s > mult * ref).mean())
            lignes.append(ligne)
    pd.DataFrame(lignes).to_csv(R21 / 'PHASE21A_D1_AMPLITUDE_COST_COVERAGE.csv', index=False)
    # tests de randomisation (famille preenregistree)
    rng = np.random.default_rng(GRAINE)
    # controle synthetique
    syn = rng.normal(0, 1, (300, 7)); ind = rng.random((300, 7)) < .1
    print('controle synthetique D1: p =', round(float(p_decalage_semaines(syn, ind, rng)), 3), flush=True)
    tests = []
    def tester(famille, mesure_nom, serie, masque_evenements):
        out = grille_semaine(j, '_serie'); msk = grille_semaine(j.assign(_ev=masque_evenements.astype(float)), '_ev')
        out, msk = out.align(msk, join='outer', axis=0)
        p = p_decalage_semaines(out.values.astype(float), np.nan_to_num(msk.values.astype(float), nan=0) > 0, rng)
        ev = serie[masque_evenements]; ref = serie[~masque_evenements]
        semaines = j.loc[masque_evenements, 'semaine_iso'].nunique()
        tests.append(dict(famille=famille, mesure=mesure_nom, n_evenements=int(masque_evenements.sum()),
                          n_semaines=int(semaines), effet=float(np.nanmean(ev) - np.nanmean(ref)), p_value=float(p),
                          statut='EVALUE' if (masque_evenements.sum() >= 50 and semaines >= 20) else 'NON_EVALUABLE_INFERENTIAL'))
    j['_serie'] = np.nan
    for H in (1, 2, 3, 5):
        j['_serie'] = (j[f'UP_{H}'] + j[f'DOWN_{H}']).values
        for etat in ('D1_COMPRESSION', 'D1_EXPANSION'):
            tester(f'{etat} amplitude future', f'UP+DOWN horizon {H}', j['_serie'].values, (j.regime == etat).values)
        j['_serie'] = (j.sens * j[f'TERMINAL_{H}']).values
        for etat in ('D1_COMPRESSION', 'D1_EXPANSION'):
            tester(f'{etat} terminal directionnel', f'sens x TERMINAL horizon {H}', j['_serie'].values, (j.regime == etat).values)
    # sequences >= 3: terminal dans le sens de la sequence
    seq = pd.read_csv(R21 / 'PHASE21A_D1_SEQUENCE_ANALYSIS.csv')
    fins = pd.to_datetime(seq.jour_fin)
    for H in (1, 5):
        # serie orientee definie pour toutes les journees (sens du corps du jour),
        # masque = journee de fin d'une sequence d'au moins 3 jours de meme sens
        serie = (j.sens * j[f'TERMINAL_{H}']).values.astype(float)
        masque = np.zeros(len(j), bool)
        for r in seq[seq.longueur_exacte >= 3].itertuples():
            pos = j.index[j.jour == pd.Timestamp(r.jour_fin)]
            if len(pos): masque[pos[0]] = True
        j['_serie'] = serie
        tester('SEQUENCE >= 3 jours', f'terminal directionnel horizon {H}', serie, masque)
    T = pd.DataFrame(tests)
    if len(T):
        p = T.p_value.values; ordre = np.argsort(p); q = np.empty(len(p)); prev = 1.0
        for i, ix in enumerate(ordre[::-1]): prev = min(prev, p[ix] * len(p) / (len(p) - i)); q[ix] = prev
        T['q_value_BH'] = q
    T.to_csv(R21 / 'PHASE21A_D1_RANDOMNESS_TESTS.csv', index=False)
    T.to_csv(R21 / 'PHASE21A_D1_MULTIPLE_TEST_CORRECTION.csv', index=False)
    # transitions de regimes
    trans = pd.crosstab(j.regime.shift(1), j.regime, normalize='index').round(4)
    trans.to_csv(R21 / 'PHASE21A_D1_REGIME_TRANSITIONS.csv')
    # registre
    reg = []
    for fam, g in T.groupby('famille'):
        qmin = g.q_value_BH.min()
        if (g.statut != 'EVALUE').all(): qual = 'D1_INSUFFICIENT_EVIDENCE'
        elif qmin < 0.05 and 'amplitude' in fam: qual = 'D1_VOLATILITY_ANOMALY_CANDIDATE'
        elif qmin < 0.05: qual = 'D1_DIRECTIONAL_ASYMMETRY_CANDIDATE'
        else: qual = 'RARE_D1_STRUCTURAL_OBSERVATION'
        note = 'candidat descriptif uniquement; jamais un PROFITABLE_EDGE'
        if fam.startswith('SEQUENCE'):
            qual = 'ARTEFACT_IDENTIFICATION_EX_POST_NON_CAUSAL'
            note = ("la fin de sequence n'est connue qu'apres la journee suivante (92,9 % de journees "
                    "suivantes de sens non identique par construction); controle causal (3e journee "
                    "consecutive de meme sens, connu a sa cloture): +2,7 bp (H1) / +6,0 bp (H5), "
                    "aucun effet; aucun candidat retenu")
        reg.append(dict(famille=fam, q_min=float(qmin), qualification=qual, note=note))
    pd.DataFrame(reg).to_csv(R21 / 'PHASE21A_D1_ANOMALY_REGISTRY.csv', index=False)
    stats = dict(n_jours_complets=int(len(d)), periode=[str(d.jour.min()), str(d.jour.max())],
                 regimes={e: int((d.regime == e).sum()) for e in ['D1_COMPRESSION', 'D1_NORMAL', 'D1_EXPANSION']},
                 n_tests=int(len(T)), n_q_significatifs=int((T.q_value_BH < .05).sum()) if len(T) else 0)
    (R21 / '_phase21a_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str))

if __name__ == '__main__': main()
