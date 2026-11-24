#!/usr/bin/env python3
"""PHASE 23-B - Contexte macro J-1 (etude A) et reactions aux annonces (etude B).
EXPLORATORY_POST_HOC, budget 0 FCFA, holdout interdit, aucun consensus/surprise.
exo: telechargement FRED/ALFRED (libre) des 3 series du registre 23-A + calendriers
     officiels (Fed FOMC, BLS CPI/NFP, BEA PCE) avec journaux de provenance.
lot: fenetres tick autour des annonces et de leurs temoins (memes jour de semaine et
     creneau UTC, sans annonce majeure), premier tick strictement apres publication.
analyse: panel J-1 causal (publication J+1 ouvree), associations par terciles +
     bootstrap semaines ISO; comparaison evenement/temoin; BH par etude."""
import glob, io, json, os, pathlib, re, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R21 = ROOT / 'reports/meta_alpha/phase21'
R23 = ROOT / 'reports/meta_alpha/phase23'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
GRAINE = 2121
NBOOT = 10000
SERIES = ['DTWEXBGS', 'DGS10', 'DFII10']


def logbp(a, b): return 10000 * np.log(b / a)


def fetch(url, timeout=120):
    import requests
    r = requests.get(url, timeout=timeout, headers={'User-Agent': 'metaalpha-research/1.0'})
    print('FETCH', url[:110], r.status_code, len(r.content), flush=True)
    return r


