#!/usr/bin/env python3
"""PHASE 25-B - Cartographie causale GVZ (J-1) et COT (dernier rapport publie).
EXPLORATORY_POST_HOC. Aucun entrainement, aucun filtre, aucune fusion GVZ x COT.
exo: GVZCLS via miroirs GitHub de FRED/CBOE (double source reconciliee) ;
     COT or via fichiers annuels officiels CFTC (futures desagreges), disponibilite
     conservative = mardi du rapport + 4 jours.
analyse: terciles fixes sur la calibration 2016-2017, relecture post-hoc 2018-2019.
Holdout jamais accede."""
import io, json, pathlib, sys, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R = ROOT / 'reports/meta_alpha'; R25 = R / 'phase25'; R24 = R / 'phase24'
SEUIL = 0.5609549968307628


def fetch(url, timeout=60):
    import requests
    r = requests.get(url, timeout=timeout, headers={'User-Agent': 'metaalpha-research/1.0'})
    print('FETCH', url[:120], r.status_code, len(r.content), flush=True)
    return r


def mode_exo():
    R25.mkdir(parents=True, exist_ok=True)
    lignes = ['# PHASE 25-B — RECONCILIATION DES SOURCES GVZ / COT', '']
    # GVZ: deux miroirs independants minimum
    urls = ['https://raw.githubusercontent.com/HK-Tan/ORACLE-VARX/main/dataset/GVZCLS_20080603_20201231.csv',
            'https://raw.githubusercontent.com/HK-Tan/ORACLE-VARX/master/dataset/GVZCLS_20080603_20201231.csv',
            'https://raw.githubusercontent.com/NippaniP/CapstoneProject/main/data/GVZCLS.csv',
            'https://raw.githubusercontent.com/NippaniP/CapstoneProject/master/data/GVZCLS.csv',
            'https://raw.githubusercontent.com/Max-Van/MakeHSBCGreatAgain/main/files/raw/GVZCLS.csv',
            'https://raw.githubusercontent.com/Max-Van/MakeHSBCGreatAgain/master/files/raw/GVZCLS.csv']
    cands = []
    for u in urls:
        try:
            r = fetch(u, timeout=45)
            if r.status_code != 200: continue
            d = pd.read_csv(io.BytesIO(r.content))
            dc = [c for c in d.columns if 'date' in c.lower()]
            vc = [c for c in d.columns if 'GVZ' in c.upper() or c.lower() in ('value', 'close', 'valeur')]
            if dc and vc:
                dd = pd.DataFrame({'date': pd.to_datetime(d[dc[0]], errors='coerce'),
                                   'gvz': pd.to_numeric(d[vc[0]], errors='coerce')}).dropna()
                dd = dd[(dd.date >= '2009-06-01') & (dd.date <= '2020-03-01')]
                lignes.append(f'- GVZ miroir {u[:90]}: {len(dd)} obs {dd.date.min()} -> {dd.date.max()}')
                if len(dd) > 2000: cands.append(dd)
        except Exception as e:
            lignes.append(f'- GVZ miroir ECHEC {type(e).__name__} {u[:60]}')
    if cands:
        g = cands[0]
        if len(cands) > 1:
            m = g.merge(cands[1], on='date', suffixes=('_a', '_b')).dropna()
            ecart = float((m.gvz_a - m.gvz_b).abs().max()) if len(m) else float('nan')
            lignes.append(f'- GVZ reconciliation deux miroirs: {len(m)} dates communes, ecart max {ecart}')
        g = g.rename(columns={'gvz': 'GVZCLS'}); g['source'] = 'miroir GitHub FRED/CBOE GVZCLS (reconcilie si 2 sources)'
        g.to_parquet(R25 / 'PHASE25B_GVZ_DATA.parquet', index=False)
        lignes.append(f'- GVZ sauvegarde: {len(g)} observations')
    else:
        lignes.append('- GVZ: AUCUNE SOURCE VERIFIABLE — etude GVZ bloquee (SOURCE_RECONCILIATION_FAILED)')
    # COT: fichiers annuels officiels CFTC (desagreges futures seulement)
    frames = []
    for an in range(2010, 2020):
        for pat in [f'https://www.cftc.gov/files/dea/history/fut_disagg_txt_{an}.zip']:
            try:
                r = fetch(pat, timeout=120)
                if r.status_code != 200: continue
                z = zipfile.ZipFile(io.BytesIO(r.content))
                nom = z.namelist()[0]
                d = pd.read_csv(z.open(nom), low_memory=False)
                colmarche = [c for c in d.columns if 'Market' in c and 'Name' in c][0]
                or_ = d[d[colmarche].str.contains('GOLD - COMMODITY', na=False)]
                lignes.append(f'- COT {an}: {len(or_)} lignes or ({pat[-30:]})')
                if len(or_): frames.append(or_)
                break
            except Exception as e:
                lignes.append(f'- COT {an}: ECHEC {type(e).__name__}')
    if frames:
        C = pd.concat(frames)
        coldate = [c for c in C.columns if 'Report_Date' in c][0]
        mm_long = [c for c in C.columns if 'M_Money_Positions_Long' in c][0]
        mm_short = [c for c in C.columns if 'M_Money_Positions_Short' in c][0]
        C['date_rapport'] = pd.to_datetime(C[coldate])
        C['net_managed_money'] = pd.to_numeric(C[mm_long], errors='coerce') - pd.to_numeric(C[mm_short], errors='coerce')
        C['disponible_depuis'] = C.date_rapport + pd.Timedelta(days=4)  # vendredi 15:30 ET + marge jours feries (conservateur)
        C = C[['date_rapport', 'disponible_depuis', 'net_managed_money']].dropna().sort_values('date_rapport')
        C['source'] = 'CFTC fut_disagg_txt officiel (disponibilite conservative +4 j)'
        C.to_parquet(R25 / 'PHASE25B_COT_DATA.parquet', index=False)
        lignes.append(f'- COT sauvegarde: {len(C)} rapports hebdomadaires')
    else:
        lignes.append('- COT: AUCUNE SOURCE — etude COT bloquee')
    (R25 / 'PHASE25B_SOURCE_RECONCILIATION.md').write_text('\n'.join(lignes))
    print('\n'.join(lignes), flush=True)


