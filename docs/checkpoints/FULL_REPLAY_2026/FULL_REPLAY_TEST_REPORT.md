# FULL REPLAY 2026 — TESTS ET REPRODUCTIBILITÉ

Rejeu : CI GitHub Actions run 46024838552 (job `datarec2026`, workflow
`phase10_all.yml`, déclenché par l'input existant `diag` — aucun nouvel input,
limite des 25 respectée), script `ci_tools/data_recovery_2026.py`, moteur gelé
importé. Réconciliation novembre : exacte (379/898/−0,432 vs seq455).
Tests locaux : `/tmp/metaalpha-venv/bin/python ci_tools/test_full_replay_2026.py`
→ **12/12 PASS** (intégrité des 7 partitions, SHA-256, ordre/nulls/doublons,
causalité des paniers, périodes non testées non remplies, réconciliation,
cohérence mensuelle, empreinte du moteur gelé, coût compté une fois et
sensibilité monotone, chaîne du registre, livrables). Échecs techniques initiaux
du CI (journal, course de push, API pyarrow) : corrigés par commits documentés,
sans toucher au moteur ni aux données.
