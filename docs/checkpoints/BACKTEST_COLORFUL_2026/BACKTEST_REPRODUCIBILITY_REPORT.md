# BACKTEST-COLORFUL-2026 — REPRODUCTIBILITÉ ET TESTS

Relance complète : `/tmp/metaalpha-venv/bin/python ci_tools/colorful_backtest_2026.py`
(moteur gelé importé, jamais modifié ; empreintes données+modèle dans
`MODEL_FINGERPRINT.json`, commit de base 7020253, préenregistrement seq454).
Tests : `/tmp/metaalpha-venv/bin/python ci_tools/test_backtest_2026.py` — 12 contrôles
(empreinte du moteur gelé, causalité ouverture<clôture sur tous les paniers, aucun
décembre, sensibilité aux coûts strictement décroissante, spread compté une fois,
valeurs HFM archivées non transformées, comparaison NOT_DIRECTLY_COMPARABLE,
mois non testables déclarés sans remplissage, novembre déclaré partiel, chaîne du
registre valide, artefacts présents). Résultat consigné après exécution dans le
commit seq455. Aucun look-ahead : `rejouer()` n'utilise que les ticks ≤ instant de
décision (vérifié par construction du moteur gelé et par les horodatages).
Limite : les contrôles de doublons/trous portent sur les 7 fichiers journaliers
locaux (voir `DAILY_COVERAGE_NOV2026.csv`) ; les mois non accessibles n'ont pas
été contrôlés byte à byte — ils sont déclarés non testables, pas supposés complets.
