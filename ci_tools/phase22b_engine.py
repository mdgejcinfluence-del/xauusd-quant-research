#!/usr/bin/env python3
"""PHASE 22-B - Sorties structurelles des familles A et B (EXPLORATORY_POST_HOC, IS).
lot: pour les evenements certifies 22-A du lot, balayage tick entree->expiration:
     premier franchissement stop structurel vs objectif (prix executables reels,
     objectif liquide au niveau theorique conservateur, stop au premier prix observe).
analyse: agregats, bootstrap semaines ISO, BH, criteres cumulatifs de candidature sec.7.
Couts 19-B: spread une fois, S0/S1/S2 en prix, commissions exclues.
Resultats: HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R21 = ROOT / 'reports/meta_alpha/phase21'
R22 = ROOT / 'reports/meta_alpha/phase22'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
GRAINE = 2119
NBOOT = 10000


def telecharger_batch(batch):
    tok = os.environ['KAGGLE_API_TOKEN']
    import requests
    url = f'https://www.kaggle.com/api/v1/datasets/download/shalom5123/{batch}'
    r = None
    for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None), ({}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
        r = requests.get(url, headers=hdrs, auth=auth, timeout=900)
        print('Kaggle', batch, r.status_code, flush=True)
        if r.status_code == 200: break
    if r is None or r.status_code != 200: raise RuntimeError('Kaggle KO ' + batch)
    dd = pathlib.Path('/tmp/kbatch'); shutil.rmtree(dd, ignore_errors=True); dd.mkdir(parents=True)
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(dd)
    return dd


def logbp(a, b): return 10000 * np.log(b / a)


def nets(direction, entree, sortie, exec_cote):
    """sortie: prix executable brut (bid si long, ask si short). Retourne dict scenarios."""
    out = {}
    for nom, s in [('S0', 0.0), ('S1', 0.5), ('S2', 1.0)]:
        if direction > 0:
            out[f'NET_{nom}_BP'] = float(logbp(np.array([entree * (1 + s / 10000)]), np.array([sortie * (1 - s / 10000)]))[0])
        else:
            out[f'NET_{nom}_BP'] = float(logbp(np.array([sortie * (1 + s / 10000)]), np.array([entree * (1 - s / 10000)]))[0])
    return out


def premier(cond):
    w = np.where(cond)[0]
    return int(w[0]) if len(w) else None


def mode_lot():
    """Traitement borne par journee (memoire limitee): requetes DuckDB par jour."""
    import duckdb
    batch = os.environ['P22_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'
    NS = 10**9

    def requete(debut, fin):
        a = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                            WHERE timestamp_utc >= '{debut}' AND timestamp_utc < '{fin}'
                            ORDER BY timestamp_utc""").fetchnumpy()
        return (a['ts'].astype('datetime64[ns]').astype('int64'),
                a['bid'].astype(float), a['ask'].astype(float))

    jours_dispo = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                                  WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    jours_lot = set(pd.to_datetime(jours_dispo).strftime('%Y-%m-%d'))
    print('lot', batch, len(jours_lot), 'jours disponibles', flush=True)

    ev = pd.read_parquet(R22 / 'PHASE22A_SWEEP_RECLAIM_EVENTS.parquet')
    ev = ev[(ev.statut == 'SWEEP_RECLAIM_CONFIRME') & (ev.population == 'PRIMAIRE')]
    cat = pd.read_parquet(R22 / 'PHASE22A_SWEEP_LEVEL_CATALOG.parquet').set_index(['jour', 'LEVEL_ID'])
    ev = ev[ev.jour.isin(jours_lot)]
    rowsA = []
    for jour, gev in ev.groupby('jour'):
        tt, bid, ask = requete(jour, (pd.Timestamp(jour) + pd.Timedelta(days=1)).strftime('%Y-%m-%d'))
        if len(tt) < 10: continue
        mid = (bid + ask) / 2.0; spread = logbp(bid, ask)
        for r in gev.itertuples():
            i_frac = int(np.searchsorted(tt, pd.Timestamp(r.ts_franchissement).value))
            i_ent = int(np.searchsorted(tt, pd.Timestamp(r.ts_reintegration).value))
            if i_ent >= len(tt): continue
            lo5 = max(0, int(np.searchsorted(tt, tt[i_frac] - 300 * NS))) if i_frac < len(tt) else 0
            buf = float(np.median(spread[lo5:i_frac])) if i_frac > 0 else float(spread[0])
            d = int(r.direction_candidate); entree = float(r.prix_entree)
            extreme = float(r.extreme_balayee)
            stop_ref = extreme * np.exp(buf / 10000) if d < 0 else extreme * np.exp(-buf / 10000)
            ligne = cat.loc[(r.jour, r.LEVEL_ID)]
            if isinstance(ligne, pd.DataFrame): ligne = ligne.iloc[0]
            boite_h, boite_l = max(ligne.niveau_prix, ligne.oppose_reference), min(ligne.niveau_prix, ligne.oppose_reference)
            centre = float(np.sqrt(boite_h * boite_l)); oppose = float(ligne.oppose_reference)
            for arch, cible in [('CENTRE', centre), ('OPPOSE', oppose)]:
                if d < 0:
                    i_stop = premier(ask[i_ent:] >= stop_ref); i_cib = premier(ask[i_ent:] <= cible)
                else:
                    i_stop = premier(bid[i_ent:] <= stop_ref); i_cib = premier(bid[i_ent:] >= cible)
                i_stop = None if i_stop is None else i_stop + i_ent
                i_cib = None if i_cib is None else i_cib + i_ent
                if i_stop is not None and i_cib is not None and i_stop == i_cib:
                    resultat, i_sort, prix_sort = 'ORDER_SEQUENCE_AMBIGUOUS', i_stop, (ask[i_stop] if d < 0 else bid[i_stop])
                elif i_stop is not None and (i_cib is None or i_stop < i_cib):
                    resultat, i_sort, prix_sort = 'STOP_AVANT_OBJECTIF', i_stop, (ask[i_stop] if d < 0 else bid[i_stop])
                elif i_cib is not None:
                    resultat, i_sort, prix_sort = 'OBJECTIF_AVANT_STOP', i_cib, cible
                else:
                    resultat, i_sort = 'EXPIRATION', len(tt) - 1
                    prix_sort = ask[i_sort] if d < 0 else bid[i_sort]
                seg = mid[i_ent:i_sort + 1]
                if d > 0:
                    mfe = float(logbp(np.array([mid[i_ent]]), np.array([seg.max()]))[0])
                    mae = float(logbp(np.array([seg.min()]), np.array([mid[i_ent]]))[0])
                else:
                    mfe = float(logbp(np.array([seg.min()]), np.array([mid[i_ent]]))[0])
                    mae = float(logbp(np.array([mid[i_ent]]), np.array([seg.max()]))[0])
                row = dict(SWEEP_EVENT_ID=r.SWEEP_EVENT_ID, jour=r.jour, LEVEL_ID=r.LEVEL_ID, architecture=arch,
                           direction=d, resultat=resultat, prix_entree=entree, prix_sortie=float(prix_sort),
                           stop_reference=float(stop_ref), cible=float(cible), buffer_bp=buf,
                           distance_stop_bp=float(abs(logbp(np.array([entree]), np.array([stop_ref]))[0])),
                           distance_cible_bp=float(abs(logbp(np.array([entree]), np.array([cible]))[0])),
                           delai_evenement_min=float((tt[i_sort] - tt[i_ent]) / (60 * NS)), MFE_BP=mfe, MAE_BP=mae,
                           semaine_iso=pd.Timestamp(r.jour).strftime('%G-W%V'), annee=pd.Timestamp(r.jour).year,
                           gap_dans_fenetre=bool((np.diff(tt[i_ent:i_sort + 1]) > 300 * NS).any()) if i_sort > i_ent else False)
                row.update(nets(d, entree, float(prix_sort), None))
                row['ratio_structurel'] = row['distance_cible_bp'] / row['distance_stop_bp'] if row['distance_stop_bp'] > 0 else np.nan
                rowsA.append(row)
        print('A jour traite', jour, flush=True)

    inpB = pd.read_parquet(R22 / 'PHASE22B_FAMILY_B_INPUT.parquet')
    inpB['jour_entree'] = pd.to_datetime(inpB.ts_entree).dt.strftime('%Y-%m-%d')
    inpB = inpB[inpB.jour_entree.isin(jours_lot)]
    rowsB = []
    for jour, gin in inpB.groupby('jour_entree'):
        debut_f = pd.Timestamp(gin.ts_entree.min()) - pd.Timedelta(minutes=10)
        fin_f = pd.Timestamp(gin.ts_expiration.max()) + pd.Timedelta(minutes=1)
        tt, bid, ask = requete(debut_f.strftime('%Y-%m-%d %H:%M:%S'), fin_f.strftime('%Y-%m-%d %H:%M:%S'))
        if len(tt) < 10: continue
        mid = (bid + ask) / 2.0
        for r in gin.itertuples():
            i_ent = int(np.searchsorted(tt, pd.Timestamp(r.ts_entree).value))
            i_conf = i_ent
            i_exp = int(np.searchsorted(tt, pd.Timestamp(r.ts_expiration).value, side='right') - 1)
            if i_ent >= len(tt) or i_exp <= i_ent: continue
            lo5 = max(0, int(np.searchsorted(tt, tt[i_conf] - 300 * NS)))
            buf = float(np.median(logbp(bid[lo5:i_conf], ask[lo5:i_conf]))) if i_conf > 0 else float(logbp(bid[:1], ask[:1])[0])
            d = int(r.direction)
            entree = ask[i_ent] if d > 0 else bid[i_ent]
            stop_ref = float(r.pullback_extreme) * np.exp(-buf / 10000) if d > 0 else float(r.pullback_extreme) * np.exp(buf / 10000)
            R_bp = float(logbp(np.array([stop_ref]), np.array([entree]))[0]) if d > 0 else float(logbp(np.array([entree]), np.array([stop_ref]))[0])
            if R_bp <= 0:
                rowsB.append(dict(IMPULSE_EPISODE_ID=r.IMPULSE_EPISODE_ID, statut='INVALID_STRUCTURAL_RISK')); continue
            seg_m = mid[i_ent:i_exp + 1]; m_ent = seg_m[0]
            mfe = float(logbp(np.array([m_ent]), np.array([seg_m.max()]))[0]) if d > 0 else float(logbp(np.array([seg_m.min()]), np.array([m_ent]))[0])
            mae = float(logbp(np.array([seg_m.min()]), np.array([m_ent]))[0]) if d > 0 else float(logbp(np.array([m_ent]), np.array([seg_m.max()]))[0])
            for K in (1.5, 2.0):
                cible = entree * np.exp(d * K * R_bp / 10000)
                if d > 0:
                    i_stop = premier(bid[i_ent:i_exp + 1] <= stop_ref); i_cib = premier(bid[i_ent:i_exp + 1] >= cible)
                else:
                    i_stop = premier(ask[i_ent:i_exp + 1] >= stop_ref); i_cib = premier(ask[i_ent:i_exp + 1] <= cible)
                if i_stop is not None and i_cib is not None and i_stop == i_cib:
                    resultat, ii, prix_sort = 'ORDER_SEQUENCE_AMBIGUOUS', i_stop, (bid[i_ent + i_stop] if d > 0 else ask[i_ent + i_stop])
                elif i_stop is not None and (i_cib is None or i_stop < i_cib):
                    resultat, ii = 'STOP_AVANT_TP', i_stop; prix_sort = bid[i_ent + ii] if d > 0 else ask[i_ent + ii]
                elif i_cib is not None:
                    resultat, ii, prix_sort = 'TP_AVANT_STOP', i_cib, cible
                else:
                    resultat, ii = 'EXPIRATION', i_exp - i_ent; prix_sort = bid[i_exp] if d > 0 else ask[i_exp]
                row = dict(IMPULSE_EPISODE_ID=r.IMPULSE_EPISODE_ID, direction=d, objectif_K=K, resultat=resultat,
                           R_BP=R_bp, prix_entree=float(entree), prix_sortie=float(prix_sort), stop_reference=float(stop_ref),
                           cible=float(cible), MFE_BP=mfe, MAE_BP=mae, buffer_bp=buf,
                           duree_min=float((tt[i_ent + ii] - tt[i_ent]) / (60 * NS)),
                           semaine_iso=r.semaine_iso, annee=pd.Timestamp(r.ts_entree).year,
                           gap_dans_fenetre=bool((np.diff(tt[i_ent:i_ent + ii + 1]) > 300 * NS).any()) if ii > 0 else False,
                           ecart_entree_22a_bp=float(logbp(np.array([r.prix_entree_22a]), np.array([entree]))[0]))
                row.update(nets(d, float(entree), float(prix_sort), None))
                row['R_realise'] = row['NET_S2_BP'] / R_bp
                rowsB.append(row)
    R22.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rowsA).to_parquet(R22 / f'P22B_A_{batch}.parquet', index=False)
    pd.DataFrame(rowsB).to_parquet(R22 / f'P22B_B_{batch}.parquet', index=False)
    print('lot termine', batch, len(rowsA), 'A-architectures', len(rowsB), 'B-objectifs', flush=True)


