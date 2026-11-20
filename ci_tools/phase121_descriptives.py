"""PHASE 12.1 - STATISTIQUES DESCRIPTIVES IS UNIQUEMENT (derogation cadree seq145).
AUCUNE mesure de performance, aucun PnL de strategie, aucun taux de reussite.
Sorties: profil saisonnier horaire (vol/spread), spread par session (conventions
proposees seq144), co-occurrence F3 (pred journaliere) x F7 — F7 n'ayant pas de serie
horaire versionnee locale, la co-occurrence utilise les regimes documentes disponibles
(vol predite F3 deciles x deciles de vol realisee horaire comme proxy DECLARE, voir rapport)."""
import json, pathlib
import pandas as pd, numpy as np

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase12_1'; OUT.mkdir(parents=True, exist_ok=True)
h = pd.read_parquet(R / 'phase7/ATLAS_HOURLY.parquet')  # serie horaire IS certifiee (seq Phase 2/7)

# 1) Profil saisonnier horaire: part de variance par heure UTC (moyenne des sumsq horaires par heure / total jour)
prof = h.groupby('heure').agg(vol_bp_med=('vol_bp', 'median'), sumsq_moy=('sumsq', 'mean'),
                              spread_med=('spread', 'median'), spread_p90=('spread', lambda s: s.quantile(.9)), n=('ret', 'size')).reset_index()
prof['part_variance_pct'] = (prof.sumsq_moy / prof.sumsq_moy.sum() * 100).round(2)
prof.to_csv(OUT / 'HOURLY_SEASONAL_PROFILE.csv', index=False)

# 2) Spread par session (conventions proposees seq144: Asie 00-08, Londres 08-13, NY 13-21 UTC)
def session(hr): return 'Asie_00-08' if hr < 8 else ('Londres_08-13' if hr < 13 else ('NewYork_13-21' if hr < 21 else 'Nuit_21-24'))
h['session'] = h.heure.map(session)
ses = h.groupby('session').agg(spread_med=('spread', 'median'), spread_p75=('spread', lambda s: s.quantile(.75)),
                               spread_p90=('spread', lambda s: s.quantile(.9)), vol_bp_med=('vol_bp', 'median'), n_heures=('ret', 'size')).reset_index()
ses.to_csv(OUT / 'SPREAD_BY_SESSION.csv', index=False)

# 3) F3: distribution de la vol predite (deciles IS) - serie journaliere certifiee
f3 = pd.read_csv(R / 'phase2/f3_har/F3_DAILY_PRED.csv').dropna(subset=['pred_har'])
f3['decile_F3'] = pd.qcut(f3.pred_har, 10, labels=False)
# 4) Co-occurrence descriptive: regime de vol predite (decile du jour) x intensite horaire realisee
# (proxy DECLARE: aucun artefact F7 horaire n'est versionne localement - voir rapport sec.3)
h['date'] = pd.to_datetime(h.date.astype(str))
f3['date'] = pd.to_datetime(f3.day.astype(str)).dt.tz_localize(None)
j = h.merge(f3[['date', 'decile_F3', 'pred_har']], on='date', how='inner')
j['decile_vol_horaire'] = pd.qcut(j.vol_bp, 10, labels=False)
co = pd.crosstab(j.decile_F3, j.decile_vol_horaire, normalize='index').round(3)
co.to_csv(OUT / 'F3_REGIME_X_HOURLY_VOL.csv')
resume = {'profil_horaire': prof.round(3).to_dict('records'), 'spread_sessions': ses.round(3).to_dict('records'),
          'f3_deciles_pred_har': {str(k): round(float(v), 4) for k, v in f3.groupby('decile_F3').pred_har.mean().items()},
          'n_jours_F3': int(len(f3)), 'n_heures_jointes': int(len(j))}
(OUT / 'DESCRIPTIVES_RESUME.json').write_text(json.dumps(resume, indent=1))
print('heures:', len(h), 'jours F3:', len(f3), 'jointure:', len(j)); print(ses.to_string(index=False))
print(prof[['heure', 'part_variance_pct', 'spread_med']].to_string(index=False))
