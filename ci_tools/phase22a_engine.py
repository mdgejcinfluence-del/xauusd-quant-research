#!/usr/bin/env python3
"""PHASE 22-A - Familles A (Sweep & Reclaim tick) et B (Impulse-Pullback-Resumption H4).
EXPLORATORY_POST_HOC, IS uniquement, holdout jamais accede. Familles separees.
lot: evenements Sweep & Reclaim par lot Kaggle (fenetre 08-16 UTC, buffer spread causal).
analyse: consolidation A + famille B depuis barset H4 certifie 20-A + inference.
Couts 19-B: spread une fois (Bid/Ask reels), slippage S0/S1/S2 en prix, commissions exclues.
Resultats: HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R21 = ROOT / 'reports/meta_alpha/phase21'
R22 = ROOT / 'reports/meta_alpha/phase22'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
GRAINE = 2117
NBOOT = 10000
HORIZONS_A = [('15m', 900), ('30m', 1800), ('1h', 3600), ('4h', 14400), ('EOD', None)]


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
    batch = os.environ['P22_BATCH']
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    cert = pd.read_parquet(R21 / 'PHASE21A_D1_BARSET.parquet')
    cert['jour_s'] = cert.jour.dt.strftime('%Y-%m-%d')
    jours_cert = set(cert.jour_s)
    hl = {r.jour_s: (r.high, r.low) for r in cert.itertuples()}
    ordonnes = sorted(jours_cert)
    precedent = {ordonnes[i]: ordonnes[i - 1] for i in range(1, len(ordonnes))}
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'
    df = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                         WHERE timestamp_utc < '{IS_END}' ORDER BY timestamp_utc""").df()
    ts = pd.to_datetime(df.ts).values.astype('datetime64[ns]')
    bid_all = df.bid.values.astype(float); ask_all = df.ask.values.astype(float); del df
    mid_all = (bid_all + ask_all) / 2.0
    spread_all = logbp(bid_all, ask_all)
    ord_jour = ts.astype('datetime64[D]')
    uniques, debuts = np.unique(ord_jour, return_index=True)
    bornes = list(debuts) + [len(ts)]
    groupes = [(str(u), np.arange(bornes[k], bornes[k + 1])) for k, u in enumerate(uniques) if str(u) in jours_cert]
    print('lot', batch, len(ts), 'ticks,', len(groupes), 'journees', flush=True)
    NS = 10**9
    lvl_rows, ev_rows, post_rows = [], [], []
    eid = 0
    for js, idx in groupes:
        tt = ts[idx].astype('int64'); m = mid_all[idx]; bd = bid_all[idx]; ak = ask_all[idx]; sp = spread_all[idx]
        heures = pd.to_datetime(ts[idx]).hour.values
        nuit = heures < 8
        if not nuit.any(): continue
        onH, onL = m[nuit].max(), m[nuit].min()
        niveaux = [('A1_OVERNIGHT_HIGH', onH, 'HIGH', (onH + onL) / 2, onL),
                   ('A2_OVERNIGHT_LOW', onL, 'LOW', (onH + onL) / 2, onH)]
        if js in precedent and precedent[js] in hl:
            pdH, pdL = hl[precedent[js]]
            niveaux += [('A3_PREVIOUS_DAY_HIGH', pdH, 'HIGH', (pdH + pdL) / 2, pdL),
                        ('A4_PREVIOUS_DAY_LOW', pdL, 'LOW', (pdH + pdL) / 2, pdH)]
        win = (heures >= 8) & (heures < 16)
        if not win.any(): continue
        wi = np.where(win)[0]
        tw, mw, sw = tt[wi], m[wi], sp[wi]
        ser = pd.Series(sw, index=pd.to_datetime(tw))
        buf = ser.rolling('5min').median().fillna(method='bfill').values
        for level_id, niveau, cote, centre, oppose in niveaux:
            seuil_prix = niveau * np.exp(buf / 10000) if cote == 'HIGH' else niveau * np.exp(-buf / 10000)
            franchit = mw > seuil_prix if cote == 'HIGH' else mw < seuil_prix
            deja = bool(franchit[0])
            lvl_rows.append(dict(jour=js, LEVEL_ID=level_id, niveau_prix=niveau, cote=cote,
                                 deja_franchi_debut_fenetre=deja, centre_reference=centre, oppose_reference=oppose))
            if deja: continue
            start = 0; rep = 0
            while rep < 10:
                cand = np.where(franchit[start:])[0]
                if not len(cand): break
                i = start + int(cand[0])
                if cote == 'HIGH':
                    rec = np.where(mw[i:] <= niveau)[0]
                else:
                    rec = np.where(mw[i:] >= niveau)[0]
                seg_ext = mw[i:(i + int(rec[0]) if len(rec) else len(mw))]
                extreme = seg_ext.max() if cote == 'HIGH' else seg_ext.min()
                profondeur = float(abs(logbp(np.array([niveau]), np.array([extreme]))[0]))
                eid += 1
                if not len(rec):
                    ev_rows.append(dict(SWEEP_EVENT_ID=eid, jour=js, LEVEL_ID=level_id, cote=cote,
                                        statut='BREAKOUT_WITHOUT_RECLAIM', population='PRIMAIRE' if rep == 0 else 'SECONDAIRE',
                                        ts_franchissement=pd.Timestamp(tw[i]), profondeur_max_bp=profondeur))
                    break
                j = i + int(rec[0]); rep += 1
                direction = -1 if cote == 'HIGH' else 1
                entree = bd[j] if direction < 0 else ak[j]
                ev_rows.append(dict(SWEEP_EVENT_ID=eid, jour=js, LEVEL_ID=level_id, cote=cote,
                                    statut='SWEEP_RECLAIM_CONFIRME', population='PRIMAIRE' if rep == 1 else 'SECONDAIRE',
                                    ts_franchissement=pd.Timestamp(tw[i]), ts_reintegration=pd.Timestamp(tw[j]),
                                    profondeur_max_bp=profondeur, direction_candidate=int(direction),
                                    prix_entree=float(entree), extreme_balayee=float(extreme),
                                    delai_franchissement_reintegration_s=float((tw[j] - tw[i]) / NS)))
                # chemins futurs sur la journee entiere (indices journee complete)
                gj = int(wi[j])
                for hnom, hsec in HORIZONS_A:
                    fin_t = tt[-1] if hsec is None else min(tt[gj] + hsec * NS, tt[-1])
                    e = int(np.searchsorted(tt, fin_t, side='right') - 1)
                    if e <= gj:
                        post_rows.append(dict(SWEEP_EVENT_ID=eid, jour=js, LEVEL_ID=level_id, horizon=hnom, censure=True)); continue
                    seg = m[gj:e + 1]
                    if direction > 0:
                        mfe = float(logbp(np.array([m[gj]]), np.array([seg.max()]))[0]); mae = float(logbp(np.array([seg.min()]), np.array([m[gj]]))[0])
                        sortie = bd[e]
                    else:
                        mfe = float(logbp(np.array([seg.min()]), np.array([m[gj]]))[0]); mae = float(logbp(np.array([m[gj]]), np.array([seg.max()]))[0])
                        sortie = ak[e]
                    row = dict(SWEEP_EVENT_ID=eid, jour=js, LEVEL_ID=level_id, horizon=hnom, censure=False,
                               direction_candidate=int(direction), prix_entree=float(entree), prix_sortie=float(sortie),
                               MFE_BP=mfe, MAE_BP=mae, TERMINAL_MID_BP=float(direction * logbp(np.array([m[gj]]), np.array([m[e]]))[0]),
                               extension_au_dela_extreme_bp=float(logbp(np.array([extreme]), np.array([seg.max() if direction < 0 else seg.min()]))[0]) if
                               ((direction < 0 and seg.max() > extreme) or (direction > 0 and seg.min() < extreme)) else 0.0,
                               touche_centre=bool(((seg <= centre) if direction < 0 else (seg >= centre)).any()),
                               touche_oppose=bool(((seg <= oppose) if direction < 0 else (seg >= oppose)).any()))
                    for s_nom, s_bp in [('S0', 0.0), ('S1', 0.5), ('S2', 1.0)]:
                        if direction > 0:
                            net = logbp(np.array([entree * (1 + s_bp / 10000)]), np.array([sortie * (1 - s_bp / 10000)]))[0]
                        else:
                            net = logbp(np.array([sortie * (1 + s_bp / 10000)]), np.array([entree * (1 - s_bp / 10000)]))[0]
                        row[f'NET_{s_nom}_BP'] = float(net)
                    post_rows.append(row)
                start = j + 1
    R22.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(lvl_rows).to_parquet(R22 / f'P22A_LEVEL_{batch}.parquet', index=False)
    pd.DataFrame(ev_rows).to_parquet(R22 / f'P22A_EVENT_{batch}.parquet', index=False)
    pd.DataFrame(post_rows).to_parquet(R22 / f'P22A_POST_{batch}.parquet', index=False)
    print('lot termine', batch, len(lvl_rows), 'niveaux-jours', len(ev_rows), 'evenements', flush=True)


