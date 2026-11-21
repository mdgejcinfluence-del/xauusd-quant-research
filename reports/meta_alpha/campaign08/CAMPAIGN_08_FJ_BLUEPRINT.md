# CAMPAGNE 8 — BLUEPRINT SCIENTIFIQUE F-J « CHOCS MINUTE EXTRÊMES ET LEUR SILLAGE »

**Statut : PRÉPARATION AUTORISÉE — AUCUN CALCUL, AUCUNE EXTRACTION,
AUCUNE CONSULTATION DE RÉSULTATS F-J.** Famille approuvée par le
fondateur (chaîné seq257) à l'issue de l'audit des lacunes (seq256,
recommandation F-J 27/30). F-L et F-H restent en réserve.

## 1. Objectif scientifique

Étudier l'anatomie événementielle des variations exceptionnellement
importantes à l'échelle M1 sur le XAU/USD : fréquence, intensité,
direction (haussières et baissières **séparément**), regroupement
temporel, et comportement ultérieur (continuation, retour partiel,
retournement, stabilisation, nouveau choc). Aucun présupposé
d'anomalie prédictive ou exploitable : un choc décrit un événement de
prix, pas une opportunité ; toute candidate éventuelle irait au
catalogue J1 sans promotion automatique, et les résultats négatifs
seront publiés.

## 2. Priorité absolue : détection causale

Un choc à la minute t n'est « extrême » que relativement à un seuil
calculé **uniquement sur des informations disponibles avant t**
(fenêtre historique causale glissante, minimum d'observations
antérieures, période d'inéligibilité initiale publiée — dictionnaire
§2). Les quantiles poolés sur 2010–2020 sont **interdits** comme
seuils de détection : ils utiliseraient le futur du point de vue de
2011. Ils ne pourront apparaître, le cas échéant, que comme référence
rétrospective étiquetée, jamais comme définition d'événement. Aucun
seuil n'est choisi en regardant les sillages (calculs interdits à ce
stade ; constantes soumises au gel).

## 3. Frontière avec les travaux antérieurs (livrable 12, résumé)

| Travail | Objet | Différence avec F-J |
|---|---|---|
| F3 (HAR-RV gelé) | prévision de la volatilité **journalière** du lendemain | F-J ne prévoit rien ; événements minute et sillage descriptif |
| F7 (classifieur gelé) | classification d'états à partir de variables construites | aucun classifieur, aucune variable cible |
| Campagne 1 (+ext.) | dépassements d'extrêmes de prix formés (niveaux) et réintégrations | le choc F-J est une **variation**, pas un franchissement de niveau ; aucun niveau n'intervient |
| Campagne 3 | épisodes d'extension après extrêmes, candidates | pas de déclencheur ni d'épisode de trading ; l'« épisode » F-J est un regroupement statistique de chocs |
| Campagne 4 | états de volatilité réalisée journaliers/intra-journaliers et transitions | pas d'état agrégé : l'unité est l'événement minute, son contexte est causal et local |
| Campagne 5 | ouvertures de session et atteintes des extrêmes de la veille | ni session-objet, ni niveau de veille ; sessions en ventilation seulement |
| F-G (Camp. 6) | géométrie de la journée entière (ER, S, τ) | pas de grandeur de journée ; anatomie d'événements datés à la minute |
| F-I (Camp. 7) | contact avec une grille arithmétique vs placebo | aucune grille ; le seuil est statistique et causal, pas un prix rond |

F-J ne doit devenir ni une nouvelle étude des régimes de volatilité
(le seuil causal sert à **dater** des événements, pas à classer des
régimes exploitables), ni une répétition des anciennes analyses
d'impulsions (qui franchissaient des niveaux). Aucune fiche C3/C4/C5
n'est modifiée ni confirmée automatiquement.

## 4. Coût informatique et suspension (livrable 11)

Même corpus IS (282 partitions, ~3,54 M barres M1) : un passage pour
les rendements et seuils causaux glissants, un passage pour les
épisodes et sillages. Coût attendu : **un run CI unique** de l'ordre
de C5–C7, synthèse locale ; 0 FCFA ; aucun budget expérimental
consommé. Suspension documentée en cas d'échec ou de dépassement, sans
aucune dégradation méthodologique (ni fenêtre causale raccourcie, ni
seuil assoupli, ni population réduite pour « faire passer » le calcul).

## 5. Restrictions

XAU/USD, corpus IS uniquement ; holdout scellé ; aucun backtest ni
`challenge_sim` ; aucun J2/J3 ; FRED suspendue ; 36 cellules S12
gelées ; T0 séparé et inactif ; fiches historiques inchangées ; F-L et
F-H en réserve, non abandonnées.
