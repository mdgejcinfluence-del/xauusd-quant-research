"""PHASE 8 - ATLAS_NR INTRADAY (0 essai, descriptif). Source: S3 Dukascopy horaire IS_NR 2020-2023.
Meme crible M6 que Phase 7: effet descriptif |rho| x sigma vs max(MDE, plancher cout 2xC aux deux ancres)."""
import glob, json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha/nr')
fs = sorted(glob.glob(str(R / 's3_hourly/s3_hourly_*.parquet')))
d = pd.concat([pd.read_parquet(f) for f in fs]).sort_values('heure').reset_index(drop=True)
d['ret'] = np.log(d.close).diff()
d['hh'] = d.heure.dt.hour; d['date'] = d.heure.dt.date
jvol = d.groupby('date').ret.apply(lambda s: float(np.sqrt((s ** 2).sum()))).rename('vol_jour')
d = d.merge(jvol, on='date'); d['regime'] = pd.qcut(d.vol_jour, 3, labels=['calme', 'moyen', 'nerveux'])
FEN = [(0, 5, '00-05'), (6, 11, '06-11'), (12, 16, '12-16'), (17, 21, '17-21'), (22, 23, '22-23')]
d['fenetre'] = d.hh.map(lambda hh: [lab for a, b, lab in FEN if a <= hh <= b][0])
m1 = d.groupby(['fenetre']).agg(vol_med_bp=('ret', lambda s: float(s.std() * 1e4)), spread_med_bp=('spread_med', 'median'),
                                spread_p95_bp=('spread_med', lambda s: float(s.quantile(.95))), n=('ret', 'size')).reset_index()
m5 = d.groupby(['fenetre', 'regime'], observed=True).agg(spread_med_bp=('spread_med', 'median'), vol_med_bp=('ret', lambda s: float(s.std() * 1e4)), n=('ret', 'size')).reset_index()
C_NR = float(d.spread_med.median()); C_BG = 4.7
d['ret4'] = d.ret.rolling(4).sum().shift(-3)
cellules = []
for (fen, reg), seg in d.groupby(['fenetre', 'regime'], observed=True):
    for hor, col in [('1h', 'ret'), ('4h', 'ret4')]:
        s = seg[col].dropna()
        if len(s) < 200: continue
        rho = float(s.autocorr(1)) if hor == '1h' else float(s.autocorr(4))
        sig = float(s.std()) * 1e4; effet = abs(rho) * sig
        n_eff = len(s) / (1 if hor == '1h' else 4)
        mde = 2.80 * sig / np.sqrt(max(n_eff, 1))
        seuil = max(mde, 2 * max(C_NR, C_BG))
        cellules.append({'fenetre': fen, 'regime': str(reg), 'horizon': hor, 'n': int(len(s)), 'rho1': rho, 'sigma_bp': sig,
                         'effet_bp': float(effet), 'MDE_bp': float(mde), 'seuil_bp': float(seuil), 'SURVIVANTE': bool(effet > seuil)})
m6 = pd.DataFrame(cellules).sort_values('effet_bp', ascending=False)
out = {'source': 'S3 Dukascopy bougies 1min agregees horaire, IS_NR 2020-2023', 'heures': int(len(d)),
       'plage': [str(d.heure.min()), str(d.heure.max())], 'C_NR_spread_median_mesure_bp': C_NR, 'C_BG': C_BG,
       'M1': m1.to_dict('records'), 'M5': m5.to_dict('records'), 'M6': m6.to_dict('records'),
       'survivantes': m6[m6.SURVIVANTE].to_dict('records')}
(R / 'ATLAS_NR_INTRADAY.json').write_text(json.dumps(out, indent=1, default=str))
print(f'heures={len(d)} C_NR mesure={C_NR:.2f} bp; survivantes={int(m6.SURVIVANTE.sum())}/{len(m6)}')
print(m6.head(8).round(2).to_string())
print('ATLAS INTRADAY TERMINE')
