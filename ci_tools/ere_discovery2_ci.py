#!/usr/bin/env python3
"""EXPANSION-001 (CI): campagne independante n.2, echantillonnage par annee civile.
Familles gelees seq514: activite tick -> volatilite suivante; sequence de
3 barres 5min de meme signe -> rendement suivant; rafale de volatilite
(decile haut) -> amplitude suivante vs base. Segments par annee."""
import json, pathlib, subprocess
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ERE_INTEL3'; OUT.mkdir(parents=True, exist_ok=True)

def segment(y): return 'decouverte' if y <= 2016 else ('validation' if y <= 2022 else 'confirmation')

def metrics(df):
    df = df.set_index('ts'); mid = (df.bid + df.ask) / 2
    b5 = mid.resample('5min').last().dropna()
    cnt = df['bid'].resample('5min').count().reindex(b5.index).fillna(0)
    r = b5.pct_change() * 10000; a = r.abs()
    out = {}
    # activite -> volatilite suivante (correlation de rang par terciles)
    hi = cnt >= cnt.quantile(0.66); lo = cnt <= cnt.quantile(0.33)
    out['vol_apres_forte_activite'] = float(a.shift(-1)[hi].mean()); out['vol_apres_faible_activite'] = float(a.shift(-1)[lo].mean())
    # sequence de 3 signes identiques -> rendement suivant
    s = np.sign(r); seq = (s == s.shift(1)) & (s == s.shift(2))
    out['ret_apres_3_hausses'] = float(r.shift(-1)[seq & (s > 0)].mean()); out['n_seq_hausses'] = int((seq & (s > 0)).sum())
    out['ret_apres_3_baisses'] = float(r.shift(-1)[seq & (s < 0)].mean()); out['n_seq_baisses'] = int((seq & (s < 0)).sum())
    # rafale (decile haut de volatilite) -> amplitude suivante vs base
    raf = a >= a.quantile(0.9)
    out['vol_apres_rafale'] = float(a.shift(-1)[raf].mean()); out['vol_base'] = float(a.mean())
    return out

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    by_year = {}
    for p in inv['partitions']:
        y = int(str(p['timestamp_min_footer'])[:4])
        by_year.setdefault(y, []).append(p)
    chosen = []
    for y in sorted(by_year):
        ps = by_year[y]
        chosen.append(ps[0])
        if len(ps) > 2: chosen.append(ps[len(ps) // 2])
    rows = []
    for p in chosen:
        y = int(str(p['timestamp_min_footer'])[:4]); local = pathlib.Path(f"/tmp/{p['name']}")
        subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, timeout=1800)
        if not local.exists():
            rows.append({'partition': p['name'], 'annee': y, 'segment': segment(y), 'statut': 'UNAVAILABLE'}); continue
        df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
        df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
        m = metrics(df); m.update(partition=p['name'], annee=y, segment=segment(y), ticks=int(len(df)), statut='OK')
        rows.append(m); print(p['name'], y, segment(y), flush=True)
        local.unlink(missing_ok=True)
    pd.DataFrame(rows).to_csv(OUT / 'ERE_INTEL3_PARTITION_METRICS.csv', index=False)
    print('termine', len(rows))

if __name__ == '__main__':
    main()
