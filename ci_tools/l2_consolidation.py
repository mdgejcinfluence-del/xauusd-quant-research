"""L2 hors budget (instruction Phase 3 sec.4): F3 et F7 sous leurs prereg Phase 2.
F3: predictions deja rolling-origin out-of-fold (fenetre 500 j, passe strict) = walk-forward;
    PBO/DSR non applicables a une famille sans variante concurrente (N=1 declare) - substitut consigne: victoires QLIKE par bloc 5/5 + MZ.
F7: forward-chaining annuel (train annees < Y, test Y), embargo par construction annuelle."""
import json, pathlib
import numpy as np, pandas as pd
out = {}
# ---- F3 L2
f3 = json.loads(pathlib.Path('reports/meta_alpha/phase2/f3_har/F3_RESULTS.json').read_text())
blocs = f3['MZ_recent_blocs']
out['F3_L2'] = {'walk_forward': 'rolling origin 500 j, passe strict (deja out-of-fold)',
                'blocs_QLIKE_gagnes': int(sum(1 for b in blocs if b['QLIKE_HAR'] < b['QLIKE_NAIF'])),
                'blocs_total': len(blocs), 'R2_MZ_median': f3['R2_MZ_median_recent'],
                'PBO_DSR': 'non applicables (famille N=1, aucun parametrage concurrent; pas de selection a deflater)',
                'statut': 'CANDIDATE VALIDEE L2 (adaptation documentee)' if all(b['QLIKE_HAR'] < b['QLIKE_NAIF'] for b in blocs) else 'RETOUR DOCUMENTE'}
# ---- F7 L2 forward-chaining
h = pd.read_csv('reports/meta_alpha/vol_hourly/PARTITION_HOUR_TS.csv', parse_dates=['hour_ts']).sort_values('hour_ts').reset_index(drop=True)
h['ret_bp'] = h.ret_hour * 10000; h['hr'] = h.hour_ts.dt.hour
def cq(x, W=500):
    import bisect
    o = [np.nan] * len(x); win = []
    for i, v in enumerate(x):
        if len(win) >= 100: o[i] = bisect.bisect_left(win, v) / len(win)
        bisect.insort(win, v)
        if len(win) > W: win.pop(0)
    return np.array(o)
rv = np.sqrt(h.sumsq_rbp.values)
seuil = pd.Series(np.abs(h.ret_bp.values)).rolling(2000, min_periods=200).quantile(0.9).values
y = (np.abs(h.ret_bp.shift(-1).values) > seuil).astype(float)
X = np.column_stack([cq(rv), cq(h.spread_bp.values), cq(h.n.astype(float).values), np.abs(h.ret_bp.values),
                     np.sin(2 * np.pi * h.hr.values / 24), np.cos(2 * np.pi * h.hr.values / 24)])
yrs = h.hour_ts.dt.year.values
ok = ~np.isnan(X).any(axis=1) & ~np.isnan(seuil)
def fit(Xt, yt, lam=1.0, iters=300):
    w = np.zeros(Xt.shape[1]); b = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(Xt @ w + b)))
        w -= 0.5 * (Xt.T @ (p - yt) / len(yt) + lam * w / len(yt)); b -= 0.5 * np.mean(p - yt)
    return w, b
def auc(pred, yt):
    o = np.argsort(pred); r = np.empty(len(o)); r[o] = np.arange(1, len(o) + 1)
    pos = yt == 1
    return float((r[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum()))
res = {}
for Y in [2017, 2018, 2019]:
    tr = ok & (yrs < Y) & (yrs >= 2013); te = ok & (yrs == Y)
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
    w, b = fit((X[tr] - mu) / sd, y[tr])
    pred = 1 / (1 + np.exp(-(((X[te] - mu) / sd) @ w + b)))
    res[str(Y)] = {'AUC': auc(pred, y[te]), 'n': int(te.sum()), 'taux_saut': float(y[te].mean())}
aucs = [v['AUC'] for v in res.values()]
out['F7_L2'] = {'forward_chaining_annuel': res, 'AUC_min': float(min(aucs)), 'stabilite': '3/3 annees > 0.60' if all(a > 0.60 for a in aucs) else 'instable',
                'statut': 'CANDIDATE VALIDEE L2' if all(a > 0.60 for a in aucs) else 'RETOUR DOCUMENTE'}
pathlib.Path('reports/meta_alpha/phase2/L2_RESULTS.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
