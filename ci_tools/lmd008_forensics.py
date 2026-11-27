#!/usr/bin/env python3
"""LMD-008: statistiques de trajectoire a posteriori des paniers geles
(MFE/MAE vs PWA final, fraction du temps sous le PWA final, rendements
forward depuis l entree) calculees sur ticks, sans modifier les moteurs.
Modes: ci (partitions certifiees via gdown) / local (novembre du repo).
Approximation declaree: PWA final constant (le PWA historique variait aux
renforcements); statistiques descriptives, pas une re-simulation."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/LOSS_MECHANISM_DIAGNOSIS_008'; OUT.mkdir(parents=True, exist_ok=True)
HORIZONS = [30, 60, 300, 900, 1800, 3600, 14400]

def stats_for(df, B, moteur):
    ts = df.ts.values; mid = ((df.bid + df.ask) / 2).values
    rows = []
    for x in B.itertuples():
        t0 = np.datetime64(x.t0); tc = np.datetime64(x.cloture)
        i0 = np.searchsorted(ts, t0); i1 = np.searchsorted(ts, tc)
        if i1 <= i0: continue
        seg = mid[i0:i1 + 1]; pwa = x.prix_moyen
        row = {'moteur': moteur, 't0': x.t0, 'cloture': x.cloture, 'nb_positions': x.nb_positions,
               'duree_s': x.duree_s, 'pnl_net_usd_S0': x.pnl_net_usd_S0,
               'MFE_bp_vs_pwa_final': round(float((seg.max() / pwa - 1) * 10000), 2),
               'MAE_bp_vs_pwa_final': round(float((seg.min() / pwa - 1) * 10000), 2),
               'frac_ticks_sous_pwa_final': round(float((seg < pwa).mean()), 3),
               'atteint_pwa_final_avant_cloture': bool(seg.max() >= pwa)}
        for h in HORIZONS:
            j = np.searchsorted(ts, t0 + np.timedelta64(h, 's'))
            row[f'fwd_{h}s_bp'] = round(float((mid[j] / mid[i0] - 1) * 10000), 2) if j < len(ts) and j > i0 else None
        rows.append(row)
    return pd.DataFrame(rows)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'local'
    frames = []
    if mode == 'ci':
        V1 = pd.read_csv(R / 'docs/checkpoints/FULL_REPLAY_2026/META_ALPHA_BASKETS_2026.csv')
        V2 = pd.read_csv(R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001/CI_V2_BASKETS_JAN_SEP.csv')
        inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
        parts = [p for p in inv['partitions'] if (p.get('timestamp_min_footer') or '') >= '2026-01-01']
        for p in parts:
            local = pathlib.Path(f"/tmp/{p['name']}")
            subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, timeout=1200)
            df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
            df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
            frames.append(stats_for(df, V1[V1.partition == p['name']], 'V1'))
            frames.append(stats_for(df, V2[V2.partition == p['name']], 'V2-F2'))
            print(p['name'], 'ok', flush=True); local.unlink(missing_ok=True)
        pd.concat(frames).to_csv(OUT / 'CI_PATH_STATS_JAN_SEP.csv', index=False)
    else:
        V1 = pd.read_csv(R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001/BACKTEST_V1_RESULTS.csv')
        V2 = pd.read_csv(R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001/BACKTEST_V2_F2_RESULTS.csv')
        for j in ('20', '22', '23', '24', '25', '26', '27'):
            df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
            frames.append(stats_for(df, V1[V1.t0.str.startswith(f'2026-11-{j}')], 'V1'))
            frames.append(stats_for(df, V2[V2.t0.str.startswith(f'2026-11-{j}')], 'V2-F2'))
        pd.concat(frames).to_csv(OUT / 'NOV_PATH_STATS.csv', index=False)
    print('DONE')

if __name__ == '__main__':
    main()
