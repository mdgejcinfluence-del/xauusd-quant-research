#!/usr/bin/env python3
"""PHASE 20-A - Radiographie structurelle H4 (EXPLORATORY_POST_HOC, IS 2010-2020).
lot: agregation H4 Mid/Bid/Ask par lot de partitions IS (DuckDB), fragments par
barre avec provenance. analyse: barset consolide, amplitudes, MFE/MAE futurs,
saisonnalites, autocorrelations, evenements (compression/expansion/sequences/
cassures), spread, tests de randomisation par decalage circulaire hebdomadaire
(valide sur synthetique), correction Benjamini-Hochberg. Aucun modele, aucune
strategie, aucun P&L. Holdout jamais accede."""
import glob, io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R20 = ROOT / 'reports/meta_alpha/phase20'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
GRAINE = 2007

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
    batch = os.environ['P20_BATCH']
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
    q = f"""WITH s AS (SELECT timestamp_utc AS ts, bid, ask, (bid+ask)/2 AS mid,
                    10000*ln(ask/bid) AS spread_bp FROM read_parquet({lst}, filename=true)
                    WHERE timestamp_utc < '{IS_END}'),
            g AS (SELECT *, time_bucket(INTERVAL 4 HOUR, ts) AS bar_start,
                    lag(ts) OVER (PARTITION BY time_bucket(INTERVAL 4 HOUR, ts) ORDER BY ts) AS pts FROM s)
            SELECT bar_start,
                   arg_min(mid, ts) AS open_mid, max(mid) AS high_mid, min(mid) AS low_mid,
                   arg_max(mid, ts) AS close_mid,
                   arg_min(bid, ts) AS open_bid, arg_max(bid, ts) AS close_bid,
                   arg_min(ask, ts) AS open_ask, arg_max(ask, ts) AS close_ask,
                   min(ts) AS first_ts, max(ts) AS last_ts, count(*) AS n_quotes,
                   max(epoch(ts)-epoch(pts)) AS max_gap_s,
                   median(spread_bp) AS spread_median_bp, avg(spread_bp) AS spread_mean_bp,
                   count(DISTINCT filename) AS n_partitions_sources
            FROM g GROUP BY bar_start ORDER BY bar_start"""
    b = con.execute(q).df()
    b['source_batch'] = batch
    R20.mkdir(parents=True, exist_ok=True)
    b.to_csv(R20 / f'P20_H4FRAG_{batch}.csv', index=False)
    print('P20 lot termine', batch, len(b), 'fragments H4', flush=True)

def consolider():
    fr = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(str(R20 / 'P20_H4FRAG_*.csv')))])
    for c in ['bar_start', 'first_ts', 'last_ts']: fr[c] = pd.to_datetime(fr[c]).dt.tz_localize(None)
    rows = []
    for bs, g in fr.groupby('bar_start'):
        go = g.loc[g.first_ts.idxmin()]; gc = g.loc[g.last_ts.idxmax()]
        rows.append(dict(bar_start=bs, open=float(go.open_mid), high=float(g.high_mid.max()), low=float(g.low_mid.min()),
                         close=float(gc.close_mid), open_bid=float(go.open_bid), close_bid=float(gc.close_bid),
                         open_ask=float(go.open_ask), close_ask=float(gc.close_ask),
                         first_ts=g.first_ts.min(), last_ts=g.last_ts.max(), n_quotes=int(g.n_quotes.sum()),
                         max_gap_s=float(max(g.max_gap_s.max(), (g.sort_values('first_ts').first_ts.diff().dt.total_seconds().max() if len(g) > 1 else 0) or 0)),
                         spread_median_bp=float(np.average(g.spread_median_bp, weights=g.n_quotes)),
                         spread_mean_bp=float(np.average(g.spread_mean_bp, weights=g.n_quotes)),
                         n_partitions_sources=int(g.n_partitions_sources.sum()), n_fragments=int(len(g)),
                         source_batches='|'.join(sorted(g.source_batch.unique()))))
    b = pd.DataFrame(rows).sort_values('bar_start').reset_index(drop=True)
    b['couverture_s'] = (b.last_ts - b.first_ts).dt.total_seconds()
    b['complete'] = (b.couverture_s >= 3.5 * 3600) & (b.max_gap_s <= 1800)
    b['qualite'] = np.where(b.complete, 'COMPLETE', 'PARTIELLE_OU_TROU')
    return b

