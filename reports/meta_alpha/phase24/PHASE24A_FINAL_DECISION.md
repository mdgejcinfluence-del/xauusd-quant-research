# PHASE 24-A — DÉCISION FINALE

Verdicts par variante :

- `CHAUFFEUR_H1_H4_GATE` : `CONDITIONAL_CHAUFFEUR_INSUFFICIENT_SAMPLE`
  (train 107, minoritaire 26 ; évaluation 34, minoritaire 5).
- `CHAUFFEUR_H1_D1_GATE` : `CONDITIONAL_CHAUFFEUR_INSUFFICIENT_SAMPLE`
  (train 86, minoritaire 15 ; évaluation 43, minoritaire 12).

Verdict global : **`CONDITIONAL_ARCHITECTURE_NOT_FEASIBLE`** sur les populations historiques
disponibles, sous les définitions gelées (Directeurs reproduits exactement, causalité des
permissions démontrée, aucune fusion autorisée pour gonfler les effectifs).

Ce qui est établi : les permissions Énergie × Horloge sont causalement propres et reproductibles,
événement par événement ; ce qui les rend inutilisables pour un réentraînement conditionnel, c'est
l'effondrement des cohortes (165 et 147 événements au total) et l'inestimabilité des paramètres
de session dans la fenêtre horaire. L'Horloge seule (916 événements d'entraînement) resterait
faisable, mais elle ne constitue pas l'architecture conditionnelle préenregistrée et ne peut pas
être substituée silencieusement aux variantes gelées.

La phase suivante ne pourra être autorisée qu'après examen de ce registre de faisabilité.
Aucun modèle n'a été entraîné ; aucun P&L n'a été calculé.
