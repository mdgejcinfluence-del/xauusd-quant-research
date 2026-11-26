#!/usr/bin/env python3
"""MA-ALPHA-GOLD-01 G-EXP-01..06 (preenregistrees seq419, EXPLORATORY_POST_HOC).
Prix quotidiens/Barres Mid = majorants; couts deduits explicitement. Periodes:
DEC 2010-2015, CTL 2016-2017, REJ 2018-2019."""
import pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research/MA-ALPHA-GOLD-01'
rng = np.random.default_rng(419)


def per(ts):
    y = pd.Timestamp(ts).year
    return 'DEC' if y <= 2015 else ('CTL' if y <= 2017 else 'REJ')


D1 = pd.read_parquet(R / 'reports/meta_alpha/phase21/PHASE21A_D1_BARSET.parquet').sort_values('jour').reset_index(drop=True)
D1['ret1'] = 10000 * np.log(D1.close / D1.close.shift(1))
for H in (5, 10):
    D1[f'fwd{H}'] = 10000 * np.log(D1.close.shift(-H) / D1.close)
spread_d1 = D1.groupby(D1.jour.dt.year)['spread_mediane_barres'].median()
COUT_D1 = float(D1.spread_mediane_barres.median())
print(f'cout aller-retour D1 retenu (spread median): {COUT_D1:.2f} bp')
res = []


def ligne(exp, regle, g, col='ret_net'):
    r = {'experience': exp, 'regle': regle, 'n': len(g)}
    for p in ('DEC', 'CTL', 'REJ'):
        s = g[g.periode == p][col]
        r[f'moy_{p}'] = round(s.mean(), 2) if len(s) else np.nan
        r[f'n_{p}'] = len(s)
    r['moyenne_totale'] = round(g[col].mean(), 2) if len(g) else np.nan
    r['mediane_totale'] = round(g[col].median(), 2) if len(g) else np.nan
    r['part_positifs'] = round((g[col] > 0).mean(), 3) if len(g) else np.nan
    res.append(r)


# ---------- G-EXP-01 COT hebdo ----------
COT = pd.read_parquet(R / 'reports/meta_alpha/phase25/PHASE25B_COT_DATA.parquet').sort_values('disponible_depuis')
D1i = D1.set_index('jour')
rows = []
for r in COT.itertuples():
    t = pd.Timestamp(r.disponible_depuis)
    idx = D1i.index.searchsorted(t)
    if idx + 11 >= len(D1):
        continue
    base = D1.close.iloc[idx]
    rows.append({'date': D1.jour.iloc[idx], 'periode': per(D1.jour.iloc[idx]), 'net': r.net_managed_money,
                 'fwd5': 10000 * np.log(D1.close.iloc[idx + 5] / base), 'fwd10': 10000 * np.log(D1.close.iloc[idx + 10] / base)})
E1 = pd.DataFrame(rows)
q1, q2 = E1[E1.periode == 'DEC'].net.quantile([1 / 3, 2 / 3]).values
d1_, d9 = E1[E1.periode == 'DEC'].net.quantile([.1, .9]).values
E1['tercile'] = pd.cut(E1.net, [-np.inf, q1, q2, np.inf], labels=['T1_net_bas', 'T2', 'T3_net_haut'])
for t, g in E1.groupby('tercile', observed=True):
    for H in (5, 10):
        gg = g.assign(ret_net=g[f'fwd{H}'] - COUT_D1)
        ligne('G-EXP-01', f'COT {t} brut H{H}', gg)
# fade extremes: short si decile haut, long si decile bas
ex = E1[(E1.net >= d9) | (E1.net <= d1_)].copy()
ex['sens'] = np.where(ex.net >= d9, -1, 1)
for H in (5, 10):
    gg = ex.assign(ret_net=ex.sens * ex[f'fwd{H}'] - COUT_D1)
    ligne('G-EXP-01', f'COT fade extremes H{H}', gg)
    gg2 = ex.assign(ret_net=-ex.sens * ex[f'fwd{H}'] - COUT_D1)
    ligne('G-EXP-01', f'COT momentum extremes H{H}', gg2)
E1.to_csv(OUT / 'GEXP01_cot_weekly.csv', index=False)