def mode_exo():
    R23.mkdir(parents=True, exist_ok=True)
    lignes = ['# PHASE 23-B — RECONCILIATION DES SOURCES', '']
    frames = []
    for s in SERIES:
        df = None; source = None
        for nom, url in [('ALFRED alfredgraph.csv', f'https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={s}&cosd=2009-06-01&coed=2020-03-01'),
                         ('FRED fredgraph.csv', f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}&cosd=2009-06-01&coed=2020-03-01'),
                         ('DBnomics miroir FRED', f'https://api.db.nomics.world/v22/series/FRED/{s}?observations=1&observation_date_from=2009-06-01')]:
            try:
                r = fetch(url, timeout=45)
                if r.status_code == 200 and len(r.content) > 200:
                    lignes.append(f'- {s} via {nom}: {len(r.content)} octets, en-tete: {r.content[:120]!r}')
                    if nom.startswith('DBnomics'):
                        obs = r.json()['series'][0]['value']
                        per = r.json()['series'][0]['period']
                        d = pd.DataFrame({'date_obs': per, 'valeur': obs})
                    else:
                        d = pd.read_csv(io.BytesIO(r.content))
                    lignes.append(f'  colonnes: {list(d.columns)}; lignes: {len(d)}')
                    if len(d.columns) >= 2:
                        df = d; source = nom; break
            except Exception as e:
                lignes.append(f'- {s} via {nom}: ECHEC {type(e).__name__} {e}')
        if df is None:
            MIROIRS = {
                'DTWEXBGS': ['https://raw.githubusercontent.com/danielmiessler/Substrate/main/Data/US-Common-Metrics/us-metrics-historical.csv'],
                'DGS10': ['https://raw.githubusercontent.com/Apress/Statistical-Quantitative-Methods-in-Finance/main/data/DGS10.csv',
                          'https://raw.githubusercontent.com/upathare1/Advanced-Term-Structures/main/Code/data/DGS10.csv'],
                'DFII10': ['https://raw.githubusercontent.com/ethanteng/finsight/main/src/datasets/DFII10.csv',
                           'https://raw.githubusercontent.com/js5810/TreasuryAuction/main/data/FRED_data/DFII10.csv'],
            }
            candidats = []
            for url in MIROIRS.get(s, []):
                try:
                    r = fetch(url, timeout=45)
                    if r.status_code == 200:
                        d = pd.read_csv(io.BytesIO(r.content))
                        dc = [c for c in d.columns if 'date' in c.lower() or 'DATE' in c]
                        vc = [c for c in d.columns if s in c or c.lower() in ('value', 'valeur', 'close')]
                        if dc and vc:
                            dd = pd.DataFrame({'date_obs': pd.to_datetime(d[dc[0]]), 'valeur': pd.to_numeric(d[vc[0]], errors='coerce')}).dropna()
                            dd = dd[(dd.date_obs >= '2009-06-01') & (dd.date_obs <= '2020-03-01')]
                            lignes.append(f'- {s} miroir {url[:80]}: {len(dd)} obs, {dd.date_obs.min()} -> {dd.date_obs.max()}')
                            if len(dd) > 2000: candidats.append(dd)
                except Exception as e:
                    lignes.append(f'- {s} miroir ECHEC {type(e).__name__}')
            if candidats:
                df = candidats[0]; source = 'miroir GitHub de FRED (vintage courante)'
                if len(candidats) > 1:
                    m = candidats[0].merge(candidats[1], on='date_obs', suffixes=('_a', '_b')).dropna()
                    ecart = float((m.valeur_a - m.valeur_b).abs().max()) if len(m) else float('nan')
                    lignes.append(f'- {s} reconciliation deux miroirs: {len(m)} dates communes, ecart max {ecart}')
                    source += f', reconcilie (ecart max {ecart})'
        if df is None:
            lignes.append(f'- {s}: AUCUNE SOURCE — serie exclue (SOURCE_RECONCILIATION_FAILED partiel)')
            continue
        d = df.copy(); d.columns = ['date_obs', 'valeur'] + list(d.columns[2:])
        d['serie'] = s; d['source'] = source
        frames.append(d[['date_obs', 'valeur', 'serie', 'source']])
    if frames:
        F = pd.concat(frames)
        F.to_parquet(R23 / 'PHASE23B_MACRO_FIRST_VINTAGE_DATA.parquet', index=False)
        lignes.append(f'- Series sauvegardees: {sorted(F.serie.unique())} (vintage: voir source; alfredgraph = vintage ALFRED si obtenu, sinon vintage courante FRED documentee comme limite)')
    # Calendriers officiels
    evenements = []
    # FOMC: pages officielles historiques par annee; dates des communiques monetaryAAAAMMJJ
    for annee in range(2010, 2020):
        try:
            r = fetch(f'https://www.federalreserve.gov/monetarypolicy/fomchistorical{annee}.htm', timeout=60)
            dates = sorted(set(re.findall(r'monetary(20\d{2})(\d{2})(\d{2})a\.htm', r.text)))
            for a, m_, j_ in dates:
                evenements.append(dict(type='FOMC', date=pd.Timestamp(int(a), int(m_), int(j_)), heure_et='14:00',
                                       source=f'federalreserve.gov fomchistorical{annee}'))
        except Exception as e:
            lignes.append(f'- FOMC {annee}: ECHEC {type(e).__name__}')
    lignes.append(f'- FOMC parse (communiques officiels): {sum(1 for e in evenements if e["type"]=="FOMC")} decisions 2010-2019')
    lignes.append('- CPI/PCE/NFP: dates officielles non enumerables de facon verifiable sans cle API (archives BLS/BEA non indexees par date de publication); familles classees INSUFFICIENT_HISTORICAL_COVERAGE plutot que reconstruites.')
    E = pd.DataFrame(evenements).drop_duplicates(['type', 'date']) if evenements else pd.DataFrame(columns=['type', 'date', 'heure_et', 'source'])
    if len(E):
        E['ts_et'] = pd.to_datetime(E.date.dt.strftime('%Y-%m-%d') + ' ' + E.heure_et)
        E['ts_utc'] = E.ts_et.dt.tz_localize('America/New_York', ambiguous='NaT', nonexistent='shift_forward').dt.tz_convert('UTC').dt.tz_localize(None)
        E = E.dropna(subset=['ts_utc']).sort_values('ts_utc')
        # groupe d annonces simultanees (meme jour)
        E['groupe_annonce'] = E.groupby(E.ts_utc.dt.date).ngroup()
        E['n_annonces_jour'] = E.groupby(E.ts_utc.dt.date).type.transform('count')
        # temoins: meme jour de semaine, meme heure UTC, decalage hebdomadaire sans annonce majeure ce jour-la
        jours_annonce = set(E.ts_utc.dt.date)
        temoins = []
        for r in E.itertuples():
            for delta in (-7, -14, 7, 14, -21, 21, -28, 28):
                cand = r.ts_utc + pd.Timedelta(days=delta)
                if cand.date() not in jours_annonce and pd.Timestamp('2010-01-04') <= cand <= pd.Timestamp('2019-12-16'):
                    temoins.append(dict(type=r.type, role='CONTROLE', ts_utc=cand, evenement_ref=r.ts_utc,
                                        jour_semaine=cand.dayofweek, source='temoin meme jour de semaine/creneau, sans annonce'))
                    break
        T = pd.DataFrame(temoins)
        E['role'] = 'EVENEMENT'
        cols = ['type', 'role', 'ts_utc', 'heure_et', 'source']
        E_out = pd.concat([E[cols + ['groupe_annonce', 'n_annonces_jour']], T[cols]], ignore_index=True)
        E_out.to_csv(R23 / 'PHASE23B_OFFICIAL_EVENT_CATALOG.csv', index=False)
        lignes.append(f'- Catalogue: {len(E)} evenements, {len(T)} temoins; types: {E.type.value_counts().to_dict()}')
    else:
        lignes.append('- Catalogue VIDE: etude B non evaluable (SOURCE_RECONCILIATION_FAILED)')
    (R23 / 'PHASE23B_SOURCE_RECONCILIATION.md').write_text('\n'.join(lignes))
    print('\n'.join(lignes), flush=True)


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
        return (a['ts'].astype('datetime64[ns]').astype('int64'), a['bid'].astype(float), a['ask'].astype(float))

    cat = pd.read_csv(R23 / 'PHASE23B_OFFICIAL_EVENT_CATALOG.csv', parse_dates=['ts_utc'])
    jours_dispo = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                                  WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    jours_lot = set(pd.to_datetime(jours_dispo).strftime('%Y-%m-%d'))
    cat = cat[cat.ts_utc.dt.strftime('%Y-%m-%d').isin(jours_lot)]
    rows = []
    for jour, gc in cat.groupby(cat.ts_utc.dt.strftime('%Y-%m-%d')):
        debut = (pd.Timestamp(jour) - pd.Timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        fin = (pd.Timestamp(jour) + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        tt, bid, ask = requete(debut, fin)
        if len(tt) < 100: continue
        mid = (bid + ask) / 2.0; spread = logbp(bid, ask)
        for r in gc.itertuples():
            t0 = pd.Timestamp(r.ts_utc).value
            i_pre = int(np.searchsorted(tt, t0, side='left') - 1)
            i_ent = int(np.searchsorted(tt, t0, side='right'))
            if i_pre < 0 or i_ent >= len(tt): continue
            prix_ref = mid[i_pre]; entree_mid = mid[i_ent]
            pre = (tt >= t0 - 3600 * NS) & (tt < t0)
            row = dict(type=r.type, role=r.role, ts_utc=r.ts_utc, jour=jour,
                       semaine_iso=pd.Timestamp(r.ts_utc).strftime('%G-W%V'), annee=pd.Timestamp(r.ts_utc).year,
                       range_pre_60min_bp=float(logbp(np.array([mid[pre].min()]), np.array([mid[pre].max()]))[0]) if pre.any() else np.nan,
                       spread_pre_median=float(np.median(spread[pre])) if pre.any() else np.nan,
                       prix_reference=float(prix_ref))
            for hnom, hsec in [('15m', 900), ('60m', 3600), ('4h', 14400), ('EOD', None)]:
                fin_t = tt[-1] if hsec is None else min(t0 + hsec * NS, tt[-1])
                e = int(np.searchsorted(tt, fin_t, side='right') - 1)
                if e <= i_ent:
                    row[f'rend_{hnom}'] = np.nan; continue
                seg = mid[i_ent:e + 1]
                row[f'rend_{hnom}'] = float(logbp(np.array([entree_mid]), np.array([mid[e]]))[0])
                row[f'up_{hnom}'] = float(logbp(np.array([entree_mid]), np.array([seg.max()]))[0])
                row[f'down_{hnom}'] = float(logbp(np.array([seg.min()]), np.array([entree_mid]))[0])
                row[f'spread_post_{hnom}'] = float(np.median(spread[i_ent:e + 1]))
                row[f'retour_prix_pre_{hnom}'] = bool(((seg <= prix_ref) & (entree_mid > prix_ref)).any() or ((seg >= prix_ref) & (entree_mid < prix_ref)).any())
            rows.append(row)
        print('jour traite', jour, flush=True)
    R23.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(R23 / f'P23B_WIN_{batch}.parquet', index=False)
    print('lot termine', batch, len(rows), 'fenetres', flush=True)


def boot_diff(a, b, col, rng):
    ev = len(a) >= 50 and len(b) >= 50 and a.semaine_iso.nunique() >= 20 and b.semaine_iso.nunique() >= 20
    if not ev: return np.nan, np.nan, (np.nan, np.nan), False
    wa, wb = a.semaine_iso.unique(), b.semaine_iso.unique()
    ga = {x: v[col].values for x, v in a.groupby('semaine_iso')}
    gb = {x: v[col].values for x, v in b.groupby('semaine_iso')}
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([ga[x] for x in rng.choice(wa, len(wa), replace=True)]).mean() - \
                   np.concatenate([gb[x] for x in rng.choice(wb, len(wb), replace=True)]).mean()
    return a[col].mean() - b[col].mean(), 2 * min((boots <= 0).mean(), (boots >= 0).mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def bh(T):
    q = np.full(len(T), np.nan); idx = T.index[T.statut == 'EVALUE']
    if len(idx):
        pv = T.loc[idx, 'p_value'].values; o = np.argsort(pv); m_ = len(pv)
        qq = pv[o] * m_ / (np.arange(m_) + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
        q[T.index.get_indexer(idx[o])] = np.minimum(qq, 1)
    T['q_value_BH'] = q
    return T


def mode_analyse():
    d1 = pd.read_parquet(R21 / 'PHASE21A_D1_BARSET.parquet')
    fwd = pd.read_parquet(R21 / 'PHASE21A_D1_FORWARD_MFE_MAE.parquet')
    j = d1.merge(fwd, on='jour')
    F = pd.read_parquet(R23 / 'PHASE23B_MACRO_FIRST_VINTAGE_DATA.parquet')
    F['date_obs'] = pd.to_datetime(F.date_obs); F['valeur'] = pd.to_numeric(F.valeur, errors='coerce')
    # disponibilite: observation datee t publiee t+1 jour ouvre (16:15 ET ~ 21:15 UTC); etat causal du jour J:
    # derniere observation dont la publication < J 00:00 UTC. Variation = ecart entre les 2 dernieres connues.
    audit, panel = [], []
    piv = {s: g.set_index('date_obs').valeur.sort_index() for s, g in F.groupby('serie')}
    for s, ser in piv.items():
        ser = ser[~ser.index.duplicated(keep='last')].dropna()
        jours_ouvres = pd.bdate_range(ser.index.min(), ser.index.max() + pd.Timedelta(days=3))
        pub = pd.Series(ser.index, index=ser.index).map(lambda t: jours_ouvres[jours_ouvres > t][0] + pd.Timedelta(hours=21, minutes=15)) if len(ser) else pd.Series(dtype='datetime64[ns]')
        for r in j.itertuples():
            connues = ser[pub.values < r.jour.value] if len(ser) else ser
            if len(connues) >= 2:
                v, vp = connues.iloc[-1], connues.iloc[-2]
                var_bp = float(logbp(np.array([vp]), np.array([v]))[0]) if s == 'DTWEXBGS' else float(v - vp)
                panel.append(dict(jour=r.jour, serie=s, valeur_connue=float(v), variation=float(var_bp),
                                  date_economique=connues.index[-1], unite='bp (log)' if s == 'DTWEXBGS' else 'points de pourcentage'))
            else:
                audit.append(dict(jour=r.jour, serie=s, statut='MACRO_OBSERVATION_NOT_CAUSALLY_AVAILABLE'))
    P = pd.DataFrame(panel)
    P.to_parquet(R23 / 'PHASE23B_XAU_DAILY_CONTEXT_PANEL.parquet', index=False)
    pd.DataFrame(audit).to_csv(R23 / 'PHASE23B_CAUSAL_AVAILABILITY_AUDIT.csv', index=False)

    jj = j.set_index('jour')
    rng = np.random.default_rng(GRAINE)
    testsA, assoc = [], []
    for s, g in P.groupby('serie'):
        g = g.copy(); g['semaine_iso'] = pd.to_datetime(g.jour).dt.strftime('%G-W%V')
        g['tercile'] = pd.qcut(g.variation.rank(method='first'), 3, labels=['bas', 'milieu', 'haut'])
        for H in (1, 2, 5):
            for mesure, col in [('rendement signe', f'TERMINAL_{H}'), ('amplitude UP+DOWN', None)]:
                gg = g.copy()
                gg['y'] = (jj.loc[gg.jour, f'UP_{H}'].values + jj.loc[gg.jour, f'DOWN_{H}'].values) if col is None else jj.loc[gg.jour, col].values
                a = gg[gg.tercile == 'haut']; b_ = gg[gg.tercile == 'bas']
                eff, p, ci, ev = boot_diff(a.rename(columns={'y': 'Y'}), b_.rename(columns={'y': 'Y'}), 'Y', rng)
                testsA.append(dict(etude='A', variable=s, horizon=H, mesure=mesure, comparaison='tercile haut vs bas',
                                   n_haut=len(a), n_bas=len(b_), effet_bp=eff, IC95_bas=ci[0], IC95_haut=ci[1], p_value=p,
                                   statut='EVALUE' if ev else 'NON_EVALUABLE_INFERENTIAL'))
                rho = np.corrcoef(gg.variation.rank(), gg.y.rank())[0, 1]
                assoc.append(dict(variable=s, horizon=H, mesure=mesure, rho_spearman=float(rho), n=len(gg)))
    TA = bh(pd.DataFrame(testsA)); TA.to_csv(R23 / 'PHASE23B_J1_ASSOCIATION_RESULTS.csv', index=False)
    pd.DataFrame(assoc).to_csv(R23 / 'PHASE23B_J1_SPEARMAN_DESCRIPTIF.csv', index=False)

    # Etude B
    W = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(str(R23 / 'P23B_WIN_*.parquet')))]).reset_index(drop=True)
    W.to_parquet(R23 / 'PHASE23B_EVENT_WINDOW_RESULTS.parquet', index=False)
    comp, testsB = [], []
    W['amplitude_60m'] = W.up_60m + W.down_60m; W['amplitude_4h'] = W.up_4h + W.down_4h
    for t_, g in W.groupby('type'):
        ev_ = g[g.role == 'EVENEMENT']; ct = g[g.role == 'CONTROLE']
        for col in ('amplitude_60m', 'amplitude_4h', 'rend_60m', 'rend_4h'):
            comp.append(dict(type=t_, mesure=col, n_evenements=len(ev_), n_temoins=len(ct),
                             evenement_moyenne=ev_[col].mean(), temoin_moyenne=ct[col].mean(),
                             evenement_mediane=ev_[col].median(), temoin_mediane=ct[col].median(),
                             spread_pre_median=ev_.spread_pre_median.median(), spread_post_60m=ev_.spread_post_60m.median()))
        for col in ('amplitude_60m', 'amplitude_4h'):
            eff, p, ci, evl = boot_diff(ev_, ct, col, rng)
            testsB.append(dict(etude='B', variable=t_, horizon=col, mesure='amplitude evenement vs temoin',
                               comparaison='evenement vs controle', n_haut=len(ev_), n_bas=len(ct), effet_bp=eff,
                               IC95_bas=ci[0], IC95_haut=ci[1], p_value=p, statut='EVALUE' if evl else 'NON_EVALUABLE_INFERENTIAL'))
    pd.DataFrame(comp).to_csv(R23 / 'PHASE23B_EVENT_CONTROL_COMPARISON.csv', index=False)
    TB = bh(pd.DataFrame(testsB))
    evw = W[W.role == 'EVENEMENT'].copy()
    evw['signe_reaction_15m'] = np.sign(evw.rend_15m)
    evw['continuation_60m'] = np.where(evw.signe_reaction_15m != 0, evw.signe_reaction_15m * evw.rend_60m, np.nan)
    evw['continuation_4h'] = np.where(evw.signe_reaction_15m != 0, evw.signe_reaction_15m * evw.rend_4h, np.nan)
    evw.groupby('type').agg(n=('rend_15m', 'count'), part_continuation_60m=('continuation_60m', lambda x: float((x > 0).mean())),
                            part_continuation_4h=('continuation_4h', lambda x: float((x > 0).mean())),
                            continuation_60m_mediane=('continuation_60m', 'median'),
                            retour_prix_pre_60m=('retour_prix_pre_60m', 'mean')).reset_index().to_csv(
        R23 / 'PHASE23B_REACTION_CONTINUATION_REVERSAL.csv', index=False)
    spr = W.groupby(['type', 'role']).agg(n=('spread_pre_median', 'count'), spread_pre=('spread_pre_median', 'median'),
                                          spread_post_15m=('spread_post_15m', 'median'), spread_post_60m=('spread_post_60m', 'median')).reset_index()
    spr.to_csv(R23 / 'PHASE23B_SPREAD_AND_EXECUTION_SENSITIVITY.csv', index=False)

    T = pd.concat([TA, TB], ignore_index=True)
    T.to_csv(R23 / 'PHASE23B_MULTIPLE_TEST_CORRECTION.csv', index=False)
    reg = []
    for _, r in T.iterrows():
        reg.append(dict(etude=r.etude, test=f"{r.variable} {r.get('horizon','')} {r.mesure}", q_value=r.q_value_BH,
                        qualification='EFFET_SIGNIFICATIF (candidat descriptif, pas un edge)' if r.q_value_BH < 0.05 else
                        ('NON_EVALUABLE_INFERENTIAL' if r.statut != 'EVALUE' else 'AUCUNE_ASSOCIATION_ROBUSTE')))
    pd.DataFrame(reg).to_csv(R23 / 'PHASE23B_EXTERNAL_INFORMATION_REGISTRY.csv', index=False)
    stats = dict(A_tests=int(len(TA)), A_sig=int((TA.q_value_BH < .05).sum()), B_tests=int(len(TB)), B_sig=int((TB.q_value_BH < .05).sum()),
                 B_fenetres=int(len(W)), B_types=W.type.value_counts().to_dict() if len(W) else {})
    (R23 / '_phase23b_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(json.dumps(stats, indent=1, default=str))


if __name__ == '__main__':
    if sys.argv[1] == 'exo': mode_exo()
    elif sys.argv[1] == 'lot': mode_lot()
    else: mode_analyse()
