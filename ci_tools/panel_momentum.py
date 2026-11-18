"""PANEL momentum F10/F11 - IS panel <= 2014-12-31 FAIL-CLOSED. OOS/HOLDOUT jamais lus par le moteur."""
import json, pathlib, sys, itertools
import numpy as np, pandas as pd
from math import erf, sqrt

R = pathlib.Path('reports/meta_alpha/panel')
IS_END = pd.Timestamp('2014-12-31')
mat = pd.read_csv(R / 'PANEL_PRICES.csv', parse_dates=['date']).set_index('date').sort_index()
assert mat.index.max() > IS_END  # le fichier certifie contient plus; le moteur tranche
mat = mat.loc[:IS_END]
man = json.loads((R / 'PANEL_MANIFEST.json').read_text())
UNIV = [t for t, v in man['fichiers'].items() if v['debut'] <= '1999-12-31']
px = mat[UNIV]
ret = px.pct_change()
EVAL0 = pd.Timestamp('2000-01-01')
sig_ewma = ret.ewm(alpha=0.06, adjust=False).std() * sqrt(252)
rv = ret ** 2
sig_har = np.sqrt(0.5 * rv.rolling(5).mean() + 0.5 * rv.rolling(22).mean()) * sqrt(252)
COST = 0.0002  # 2 bp par cote, table gelee
CLASS = {}
for t in UNIV:
    CLASS[t] = ('metaux' if t in ['GC','SI','HG','PL','PA'] else
                'energie' if t in ['CL','NG','HO','RB'] else
                'indices' if t in ['ES','YM','MD','FDAX','FCE','HSI','TF','EMA','Z'] else
                'taux' if t in ['TY','FV','TU','FGBL'] else
                'fx' if t in ['AD','BP','EC','DX','B'] else 'agri_autres')

def norm_cdf(x): return 0.5 * (1 + erf(x / sqrt(2)))
def inv_cdf(p):
    # Acklam approx
    a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00]
    b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01]
    c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00]
    d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00]
    plow=0.02425; phigh=1-plow
    if p<plow: q=sqrt(-2*np.log(p)); return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p>phigh: q=sqrt(-2*np.log(1-p)); return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q=p-0.5; r=q*q; return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

def scale_to_vol(w, sig_row, target=0.10):
    w = w.copy(); act = ~np.isnan(w) & (sig_row > 0)
    if act.sum() == 0: return w * 0
    pv = np.sqrt(np.sum((np.nan_to_num(w[act]) * sig_row[act]) ** 2))
    return w * (target / pv) if pv > 0 else w * 0

def run_variant(kind, L, mode, mode2, cost_mult=1.0, shuffle=False, inverse=False, seed=42):
    dates = px.index; pos = pd.DataFrame(0.0, index=dates, columns=UNIV); cur = pd.Series(0.0, index=UNIV)
    rng = np.random.default_rng(seed)
    rets_sig = px / px.shift(L) - 1
    reb = [i for i in range(len(dates)) if dates[i] >= EVAL0 and i % 5 == 0]
    turnover = pd.Series(0.0, index=dates)
    for i in reb:
        s = rets_sig.iloc[i].dropna(); sg = sig_ewma.iloc[i]
        if len(s) < 10: continue
        w = pd.Series(0.0, index=UNIV)
        if kind == 'F10':
            r = s.rank(pct=True)
            if shuffle: r = pd.Series(rng.permutation(r.values), index=r.index)
            q = 0.2 if mode == 'quintile' else 1/3
            side = pd.Series(0.0, index=s.index); side[r >= 1 - q] = 1; side[r <= q] = -1
            if inverse: side = -side
            base = side / sg[s.index] if mode2 == 'riskparity' else side
            w[s.index] = base
            w = w / w.abs().sum() if w.abs().sum() > 0 else w
        else:
            side = np.sign(s)
            if inverse: side = -side
            sgx = (sig_ewma if mode == 'ewma' else sig_har).iloc[i]
            n_act = max(int((side != 0).sum()), 1)
            base = side * (0.10 / sqrt(n_act)) / sgx[s.index]
            w[s.index] = base.fillna(0)
            cap = float(mode2)
            for cl in set(CLASS.values()):
                mem = [t for t in UNIV if CLASS[t] == cl]
                gross_cl = w[mem].abs().sum(); gross_tot = w.abs().sum()
                if gross_tot > 0 and gross_cl / gross_tot > cap: w[mem] *= (cap * gross_tot / gross_cl)
        w = scale_to_vol(w, sg if kind == 'F10' else (sig_ewma.iloc[i]))
        turnover.iloc[i] = (w - cur).abs().sum()
        cur = w; pos.iloc[i] = cur
    pos = pos.ffill().fillna(0)
    pnl = (pos.shift(1) * ret).sum(axis=1) - turnover * COST * cost_mult
    return pnl.loc[EVAL0:]

