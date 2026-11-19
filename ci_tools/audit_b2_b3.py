"""REPONSE A L'AUDIT - portes B2 (prime de variance, MESURE descriptive) et B3 (borne maker, descriptive horaire).
0 essai, aucun test directionnel, aucune performance de trading. B1 reste en attente d'ordre Phase 9."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase9'; OUT.mkdir(parents=True, exist_ok=True)
# --- B2: GVZ (implicite, %) vs RV realisee annualisee (F3/DAILY_VOL, bp^2 -> %) ---
dv = pd.read_csv(R / 'vol_models/DAILY_VOL.csv', parse_dates=['date'])
jour = dv.groupby('date').rv.sum()
vol_j = np.sqrt(jour) * np.sqrt(252) / 100 * 100 / 100  # sqrt(somme r^2 en ratio) -> vol jour ratio; annualisee en %
vol_j = np.sqrt(jour) * np.sqrt(252) * 100
gvz = pd.read_parquet(R / 'exogenous/data_is/fred_gvz_officiel.parquet')
gvz['date'] = (gvz.available_at_utc - pd.Timedelta(days=1)).dt.date  # reference = available - 1j (convention du pack)
g = gvz.set_index('date').value
df = pd.DataFrame({'gvz': g}); df['rv_futur_21j'] = vol_j.rolling(21).mean().shift(-21)
df['rv_contemp'] = vol_j
df = df.dropna()
df['prime_futur'] = df.gvz - df.rv_futur_21j
par_era = {}
for lab, seg in [('2010-2013', df[df.index < pd.Timestamp('2014-01-01').date()]), ('2014-2016', df[(df.index >= pd.Timestamp('2014-01-01').date()) & (df.index < pd.Timestamp('2017-01-01').date())]), ('2017-2020', df[df.index >= pd.Timestamp('2017-01-01').date()])]:
    if len(seg): par_era[lab] = {'prime_moyenne_pts': float(seg.prime_futur.mean()), 'part_positive': float((seg.prime_futur > 0).mean()), 'n': int(len(seg))}
b2 = {'definition': 'prime = GVZ(t) - RV realisee annualisee moyenne des 21 jours de bourse suivants (mesure, pas une strategie)',
      'n': int(len(df)), 'prime_moyenne_pts_vol': float(df.prime_futur.mean()), 'prime_mediane': float(df.prime_futur.median()),
      'part_positive': float((df.prime_futur > 0).mean()), 'par_era': par_era,
      'lecture': "prime positive persistante = l'implicite paie au-dessus du realise en moyenne (structure documentee ailleurs, confirmee ici en mesure). Monetisation: vendre de la volatilite exige des options - hors infra actuelle (CFD taker). Aucun essai consomme, aucune position simulee."}
# --- B3: borne descriptive horaire (le tick trancherait; ici on borne) ---
h = pd.read_parquet(R / 'phase7/ATLAS_HOURLY.parquet').sort_values('hour_ts')
h['ret_next'] = h.ret.shift(-1)
dec = h.spread.quantile(0.9)
b3 = {'spread_median_global_bp': float(h.spread.median()), 'spread_median_decile_haut_bp': float(h.spread[h.spread >= dec].median()),
      'abs_ret_heure_suivante_decile_haut_bp': float(h.ret_next[h.spread >= dec].abs().median() * 1e4),
      'abs_ret_heure_suivante_reste_bp': float(h.ret_next[h.spread < dec].abs().median() * 1e4),
      'lecture': ("borne horaire grossiere: dans les heures ou le spread est large (la ou un maker capterait le plus), "
                  "le mouvement absolu de l'heure suivante est aussi le plus grand - l'adverse selection y est maximale. "
                  "Le tick seul trancherait (file d'attente, remplissage partiel): etude CI dediee a preenregistrer si le proprietaire ouvre la Phase 9. "
                  "Rappel: CFD retail = 100% taker; le maker exige futures/bourse - hors perimetre Blue Guardian.")}
(OUT / 'PORTES_B2_B3.json').write_text(json.dumps({'B2': b2, 'B3': b3}, indent=1, default=str))
print(json.dumps(b2, indent=1, default=str)); print(json.dumps(b3, indent=1, default=str))
print('B2/B3 DESCRIPTIF TERMINE - 0 essai')
