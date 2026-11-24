#!/usr/bin/env python3
"""MA-EDGE-02 EXP-08..EXP-12 (EXPLORATORY_POST_HOC, preregistre seq411).
Donnees consommees 2010-2019; barres Mid = majorant; couts en scenarios."""
import pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
R24 = R / 'reports/meta_alpha/phase24'
OUT = R / 'research/MA-EDGE-02'
rng = np.random.default_rng(411)

B = pd.read_parquet(R24 / 'PHASE24B_M15_BARSET.parquet')
B = B[B.complete].sort_values('bar_start').reset_index(drop=True)
cl, hi, lo, op = B.close.values, B.high.values, B.low.values, B.open.values
starts = B.bar_start.values
idx_of = {str(s): i for i, s in enumerate(B.bar_start)}
absb = np.abs(10000 * np.log(cl / op))
q90 = np.full(len(B), np.nan)
for i in range(250, len(B)):
    fen = absb[i - 250:i]
    if np.isfinite(fen).all():
        q90[i] = np.quantile(fen, .90)
imp = [i for i in range(250, len(B)) if np.isfinite(q90[i]) and absb[i] >= q90[i] and absb[i] > 0]
print(f'barres completes={len(B)} impulsions={len(imp)}')


def periode(ts):
    y = pd.Timestamp(ts).year
    return 'DEC' if y <= 2015 else ('CTL' if y <= 2017 else 'REJ')


def fwd(i, d, H):
    """rendement directionnel Mid a H barres + MFE/MAE (bp log)."""
    if i + H >= len(B):
        return None
    r = d * 10000 * np.log(cl[i + H] / cl[i])
    seg_hi, seg_lo = hi[i + 1:i + H + 1], lo[i + 1:i + H + 1]
    mfe = d * 10000 * np.log((seg_hi.max() if d > 0 else seg_lo.min()) / cl[i])
    mae = d * 10000 * np.log((seg_lo.min() if d > 0 else seg_hi.max()) / cl[i])
    return r, mfe, mae


# ---------- EXP-09 familles nouvelles + placebo ----------
rows = []
for i in imp:
    t0 = starts[i] + np.timedelta64(15, 'm')
    if not (8 <= pd.Timestamp(t0).hour < 16):
        continue
    d = 1 if cl[i] > op[i] else -1
    per = periode(t0)
    for H in (8, 32):
        f = fwd(i, d, H)
        if f:
            rows.append(dict(regle='A_continuation', H=H, periode=per, annee=pd.Timestamp(t0).year, ret=f[0]))
            rows.append(dict(regle='B_fade', H=H, periode=per, annee=pd.Timestamp(t0).year, ret=-f[0]))
    f8 = fwd(i, d, 8)
    # C confirmation locale
    if i + 9 < len(B) and (cl[i + 1] - cl[i]) * d > 0:
        rows.append(dict(regle='C_confirmation', H=8, periode=per, annee=pd.Timestamp(t0).year,
                         ret=d * 10000 * np.log(cl[i + 9] / cl[i + 1])))
    # D entree differee si retracement < 50% du corps
    if i + 12 < len(B):
        corps = abs(cl[i] - op[i])
        retrace = (cl[i] - cl[i + 4]) * d  # >0 si prix revenu contre l'impulsion
        if retrace < 0.5 * corps:
            rows.append(dict(regle='D_differee', H=8, periode=per, annee=pd.Timestamp(t0).year,
                             ret=d * 10000 * np.log(cl[i + 12] / cl[i + 4])))
E9 = pd.DataFrame(rows)
E9.to_csv(OUT / 'EXP09_family_trades.csv', index=False)
# placebo: instants aleatoires horloge, sens aleatoire, horizon 8/32
elig = [i for i in range(250, len(B) - 33) if 8 <= (pd.Timestamp(starts[i]) + pd.Timedelta(minutes=15)).hour < 16]
plac = {8: [], 32: []}
for _ in range(200):
    sel = rng.choice(elig, size=min(len(imp), len(elig)), replace=False)
    for H in (8, 32):
        vals = []
        for i in sel:
            d = rng.choice([-1, 1])
            vals.append(d * 10000 * np.log(cl[i + H] / cl[i]))
        plac[H].append(np.mean(vals))
res9 = []
for (regle, H), g in E9.groupby(['regle', 'H']):
    ligne = dict(regle=regle, H=H, n=len(g))
    for per in ('DEC', 'CTL', 'REJ'):
        ligne[f'moy_{per}'] = round(g[g.periode == per].ret.mean(), 2) if (g.periode == per).any() else np.nan
    ligne['p97_5_placebo'] = round(np.quantile(plac[H], .975), 2) if regle in ('A_continuation',) else np.nan
    res9.append(ligne)
R9 = pd.DataFrame(res9)
R9.to_csv(OUT / 'EXP09_family_summary.csv', index=False)
print(R9.to_string())

