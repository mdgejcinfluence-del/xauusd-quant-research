"""F14 ETAPE A - INGENIERIE HORS BUDGET (0 essai): alignement available_at_utc, deux vitesses,
trois portes par driver, gate R3. Aucune variante du modele n'est testee ici.
Perimetre IS strict: decision jour d a 22:00 UTC, drivers pris a available_at_utc <= decision
ET <= 2020-01-20T09:36:27. Prix or: DAILY_VOL (corpus tick, clotures reconstruites par chainage)."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase6'; OUT.mkdir(parents=True, exist_ok=True)
IS_END = pd.Timestamp('2020-01-20 09:36:27', tz='UTC')
P = R / 'exogenous/data_is'

# ---------- prix or journalier (chainage des segments DAILY_VOL) ----------
dv = pd.read_csv(R / 'vol_models/DAILY_VOL.csv', parse_dates=['date'])
dv = dv[dv.date <= '2020-01-20'].sort_values(['date', 'partition'])
g = dv.groupby('date').apply(lambda x: np.prod(1 + x.ret_day) - 1, include_groups=False)
gold = pd.DataFrame({'date': g.index, 'ret': g.values})
gold['lnP'] = np.log1p(gold.ret).cumsum()
gold['decision'] = pd.to_datetime(gold.date, utc=True) + pd.Timedelta(hours=22)
gold = gold[gold.decision <= IS_END].reset_index(drop=True)

# ---------- drivers alignes par available_at_utc (asof sur l'instant de decision) ----------
def load(nom, col='value'):
    d = pd.read_parquet(P / f'{nom}.parquet')[['available_at_utc', col]].dropna().sort_values('available_at_utc')
    return d[d.available_at_utc <= IS_END]
def asof(d, colname):
    m = pd.merge_asof(gold[['decision']], d.rename(columns={'value': colname, d.columns[1]: colname}) if False else d,
                      left_on='decision', right_on='available_at_utc', direction='backward')
    return m[colname].values
def asof_named(nom, series):
    d = pd.DataFrame({'available_at_utc': series.index, 'v': series.values}).sort_values('available_at_utc')
    m = pd.merge_asof(gold[['decision']], d, left_on='decision', right_on='available_at_utc', direction='backward')
    return m['v'].values

gold['DFII10'] = asof_named('fred_dfii10_officiel', load('fred_dfii10_officiel').set_index('available_at_utc')['value'])
gold['dollar'] = asof_named('fred_dollar_broad', load('fred_dollar_broad').set_index('available_at_utc')['value'])
gold['GVZ'] = asof_named('fred_gvz_officiel', load('fred_gvz_officiel').set_index('available_at_utc')['value'])
gold['WTI'] = asof_named('fred_wti', load('fred_wti').set_index('available_at_utc')['value'])
gc = load('comex_gc_ohlcv', 'Volume'); gold['volume_GC'] = asof_named('gc', gc.set_index('available_at_utc')['Volume'])
cot = pd.read_parquet(P / 'cftc_cot_gold_disagg.parquet')
cot = cot[cot.available_at_utc <= IS_END]
cotnet = (cot.m_money_positions_long_all - cot.m_money_positions_short_all) / cot.open_interest_all
gold['COT_net'] = asof_named('cot', pd.Series(cotnet.values, index=cot.available_at_utc))

DRIVERS = ['DFII10', 'dollar', 'COT_net', 'GVZ', 'volume_GC', 'WTI']
for d in DRIVERS:
    s = pd.Series(gold[d].astype(float))
    mu = s.rolling(28, min_periods=20).mean(); sd = s.rolling(28, min_periods=20).std()
    gold[f'z_{d}'] = (s - mu) / sd
gold.to_parquet(OUT / 'F14_DAILY_ALIGNED.parquet', index=False)
print(f'jours alignes: {len(gold)} ({gold.date.min()} -> {gold.date.max()})')

# ---------- mesures: deux vitesses + test du bus (par driver, placebos -30/-60/-90) ----------
ret = gold.ret.values; lnP = gold.lnP.values
def reponses(z, decal=0):
    zz = np.roll(z, decal) if decal else z
    chocs = np.where(np.abs(zz) > 2)[0]
    chocs = chocs[(chocs > 30) & (chocs < len(ret) - 25)]
    if len(chocs) < 15: return None, 0
    sgn = np.sign(zz[chocs])
    cum = {}
    for h in [0, 1, 2, 3, 5, 10, 15, 21]:
        cum[h] = float(np.mean([sgn[k] * (lnP[min(i + h, len(lnP) - 1)] - lnP[i]) for k, i in enumerate(chocs)]))
    lags = {L: float(np.mean([sgn[k] * ret[i + L] for k, i in enumerate(chocs) if i + L < len(ret)])) for L in range(0, 6)}
    return (cum, lags), len(chocs)
def fit_tau(cum):
    hs = np.array(list(cum)); y = np.array([cum[h] for h in hs]); best = None
    for tf in np.arange(0.3, 3.1, 0.3):
        for ts in np.arange(3, 31, 1.0):
            X = np.column_stack([1 - np.exp(-hs / tf), 1 - np.exp(-hs / ts)])
            coef, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ coef; ss = float(r @ r)
            if best is None or ss < best[0]: best = (ss, float(tf), float(ts), float(coef[0]), float(coef[1]))
    return best
mesures = {}
for d in DRIVERS:
    z = gold[f'z_{d}'].fillna(0).values
    (cum, lags), nch = reponses(z)
    if cum is None: mesures[d] = {'chocs': nch, 'statut': 'TROP PEU DE CHOCS'}; continue
    ss, tf, ts, a, b = fit_tau(cum)
    pic = int(max(lags, key=lambda k: abs(lags[k])))
    plac = {}
    for dec in [-30, -60, -90]:
        (c2, l2), _ = reponses(z, dec)
        plac[str(dec)] = float(max(abs(v) for v in l2.values())) if l2 else None
    mesures[d] = {'chocs': int(nch), 'tau_fast_j': tf, 'tau_slow_j': ts, 'a_fast': a, 'b_slow': b,
                  'reponse_cumulee': {str(k): v for k, v in cum.items()}, 'pic_lag_j': pic,
                  'reponse_par_lag': {str(k): v for k, v in lags.items()},
                  'placebo_pic_max': plac, 'pic_reel_abs': float(abs(lags[pic]))}
    print(d, mesures[d])

# ---------- portes statistiques: regression du modele (gel) + BY + sous-periodes + quintiles ----------
MODELE = ['DFII10', 'dollar', 'COT_net', 'GVZ', 'volume_GC']
df = gold.dropna(subset=[f'z_{d}' for d in MODELE]).reset_index(drop=True)
mois = pd.get_dummies(df.date.dt.month, prefix='m', drop_first=True).astype(float)
X = np.column_stack([np.ones(len(df))] + [df[f'z_{d}'].values for d in MODELE] + [mois.values])
y = df.lnP.values
def ols_nw(X, y, lag=21):
    XtX_inv = np.linalg.inv(X.T @ X); beta = XtX_inv @ X.T @ y; e = y - X @ beta
    n, k = X.shape; S = np.zeros((k, k))
    for l in range(lag + 1):
        w = 1 if l == 0 else 2 * (1 - l / (lag + 1))
        G = (X[l:] * e[l:, None]).T @ (X[:n - l] * e[:n - l, None]) if l else (X * e[:, None]).T @ (X * e[:, None])
        S += w * G if l else G
    V = XtX_inv @ S @ XtX_inv; se = np.sqrt(np.diag(V))
    from math import erf, sqrt
    t = beta / se; p = np.array([1 - erf(abs(x) / sqrt(2)) for x in t])
    return beta, t, p, float(np.std(e))
beta, t, p, sig = ols_nw(X, y)
def by(pv):
    m = len(pv); ordre = np.argsort(pv); c = sum(1 / i for i in range(1, m + 1)); adj = np.empty(m); run = 1.0
    for i in range(m - 1, -1, -1):
        run = min(run, pv[ordre[i]] * m * c / (i + 1)); adj[ordre[i]] = run
    return adj
padj = by(p[1:6])
portes = {}
signes_attendus = {'DFII10': -1, 'dollar': -1}
for i, d in enumerate(MODELE):
    sous = []
    for q in range(4):
        seg = df.iloc[q * len(df) // 4:(q + 1) * len(df) // 4]
        Xs = np.column_stack([np.ones(len(seg)), seg[f'z_{d}'].values])
        bs, *_ = np.linalg.lstsq(Xs, seg.lnP.values, rcond=None); sous.append(float(np.sign(bs[1])))
    q5 = pd.qcut(df[f'z_{d}'], 5, duplicates='drop')
    moy = df.groupby(q5, observed=True).lnP.mean().values
    rq = np.corrcoef(np.arange(len(moy)), moy)[0, 1]
    bus = mesures.get(d, {})
    pic = bus.get('pic_lag_j', -1); plac = bus.get('placebo_pic_max', {}) or {}
    plac_max = max([abs(v) for v in plac.values() if v is not None], default=9)
    portes[d] = {'beta': float(beta[1 + i]), 't_NW': float(t[1 + i]), 'p_BY': float(padj[i]),
                 'signe_sous_periodes': sous, 'signe_coherent_3sur4': bool(max(sous.count(1), sous.count(-1)) >= 3),
                 'signe_attendu_canal': signes_attendus.get(d), 'signe_conforme_canal': (signes_attendus.get(d) is None or np.sign(beta[1 + i]) == signes_attendus[d]),
                 'monotonie_quintiles_rho': float(rq), 'bus_pic_lag': pic,
                 'bus_passe': bool(1 <= pic <= 3 and plac_max < 0.5 * bus.get('pic_reel_abs', 0)),
                 'porte_t': bool(abs(t[1 + i]) > 3 and padj[i] < 0.05),
                 'PORTE_GLOBALE': bool(abs(t[1 + i]) > 3 and padj[i] < 0.05 and max(sous.count(1), sous.count(-1)) >= 3 and abs(rq) >= 0.6 and (1 <= pic <= 3) and plac_max < 0.5 * bus.get('pic_reel_abs', 0) and (signes_attendus.get(d) is None or np.sign(beta[1 + i]) == signes_attendus[d]))}
    print(d, portes[d])

# ---------- gate R3 ----------
jours = len(df); duree = 10
paris = jours / duree
r10 = np.array([lnP[i + 10] - lnP[i] for i in range(0, len(lnP) - 10, 10)])
mde = 2.80 * np.std(r10) / np.sqrt(len(r10))   # 80% puissance, alpha 5% bilateral
C1_bps = 5.0   # aller-retour declare: spread reel ~3 bp + scenario 1 bp/cote x2 (CONDITIONNEL, BROKER_CONFIG UNKNOWN)
effet_min = 2 * C1_bps / 1e4 / 0.6  # ECR>=2 sur m_LB = exp(0,6|G_LB|)-1 -> ecart brut minimal requis approx
gate = {'jours_IS_tradeables': int(jours), 'duree_moyenne_trade_j_assumee': duree, 'paris_independants': float(paris),
        'sigma_retour_10j': float(np.std(r10)), 'MDE_80pct_log': float(mde), 'MDE_80pct_bp': float(mde * 1e4),
        'C1_aller_retour_bp_declare': C1_bps, 'effet_minimal_requis_bp (ECR>=2, haircut 0,6)': float(effet_min * 1e4),
        'verdict': 'TESTABLE' if mde < effet_min else 'NON TESTABLE'}
print(gate)
(OUT / 'F14_ETAPE_A.json').write_text(json.dumps({'mesures_deux_vitesses_bus': mesures, 'portes': portes,
    'sigma_residus_modele_complet': sig, 'gate_R3': gate,
    'note': 'Etape A = mesure/gates hors budget (ordre sec.3.0/3.3). Aucune variante testee. Couts CONDITIONNELS (BROKER_CONFIG UNKNOWN).'}, indent=1, default=str))
print('ETAPE A TERMINEE')
