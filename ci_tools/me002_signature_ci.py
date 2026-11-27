#!/usr/bin/env python3
"""ME-002.1 (CI): episodes de desequilibre temporaire vs mediane 15min
(protocole seq488). Fade executable Bid/Ask, couts comptes une fois."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME002_DISLOCATION_001'; OUT.mkdir(parents=True, exist_ok=True)
PARTS = {'part_000211.parquet': 'decouverte_2012', 'part_000250.parquet': 'decouverte_2016',
         'part_000289.parquet': 'validation_2020', 'part_000327.parquet': 'validation_2024',
         'part_000345.parquet': 'validation_2026'}
SEUILS = [5.0, 10.0, 20.0]

def bars(df):
    df = df.set_index('ts'); m = (df.bid + df.ask) / 2
    return pd.DataFrame({'mid': m.resample('5s').first(), 'bid': df.bid.resample('5s').first(),
                         'ask': df.ask.resample('5s').first(),
                         'bid_last': df.bid.resample('5s').last(), 'ask_last': df.ask.resample('5s').last()}).dropna().reset_index()

def episodes(b, A):
    mid = b.mid.values; n = len(b)
    med = pd.Series(mid).rolling(180, min_periods=180).median().shift(1).values
    out = []; i = 180
    while i < n:
        if np.isnan(med[i]) or abs(mid[i] / med[i] - 1) * 10000 < A:
            i += 1; continue
        sens = 'pic' if mid[i] > med[i] else 'creux'
        ref = med[i]; start = i
        entry = b.bid.values[i] if sens == 'pic' else b.ask.values[i]
        j = i; touche = None
        while j < min(n, start + 2880):
            if (sens == 'pic' and mid[j] <= ref) or (sens == 'creux' and mid[j] >= ref):
                touche = j; break
            j += 1
        end = touche if touche is not None else min(n - 1, start + 2880)
        exitp = (b.ask_last.values[end] if sens == 'pic' else b.bid_last.values[end])
        brut = ((entry - exitp) / entry * 10000) if sens == 'pic' else ((exitp - entry) / entry * 10000)
        out.append({'debut': str(b.ts[start]), 'seuil_bp': A, 'sens': sens,
                    'ecart_initial_bp': round(float((mid[start] / ref - 1) * 10000), 2),
                    'resorbe': touche is not None,
                    'duree_s': float((b.ts[end] - b.ts[start]) / np.timedelta64(1, 's')),
                    'edge_spread_inclus_bp': round(float(brut), 2), 'edge_central_bp': round(float(brut - 1.2), 2)})
        i = end + 1 if end > start else i + 1
    return out

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    by = {p['name']: p for p in inv['partitions']}; rows = []
    for name, seg in PARTS.items():
        local = pathlib.Path(f'/tmp/{name}')
        subprocess.run(['gdown', '-q', '--output', str(local), by[name]['drive_id']], capture_output=True, timeout=1200)
        df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
        df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
        b = bars(df)
        for A in SEUILS:
            eps = episodes(b, A)
            for e in eps: e.update(partition=name, segment=seg)
            rows += eps; print(name, seg, A, len(eps), flush=True)
        local.unlink(missing_ok=True)
    pd.DataFrame(rows).to_csv(OUT / 'ME002_EPISODE_CATALOG.csv', index=False)
    print('TOTAL', len(rows))

if __name__ == '__main__':
    main()
