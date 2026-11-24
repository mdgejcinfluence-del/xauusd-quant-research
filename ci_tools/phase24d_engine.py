#!/usr/bin/env python3
"""PHASE 24-D - Evaluation economique evenementielle du Chauffeur M15 gele.
EXPLORATORY_POST_HOC (seq396). Aucun reentrainement. Entree: premier tick reel
strictement apres t_decision (Ask LONG / Bid SHORT, delai <= 60 s, entree < 16:00 UTC).
Sortie: t_decision + 32x15 min, premier Bid/Ask reel a partir de la cible.
Comptabilite 19-B: spread integre une fois; S0=0, S1=0,5, S2=1 bp/cote (principal).
Aucun stop/TP, aucun portefeuille. Holdout interdit.
lot: chemins tick des evenements selectionnes du lot. analyse: P&L + incertitude grappe."""
import io, json, os, pathlib, shutil, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R = ROOT / 'reports/meta_alpha'; R24 = R / 'phase24'
IS_END = pd.Timestamp('2020-01-20 09:36:27')
NS = 10**9; GRAINE = 2125; NBOOT = 10000


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
    S = pd.read_parquet(R24 / 'PHASE24D_SELECTED_EVENTS.parquet')
    S['jour'] = pd.to_datetime(S.t_decision).dt.strftime('%Y-%m-%d')
    jours_dispo = con.execute(f"""SELECT DISTINCT CAST(timestamp_utc AS DATE) AS d FROM read_parquet({lst})
                                  WHERE timestamp_utc < '{IS_END}'""").fetchnumpy()['d']
    jl = set(pd.to_datetime(jours_dispo).strftime('%Y-%m-%d'))
    S = S[S.jour.isin(jl)]
    rows = []
    for jour, gc in S.groupby('jour'):
        debut = (pd.Timestamp(jour) - pd.Timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        fin = (pd.Timestamp(jour) + pd.Timedelta(days=3)).strftime('%Y-%m-%d')
        a = con.execute(f"""SELECT timestamp_utc AS ts, bid, ask FROM read_parquet({lst})
                            WHERE timestamp_utc >= '{debut}' AND timestamp_utc < '{fin}'
                            ORDER BY timestamp_utc""").fetchnumpy()
        if len(a['ts']) < 100: continue
        tt = a['ts'].astype('datetime64[ns]').astype('int64'); bid = a['bid'].astype(float); ask = a['ask'].astype(float)
        for r in gc.itertuples():
            td = pd.Timestamp(r.t_decision); d = int(r.direction)
            t_dec = td.value; t_cible = t_dec + 32 * 15 * 60 * NS
            ie = int(np.searchsorted(tt, t_dec, side='right'))
            rec = dict(event_id=r.event_id, grappe_id=r.grappe_id, semaine_iso=r.semaine_iso,
                       t_decision=str(td), direction=d, etat_h4=r.etat_h4, etat_d1=r.etat_d1)
            if ie >= len(tt) or (tt[ie] - t_dec) / NS > 60:
                rec['statut'] = 'NON_EXECUTION'; rows.append(rec); continue
            t_ent = tt[ie]
            if pd.Timestamp(t_ent).hour >= 16 or (pd.Timestamp(t_ent).date() == td.date() and pd.Timestamp(t_ent) >= td.normalize() + pd.Timedelta(hours=16)):
                rec['statut'] = 'ENTRY_OUTSIDE_ALLOWED_WINDOW'; rows.append(rec); continue
            px_e = float(ask[ie]) if d > 0 else float(bid[ie])
            ix = int(np.searchsorted(tt, t_cible, side='left'))
            if ix >= len(tt):
                rec['statut'] = 'EXIT_CENSORED'; rec['prix_entree'] = px_e; rows.append(rec); continue
            px_s = float(bid[ix]) if d > 0 else float(ask[ix])
            rec.update(statut='COMPLET', prix_entree=px_e, prix_sortie=px_s,
                       delai_entree_sec=float((t_ent - t_dec) / NS), retard_sortie_sec=float((tt[ix] - t_cible) / NS))
            brut = float(d * 10000 * np.log(px_s / px_e))
            for s_, nom in [(0.0, 'S0'), (0.5, 'S1'), (1.0, 'S2')]:
                rec[f'PNL_{nom}'] = brut - 2 * s_
            # trajectoire executable: LONG valorise au Bid, SHORT a l Ask
            seg_t = tt[ie:ix + 1]; seg_p = bid[ie:ix + 1] if d > 0 else ask[ie:ix + 1]
            flott = d * 10000 * np.log(seg_p / px_e)
            rec['MFE_bp'] = float(flott.max()); rec['MAE_bp'] = float(-flott.min())
            rec['t_MFE_min'] = float((seg_t[int(np.argmax(flott))] - t_ent) / NS / 60)
            rec['t_MAE_min'] = float((seg_t[int(np.argmin(flott))] - t_ent) / NS / 60)
            dt = np.diff(seg_t) / NS / 60
            rec['duree_en_perte_min'] = float((dt[flott[:-1] < 0]).sum()) if len(dt) else 0.0
            rec['MFE_positif_mais_terminal_negatif'] = bool(flott.max() > 0 and brut < 0)
            rec['grosse_perte_flottante_puis_positif'] = bool(flott.min() < -50 and brut > 0)
            rows.append(rec)
        print('jour traite', jour, flush=True)
    R24.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(R24 / f'P24D_PNL_{batch}.parquet', index=False)
    print('lot termine', batch, len(rows), flush=True)


def boot_moyenne(df, col, rng):
    groupes = {g: v[col].values for g, v in df.groupby('grappe_id')}
    cles = list(groupes.keys())
    if len(df) < 50 or df.semaine_iso.nunique() < 20:
        return float(df[col].mean()), (np.nan, np.nan), False
    boots = np.empty(NBOOT)
    for i in range(NBOOT):
        boots[i] = np.concatenate([groupes[c] for c in rng.choice(cles, len(cles), replace=True)]).mean()
    return float(df[col].mean()), tuple(np.percentile(boots, [2.5, 97.5])), True


def mode_analyse():
    import glob as _g
    P = pd.concat([pd.read_parquet(f) for f in _g.glob(str(R24 / 'P24D_PNL_*.parquet'))]).drop_duplicates('event_id')
    P.to_parquet(R24 / 'PHASE24D_EVENT_PNL_RESULTS.parquet', index=False)
    C = P[P.statut == 'COMPLET'].copy()
    rng = np.random.default_rng(GRAINE)
    res = {}
    politiques = {'P0': C, 'P1': C[C.etat_h4 == 'EXPANSION'], 'P2': C[C.etat_d1 == 'D1_EXPANSION']}
    lignes = []
    for nom, g in politiques.items():
        moy, ic, ev = boot_moyenne(g, 'PNL_S2', rng)
        lignes.append(dict(politique=nom, n=len(g), grappes=int(g.grappe_id.nunique()), semaines=int(g.semaine_iso.nunique()),
                           evaluable=ev, PNL_S2_moyen=moy, IC95_bas=ic[0], IC95_haut=ic[1],
                           PNL_S2_median=float(g.PNL_S2.median()), PNL_S0_moyen=float(g.PNL_S0.mean()),
                           PNL_S1_moyen=float(g.PNL_S1.mean()), part_positive=float((g.PNL_S2 > 0).mean()),
                           MAE_P95=float(g.MAE_bp.quantile(.95)), MAE_P99=float(g.MAE_bp.quantile(.99)),
                           pire=float(g.PNL_S2.min()), P5=float(g.PNL_S2.quantile(.05))))
        res[nom] = lignes[-1]
    pd.DataFrame(lignes).to_csv(R24 / 'PHASE24D_P0_P1_P2_COMPARISON.csv', index=False)
    # apparie: P0 restreint aux memes identifiants que P1 / P2 (memes evenements, difference = 0 par construction de politique)
    paires = []
    for nom in ('P1', 'P2'):
        g = politiques[nom]
        paires.append(dict(comparaison=f'P0_sur_cohorte_{nom}', n=len(g), PNL_S2_moyen=float(g.PNL_S2.mean()),
                           note='memes evenements et memes P&L que la politique a permission: la permission selectionne, elle ne modifie ni entree ni sortie'))
    pd.DataFrame(paires).to_csv(R24 / 'PHASE24D_PAIRED_COMMON_COHORT_RESULTS.csv', index=False)
    couts = []
    for nom, g in politiques.items():
        for s_ in ('S0', 'S1', 'S2'):
            couts.append(dict(politique=nom, scenario=s_, PNL_moyen=float(g[f'PNL_{s_}'].mean()), PNL_median=float(g[f'PNL_{s_}'].median())))
    pd.DataFrame(couts).to_csv(R24 / 'PHASE24D_S0_S1_S2_COST_AUDIT.csv', index=False)
    res['statuts'] = P.statut.value_counts().to_dict()
    res['chevauchement'] = dict(evenements=len(C))
    (R24 / '_phase24d_stats.json').write_text(json.dumps(res, indent=1, default=str))
    print(res, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'lot': mode_lot()
    elif sys.argv[1] == 'analyse': mode_analyse()
