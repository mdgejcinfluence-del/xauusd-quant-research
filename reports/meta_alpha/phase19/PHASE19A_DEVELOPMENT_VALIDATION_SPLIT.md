# PHASE 19-A — PLAN DE SÉPARATION DÉVELOPPEMENT / VALIDATION VERROUILLÉE

## Principe
Les deux populations naissent de la capture prospective (postérieure à septembre 2026) et sont séparées **chronologiquement et avant tout examen économique** : d'abord `NEW_DEVELOPMENT_DATA`, ensuite `NEW_LOCKED_VALIDATION_DATA`, sans chevauchement, grappes et événements intacts de part et d'autre de la frontière (purge d'horizon identique aux conventions historiques : aucun événement dont la fenêtre enjambe la frontière n'est affecté aux deux populations).

## Rôles
- `NEW_DEVELOPMENT_DATA` : seule population où une hypothèse, des variables et un modèle pourront être conçus et ajustés, sur décision distincte. Tout ce qui y est appris la contamine définitivement comme validation.
- `NEW_LOCKED_VALIDATION_DATA` : **aucun accès** (ni valeurs, ni métriques, ni comptages économiques au-delà du contrôle d'intégrité de capture) jusqu'au gel chaîné d'un candidat complet (variables, coefficients, règle de décision). Ouverture unique, consignée au registre, après gel.

## Taille minimale de la validation (à geler avant ouverture)
Justification : les évaluations historiques portaient sur ~440 événements filtrés en deux ans (≈ 220/an). Pour qu'une comparaison MAE/RMSE et une sélection `PREDICTED_EXPECTED_R > 0` soient informatives sans être dominées par quelques événements, la population verrouillée devra contenir **au minimum 300 événements filtrés par le modèle directionnel gelé, et au minimum 150 événements retenus ou une couverture documentée permettant de conclure à l'absence de sélection** ; en deçà, le verdict préenregistré sera `NON_EVALUABLE` et la population restera fermée plutôt que d'être consommée par une lecture sous-dimensionnée. Ces seuils sont une proposition de conception à geler par la décision qui autorisera la capture ; ils ne sont pas modifiables après ouverture.

## Garanties anti-contamination
Affectation des lots à la naissance (chaînée), journal d'accès, interdiction de « jeter un œil » aux métriques de la population verrouillée, interdiction de transférer un paramètre appris sur le développement sans le déclarer, et règle absolue : une population ayant servi à concevoir un modèle ne pourra jamais valider ce modèle.
