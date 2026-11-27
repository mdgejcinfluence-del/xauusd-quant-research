#!/usr/bin/env python3
"""ME-001.4: collecte prospective (categorie D) des ticks Dukascopy
posterieurs au gel seq484 (2026-11-27). Enregistre couverture + SHA-256
par jour dans le registre du checkpoint; les ticks ne sont jamais
commites et aucune performance n'est calculee (regle seq486)."""
import hashlib, json, pathlib, sys
import pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from edge02_dukascopy import telecharger_heure, qualite

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_PROSPECTIVE_004'; OUT.mkdir(parents=True, exist_ok=True)
GEL = pd.Timestamp('2026-11-27')

def main():
    debut = pd.Timestamp(sys.argv[1]) if len(sys.argv) > 1 else (pd.Timestamp.utcnow().tz_localize(None).normalize() - pd.Timedelta(days=2))
    fin = pd.Timestamp(sys.argv[2]) if len(sys.argv) > 2 else pd.Timestamp.utcnow().tz_localize(None).floor('h')
    reg_p = OUT / 'ME001_PROSPECTIVE_REGISTRY.csv'
    reg = pd.read_csv(reg_p) if reg_p.exists() else pd.DataFrame(columns=['jour', 'ticks', 'sha256_parquet', 'collecte_le', 'categorie', 'statut'])
    deja = set(reg.jour.astype(str))
    rows = []
    for jour in pd.date_range(debut.normalize(), fin.normalize(), freq='D'):
        js = str(jour.date())
        if js in deja: continue
        frames = []
        for h in pd.date_range(jour, jour + pd.Timedelta(hours=23), freq='h'):
            df = telecharger_heure(h)
            if df is not None and len(df): frames.append(df)
        if not frames:
            rows.append({'jour': js, 'ticks': 0, 'sha256_parquet': None, 'collecte_le': str(pd.Timestamp.utcnow()),
                         'categorie': 'D' if jour > GEL else 'C', 'statut': 'AUCUNE_DONNEE_PUBLIEE'}); continue
        day = pd.concat(frames).drop_duplicates('ts').sort_values('ts')
        tmp = pathlib.Path(f'/tmp/duka_{js}.parquet'); day.to_parquet(tmp, index=False)
        sha = hashlib.sha256(tmp.read_bytes()).hexdigest(); tmp.unlink()
        rows.append({'jour': js, 'ticks': int(len(day)), 'sha256_parquet': sha, 'collecte_le': str(pd.Timestamp.utcnow()),
                     'categorie': 'D' if jour > GEL else 'C', 'statut': 'COLLECTE'})
        print(js, len(day), sha[:12], flush=True)
    if rows: reg = pd.concat([reg, pd.DataFrame(rows)], ignore_index=True)
    reg.to_csv(reg_p, index=False)
    print('registre:', len(reg), 'jours')

if __name__ == '__main__':
    main()
