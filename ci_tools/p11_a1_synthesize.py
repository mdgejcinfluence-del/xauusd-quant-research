"""P11-A1 SYNTHESE DESCRIPTIVE (seq141). Aucun signal, aucun PnL, aucune optimisation.
Agrege P11_A1_EVENT_MINUTES.csv: par famille x minute, couverture, durees de spread eleve,
retour au niveau habituel (reference pre-annonce de l'evenement), metriques par evenement."""
import json, pathlib
import pandas as pd, numpy as np

R = pathlib.Path('reports/meta_alpha'); D = R / 'p11_a1'
m = pd.read_csv(D / 'P11_A1_EVENT_MINUTES.csv')
m['t_avail'] = pd.to_datetime(m.t_avail)
ev_ref = pd.read_csv(R / 'phase6/f15_events/F15_EVENT_PNL.csv'); ev_ref = ev_ref[ev_ref.dec == 0]

# reference habituelle par evenement = mediane du spread minute sur T-5..T-1
pre = m[m.minute.between(-5, -1)].groupby(['type', 't_avail']).spread_med_bp.median().rename('spread_pre_bp')
m = m.join(pre, on=['type', 't_avail'])
m['eleve'] = m.spread_med_bp > 2 * m.spread_pre_bp

par_minute = (m.groupby(['type', 'minute'])
              .agg(n_evenements=('t_avail', 'nunique'), n_ticks_med=('n_ticks', 'median'),
                   spread_med=('spread_med_bp', 'median'), spread_p90=('spread_med_bp', lambda s: s.quantile(.9)),
                   spread_p95=('spread_med_bp', lambda s: s.quantile(.95)), spread_p99=('spread_med_bp', lambda s: s.quantile(.99)),
                   couverture=('couverture', 'mean'), intertick_med_s=('intertick_med_s', 'median'),
                   trou_max_s_med=('trou_max_s', 'median')).reset_index())

even = []
for (t, ta), g in m.groupby(['type', 't_avail']):
    w = g.set_index('minute').sort_index()
    post = w.loc[0:5]
    duree = int(w.loc[0:30, 'eleve'].sum()) if 'eleve' in w else np.nan
    retour = np.nan
    for mn in range(0, 31):
        if mn in w.index and w.loc[mn, 'spread_med_bp'] <= 1.5 * w.loc[-5:0, 'spread_med_bp'].median() if False else False: pass
    pre_med = w.loc[-5:-1, 'spread_med_bp'].median()
    cand = [mn for mn in range(0, 31) if mn in w.index and w.loc[mn, 'spread_med_bp'] <= 1.5 * pre_med]
    retour = min(cand) if cand else np.nan
    even.append({'type': t, 't_avail_utc': ta.isoformat(), 'spread_pre_median_bp': pre_med,
                 'spread_T1_bp': w.loc[1, 'spread_med_bp'] if 1 in w.index else np.nan,
                 'spread_T2_bp': w.loc[2, 'spread_med_bp'] if 2 in w.index else np.nan,
                 'spread_T3_bp': w.loc[3, 'spread_med_bp'] if 3 in w.index else np.nan,
                 'spread_T4_bp': w.loc[4, 'spread_med_bp'] if 4 in w.index else np.nan,
                 'spread_T5_bp': w.loc[5, 'spread_med_bp'] if 5 in w.index else np.nan,
                 'spread_max_T0_T5_bp': post.spread_max_bp.max(), 'n_ticks_T0_T5': int(post.n_ticks.sum()),
                 'minutes_spread_eleve_T0_T30': duree, 'retour_sous_1.5x_pre_min': retour,
                 'trou_max_T0_T5_s': post.trou_max_s.max(), 'minutes_couvertes_sur_36': int(w.couverture.sum())})
even = pd.DataFrame(even); even.to_csv(D / 'P11_A1_EVENT_METRICS.csv', index=False)
par_minute.to_csv(D / 'P11_A1_BY_MINUTE.csv', index=False)

resume = {}
for t, g in even.groupby('type'):
    resume[t] = {'n_evenements_extraites': int(len(g)),
                 'spread_pre_bp': {'mediane': round(float(g.spread_pre_median_bp.median()), 2), 'p95': round(float(g.spread_pre_median_bp.quantile(.95)), 2)},
                 **{f'spread_T{k}_bp': {'mediane': round(float(g[f'spread_T{k}_bp'].median()), 2), 'p90': round(float(g[f'spread_T{k}_bp'].quantile(.9)), 2), 'p95': round(float(g[f'spread_T{k}_bp'].quantile(.95)), 2), 'p99': round(float(g[f'spread_T{k}_bp'].quantile(.99)), 2)} for k in range(1, 6)},
                 'minutes_spread_eleve_T0_T30': {'mediane': float(g.minutes_spread_eleve_T0_T30.median()), 'p90': float(g.minutes_spread_eleve_T0_T30.quantile(.9))},
                 'retour_sous_1.5x_pre_min': {'mediane': float(g['retour_sous_1.5x_pre_min'].median()), 'p90': float(g['retour_sous_1.5x_pre_min'].quantile(.9)), 'jamais_sur_30min_pct': round(float(g['retour_sous_1.5x_pre_min'].isna().mean() * 100), 1)},
                 'trou_max_T0_T5_s': {'mediane': float(g.trou_max_T0_T5_s.median()), 'p95': float(g.trou_max_T0_T5_s.quantile(.95))},
                 'couverture_minutes_mediane_sur_36': float(g.minutes_couvertes_sur_36.median())}
resume['_couverture_globale'] = {'evenements_F15_reels_attendus': int(len(ev_ref)), 'evenements_extraites': int(even[['type','t_avail_utc']].drop_duplicates().shape[0])}
(D / 'P11_A1_RESUME.json').write_text(json.dumps(resume, indent=1))
print(json.dumps(resume, indent=1))
