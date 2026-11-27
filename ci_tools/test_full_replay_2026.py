#!/usr/bin/env python3
"""Tests FULL REPLAY 2026 (12 controles effectivement executes)."""
import json, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
REC = R / 'docs/checkpoints/DATA_RECOVERY_2026'; REP = R / 'docs/checkpoints/FULL_REPLAY_2026'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)
A = pd.read_csv(REC / 'PARTITION_INTEGRITY_AUDIT_2026.csv')
t('01 sept partitions identifiees', len(A) == 7)
t('02 toutes VERIFIED (taille+lignes concordantes)', (A.statut == 'VERIFIED').all() and (A.taille_observee == A.taille_attendue).all() and (A.lignes_observees == A.lignes_attendues).all())
t('03 SHA-256 calcules pour chaque partition', A.sha256_calcule.str.len().eq(64).all())
t('04 ordre chronologique et zero null/doublon partout', A.ordre_chronologique.all() and (A.nulls == 0).all() and (A.doublons_timestamps == 0).all())
B = pd.read_csv(REP / 'META_ALPHA_BASKETS_2026.csv')
t('05 3728 paniers, causalite cloture>ouverture', len(B) == 3728 and (pd.to_datetime(B.cloture, format='mixed') > pd.to_datetime(B.t0, format='mixed')).all())
t('06 aucun panier en octobre/decembre (periodes non testees non remplies)', not B.mois_cloture.str.contains('2026-10|2026-12').any())
rec = json.loads((REP / 'RECONCILIATION_NOV.json').read_text())
t('07 reconciliation novembre exacte vs seq455', rec['conforme'])
M = pd.read_csv(REP / 'META_ALPHA_MONTHLY_RESULTS_2026.csv')
t('08 resultats mensuels coherents avec les paniers', abs(M.pnl_net_S0.sum() - B.pnl_net_usd_S0.sum()) < 0.05)
import hashlib
fp = json.loads((REP / 'META_ALPHA_V1_FINGERPRINT.json').read_text())
t('09 moteur gele: empreinte inchangee', fp['sha256_colorful_replay.py'] == hashlib.sha256((R / 'ci_tools/colorful_replay.py').read_bytes()).hexdigest())
t('10 sensibilite couts strictement decroissante au total', B.pnl_net_usd_S0.sum() > B.pnl_S1.sum() > B.pnl_S2.sum() > B.pnl_S3.sum())
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('11 chaine du registre valide', verify()[0])
t('12 livrables presents', all((REP / f).exists() for f in ['FULL_REPLAY_2026_FINAL_REPORT.md', 'META_ALPHA_FAILURE_ATTRIBUTION_2026.md', 'chart_equity_monthly.png']) and (REC / 'DATASET_MANIFEST_2026.json').exists())
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