# ---------- G-EXP-02 GVZ ----------
G = pd.read_parquet(R / 'reports/meta_alpha/phase25/PHASE25B_GVZ_DATA.parquet').sort_values('date')
G['gvz_var5'] = G.GVZCLS - G.GVZCLS.shift(5)
m = G.merge(D1[['jour', 'close']], left_on='date', right_on='jour', how='inner').sort_values('date')
m['RV20'] = (10000 * np.log(m.close / m.close.shift(1))).rolling(20).std()
for H in (5, 20):
    m[f'fwd{H}'] = 10000 * np.log(m.close.shift(-H) / m.close)
m['periode'] = [per(t) for t in m.date]
m = m.dropna(subset=['fwd20']).copy()
m['ecart'] = m.GVZCLS - m.RV20 / 100 * 16  # GVZ en % annualise vs RV bp->% approx (documente)
dec = m[m.periode == 'DEC']
g1, g2 = dec.GVZCLS.quantile([1 / 3, 2 / 3]).values
m['tercile'] = pd.cut(m.GVZCLS, [-np.inf, g1, g2, np.inf], labels=['GVZ_bas', 'GVZ_mid', 'GVZ_haut'])
for t, g in m.groupby('tercile', observed=True):
    for H in (5, 20):
        ligne('G-EXP-02', f'GVZ {t} long brut H{H}', g.assign(ret_net=g[f'fwd{H}'] - COUT_D1))
for H in (5, 20):
    hi_ = m[m.tercile == 'GVZ_haut'].assign(ret_net=lambda x: x[f'fwd{H}'] - COUT_D1)
    ligne('G-EXP-02', f'GVZ haut -> LONG (peur) H{H}', hi_)
    ligne('G-EXP-02', f'GVZ haut -> SHORT H{H}', hi_.assign(ret_net=-hi_[f'fwd{H}'] - COUT_D1))
m.to_csv(OUT / 'GEXP02_gvz.csv', index=False)

# ---------- G-EXP-03 taux reels ----------
P = pd.read_parquet(R / 'reports/meta_alpha/phase23/PHASE23B_XAU_DAILY_CONTEXT_PANEL.parquet')
F = P[P.serie == 'DFII10'][['jour', 'valeur_connue']].sort_values('jour')
m3 = D1[['jour', 'close', 'fwd5']].copy()
m3['fwd20'] = 10000 * np.log(m3.close.shift(-20) / m3.close)
m3 = m3.merge(F, on='jour', how='left')
m3['var5'] = m3.valeur_connue - m3.valeur_connue.shift(5)
m3['periode'] = [per(t) for t in m3.jour]
m3 = m3.dropna(subset=['var5', 'fwd20'])
for H in (5, 20):
    gg = m3.assign(ret_net=np.where(m3.var5 < 0, m3[f'fwd{H}'], -m3[f'fwd{H}']) - COUT_D1)
    ligne('G-EXP-03', f'Taux reels: baisse->long / hausse->short H{H}', gg)
    ligne('G-EXP-03', f'Taux reels: rendement brut long conditionnel H{H}', m3.assign(ret_net=m3[f'fwd{H}'] - COUT_D1))
m3.to_csv(OUT / 'GEXP03_real_rates.csv', index=False)

# ---------- G-EXP-04 D1 momentum / fade / cassure ----------
m4 = D1.copy()
m4['periode'] = [per(t) for t in m4.jour]
m4['ret5p'] = 10000 * np.log(m4.close / m4.close.shift(5))
m4['fwd1'] = m4.ret1.shift(-1)
m4 = m4.dropna(subset=['ret5p', 'fwd5'])
for H, col in ((1, 'fwd1'), (5, 'fwd5')):
    ligne('G-EXP-04', f'Momentum 5j signe H{H}', m4.assign(ret_net=np.sign(m4.ret5p) * m4[col] - COUT_D1))
    ligne('G-EXP-04', f'Fade momentum 5j H{H}', m4.assign(ret_net=-np.sign(m4.ret5p) * m4[col] - COUT_D1))
