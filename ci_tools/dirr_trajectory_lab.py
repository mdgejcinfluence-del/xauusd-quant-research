#!/usr/bin/env python3
"""DIRR-003 — trajectoires completes des paniers reels + contrefactuels a horizon
commun. Entrees reelles (heures affichees, UTC+2 suppose -> UTC), prix Mid au tick
Dukascopy (comparatifs, jamais HFM). PnL latent exprime en bp ponderes volume.
Contrefactuels: meme instant de sortie reelle, inventaire tronque (conditionnel,
non causal); premier retour PWA = scenario chiffre (regle deja refutee)."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/DEEP_INVENTORY_RECOVERY_003'; OUT.mkdir(parents=True, exist_ok=True)
PANIERS = {
 'A': ('2026-11-26', [('2026-11-26 11:31:20', .01), ('2026-11-26 11:32:00', .01), ('2026-11-26 11:35:00', .02)], '2026-11-26 11:50:32', 11),
 'B': ('2026-11-26', [('2026-11-26 11:50:34', .01), ('2026-11-26 11:51:03', .01), ('2026-11-26 12:01:01', .02)], '2026-11-26 12:02:29', 13),
 'C': ('2026-11-27', [('2026-11-27 08:30:00', .01), ('2026-11-27 08:30:20', .01), ('2026-11-27 08:33:34', .03)], '2026-11-27 08:40:50', -6),
 'D': ('2026-11-27', [('2026-11-27 08:45:00', .01)], '2026-11-27 08:45:17', 1),
 'E': ('2026-11-27', [('2026-11-27 09:00:00', .01), ('2026-11-27 09:00:16', .01)], '2026-11-27 09:01:27', 3)}

def mid_at(df, t):
    s = df[df.ts <= t]
    return float(s.mid.iloc[-1]) if len(s) else np.nan

def main():
    traj, cf = [], []
    for nom, (jour, entrees, clot, profit) in PANIERS.items():
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_{jour}.parquet').sort_values('ts')
        df['mid'] = (df.bid + df.ask) / 2
        prix = [mid_at(df, pd.Timestamp(t)) for t, _ in entrees]; vols = [v for _, v in entrees]
        t0, tc = pd.Timestamp(entrees[0][0]), pd.Timestamp(clot)
        seg = df[(df.ts >= t0) & (df.ts <= tc)].copy()
        # PWA dynamique et PnL latent (bp ponderes) a chaque tick
        pwa, pnl = [], []
        for ts in seg.ts:
            act = [(p, v) for (t, v), p in zip(entrees, prix) if pd.Timestamp(t) <= ts]
            V = sum(v for _, v in act); m = sum(p * v for p, v in act) / V
            pwa.append(m); pnl.append((float(seg[seg.ts == ts].mid.iloc[0]) / m - 1) * 10000)
        seg['pwa'] = pwa; seg['pnl_latent_bp'] = pnl
        sous = float((seg.pnl_latent_bp < 0).mean() * 100)
        traj.append({'panier': nom, 'regime_observe': 'IMMEDIATE' if (tc - t0).total_seconds() <= 120 and float(seg.pnl_latent_bp.min()) > -2 else 'INVENTORY_RECOVERY',
            'entrees': len(entrees), 'volumes': '/'.join(str(v) for v in vols), 'prix_entrees_mid': '/'.join(str(round(p, 2)) for p in prix),
            'pwa_final': round(pwa[-1], 2), 'mid_cloture': round(float(seg.mid.iloc[-1]), 2),
            'ecart_cloture_vs_pwa_bp': round(float(pnl[-1]), 2),
            'pnl_latent_min_bp': round(float(seg.pnl_latent_bp.min()), 2), 'pnl_latent_max_bp': round(float(seg.pnl_latent_bp.max()), 2),
            'temps_sous_pwa_pct': round(sous, 1), 'duree_s': (tc - t0).total_seconds(), 'profit_affiche_jpy': profit})
        # contrefactuels a meme instant de sortie (conditionnels)
        mid_c = float(seg.mid.iloc[-1])
        for k, etiquette in ((1, 'sans_renforcement (1 pos)'), (2, 'sans_3e (2 pos)')):
            if len(entrees) > k:
                V = sum(vols[:k]); m = sum(p * v for p, v in zip(prix[:k], vols[:k])) / V
                cf.append({'panier': nom, 'scenario': etiquette, 'horizon': 'cloture reelle (meme instant)',
                           'resultat_bp_pondere': round((mid_c / m - 1) * 10000, 2),
                           'resultat_reel_bp_pondere': round(float(pnl[-1]), 2)})
        # scenario premier retour PWA (regle deja refutee; chiffre seulement)
        apres = seg[seg.ts > pd.Timestamp(entrees[-1][0])]
        ret = apres[apres.pnl_latent_bp >= 0]
        cf.append({'panier': nom, 'scenario': 'cloture au premier retour PWA (scenario, regle refutee)',
                   'horizon': str(ret.ts.iloc[0]) if len(ret) else 'jamais avant cloture reelle',
                   'resultat_bp_pondere': 0.0 if len(ret) else None,
                   'resultat_reel_bp_pondere': round(float(pnl[-1]), 2)})
        seg[['ts', 'mid', 'pwa', 'pnl_latent_bp']].to_csv(OUT / f'TRAJECTORY_{nom}.csv', index=False)
    pd.DataFrame(traj).to_csv(OUT / 'REAL_BASKET_TRAJECTORY_ANALYSIS.csv', index=False)
    pd.DataFrame(cf).to_csv(OUT / 'COUNTERFACTUAL_SCENARIOS.csv', index=False)
    print(pd.DataFrame(traj).to_string()); print(); print(pd.DataFrame(cf).to_string())

if __name__ == '__main__':
    main()
