#!/usr/bin/env python3
"""GO-LIVE-001 (CI), protocole gele seq521. Familles NOUVELLES (dedup vs seq509-515):
post-impulsion directionnelle; efficacite range-vs-cloture; transitions de regime.
Mid uniquement. Segments: decouverte <=2016, validation 2017-2022, confirmation >=2023."""
import json, pathlib, subprocess
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/GO_LIVE_001'; OUT.mkdir(parents=True, exist_ok=True)

def segment(y): return 'decouverte' if y <= 2016 else ('validation' if y <= 2022 else 'confirmation')

def metrics(df):
    df = df.set_index('ts'); mid = (df.bid + df.ask) / 2
    b5 = mid.resample('5min').last().dropna()
    r = (b5.pct_change() * 10000).dropna(); a = r.abs()
    o = {}
    # (1) post-impulsion: |ret| >= d90 -> rendement suivant signe dans le sens de l'impulsion
    imp = a >= a.quantile(0.9)
    signed_next = (r.shift(-1) * np.sign(r))[imp]
    o['continuation_post_impulsion_bp'] = float(signed_next.mean()); o['n_impulsions'] = int(imp.sum())
    o['vol_apres_impulsion'] = float(a.shift(-1)[imp].mean()); o['vol_base'] = float(a.mean())
    # (2) representation: range 1min (high-low en bp) vs |ret| 1min pour predire vol 5min suivante
    b1 = mid.resample('1min').agg(['first', 'last', 'max', 'min']).dropna()
    rng = (b1['max'] - b1['min']) / b1['last'] * 10000
    nxt = a.reindex(b1.index, method='nearest')
    hi_r = rng >= rng.median(); hi_c = (b1['last'] - b1['first']).abs() / b1['last'] * 10000 >= ((b1['last'] - b1['first']).abs() / b1['last'] * 10000).median()
    o['volnext_range_haut'] = float(nxt[hi_r].mean()); o['volnext_range_bas'] = float(nxt[~hi_r].mean())
    o['volnext_close_haut'] = float(nxt[hi_c].mean()); o['volnext_close_bas'] = float(nxt[~hi_c].mean())
    # (3) transitions de regime (terciles d'amplitude 5min)
    q1, q2 = a.quantile(1/3), a.quantile(2/3)
    state = pd.cut(a, [-np.inf, q1, q2, np.inf], labels=[0, 1, 2]).astype(float)
    agite = state == 2; calme = state == 0; nxt_agite = agite.shift(-1)
    o['p_agite_apres_agite'] = float(nxt_agite[agite].mean()); o['p_agite_apres_calme'] = float(nxt_agite[calme].mean())
    return o

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    by_year = {}
    for p in inv['partitions']:
        by_year.setdefault(int(str(p['timestamp_min_footer'])[:4]), []).append(p)
    chosen = []
    for y in sorted(by_year):
        ps = by_year[y]; chosen.append(ps[0])
        if len(ps) > 2: chosen.append(ps[len(ps) // 2])
    csv_p = OUT / 'GO_LIVE_001_PARTITION_METRICS.csv'
    done = {}
    if csv_p.exists():  # reprise idempotente: ne retraiter que les partitions manquantes
        for r in pd.read_csv(csv_p).to_dict('records'):
            if r.get('statut') == 'OK': done[r['partition']] = r
    rows = list(done.values())
    for p in chosen:
        if p['name'] in done: continue
        y = int(str(p['timestamp_min_footer'])[:4]); local = pathlib.Path(f"/tmp/{p['name']}")
        def is_parquet(path):
            try:
                if p.get('file_bytes') and path.stat().st_size != p['file_bytes']: return False
                with open(path, 'rb') as f: return f.read(4) == b'PAR1'
            except Exception: return False
        ok_dl = False
        for attempt in range(3):
            subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, timeout=1800)
            if local.exists() and is_parquet(local): ok_dl = True; break
            if local.exists(): print('dl rejete (taille/magie)', p['name'], local.stat().st_size, 'attendu', p.get('file_bytes'), flush=True); local.unlink()
            try:  # repli: telechargement direct (patron kaggle_migrate.dl)
                import requests as rq
                url = f"https://drive.usercontent.google.com/download?id={p['drive_id']}&export=download&confirm=t"
                with rq.get(url, stream=True, timeout=600, headers={'User-Agent': 'Mozilla/5.0'}) as resp:
                    resp.raise_for_status()
                    with open(local, 'wb') as f:
                        for ch in resp.iter_content(1 << 20): f.write(ch)
                if local.exists() and is_parquet(local): ok_dl = True; break
            except Exception as e:
                print('dl echec', p['name'], 'tentative', attempt, type(e).__name__, flush=True)
        if not ok_dl:
            rows.append({'partition': p['name'], 'annee': y, 'segment': segment(y), 'statut': 'UNAVAILABLE'}); continue
        try:
            df = pd.read_parquet(local)  # schema variable selon les blocs du corpus (seq503)
            low = {c.lower(): c for c in df.columns}
            ts_c = next(low[k] for k in ('timestamp_utc', 'timestamp', 'ts', 'time', 'date') if k in low)
            df = df.rename(columns={ts_c: 'ts', low['bid']: 'bid', low['ask']: 'ask'})[['ts', 'bid', 'ask']]
            df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
            m = metrics(df); m.update(partition=p['name'], annee=y, segment=segment(y), ticks=int(len(df)), statut='OK')
            rows.append(m); print(p['name'], y, segment(y), flush=True)
        except Exception as e:  # jamais perdre la campagne pour une partition: statut diagnostique journalise
            rows.append({'partition': p['name'], 'annee': y, 'segment': segment(y), 'statut': f'ERROR_{type(e).__name__}'})
            print('erreur partition', p['name'], type(e).__name__, str(e)[:200], flush=True)
        local.unlink(missing_ok=True)
        pd.DataFrame(rows).to_csv(csv_p, index=False)  # checkpoint incremental
    pd.DataFrame(rows).to_csv(csv_p, index=False)
    print('termine', len(rows))

if __name__ == '__main__':
    main()
