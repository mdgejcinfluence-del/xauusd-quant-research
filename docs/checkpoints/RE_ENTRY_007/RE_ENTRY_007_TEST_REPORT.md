# RE-ENTRY-007 — RAPPORT DE TESTS

Commandes exécutées (venv projet) :
```
/tmp/metaalpha-venv/bin/python ci_tools/reentry007_audit.py
/tmp/metaalpha-venv/bin/python ci_tools/test_reentry007.py
```
Résultat : **15/15 tests PASS** (reconnaissance des snapshots, SHA-256 cohérents,
capture déjà connue détectée, déduplication 6/6 déjà connues, 0 nouvelle, clés
uniques, ambiguës comptées, chronologie, diff, historique préservé, seuils H3
inchangés, chaîne du registre valide par `ledger_chain.verify`, aucun prix
artificiel, artefacts présents). Aucune erreur rencontrée ; aucun test présenté
comme réussi sans exécution. Note d'environnement : le python système n'a pas
pandas — utiliser `/tmp/metaalpha-venv/bin/python`.
