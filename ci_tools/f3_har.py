"""F3 HAR-RV local sur serie horaire existante. Aucun nouvel acces aux donnees brutes."""
import json, pathlib
import numpy as np, pandas as pd
R = pathlib.Path('reports/meta_alpha/phase2/f3_har'); R.mkdir(parents=True, exist_ok=True)
df = pd.read_csv('reports/meta_alpha/vol_hourly/PARTITION_HOUR_TS.csv', parse_dates=['hour_ts']).sort_values('hour_ts')
df['day'] = df.hour_ts.dt.floor('D')
day = df.groupby('day').agg(rv=('sumsq_rbp', 'sum'), hours=('n', 'size')).reset_index()
day = day[day.hours >= 12].reset_index(drop=True)  # jours de flux substantiels uniquement
rv = np.sqrt(day.rv.values)  # volatilite journaliere realisee (bp)
n = len(rv)
X = np.column_stack([np.ones(n), rv, pd.Series(rv).rolling(5).mean().values, pd.Series(rv).rolling(22).mean().values])
y = rv.copy()
pred_har = np.full(n, np.nan); pred_naive = np.full(n, np.nan)
WIN = 500
for t in range(max(WIN, 22), n - 1):
    # paires d'entrainement (X[s], y[s+1]) pour s+1 <= t : passe strict
    sidx = np.arange(22, t)
    m = ~np.isnan(X[sidx]).any(axis=1)
    sidx = sidx[m][-WIN:]
    beta, *_ = np.linalg.lstsq(X[sidx], y[sidx + 1], rcond=None)
    pred_har[t + 1] = X[t] @ beta
    pred_naive[t + 1] = rv[t]
ok = ~np.isnan(pred_har) & (rv > 0)
def qlike(p, a): return float(np.mean(a / p - np.log(a / p) - 1))
recent = (day.day.dt.year.values >= 2016) & ok
res = {'jours': int(n), 'jours_evalues': int(ok.sum()),
       'QLIKE_HAR_IS': qlike(pred_har[ok], rv[ok]), 'QLIKE_NAIF_IS': qlike(pred_naive[ok], rv[ok]),
       'QLIKE_HAR_recent': qlike(pred_har[recent], rv[recent]), 'QLIKE_NAIF_recent': qlike(pred_naive[recent], rv[recent])}
# Mincer-Zarnowitz recent par 5 blocs
idx = np.where(recent)[0]; blocs = np.array_split(idx, 5); mz = []
for b in blocs:
    A = np.column_stack([np.ones(len(b)), pred_har[b]])
    beta, *_ = np.linalg.lstsq(A, rv[b], rcond=None)
    fit = A @ beta; ss = 1 - np.sum((rv[b] - fit) ** 2) / np.sum((rv[b] - rv[b].mean()) ** 2)
    mz.append({'alpha': float(beta[0]), 'beta': float(beta[1]), 'R2': float(ss), 'QLIKE_HAR': qlike(pred_har[b], rv[b]), 'QLIKE_NAIF': qlike(pred_naive[b], rv[b])})
res['MZ_recent_blocs'] = mz
res['R2_MZ_median_recent'] = float(np.median([b['R2'] for b in mz]))
res['succes_gele'] = bool(res['QLIKE_HAR_recent'] < res['QLIKE_NAIF_recent'] and res['R2_MZ_median_recent'] > 0.15)
res['verdict'] = 'SUCCES GELE (F3 = composant de gestion qualifie L1)' if res['succes_gele'] else 'CRITERE NON ATTEINT'
(R / 'F3_RESULTS.json').write_text(json.dumps(res, indent=1))
day.assign(pred_har=pred_har, pred_naive=pred_naive).to_csv(R / 'F3_DAILY_PRED.csv', index=False)
print(json.dumps(res, indent=1))
