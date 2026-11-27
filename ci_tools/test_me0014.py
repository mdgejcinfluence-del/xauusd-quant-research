#!/usr/bin/env python3
"""Tests ME-001.4 (executes)."""
import pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/ME001_PROSPECTIVE_004'
ok = []
def t(n, c): ok.append(bool(c)); print(('PASS' if c else 'FAIL'), n)

A = pd.read_csv(OUT / 'ME001_DATA_INDEPENDENCE_AUDIT.csv')
t('01 audit: categories C (novembre), B (Kaggle), D (prospectif) explicites',
  (A.categorie.str.startswith('C')).any() and (A.categorie.str.startswith('B')).any() and (A.categorie.str.startswith('D')).any())
G = pd.read_csv(OUT / 'ME001_PROSPECTIVE_REGISTRY.csv')
t('02 registre prospectif: jours traces avec SHA-256', len(G) >= 1 and G.sha256_parquet.notna().all())
P = pd.read_csv(OUT / 'ME001_NET_PERFORMANCE.csv')
t('03 aucune performance fabriquee: fichier de performance en statut DONNEES INSUFFISANTES',
  P.statut.astype(str).str.contains('DONNEES INSUFFISANTES').all())
proto = (R / 'docs/checkpoints/ME001_ENTRY_RISK_003/ME001_INDEPENDENT_VALIDATION_PROTOCOL.md').read_text()
t('04 protocole gele retrouve (seuils 7,76/7,88/5,32)', all(s in proto for s in ('7,76', '7,88', '5,32')))
reg = (R / 'docs/governance/META_ALPHA_MODEL_REGISTRY.md').read_text()
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('05 ME-001 toujours SIGNATURE_DETECTED + chaine valide', 'SIGNATURE_DETECTED' in reg and verify()[0])
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