# ---------- EXP-11 asymetrie excursions ----------
rows = []
for i in imp:
    t0 = starts[i] + np.timedelta64(15, 'm')
    d = 1 if cl[i] > op[i] else -1
    for H in (4, 8, 32):
        f = fwd(i, d, H)
        if f:
            rows.append(dict(periode=periode(t0), direction=d, amplitude=absb[i], H=H, ret=f[0], MFE=f[1], MAE=f[2]))
E11 = pd.DataFrame(rows)
b1, b2 = E11[(E11.periode == 'DEC') & (E11.H == 8)].amplitude.quantile([1 / 3, 2 / 3]).values
E11['tercile_amp'] = pd.cut(E11.amplitude, [-np.inf, b1, b2, np.inf], labels=['T1', 'T2', 'T3'])
R11 = E11.groupby(['H', 'tercile_amp'], observed=True).agg(
    n=('ret', 'size'), MFE_med=('MFE', 'median'), MAE_med=('MAE', 'median'),
    ratio_med=('ret', lambda s: 0), ret_moy=('ret', 'mean')).reset_index()
R11['asymetrie_MFE_plus_MAE'] = (R11.MFE_med + R11.MAE_med).round(2)
R11[['H', 'tercile_amp', 'n', 'MFE_med', 'MAE_med', 'asymetrie_MFE_plus_MAE', 'ret_moy']].to_csv(OUT / 'EXP11_excursion_asymmetry.csv', index=False)
print(R11[['H', 'tercile_amp', 'n', 'MFE_med', 'MAE_med', 'asymetrie_MFE_plus_MAE', 'ret_moy']].to_string())

# ---------- Evenements: jointures ----------
G = pd.read_parquet(R24 / 'PHASE24B_M15_GATE_PERMISSION_PANEL.parquet')
C = pd.read_parquet(R24 / 'PHASE24E_FIRST_PASSAGE_CATALOG.parquet')
D = pd.read_parquet(R24 / 'PHASE24D_EVENT_PNL_RESULTS.parquet')
sel = D[D.statut == 'COMPLET'][['event_id', 'PNL_S0', 'PNL_S2', 'prix_entree', 'direction']]
C['DECISION_TIMESTAMP'] = pd.to_datetime(C.DECISION_TIMESTAMP)
M = C.merge(sel, on='event_id', how='left').drop_duplicates('event_id')
M['idx_dec'] = [idx_of.get(str(pd.Timestamp(t) - pd.Timedelta(minutes=15)), -1) for t in M.DECISION_TIMESTAMP]
M = M[M.idx_dec >= 0].copy()
print('evenements mappes:', len(M), 'avec PnL:', M.PNL_S2.notna().sum())

# ---------- EXP-08 trajectoire precoce (selectionnes) ----------
r8 = []
for r in M[M.PNL_S2.notna()].itertuples():
    i, d = int(r.idx_dec), int(r.EVENT_DIRECTION)
    if i + 4 >= len(B):
        continue
    r60 = d * 10000 * np.log(cl[i + 4] / cl[i])
    seg_hi, seg_lo = hi[i + 1:i + 5], lo[i + 1:i + 5]
    mfe60 = d * 10000 * np.log((seg_hi.max() if d > 0 else seg_lo.min()) / cl[i])
    mae60 = d * 10000 * np.log((seg_lo.min() if d > 0 else seg_hi.max()) / cl[i])
    r8.append(dict(event_id=r.event_id, periode=periode(r.DECISION_TIMESTAMP), r60=r60, mfe60=mfe60,
                   mae60=mae60, PNL_S2=r.PNL_S2, Y=r.Y_RESUMPTION))
E8 = pd.DataFrame(r8)
E8['etat60'] = pd.cut(E8.r60, [-np.inf, -10, 10, np.inf], labels=['ADVERSE', 'PLAT', 'FAVORABLE'])
R8 = E8.groupby(['periode', 'etat60'], observed=True).agg(n=('PNL_S2', 'size'), PNL_moy=('PNL_S2', 'mean'),
                                                          PNL_med=('PNL_S2', 'median'), freq_Y=('Y', 'mean')).reset_index()
E8.to_csv(OUT / 'EXP08_early_trajectory.csv', index=False)
R8.to_csv(OUT / 'EXP08_summary.csv', index=False)
print(R8.to_string())

# ---------- EXP-10 geometrie du risque ----------
r10 = []
for r in M.itertuples():
    i, d = int(r.idx_dec), int(r.EVENT_DIRECTION)
    j = idx_of.get(str(r.barre_impulsion)) if hasattr(r, 'barre_impulsion') else None
    r10.append(dict(event_id=r.event_id, idx_dec=i, d=d))
