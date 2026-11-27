#!/usr/bin/env python3
"""ME-001.1 (CI): detection des episodes de recuperation, protocole seq480.
Barres 5s depuis ticks certifies (gdown), reference causale max 15min,
episodes non chevauchants, edge executif Bid/Ask compte une fois."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_RECOVERY_SIGNATURE_001'; OUT.mkdir(parents=True, exist_ok=True)
PARTS = {'part_000211.parquet': 'decouverte_2012', 'part_000250.parquet': 'decouverte_2016',
         'part_000289.parquet': 'validation_2020', 'part_000327.parquet': 'validation_2024',
         'part_000345.parquet': 'validation_2026'}
SEUILS = [5.0, 10.0, 20.0]
HORIZONS = [300, 900, 3600, 14400, 86400]

def bars(df):
    df = df.set_index('ts')
    m = (df.bid + df.ask) / 2
    b = pd.DataFrame({'mid_first': m.resample('5s').first(), 'mid_max': m.resample('5s').max(),
                      'mid_min': m.resample('5s').min(), 'ask_first': df.ask.resample('5s').first(),
                      'bid_last': df.bid.resample('5s').last(), 'ask_last': df.ask.resample('5s').last(),
                      'bid_first': df.bid.resample('5s').first()}).dropna()
    return b.reset_index()

def episodes(b, A):
    mid = b.mid_first.values; t = b.ts.values
    ref = pd.Series(mid).rolling(180, min_periods=180).max().values  # 15min causal (barres passees incl. courante: max sur fenetre terminee a la barre precedente via shift)
    ref = np.roll(ref, 1); ref[:180] = np.nan
    vol15 = pd.Series(mid).rolling(180, min_periods=180).std().values / mid * 10000
    vol15 = np.roll(vol15, 1)
    out = []; i = 180
    n = len(b)
    while i < n:
        if np.isnan(ref[i]) or mid[i] > ref[i] * (1 - A / 10000):
            i += 1; continue
        R0 = ref[i]; start = i; entry_ask = b.ask_first.values[i]
        depth = mid[i]; j = i
        rec = {}
        while j < n and (t[j] - t[start]) / np.timedelta64(1, 's') <= 86400:
            depth = min(depth, b.mid_min.values[j])
            disp = R0 - (R0 * (1 - A / 10000))
            frac = (mid[j] - depth) / (R0 - depth) if R0 > depth else 1.0
            for f in (0.25, 0.5, 0.75, 1.0):
                if f not in rec and frac >= f: rec[f] = (t[j] - t[start]) / np.timedelta64(1, 's')
            if mid[j] >= R0: break
            j += 1
        duree = (t[min(j, n - 1)] - t[start]) / np.timedelta64(1, 's')
        # edge executif: sortie au bid a recuperation complete, sinon au bid a 4h
        k4 = np.searchsorted(t, t[start] + np.timedelta64(14400, 's'))
        if 1.0 in rec:
            kk = start + int(rec[1.0] // 5); exit_bid = b.bid_last.values[min(kk, n - 1)]; mode_sortie = 'recuperation'
        else:
            exit_bid = b.bid_last.values[min(k4, n - 1)]; mode_sortie = 'horizon_4h'
        brut_bp = (exit_bid / entry_ask - 1) * 10000
        out.append({'debut': str(b.ts[start]), 'seuil_bp': A, 'reference': round(float(R0), 2),
                    'profondeur_max_bp': round(float((depth / R0 - 1) * 10000), 2),
                    'duree_episode_s': float(duree), 'vol15_bp': round(float(vol15[start]), 2) if not np.isnan(vol15[start]) else None,
                    **{f'temps_retracement_{int(f*100)}pct_s': rec.get(f) for f in (0.25, 0.5, 0.75, 1.0)},
                    **{f'recupere_{h}s': bool(rec.get(1.0, 10**18) <= h) for h in HORIZONS},
                    'mode_sortie_edge': mode_sortie, 'edge_net_spread_inclus_bp': round(float(brut_bp), 2),
                    'edge_net_central_bp': round(float(brut_bp - 1.2), 2)})
        i = max(j, i + 1)
    return out

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    by_name = {p['name']: p for p in inv['partitions']}
    all_eps = []
    for name, segment in PARTS.items():
        p = by_name[name]; local = pathlib.Path(f'/tmp/{name}')
        subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, timeout=1200)
        df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
        df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
        b = bars(df)
        for A in SEUILS:
            eps = episodes(b, A)
            for e in eps: e.update(partition=name, segment=segment)
            all_eps += eps
            print(name, segment, 'A=', A, 'episodes', len(eps), flush=True)
        local.unlink(missing_ok=True)
    E = pd.DataFrame(all_eps)
    E.to_csv(OUT / 'ME001_EPISODE_CATALOG.csv', index=False)
    print('TOTAL', len(E))

if __name__ == '__main__':
    main()