def boot0(a, col, rng):
    ev = len(a) >= 50 and a.semaine_iso.nunique() >= 20
    if not ev: return np.nan, np.nan, (np.nan, np.nan), False
    w = a.semaine_iso.unique(); g = {x: v[col].values for x, v in a.groupby('semaine_iso')}
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([g[x] for x in rng.choice(w, len(w), replace=True)]).mean()
    return a[col].mean(), 2 * min((boots <= 0).mean(), (boots >= 0).mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def mode_analyse():
    def lire(motif):
        frames = []
        for f in sorted(glob.glob(str(R22 / motif))):
            d = pd.read_parquet(f); d['lot_source'] = pathlib.Path(f).stem.rsplit('_', 1)[-1]; frames.append(d)
        return pd.concat(frames).reset_index(drop=True)
    A = lire('P22B_A_*.parquet'); B = lire('P22B_B_*.parquet')
    ev = pd.read_parquet(R22 / 'PHASE22A_SWEEP_RECLAIM_EVENTS.parquet')
    nA = int(((ev.statut == 'SWEEP_RECLAIM_CONFIRME') & (ev.population == 'PRIMAIRE')).sum())
    rec = [dict(famille='A', evenements_22a_primaires=nA, evenements_22b_resultats=int(A.SWEEP_EVENT_ID.nunique()),
                architectures=int(len(A)), manquants=nA - int(A.SWEEP_EVENT_ID.nunique())),
           dict(famille='B', evenements_22a_primaires=505, evenements_22b_resultats=int(B.IMPULSE_EPISODE_ID.nunique()) if 'IMPULSE_EPISODE_ID' in B else 0,
                architectures=int(len(B)), manquants=505 - (int(B.IMPULSE_EPISODE_ID.nunique()) if 'IMPULSE_EPISODE_ID' in B else 0))]
    pd.DataFrame(rec).to_csv(R22 / 'PHASE22B_EVENT_RECONCILIATION.csv', index=False)
    A.to_parquet(R22 / 'PHASE22B_SWEEP_STRUCTURAL_EXIT_RESULTS.parquet', index=False)
    Bv = B[B.statut.isna() | (B.statut != 'INVALID_STRUCTURAL_RISK')] if 'statut' in B else B
    Bv.to_parquet(R22 / 'PHASE22B_IMPULSE_STRUCTURAL_EXIT_RESULTS.parquet', index=False)

    A.groupby(['LEVEL_ID', 'architecture', 'resultat']).size().unstack(fill_value=0).to_csv(R22 / 'PHASE22B_SWEEP_TARGET_FIRST_TOUCH.csv')
    Bv.groupby(['objectif_K', 'resultat']).agg(
        n=('NET_S2_BP', 'count'), net_S2_moyen=('NET_S2_BP', 'mean'), net_S2_median=('NET_S2_BP', 'median'),
        R_median=('R_BP', 'median'), R_realise_moyen=('R_realise', 'mean'), duree_mediane_min=('duree_min', 'median')
    ).reset_index().to_csv(R22 / 'PHASE22B_IMPULSE_R_MULTIPLE_RESULTS.csv', index=False)

    comp = []
    for nom, gg in [('A', A), ('B', Bv)]:
        for s in ('S0', 'S1', 'S2'):
            comp.append(dict(famille=nom, scenario=s, n=len(gg), moyenne=gg[f'NET_{s}_BP'].mean(), mediane=gg[f'NET_{s}_BP'].median(),
                             taux_positif=float((gg[f'NET_{s}_BP'] > 0).mean())))
    pd.DataFrame(comp).to_csv(R22 / 'PHASE22B_S0_S1_S2_COMPARISON.csv', index=False)

    rng = np.random.default_rng(GRAINE)
    tests = []
    for (lvl, arch), gg in A.groupby(['LEVEL_ID', 'architecture']):
        eff, p, ci, evl = boot0(gg, 'NET_S2_BP', rng)
        tests.append(dict(famille='A', comparaison=f'{lvl} cible {arch}', n=len(gg), semaines=gg.semaine_iso.nunique(),
                          effet=eff, IC95_bas=ci[0], IC95_haut=ci[1], p_value=p, statut='EVALUE' if evl else 'NON_EVALUABLE_INFERENTIAL'))
    for K, gg in Bv.groupby('objectif_K'):
        eff, p, ci, evl = boot0(gg, 'NET_S2_BP', rng)
        tests.append(dict(famille='B', comparaison=f'TP {K}R', n=len(gg), semaines=gg.semaine_iso.nunique(),
                          effet=eff, IC95_bas=ci[0], IC95_haut=ci[1], p_value=p, statut='EVALUE' if evl else 'NON_EVALUABLE_INFERENTIAL'))
    T = pd.DataFrame(tests)
    q = np.full(len(T), np.nan); idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; o = np.argsort(pv); m_ = len(pv)
        qq = pv[o] * m_ / (np.arange(m_) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[o])] = np.minimum(qq, 1)
    T['q_value_BH'] = q

    reg = []
    for _, r in T.iterrows():
        gg = A[(A.LEVEL_ID == r.comparaison.split(' cible')[0]) & (A.architecture == r.comparaison.split('cible ')[-1])] if r.famille == 'A' else Bv[Bv.objectif_K == float(r.comparaison.split('TP ')[-1].replace('R', ''))]
        candidat = bool(r.statut == 'EVALUE' and r.IC95_bas > 0)
        stab = ''
        if len(gg):
            a1 = gg[gg.annee <= 2015].NET_S2_BP.mean(); a2 = gg[gg.annee >= 2016].NET_S2_BP.mean()
            stab = f'2010-2015 {a1:.2f} bp; 2016-2019 {a2:.2f} bp'
            if candidat and np.sign(a1) != np.sign(a2): candidat = False
        reg.append(dict(famille=r.famille, configuration=r.comparaison, n=r.n, esperance_S2=r.effet, IC95_bas=r.IC95_bas,
                        IC95_haut=r.IC95_haut, q_value=r.q_value_BH, stabilite=stab,
                        verdict='CANDIDATE_EXPLORATORY_CRITERIA_MET' if candidat else 'NOT_CANDIDATE'))
    pd.DataFrame(reg).to_csv(R22 / 'PHASE22B_CANDIDATE_REGISTRY.csv', index=False)
    T.to_csv(R22 / 'PHASE22B_MULTIPLE_TEST_CORRECTION.csv', index=False)

    (R22 / 'PHASE22B_SWEEP_STOP_RISK_AUDIT.md').write_text(
        '# PHASE 22-B — AUDIT STOP FAMILLE A\n\nStop = extreme balaye Mid +/- buffer spread pre-franchissement (22-A). '
        'Declenchement sur premier prix executable (Ask short / Bid long) franchissant le niveau; sortie au prix '
        'reellement observe, jamais forcee au niveau theorique. Objectif liquide au niveau theorique conservateur '
        '(remplissage limite non certifie). Voir PHASE22B_SWEEP_TARGET_FIRST_TOUCH.csv pour les issues.\n')
    (R22 / 'PHASE22B_EXECUTION_AND_GAP_AUDIT.md').write_text(
        f"# PHASE 22-B — AUDIT EXECUTION ET GAPS\n\n- A: resultats {len(A)}, fenetres avec gap > 300 s: {int(A.gap_dans_fenetre.sum()) if len(A) else 0}\n"
        f"- B: resultats {len(Bv)}, fenetres avec gap > 300 s: {int(Bv.gap_dans_fenetre.sum()) if len(Bv) else 0}, "
        f"sequences ambigues: {int((Bv.resultat == 'ORDER_SEQUENCE_AMBIGUOUS').sum()) if len(Bv) else 0}\n"
        '- Aucun remplissage reel revendique; objectifs liquides au niveau theorique (conservateur); stops au premier prix observe.\n')
    lignes = ['# PHASE 22-B — AUDIT QUEUES ET DRAWDOWN', '']
    for nom, gg in [('A', A), ('B', Bv)]:
        if len(gg):
            s = gg.sort_values(['annee', 'jour' if 'jour' in gg else 'IMPULSE_EPISODE_ID']).NET_S2_BP if 'jour' in gg else gg.NET_S2_BP
            cum = s.cumsum(); dd = (cum - cum.cummax()).min()
            lignes.append(f"- {nom}: P5 {gg.NET_S2_BP.quantile(.05):.1f} bp, pire {gg.NET_S2_BP.min():.1f} bp, "
                          f"pertes >50 bp: {float((gg.NET_S2_BP < -50).mean()):.3f}, drawdown sequence (ordre chronologique, descriptif): {dd:.0f} bp")
    (R22 / 'PHASE22B_TAIL_AND_DRAWDOWN_AUDIT.md').write_text('\n'.join(lignes))
    (R22 / 'PHASE22B_CLUSTERED_UNCERTAINTY.md').write_text(
        '# PHASE 22-B — INCERTITUDE PAR GRAPPES\n\nBootstrap semaines ISO 10 000 replications graine 2119, '
        'BH q=0,05 sur 10 tests (A: 4 niveaux x 2 cibles; B: TP 1,5R/2R). Candidature sec.7 cumulative: '
        'esperance S2 > 0, borne IC95 > 0, pas d inversion severe entre sous-periodes, queues documentees.\n')
    stab_l = ['# PHASE 22-B — STABILITE TEMPORELLE', '']
    for (lvl, arch), gg in A.groupby(['LEVEL_ID', 'architecture']):
        stab_l.append(f"- A {lvl} {arch}: 2010-2015 {gg[gg.annee <= 2015].NET_S2_BP.mean():.2f} bp (n={int((gg.annee <= 2015).sum())}); "
                      f"2016-2019 {gg[gg.annee >= 2016].NET_S2_BP.mean():.2f} bp (n={int((gg.annee >= 2016).sum())})")
    for K, gg in Bv.groupby('objectif_K'):
        stab_l.append(f"- B TP{K}R: 2010-2015 {gg[gg.annee <= 2015].NET_S2_BP.mean():.2f} bp; 2016-2019 {gg[gg.annee >= 2016].NET_S2_BP.mean():.2f} bp")
    (R22 / 'PHASE22B_TEMPORAL_STABILITY.md').write_text('\n'.join(stab_l))
    (R22 / 'PHASE22B_FAMILY_COMPARISON.md').write_text(
        '# PHASE 22-B — COMPARAISON DES FAMILLES (SEPAREES)\n\nAucun portefeuille combine, aucune correlation presumee. '
        'Voir PHASE22B_CANDIDATE_REGISTRY.csv et PHASE22B_FINAL_REPORT.md.\n')
    stats = dict(A_resultats=int(len(A)), B_resultats=int(len(Bv)), n_tests=int(len(T)), n_sig=int((T.q_value_BH < .05).sum()),
                 candidats=int((pd.DataFrame(reg).verdict == 'CANDIDATE_EXPLORATORY_CRITERIA_MET').sum()) if reg else 0)
    (R22 / '_phase22b_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str))


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