# niveau d'invalidation: extreme de la barre d'impulsion (depuis le catalogue gate)
IMP = pd.read_parquet(R24 / 'PHASE24B_M15_IMPULSE_EVENT_CATALOG.parquet').dropna(subset=['t_reintegration']).drop_duplicates(['t_reintegration', 'direction'])
M['barre_impulsion'] = M.set_index([M.DECISION_TIMESTAMP.astype(str), M.EVENT_DIRECTION]).index.map(
    dict(zip(IMP.t_reintegration.astype(str) + '|' + IMP.direction.astype(str), IMP.barre_impulsion))) if False else np.nan
_norm = lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M')
_cle_imp = dict(zip([_norm(t) + '|' + str(int(d)) for t, d in zip(IMP.t_reintegration, IMP.direction)], IMP.barre_impulsion))
M['barre_impulsion'] = [_cle_imp.get(_norm(t) + '|' + str(int(d))) for t, d in zip(M.DECISION_TIMESTAMP, M.EVENT_DIRECTION)]
print('barres impulsion retrouvees:', M.barre_impulsion.notna().sum(), '/', len(M))
GG = G.assign(cle=G.t_decision.astype(str) + '|' + G.direction.astype(str))
inval = {}
for r in GG.assign(cle=[_norm(t) + '|' + str(int(d)) for t, d in zip(GG.t_decision, GG.direction)]).itertuples():
    j = idx_of.get(str(pd.Timestamp(r.barre_impulsion))) if pd.notna(r.barre_impulsion) else None
    if j is not None:
        inval[r.cle] = lo[j] if r.direction > 0 else hi[j]
M['cle'] = [_norm(t) + '|' + str(int(d)) for t, d in zip(M.DECISION_TIMESTAMP, M.EVENT_DIRECTION)]
M['niv_inval'] = M.cle.map(inval)
M['prix_dec'] = [cl[int(i)] for i in M.idx_dec]
M['risque_bp'] = M.apply(lambda r: abs(10000 * np.log(r.prix_dec / r.niv_inval)) if pd.notna(r.niv_inval) else np.nan, axis=1)
M['potentiel_bp'] = M.apply(lambda r: abs(10000 * np.log(r.FAVORABLE_REFERENCE_LEVEL / r.prix_dec)), axis=1)
M['ratio'] = M.potentiel_bp / M.risque_bp
M.loc[~np.isfinite(M.ratio), 'ratio'] = np.nan
dec = M[pd.to_datetime(M.DECISION_TIMESTAMP).dt.year <= 2015]
q1, q2 = dec.ratio.quantile([1 / 3, 2 / 3]).values if dec.ratio.notna().sum() > 30 else (np.nan, np.nan)
if not (np.isfinite(q1) and np.isfinite(q2) and q1 < q2):
    q1, q2 = M.ratio.quantile([1 / 3, 2 / 3]).values
print('bornes terciles ratio (potentiel/risque):', round(q1, 3), round(q2, 3), '| ratio median:', round(M.ratio.median(), 3))
M['tercile_ratio'] = pd.cut(M.ratio, [-np.inf, q1, q2, np.inf], labels=['T1_risque_eleve', 'T2', 'T3_risque_faible'])
M['periode'] = [periode(t) for t in pd.to_datetime(M.DECISION_TIMESTAMP)]
R10a = M.groupby(['periode', 'tercile_ratio'], observed=True).agg(n=('Y_RESUMPTION', 'size'), freq_Y=('Y_RESUMPTION', 'mean')).reset_index()
R10b = M[M.PNL_S2.notna()].groupby(['periode', 'tercile_ratio'], observed=True).agg(n=('PNL_S2', 'size'), PNL_moy=('PNL_S2', 'mean')).reset_index()
R10a.to_csv(OUT / 'EXP10_risk_geometry_Y.csv', index=False)
R10b.to_csv(OUT / 'EXP10_risk_geometry_PNL.csv', index=False)
print(R10a.to_string()); print(R10b.to_string())

# ---------- EXP-12 abstention cout ----------
sp = dict(zip(B.bar_start.astype(str), B.spread_median_bp))
M['spread_dec'] = [sp.get(str(pd.Timestamp(t) - pd.Timedelta(minutes=15))) for t in M.DECISION_TIMESTAMP]
S = M[M.PNL_S2.notna()].copy()
q1, q2 = S.spread_dec.quantile([1 / 3, 2 / 3]).values
S['tercile_spread'] = pd.cut(S.spread_dec, [-np.inf, q1, q2, np.inf], labels=['T1_spread_bas', 'T2', 'T3_spread_haut'])
R12 = S.groupby(['periode', 'tercile_spread'], observed=True).agg(
    n=('PNL_S2', 'size'), PNL_S2_moy=('PNL_S2', 'mean'), cout_moy=('PNL_S0', lambda s: 0)).reset_index()
S['cout_bp'] = S.PNL_S0 - S.PNL_S2
R12['cout_moyen_bp'] = S.groupby(['periode', 'tercile_spread'], observed=True).cout_bp.mean().values
R12.to_csv(OUT / 'EXP12_cost_abstention.csv', index=False)
print(R12.to_string())
print('TERMINE')
