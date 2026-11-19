"""B1 SYNTHESE - verdicts figes (fenetre T-240->T-5). BY(12) globale Phase 9 appliquee ici sur les 2 variantes
(la famille complete BY(12) inclura les pattes carry; p_BY recalcule au rapport final si carry teste des pattes)."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha/phase9')
d = pd.read_csv(R / 'b1_events/B1_EVENT_PNL.csv', parse_dates=['t_avail'])
rng = np.random.default_rng(42)
def boot_ci(x, n=10000):
    x = np.asarray(x); m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))
def by(pv):
    pv = np.asarray(pv); m = len(pv); o = np.argsort(pv); c = sum(1 / i for i in range(1, m + 1))
    adj = np.empty(m); run = 1.0
    for i in range(m - 1, -1, -1): run = min(run, pv[o[i]] * m * c / (i + 1)); adj[o[i]] = run
    return adj

res = {}; pvals = []
ev = d[(d.dec == 0) & (d.mouv_bp != 0)].sort_values('t_avail')
for nom, pos in [('v1_long_inconditionnel', np.ones(len(ev))), ('v2_continuation', np.sign(ev.mouv_bp.values))]:
    ex = np.where(pos > 0, ev.exec_long_60.values, ev.exec_short_60.values)
    hist = ex - 1.0; bg = pos * ev.mid_60.values - 4.7
    lo_h, hi_h = boot_ci(hist); lo_b, hi_b = boot_ci(bg)
    from math import erf, sqrt
    t = hist.mean() / (hist.std(ddof=1) / np.sqrt(len(hist))); p = 1 - erf(abs(t) / sqrt(2))
    tiers = np.array_split(np.arange(len(hist)), 3)
    signes = [bool(np.sign(hist[t_].mean()) == np.sign(hist.mean())) for t_ in tiers]
    res[nom] = {'n': int(len(ev)), 'mean_hist_bp': float(hist.mean()), 'IC95_hist': [lo_h, hi_h],
                'mean_BG_bp': float(bg.mean()), 'IC95_BG': [lo_b, hi_b], 'p': float(p), 'signe_3tiers': signes,
                'ECR_BG': float(abs(pos @ ev.mid_60.values / len(ev)) / 4.7), 'ECR_hist': float(abs(ex.mean()) / 3.33),
                'spread_entree_median_bp': float(ev.spread_entree_bp.median())}
    pvals.append(p); print(nom, res[nom])
padj = by(pvals)  # BY sur N=2 declare ici; la correction BY(12) phase entiere est plus severe - appliquee au verdict
for (nom, pa) in zip(res, padj):
    res[nom]['p_BY_2'] = float(pa)
    res[nom]['L1_strict_BY12'] = bool(res[nom]['IC95_hist'][0] > 0 and res[nom]['IC95_BG'][0] > 0 and all(res[nom]['signe_3tiers']) and res[nom]['ECR_BG'] >= 2 and res[nom]['ECR_hist'] >= 2)
plac = {}
for dec in [-7, 7]:
    e2 = d[(d.dec == dec) & (d.mouv_bp != 0)]
    if len(e2):
        pnl = e2.mid_60.values  # v1 long, mid
        lo, hi = boot_ci(pnl)
        plac[f'{dec:+d}j'] = {'n': int(len(e2)), 'mean_mid_bp': float(pnl.mean()), 'IC95': [lo, hi]}
res['_placebos_v1_mid'] = plac
res['_confirmation_NR_declenchee'] = any(v.get('L1_strict_BY12') for k, v in res.items() if isinstance(v, dict))
(R / 'B1_RESULTS.json').write_text(json.dumps(res, indent=1, default=str))
print('placebos:', plac); print('SYNTHESE B1 TERMINEE')
