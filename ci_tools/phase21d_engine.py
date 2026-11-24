#!/usr/bin/env python3
"""PHASE 21-D - Anatomie tick par tick des grandes amplitudes D1 (EXPLORATORY_POST_HOC, IS).
lot: par lot Kaggle IS, chemins tick journaliers des journees certifiees 21-A
     (records, premiers passages 30/60/100 bp, chemins post-passage, spread).
analyse: consolidation, chronologie exacte des extremes, comparaison declencheur
     haut/bas, bootstrap par grappes de semaines ISO, BH. Aucun modele/strategie/
     P&L. Holdout jamais accede. Ordre final des extremes = retrospectif uniquement."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R21 = ROOT / 'reports/meta_alpha/phase21'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
GRAINE = 2115
NBOOT = 10000
SEUILS = (30, 60, 100)
HORIZONS_H = (1, 2, 4)


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


def mode_lot():
    import duckdb
    batch = os.environ['P21_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    cert = pd.read_parquet(R21 / 'PHASE21A_D1_BARSET.parquet')
    jours_cert = set(cert.jour.dt.strftime('%Y-%m-%d'))
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'
    df = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                         WHERE timestamp_utc < '{IS_END}' ORDER BY timestamp_utc""").df()
    ts = pd.to_datetime(df.ts).values.astype('datetime64[ns]')
    bid_all = df.bid.values.astype(np.float64); ask_all = df.ask.values.astype(np.float64)
    del df
    mid_all = (bid_all + ask_all) / 2.0
    spread_all = logbp(bid_all, ask_all)
    # groupes de jours par ordinal (aucune chaine par tick: economie memoire lots denses)
    ord_jour = ts.astype('datetime64[D]')
    uniques, debuts = np.unique(ord_jour, return_index=True)
    bornes = list(debuts) + [len(ts)]
    groupes_jours = []
    for k, u in enumerate(uniques):
        js = str(u)
        if js in jours_cert:
            groupes_jours.append((js, np.arange(bornes[k], bornes[k + 1])))
    print('lot', batch, len(ts), 'ticks,', len(groupes_jours), 'journees certifiees', flush=True)
    day_rows, pass_rows, post_rows, rec_rows, spread_rows = [], [], [], [], []
    NS_H = 3600 * 10**9
    for js, idx in groupes_jours:
        tt = ts[idx].astype('int64')
        m = mid_all[idx]; sp = spread_all[idx]
        bid_j, ask_j = bid_all[idx], ask_all[idx]
        o = m[0]
        runh = np.maximum.accumulate(m); runl = np.minimum.accumulate(m)
        crange = logbp(runl, runh)
        gaps = np.diff(tt) / 1e9
        fh, fl = runh[-1], runl[-1]
        i_fh_first = int(np.argmax(m >= fh)); i_fl_first = int(np.argmax(m <= fl))
        i_fh_last = int(len(m) - 1 - np.argmax((m >= fh)[::-1])); i_fl_last = int(len(m) - 1 - np.argmax((m <= fl)[::-1]))
        rec_h = np.where(np.r_[True, np.diff(runh) > 0])[0]
        rec_l = np.where(np.r_[True, np.diff(runl) > 0])[0]
        ordre = ('HIGH_FINAL_FIRST' if tt[i_fh_first] < tt[i_fl_first] else
                 'LOW_FINAL_FIRST' if tt[i_fl_first] < tt[i_fh_first] else 'FINAL_EXTREMES_SAME_TIMESTAMP')
        day_rows.append(dict(jour=js, n_ticks=len(m), open_tick=o, high_tick=fh, low_tick=fl, close_tick=m[-1],
                             ts_premier_high_final=pd.Timestamp(ts[idx][i_fh_first]), ts_premier_low_final=pd.Timestamp(ts[idx][i_fl_first]),
                             ts_dernier_high_final=pd.Timestamp(ts[idx][i_fh_last]), ts_dernier_low_final=pd.Timestamp(ts[idx][i_fl_last]),
                             ordre_extremes_finaux=ordre, n_records_high=len(rec_h), n_records_low=len(rec_l),
                             doublons_ts=int(len(tt) - len(np.unique(tt))), bid_sup_ask=int((bid_j > ask_j).sum()),
                             prix_non_positifs=int(((bid_j <= 0) | (ask_j <= 0)).sum()),
                             max_gap_s=float(gaps.max()) if len(gaps) else 0.0,
                             n_gaps_sup_300s=int((gaps > 300).sum()), spread_mediane_bp=float(np.median(sp)),
                             duree_premier_au_dernier_high_s=float((tt[i_fh_last] - tt[i_fh_first]) / 1e9)))
        # catalogue records
        prev_t = tt[0]; prev_h = prev_l = o
        recs = sorted([(tt[i], 'RECORD_HIGH', m[i], runh[i], runl[i]) for i in rec_h] +
                      [(tt[i], 'RECORD_LOW', m[i], runh[i], runl[i]) for i in rec_l])
        for k, (t_, side, px, rh, rl) in enumerate(recs):
            if side == 'RECORD_HIGH':
                dist = logbp(np.array([o]), np.array([rh]))[0]; ext = logbp(np.array([prev_h]), np.array([rh]))[0] if k else 0.0; prev_h = rh
            else:
                dist = -logbp(np.array([rl]), np.array([o]))[0]; ext = logbp(np.array([rl]), np.array([prev_l]))[0] if k else 0.0; prev_l = rl
            rec_rows.append(dict(jour=js, ts=pd.Timestamp(t_), type=side, prix_mid=px, distance_ouverture_bp=dist,
                                 extension_bp=float(ext), delai_depuis_record_prec_s=float((t_ - prev_t) / 1e9),
                                 range_cumule_bp=float(logbp(np.array([rl]), np.array([rh]))[0]), rang_record=k + 1))
            prev_t = t_
        # premiers passages
        for s in SEUILS:
            hit = np.where(crange >= s)[0]
            if not len(hit):
                pass_rows.append(dict(jour=js, seuil_bp=s, statut='THRESHOLD_NOT_REACHED'))
                continue
            i = int(hit[0])
            trig = 'HIGH' if runh[i] > (runh[i - 1] if i else o) else ('LOW' if runl[i] < (runl[i - 1] if i else o) else 'BOTH')
            if runh[i] > (runh[i - 1] if i else o) and runl[i] < (runl[i - 1] if i else o): trig = 'BOTH'
            tranche = int(pd.Timestamp(ts[idx][i]).hour // 4 + 1)
            pass_rows.append(dict(jour=js, seuil_bp=s, statut='ATTEINT', ts_passage=pd.Timestamp(ts[idx][i]), tranche_h4=tranche,
                                  cote_declencheur=trig, temps_ecoule_min=float(tt[i] - tt[0]) / 60e9,
                                  temps_restant_min=float(tt[-1] - tt[i]) / 60e9,
                                  up_excursion_connue_bp=float(logbp(np.array([o]), np.array([runh[i]]))[0]),
                                  down_excursion_connue_bp=float(logbp(np.array([runl[i]]), np.array([o]))[0]),
                                  range_cumule_bp=float(crange[i]), n_records_avant=int(((rec_h <= i).sum() + (rec_l <= i).sum())),
                                  spread_au_passage_bp=float(sp[i])))
            win_av = sp[(tt >= tt[i] - 5 * 60 * 10**9) & (tt < tt[i])]
            win_ap = sp[(tt > tt[i]) & (tt <= tt[i] + 5 * 60 * 10**9)]
            spread_rows.append(dict(jour=js, seuil_bp=s, cote_declencheur=trig,
                                    spread_avant_mediane=float(np.median(win_av)) if len(win_av) else np.nan,
                                    spread_au_passage_bp=float(sp[i]),
                                    spread_apres_mediane=float(np.median(win_ap)) if len(win_ap) else np.nan,
                                    n_ticks_avant=len(win_av), n_ticks_apres=len(win_ap)))
            for hn, hlim in [(f'{h}h', h * NS_H) for h in HORIZONS_H] + [('EOD', None)]:
                j_end = len(m) - 1 if hlim is None else int(np.searchsorted(tt, tt[i] + hlim, side='right') - 1)
                if j_end <= i:
                    post_rows.append(dict(jour=js, seuil_bp=s, horizon=hn, censure=True)); continue
                seg = slice(i, j_end + 1)
                f_up = logbp(np.array([m[i]]), np.array([m[seg].max()]))[0]
                f_dn = logbp(np.array([m[seg].min()]), np.array([m[i]]))[0]
                if trig == 'HIGH':
                    ext_trig = logbp(np.array([runh[i]]), np.array([max(runh[i], m[seg].max())]))[0]
                    ext_opp = logbp(np.array([min(runl[i], m[seg].min())]), np.array([runl[i]]))[0]
                elif trig == 'LOW':
                    ext_trig = logbp(np.array([min(runl[i], m[seg].min())]), np.array([runl[i]]))[0]
                    ext_opp = logbp(np.array([runh[i]]), np.array([max(runh[i], m[seg].max())]))[0]
                else:
                    ext_trig = ext_opp = np.nan
                post_rows.append(dict(jour=js, seuil_bp=s, horizon=hn, censure=False, cote_declencheur=trig,
                                      extension_declencheur_bp=float(ext_trig), extension_opposee_bp=float(ext_opp),
                                      FUTURE_UP_BP=float(f_up), FUTURE_DOWN_BP=float(f_dn),
                                      TERMINAL_BP=float(logbp(np.array([m[i]]), np.array([m[j_end]]))[0]),
                                      range_cumule_final_horizon_bp=float(crange[j_end]),
                                      extension_range_bp=float(crange[j_end] - crange[i]),
                                      retracement_depuis_extreme_bp=float(abs(logbp(np.array([m[seg].max() if trig != 'LOW' else m[seg].min()]), np.array([m[j_end]]))[0]))))
    R21.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(day_rows).to_csv(R21 / f'P21D_DAY_{batch}.csv', index=False)
    pd.DataFrame(pass_rows).to_csv(R21 / f'P21D_PASSAGE_{batch}.csv', index=False)
    pd.DataFrame(post_rows).to_csv(R21 / f'P21D_POST_{batch}.csv', index=False)
    pd.DataFrame(rec_rows).to_csv(R21 / f'P21D_RECORD_{batch}.csv', index=False)
    pd.DataFrame(spread_rows).to_csv(R21 / f'P21D_SPREAD_{batch}.csv', index=False)
    print('lot termine', batch, len(day_rows), 'jours', len(pass_rows), 'passages', len(rec_rows), 'records', flush=True)


def boot_diff(a, b, mesure, rng):
    ev = len(a) >= 50 and len(b) >= 50 and a.semaine_iso.nunique() >= 20 and b.semaine_iso.nunique() >= 20
    if not ev: return np.nan, np.nan, (np.nan, np.nan), False
    wa, wb = a.semaine_iso.unique(), b.semaine_iso.unique()
    ga = {w: x[mesure].values for w, x in a.groupby('semaine_iso')}
    gb = {w: x[mesure].values for w, x in b.groupby('semaine_iso')}
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([ga[w] for w in rng.choice(wa, len(wa), replace=True)]).mean() - \
                   np.concatenate([gb[w] for w in rng.choice(wb, len(wb), replace=True)]).mean()
    return a[mesure].mean() - b[mesure].mean(), 2 * min((boots <= 0).mean(), (boots >= 0).mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def mode_analyse():
    day = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R21 / 'P21D_DAY_*.csv')))])
    pas = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R21 / 'P21D_PASSAGE_*.csv')))])
    post = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R21 / 'P21D_POST_*.csv')))])
    rec = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R21 / 'P21D_RECORD_*.csv')))])
    spr = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R21 / 'P21D_SPREAD_*.csv')))])
    d1 = pd.read_parquet(R21 / 'PHASE21A_D1_BARSET.parquet')
    d1['jour'] = d1.jour.dt.strftime('%Y-%m-%d')
    info = d1.set_index('jour')
    for df in (day, pas, post, rec, spr):
        df['semaine_iso'] = pd.to_datetime(df.jour).dt.strftime('%G-W%V')
        df['annee'] = pd.to_datetime(df.jour).dt.year
    day['regime'] = day.jour.map(info.regime); day['RANGE_BP_D1'] = day.jour.map(info.RANGE_BP)
    day.to_parquet(R21 / 'PHASE21D_DAILY_TICK_PATH.parquet', index=False)
    day[['jour', 'ts_premier_high_final', 'ts_premier_low_final', 'ts_dernier_high_final', 'ts_dernier_low_final',
         'ordre_extremes_finaux', 'n_records_high', 'n_records_low', 'duree_premier_au_dernier_high_s',
         'RANGE_BP_D1', 'regime']].to_csv(R21 / 'PHASE21D_FINAL_EXTREME_CHRONOLOGY.csv', index=False)
    pas.to_parquet(R21 / 'PHASE21D_FIRST_PASSAGE_EVENTS.parquet', index=False)
    post.to_parquet(R21 / 'PHASE21D_POST_PASSAGE_PATHS.parquet', index=False)
    rec.to_parquet(R21 / 'PHASE21D_RECORD_SEQUENCE_CATALOG.parquet', index=False)

    audit = ['# PHASE 21-D — AUDIT SOURCE TICK', '', 'Statut : EXPLORATORY_POST_HOC. Ticks IS Kaggle '
             '(timestamp_utc, bid, ask), Mid=(bid+ask)/2, journees certifiees 21-A uniquement, holdout jamais accede.', '',
             f"- Journees tick reconstruites : {day.jour.nunique()} (certifiees 21-A : {len(info)})",
             f"- Ticks totaux traites : {int(day.n_ticks.sum())}",
             f"- Doublons timestamp : {int(day.doublons_ts.sum())} ; bid>ask : {int(day.bid_sup_ask.sum())} ; prix non positifs : {int(day.prix_non_positifs.sum())}",
             f"- Journees avec gap > 300 s : {int((day.n_gaps_sup_300s > 0).sum())} (cause non etablie : GAP_CAUSE_UNVERIFIED)",
             '- Aucune interpolation, aucun comblement. Ordre final des extremes : retrospectif uniquement, jamais predictif.']
    (R21 / 'PHASE21D_TICK_SOURCE_AUDIT.md').write_text('\n'.join(audit))

    atteints = pas[pas.statut == 'ATTEINT']
    comp = atteints.groupby(['seuil_bp', 'cote_declencheur']).agg(
        n=('jour', 'count'), semaines=('semaine_iso', 'nunique'), temps_ecoule_median_min=('temps_ecoule_min', 'median'),
        up_connue_mediane=('up_excursion_connue_bp', 'median'), down_connue_mediane=('down_excursion_connue_bp', 'median')).reset_index()
    postm = post[~post.censure].groupby(['seuil_bp', 'cote_declencheur', 'horizon']).agg(
        extension_declencheur_mediane=('extension_declencheur_bp', 'median'), extension_opposee_mediane=('extension_opposee_bp', 'median'),
        terminal_median=('TERMINAL_BP', 'median')).reset_index()
    comp.merge(postm, on=['seuil_bp', 'cote_declencheur'], how='left').to_csv(R21 / 'PHASE21D_UP_DOWN_TRIGGER_COMPARISON.csv', index=False)

    cov = []
    pp = post[~post.censure].copy()
    pp['FAV'] = np.where(pp.cote_declencheur == 'HIGH', pp.FUTURE_UP_BP, pp.FUTURE_DOWN_BP)
    pp['ADV'] = np.where(pp.cote_declencheur == 'HIGH', pp.FUTURE_DOWN_BP, pp.FUTURE_UP_BP)
    for (s, c, h), gg in pp.groupby(['seuil_bp', 'cote_declencheur', 'horizon']):
        for ref in (4.0, 4.5):
            row = dict(seuil_bp=s, cote=c, horizon=h, reference_bp=ref, statut_reference='REFERENCE_COST_UNVERIFIED',
                       n=len(gg), MFE_mediane=gg.FAV.median(), MAE_mediane=gg.ADV.median())
            for k in (1, 2, 3, 5): row[f'part_MFE_sup_{k}x'] = float((gg.FAV > k * ref).mean())
            for s2 in SEUILS: row[f'part_ext_range_sup_{s2}bp'] = float((gg.extension_range_bp > s2).mean())
            cov.append(row)
    pd.DataFrame(cov).to_csv(R21 / 'PHASE21D_AMPLITUDE_COST_COVERAGE.csv', index=False)
    spr.groupby(['seuil_bp', 'cote_declencheur']).agg(
        n=('jour', 'count'), spread_avant_mediane=('spread_avant_mediane', 'median'),
        spread_passage_mediane=('spread_au_passage_bp', 'median'), spread_apres_mediane=('spread_apres_mediane', 'median'),
        spread_passage_P90=('spread_au_passage_bp', lambda x: x.quantile(.9))).reset_index().to_csv(
        R21 / 'PHASE21D_SPREAD_MICROSTRUCTURE.csv', index=False)

    rng = np.random.default_rng(GRAINE)
    tests = []
    pp['TERMINAL_ALIGNE'] = np.where(pp.cote_declencheur == 'HIGH', pp.TERMINAL_BP, -pp.TERMINAL_BP)
    for s in SEUILS:
        for h in [f'{x}h' for x in HORIZONS_H] + ['EOD']:
            for mesure in ('extension_declencheur_bp', 'extension_opposee_bp', 'TERMINAL_ALIGNE'):
                a = pp[(pp.seuil_bp == s) & (pp.horizon == h) & (pp.cote_declencheur == 'HIGH')].dropna(subset=[mesure])
                b = pp[(pp.seuil_bp == s) & (pp.horizon == h) & (pp.cote_declencheur == 'LOW')].dropna(subset=[mesure])
                eff, p, ci, ev = boot_diff(a, b, mesure, rng)
                tests.append(dict(seuil_bp=s, horizon=h, mesure=mesure, comparaison='declencheur HIGH vs LOW',
                                  n1=len(a), n2=len(b), effet=eff, IC95_bas=ci[0], IC95_haut=ci[1], p_value=p,
                                  statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
    T = pd.DataFrame(tests)
    q = np.full(len(T), np.nan); idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; o = np.argsort(pv); m_ = len(pv)
        qq = pv[o] * m_ / (np.arange(m_) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[o])] = np.minimum(qq, 1)
    T['q_value_BH'] = q
    T.to_csv(R21 / 'PHASE21D_MULTIPLE_TEST_CORRECTION.csv', index=False)

    stab = []
    for per, m in [('complet', day.annee > 0), ('2010-2015', day.annee <= 2015), ('2016-2019', day.annee >= 2016)]:
        sub = atteints[m.loc[atteints.index] if False else (atteints.annee <= 2015 if per == '2010-2015' else atteints.annee >= 2016 if per == '2016-2019' else atteints.annee > 0)]
        for (s, c), gg in sub.groupby(['seuil_bp', 'cote_declencheur']):
            stab.append(dict(periode=per, seuil_bp=s, cote=c, n=len(gg), temps_ecoule_median_min=gg.temps_ecoule_min.median()))
        for o_, gg in day[m].groupby('ordre_extremes_finaux'):
            stab.append(dict(periode=per, seuil_bp=np.nan, cote=o_, n=len(gg), temps_ecoule_median_min=np.nan))
    pd.DataFrame(stab).to_csv(R21 / 'PHASE21D_TEMPORAL_STABILITY.csv', index=False)

    reg = []
    for (s, h), gg in T.groupby(['seuil_bp', 'horizon']):
        ev = gg[gg.statut == 'EVALUE']
        if not len(ev): reg.append(dict(seuil_bp=s, horizon=h, q_min=np.nan, qualification='INSUFFICIENT_TICK_COVERAGE')); continue
        sig = ev[ev.q_value_BH < 0.05]
        reg.append(dict(seuil_bp=s, horizon=h, q_min=float(ev.q_value_BH.min()),
                        qualification=('EFFET_SIGNIFICATIF ' + ';'.join(sig.mesure) if len(sig) else 'AUCUN_EFFET_SIGNIFICATIF - expansion bidirectionnelle')))
    pd.DataFrame(reg).to_csv(R21 / 'PHASE21D_ANOMALY_REGISTRY.csv', index=False)
    (R21 / 'PHASE21D_CLUSTERED_UNCERTAINTY.md').write_text(
        '# PHASE 21-D — INCERTITUDE PAR GRAPPES\n\nBootstrap par grappes de semaines ISO (10 000 replications, graine 2115), '
        'unites = journees evenementielles (un premier passage par seuil et par journee). p percentile bilaterale, '
        'BH q=0,05 sur la famille preenregistree (3 seuils x 4 horizons x 3 mesures = 36 tests). '
        'Minima 50 journees / 20 semaines ISO sinon NON_EVALUABLE_INFERENTIAL. Aucune permutation de ticks.\n')
    stats = dict(jours=int(day.jour.nunique()), ordre=day.ordre_extremes_finaux.value_counts().to_dict(),
                 passages={str(s): int((atteints.seuil_bp == s).sum()) for s in SEUILS},
                 declencheurs={str(s): atteints[atteints.seuil_bp == s].cote_declencheur.value_counts().to_dict() for s in SEUILS},
                 n_tests=int(len(T)), n_sig=int((T.q_value_BH < .05).sum()))
    (R21 / '_phase21d_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str))


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