def logbp(p1, p2): return 10000 * np.log(p2 / p1)

def construire_barset():
    b = consolider()
    b['BODY_BP'] = logbp(b.open, b.close); b['ABS_BODY_BP'] = b.BODY_BP.abs()
    b['RANGE_BP'] = 10000 * np.log(b.high / b.low)
    prev_close = b.close.shift(1); consecutif = (b.bar_start.diff() == pd.Timedelta(hours=4)) & b.complete & b.complete.shift(1).fillna(False)
    tr_hi = 10000 * np.log(np.maximum(b.high, prev_close) / np.minimum(b.low, prev_close))
    b['TRUE_RANGE_BP'] = np.where(consecutif, tr_hi, np.nan)
    # ATR14 causal: moyenne simple des 14 TRUE_RANGE precedents (barre courante exclue), chaines consecutives exigees
    atr = np.full(len(b), np.nan)
    tr = b.TRUE_RANGE_BP.values; comp = b.complete.values
    for i in range(14, len(b)):
        fen = tr[i - 14:i]
        if comp[i] and np.isfinite(fen).all() and (b.bar_start.values[i] - b.bar_start.values[i - 14]) == np.timedelta64(14 * 4, 'h'):
            atr[i] = fen.mean()
    b['ATR14_H4_PREV'] = atr
    b['RANGE_ATR14'] = b.RANGE_BP / b.ATR14_H4_PREV; b['BODY_ATR14'] = b.ABS_BODY_BP / b.ATR14_H4_PREV
    b['sens'] = np.sign(b.BODY_BP).astype(int)
    b['slot_utc'] = b.bar_start.dt.hour; b['jour_semaine'] = b.bar_start.dt.dayofweek
    b['semaine_iso'] = b.bar_start.dt.strftime('%G-W%V')
    return b

def forward(b):
    """MFE/MAE futurs horizons 1..4 sur barres completes consecutives, depuis le Close."""
    n = len(b); out = pd.DataFrame({'bar_start': b.bar_start, 'event_id': ['H4-' + t.strftime('%Y%m%d%H') for t in b.bar_start]})
    comp = b.complete.values; starts = b.bar_start.values
    for H in (1, 2, 3, 4):
        mfe = np.full(n, np.nan); mae = np.full(n, np.nan); up = np.full(n, np.nan); dn = np.full(n, np.nan); term = np.full(n, np.nan)
        for i in range(n - H):
            if not comp[i] or not comp[i + 1:i + H + 1].all(): continue
            if starts[i + H] - starts[i] != np.timedelta64(4 * H, 'h'): continue
            c = b.close.values[i]; hi = b.high.values[i + 1:i + H + 1].max(); lo = b.low.values[i + 1:i + H + 1].min()
            up[i] = 10000 * np.log(hi / c); dn[i] = -10000 * np.log(lo / c)
            s = b.sens.values[i]
            if s > 0: mfe[i], mae[i] = up[i], dn[i]
            elif s < 0: mfe[i], mae[i] = dn[i], up[i]
            term[i] = s * 10000 * np.log(b.close.values[i + H] / c) if s != 0 else np.nan
        out[f'MFE_{H}'] = mfe; out[f'MAE_{H}'] = mae; out[f'UP_{H}'] = up; out[f'DOWN_{H}'] = dn; out[f'TERMINAL_{H}'] = term
    return out

