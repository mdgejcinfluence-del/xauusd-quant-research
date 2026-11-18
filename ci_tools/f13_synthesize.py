"""F13 synthese: GATES (n, n_eff) calcules et imprimes AVANT toute agregation de performance."""
import json, pathlib
import numpy as np, pandas as pd
R = pathlib.Path('reports/meta_alpha/phase2/f13_events')
gap = pd.read_csv(R / 'F13_GAP.csv', parse_dates=['t_sunday'])
jmp = pd.read_csv(R / 'F13_JUMP.csv')
jmp['t'] = pd.to_datetime(jmp.t, utc=True, format='mixed')
def neff(x):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    if len(x) < 10: return float(len(x))
    rho = sum(np.corrcoef(x[:-k], x[k:])[0, 1] for k in range(1, 6) if len(x) > k + 5)
    return float(len(x) / max(1 + 2 * rho, 0.2))
def boot_ci(x, seed=42, B=4000):
    x = np.asarray(x, float); rng = np.random.default_rng(seed)
    ms = [rng.choice(x, len(x), replace=True).mean() for _ in range(B)]
    return float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5))
def tiers_sign(x, t):
    o = np.argsort(pd.to_datetime(t).values); xs = np.asarray(x)[o]
    return [float(np.mean(v)) for v in np.array_split(xs, 3)] if len(xs) >= 30 else []
res = {}
# ---------- GATE A/B ----------
g = gap.dropna(subset=['fade_ret_bp'])
res['GATE_AB'] = {'evenements_gap_qualifies': int(len(g)), 'n_eff_fade': round(neff(g.fade_ret_bp.values), 1),
                  'seuil_R1': 200, 'testable': bool(neff(g.fade_ret_bp.values) >= 200)}
print('GATE A/B:', res['GATE_AB'], flush=True)
if res['GATE_AB']['testable']:
    for cell, col in [('F13-A_FADE', 'fade_ret_bp'), ('F13-B_SUIVI', 'follow_ret_bp')]:
        x = g[col].values; lo, hi = boot_ci(x); ti = tiers_sign(x, g.t_sunday)
        res[cell] = {'n': int(len(x)), 'moy_bp': float(np.mean(x)), 'IC95': [lo, hi], 'tiers_bp': ti,
                     'succes': bool(np.mean(x) > 0 and lo > 0 and len(ti) == 3 and all(np.sign(v) == np.sign(np.mean(x)) for v in ti))}
else:
    res['F13-A_FADE'] = res['F13-B_SUIVI'] = {'verdict': 'NON TESTABLE (gate R1)'}
# ---------- F7 alerte (entraine 2013-2016, applique 2017+, top 5%) ----------
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
yrs = h.hour_ts.dt.year.values; ok = ~np.isnan(X).any(axis=1) & ~np.isnan(seuil)
def fit(Xt, yt, lam=1.0, iters=300):
    w = np.zeros(Xt.shape[1]); b = 0.0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(Xt @ w + b)))
        w -= 0.5 * (Xt.T @ (p - yt) / len(yt) + lam * w / len(yt)); b -= 0.5 * np.mean(p - yt)
    return w, b
tr = ok & (yrs >= 2013) & (yrs <= 2016)
mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
w, b = fit((X[tr] - mu) / sd, y[tr])
h['p_alert'] = 1 / (1 + np.exp(-(((X - mu) / sd) @ w + b)))
app = h[h.hour_ts.dt.year >= 2017]
thr = app.p_alert.quantile(0.95)
alert_hours = set(app.loc[app.p_alert >= thr, 'hour_ts'].dt.floor('h'))
jmp['hour'] = jmp.t.dt.floor('h')
jmp['alert'] = jmp.hour.isin(alert_hours)
jmp['yr'] = jmp.t.dt.year
med_sp = jmp.groupby('partition').spbp.transform('median')
p75_sp = jmp.groupby('partition').spbp.transform(lambda s: s.quantile(0.75))
# ---------- GATE C ----------
c = jmp[(jmp.yr >= 2017) & jmp.alert & (jmp.spbp <= med_sp)]
res['GATE_C'] = {'evenements': int(len(c)), 'n_eff': round(neff(c.dirori200.values), 1), 'testable': bool(neff(c.dirori200.values) >= 200)}
print('GATE C:', res['GATE_C'], flush=True)
if res['GATE_C']['testable']:
    x = c.dirori200.values; lo, hi = boot_ci(x); ti = tiers_sign(x, c.t)
    res['F13-C_ORI_F7'] = {'n': int(len(x)), 'moy_bp': float(np.mean(x)), 'IC95': [lo, hi], 'tiers_bp': ti,
                           'succes': bool(np.mean(x) > 0 and lo > 0 and len(ti) == 3 and all(np.sign(v) == np.sign(np.mean(x)) for v in ti))}
else: res['F13-C_ORI_F7'] = {'verdict': 'NON TESTABLE (gate R1)'}
# ---------- GATE D ----------
d = jmp[(jmp.yr >= 2017) & jmp.alert & (jmp.spbp <= p75_sp)]
res['GATE_D'] = {'evenements': int(len(d)), 'n_eff': round(neff(d.dirjump200.values), 1), 'testable': bool(neff(d.dirjump200.values) >= 200)}
print('GATE D:', res['GATE_D'], flush=True)
if res['GATE_D']['testable']:
    for H in ['dirjump200', 'dirjump1000']:
        x = d[H].values; lo, hi = boot_ci(x); ti = tiers_sign(x, d.t)
        res[f'F13-D_POSTSAUT_{H[-3:]}'] = {'n': int(len(x)), 'moy_bp': float(np.mean(x)), 'IC95': [lo, hi], 'tiers_bp': ti,
                                           'succes': bool(np.mean(x) > 0 and lo > 0 and len(ti) == 3 and all(np.sign(v) == np.sign(np.mean(x)) for v in ti))}
else: res['F13-D_POSTSAUT'] = {'verdict': 'NON TESTABLE (gate R1)'}
(R / 'F13_SYNTHESIS.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=1, default=str)[:2500])
