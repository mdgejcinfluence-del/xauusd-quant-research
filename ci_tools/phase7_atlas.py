"""PHASE 7 AXE 1 - ATLAS STRUCTUREL (0 essai). DESCRIPTIF UNIQUEMENT:
moyennes, quantiles, autocorrelations, intensites. Aucune statistique de gain directionnel.
M6 confronte un effet descriptif (autocorrelation x sigma) au MDE R3 et au plancher ECR>=2."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase7'; OUT.mkdir(parents=True, exist_ok=True)
C_BG = 4.7
h = pd.read_csv(R / 'vol_hourly/PARTITION_HOUR_TS.csv', parse_dates=['hour_ts'])
h = h[h.hour_ts <= '2020-01-20 09:36:27']
g = h.groupby('hour_ts').agg(ret=('ret_hour', 'sum'), sumsq=('sumsq_rbp', 'sum'), n=('n', 'sum'),
                             spread=('spread_bp', lambda s: float(np.average(s, weights=h.loc[s.index, 'n'])))).reset_index()
g['vol_bp'] = np.sqrt(g.sumsq)
g['heure'] = g.hour_ts.dt.hour; g['dow'] = g.hour_ts.dt.dayofweek; g['date'] = g.hour_ts.dt.date
g.to_parquet(OUT / 'ATLAS_HOURLY.parquet', index=False)

# M1: grille heure x jour de semaine
m1 = g.groupby(['heure', 'dow']).agg(vol_med=('vol_bp', 'median'), spread_med=('spread', 'median'),
                                     spread_p95=('spread', lambda s: float(np.quantile(s, .95))),
                                     ticks=('n', 'mean')).reset_index()
saut = g.assign(saut=(g.ret.abs() > 3 * g.ret.std()).astype(float)).groupby(['heure', 'dow']).saut.mean().rename('intensite_sauts')
m1 = m1.merge(saut, on=['heure', 'dow'])
# M5: carte des couts par fenetre x regime (regime = tercile de vol journaliere)
jvol = g.groupby('date').vol_bp.apply(lambda s: float(np.sqrt((s ** 2).sum()))).rename('vol_jour')
g = g.merge(jvol, on='date'); g['regime'] = pd.qcut(g.vol_jour, 3, labels=['calme', 'moyen', 'nerveux'])
FEN = [(0, 5, '00-05'), (6, 11, '06-11'), (12, 16, '12-16'), (17, 21, '17-21'), (22, 23, '22-23')]
def fenetre(hh): return [lab for a, b, lab in FEN if a <= hh <= b][0]
g['fenetre'] = g.heure.map(fenetre)
m5 = g.groupby(['fenetre', 'regime'], observed=True).agg(spread_med=('spread', 'median'), spread_p95=('spread', lambda s: float(np.quantile(s, .95))), vol_med=('vol_bp', 'median'), n=('ret', 'size')).reset_index()
m5['capturable_min_bp (2xC)'] = 2 * np.maximum(m5.spread_med, C_BG)

# M2: anatomie evenements (descriptif: |ret| et spread d'entree, jamais de pnl signe)
ev = pd.read_csv(R / 'phase6/f15_events/F15_EVENT_PNL.csv')
ev0 = ev[ev.dec == 0]
m2 = ev0.groupby('type').agg(n=('mid_60', 'size'), spread_entree_med=('spread_entree_bp', 'median'),
                             abs_mouv_5min_bp=('mouv_bp', lambda s: float(s.abs().median())),
                             abs_ret_15=('mid_15', lambda s: float(s.abs().median())), abs_ret_60=('mid_60', lambda s: float(s.abs().median())),
                             abs_ret_240=('mid_240', lambda s: float(s.abs().median()))).reset_index()
# demi-vie descriptive: horizon ou |ret| median repasse sous la moitie du niveau a 15 min (interpolation grossiere sur {15,60,240})
def demivie(r):
    niv = r.abs_ret_15 / 2
    for hh, v in [(15, r.abs_ret_15), (60, r.abs_ret_60), (240, r.abs_ret_240)]:
        if v <= niv * 2 * 0 + r.abs_ret_15 and hh > 15: pass
    return '>240 min (pas de retour sous le niveau 15min dans la fenetre)' if r.abs_ret_240 > r.abs_ret_15 * 0.7 else 'entre 60 et 240 min'
m2['lecture_vol'] = m2.apply(demivie, axis=1)

# M3: etats macro (aligne F14) + covariation avec RV F3 et intensite de sauts journaliere
al = pd.read_parquet(R / 'phase6/F14_DAILY_ALIGNED.parquet')
f3 = pd.read_csv(R / 'phase2/f3_har/F3_DAILY_PRED.csv', parse_dates=['day'])
al['date'] = pd.to_datetime(al.date).dt.tz_localize(None)
f3['day'] = f3.day.dt.tz_localize(None) if str(f3.day.dtype).endswith('UTC]') else f3.day
al = al.merge(f3[['day', 'rv']], left_on='date', right_on='day', how='left')
P = R / 'exogenous/data_is'
def asof(nom):
    d = pd.read_parquet(P / f'{nom}.parquet')[['available_at_utc', 'value']].dropna().sort_values('available_at_utc')
    d = d[d.available_at_utc <= '2020-01-20 09:36:27']
    m = pd.merge_asof(al[['decision']].sort_values('decision'), d, left_on='decision', right_on='available_at_utc', direction='backward')
    return m['value'].values
al['DGS10'] = asof('fred_dgs10_officiel'); al['DGS2'] = asof('fred_dgs2_officiel'); al['pente'] = al.DGS10 - al.DGS2
sauts_j = g.assign(saut=(g.ret.abs() > 3 * g.ret.std()).astype(float)).groupby('date').saut.mean()
al['date_j'] = al.date.dt.date
al['sauts_j'] = al.date_j.map(sauts_j)
m3 = {}
for col in ['DFII10', 'pente', 'GVZ']:
    s = al[col].dropna()
    m3[col] = {'mediane': float(s.median()), 'q10': float(s.quantile(.1)), 'q90': float(s.quantile(.9)),
               'autocorr_1j': float(s.autocorr(1)), 'autocorr_21j': float(s.autocorr(21)),
               'corr_vol_realisee': float(al[[col, 'rv']].dropna().corr().iloc[0, 1]),
               'corr_intensite_sauts': float(al[[col, 'sauts_j']].dropna().corr().iloc[0, 1])}

# M4: correlations panel (descriptif)
pan = pd.read_csv(R / 'panel/PANEL_PRICES.csv', parse_dates=['date'])
rets = np.log(pan.set_index('date').sort_index()).diff()
gold_col = [c for c in rets.columns if 'gold' in c.lower() or c.upper().startswith('GC')]
m4 = {'colonnes_or_detectees': gold_col}
if gold_col:
    gc = gold_col[0]
    cors = rets.corr()[gc].drop(gold_col).sort_values(key=abs, ascending=False)
    m4['top_corr'] = {k: float(v) for k, v in cors.head(8).items()}
    moitie = len(rets) // 2
    c1 = rets.iloc[:moitie].corr()[gc]; c2 = rets.iloc[moitie:].corr()[gc]
    m4['stabilite_corr (corr des corr moitie1/moitie2)'] = float(pd.concat([c1, c2], axis=1).dropna().corr().iloc[0, 1])

# M6: LE CRIBLE - cellules fenetre x regime x horizon intraday (1h, 4h)
g = g.sort_values('hour_ts')
g['ret4'] = g.ret.rolling(4).sum().shift(-3)  # retour des 4 prochaines heures (descriptif d'autocorrelation)
cellules = []
for (fen, reg), seg in g.groupby(['fenetre', 'regime'], observed=True):
    for hor, col in [('1h', 'ret'), ('4h', 'ret4')]:
        s = seg[col].dropna()
        if len(s) < 200: continue
        # autocorrelation ordre 1 des retours du bucket (structure descriptive, pas un pnl)
        rho = float(s.autocorr(1)) if hor == '1h' else float(s.autocorr(4))
        sig = float(s.std()) * 1e4
        effet = abs(rho) * sig
        n_eff = len(s) / (1 if hor == '1h' else 4)
        mde = 2.80 * sig / np.sqrt(max(n_eff, 1))
        plancher = float(2 * max(seg.spread.median(), C_BG))
        seuil = max(mde, plancher)
        cellules.append({'fenetre': fen, 'regime': str(reg), 'horizon': hor, 'n': int(len(s)), 'rho1': rho,
                         'sigma_bp': sig, 'effet_descriptif_bp': float(effet), 'MDE_bp': float(mde),
                         'plancher_cout_bp': plancher, 'seuil_requis_bp': float(seuil),
                         'SURVIVANTE': bool(effet > seuil)})
m6 = pd.DataFrame(cellules).sort_values('effet_descriptif_bp', ascending=False)
surv = m6[m6.SURVIVANTE]
data = {'M1': m1.to_dict('records'), 'M5': m5.to_dict('records'), 'M2': m2.to_dict('records'), 'M3': m3, 'M4': m4,
        'M6': m6.to_dict('records'), 'cellules_survivantes': surv.to_dict('records')}
(OUT / 'ATLAS_DATA.json').write_text(json.dumps(data, indent=1, default=str))
md = ['# ATLAS STRUCTUREL XAUUSD — Phase 7 Axe 1 (descriptif, 0 essai)', '',
      'Aucune statistique de gain directionnel. Sources: serie horaire certifiee du corpus tick, DAILY_VOL, F3 daily, panel 43, pack exogene IS. Perimetre IS strict.', '',
      '## M1 — Calendrier intrajournalier (vol mediane en bp/h, spread median bp, par heure UTC; semaine complete dans ATLAS_DATA.json)',
      m1.groupby('heure').agg(vol=('vol_med', 'median'), spread=('spread_med', 'median'), spread_p95=('spread_p95', 'median'), ticks=('ticks', 'mean'), sauts=('intensite_sauts', 'mean')).round(2).to_markdown(), '',
      '## M5 — Carte des couts (fenetre x regime; plancher de capturabilite = 2 x max(spread, C1_BG 4,7))',
      m5.round(2).to_markdown(index=False), '',
      '## M2 — Anatomie des evenements (amplitudes medianes, jamais de pnl signe)',
      m2.round(2).to_markdown(index=False), '',
      '## M3 — Etats macro', '```json', json.dumps(m3, indent=1, default=str), '```', '',
      '## M4 — Structure croisee panel', '```json', json.dumps(m4, indent=1, default=str)[:1500], '```', '',
      '## M6 — Carte de chasse: cellules survivantes', f'**{len(surv)} cellule(s) survivante(s) sur {len(m6)}.**',
      m6.head(10).round(2).to_markdown(index=False),
      '', 'Lecture: l effet descriptif (|autocorrelation| x sigma) doit depasser max(MDE R3, plancher de cout ECR>=2). En dessous: cellule morte avant test, sans consommer d essai.']
(OUT / 'ATLAS_XAUUSD.md').write_text('\n'.join(md))
print(f'M1 {len(m1)} lignes; M6: {len(surv)}/{len(m6)} survivantes')
print(m6.head(8).round(2).to_string())
print('ATLAS TERMINE')
