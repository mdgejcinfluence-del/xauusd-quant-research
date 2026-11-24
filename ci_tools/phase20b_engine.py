#!/usr/bin/env python3
"""PHASE 20-B - Confluence H4 x M1 (EXPLORATORY_POST_HOC).
lot: chemins futurs des 543 evenements d'evaluation M1 (entree premier tick apres
t_decision; sorties premier tick >= entree+H pour H=4/8/12/16; extremes de
liquidation et leurs horodatages par horizon).
analyse: alignement causal du regime H4 (derniere barre complete avant decision,
seuils roulants 250 barres de la Phase 20-A reproduits), reconciliation 19-C,
comparaisons par regime, bootstrap par grappe. Aucun modele. Holdout jamais accede."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R12 = ROOT / 'reports/meta_alpha/phase12'
R17 = ROOT / 'reports/meta_alpha/phase17'
R19 = ROOT / 'reports/meta_alpha/phase19'
R20 = ROOT / 'reports/meta_alpha/phase20'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
M0_M1 = 0.7591463414634146
HORIZONS = (4, 8, 12, 16)

def population():
    F = pd.read_csv(R12 / 'PHASE12B_FEATURES.csv')
    P = json.loads((R12 / 'PHASE12C1_MODEL_PARAMETERS.json').read_text())
    d = F[(F.famille == 'F10-01') & (F.ensemble == 'EVALUATION') &
          (F.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1']))].copy()
    z = np.full(len(d), float(P['intercept']))
    for var, beta in P['coefficients'].items():
        if var.startswith('SESSION_REINTEGRATION='):
            z = z + beta * (d.SESSION_REINTEGRATION == var.split('=', 1)[1]).astype(float).values
        else:
            z = z + beta * d[var].astype(float).values
    d['p_M1'] = 1 / (1 + np.exp(-np.clip(z, -35, 35)))
    P11 = pd.read_csv(ROOT / 'reports/meta_alpha/phase11/PHASE11C_EVENT_PATHS.csv', usecols=['event_id', 'direction'])
    d = d.merge(P11, on='event_id', validate='one_to_one')
    d['t_decision'] = pd.to_datetime(d.t_reintegration)
    d['passe_filtre'] = d.p_M1 > M0_M1
    return d[['event_id', 'grappe_id', 'direction', 't_decision', 'p_M1', 'passe_filtre']]

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
    batch = os.environ['P20B_BATCH']
    E = population()
    inv = json.loads((ROOT / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())['partitions']
    ks = json.loads((ROOT / 'reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {n: i['batch'] for n, i in ks['uploaded'].items()}
    parts = [p for p in inv if p['timestamp_max_footer'] and
             pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None) <= IS_END
             and batchof.get(p['name']) == batch]
    localdir = telecharger_batch(batch)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute('SET threads=2')
    spans = [(pd.Timestamp(p['timestamp_min_footer'].replace('Z', '+00:00')).tz_localize(None),
              pd.Timestamp(p['timestamp_max_footer'].replace('Z', '+00:00')).tz_localize(None), p['name']) for p in parts]
    E = E[E.t_decision.map(lambda t: any(a <= t <= b for a, b, _ in spans))].copy()
    print('P20B lot', batch, len(parts), 'partitions,', len(E), 'evenements', flush=True)
    rows = []
    for r in E.itertuples():
        liq = 'bid' if r.direction == 1 else 'ask'
        fin = r.t_decision + pd.Timedelta(days=4)
        frames = []
        for a, b, name in spans:
            if b < r.t_decision or a > fin: continue
            local = localdir / name
            if not local.exists(): continue
            q = f"""SELECT timestamp_utc AS ts, bid, ask, {liq} AS liq FROM read_parquet('{local}')
                    WHERE timestamp_utc > '{r.t_decision}' AND timestamp_utc <= '{fin}' ORDER BY timestamp_utc"""
            frames.append(con.execute(q).df())
        if not frames: continue
        w = pd.concat(frames); w['ts'] = pd.to_datetime(w.ts, format='mixed').dt.tz_localize(None)
        w = w.sort_values('ts').drop_duplicates('ts').reset_index(drop=True)
        if not len(w): continue
        t0 = w.iloc[0]; entree = float(t0.ask if r.direction == 1 else t0.bid); te = t0.ts
        rec = {'event_id': r.event_id, 'source_batch': batch, 'ts_entree': str(te), 'prix_entree': entree}
        fav = r.direction * (w.liq - entree)
        for H in HORIZONS:
            cible = te + pd.Timedelta(hours=H)
            apres = w[w.ts >= cible]
            rec[f'sortie_dispo_H{H}'] = int(len(apres) > 0)
            if not len(apres): continue
            s = apres.iloc[0]; seg = w[w.ts <= s.ts]; f = fav.loc[seg.index]
            rec[f'ts_sortie_H{H}'] = str(s.ts); rec[f'prix_sortie_H{H}'] = float(s.liq)
            rec[f'delai_sortie_s_H{H}'] = float((s.ts - cible).total_seconds())
            imax, imin = f.idxmax(), f.idxmin()
            rec[f'MFE_H{H}'] = float(f.max()); rec[f'MAE_H{H}'] = float(f.min())
            rec[f't_MFE_min_H{H}'] = float((w.ts.loc[imax] - te).total_seconds() / 60)
            rec[f't_MAE_min_H{H}'] = float((w.ts.loc[imin] - te).total_seconds() / 60)
        rows.append(rec)
    R20.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(R20 / f'P20B_PATHS_{batch}.csv', index=False)
    print('P20B lot termine', batch, len(rows), flush=True)

def remplir(direction, pe, ps, s):
    if direction == 1: a, b = pe * (1 + s / 10000), ps * (1 - s / 10000)
    else: a, b = pe * (1 - s / 10000), ps * (1 + s / 10000)
    return float(direction * np.log(b / a) * 10000)

def regimes_h4():
    """Reproduction exacte des seuils roulants 20-A sur le barset commite."""
    b = pd.read_parquet(R20 / 'PHASE20A_H4_BARSET.parquet')
    rng = b.RANGE_BP.values; q10 = np.full(len(b), np.nan); q90 = np.full(len(b), np.nan)
    for i in range(250, len(b)):
        fen = rng[i - 250:i]
        if np.isfinite(fen).all(): q10[i] = np.quantile(fen, .10); q90[i] = np.quantile(fen, .90)
    b['Q10_roulant'] = q10; b['Q90_roulant'] = q90
    b['regime'] = np.where(rng <= q10, 'COMPRESSION', np.where(rng >= q90, 'EXPANSION', 'NORMAL'))
    b.loc[~np.isfinite(q10), 'regime'] = 'INDETERMINE_CHAUFFE'
    b['fin_barre'] = b.bar_start + pd.Timedelta(hours=4)
    return b

def mode_analyse():
    E = population()
    H = regimes_h4()
    bars_ok = H[H.complete].sort_values('bar_start')
    P = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R20 / 'P20B_PATHS_*.csv'))) if pathlib.Path(f).stat().st_size > 50])
    doublons = int(P.event_id.duplicated().sum()); P = P.drop_duplicates('event_id')
    j = E.merge(P, on='event_id', how='left')
    # alignement causal: derniere barre H4 complete avec fin_barre <= t_decision
    fins = bars_ok.fin_barre.values; regimes = bars_ok.regime.values; debuts = bars_ok.bar_start.values
    al = []
    for r in j.itertuples():
        k = np.searchsorted(fins, np.datetime64(r.t_decision), side='right') - 1
        if k < 0: al.append((r.event_id, None, 'H4_STATE_UNAVAILABLE')); continue
        rg = regimes[k]
        al.append((r.event_id, str(debuts[k]), 'H4_STATE_UNAVAILABLE' if rg == 'INDETERMINE_CHAUFFE' else rg))
    A = pd.DataFrame(al, columns=['event_id', 'barre_h4_bar_start', 'etat_h4'])
    j = j.merge(A, on='event_id')
    j[['event_id', 'grappe_id', 't_decision', 'p_M1', 'passe_filtre', 'barre_h4_bar_start', 'etat_h4']]\
        .to_parquet(R20 / 'PHASE20B_H4_STATE_ALIGNMENT.parquet', index=False)
    # resultats par horizon et scenario
    lignes_cout = []; paths = []
    for Hh in HORIZONS:
        d = j[j[f'sortie_dispo_H{Hh}'] == 1].copy()
        for scen, s in [('S0', 0.0), ('S1', 0.5), ('S2', 1.0)]:
            pe = d.prix_entree.values.astype(float); ps = d[f'prix_sortie_H{Hh}'].values.astype(float)
            dirv = d.direction.values.astype(float)
            a = np.where(dirv == 1, pe * (1 + s / 10000), pe * (1 - s / 10000))
            bb = np.where(dirv == 1, ps * (1 - s / 10000), ps * (1 + s / 10000))
            d[f'PL_{scen}'] = dirv * np.log(bb / a) * 10000
        paths.append(d[['event_id', 'grappe_id', 'direction', 'passe_filtre', 'etat_h4', 't_decision', 'ts_entree', 'prix_entree'] +
                        [f'{c}_H{Hh}' for c in ['ts_sortie', 'prix_sortie', 'delai_sortie_s', 'MFE', 'MAE', 't_MFE_min', 't_MAE_min']] +
                        ['PL_S0', 'PL_S1', 'PL_S2']].assign(horizon=Hh))
    pd.concat(paths).to_parquet(R20 / 'PHASE20B_EVENT_FORWARD_PATHS.parquet', index=False)
    # reconciliation 19-C (H8/H16, PL_S2, population principale)
    rec19 = {}
    for Hh in (8, 16):
        ref = pd.read_parquet(R19 / f'PHASE19C_H{Hh}_EVENT_RESULTS.parquet').set_index('event_id')
        d = [p for p in paths if p.horizon.iloc[0] == Hh][0]
        d = d[d.passe_filtre].set_index('event_id')
        communs = d.index.intersection(ref.index)
        rec19[f'H{Hh}'] = dict(communs=int(len(communs)),
                               ecart_prix_entree_max=float((d.loc[communs, 'prix_entree'] - ref.loc[communs, 'prix_entree_calcule']).abs().max()),
                               ecart_PL_S2_max=float((d.loc[communs, 'PL_S2'] - ref.loc[communs, 'PL_S2']).abs().max()))
    # comparaisons par regime (population principale)
    rng = np.random.default_rng(2009); lignes = []; tests = []
    PP = pd.concat(paths)
    for Hh in HORIZONS:
        d = PP[(PP.horizon == Hh) & (PP.passe_filtre)]
        for etat, g in d.groupby('etat_h4'):
            lignes.append(dict(population='PRINCIPALE_443', horizon=Hh, regime=etat, n=int(len(g)),
                               n_grappes=int(g.grappe_id.nunique()), PL_S2_moyen=float(g.PL_S2.mean()), PL_S2_mediane=float(g.PL_S2.median()),
                               part_positifs=float((g.PL_S2 > 0).mean()), MFE_moyen=float(g[f'MFE_H{Hh}'].mean()), MAE_moyen=float(g[f'MAE_H{Hh}'].mean()),
                               ecart_type=float(g.PL_S2.std()), perte_max=float(g.PL_S2.min())))
        for scen in ['S0', 'S1', 'S2']:
            pass
        norm = d[d.etat_h4 == 'NORMAL']
        for etat in ['EXPANSION', 'COMPRESSION']:
            g = d[d.etat_h4 == etat]
            if len(g) < 5 or len(norm) < 5: continue
            # bootstrap par grappe de la difference des moyennes PL_S2
            gg = g.groupby('grappe_id').PL_S2.mean().values; nn = norm.groupby('grappe_id').PL_S2.mean().values
            boots = np.array([rng.choice(gg, len(gg), replace=True).mean() - rng.choice(nn, len(nn), replace=True).mean() for _ in range(2000)])
            obs = float(g.PL_S2.mean() - norm.PL_S2.mean())
            p = float(min(1.0, 2 * min((boots <= 0).mean(), (boots >= 0).mean())))
            sem_etat = int(pd.to_datetime(g.t_decision).dt.strftime('%G-W%V').nunique())
            sem_norm = int(pd.to_datetime(norm.t_decision).dt.strftime('%G-W%V').nunique())
            statut = 'EVALUE' if (len(g) >= 50 and sem_etat >= 20) else 'NON_EVALUABLE_INFERENTIAL'
            tests.append(dict(comparaison=f'{etat} vs NORMAL', horizon=Hh, mesure='PL_S2 moyen (difference)',
                              n_etat=int(len(g)), n_normal=int(len(norm)), semaines_etat=sem_etat, semaines_normal=sem_norm,
                              effet=float(obs), p_value=p, statut=statut,
                              ic95=[float(np.quantile(boots, .025)), float(np.quantile(boots, .975))]))
            lignes.append(dict(population='COMPARAISON', horizon=Hh, regime=f'{etat} vs NORMAL', n=int(len(g)),
                               PL_S2_moyen=float(obs)))
    pd.DataFrame(lignes).to_csv(R20 / 'PHASE20B_REGIME_COMPARISON.csv', index=False)
    # scenarios de cout par regime/horizon
    couts = []
    for Hh in HORIZONS:
        d = PP[(PP.horizon == Hh) & (PP.passe_filtre)]
        for etat, g in d.groupby('etat_h4'):
            for scen in ['S0', 'S1', 'S2']:
                couts.append(dict(horizon=Hh, regime=etat, scenario=scen, n=int(len(g)), PL_moyen=float(g[f'PL_{scen}'].mean()),
                                  PL_mediane=float(g[f'PL_{scen}'].median()), part_positifs=float((g[f'PL_{scen}'] > 0).mean())))
    pd.DataFrame(couts).to_csv(R20 / 'PHASE20B_COST_SCENARIOS.csv', index=False)
    # population secondaire descriptive (543, amplitude uniquement)
    sec = []
    for Hh in HORIZONS:
        d = PP[PP.horizon == Hh]
        for etat, g in d.groupby('etat_h4'):
            sec.append(dict(population='SECONDAIRE_543 (descriptif amplitude)', horizon=Hh, regime=etat, n=int(len(g)),
                            MFE_moyen=float(g[f'MFE_H{Hh}'].mean()), MAE_moyen=float(g[f'MAE_H{Hh}'].mean())))
    pd.DataFrame(sec).to_csv(R20 / 'PHASE20B_SECONDARY_DESCRIPTIVE.csv', index=False)
    # BH sur les tests primaires
    T = pd.DataFrame(tests)
    if len(T):
        p = T.p_value.values; ordre = np.argsort(p); q = np.empty(len(p)); prev = 1.0
        for i, idx in enumerate(ordre[::-1]): prev = min(prev, p[idx] * len(p) / (len(p) - i)); q[idx] = prev
        T['q_value_BH'] = q
    T.to_csv(R20 / 'PHASE20B_PRIMARY_TESTS.csv', index=False)
    stats = dict(reconciliation_19C=rec19, doublons_lots=doublons, effectifs_regimes={
        e: int((j[j.passe_filtre].etat_h4 == e).sum()) for e in ['EXPANSION', 'NORMAL', 'COMPRESSION', 'H4_STATE_UNAVAILABLE']},
        n_principale=int(j.passe_filtre.sum()), n_secondaire=int(len(j)))
    (R20 / '_phase20b_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str), flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