def boot0(a, rng):
    """Bootstrap grappes semaines ISO, H0 moyenne=0."""
    ev = len(a) >= 50 and a.semaine_iso.nunique() >= 20
    if not ev: return np.nan, np.nan, (np.nan, np.nan), False
    w = a.semaine_iso.unique(); g = {x: v.NET_S2_BP.values for x, v in a.groupby('semaine_iso')}
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([g[x] for x in rng.choice(w, len(w), replace=True)]).mean()
    return a.NET_S2_BP.mean(), 2 * min((boots <= 0).mean(), (boots >= 0).mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def boot_diff(a, b, mesure, rng):
    ev = len(a) >= 50 and len(b) >= 50 and a.semaine_iso.nunique() >= 20 and b.semaine_iso.nunique() >= 20
    if not ev: return np.nan, np.nan, (np.nan, np.nan), False
    wa, wb = a.semaine_iso.unique(), b.semaine_iso.unique()
    ga = {x: v[mesure].values for x, v in a.groupby('semaine_iso')}
    gb = {x: v[mesure].values for x, v in b.groupby('semaine_iso')}
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([ga[x] for x in rng.choice(wa, len(wa), replace=True)]).mean() - \
                   np.concatenate([gb[x] for x in rng.choice(wb, len(wb), replace=True)]).mean()
    return a[mesure].mean() - b[mesure].mean(), 2 * min((boots <= 0).mean(), (boots >= 0).mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def famille_b(tests, rng):
    R20 = ROOT / 'reports/meta_alpha/phase20'
    b = pd.read_parquet(R20 / 'PHASE20A_H4_BARSET.parquet')
    b = b[b.complete].sort_values('bar_start').reset_index(drop=True)
    b['ABS_BODY'] = b.BODY_BP.abs()
    b['Q90'] = b.ABS_BODY.rolling(250).quantile(.9).shift(1)
    b['impulsion'] = (b.ABS_BODY > b.Q90) & (b.BODY_BP != 0)
    imp_rows, pb_rows, res_rows, fwd_rows = [], [], [], []
    actif = None
    for i, r in enumerate(b.itertuples()):
        if r.impulsion:
            imp_rows.append(dict(IMPULSE_EVENT_ID=len(imp_rows) + 1, bar_start=r.bar_start, direction=int(np.sign(r.BODY_BP)),
                                 ABS_BODY_BP=r.ABS_BODY, Q90=r.Q90, episode_actif=bool(actif is not None)))
        if actif is None:
            if r.impulsion:
                actif = dict(debut=i, direction=int(np.sign(r.BODY_BP)), open_imp=r.open, extreme=r.high if r.BODY_BP > 0 else r.low,
                             abs_body=r.ABS_BODY, pullback=None, pullback_i=None, statut=None)
            continue
        k = i - actif['debut']
        if k == 0: continue
        d = actif['direction']
        if k <= 8:
            # invalidation: retour a l'open de l'impulsion
            if (d > 0 and r.low <= actif['open_imp']) or (d < 0 and r.high >= actif['open_imp']):
                actif['statut'] = 'IMPULSE_FULL_RETRACE_INVALIDATION'
            elif actif['pullback'] is None:
                if (d > 0 and r.BODY_BP < 0) or (d < 0 and r.BODY_BP > 0):
                    actif['pullback'] = i; actif['pullback_i'] = k
            else:
                prev = b.iloc[i - 1]
                if (d > 0 and r.close > prev.high) or (d < 0 and r.close < prev.low):
                    actif['statut'] = 'RESUMPTION_CONFIRMED'; actif['reprise_i'] = i
            if actif['statut'] is None and k == 8:
                actif['statut'] = 'NO_RESUMPTION_WITHIN_8_H4' if actif['pullback'] is not None else 'NO_PULLBACK_WITHIN_8_H4'
        if actif['statut'] is not None:
            pb_rows.append(dict(IMPULSE_EPISODE_ID=len(pb_rows) + 1, bar_impulsion=b.bar_start.iloc[actif['debut']],
                                direction=actif['direction'], ABS_BODY_BP=actif['abs_body'], statut=actif['statut'],
                                barres_pullback=(actif['pullback_i'] if actif['pullback'] is not None else np.nan),
                                ratio_retracement=np.nan))
            if actif['statut'] == 'RESUMPTION_CONFIRMED':
                ri = actif['reprise_i']; ei = ri + 1
                if ei < len(b):
                    entree_bar = b.iloc[ei]
                    entree = entree_bar.open_ask if d > 0 else entree_bar.open_bid
                    res_rows.append(dict(IMPULSE_EPISODE_ID=len(pb_rows), bar_reprise=b.bar_start.iloc[ri],
                                         bar_entree=entree_bar.bar_start, direction=d, prix_entree=float(entree),
                                         semaine_iso=entree_bar.semaine_iso))
                    for H in (1, 2, 4, 8):
                        xi = ei + H - 1
                        if xi >= len(b): continue
                        seg = b.iloc[ei:xi + 1]; xb = b.iloc[xi]
                        sortie = xb.close_bid if d > 0 else xb.close_ask
                        row = dict(IMPULSE_EPISODE_ID=len(pb_rows), horizon_barres=H, direction=d,
                                   prix_entree=float(entree), prix_sortie=float(sortie), semaine_iso=entree_bar.semaine_iso,
                                   MFE_BP=float(d * logbp(np.array([entree]), np.array([seg.high.max() if d > 0 else seg.low.min()]))[0]),
                                   MAE_BP=float(-d * logbp(np.array([entree]), np.array([seg.low.min() if d > 0 else seg.high.max()]))[0]))
                        for s_nom, s_bp in [('S0', 0.0), ('S1', 0.5), ('S2', 1.0)]:
                            if d > 0: net = logbp(np.array([entree * (1 + s_bp / 10000)]), np.array([sortie * (1 - s_bp / 10000)]))[0]
                            else: net = logbp(np.array([sortie * (1 + s_bp / 10000)]), np.array([entree * (1 - s_bp / 10000)]))[0]
                            row[f'NET_{s_nom}_BP'] = float(net)
                        fwd_rows.append(row)
            actif = None
    pd.DataFrame(imp_rows).to_parquet(R22 / 'PHASE22A_H4_IMPULSE_CATALOG.parquet', index=False)
    pd.DataFrame(pb_rows).to_parquet(R22 / 'PHASE22A_PULLBACK_EVENTS.parquet', index=False)
    pd.DataFrame(res_rows).to_parquet(R22 / 'PHASE22A_RESUMPTION_EVENTS.parquet', index=False)
    F = pd.DataFrame(fwd_rows); F.to_parquet(R22 / 'PHASE22A_IMPULSE_FORWARD_PATHS.parquet', index=False)
    for H in (2, 4, 8):
        a = F[F.horizon_barres == H]
        eff, p, ci, ev = boot0(a, rng)
        tests.append(dict(famille='B', comparaison=f'reprise confirmee H{H} barres, net S2 vs 0', n=len(a),
                          semaines=a.semaine_iso.nunique() if len(a) else 0, effet=eff, IC95_bas=ci[0], IC95_haut=ci[1],
                          p_value=p, statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
        tests.append(dict(famille='B', comparaison=f'reprise vs sans-reprise H{H} (terminal aligne mid, descriptif)', n=len(a),
                          semaines=a.semaine_iso.nunique() if len(a) else 0, effet=np.nan, IC95_bas=np.nan, IC95_haut=np.nan,
                          p_value=np.nan, statut='NON_EVALUABLE_INFERENTIAL'))
    return F, pd.DataFrame(pb_rows)


def mode_analyse():
    R22.mkdir(parents=True, exist_ok=True)
    lvl = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(R22 / 'P22A_LEVEL_*.parquet')))]).reset_index(drop=True)
    ev = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(R22 / 'P22A_EVENT_*.parquet')))]).reset_index(drop=True)
    post = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(R22 / 'P22A_POST_*.parquet')))]).reset_index(drop=True)
    for df in (lvl, ev, post):
        df['semaine_iso'] = pd.to_datetime(df.jour).dt.strftime('%G-W%V'); df['annee'] = pd.to_datetime(df.jour).dt.year
    lvl.to_parquet(R22 / 'PHASE22A_SWEEP_LEVEL_CATALOG.parquet', index=False)
    ev.to_parquet(R22 / 'PHASE22A_SWEEP_RECLAIM_EVENTS.parquet', index=False)
    prim = ev[(ev.statut == 'SWEEP_RECLAIM_CONFIRME') & (ev.population == 'PRIMAIRE')]
    postp = post.merge(prim[['SWEEP_EVENT_ID']], on='SWEEP_EVENT_ID')
    postp['semaine_iso'] = pd.to_datetime(postp.jour).dt.strftime('%G-W%V')
    postp.to_parquet(R22 / 'PHASE22A_SWEEP_FORWARD_PATHS.parquet', index=False)
    grp = postp[~postp.censure].groupby(['LEVEL_ID', 'horizon']).agg(
        n=('NET_S2_BP', 'count'), net_S2_moyen=('NET_S2_BP', 'mean'), net_S2_median=('NET_S2_BP', 'median'),
        taux_positif=('NET_S2_BP', lambda x: float((x > 0).mean())), MFE_mediane=('MFE_BP', 'median'), MAE_mediane=('MAE_BP', 'median'),
        part_centre=('touche_centre', 'mean'), part_oppose=('touche_oppose', 'mean')).reset_index()
    grp.to_csv(R22 / 'PHASE22A_SWEEP_GROUP_COMPARISON.csv', index=False)

    rng = np.random.default_rng(GRAINE)
    tests = []
    for level_id, gg in postp.groupby('LEVEL_ID'):
        for h in ('1h', '4h', 'EOD'):
            a = gg[(gg.horizon == h) & (~gg.censure)]
            eff, p, ci, evl = boot0(a, rng)
            tests.append(dict(famille='A', comparaison=f'{level_id} {h}, net S2 vs 0', n=len(a),
                              semaines=a.semaine_iso.nunique() if len(a) else 0, effet=eff, IC95_bas=ci[0], IC95_haut=ci[1],
                              p_value=p, statut='EVALUE' if evl else 'NON_EVALUABLE_INFERENTIAL'))
    F, PB = famille_b(tests, rng)
    T = pd.DataFrame(tests)
    q = np.full(len(T), np.nan); idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; o = np.argsort(pv); m_ = len(pv)
        qq = pv[o] * m_ / (np.arange(m_) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[o])] = np.minimum(qq, 1)
    T['q_value_BH'] = q
    T.to_csv(R22 / 'PHASE22A_MULTIPLE_TEST_CORRECTION.csv', index=False)

    fam = []
    for level_id, gg in postp[postp.horizon == 'EOD'].groupby('LEVEL_ID'):
        fam.append(dict(famille='A', groupe=level_id, n=len(gg), net_S0=gg.NET_S0_BP.mean(), net_S1=gg.NET_S1_BP.mean(),
                        net_S2=gg.NET_S2_BP.mean(), net_S2_median=gg.NET_S2_BP.median(), MAE_mediane=gg.MAE_BP.median()))
    for H, gg in F.groupby('horizon_barres'):
        fam.append(dict(famille='B', groupe=f'reprise H{H}', n=len(gg), net_S0=gg.NET_S0_BP.mean(), net_S1=gg.NET_S1_BP.mean(),
                        net_S2=gg.NET_S2_BP.mean(), net_S2_median=gg.NET_S2_BP.median(), MAE_mediane=gg.MAE_BP.median()))
    pd.DataFrame(fam).to_csv(R22 / 'PHASE22A_STRATEGY_FAMILY_COMPARISON.csv', index=False)

    reg = []
    for _, r in T.iterrows():
        qual = 'INSUFFICIENT_EVIDENCE' if r.statut != 'EVALUE' else ('EFFET_SIGNIFICATIF (candidat a qualifier)' if r.q_value_BH < 0.05 else 'NO_ECONOMIC_ASYMMETRY_SUPPORTED')
        reg.append(dict(famille=r.famille, comparaison=r.comparaison, q_value=r.q_value_BH, qualification=qual))
    pd.DataFrame(reg).to_csv(R22 / 'PHASE22A_ANOMALY_REGISTRY.csv', index=False)
    (R22 / 'PHASE22A_COST_SCENARIO_AUDIT.md').write_text(
        '# PHASE 22-A — AUDIT COUTS\n\nComptabilite 19-B: spread integre exactement une fois (achat Ask, vente Bid, '
        'prix reels). Slippage S0/S1/S2 = 0/0,5/1 bp par cote applique en prix; S2 principal; commissions exclues. '
        'Resultats: HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION. Aucune conversion '
        'monetaire (BROKER_SPECIFICATION_UNVERIFIED). References 4,0/4,5 bp: REFERENCE_COST_UNVERIFIED.\n')
    lignes_risque = ['# PHASE 22-A — AUDIT RISQUE ET QUEUES', '']
    for nom, gg, col in [('A EOD', postp[postp.horizon == 'EOD'], 'NET_S2_BP'), ('B H8', F[F.horizon_barres == 8], 'NET_S2_BP')]:
        if len(gg):
            lignes_risque.append(f"- {nom}: n={len(gg)}, MAE mediane {gg.MAE_BP.median():.1f} bp, "
                                 f"net S2 P5 {gg[col].quantile(.05):.1f} bp, pire {gg[col].min():.1f} bp, "
                                 f"part des pertes > 50 bp: {float((gg[col] < -50).mean()):.3f}")
    lignes_risque.append('- Extreme balaye = niveau d invalidation descriptif; aucune politique de stop optimisee.')
    (R22 / 'PHASE22A_RISK_AND_TAIL_AUDIT.md').write_text('\n'.join(lignes_risque))
    lignes_stab = ['# PHASE 22-A — STABILITE TEMPORELLE', '']
    for per, m in [('2010-2015', postp.annee <= 2015), ('2016-2019', postp.annee >= 2016)]:
        gg = postp[m & (postp.horizon == 'EOD')]
        lignes_stab.append(f"- A EOD {per}: n={len(gg)}, net S2 moyen {gg.NET_S2_BP.mean() if len(gg) else float('nan'):.2f} bp")
    for per, m in [('2010-2015', pd.to_datetime(F.semaine_iso.str[:4] + '-01-04').dt.year <= 2015 if len(F) else slice(None)),
                   ('2016-2019', pd.to_datetime(F.semaine_iso.str[:4] + '-01-04').dt.year >= 2016 if len(F) else slice(None))]:
        gg = F[m] if len(F) else F
        g8 = gg[gg.horizon_barres == 8] if len(gg) else gg
        lignes_stab.append(f"- B H8 {per}: n={len(g8)}, net S2 moyen {g8.NET_S2_BP.mean() if len(g8) else float('nan'):.2f} bp")
    lignes_stab.append('- Sous-periodes = diagnostics post-hoc, jamais des validations independantes.')
    (R22 / 'PHASE22A_TEMPORAL_STABILITY.md').write_text('\n'.join(lignes_stab))
    stats = dict(A_evenements_primaires=int(len(prim)), A_par_niveau=prim.LEVEL_ID.value_counts().to_dict(),
                 A_sans_reclaim=int((ev.statut == 'BREAKOUT_WITHOUT_RECLAIM').sum()),
                 B_statuts=PB.statut.value_counts().to_dict() if len(PB) else {},
                 n_tests=int(len(T)), n_sig=int((T.q_value_BH < .05).sum()))
    (R22 / '_phase22a_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str))


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