def terciles_analyse(df, col, nom):
    cal = df[df.split == 'CALIBRATION']
    qs = cal[col].quantile([0, 1 / 3, 2 / 3, 1]).values
    df = df.copy(); df['tercile'] = pd.cut(df[col], qs, labels=['T1_bas', 'T2_moyen', 'T3_haut'], include_lowest=True, duplicates='drop')
    rows = []
    for split in ['CALIBRATION', 'EVALUATION']:
        for t, g in df[df.split == split].groupby('tercile', observed=True):
            gg = g.dropna(subset=['PNL_S2'])
            if not len(gg): continue
            real = gg[gg.Y_RESUMPTION == 1]; non = gg[gg.Y_RESUMPTION == 0]
            rows.append(dict(source=nom, split=split, tercile=str(t), n=len(gg), grappes=int(gg.grappe_id.nunique()),
                             freq_Y=round(float(gg.Y_RESUMPTION.mean()), 3),
                             G=round(float(real.PNL_S2.mean()), 2) if len(real) else np.nan,
                             L=round(float(-non.PNL_S2.mean()), 2) if len(non) else np.nan,
                             esperance_S2=round(float(gg.PNL_S2.mean()), 2), mediane_S2=round(float(gg.PNL_S2.median()), 2),
                             MAE_mediane=round(float(gg.MAE_bp.median()), 1) if 'MAE_bp' in gg else np.nan))
    return pd.DataFrame(rows), qs


def mode_analyse():
    P = pd.read_parquet(R24 / 'PHASE24B_M15_GATE_PERMISSION_PANEL.parquet')
    P['event_id'] = ['EV-M15-%06d' % i for i in range(len(P))]
    cal = pd.read_parquet(R24 / 'PHASE24F_CALIB_PNL_RESULTS.parquet')[['event_id', 'PNL_S2', 'MAE_bp', 'statut']]
    ev = pd.read_parquet(R24 / 'PHASE24D_EVENT_PNL_RESULTS.parquet')[['event_id', 'PNL_S2', 'MAE_bp', 'statut']]
    pnl = pd.concat([cal, ev]).drop_duplicates('event_id')
    M = P.merge(pnl, on='event_id', how='left')
    M = M[M.split.isin(['CALIBRATION', 'EVALUATION'])]
    M = M[(M.split == 'EVALUATION') & M.horloge_ok | (M.split == 'CALIBRATION') & M.horloge_ok]
    M['date_decision'] = pd.to_datetime(M.t_decision).dt.normalize()
    sorties = []
    if (R25 / 'PHASE25B_GVZ_DATA.parquet').exists():
        G = pd.read_parquet(R25 / 'PHASE25B_GVZ_DATA.parquet').sort_values('date')
        # J-1 strict: derniere date GVZ strictement anterieure a la date de decision
        mg = pd.merge_asof(M.sort_values('date_decision'), G, left_on='date_decision', right_on='date',
                           direction='backward', allow_exact_matches=False)
        t, qs = terciles_analyse(mg, 'GVZCLS', 'GVZ')
        t.to_csv(R25 / 'PHASE25B_GVZ_TERCILES.csv', index=False)
        sorties.append(f'GVZ frontieres calibration: {np.round(qs, 2)}')
        print(t.to_string(), flush=True)
    if (R25 / 'PHASE25B_COT_DATA.parquet').exists():
        C = pd.read_parquet(R25 / 'PHASE25B_COT_DATA.parquet').sort_values('disponible_depuis')
        mg = pd.merge_asof(M.sort_values('date_decision'), C, left_on='date_decision', right_on='disponible_depuis',
                           direction='backward')
        t, qs = terciles_analyse(mg, 'net_managed_money', 'COT')
        t.to_csv(R25 / 'PHASE25B_COT_TERCILES.csv', index=False)
        sorties.append(f'COT frontieres calibration: {np.round(qs, 0)}')
        print(t.to_string(), flush=True)
    (R25 / '_phase25b_stats.txt').write_text('\n'.join(sorties))


if __name__ == '__main__':
    if sys.argv[1] == 'exo': mode_exo()
    elif sys.argv[1] == 'analyse': mode_analyse()
