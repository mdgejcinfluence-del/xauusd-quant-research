#!/usr/bin/env python3
"""ERE-INTELLIGENCE-002 (CI): decouverte independante sur corpus certifie.
Protocole gele seq510: 12 partitions stratifiees, segments par annee,
6 familles descriptives au Mid. Aucune strategie, aucun seuil optimise."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ERE_INTEL2'; OUT.mkdir(parents=True, exist_ok=True)

def segment(year):
    return 'decouverte' if year <= 2016 else ('validation' if year <= 2022 else 'confirmation')

def metrics(df):
    df = df.set_index('ts'); mid = (df.bid + df.ask) / 2
    b1 = mid.resample('1min').last().dropna(); b5 = mid.resample('5min').last().dropna()
    r1 = b1.pct_change() * 10000; r5 = b5.pct_change() * 10000
    out = {}
    nxt = r5.shift(-1).abs()
    out['asym_vol_apres_hausse'] = float(nxt[r5 > 0].mean()); out['asym_vol_apres_baisse'] = float(nxt[r5 < 0].mean())
    ext = r1.abs() >= 10; nxt1 = r1.shift(-1)
    out['bounce_part_reversion'] = float((np.sign(nxt1[ext]) != np.sign(r1[ext])).mean()) if ext.sum() else np.nan
    out['bounce_n'] = int(ext.sum())
    a = r5.abs().dropna()
    out['vol_clustering_acf1'] = float(a.autocorr(1)) if len(a) > 10 else np.nan
    s = np.sign(r5.dropna())
    out['sign_persistence'] = float((s == s.shift(1)).mean()) if len(s) > 10 else np.nan
    q = a.quantile(0.2); low = a <= q
    out['expansion_apres_contraction'] = float(a.shift(-1)[low].mean()); out['expansion_base'] = float(a.mean())
    hourly = r5.abs().groupby(b5.index.hour).mean()
    out['heure_vol_max'] = int(hourly.idxmax()); out['heure_vol_min'] = int(hourly.idxmin())
    out['ratio_vol_max_min'] = float(hourly.max() / hourly.min()) if hourly.min() > 0 else np.nan
    out['n_barres_5min'] = int(len(b5)); out['spread_moyen_bp'] = float(((df.ask - df.bid) / mid * 10000).mean())
    return out

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    parts = inv['partitions'][::29][:12]
    rows = []
    for p in parts:
        local = pathlib.Path(f"/tmp/{p['name']}")
        subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, timeout=1800)
        if not local.exists():
            rows.append({'partition': p['name'], 'statut': 'UNAVAILABLE'}); continue
        df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
        df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
        year = int(str(p['timestamp_min_footer'])[:4])
        m = metrics(df); m.update(partition=p['name'], segment=segment(year), annee=year, ticks=int(len(df)), statut='OK')
        rows.append(m); print(p['name'], year, m['segment'], 'ticks', len(df), flush=True)
        local.unlink(missing_ok=True)
    pd.DataFrame(rows).to_csv(OUT / 'ERE_INTEL2_PARTITION_METRICS.csv', index=False)
    print('termine', len(rows))

if __name__ == '__main__':
    main()
