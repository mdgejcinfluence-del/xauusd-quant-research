#!/usr/bin/env python3
"""ME-001.2 (CI): trajectoires et signatures precoces des episodes seq480.
Memes episodes; enregistre horizons, caracteristiques aux points de
controle, issues des familles de sortie fixees (seq482). Causal strict."""
import json, pathlib, subprocess, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_NONRECOVERY_002'; OUT.mkdir(parents=True, exist_ok=True)
PARTS = {'part_000211.parquet': 'decouverte_2012', 'part_000250.parquet': 'decouverte_2016',
         'part_000289.parquet': 'validation_2020', 'part_000327.parquet': 'validation_2024',
         'part_000345.parquet': 'validation_2026'}
SEUILS = [5.0, 10.0, 20.0]
HOR = [10, 30, 60, 300, 900, 1800, 3600, 14400, 86400]
TAUS = [60, 300, 900]

def bars(df):
    df = df.set_index('ts'); m = (df.bid + df.ask) / 2
    return pd.DataFrame({'mid_first': m.resample('5s').first(), 'mid_max': m.resample('5s').max(),
                         'mid_min': m.resample('5s').min(), 'ask_first': df.ask.resample('5s').first(),
                         'bid_last': df.bid.resample('5s').last()}).dropna().reset_index()

def analyse(b):
    mid = b.mid_first.values; t = b.ts.values; n = len(b)
    ref = pd.Series(mid).rolling(180, min_periods=180).max().shift(1).values
    bid = b.bid_last.values; ask = b.ask_first.values
    rows = []
    for A in SEUILS:
        i = 180
        while i < n:
            if np.isnan(ref[i]) or mid[i] > ref[i] * (1 - A / 10000):
                i += 1; continue
            R0 = ref[i]; start = i; entry = ask[i]
            jmax = min(n - 1, start + 17280)  # 24h en barres 5s
            seg_mid = mid[start:jmax + 1]; seg_min = b.mid_min.values[start:jmax + 1]
            depth_run = np.minimum.accumulate(seg_min)
            # retracement fraction vs profondeur courante
            denom = (R0 - depth_run); denom[denom <= 0] = np.nan
            frac = (seg_mid - depth_run) / denom
            rec_idx = np.argmax(seg_mid >= R0) if (seg_mid >= R0).any() else None
            if rec_idx == 0: rec_idx = None
            end = rec_idx if rec_idx is not None else len(seg_mid) - 1
            raison = 'recupere' if rec_idx is not None else ('horizon_24h' if jmax - start >= 17280 else 'censure_fin_partition')
            row = {'debut': str(b.ts[start]), 'seuil_bp': A, 'reference': round(float(R0), 2),
                   'prix_declenchement': round(float(mid[start]), 2), 'raison_fin': raison,
                   'profondeur_max_bp': round(float((depth_run[end] / R0 - 1) * 10000), 2),
                   'duree_s': float((t[start + end] - t[start]) / np.timedelta64(1, 's')),
                   'recupere_24h': raison == 'recupere'}
            for h in HOR:
                k = start + h // 5
                row[f'rend_{h}s_bp'] = round(float((mid[k] / R0 - 1) * 10000), 2) if k <= start + end else None
            # baseline: sortie recuperation ou 4h
            def prix_sortie(idx): return bid[start + min(idx, len(seg_mid) - 1)]
            k4 = min(2880, len(seg_mid) - 1)
            base_idx = rec_idx if rec_idx is not None else k4
            row['edge_baseline_bp'] = round(float((prix_sortie(base_idx) / entry - 1) * 10000 - 1.2), 2)
            # familles de sortie fixees
            def edge_si(idx): return round(float((prix_sortie(idx) / entry - 1) * 10000 - 1.2), 2)
            row['edge_sortie_1h_bp'] = edge_si(rec_idx if (rec_idx is not None and rec_idx <= 720) else 720)
            for X in (30, 50, 80):
                viol = np.argmax(seg_min <= R0 * (1 - X / 10000)) if (seg_min <= R0 * (1 - X / 10000)).any() else None
                idx = viol if (viol is not None and (rec_idx is None or viol < rec_idx)) else base_idx
                row[f'edge_sortie_excursion_{X}bp'] = edge_si(idx)
            # non-amelioration: apres 300s, 900s sans nouveau max de frac
            idx_na = base_idx
            if len(seg_mid) > 240:
                f = np.nan_to_num(frac, nan=0.0); runmax = np.maximum.accumulate(f)
                last_imp = 0
                for k in range(60, len(seg_mid)):
                    if f[k] >= runmax[k] - 1e-12: last_imp = k
                    if k - last_imp >= 180:
                        idx_na = k; break
                if rec_idx is not None and rec_idx < idx_na: idx_na = rec_idx
            row['edge_sortie_nonamelioration_bp'] = edge_si(idx_na)
            # caracteristiques aux points de controle + drapeau seq482
            for tau in TAUS:
                k = tau // 5
                if k < len(seg_mid):
                    fmax = float(np.nanmax(frac[:k + 1])) if k >= 0 else 0.0
                    # temps depuis derniere amelioration
                    f = np.nan_to_num(frac[:k + 1], nan=0.0); rm = np.maximum.accumulate(f)
                    imp = np.where(f >= rm - 1e-12)[0]
                    row[f'frac_max_{tau}s'] = round(fmax, 3)
                    row[f'profondeur_{tau}s_bp'] = round(float((depth_run[k] / R0 - 1) * 10000), 2)
                    row[f'sans_amelioration_{tau}s_s'] = int((k - (imp[-1] if len(imp) else 0)) * 5)
                    row[f'drapeau_{tau}s'] = bool(fmax < 0.25 and (depth_run[k] / R0 - 1) * 10000 <= -2 * A)
                    row[f'edge_drapeau_{tau}s_bp'] = edge_si(k) if row[f'drapeau_{tau}s'] else None
                else:
                    row[f'drapeau_{tau}s'] = None
            rows.append(row)
            i = start + end + 1 if end > 0 else i + 1
    return rows

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    by = {p['name']: p for p in inv['partitions']}; allr = []
    for name, seg in PARTS.items():
        local = pathlib.Path(f'/tmp/{name}')
        subprocess.run(['gdown', '-q', '--output', str(local), by[name]['drive_id']], capture_output=True, timeout=1200)
        df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
        df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
        rr = analyse(bars(df))
        for r in rr: r.update(partition=name, segment=seg)
        allr += rr; print(name, seg, len(rr), flush=True); local.unlink(missing_ok=True)
    pd.DataFrame(allr).to_csv(OUT / 'ME001_EPISODE_TRAJECTORIES.csv', index=False)
    print('TOTAL', len(allr))

if __name__ == '__main__':
    main()
