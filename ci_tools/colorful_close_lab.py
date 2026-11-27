#!/usr/bin/env python3
"""COLORFUL-FILTER-002: reconstruction des fermetures reelles (C1-C4) + dissection des
10 paniers supplementaires V2 (X1). Prix Mid Dukascopy (comparatifs, jamais HFM).
Entrees reelles: heures affichees serveur, UTC+2 suppose. Aucun prix futur pour les
features d'entree; l'analyse de cloture est descriptive du passe observe."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research/COLORFUL-FILTER-002'; OUT.mkdir(parents=True, exist_ok=True)
# nom: (jour, [(entree UTC, volume)], cloture UTC)
PANIERS = {
 'A': ('2026-11-26', [('2026-11-26 11:31:20', .01), ('2026-11-26 11:32:00', .01), ('2026-11-26 11:35:00', .02)], '2026-11-26 11:50:32'),
 'B': ('2026-11-26', [('2026-11-26 11:50:34', .01), ('2026-11-26 11:51:03', .01), ('2026-11-26 12:01:01', .02)], '2026-11-26 12:02:29'),
 'C': ('2026-11-27', [('2026-11-27 08:30:00', .01), ('2026-11-27 08:30:20', .01), ('2026-11-27 08:33:34', .03)], '2026-11-27 08:40:50'),
 'D': ('2026-11-27', [('2026-11-27 08:45:00', .01)], '2026-11-27 08:45:17'),
 'E': ('2026-11-27', [('2026-11-27 09:00:00', .01), ('2026-11-27 09:00:16', .01)], '2026-11-27 09:01:27'),
}

def mid_at(df, t):
    s = df[df.ts <= t]
    return float(s.mid.iloc[-1]) if len(s) else None

def main():
    res = {'clotures': {}, 'extras_V2': []}
    dfs = {}
    for nom, (jour, entrees, clot) in PANIERS.items():
        if jour not in dfs:
            df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_{jour}.parquet').sort_values('ts')
            df['mid'] = (df.bid + df.ask) / 2; dfs[jour] = df
        df = dfs[jour]
        prix = [mid_at(df, pd.Timestamp(t)) for t, _ in entrees]
        vols = [v for _, v in entrees]
        moy = float(np.average(prix, weights=vols))
        t_last, t_clot = pd.Timestamp(entrees[-1][0]), pd.Timestamp(clot)
        seg = df[(df.ts > t_last) & (df.ts <= t_clot)]
        au_dessus = seg[seg.mid >= moy]
        premier = str(au_dessus.ts.iloc[0]) if len(au_dessus) else None
        # episodes distincts au-dessus de la moyenne avant cloture
        signe = (seg.mid.values >= moy); episodes = int(np.sum((~signe[:-1]) & signe[1:])) + (1 if signe[0] else 0) if len(signe) else 0
        mid_clot = mid_at(df, t_clot)
        seg_all = df[(df.ts >= pd.Timestamp(entrees[0][0])) & (df.ts <= t_clot)]
        j = np.searchsorted(df.ts.values, np.datetime64(t_clot))
        def ret(s):
            k = np.searchsorted(df.ts.values, np.datetime64(t_clot) - np.timedelta64(s, 's'))
            return float((df.mid.values[j] / df.mid.values[k] - 1) * 10000)
        res['clotures'][nom] = {
            'prix_entrees_mid': [round(p, 2) for p in prix], 'prix_moyen_pondere': round(moy, 2),
            'premier_retour_au_dessus_moyenne': premier,
            'delai_premier_retour_s': round((pd.Timestamp(premier) - t_last).total_seconds(), 1) if premier else None,
            'episodes_au_dessus_avant_cloture': episodes,
            'mid_cloture_moins_moyenne_bp': round((mid_clot / moy - 1) * 10000, 2),
            'excursion_max_sous_moyenne_bp': round((seg_all.mid.min() / moy - 1) * 10000, 2) if len(seg_all) else None,
            'duree_reelle_s': (t_clot - pd.Timestamp(entrees[0][0])).total_seconds(),
            'cloture_minute_dans_bougie_M15': int(t_clot.minute % 15), 'cloture_seconde': int(t_clot.second),
            'ret60s_a_cloture_bp': round(ret(60), 2), 'ret300s_a_cloture_bp': round(ret(300), 2)}
    # X1: paniers V2 non apparies
    v2 = json.loads((R / 'research/COLORFUL-FILTER-001/REPLAY_V2_RESULTS.json').read_text())
    lab = json.loads((R / 'research/COLORFUL-FILTER-001/FILTER_LAB_RESULTS.json').read_text())
    appariees = {'2026-11-26 11:31', '2026-11-26 11:49', '2026-11-27 08:30', '2026-11-27 08:45', '2026-11-27 09:00'}
    for jour_cle, paniers in v2.items():
        for p in paniers:
            if p['t0'][:16] in appariees and jour_cle:  # apparie (tolerance large, verifie par ecarts seq448)
                continue
            res['extras_V2'].append({'t0': p['t0'], 'regle': p['regle'], 'nb': p['nb'],
                                     'duree_s': round(p['duree_s']), 'pnl': p['pnl_usd_unite']})
    (OUT / 'CLOSE_LAB_RESULTS.json').write_text(json.dumps(res, indent=1, default=str))
    print(pd.DataFrame(res['clotures']).T.to_string())
    print('\nExtras V2 (brut):'); print(pd.DataFrame(res['extras_V2']).to_string())

if __name__ == '__main__':
    main()
