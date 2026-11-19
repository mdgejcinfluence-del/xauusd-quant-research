"""F15/F16 - GATES R3 (avant toute performance, ordre Phase 6B). Aucun retour d'evenement,
aucun P&L de signal n'est calcule ici: seulement n, sigma d'horizon, MDE, effets minimaux."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase6'
P = R / 'exogenous/data_is'
C_BG = 4.7  # bp aller-retour, OWNER_CONFIG_V2

# sigma horaire + spread d'epoque (serie horaire deja certifiee du corpus)
h = pd.read_csv(R / 'vol_hourly/PARTITION_HOUR_TS.csv')
h = h[h.hour_ts <= '2020-01-20']
sig_h = float(h.ret_hour.std()); spread_hist = float(h.spread_bp.median())
C_HIST = spread_hist + 2 * 0.5  # spread reel median + commission BG 2x0,5 bp
print(f'sigma 60min={sig_h*1e4:.1f} bp; spread median IS={spread_hist:.2f} bp; C1_hist RT={C_HIST:.2f} bp; C1_BG RT={C_BG} bp')

def mde(sigma, n): return 2.80 * sigma / np.sqrt(n)
res = {'sigma_60min_bp': sig_h * 1e4, 'spread_median_IS_bp': spread_hist, 'C1_hist_RT_bp': C_HIST, 'C1_BG_RT_bp': C_BG}

# --- F15: comptes d'evenements (releases distinctes) ---
ev = {}
pay = pd.read_parquet(P / 'macro_payems_pit.parquet'); ev['FOMC'] = 81
ev['NFP'] = int(pay.vintage_date.nunique())
cpi = pd.read_parquet(P / 'macro_cpiaucsl_pit.parquet'); ev['CPI'] = int(cpi.vintage_date.nunique())
f15 = {}
for nom, n in ev.items():
    m = mde(sig_h, n)
    f15[nom] = {'n_evenements': n, 'MDE_80pct_bp': float(m * 1e4),
                'effet_min_BG_bp (2xC1_BG)': 2 * C_BG, 'effet_min_hist_bp (2xC1_hist)': float(2 * C_HIST),
                'verdict': 'TESTABLE' if m * 1e4 <= min(2 * C_BG, 2 * C_HIST) else 'NON TESTABLE (MDE > effet aux deux ancres)'}
    print('F15', nom, f15[nom])
res['F15'] = f15

# --- F16: semaines COT IS + sigma 2 semaines de l'or ---
cot = pd.read_parquet(P / 'cftc_cot_gold_disagg.parquet')
sem = int(cot.reference_date.nunique())
al = pd.read_parquet(OUT / 'F14_DAILY_ALIGNED.parquet')
lnP = al.lnP.values
r2s = np.array([lnP[i + 14] - lnP[i] for i in range(0, len(lnP) - 14, 14)])
paris = sem / 2
m16 = mde(np.std(r2s), paris)
res['F16'] = {'semaines_COT_IS': sem, 'paris_independants_2sem': float(paris), 'sigma_2sem_bp': float(np.std(r2s) * 1e4),
              'MDE_80pct_bp': float(m16 * 1e4), 'effet_min_BG_bp': 2 * C_BG, 'effet_min_hist_bp': float(2 * C_HIST),
              'verdict': 'TESTABLE' if m16 * 1e4 <= min(2 * C_BG, 2 * C_HIST) else 'NON TESTABLE (MDE > effet aux deux ancres)'}
print('F16', res['F16'])
(OUT / 'F15_F16_GATES.json').write_text(json.dumps(res, indent=1, default=str))
print('GATES TERMINES')
