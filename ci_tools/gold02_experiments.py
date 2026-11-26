#!/usr/bin/env python3
"""MA-ALPHA-GOLD-02 M-EXP-01..04 (preenregistrees seq421, EXPLORATORY_POST_HOC)."""
import pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research/MA-ALPHA-GOLD-02'


def per(ts):
    y = pd.Timestamp(ts).year
    return 'DEC' if y <= 2015 else ('CTL' if y <= 2017 else 'REJ')


res = []


def ligne(exp, regle, g, col='ret_net'):
    r = {'experience': exp, 'regle': regle, 'n': len(g)}
    for p in ('DEC', 'CTL', 'REJ'):
        s = g[g.periode == p][col] if 'periode' in g else pd.Series(dtype=float)
        r[f'moy_{p}'] = round(s.mean(), 2) if len(s) else np.nan
    r['moyenne'] = round(g[col].mean(), 2) if len(g) else np.nan
    r['mediane'] = round(g[col].median(), 2) if len(g) else np.nan
    res.append(r)


B = pd.read_parquet(R / 'reports/meta_alpha/phase24/PHASE24B_M15_BARSET.parquet')
B = B[B.complete].sort_values('bar_start').reset_index(drop=True)
cl, hi, lo, op = B.close.values, B.high.values, B.low.values, B.open.values
absb = np.abs(10000 * np.log(cl / op))
q90 = np.full(len(B), np.nan)
for i in range(250, len(B)):
    fen = absb[i - 250:i]
    if np.isfinite(fen).all():
        q90[i] = np.quantile(fen, .90)
imp = [i for i in range(250, len(B)) if np.isfinite(q90[i]) and absb[i] >= q90[i] and absb[i] > 0]
SPREAD_M15 = float(B.spread_median_bp.median()) if 'spread_median_bp' in B else 2.0
print('spread median M15 (bp):', round(SPREAD_M15, 2), '| impulsions:', len(imp))

# M-EXP-01 fade tres court terme
for portee, filt in (('toutes_heures', lambda h: True), ('horloge_08_16', lambda h: 8 <= h < 16)):
    for H in (1, 2, 4):
        rows = []
        for i in imp:
            t0 = B.bar_start.iloc[i] + pd.Timedelta(minutes=15)
            if not filt(t0.hour) or i + H >= len(B):
                continue
            d = 1 if cl[i] > op[i] else -1
            rows.append({'periode': per(t0), 'ret_net': -d * 10000 * np.log(cl[i + H] / cl[i]) - SPREAD_M15,
                         'ret_net_p1': -d * 10000 * np.log(cl[i + H] / cl[i]) - SPREAD_M15 - 2})
        g = pd.DataFrame(rows)
        ligne('M-EXP-01', f'Fade impulsion H{H} {portee}', g)
        ligne('M-EXP-01', f'Fade impulsion H{H} {portee} (cout+1/cote)', g, col='ret_net_p1')

# M-EXP-02 grille: episodes quotidiens 08:00
B['jour'] = B.bar_start.dt.date
B['heure'] = B.bar_start.dt.hour
resultats = []
for jour, g in B.groupby('jour'):
    g = g.reset_index(drop=True)
    debut = g[g.heure == 8]
    if not len(debut) or len(g) < 40:
        continue
    i0 = int(debut.index[0])
    p_entree = [g.close.iloc[i0]]
    prix = g.close.iloc[i0]
    flottant_min, realise = 0.0, None
    for k in range(i0 + 1, min(i0 + 129, len(g))):
        px = g.close.iloc[k]
        while len(p_entree) < 6 and px <= p_entree[-1] * np.exp(-25 / 10000):
            p_entree.append(px)
        pm = np.mean(p_entree)
        pnl_lat = len(p_entree) * 10000 * np.log(px / pm)
        flottant_min = min(flottant_min, pnl_lat)
        if px >= pm:
            realise = len(p_entree) * 10000 * np.log(px / pm) - len(p_entree) * SPREAD_M15
            break
    if realise is None:
        px = g.close.iloc[min(i0 + 128, len(g) - 1)]
        pm = np.mean(p_entree)
        realise = len(p_entree) * 10000 * np.log(px / pm) - len(p_entree) * SPREAD_M15
    resultats.append({'jour': str(jour), 'periode': per(g.bar_start.iloc[i0]), 'pnl': realise,
                      'perte_flottante_max_bp_x_unites': flottant_min, 'nb_entrees': len(p_entree)})
