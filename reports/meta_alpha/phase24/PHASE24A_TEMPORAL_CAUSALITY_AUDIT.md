# PHASE 24-A — AUDIT DE CAUSALITÉ TEMPORELLE

Vérifications événement par événement (`PHASE24A_EVENT_PERMISSION_PANEL.parquet`, 2 690
événements H1 évaluables) :

- Barre H4 directrice : fin de barre ≤ t_decision par construction (recherche de la dernière
  barre complète clôturée) — aucune barre en cours utilisée.
- Journée D1 directrice : strictement antérieure à la date de décision et certifiée complète
  (barset 21-A) — le range final du jour même n'est jamais utilisé.
- Les 5 variables H1 sont les extractions bornées de Phase 12-A, connues à t_reintegration —
  aucune variable de fenêtre complète interdite n'est présente (0 valeur manquante).
- Horloge appliquée à t_decision ; l'horodatage d'entrée réel (premier tick) n'est pas revérifié
  dans cette phase (pas d'accès tick autorisé pour un comptage de faisabilité) : les événements
  décidés dans la dernière minute avant 16:00 devront être revérifiés en phase d'exécution
  (`ENTRY_OUTSIDE_ALLOWED_WINDOW`). Limite déclarée, non dissimulée.
- Aucune information future ne participe au filtrage : les permissions n'utilisent ni RESUMPTION,
  ni MFE/MAE futurs, ni rendement.

Aucune fuite démontrée sur les permissions Directeur/Horloge/variables : **pas de
`CAUSALITY_AUDIT_FAILED`**. La causalité des effectifs est établie ; c'est la taille des cohortes
qui fait défaut.