def sharpe(x): x = x.dropna(); return float(x.mean() / x.std() * sqrt(252)) if x.std() > 0 else 0.0
def bloc_scores(pnl, L):
    idx = pnl.index; blocs = np.array_split(np.arange(len(idx)), 5); out = []
    for b in blocs:
        seg = pnl.iloc[b][min(L, 252):] if len(b) > min(L, 252) + 30 else pnl.iloc[b]
        out.append(sharpe(seg))
    return out
def years_pos(pnl):
    a = pnl.groupby(pnl.index.year).apply(lambda x: (1 + x).prod() - 1)
    return float((a > 0).mean()), a.round(4).to_dict()
def dsr(variant_pnls, best_pnl):
    SRs = np.array([sharpe(v) for v in variant_pnls]); N = len(SRs)
    x = best_pnl.dropna(); T = len(x); sr_d = x.mean() / x.std()
    V = np.var(SRs / sqrt(252) * sqrt(252)) / 252  # variance des SR journaliers approx via annuels/252
    Vd = np.var([v.mean() / v.std() for v in variant_pnls])
    sr_star = sqrt(Vd) * ((1 - 0.5772156649) * inv_cdf(1 - 1 / N) + 0.5772156649 * inv_cdf(1 - 1 / (N * np.e)))
    sk = float(x.skew()); ku = float(x.kurt()) + 3
    return float(norm_cdf((sr_d - sr_star) * sqrt(T - 1) / sqrt(1 - sk * sr_d + (ku - 1) / 4 * sr_d ** 2))), float(sr_star * sqrt(252))
def pbo(variant_pnls, seed=42, ncomb=1500):
    M = pd.concat(variant_pnls, axis=1).dropna()
    blocs = np.array_split(np.arange(len(M)), 16)
    B = np.array([[sharpe(M.iloc[b, j]) for j in range(M.shape[1])] for b in blocs])
    rng = np.random.default_rng(seed); cnt = 0; tot = 0
    for _ in range(ncomb):
        tr = rng.choice(16, 8, replace=False); te = np.array([i for i in range(16) if i not in tr])
        best = np.argmax(B[tr].mean(0)); ranks = B[te].mean(0)
        pct = (ranks < ranks[best]).mean(); tot += 1; cnt += (pct <= 0.5)
    return float(cnt / tot)

def main(kind):
    if kind == 'F10':
        grid = [(L, c, w) for L in [21, 63, 126, 252] for c in ['quintile', 'tercile'] for w in ['riskparity', 'equal']]
    else:
        grid = [(L, v, c) for L in [63, 126, 252] for v in ['ewma', 'har'] for c in ['0.2', '0.3']]
    pnls = {}; meta = {}
    for g in grid:
        p = run_variant(kind, g[0], g[1], g[2]); pnls[str(g)] = p
        yp, _ = years_pos(p)
        meta[str(g)] = {'sharpe_net': sharpe(p), 'sharpe_stress2': sharpe(run_variant(kind, g[0], g[1], g[2], cost_mult=2.0)),
                        'annees_pos': yp, 'blocs': [round(x, 3) for x in bloc_scores(p, g[0])]}
    best = max(meta, key=lambda k: meta[k]['sharpe_net'])
    bl = eval(best)
    d, sr_star = dsr(list(pnls.values()), pnls[best]); pb = pbo(list(pnls.values()))
    inv = sharpe(run_variant(kind, bl[0], bl[1], bl[2], inverse=True))
    shf = sharpe(run_variant(kind, bl[0], bl[1], bl[2], shuffle=True)) if kind == 'F10' else None
    succ = bool(meta[best]['sharpe_net'] >= 0.8 and meta[best]['annees_pos'] >= 0.65 and d >= 0.95 and pb < 0.20 and meta[best]['sharpe_stress2'] > 0)
    out = {'famille': kind, 'n_essais': len(grid), 'variantes': meta, 'meilleure': best, 'DSR': d, 'SR_etoile_ann': sr_star,
           'PBO': pb, 'placebo_cote_sharpe_inverse': inv, 'placebo_rangs_melanges': shf,
           'succes_gele_L1': succ,
           'criteres': 'Sharpe>=0.8, annees>=65%, DSR>=0.95, PBO<0.20, stress2>0'}
    (R / f'{kind}_RESULTS.json').write_text(json.dumps(out, indent=1))
    pnls[best].rename('pnl').to_csv(R / f'{kind}_BEST_DAILY.csv')
    print(json.dumps({'famille': kind, 'meilleure': best, 'meta_best': meta[best], 'DSR': round(d, 4), 'PBO': round(pb, 3),
                      'placebo_inverse': round(inv, 3), 'placebo_shuffle': (round(shf, 3) if shf is not None else None), 'SUCCES': succ}, indent=1))

if __name__ == '__main__': main(sys.argv[1])
