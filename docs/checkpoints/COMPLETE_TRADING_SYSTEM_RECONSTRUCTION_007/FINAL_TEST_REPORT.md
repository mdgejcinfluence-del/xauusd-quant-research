# CTRS-007 — RAPPORT DE TESTS FINAL

Audit scientifique automatisé : `ci_tools/test_ctrs007.py` (recalcul des
PWA/PnL depuis les trajectoires gelées, reproduction des réfutations
EMI-006, non-séparabilité des trois horloges bornée par les intervalles
inter-ticks, intégrité du manifeste SHA-256, verdict B cohérent avec le
registre, chaîne valide). Résultat d'exécution consigné dans l'entrée de
registre seq473 et dans le message du commit de clôture.
Aucun test ne vérifie la seule présence de fichiers sans contenu
scientifique associé, à l'exception du contrôle d'intégrité documentaire.
