#!/usr/bin/env python3
"""AESR-002 — laboratoire de mecanismes economiques (donnees existantes uniquement).
E1 retours forward apres entrees (reelles A-E et simulees V1 nov.); E2 trajectoires
des paniers reels (MAE, temps sous le prix moyen); E3 arithmetique du profil public;
E4 capture de mouvement des paniers simules. Ticks Dukascopy comparatifs, jamais HFM.
Aucune inference market-making (carnet non observable)."""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay import rejouer

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/AUTONOMOUS_ECONOMIC_RECONSTRUCTION_002'; OUT.mkdir(parents=True, exist_ok=True)
REELLES = {'A': ('2026-11-26', '2026-11-26 11:31:20', '2026-11-26 11:50:32'),
           'B': ('2026-11-26', '2026-11-26 11:50:34', '2026-11-26 12:02:29'),
           'C': ('2026-11-27', '2026-11-27 08:30:00', '2026-11-27 08:40:50'),
           'D': ('2026-11-27', '2026-11-27 08:45:00', '2026-11-27 08:45:17'),
           'E': ('2026-11-27', '2026-11-27 09:00:00', '2026-11-27 09:01:27')}
HORIZONS = (60, 300, 900)

def charge(jour):
    df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_{jour}.parquet').sort_values('ts')
    df['mid'] = (df.bid + df.ask) / 2
    return df

def fwd(df, t, s):
    a = df[df.ts <= t]; b = df[df.ts <= t + pd.Timedelta(seconds=s)]
    if not len(a) or not len(b): return None
    return round(float((b.mid.iloc[-1] / a.mid.iloc[-1] - 1) * 10000), 2)

def main():
    res = {'E1_reelles': {}, 'E2_reelles': {}, 'E1_simulees': {}, 'E3_profil': {}}
    dfs = {}
    for nom, (jour, t0, tc) in REELLES.items():
        df = dfs.setdefault(jour, charge(jour))
        t0, tc = pd.Timestamp(t0), pd.Timestamp(tc)
        res['E1_reelles'][nom] = {f'fwd{s}s_bp': fwd(df, t0, s) for s in HORIZONS} | {'a_cloture_bp': fwd(df, t0, (tc - t0).total_seconds())}
        seg = df[(df.ts >= t0) & (df.ts <= tc)]
        p1 = float(df[df.ts <= t0].mid.iloc[-1])
        res['E2_reelles'][nom] = {'mae_vs_entree_bp': round(float((seg.mid.min() / p1 - 1) * 10000), 2),
            'mfe_vs_entree_bp': round(float((seg.mid.max() / p1 - 1) * 10000), 2),
            'part_temps_sous_prix_entree_pct': round(float(100 * (seg.mid < p1).mean()), 1),
            'duree_s': (tc - t0).total_seconds()}
    fw = {s: [] for s in HORIZONS}
    for j in ('20', '22', '23', '24', '25', '26', '27'):
        df = charge(f'2026-11-{j}')
        for x in rejouer(df, df.ts.min(), df.ts.max()):
            for s in HORIZONS:
                v = fwd(df, x['t0'], s)
                if v is not None: fw[s].append(v)
    for s in HORIZONS:
        a = pd.Series(fw[s])
        res['E1_simulees'][f'fwd{s}s'] = {'n': len(a), 'moyenne_bp': round(float(a.mean()), 2),
            'mediane_bp': round(float(a.median()), 2), 'part_positifs_pct': round(float(100 * (a > 0).mean()), 1)}
    res['E3_profil'] = {'esperance_par_transaction_affichee_jpy': round(0.674 * 22.37 - 0.326 * 27.82, 2),
        'ratio_gain_moyen_sur_perte_moyenne': round(22.37 / 27.82, 3),
        'lecture': 'esperance affichee positive portee par la frequence (67.4%) malgre un gain moyen inferieur a la perte moyenne: signature compatible avec un mecanisme a haute frequence de petits gains et queue negative, non une preuve'}
    (OUT / 'MECHANISM_RESULTS.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    main()
