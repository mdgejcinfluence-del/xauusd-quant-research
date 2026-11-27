#!/usr/bin/env python3
"""Tests BACKTEST-COLORFUL-2026 (12 controles). /tmp/metaalpha-venv/bin/python ci_tools/test_backtest_2026.py"""
import hashlib, json, pathlib, sys
import pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]; OUT = R / 'docs/checkpoints/BACKTEST_COLORFUL_2026'
ok = []
def t(n, c): ok.append(c); print(('PASS' if c else 'FAIL'), n)
fp = json.loads((OUT / 'MODEL_FINGERPRINT.json').read_text())
t('01 empreinte moteur = fichier gele actuel', fp['sha256_colorful_replay.py'] == hashlib.sha256((R / 'ci_tools/colorful_replay.py').read_bytes()).hexdigest())
B = pd.read_csv(OUT / 'MONTHLY_BASKETS_2026.csv')
t('02 paniers generes et horodates en novembre', len(B) > 300 and str(B.t0.min()).startswith('2026-11'))
t('03 causalite: cloture posterieure a louverture partout', bool((pd.to_datetime(B.cloture, format='mixed') > pd.to_datetime(B.t0, format='mixed')).all()))
t('04 aucun panier hors periode demandee (pas de decembre)', str(B.t0.max()) < '2026-11-28')
sc = pd.read_csv(OUT / 'COST_SENSITIVITY_2026.csv')
t('05 sensibilite monotone decroissante S0>S1>S2>S3', bool((sc.pnl_net_total_usd_modele.diff().dropna() < 0).all()))
t('06 spread compte une fois: cout moteur 1.2bp documente', fp['cout_bp_moteur'] == 1.2)
hfm = pd.read_csv(OUT / 'HFM_MONTHLY_REFERENCE_2026.csv')
t('07 valeurs HFM archivees non transformees (11 lignes)', len(hfm) == 11 and hfm.statut.str.contains('UNVERIFIED').all())
comp = pd.read_csv(OUT / 'HFM_VS_META_ALPHA_COMPARISON_2026.csv')
t('08 comparaison marquee NOT_DIRECTLY_COMPARABLE', (comp.ecart == 'NOT_DIRECTLY_COMPARABLE').all())
couv = pd.read_csv(OUT / 'MONTHLY_DATA_COVERAGE_2026.csv')
t('09 janvier-octobre declares NON_TESTABLES (aucun remplissage)', (couv.statut[:10] == 'NON_TESTABLE').all())
met = pd.read_csv(OUT / 'META_ALPHA_MONTHLY_RESULTS_2026.csv')
t('10 novembre declare PARTIEL, pas integral', 'PARTIEL' in met.statut.iloc[0])
sys.path.insert(0, str(R / 'ci_tools')); from ledger_chain import verify
t('11 chaine du registre valide, historique non reecrit', verify()[0])
t('12 artefacts et graphiques presents', all((OUT / f).exists() for f in ['chart_hfm_vs_equity.png', 'chart_baskets_per_day.png', 'MONTHLY_BASKETS_2026.csv', 'CAPITAL_SCENARIOS_2026.csv']))
print(f"\n{sum(ok)}/{len(ok)} tests PASS"); sys.exit(0 if all(ok) else 1)
