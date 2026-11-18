"""F5 + F7 locaux sur serie horaire IS existante. Aucun acces donnees brutes/OOS."""
import json, pathlib
import numpy as np, pandas as pd
h = pd.read_csv('reports/meta_alpha/vol_hourly/PARTITION_HOUR_TS.csv', parse_dates=['hour_ts']).sort_values('hour_ts').reset_index(drop=True)
h['ret_bp'] = h.ret_hour * 10000
h['fwd'] = h.ret_bp.shift(-1)
h['hr'] = h.hour_ts.dt.hour; h['dow'] = h.hour_ts.dt.dayofweek
recent = h[h.hour_ts.dt.year >= 2016]
# ---------- F5 ----------
med_hr = recent.groupby('hr').ret_bp.transform('median')
des = recent.fwd - recent.groupby('hr').fwd.transform('median')
tab = des.groupby([recent.dow, recent.hr]).agg(['mean', 'count']).reset_index()
tab.columns = ['dow', 'hr', 'moy', 'n']
top = tab.reindex(tab.moy.abs().sort_values(ascending=False).index).head(8)
# stabilite signe 3 tiers sur la meilleure cellule
best = top.iloc[0]
cells_r = recent[(recent.dow == best.dow) & (recent.hr == best.hr)]
vals = (cells_r.fwd - cells_r.groupby('hr').fwd.transform('median')).values
tiers = [float(np.nanmean(x)) for x in np.array_split(vals, 3)] if len(vals) >= 30 else []
f5 = {'top_cellules': top.round(3).to_dict('records'),
      'meilleure_cellule': {'dow': int(best.dow), 'heure': int(best.hr), 'moy_bp': float(best.moy), 'n': int(best.n)},
      'stabilite_3tiers_bp': tiers,
      'succes_gele': bool(abs(best.moy) >= 0.5 and len(tiers) == 3 and all(np.sign(t) == np.sign(best.moy) for t in tiers))}
pathlib.Path('reports/meta_alpha/phase2/f5_season').mkdir(exist_ok=True)
pathlib.Path('reports/meta_alpha/phase2/f5_season/F5_RESULTS.json').write_text(json.dumps(f5, indent=1))
# ---------- F7 ----------
def cq(x, W=500):
    import bisect
    out = [np.nan] * len(x); win = []
    for i, v in enumerate(x):
        if len(win) >= 100: out[i] = bisect.bisect_left(win, v) / len(win)
        bisect.insort(win, v)
        if len(win) > W: win.pop(0)
    return np.array(out)
rv = np.sqrt(h.sumsq_rbp.values)
q90 = cq(np.abs(h.ret_bp.values), W=2000)  # quantile causal approx de |ret| courant (rang)
seuil = pd.Series(np.abs(h.ret_bp.values)).rolling(2000, min_periods=200).quantile(0.9).values
y = (np.abs(h.ret_bp.shift(-1).values) > seuil).astype(float)
feat = np.column_stack([cq(rv), cq(h.spread_bp.values), cq(h.n.astype(float).values), np.abs(h.ret_bp.values),
                        np.sin(2 * np.pi * h.hr.values / 24), np.cos(2 * np.pi * h.hr.values / 24)])
X = feat; ok = ~np.isnan(X).any(axis=1) & ~np.isnan(y) & ~np.isnan(seuil)
X, yv, yrs = X[ok], y[ok], h.hour_ts.dt.year.values[ok]
rec = yrs >= 2016; X, yv = X[rec], yv[rec]
mu, sd = X.mean(0), X.std(0) + 1e-9; Xs = (X - mu) / sd
def fit_logreg(Xt, yt, lam=1.0, iters=300):
    w = np.zeros(Xt.shape[1]); b = 0.0
    for it in range(iters):
        z = Xt @ w + b; p = 1 / (1 + np.exp(-z))
        g = Xt.T @ (p - yt) / len(yt) + lam * w / len(yt); gb = np.mean(p - yt)
        w -= 0.5 * g; b -= 0.5 * gb
    return w, b
pred = np.full(len(yv), np.nan); folds = np.array_split(np.arange(len(yv)), 5)
for k, te in enumerate(folds):
    tr = np.concatenate([f for j, f in enumerate(folds) if j != k])
    tr = tr[(tr < te.min() - 24) | (tr > te.max() + 24)]  # purge/embargo 24 h autour du pli
    w, b = fit_logreg(Xs[tr], yv[tr]); pred[te] = 1 / (1 + np.exp(-(Xs[te] @ w + b)))
m = ~np.isnan(pred)
# AUC par rangs
order = np.argsort(pred[m]); ranks = np.empty(len(order)); ranks[order] = np.arange(1, len(order) + 1)
pos = yv[m] == 1; auc = float((ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum()))
k5 = max(1, int(0.05 * m.sum())); topidx = np.argsort(pred[m])[-k5:]
lift = float(yv[m][topidx].mean() / yv[m].mean())
f7 = {'n_recent': int(m.sum()), 'taux_base_saut': float(yv[m].mean()), 'AUC_oof': auc, 'lift_top5pct': lift,
      'succes_gele': bool(auc >= 0.60 and lift >= 2.0)}
pathlib.Path('reports/meta_alpha/phase2/f7_jumps').mkdir(exist_ok=True)
pathlib.Path('reports/meta_alpha/phase2/f7_jumps/F7_RESULTS.json').write_text(json.dumps(f7, indent=1))
print('F5', json.dumps(f5)[:500]); print('F7', f7)