def bh(pvals):
    p = np.asarray(pvals, float); ordre = np.argsort(p); q = np.empty(len(p)); prev = 1.0
    for i, idx in enumerate(ordre[::-1]):
        rang = len(p) - i; prev = min(prev, p[idx] * len(p) / rang); q[idx] = prev
    return q

def test_decalage(semaines_outcomes, indicateurs, n_rep=10000, graine=GRAINE):
    """semaines_outcomes: array (n_semaines, 42) de resultats futurs (grille hebdomadaire);
    indicateurs: dict nom -> array (n_semaines, 42) booleen d'evenements.
    Decalage circulaire des resultats par semaines entieres (min 2) dans l'annee:
    ici decalage global sur l'axe semaines (grille deja ordonnee), p bilaterale."""
    ...

def mode_analyse():
    b = construire_barset()
    b.to_parquet(R20 / 'PHASE20A_H4_BARSET.parquet', index=False)
    fw = forward(b)
    fw.to_parquet(R20 / 'PHASE20A_H4_FORWARD_MFE_MAE.parquet', index=False)
    j = b.merge(fw, on=['bar_start'], how='left')
    # ---- qualite des donnees
    attendues = pd.date_range(b.bar_start.min(), b.bar_start.max(), freq='4h')
    dq = [dict(verif='barres_presentes', n=int(len(b))),
          dict(verif='barres_attendues_grille_4h', n=int(len(attendues))),
          dict(verif='barres_absentes_grille', n=int(len(attendues) - len(b))),
          dict(verif='barres_completes', n=int(b.complete.sum())),
          dict(verif='barres_partielles_ou_trou', n=int((~b.complete).sum())),
          dict(verif='doublons_bar_start', n=int(b.bar_start.duplicated().sum())),
          dict(verif='prix_non_positifs', n=int((b[['open','high','low','close']] <= 0).sum().sum())),
          dict(verif='bid_sup_ask_ouverture', n=int((b.open_bid > b.open_ask).sum())),
          dict(verif='ohlc_incoherentes', n=int(((b.high < b[['open','close']].max(axis=1)) | (b.low > b[['open','close']].min(axis=1))).sum())),
          dict(verif='GAP_CAUSE_UNVERIFIED (intervalles sans cotation: cause non etablie)', n=int(len(attendues) - len(b)))]
    pd.DataFrame(dq).to_csv(R20 / 'PHASE20A_H4_DATA_QUALITY.csv', index=False)
    # ---- distributions d'amplitude
    def dist(nom, s):
        s = pd.Series(s).dropna(); r = dict(mesure=nom, n=int(len(s)), moyenne=float(s.mean()), mediane=float(s.median()),
            ecart_type=float(s.std()), mad=float((s - s.median()).abs().median()), minimum=float(s.min()), maximum=float(s.max()))
        for p in (1, 5, 10, 25, 50, 75, 90, 95, 99): r[f'P{p}'] = float(s.quantile(p / 100))
        for seuil in (30, 60, 100): r[f'part_sup_{seuil}bp'] = float((s > seuil).mean())
        return r
    dists = [dist('BODY_BP signe', j.BODY_BP), dist('ABS_BODY_BP', j.ABS_BODY_BP), dist('RANGE_BP', j.RANGE_BP),
             dist('TRUE_RANGE_BP', j.TRUE_RANGE_BP), dist('RANGE_ATR14', j.RANGE_ATR14), dist('BODY_ATR14', j.BODY_ATR14)]
    pd.DataFrame(dists).to_csv(R20 / 'PHASE20A_H4_AMPLITUDE_DISTRIBUTIONS.csv', index=False)
    # ---- carte sessions / jours / matrice 42
    lignes = []
    def stats_session(g, type_, cle):
        r = dict(type=type_, cle=str(cle), n=int(len(g)), BODY_moyen=float(g.BODY_BP.mean()), BODY_mediane=float(g.BODY_BP.median()),
                 RANGE_mediane=float(g.RANGE_BP.median()), RANGE_P90=float(g.RANGE_BP.quantile(.9)), RANGE_P95=float(g.RANGE_BP.quantile(.95)),
                 RANGE_P99=float(g.RANGE_BP.quantile(.99)), part_RANGE_sup30=float((g.RANGE_BP > 30).mean()),
                 part_RANGE_sup60=float((g.RANGE_BP > 60).mean()), part_RANGE_sup100=float((g.RANGE_BP > 100).mean()),
                 grandes_positives=float(((g.BODY_BP > 60)).mean()), grandes_negatives=float((g.BODY_BP < -60).mean()))
        for H in (1, 2, 3, 4):
            r[f'MFE{H}_mediane'] = float(g[f'MFE_{H}'].median()); r[f'MAE{H}_mediane'] = float(g[f'MAE_{H}'].median())
        return r
    for slot, g in j.groupby('slot_utc'): lignes.append(stats_session(g, 'SLOT_UTC', slot))
    for js, g in j.groupby('jour_semaine'): lignes.append(stats_session(g, 'JOUR_SEMAINE (0=lundi)', js))
    for (js, slot), g in j.groupby(['jour_semaine', 'slot_utc']): lignes.append(stats_session(g, 'MATRICE_JOURxSLOT', f'{js}x{slot:02d}'))
    pd.DataFrame(lignes).to_csv(R20 / 'PHASE20A_H4_SESSION_WEEKDAY_MAP.csv', index=False)
    # ---- autocorrelations
    series = {'rendements signes': j.BODY_BP, 'rendements absolus': j.ABS_BODY_BP, 'RANGE_BP': j.RANGE_BP,
              'TRUE_RANGE_BP': j.TRUE_RANGE_BP, 'direction (signe du corps)': j.sens.astype(float)}
    ac = []
    for nom, s in series.items():
        s = s.reset_index(drop=True)
        for lag in list(range(1, 13)) + [24]:
            r = s.autocorr(lag) if s.autocorr(lag) == s.autocorr(lag) else np.nan
            ac.append(dict(serie=nom, retard_H4=lag, autocorrelation=float(r) if r == r else None,
                           ic95_approx=[float(-1.96 / np.sqrt(len(s.dropna()))), float(1.96 / np.sqrt(len(s.dropna())))],
                           note='IC sous hypothese bruit blanc: lecture descriptive, dependance hebdomadaire documentee par ailleurs'))
    pd.DataFrame(ac).to_csv(R20 / 'PHASE20A_H4_AUTOCORRELATION.csv', index=False)
    # ---- evenements: compression/expansion roulantes, sequences, cassures
    ev = evenements(j)
    ev.to_parquet(R20 / 'PHASE20A_H4_EVENT_CATALOG.parquet', index=False)
    cond, tests = comportements(j, ev)
    cond.to_csv(R20 / 'PHASE20A_H4_CONDITIONAL_BEHAVIOR.csv', index=False)
    brk = cond[cond.famille.str.startswith('CASSURE')].copy()
    brk.to_csv(R20 / 'PHASE20A_H4_BREAKOUT_ANALYSIS.csv', index=False)
    stk = cond[cond.famille.str.startswith('SEQUENCE')].copy()
    stk.to_csv(R20 / 'PHASE20A_H4_STREAK_ANALYSIS.csv', index=False)
    tests.to_csv(R20 / 'PHASE20A_H4_RANDOMNESS_TESTS.csv', index=False)
    mt = tests.copy(); mt['q_value_BH'] = bh(mt.p_value.values) if len(mt) else []
    mt.to_csv(R20 / 'PHASE20A_H4_MULTIPLE_TEST_CORRECTION.csv', index=False)
    # ---- spread / amplitude
    lignes = []
    for slot, g in j.groupby('slot_utc'):
        lignes.append(dict(slot_utc=int(slot), n_barres=int(len(g)), spread_mediane_par_barre=float(g.spread_median_bp.median()),
                           spread_moyen_pondere_cotations=float(np.average(g.spread_mean_bp, weights=g.n_quotes)),
                           RANGE_mediane=float(g.RANGE_BP.median()),
                           SPREAD_TO_RANGE=float(g.spread_median_bp.median() / g.RANGE_BP.median()),
                           ratio_individuel_mediane=float((g.spread_median_bp / g.RANGE_BP).median()),
                           ratio_individuel_P75=float((g.spread_median_bp / g.RANGE_BP).quantile(.75)),
                           ratio_individuel_P90=float((g.spread_median_bp / g.RANGE_BP).quantile(.9))))
    pd.DataFrame(lignes).to_csv(R20 / 'PHASE20A_H4_SPREAD_AMPLITUDE_MAP.csv', index=False)
    # ---- registre d'anomalies
    reg = registre_anomalies(cond, mt, j)
    reg.to_csv(R20 / 'PHASE20A_H4_ANOMALY_REGISTRY.csv', index=False)
    stats = dict(n_barres=int(len(b)), n_completes=int(b.complete.sum()), periode=[str(b.bar_start.min()), str(b.bar_start.max())],
                 n_evenements=int(len(ev)), n_tests=int(len(mt)), n_q_significatifs=int((mt.q_value_BH < 0.05).sum()) if len(mt) else 0)
    (R20 / '_phase20a_stats.json').write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1), flush=True)

