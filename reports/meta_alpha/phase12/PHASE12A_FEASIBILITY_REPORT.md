# PHASE 12-A — RAPPORT DE FAISABILITÉ

**Base : effectifs publiés (11-C, réconciliés 11-C.1 seq307) et
schémas réels des livrables 11-C. Aucun calcul prédictif, aucune
corrélation, aucune comparaison de groupes effectués.**

## 1. Effectifs disponibles pour la cible

La question 12-A est conditionnée à la réintégration confirmée.
Parmi les événements réintégrés à trajectoire complète (seuls
étiquetables sans ambiguïté) :

| Famille | Réintégrés complets | RESUMPTION = 1 | RESUMPTION = 0 | Censurés réintégrés | Part de la classe 1 |
|---|---|---|---|---|---|
| F10-01 (H1) | 2 692 | 2 032 | 660 | 3 | 75,5 % |
| F10-03 (H4) | 629 | 539 | 90 | 3 | 85,7 % |

Cas `AMBIGUOUS` : 0 observé en 11-C des deux côtés
(`intra_minute_order_unknown` = 0 et aucun archétype
`AMBIGU_INTRA_MINUTE`) ; la classe reste prévue au protocole.
Les non-réintégrés (412 H1, 28 H4) sont hors population cible par
construction de la question, non des « échecs » de reprise.

## 2. Disponibilité réelle des variables (schéma inspecté)

`PHASE11C_EVENT_PATHS.csv` contient 75 colonnes. Constats (détail :
`PHASE12A_FEATURE_DICTIONARY.csv`) :

- **Disponibles à t_reintegration sans fuite** : session de
  réintégration et de déclenchement, direction, corps et range de
  la bougie déclencheuse, délai t0 → t_reintegration
  (`reintegration_delai_minutes`, absent exactement pour les 440
  non-réintégrés, hors population).
- **Existantes mais fuitives en l'état** : la plupart des mesures
  d'anatomie sont calculées sur la fenêtre complète de 8 bougies
  (profondeur maximale de repli, fraction du corps reprise, MFE/MAE
  maximaux, nombre de retours, horizons par bougie). Les utiliser
  comme variables reviendrait à prédire le passé avec le futur :
  **interdites telles quelles**.
- **Manquantes (extraction bornée requise en Phase 12-B)** : les
  cinq variables du modèle préspécifié (ratio de repli à
  t_reintegration, durée extrême favorable → t_reintegration, MFE
  atteint à t_reintegration et sa durée, nombre de touches de P0
  avant t_reintegration). Elles sont définissables sans ambiguïté à
  partir des minutes ≤ t_reintegration, mais n'existent dans aucun
  artefact actuel. Ne pas les déclarer disponibles serait une
  erreur ; les déclarer disponibles en serait une autre.

La cible, elle, est déjà matérialisée (`reprise_apres_reintegration`
croisée avec `horizon_atteint` et `intra_minute_order_unknown`).

## 3. Faisabilité des segments chronologiques

Séparation préspécifiée (2010–2015 / 2016–2017 / 2018–2020, par
grappe entière). Sans calculer la moindre statistique prédictive,
les seuls effectifs publiés permettent un contrôle de structure :

- **H1** : 2 032 reprises et 660 absences au total. Même avec une
  répartition chronologique inégale, le segment d'évaluation
  (2018–2020) a des chances raisonnables d'atteindre les critères
  préspécifiés (≥ 100 étiquetés, minorité ≥ 50). Faisabilité
  **plausible, à confirmer par les seuls comptages de segment en
  Phase 12-B**.
- **H4** : 90 absences de reprise au total sur dix ans. Le segment
  d'évaluation ne contiendra vraisemblablement que quelques
  dizaines d'absences, possiblement sous le seuil de 50 : la famille
  H4 doit être considérée comme **à risque élevé de NON
  ÉVALUABLE** pour le test prédictif (descriptif seul alors
  publié). Aucune modification de population, aucun pooling H1/H4
  et aucun élargissement de segment ne sont autorisés pour y
  remédier. Aucune puissance statistique n'est déduite ici : aucune
  méthode de puissance n'a été préétablie, et l'inférer des taux
  observés serait circulaire.

## 4. Risques principaux identifiés

1. **Fuite temporelle** : le risque majeur de cette étude ; traité
   par l'interdiction des colonnes fenêtre complète et l'extraction
   bornée à t_reintegration.
2. **Hypothèses inspirées des mêmes données** (Phase 11 observée
   sur l'IS) : niveau de preuve plafonné à « historiquement évaluée
   — non indépendamment confirmée », quel que soit le résultat.
3. **Déséquilibre des classes** (surtout H4) : métriques
   probabilistes et calibration imposées, AUC jamais seule.
4. **Dépendance par grappes et chevauchement de fenêtres** :
   séparation par grappe entière et purge des chevauchements de
   segments préspécifiées.

## 5. Conclusion de faisabilité

Le protocole est définissable et préenregistrable sans ambiguïté
(cible, instant de décision, variables et leur statut, séparations,
métriques, critères d'insuffisance, règles anti-fuite). La Phase
12-B exigera (i) une extraction bornée des cinq variables aux
minutes ≤ t_reintegration et (ii) le gel préalable du protocole
12-A, chacun par décision distincte. Faisabilité H1 plausible,
H4 fragile (minorité de 90). 

**Verdict : `PROTOCOL_READY_FOR_PHASE12B`** — sans lancement
automatique de la Phase 12-B.
