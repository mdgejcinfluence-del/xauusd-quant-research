#!/usr/bin/env python3
"""MA-ALPHA-GOLD-03 N-EXP-01..04 (preenregistrees seq423, EXPLORATORY_POST_HOC)."""
import pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research/MA-ALPHA-GOLD-03'


def per(ts):
    y = pd.Timestamp(ts).year
    return 'DEC' if y <= 2015 else ('CTL' if y <= 2017 else 'REJ')


B = pd.read_parquet(R / 'reports/meta_alpha/phase24/PHASE24B_M15_BARSET.parquet')
B = B[B.complete].sort_values('bar_start').reset_index(drop=True)
cl, hi, lo, op = B.close.values, B.high.values, B.low.values, B.open.values
sp = B.spread_median_bp.values if 'spread_median_bp' in B else np.full(len(B), np.nan)
absb = np.abs(10000 * np.log(cl / op))
q90 = np.full(len(B), np.nan)
for i in range(250, len(B)):
    fen = absb[i - 250:i]
    if np.isfinite(fen).all():
        q90[i] = np.quantile(fen, .90)
imp = [i for i in range(250, len(B) - 9) if np.isfinite(q90[i]) and absb[i] >= q90[i] and absb[i] > 0]
print('impulsions:', len(imp), '| spread median global:', round(float(np.nanmedian(sp)), 2))

# ---------- N-EXP-01 / 02 / 04 : fade brut, markouts, terciles de spread ----------
dec_mask = np.array([per(t) == 'DEC' for t in B.bar_start])
s_dec = sp[[i for i in imp if dec_mask[i]]]
t1, t2 = np.nanquantile(s_dec, [1 / 3, 2 / 3])
rows = []
for i in imp:
    d = 1 if cl[i] > op[i] else -1
    t0 = B.bar_start.iloc[i] + pd.Timedelta(minutes=15)
    ligne = {'periode': per(t0), 'spread': sp[i], 'heure': t0.hour}
    for H in (1, 2, 4, 8):
        ligne[f'brut{H}'] = -d * 10000 * np.log(cl[i + H] / cl[i])
    rows.append(ligne)
F = pd.DataFrame(rows)
F['tercile_spread'] = pd.cut(F.spread, [-np.inf, t1, t2, np.inf], labels=['SP_bas', 'SP_mid', 'SP_haut'])
F.to_csv(OUT / 'NEXP01_fade_brut.csv', index=False)
res = []
for H in (1, 2, 4, 8):
    res.append({'experience': 'N-EXP-01', 'mesure': f'Fade brut H{H} (Mid, avant couts)',
                'moyenne': round(F[f'brut{H}'].mean(), 3), 'mediane': round(F[f'brut{H}'].median(), 3),
                'part_positifs': round((F[f'brut{H}'] > 0).mean(), 3),
                'moy_DEC': round(F[F.periode == 'DEC'][f'brut{H}'].mean(), 3),
                'moy_CTL': round(F[F.periode == 'CTL'][f'brut{H}'].mean(), 3),
                'moy_REJ': round(F[F.periode == 'REJ'][f'brut{H}'].mean(), 3)})
for t, g in F.groupby('tercile_spread', observed=True):
    res.append({'experience': 'N-EXP-02', 'mesure': f'Fade brut H2 par {t} (spread median du groupe: {g.spread.median():.2f} bp)',
                'moyenne': round(g.brut2.mean(), 3), 'mediane': round(g.brut2.median(), 3),
                'part_positifs': round((g.brut2 > 0).mean(), 3),
                'moy_DEC': round(g[g.periode == 'DEC'].brut2.mean(), 3),
                'moy_CTL': round(g[g.periode == 'CTL'].brut2.mean(), 3),
                'moy_REJ': round(g[g.periode == 'REJ'].brut2.mean(), 3)})
profil = {f'barre{k}': round(F[f'brut{k}'].mean(), 3) for k in (1, 2, 4, 8)}
print('profil markout moyen (brut cumule):', profil)

# ---------- N-EXP-03 : prime de variance, constructions multiples ----------
G = pd.read_parquet(R / 'reports/meta_alpha/phase25/PHASE25B_GVZ_DATA.parquet').sort_values('date')
D1 = pd.read_parquet(R / 'reports/meta_alpha/phase21/PHASE21A_D1_BARSET.parquet').sort_values('jour')
m = G.merge(D1[['jour', 'close']], left_on='date', right_on='jour', how='inner').sort_values('date').reset_index(drop=True)
r1 = 10000 * np.log(m.close / m.close.shift(1))
m['RV20_suiv'] = r1.shift(-1).rolling(20).std().shift(-19) * np.sqrt(252) / 100
m['periode'] = [per(t) for t in m.date]
m = m.dropna(subset=['RV20_suiv']).copy()
m['ecart'] = m.GVZCLS - m.RV20_suiv
m['ecart_pct'] = 100 * m.ecart / m.GVZCLS
for nom, g in (('chevauchante (quotidienne)', m), ('non-chevauchante (tous les 20 j)', m.iloc[::20]),
               ('sans les 10 plus grands sauts RV', m.nsmallest(len(m) - 10, 'RV20_suiv'))):
    res.append({'experience': 'N-EXP-03', 'mesure': f'Ecart IV-RV {nom}',
                'moyenne': round(g.ecart.mean(), 2), 'mediane': round(g.ecart.median(), 2),
                'part_positifs': round((g.RV20_suiv > g.GVZCLS).mean(), 3),
                'moy_DEC': round(g[g.periode == 'DEC'].ecart.median(), 2),
                'moy_CTL': round(g[g.periode == 'CTL'].ecart.median(), 2),
                'moy_REJ': round(g[g.periode == 'REJ'].ecart.median(), 2)})
m[['date', 'GVZCLS', 'RV20_suiv', 'ecart', 'ecart_pct', 'periode']].to_csv(OUT / 'NEXP03_variance_premium.csv', index=False)
RES = pd.DataFrame(res)
RES.to_csv(OUT / 'MONETIZATION_EXPERIMENT_RESULTS.csv', index=False)
print(RES.to_string())
print('TERMINE')
