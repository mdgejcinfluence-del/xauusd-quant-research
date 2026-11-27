#!/usr/bin/env python3
"""BACKTEST-2026-001 (CI): rejeu du moteur V2-F2 GELE (import sans modification)
sur les partitions certifiees 2026 (342-348) telechargees via gdown, meme
protocole que DATA-RECOVERY-2026 (seq456-457). Les partitions ne sont jamais
commitees. Sorties: paniers V2 + audit de couverture, dans le checkpoint
BACKTEST_2026_FULL_PERIOD_001. Aucun parametre modifie."""
import hashlib, json, pathlib, subprocess, sys
import pandas as pd
import pyarrow.parquet as pq
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay_v2 import rejouer

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001'; OUT.mkdir(parents=True, exist_ok=True)
LOG = open(OUT / 'CI_V2_LOG.txt', 'w')
def log(*a): print(*a); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    parts = [p for p in inv['partitions'] if (p.get('timestamp_min_footer') or '') >= '2026-01-01']
    log('partitions 2026:', len(parts))
    audit, paniers_tous = [], []
    for p in parts:
        local = pathlib.Path(f"/tmp/{p['name']}")
        ligne = {'partition': p['name'], 'drive_id': p['drive_id'], 'taille_attendue': p['file_bytes'], 'lignes_attendues': p['rows']}
        try:
            r = subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, text=True, timeout=1200)
            if not local.exists() or local.stat().st_size == 0:
                ligne.update(statut='UNAVAILABLE', erreur=(r.stderr or r.stdout)[-300:]); audit.append(ligne); continue
            sha = hashlib.sha256(local.read_bytes()).hexdigest()
            meta = pq.ParquetFile(local).metadata
            ligne.update(sha256=sha, lignes_observees=meta.num_rows,
                         statut='VERIFIED' if (local.stat().st_size == p['file_bytes'] and meta.num_rows == p['rows']) else 'VERIFIED_WITH_DIFFERENCES')
            df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask']).rename(columns={'timestamp_utc': 'ts'})
            df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
            ligne.update(debut=str(df.ts.min()), fin=str(df.ts.max()), doublons=int(df.ts.duplicated().sum()),
                         spread_median_bp=round(float(((df.ask - df.bid) / ((df.ask + df.bid) / 2) * 10000).median()), 2))
            paniers = rejouer(df, df.ts.min(), df.ts.max())
            for x in paniers:
                vol = sum(v for _, v, _ in x['entrees'])
                paniers_tous.append({'partition': p['name'], 't0': str(x['t0']), 'cloture': str(x['cloture']),
                    'mois_cloture': str(x['cloture'])[:7], 'regle': x['regle'], 'nb_positions': x['nb'],
                    'volume_total': round(vol, 2), 'prix_moyen': round(x['prix_moyen'], 2),
                    'duree_s': round(x['duree_s'], 1), 'pnl_net_usd_S0': x['pnl_usd_unite'], 'renforcements': x['nb'] - 1})
            ligne['paniers_V2'] = len(paniers); log(p['name'], ligne['statut'], 'V2 paniers', len(paniers))
            del df
        except Exception as e:
            ligne.update(statut='UNAVAILABLE', erreur=f'{type(e).__name__}: {e}'); log(p['name'], 'ERREUR', e)
        audit.append(ligne); local.unlink(missing_ok=True)
    pd.DataFrame(audit).to_csv(OUT / 'CI_PARTITION_AUDIT.csv', index=False)
    B = pd.DataFrame(paniers_tous)
    if len(B):
        def scen(d): return (B.pnl_net_usd_S0 - d / 10000 * B.prix_moyen * B.volume_total)
        B['pnl_S1'] = scen(0.3).round(4); B['pnl_S2'] = scen(0.6).round(4); B['pnl_S3'] = scen(2.0).round(4)
        B.to_csv(OUT / 'CI_V2_BASKETS_JAN_SEP.csv', index=False)
        log('TOTAL V2 janv-sept paniers', len(B), 'PnL S0', round(B.pnl_net_usd_S0.sum(), 3))
    LOG.close()

if __name__ == '__main__':
    main()