def evenements(j):
    ev = []
    rng = j.RANGE_BP.values; comp = j.complete.values
    q10 = np.full(len(j), np.nan); q90 = np.full(len(j), np.nan)
    for i in range(250, len(j)):
        fen = rng[i - 250:i]
        if np.isfinite(fen).all(): q10[i] = np.quantile(fen, .10); q90[i] = np.quantile(fen, .90)
    for i in range(len(j)):
        if np.isfinite(q10[i]) and rng[i] <= q10[i]: ev.append(dict(bar_start=j.bar_start.iloc[i], famille='COMPRESSION_Q10_ROULANT', run_id='', direction=0))
        if np.isfinite(q90[i]) and rng[i] >= q90[i]: ev.append(dict(bar_start=j.bar_start.iloc[i], famille='EXPANSION_Q90_ROULANT', run_id='', direction=0))
    # sequences maximales de meme sens
    sens = j.sens.values; debut = 0
    for i in range(1, len(j) + 1):
        if i == len(j) or sens[i] == 0 or sens[i] != sens[debut] or j.bar_start.iloc[i] - j.bar_start.iloc[i - 1] != pd.Timedelta(hours=4):
            if sens[debut] != 0 and i - debut >= 2:
                ev.append(dict(bar_start=j.bar_start.iloc[i - 1], famille=f'SEQUENCE_LONGUEUR_{min(i - debut, 5)}{"+" if i - debut >= 5 else ""}',
                               run_id=f'RUN-{debut}', direction=int(sens[debut])))
            debut = i
    # cassures (niveaux des barres precedentes uniquement)
    hi = j.high.values; lo = j.low.values; cl = j.close.values
    for i in range(6, len(j)):
        if j.bar_start.iloc[i] - j.bar_start.iloc[i - 1] != pd.Timedelta(hours=4): continue
        for fam, niv_hi, niv_lo in [('CASSURE_PRECEDENTE', hi[i - 1], lo[i - 1]), ('CASSURE_6_BARRES', hi[i - 6:i].max(), lo[i - 6:i].min())]:
            if hi[i] > niv_hi: ev.append(dict(bar_start=j.bar_start.iloc[i], famille=fam + '_HAUT_INTRABARRE', run_id='', direction=1))
            if lo[i] < niv_lo: ev.append(dict(bar_start=j.bar_start.iloc[i], famille=fam + '_BAS_INTRABARRE', run_id='', direction=-1))
            if cl[i] > niv_hi: ev.append(dict(bar_start=j.bar_start.iloc[i], famille=fam + '_HAUT_CLOTURE', run_id='', direction=1))
            if cl[i] < niv_lo: ev.append(dict(bar_start=j.bar_start.iloc[i], famille=fam + '_BAS_CLOTURE', run_id='', direction=-1))
    E = pd.DataFrame(ev)
    return E

