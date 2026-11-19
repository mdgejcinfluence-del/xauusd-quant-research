"""F15 SYNTHESE - verdicts sur H=60 gele uniquement (15/240 rapportes, jamais juges).
Ancres: hist = exec reel - commission 1,0 bp; BG = mid - 4,7 bp. BY famille N=6."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha/phase6')
d = pd.read_csv(R / 'f15_events/F15_EVENT_PNL.csv', parse_dates=['t_avail'])
rng = np.random.default_rng(42)
def boot_ci(x, n=10000):
    x = np.asarray(x); m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))
def by(pv):
    pv = np.asarray(pv); m = len(pv); o = np.argsort(pv); c = sum(1 / i for i in range(1, m + 1))
    adj = np.empty(m); run = 1.0
    for i in range(m - 1, -1, -1): run = min(run, pv[o[i]] * m * c / (i + 1)); adj[o[i]] = run
    return adj

res = {}; pvals = []; cles = []
for typ in ['FOMC', 'NFP', 'CPI']:
    ev = d[(d.type == typ) & (d.dec == 0) & (d.mouv_bp != 0)].sort_values('t_avail')
    for nom, dirn in [('derive', 1), ('retournement', -1)]:
        pos = dirn * np.sign(ev.mouv_bp.values)
        ex = np.where(pos > 0, ev.exec_long_60.values, ev.exec_short_60.values)
        hist = ex - 1.0
        bg = pos * ev.mid_60.values - 4.7
        lo_h, hi_h = boot_ci(hist); lo_b, hi_b = boot_ci(bg)
        t = hist.mean() / (hist.std(ddof=1) / np.sqrt(len(hist)))
        from math import erf, sqrt
        p = 1 - erf(abs(t) / sqrt(2))
        tiers = np.array_split(np.arange(len(hist)), 3)
        signes = [bool(np.sign(hist[t].mean()) == np.sign(hist.mean())) for t in tiers]
        r = {'n': int(len(ev)), 'mean_hist_bp': float(hist.mean()), 'IC95_hist': [lo_h, hi_h],
             'mean_BG_bp': float(bg.mean()), 'IC95_BG': [lo_b, hi_b], 'p': float(p),
             'signe_3tiers': signes, 'ECR_BG': float(abs(pos @ ev.mid_60.values / len(ev)) / 4.7),
             'ECR_hist': float(abs(ex.mean()) / 3.33),
             'rappel_15_hist_bp': float((np.where(pos > 0, ev.exec_long_15.values, ev.exec_short_15.values) - 1).mean()),
             'rappel_240_hist_bp': float((np.where(pos > 0, ev.exec_long_240.values, ev.exec_short_240.values) - 1).mean()),
             'spread_entree_median_bp': float(ev.spread_entree_bp.median())}
        res[f'{typ}_{nom}'] = r; pvals.append(p); cles.append(f'{typ}_{nom}')
        print(f'{typ}_{nom}', r)
padj = by(pvals)
for k, pa in zip(cles, padj):
    res[k]['p_BY'] = float(pa)
    res[k]['L1'] = bool(res[k]['IC95_hist'][0] > 0 and res[k]['IC95_BG'][0] > 0 and all(res[k]['signe_3tiers'])
                        and res[k]['ECR_BG'] >= 2 and res[k]['ECR_hist'] >= 2 and pa < 0.05)
plac = {}
for typ in ['FOMC', 'NFP', 'CPI']:
    for dec in [-30, 30]:
        ev = d[(d.type == typ) & (d.dec == dec) & (d.mouv_bp != 0)]
        if len(ev):
            pnl = np.sign(ev.mouv_bp.values) * ev.mid_60.values
            lo, hi = boot_ci(pnl)
            plac[f'{typ}_{dec:+d}j'] = {'n': int(len(ev)), 'mean_mid_bp': float(pnl.mean()), 'IC95': [lo, hi]}
res['_placebos_calendaires_derive_mid'] = plac
res['_gate_R3'] = 'TESTABLE (F15_F16_GATES.json)'; res['_alignement'] = 'v2: premier mouvement T+60s->T+5min, entree premier tick >= T+5min (v1 rejetee seq112)'
res['_succes_global'] = any(v.get('L1') for k, v in res.items() if not k.startswith('_'))
(R / 'F15_RESULTS.json').write_text(json.dumps(res, indent=1, default=str))
print('L1 passes:', [k for k, v in res.items() if isinstance(v, dict) and v.get('L1')])
print('SYNTHESE TERMINEE')
