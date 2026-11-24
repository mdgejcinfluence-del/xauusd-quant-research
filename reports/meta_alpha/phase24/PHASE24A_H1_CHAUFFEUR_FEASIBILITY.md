# PHASE 24-A — FAISABILITÉ DU CHAUFFEUR H1 CONDITIONNEL

Critères gelés : évaluation ≥ 100 événements et ≥ 50 en classe minoritaire ; train ≥ 20
observations de classe minoritaire par paramètre estimé (M1 = 9 paramètres → minoritaire ≥ 180).

| Variante | Train (minoritaire) | Évaluation (minoritaire) | Verdict |
|---|---|---|---|
| `CHAUFFEUR_H1_H4_GATE` (H4_TIME) | 107 (26 ; 2,9/paramètre) | 34 (5) | `CONDITIONAL_CHAUFFEUR_INSUFFICIENT_SAMPLE` |
| `CHAUFFEUR_H1_D1_GATE` (D1_TIME) | 86 (15 ; 1,7/paramètre) | 43 (12) | `CONDITIONAL_CHAUFFEUR_INSUFFICIENT_SAMPLE` |

Références : BASELINE train 1 640 (395), évaluation 543 (133) ; TIME_ONLY train 916 (201 ; 22,3/par.),
évaluation 296 (62) — l'Horloge seule reste au-dessus des minima ; H4_ONLY train minoritaire 135
(15,0/par.), évaluation 160 (41) ; D1_ONLY évaluation 80 (28). C'est la **combinaison**
Directeur × Horloge qui effondre les effectifs (H4_TIME : 165 événements au total ; D1_TIME : 147).

Risque structurel supplémentaire : dans la fenêtre 08:00-16:00, les indicatrices
SESSION_REINTEGRATION NY_AFTERNOON et NIGHT_OTHER sont absentes et ASIA ne compte qu'1 événement
(train) : un réentraînement conditionnel ferait face à une quasi-séparation et à des paramètres de
session non estimables — l'architecture à 9 paramètres n'est pas estimable sur ces cohortes.

Interdictions respectées : aucune fusion H4/D1 pour gonfler les effectifs, aucun passage en M15,
aucun P&L ni examen de rendement futur par variante (les fréquences de classe du train sont les
seules statistiques de cible présentées, comme l'exige le comptage de faisabilité).
Directeurs H4 et D1 : reproduits exactement — ni `H4_DIRECTOR_NOT_REPRODUCIBLE` ni
`D1_DIRECTOR_NOT_REPRODUCIBLE`.