def comportements(j, ev):
    """Comportements conditionnels + tests de decalage circulaire hebdomadaire."""
    jj = j.set_index('bar_start')
    lignes = []; tests = []
    # grille hebdomadaire reguliere (42 creneaux) pour la randomisation
    grille = pd.date_range(j.bar_start.min(), j.bar_start.max(), freq='4h')
    base = pd.DataFrame({'bar_start': grille}).merge(j, on='bar_start', how='left')
    rng = np.random.default_rng(GRAINE)
    # controle synthetique de la procedure de decalage (avant usage)
    syn = rng.normal(0, 1, (400, 42)); ind_syn = rng.random((400, 42)) < 0.1
    p_syn = p_decalage(semaines_depuis_grille(syn), ind_syn, rng)
    print('controle synthetique randomisation: p =', round(float(p_syn), 3), '(attendu non significatif en general)', flush=True)
    for fam, g in ev.groupby('famille'):
        idx = j.bar_start.isin(g.bar_start).values
        n_sem = j.loc[idx, 'semaine_iso'].nunique()
        dir_fam = int(g.direction.iloc[0]) if 'direction' in g else 0
        for H in (1, 2, 3, 4):
            term_raw = 10000 * np.log(j.close.shift(-H) / j.close).values
            if dir_fam == 0:
                serie = np.abs(j[f'UP_{H}'].values) + np.abs(j[f'DOWN_{H}'].values)  # amplitude d'excursion totale
            else:
                serie = dir_fam * term_raw
            obs = np.nanmean(serie[idx]) if idx.any() else np.nan
            ref = np.nanmean(serie[~idx]) if (~idx).any() else np.nan
            lignes.append(dict(famille=fam, horizon=H, n_evenements=int(idx.sum()), n_semaines=int(n_sem),
                               effet_moyen=float(obs - ref) if np.isfinite(obs) else None,
                               MFE_mediane=float(np.nanmedian(j[f'MFE_{H}'].values[idx])) if idx.any() else None,
                               MAE_mediane=float(np.nanmedian(j[f'MAE_{H}'].values[idx])) if idx.any() else None,
                               terminal_moyen=float(np.nanmean(j[f'TERMINAL_{H}'].values[idx])) if idx.any() else None,
                               part_sup30=float(np.nanmean((np.abs(j[f'TERMINAL_{H}'].values[idx]) > 30))) if idx.any() else None,
                               part_sup60=float(np.nanmean((np.abs(j[f'TERMINAL_{H}'].values[idx]) > 60))) if idx.any() else None,
                               part_sup100=float(np.nanmean((np.abs(j[f'TERMINAL_{H}'].values[idx]) > 100))) if idx.any() else None))
            if idx.sum() >= 50 and n_sem >= 20:
                base['_serie_test'] = serie
                p = p_decalage(semaines_depuis_grille(base, '_serie_test'), masque_grille(base, g.bar_start), rng)
                tests.append(dict(famille=fam, horizon=H, mesure=f'TERMINAL_{H} (ou amplitude pour compression/expansion)',
                                  n_evenements=int(idx.sum()), n_semaines=int(n_sem), effet=float(obs - ref), p_value=float(p),
                                  statut='EVALUE'))
            else:
                tests.append(dict(famille=fam, horizon=H, mesure='TERMINAL', n_evenements=int(idx.sum()), n_semaines=int(n_sem),
                                  effet=float(obs - ref) if np.isfinite(obs) else None, p_value=np.nan, statut='NON_EVALUABLE_INFERENTIAL'))
    return pd.DataFrame(lignes), pd.DataFrame(tests)