qq = m4[m4.periode == 'DEC'].ABS_BODY_BP.quantile(.9)
ext = m4[m4.ABS_BODY_BP >= qq]
for H, col in ((1, 'fwd1'), (5, 'fwd5')):
    ligne('G-EXP-04', f'Fade journee extreme H{H}', ext.assign(ret_net=-np.sign(ext.ret1) * ext[col] - COUT_D1))
    ligne('G-EXP-04', f'Continuation journee extreme H{H}', ext.assign(ret_net=np.sign(ext.ret1) * ext[col] - COUT_D1))
comp = m4[m4.EPISODE_D1_COMPRESSION == True] if 'EPISODE_D1_COMPRESSION' in m4 else m4.iloc[0:0]
if len(comp):
    ligne('G-EXP-04', 'Cassure apres compression (sens du corps) H5', comp.assign(ret_net=np.sign(comp.ret1) * comp.fwd5 - COUT_D1))

# ---------- G-EXP-05 barrieres TP/SL (M15) ----------
B = pd.read_parquet(R / 'reports/meta_alpha/phase24/PHASE24B_M15_BARSET.parquet')
B = B[B.complete].sort_values('bar_start').reset_index(drop=True)
cl, hi, lo = B.close.values, B.high.values, B.low.values
starts = B.bar_start
GATE = pd.read_parquet(R / 'reports/meta_alpha/phase24/PHASE24C_EVENT_PREDICTIONS.parquet')
CAT = pd.read_parquet(R / 'reports/meta_alpha/phase24/PHASE24E_FIRST_PASSAGE_CATALOG.parquet')
sel_ids = set(GATE[(GATE.p_M15_TIME_ONLY > 0.5609549968307628)].event_id)
idx_of = {str(s): i for i, s in enumerate(B.bar_start)}
evenements = []
for r in CAT.itertuples():
    i = idx_of.get(str(pd.Timestamp(r.DECISION_TIMESTAMP) - pd.Timedelta(minutes=15)))
    if i is not None:
        evenements.append((i, int(r.EVENT_DIRECTION), r.event_id in sel_ids, per(r.DECISION_TIMESTAMP)))
GRILLE = [(20, 20), (30, 15), (15, 30), (40, 20), (20, 40), (30, 30)]
COUT_M15 = 2.0  # deduction forfaitaire documentee (spread+scenarios) par aller-retour, sensibilite +2


def barriere(i, d, TP, SL, H=32):
    p0 = cl[i]
    up, dn = p0 * np.exp(d * TP / 10000), p0 * np.exp(-d * SL / 10000)
    for k in range(i + 1, min(i + H + 1, len(B))):
        touche_sl = lo[k] <= dn if d > 0 else hi[k] >= dn
        touche_tp = hi[k] >= up if d > 0 else lo[k] <= up
        if touche_sl:
            return -SL
        if touche_tp:
            return TP
    return d * 10000 * np.log(cl[min(i + H, len(B) - 1)] / p0)


for pop, filt in (('selectionnes', lambda s: s), ('tous_reintegres', lambda s: True)):
    evs = [(i, d, p) for (i, d, s, p) in evenements if (s if pop == 'selectionnes' else True)]
    for TP, SL in GRILLE:
        rows = [{'periode': p, 'ret_net': barriere(i, d, TP, SL) - COUT_M15} for (i, d, p) in evs]
        ligne('G-EXP-05', f'{pop} TP{TP}/SL{SL}', pd.DataFrame(rows))

# ---------- G-EXP-06 sessions ----------
H4 = pd.read_parquet(R / 'reports/meta_alpha/phase20/PHASE20A_H4_BARSET.parquet').sort_values('bar_start')
H4['ret'] = 10000 * np.log(H4.close / H4.close.shift(1))
H4['periode'] = [per(t) for t in H4.bar_start]
H4['bloc'] = pd.cut(H4.bar_start.dt.hour, [-1, 6, 12, 16, 21, 23], labels=['00-07', '07-13', '13-17', '17-22', '22-24'])
for b, g in H4.groupby('bloc', observed=True):
    ligne('G-EXP-06', f'Derive bloc {b} (long)', g.assign(ret_net=g.ret - 1.0))
RES = pd.DataFrame(res)
RES.to_csv(OUT / 'EXPERIMENT_RESULTS.csv', index=False)
print(RES.to_string())
print('TERMINE')
