# PHASE 17-D — RAPPORT DE FAISABILITÉ (artefacts existants uniquement)

## 1. Données requises : toutes présentes, reliables par `event_id`
P&L S2 en bp par événement : `PHASE17B_LABELS_B08/B09.csv` (1 946 lignes chacun) avec `mecanisme`, `statut_label`, prix d'entrée, prix de sortie et P&L S0/S1/S2. `ATR14_H1` à la décision : `PHASE17B_FEATURES_B08/B09.csv`, **0 valeur manquante** sur les 1 946 événements ; liaison `event_id` + `grappe_id` exacte et sans doublon (rapprochement un-à-un vérifié). Prix d'entrée absent uniquement pour les 2 NON_EXECUTION par contrat, exclues de la cible par définition. Distance initiale du stop : dérivable sans ambiguïté, `k × ATR14_H1` convertie en bp via le prix d'entrée (même unité que le P&L). Cohérence entre contrats : mêmes candidats (1 143/360/443), labels construits séparément, réconciliation 17-B avec la Phase 14 parfaite. Aucune relecture de ticks, aucune régénération de labels, aucun recalcul des résultats 17-B.

## 2. Effectifs utilisables pour la cible continue
B08 : 1 137 / 357 / 440 étiquetés ; B09 : 1 133 / 356 / 435 (censurés et NON_EXECUTION exclus, cf. `PHASE17D_SPLIT_AND_PURGE_AUDIT.csv`). Volumes très supérieurs aux minima d'évaluabilité historiques ; aucune grappe partagée entre segments.

## 3. Adéquation d'une régression linéaire simple
La distribution de R est bornée par construction des barrières (environ −2,2 à +2,6 R), à kurtosis négative et asymétrie modérée (B08 apprentissage : +0,70) : une moyenne conditionnelle linéaire est une première représentation défendable et interprétable, nettement moins exposée aux queues que la même régression en bp (kurtosis positive en apprentissage, extrêmes à ±220 bp). Limites consignées : B08 reste asymétrique avec médiane très négative (masse au SL), l'hétéroscédasticité résiduelle n'est pas exclue, et une espérance conditionnelle ne décrit pas le risque de perte. Une modélisation séparée de quantiles du payoff ou de la probabilité de perte extrême présenterait un intérêt documentaire, mais **elle n'est ni implémentée ni préenregistrée comme modèle concurrent** dans la présente phase : un seul modèle candidat est conçu, conformément à l'ordre de mission. Si la régression linéaire échouait en 17-E, toute alternative exigerait une décision distincte.

## 4. Limites
Biais de sélection M1 en échantillon sur l'apprentissage (hérité, documenté, non corrigeable sans réentraîner M1 — interdit) ; évaluation déjà étudiée ; commissions exclues ; la normalisation stabilise l'échelle mais pas démontrée pour le niveau moyen de R.

## 5. Verdict de faisabilité
Toutes les conditions du §15 de l'ordre de mission sont remplies : P&L continus présents, distances de risque récupérables, normalisation sans ambiguïté, variables sans fuite, séparations valides, métriques et règle de décision préenregistrables → **`PHASE17D_READY_FOR_CONTINUOUS_PAYOFF_MODEL`**. Ce verdict autorise uniquement la présentation du protocole gelé ; l'entraînement exigera une décision distincte (Phase 17-E éventuelle).
