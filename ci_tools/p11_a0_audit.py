"""P11-A0 - AUDIT DESCRIPTIF (autorisation proprietaire 2026-11-18, seq139).
Donnees: UNIQUEMENT les artefacts deja dans le depot git (aucun telechargement):
F15_EVENT_PNL.csv (entree tick >= T+5min, v2 seq112), ATLAS_DATA.json M2, F15_F16_GATES.json.
Aucun test, aucun signal, aucune optimisation, aucun taux de reussite strategique.
Les quantites absentes des artefacts sont ecrites NON MESURABLE, jamais imputees."""
import json, pathlib
import pandas as pd, numpy as np

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'p11_a0'; OUT.mkdir(parents=True, exist_ok=True)
ev = pd.read_csv(R / 'phase6/f15_events/F15_EVENT_PNL.csv')
ev = ev[ev.dec == 0].copy()  # evenements reels uniquement (dec != 0 = placebos, exclus de l'audit descriptif)
ev['t_avail'] = pd.to_datetime(ev.t_avail)
m2 = {r['type']: r for r in json.loads((R / 'phase7/ATLAS_DATA.json').read_text())['M2']}
gates = json.loads((R / 'phase6/F15_F16_GATES.json').read_text())

rows = []
for _, r in ev.iterrows():
    g = gates['F15'].get(r['type'], {})
    rows.append({
        'type': r['type'], 't_avail_utc': r['t_avail'].isoformat(),
        'spread_a_entree_Tplus5min_bp (MESURE, tick d entree v2)': r['spread_entree_bp'],
        'amplitude_premier_mouvement_T_Tplus5min_bp (MESURE descriptive, NON capturable par construction: mouvement anterieur a l entree)': r['mouv_bp'],
        'abs_mouvement_5min_median_atlas_M2_bp': m2.get(r['type'], {}).get('abs_mouv_5min_bp'),
        'spread_avant_annonce_Tmoins5_bp': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES (artefact local absent)',
        'spread_Tplus1_a_Tplus4min_bp': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES (artefact local absent)',
        'duree_episode_spread_eleve': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES',
        'delai_retour_spread_habituel': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES',
        'cotations_manquantes_ou_perimees': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES',
        'slippage_reel': 'NON MESURABLE AVEC LES DONNEES DISPONIBLES (aucune donnee d execution dans le depot)',
        'exec_long_15min_bp (MESURE passee F15, rappel descriptif seulement)': r['exec_long_15'],
        'exec_short_15min_bp (MESURE passee F15, rappel descriptif seulement)': r['exec_short_15'],
    })
out = pd.DataFrame(rows); out.to_csv(OUT / 'P11_A0_EVENT_MEASURES.csv', index=False)

def stats(s):
    return {'n': int(s.notna().sum()), 'mediane': round(float(s.median()), 2), 'p90': round(float(s.quantile(.9)), 2),
            'p95': round(float(s.quantile(.95)), 2), 'p99': round(float(s.quantile(.99)), 2), 'max': round(float(s.max()), 2)}
resume = {}
for t, d in out.groupby('type'):
    resume[t] = {'n_evenements': len(d), 'spread_a_entree_Tplus5min_bp': stats(d.iloc[:, 2]),
                 'amplitude_abs_premier_mouvement_bp': stats(d.iloc[:, 3].abs()),
                 'reference_spread_median_IS_global_bp': gates['spread_median_IS_bp'],
                 'C1_hist_RT_bp': gates['C1_hist_RT_bp'], 'C1_BG_RT_bp': gates['C1_BG_RT_bp']}
(OUT / 'P11_A0_RESUME.json').write_text(json.dumps(resume, indent=1))
print(json.dumps(resume, indent=1)); print('lignes evenements:', len(out))
