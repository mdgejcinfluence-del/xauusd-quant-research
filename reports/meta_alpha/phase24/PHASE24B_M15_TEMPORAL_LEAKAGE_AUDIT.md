# PHASE 24-B — AUDIT DE FUITE TEMPORELLE M15

- Seuil d'impulsion : Q90 calculé sur les 250 barres complètes **précédentes**, barre courante
  exclue — causal par construction.
- Variables : toutes bornées à la clôture de la barre de réintégration (t_decision) ; le label
  n'utilise que les clôtures postérieures, jamais réinjectées comme variables (audit ligne par
  ligne dans `PHASE24B_M15_CAUSAL_FEATURE_AUDIT.csv`).
- Directeurs : définitions 24-A inchangées — H4 = dernière barre complète clôturée avant la
  décision (taux de non-validables 1,5 %) ; D1 = dernière journée certifiée strictement
  antérieure (13,1 % de non-validables : chauffe + couverture, jamais comblés).
- Horloge : appliquée à t_decision ; la vérification du premier tick d'entrée ≥ 16:00 relève de
  la phase d'exécution, comme documenté en 24-A.
- Grappes : fenêtres d'observation chevauchantes regroupées sous identifiant commun
  (`grappe_id`) pour préserver la dépendance dans toute inférence future.
- Splits par année de t0 : 2010-2015 / 2016-2017 / 2018-2019 (couverture réelle ; l'évaluation
  « 2018-2020 » est limitée aux données certifiées, holdout fermé).

Aucune fuite démontrée : **pas de `M15_CAUSALITY_AUDIT_FAILED`**, label reproductible
(`M15_LABEL_NOT_REPRODUCIBLE` écarté), qualité des données conforme (`M15_DATA_QUALITY_FAILED`
écarté : 99,58 % de barres complètes).
