#!/usr/bin/env python3
"""ME-003.1 (CI): continuation d'impulsion 5min, protocole seq490.
Trade dans le sens du mouvement, sorties a horizons fixes, Bid/Ask."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME003_IMPULSE_001'; OUT.mkdir(parents=True, exist_ok=True)
PARTS = {'part_000211.parquet': 'decouverte_2012', 'part_000250.parquet': 'decouverte_2016',
         'part_000289.parquet': 'validation_2020', 'part_000327.parquet': 'validation_2024',
         'part_000345.parquet': 'validation_2026'}
SEUILS = [5.0, 10.0, 20.0]
HOR = {900: '15m', 3600: '1h', 14400: '4h'}

def bars(df):
    df = df.set_index('ts'); m = (df.bid + df.ask) / 2
    return pd.DataFrame({'mid': m.resample('5s').first(), 'mid_max': m.resample('5s').max(), 'mid_min': m.resample('5s').min(),
                         'bid_last': df.bid.resample('5s').last(), 'ask_last': df.ask.resample('5s').last(),
                         'bid': df.bid.resample('5s').first(), 'ask': df.ask.resample('5s').first()}).dropna().reset_index()

def episodes(b, A):
    mid = b.mid.values; n = len(b); out = []; i = 60
    ret5 = np.full(n, np.nan); ret5[60:] = (mid[60:] / mid[:-60] - 1) * 10000
    while i < n:
        if np.isnan(ret5[i]) or abs(ret5[i]) < A:
            i += 1; continue
        sens = 'hausse' if ret5[i] > 0 else 'baisse'
        entry = b.ask.values[i] if sens == 'hausse' else b.bid.values[i]
        row = {'debut': str(b.ts[i]), 'seuil_bp': A, 'sens': sens, 'impulsion_bp': round(float(ret5[i]), 2)}
        seg_max = b.mid_max.values[i:min(n, i + 720)]; seg_min = b.mid_min.values[i:min(n, i + 720)]
        if sens == 'hausse':
            row['MFE_1h_bp'] = round(float((seg_max.max() / entry - 1) * 10000), 2)
            row['MAE_1h_bp'] = round(float((seg_min.min() / entry - 1) * 10000), 2)
            row['continuation_1h'] = bool((seg_max.max() / mid[i] - 1) * 10000 >= A / 2)
        else:
            row['MFE_1h_bp'] = round(float((entry / seg_min.min() - 1) * 10000), 2)
            row['MAE_1h_bp'] = round(float((entry / seg_max.max() - 1) * 10000), 2)
            row['continuation_1h'] = bool((mid[i] / seg_min.min() - 1) * 10000 >= A / 2)
        for h, lab in HOR.items():
            k = min(n - 1, i + h // 5)
            xp = b.bid_last.values[k] if sens == 'hausse' else b.ask_last.values[k]
            brut = (xp / entry - 1) * 10000 if sens == 'hausse' else (entry / xp - 1) * 10000
            row[f'edge_{lab}_bp'] = round(float(brut), 2)
            row[f'edge_{lab}_central_bp'] = round(float(brut - 1.2), 2)
        out.append(row)
        i += 720  # refroidissement 1h
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
    pd.DataFrame(rows).to_csv(OUT / 'ME003_EPISODE_CATALOG.csv', index=False)
    print('TOTAL', len(rows))

if __name__ == '__main__':
    main()
