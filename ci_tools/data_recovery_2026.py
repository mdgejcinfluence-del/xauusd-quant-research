#!/usr/bin/env python3
"""DATA-RECOVERY-2026-001 (CI): recupere les 7 partitions Drive 2026 via gdown
(mecanisme autorise deja utilise par les moteurs historiques), audite leur integrite
vs INVENTORY_348_EXHAUSTIVE, puis rejoue le moteur V1 GELE (import sans modification)
partition par partition. Les partitions ne sont JAMAIS commitees dans Git.
Convention: attribution mensuelle au mois de CLOTURE du panier; un panier ouvert en
fin de partition et non cloture a la frontiere est classe AFFECTE_FRONTIERE (etat
documente, aucune cloture inventee). Sources: Dukascopy certifie, jamais HFM."""
import hashlib, json, pathlib, subprocess, sys
import numpy as np, pandas as pd
import pyarrow.parquet as pq
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay import rejouer, COUT_BP

R = pathlib.Path(__file__).resolve().parents[1]
REC = R / 'docs/checkpoints/DATA_RECOVERY_2026'; REC.mkdir(parents=True, exist_ok=True)
REP = R / 'docs/checkpoints/FULL_REPLAY_2026'; REP.mkdir(parents=True, exist_ok=True)
LOG = open(REC / 'RECOVERY_LOG.txt', 'w')
def log(*a): print(*a); LOG.write(' '.join(str(x) for x in a) + '\n'); LOG.flush()

