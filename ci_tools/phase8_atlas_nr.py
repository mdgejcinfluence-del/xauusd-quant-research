"""PHASE 8 - ATLAS_NR (0 essai, descriptif pur). Corpus NR daily GC IS 2020-2023 uniquement.
Horaire Yahoo = 2024+ seulement (VALID/scellé): atlas intraday IS_NR impossible via S1 - consigne.
S3 Dukascopy qualifie mais backfill mensuel = programme cron (pas encore execute): l'atlas NR v1 est journalier."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha/nr'); OUT = R
C_BG = 4.7; C_NR = 1.35   # bp, snapshot S2 mesure (min inter-profils, 2026-11-19; cron en accumulation)
d = pd.read_parquet(R / 'data_is/yahoo_gc_daily.parquet').sort_values('ts')
d['ret'] = np.log(d.close).diff(); d['dow'] = d.ts.dt.dayofweek; d['mois'] = d.ts.dt.month
d['vol20'] = d.ret.rolling(20).std()
d['regime'] = pd.qcut(d.vol20, 3, labels=['calme', 'moyen', 'nerveux'])
m1 = d.groupby('dow').agg(vol_med=('ret', lambda s: float(s.std() * 1e4)), absret_med=('ret', lambda s: float(s.abs().median() * 1e4)),
                          volume_med=('volume', 'median'), n=('ret', 'size')).reset_index()
# M2: anatomie evenements (dates publiques FOMC du pack - faits publics; amplitudes, aucun pnl signe)
fomc = pd.read_csv('reports/meta_alpha/phase6/F15_EVENTS.csv')
fomc = fomc[(fomc.type == 'FOMC') & (fomc.t_avail >= '2020-01-01') & (fomc.t_avail < '2024-01-01')]
jours_ev = set(pd.to_datetime(fomc.t_avail).dt.date)
d['evt_fomc'] = d.ts.dt.date.isin(jours_ev)
m2 = d.groupby('evt_fomc').agg(absret_med_bp=('ret', lambda s: float(s.abs().median() * 1e4)), n=('ret', 'size')).to_dict('index')
# M6: cellules regime x horizon (autocorrelation descriptive, methode Phase 7)
cellules = []
for reg, seg in d.groupby('regime', observed=True):
    for hor in [1, 5]:
        s = seg.ret.dropna()
        rho = float(s.autocorr(hor))
        sig = float(s.std()) * 1e4
        effet = abs(rho) * sig
        n_eff = len(s) / hor
        mde = 2.80 * sig / np.sqrt(max(n_eff, 1))
        seuil = max(mde, 2 * C_BG, 2 * C_NR)
        cellules.append({'regime': str(reg), 'horizon_j': hor, 'n': int(len(s)), 'rho': rho, 'sigma_bp': sig,
                         'effet_bp': float(effet), 'MDE_bp': float(mde), 'seuil_bp': float(seuil), 'SURVIVANTE': bool(effet > seuil)})
m6 = pd.DataFrame(cellules)
data = {'M1_semaine': m1.to_dict('records'), 'M2_fomc_amplitudes': str(m2), 'M6': m6.to_dict('records'),
        'C1_NR_mesure_bp': C_NR, 'note_S2': 'snapshot unique a ce stade (50,4 cents @ 3725$); le cron 14h/22h UTC accumule la distribution - ancre provisoire',
        'absences': ['M3 macro NR: aucune source macro NR collectee (FRED sans cle) - consigne, pas fabrique',
                     'M1 intraday IS_NR: horaire Yahoo 2024+ seulement; S3 qualifie, backfill mensuel non encore execute']}
(OUT / 'ATLAS_NR_DATA.json').write_text(json.dumps(data, indent=1, default=str))
md = ['# ATLAS_NR — Phase 8 (descriptif, 0 essai, IS_NR 2020-2023 daily GC)', '',
      '## M1 semaine (vol et |ret| medians en bp, volume median)', m1.round(1).to_markdown(index=False), '',
      '## M2 FOMC (amplitudes medianes |ret| en bp)', str(m2), '',
      '## M5 couts', f'C1_NR mesure (S2, snapshot): ~{C_NR} bp (spread min inter-profils 50,4 cents a 3 725 $). C1_BG challenge: {C_BG} bp. Le regime actuel divise le spread en bp par ~2,5 vs l ancien corpus - mesure, pas importe.', '',
      '## M6 crible', m6.round(2).to_markdown(index=False), '',
      '## Absences consignees', '- M3 macro NR: aucune source collectee (pas de cle FRED) - non fabrique.', '- Intraday IS_NR: horaire Yahoo 2024+ uniquement; Dukascopy S3 QUALIFIE (18 478 ticks/h decompresses), backfill mensuel 2020-2023 = programme cron a venir, pas encore de matiere.']
(OUT / 'ATLAS_NR.md').write_text('\n'.join(md))
print(m6.round(2).to_string()); print('ATLAS NR TERMINE')
