# STRATEGY-DISCOVERY-001 — TESTS

Exécutés : `/tmp/metaalpha-venv/bin/python ci_tools/discovery_diagnostics.py`
(trajectoires + contrefactuel + comparaison, ~40 s) puis
`/tmp/metaalpha-venv/bin/python ci_tools/test_discovery_001.py` → **8/8 PASS**
(V1 gelé intact par empreinte, comparaison à données identiques, 379 paniers
réconciliés avec seq455, contrefactuel et censure documentés, statuts du registre
conformes, hypothèses réfutées conservées, chaîne du registre valide, livrables
présents). Un échec initial de forme (CSV du registre sans quoting) a été corrigé
et re-testé — consigné ici plutôt que masqué.