GR = pd.DataFrame(resultats)
GR.to_csv(OUT / 'MEXP02_grid_episodes.csv', index=False)
resume = {'episodes': len(GR), 'pnl_median': round(GR.pnl.median(), 1), 'pnl_moyen': round(GR.pnl.mean(), 1),
          'part_gagnants': round((GR.pnl > 0).mean(), 3),
          'perte_flottante_mediane': round(GR.perte_flottante_max_bp_x_unites.median(), 0),
          'perte_flottante_p95': round(GR.perte_flottante_max_bp_x_unites.quantile(.05), 0),
          'perte_flottante_pire': round(GR.perte_flottante_max_bp_x_unites.min(), 0),
          'ruine_buffer500_%': round(100 * (GR.perte_flottante_max_bp_x_unites <= -500).mean(), 1),
          'ruine_buffer1000_%': round(100 * (GR.perte_flottante_max_bp_x_unites <= -1000).mean(), 1),
          'ruine_buffer2000_%': round(100 * (GR.perte_flottante_max_bp_x_unites <= -2000).mean(), 1)}
print(resume)
pd.DataFrame([resume]).to_csv(OUT / 'MEXP02_grid_summary.csv', index=False)

# M-EXP-03 prime de variance
G = pd.read_parquet(R / 'reports/meta_alpha/phase25/PHASE25B_GVZ_DATA.parquet').sort_values('date')
D1 = pd.read_parquet(R / 'reports/meta_alpha/phase21/PHASE21A_D1_BARSET.parquet').sort_values('jour')
m = G.merge(D1[['jour', 'close']], left_on='date', right_on='jour', how='inner').sort_values('date')
r1 = 10000 * np.log(m.close / m.close.shift(1))
m['RV20_suivante'] = r1.shift(-1).rolling(20).std().shift(-19) * np.sqrt(252) / 100
m['periode'] = [per(t) for t in m.date]
m = m.dropna(subset=['RV20_suivante'])
m['prime'] = m.GVZCLS - m.RV20_suivante
ligne('M-EXP-03', 'Prime IV-RV suivante (mesure, pas strategie)', m.assign(ret_net=m.prime), col='ret_net')
print('part RV > IV:', round((m.RV20_suivante > m.GVZCLS).mean(), 3), '| prime mediane:', round(m.prime.median(), 2))
m[['date', 'GVZCLS', 'RV20_suivante', 'prime', 'periode']].to_csv(OUT / 'MEXP03_variance_premium.csv', index=False)

# M-EXP-04 exposition selective par bloc
H4 = pd.read_parquet(R / 'reports/meta_alpha/phase20/PHASE20A_H4_BARSET.parquet').sort_values('bar_start')
H4['ret'] = 10000 * np.log(H4.close / H4.close.shift(1))
H4['periode'] = [per(t) for t in H4.bar_start]
SP_H4 = float(H4.spread_median_bp.median())
blocs = {'00-07': (0, 7), '07-13': (7, 13), '13-17': (13, 17), '17-22': (17, 22), '22-24': (22, 24)}
for nom, (a, b) in blocs.items():
    g = H4[(H4.bar_start.dt.hour >= a) & (H4.bar_start.dt.hour < b)].copy()
    jours = g.groupby(g.bar_start.dt.date).ret.sum().reset_index()
    jours['periode'] = [per(t) for t in jours.bar_start]
    jours['ret_net'] = jours.ret - SP_H4
    ligne('M-EXP-04', f'Hold-only bloc {nom} (net 1 AR/jour)', jours)

RES = pd.DataFrame(res)
RES.to_csv(OUT / 'EXPERIMENT_RESULTS.csv', index=False)
print(RES.to_string())
print('TERMINE')