def semaines_depuis_grille(base_ou_syn, colonne=None):
    if colonne is None:  # synthetique deja en (semaines, 42)
        return base_ou_syn
    b = base_ou_syn.copy()
    b['semaine'] = b.bar_start.dt.strftime('%G-W%V')
    piv = b.pivot_table(index='semaine', columns=b.bar_start.dt.hour, values=colonne, aggfunc='first')
    # reordonner en 42 creneaux: pivot par (jour, heure) via index de grille
    b['creneau'] = ((b.bar_start.dt.dayofweek) * 6 + (b.bar_start.dt.hour // 4))
    piv = b.pivot_table(index='semaine', columns='creneau', values=colonne, aggfunc='first')
    piv = piv.reindex(columns=range(42))
    return piv.values.astype(float)

def masque_grille(base, dates):
    b = base.copy(); b['semaine'] = b.bar_start.dt.strftime('%G-W%V')
    b['creneau'] = ((b.bar_start.dt.dayofweek) * 6 + (b.bar_start.dt.hour // 4))
    b['est'] = b.bar_start.isin(set(dates))
    piv = b.pivot_table(index='semaine', columns='creneau', values='est', aggfunc='first').reindex(columns=range(42))
    return np.nan_to_num(piv.values.astype(float), nan=0.0) > 0

def p_decalage(outcomes, indicateur, rng, n_rep=10000):
    """Decalage circulaire des resultats par semaines entieres (>=2) sur l'axe des
    semaines de la grille; p bilaterale sur la moyenne des evenements."""
    obs_mask = indicateur & np.isfinite(outcomes)
    if obs_mask.sum() == 0: return np.nan
    obs = np.nanmean(outcomes[obs_mask])
    n_sem = outcomes.shape[0]; stats = []
    for _ in range(n_rep):
        k = int(rng.integers(2, max(3, n_sem - 2)))
        decale = np.roll(outcomes, shift=k, axis=0)
        m = indicateur & np.isfinite(decale)
        if m.sum(): stats.append(np.nanmean(decale[m]))
    stats = np.array(stats)
    return float((np.abs(stats - np.nanmean(outcomes[np.isfinite(outcomes)])) >= abs(obs - np.nanmean(outcomes[np.isfinite(outcomes)]))).mean())

def registre_anomalies(cond, mt, j):
    lignes = []
    qmap = {}
    if len(mt):
        for r in mt.itertuples(): qmap[(r.famille, r.horizon)] = (r.p_value, getattr(r, 'q_value_BH', np.nan), r.statut)
    for fam, g in cond.groupby('famille'):
        g4 = g[g.horizon == 4].iloc[0] if (g.horizon == 4).any() else g.iloc[-1]
        p, q, statut = qmap.get((fam, 4), (np.nan, np.nan, 'NON_EVALUABLE_INFERENTIAL'))
        # stabilite: effet terminal H4 par sous-periode via catalogue simplifie (signe compare dans comportements par periode non recalcule ici)
        if statut != 'EVALUE' or not np.isfinite(q): qual = 'INSUFFICIENT_EVIDENCE'
        elif q < 0.05 and abs(g4.effet_moyen or 0) > 4.5: qual = 'AMPLITUDE_SUPPORTED_ANOMALY'
        elif q < 0.05: qual = 'STATISTICAL_ANOMALY_CANDIDATE'
        else: qual = 'RARE_STRUCTURAL_OBSERVATION'
        lignes.append(dict(famille=fam, definition='voir PHASE20A_H4_EVENT_CATALOG et moteur phase20a_engine.evenements',
                           n_occurrences=int(g4.n_evenements), n_semaines=int(g4.n_semaines),
                           effet_terminal_H4_bp=g4.effet_moyen, MFE_mediane_H4=g4.MFE_mediane, MAE_mediane_H4=g4.MAE_mediane,
                           part_sup30=g4.part_sup30, part_sup60=g4.part_sup60, part_sup100=g4.part_sup100,
                           p_value=p, q_value=q, qualification=qual))
    return pd.DataFrame(lignes)

if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
