#!/usr/bin/env python3
"""PHASE 24-B - Barset M15 IS + evenements impulsion/repli/reintegration M15.
EXPLORATORY_POST_HOC, aucun entrainement, aucun P&L. Definitions figees seq392.
lot: barres M15 [t,t+15) Mid depuis ticks Bid/Ask du lot (borne par journee).
analyse: catalogue d'evenements, permissions (Directeurs 24-A inchanges + Horloge),
balance des classes et faisabilite (criteres 24-A). Holdout interdit."""
import io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R = ROOT / 'reports/meta_alpha'
R24 = R / 'phase24'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
NS = 10**9


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


def mode_lot():
    import duckdb
    batch = os.environ['P23_BATCH']
    inv = json.loads((R / 'INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((R / 'kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    fichiers = [str(localdir / p['name']) for p in parts if (localdir / p['name']).exists()]
    con = duckdb.connect(); con.execute("SET memory_limit='6GB'"); con.execute('SET threads=3')
    lst = '[' + ','.join(f"'{f}'" for f in fichiers) + ']'
    jours = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                            WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    toutes = []
    for jour in pd.to_datetime(jours).strftime('%Y-%m-%d'):
        a = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                            WHERE timestamp_utc >= '{jour}' AND timestamp_utc < DATE '{jour}' + INTERVAL 1 DAY
                            ORDER BY timestamp_utc""").fetchnumpy()
        if len(a['ts']) < 100: continue
        tt = a['ts'].astype('datetime64[ns]'); mid = (a['bid'].astype(float) + a['ask'].astype(float)) / 2
        spr = 10000 * np.log(a['ask'].astype(float) / a['bid'].astype(float))
        debut = np.datetime64(jour, 'ns'); idx = ((tt - debut) // np.timedelta64(15, 'm')).astype(int)
        for k in np.unique(idx):
            m = idx == k
            t_m, mid_m = tt[m], mid[m]
            gaps = np.diff(t_m.astype('int64')) / NS if len(t_m) > 1 else np.array([0.0])
            toutes.append(dict(bar_start=debut + np.timedelta64(15 * int(k), 'm'), open=float(mid_m[0]),
                               high=float(mid_m.max()), low=float(mid_m.min()), close=float(mid_m[-1]),
                               n_quotes=int(m.sum()), first_ts=t_m[0], last_ts=t_m[-1],
                               spread_median_bp=float(np.median(spr[m])),
                               max_gap_s=float(gaps.max()) if len(gaps) else 0.0))
        print('jour', jour, flush=True)
    B = pd.DataFrame(toutes)
    B['complete'] = (B.n_quotes >= 10) & (B.max_gap_s < 600) & ((B.last_ts - B.first_ts).dt.total_seconds() >= 600)
    R24.mkdir(parents=True, exist_ok=True)
    B.to_parquet(R24 / f'P24B_M15_{batch}.parquet', index=False)
    print('lot termine', batch, len(B), 'barres', flush=True)


def mode_analyse():
    import glob as _g
    B = pd.concat([pd.read_parquet(f) for f in _g.glob(str(R24 / 'P24B_M15_*.parquet'))])
    B = B.drop_duplicates('bar_start').sort_values('bar_start').reset_index(drop=True)
    B['BODY_BP'] = 10000 * np.log(B.close / B.open)
    B.to_parquet(R24 / 'PHASE24B_M15_BARSET.parquet', index=False)
    absb = B.BODY_BP.abs().values
    q90 = np.full(len(B), np.nan)
    for i in range(250, len(B)):
        fen = absb[i - 250:i]
        if np.isfinite(fen).all(): q90[i] = np.quantile(fen, .90)
    B['Q90_prev250'] = q90
    fermees = B[B.complete].reset_index(drop=True)
    evenements = []
    cl = fermees.close.values; hi = fermees.high.values; lo = fermees.low.values
    op = fermees.open.values; starts = fermees.bar_start.values
    absb_c = np.abs(10000 * np.log(cl / op))
    q90c = np.full(len(fermees), np.nan)
    for i in range(250, len(fermees)):
        fen = absb_c[i - 250:i]
        if np.isfinite(fen).all(): q90c[i] = np.quantile(fen, .90)
    for i in range(250, len(fermees)):
        if not np.isfinite(q90c[i]) or absb_c[i] < q90c[i] or absb_c[i] == 0: continue
        d = 1 if (cl[i] - op[i]) > 0 else -1
        t0 = starts[i] + np.timedelta64(15, 'm'); P0 = cl[i]
        fenetre = slice(i + 1, i + 33)
        if i + 32 >= len(fermees):
            statut = 'CENSURE_FENETRE'; reint = -1; res = np.nan; inval = False
            evenements.append(dict(barre_impulsion=str(starts[i]), t0=str(t0), direction=d, P0=float(P0), statut=statut))
            continue
        closes = cl[fenetre]
        # invalidation: cloture au-dela de l'extreme adverse de la barre d'impulsion
        niv_inval = lo[i] if d > 0 else hi[i]
        inval_idx = np.where(closes < niv_inval)[0] if d > 0 else np.where(closes > niv_inval)[0]
        inval = len(inval_idx) > 0
        # reintegration: cloture strictement autre cote de P0 apres cloture confirmant le deplacement
        cote = (closes - P0) * d
        confirme = np.where(cote > 0)[0]
        reint = -1
        if len(confirme):
            apres = np.where(cote[confirme[0]:] < 0)[0]
            if len(apres): reint = confirme[0] + apres[0]
        rec = dict(barre_impulsion=str(starts[i]), t0=str(t0), direction=d, P0=float(P0),
                   body_bp=float(10000 * np.log(cl[i] / op[i])), seuil_q90=float(q90c[i]),
                   invalide=bool(inval), t_invalidation_barres=(int(inval_idx[0] + 1) if inval else np.nan))
        if reint < 0:
            rec.update(statut='NON_REINTEGRE', Y_RESUMPTION=np.nan); evenements.append(rec); continue
        t_reint = starts[i + 1 + reint] + np.timedelta64(15, 'm')
        seg_hi = hi[i + 1:i + 2 + reint]; seg_lo = lo[i + 1:i + 2 + reint]
        extreme = seg_hi.max() if d > 0 else seg_lo.min()
        mfe = float(10000 * np.log(extreme / P0)) * d
        meilleur_clot = (closes[:reint] * d).max() * d if reint > 0 else P0
        meilleur = float(meilleur_clot)
        suite = closes[reint + 1:]
        res = int(((suite - meilleur) * d > 0).any()) if len(suite) else 0
        creux = seg_lo.min() if d > 0 else seg_hi.max()
        profondeur = float(10000 * np.log(extreme / creux)) * d
        rec.update(statut='REINTEGRE', t_reintegration=str(t_reint), Y_RESUMPTION=float(res),
                   MFE_A_TREINT_BP=mfe, ratio_repli=(profondeur / mfe if mfe > 0 else np.nan),
                   duree_extreme_vers_treint_min=float(15 * (reint - int(np.argmax(seg_hi) if d > 0 else np.argmin(seg_lo)))),
                   nb_touches_P0=int(((seg_lo <= P0) if d > 0 else (seg_hi >= P0)).sum()),
                   cens=False)
        evenements.append(rec)
    E = pd.DataFrame(evenements)
    E.to_parquet(R24 / 'PHASE24B_M15_IMPULSE_EVENT_CATALOG.parquet', index=False)
    P = E[E.statut == 'REINTEGRE'].copy()
    P.to_parquet(R24 / 'PHASE24B_M15_PULLBACK_REINTEGRATION_CATALOG.parquet', index=False)
    # grappes: composantes connexes de fenetres [t0, t0+8h) chevauchantes
    P['t0'] = pd.to_datetime(P.t0); P['fin'] = P.t0 + pd.Timedelta(hours=8)
    P = P.sort_values('t0').reset_index(drop=True)
    gid = np.zeros(len(P), dtype=int); cour = 0; fin_max = None
    for k, r in enumerate(P.itertuples()):
        if fin_max is not None and r.t0 > fin_max: cour += 1
        gid[k] = cour; fin_max = r.fin if fin_max is None else max(fin_max, r.fin)
    P['grappe_id'] = ['GR-M15-%05d' % g for g in gid]
    P['t_decision'] = pd.to_datetime(P.t_reintegration)
    P['semaine_iso'] = P.t_decision.dt.strftime('%G-W%V')
    P['split'] = np.where(P.t0.dt.year <= 2015, 'APPRENTISSAGE', np.where(P.t0.dt.year <= 2017, 'CALIBRATION', 'EVALUATION'))
    # permissions: panel 24-A recalcule (directeurs)
    b4 = pd.read_parquet(R / 'phase20/PHASE20A_H4_BARSET.parquet').sort_values('bar_start')
    rng4 = b4.RANGE_BP.values; q = np.full(len(b4), np.nan)
    for i in range(250, len(b4)):
        fen = rng4[i - 250:i]
        if np.isfinite(fen).all(): q[i] = np.quantile(fen, .90)
    b4['regime'] = np.where(rng4 >= q, 'EXPANSION', 'NON_EXPANSION'); b4.loc[~np.isfinite(q), 'regime'] = 'INDETERMINE_CHAUFFE'
    b4['fin_barre'] = b4.bar_start + pd.Timedelta(hours=4)
    bok = b4[b4.complete]; fins = bok.fin_barre.values; regs = bok.regime.values
    etat = []
    for t in P.t_decision:
        k = np.searchsorted(fins, np.datetime64(t), side='right') - 1
        etat.append('NON_VALIDABLE' if k < 0 or regs[k] == 'INDETERMINE_CHAUFFE' else regs[k])
    P['etat_h4'] = etat
    dj = pd.read_parquet(R / 'phase21/PHASE21A_D1_BARSET.parquet')
    dmap = dict(zip(dj.jour.astype(str), dj.regime)); js = np.array(sorted(dmap.keys()))
    etat1 = []
    for t in P.t_decision:
        k = np.searchsorted(js, t.strftime('%Y-%m-%d'), side='left') - 1
        etat1.append('NON_VALIDABLE' if k < 0 or dmap[js[k]] == 'INDETERMINE_CHAUFFE' else dmap[js[k]])
    P['etat_d1'] = etat1
    P['horloge_ok'] = (P.t_decision.dt.hour >= 8) & (P.t_decision.dt.hour < 16)
    P['perm_TIME_ONLY'] = P.horloge_ok
    P['perm_H4_TIME'] = (P.etat_h4 == 'EXPANSION') & P.horloge_ok
    P['perm_D1_TIME'] = (P.etat_d1 == 'D1_EXPANSION') & P.horloge_ok
    P.to_parquet(R24 / 'PHASE24B_M15_GATE_PERMISSION_PANEL.parquet', index=False)
    rows, bal = [], []
    total_imp = len(E); non_reint = int((E.statut == 'NON_REINTEGRE').sum()); cens = int((E.statut == 'CENSURE_FENETRE').sum())
    for cfg in ['TIME_ONLY', 'H4_TIME', 'D1_TIME']:
        g = P[P[f'perm_{cfg}']]
        for sp in ['TOUS', 'APPRENTISSAGE', 'CALIBRATION', 'EVALUATION']:
            gg = g if sp == 'TOUS' else g[g.split == sp]
            rows.append(dict(variante='M15_' + cfg, split=sp, n=len(gg), grappes=int(gg.grappe_id.nunique()),
                             semaines_iso=int(gg.semaine_iso.nunique()), Y1=int((gg.Y_RESUMPTION == 1).sum()),
                             Y0=int((gg.Y_RESUMPTION == 0).sum())))
        tr = g[g.split == 'APPRENTISSAGE']
        mn = int(min((tr.Y_RESUMPTION == 1).sum(), (tr.Y_RESUMPTION == 0).sum()))
        ev = g[g.split == 'EVALUATION']
        mnev = int(min((ev.Y_RESUMPTION == 1).sum(), (ev.Y_RESUMPTION == 0).sum()))
        bal.append(dict(variante='M15_' + cfg, n_total=len(g), train_minoritaire=mn, parametres=5,
                        train_min_par_param=round(mn / 5, 1), eval_n=len(ev), eval_minoritaire=mnev,
                        faisable=bool(mn >= 100 and len(ev) >= 100 and mnev >= 50)))
    pd.DataFrame(rows).to_csv(R24 / 'PHASE24B_M15_COHORT_COUNTS.csv', index=False)
    pd.DataFrame(bal).to_csv(R24 / 'PHASE24B_M15_CLASS_BALANCE.csv', index=False)
    stats = dict(barres_M15=int(len(B)), impulsions=int(total_imp), reintegres=int(len(P)),
                 non_reintegres=non_reint, censures=cens,
                 balance={r['variante']: r for r in bal})
    (R24 / '_phase24b_stats.json').write_text(json.dumps(stats, indent=1))
    print(stats, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