def main():
    inv = json.loads((R / 'reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json').read_text())
    parts = [p for p in inv['partitions'] if (p.get('timestamp_min_footer') or '') >= '2026-01-01']
    log('partitions 2026 identifiees:', len(parts))
    audit, tous_paniers = [], []
    for p in parts:
        local = pathlib.Path(f"/tmp/{p['name']}")
        ligne = {'partition': p['name'], 'drive_id': p['drive_id'], 'taille_attendue': p['file_bytes'],
                 'lignes_attendues': p['rows'], 'debut_attendu': p['timestamp_min_footer'], 'fin_attendue': p['timestamp_max_footer']}
        try:
            r = subprocess.run(['gdown', '-q', '--output', str(local), p['drive_id']], capture_output=True, text=True, timeout=1200)
            if not local.exists() or local.stat().st_size == 0:
                ligne.update(statut='UNAVAILABLE', erreur=(r.stderr or r.stdout)[-300:]); audit.append(ligne); log(p['name'], 'ECHEC telechargement'); continue
            taille = local.stat().st_size
            sha = hashlib.sha256(local.read_bytes()).hexdigest()
            meta = pq.ParquetFile(local).metadata
            ligne.update(taille_observee=taille, sha256_calcule=sha, lignes_observees=meta.num_rows,
                         schema=';'.join(meta.schema_arrow.names))
            concord = (taille == p['file_bytes'] and meta.num_rows == p['rows'])
            ligne['statut'] = 'VERIFIED' if concord else 'VERIFIED_WITH_DIFFERENCES'
            df = pd.read_parquet(local, columns=['timestamp_utc', 'bid', 'ask'])
            df = df.rename(columns={'timestamp_utc': 'ts'})
            df['ts'] = pd.to_datetime(df.ts).dt.tz_localize(None)
            ligne.update(debut_observe=str(df.ts.min()), fin_observe=str(df.ts.max()),
                         ordre_chronologique=bool(df.ts.is_monotonic_increasing),
                         doublons_timestamps=int(df.ts.duplicated().sum()),
                         nulls=int(df.isna().sum().sum()),
                         spread_median_bp=round(float(((df.ask - df.bid) / ((df.ask + df.bid) / 2) * 10000).median()), 2))
            paniers = rejouer(df, df.ts.min(), df.ts.max())
            for x in paniers:
                vol = sum(v for _, v, _ in x['entrees'])
                tous_paniers.append({'partition': p['name'], 't0': str(x['t0']), 'cloture': str(x['cloture']),
                    'mois_cloture': str(x['cloture'])[:7], 'regle': x['regle'], 'nb_positions': x['nb'],
                    'volume_total': round(vol, 2), 'prix_moyen': round(x['prix_moyen'], 2),
                    'duree_s': round(x['duree_s'], 1), 'pnl_net_usd_S0': x['pnl_usd_unite'], 'renforcements': x['nb'] - 1})
            ligne['paniers_generes'] = len(paniers)
            log(p['name'], ligne['statut'], 'paniers', len(paniers))
            del df
        except Exception as e:
            ligne.update(statut='UNAVAILABLE', erreur=f'{type(e).__name__}: {e}'); log(p['name'], 'ERREUR', e)
        audit.append(ligne)
        local.unlink(missing_ok=True)
    pd.DataFrame(audit).to_csv(REC / 'PARTITION_INTEGRITY_AUDIT_2026.csv', index=False)
    B = pd.DataFrame(tous_paniers)
    if len(B):
        def pnl_scen(d): return (B.pnl_net_usd_S0 - d / 10000 * B.prix_moyen * B.volume_total)
        B['pnl_S1'] = pnl_scen(COUT_BP * .25).round(4); B['pnl_S2'] = pnl_scen(COUT_BP * .50).round(4); B['pnl_S3'] = pnl_scen(2.0).round(4)
        B.to_csv(REP / 'META_ALPHA_BASKETS_2026.csv', index=False)
        lignes = []
        for m, g in B.groupby('mois_cloture'):
            eq = g.pnl_net_usd_S0.cumsum(); gains, pertes = g[g.pnl_net_usd_S0 > 0], g[g.pnl_net_usd_S0 <= 0]
            lignes.append({'mois (cloture)': m, 'paniers': len(g), 'positions': int(g.nb_positions.sum()),
                'renforcements': int(g.renforcements.sum()), 'pnl_net_S0': round(g.pnl_net_usd_S0.sum(), 3),
                'pnl_S1': round(g.pnl_S1.sum(), 3), 'pnl_S2': round(g.pnl_S2.sum(), 3), 'pnl_S3': round(g.pnl_S3.sum(), 3),
                'gagnants_pct': round(100 * len(gains) / len(g), 1),
                'profit_factor': round(gains.pnl_net_usd_S0.sum() / abs(pertes.pnl_net_usd_S0.sum()), 3) if len(pertes) and pertes.pnl_net_usd_S0.sum() != 0 else None,
                'esperance_panier': round(g.pnl_net_usd_S0.mean(), 4),
                'duree_moy_s': round(g.duree_s.mean(), 1), 'duree_max_s': round(g.duree_s.max(), 1),
                'drawdown_max_mois': round(float((eq - eq.cummax()).min()), 3), 'pire_panier': round(g.pnl_net_usd_S0.min(), 4)})
        pd.DataFrame(lignes).to_csv(REP / 'META_ALPHA_MONTHLY_RESULTS_2026.csv', index=False)
        log('TOTAL paniers', len(B), 'PnL S0', round(B.pnl_net_usd_S0.sum(), 3))
    # Reconciliation novembre (donnees locales du depot, reference seq455)
    tot = []
    for j in ('20', '22', '23', '24', '25', '26', '27'):
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
        tot += rejouer(df, df.ts.min(), df.ts.max())
    pnl = round(sum(x['pnl_usd_unite'] for x in tot), 4)
    log(f"RECONCILIATION NOV: paniers={len(tot)} (ref 379) positions={sum(x['nb'] for x in tot)} (ref 898) pnl={pnl} (ref -0.432)")
    (REP / 'RECONCILIATION_NOV.json').write_text(json.dumps(
        {'paniers': len(tot), 'positions': sum(x['nb'] for x in tot), 'pnl_net': pnl,
         'reference_seq455': {'paniers': 379, 'positions': 898, 'pnl_net': -0.432},
         'conforme': len(tot) == 379 and abs(pnl + 0.432) < 0.01}, indent=1))
    LOG.close()

if __name__ == '__main__':
    main()
