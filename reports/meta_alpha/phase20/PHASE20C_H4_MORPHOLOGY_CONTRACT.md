# PHASE 20-C — CONTRAT DE CALCUL DES MORPHOLOGIES H4

**Statut : `EXPLORATORY_POST_HOC`. Sources : barset et excursions de la Phase 20-A uniquement (aucune nouvelle extraction, aucun tick relu).**

## Formules (toutes en log-bp, depuis le Mid OHLC de la barre complète)
- `BODY_BP = 10000 ln(Close/Open)` ; `RANGE_BP = 10000 ln(High/Low)` (déjà dans le barset 20-A, réutilisés).
- `BODY_EFFICIENCY = |BODY_BP| / RANGE_BP`.
- `CLOSE_LOCATION = (Close − Low) / (High − Low)` ∈ [0,1] (prix, barre de range nul exclue — aucune dans le barset complet).
- `UPPER_WICK_BP = 10000 ln(High / max(Open,Close))` ; `LOWER_WICK_BP = 10000 ln(min(Open,Close) / Low)` ; `UPPER_WICK_SHARE = UPPER_WICK_BP / RANGE_BP` ; `LOWER_WICK_SHARE = LOWER_WICK_BP / RANGE_BP` ; `WICK_IMBALANCE = (LOWER_WICK_BP − UPPER_WICK_BP) / RANGE_BP` (positif = mèche inférieure dominante).

## Seuils causaux (barre courante exclue)
Référence glissante = **250 barres H4 complètes précédentes** : seuil d'expansion `Q90(RANGE_BP)` ; déciles de `CLOSE_LOCATION` et de `WICK_IMBALANCE` sur la même référence. Application du texte de mission 20-C ; recouvrement avec le catalogue d'expansion 20-A vérifié et consigné (la référence 20-A incluait les barres partielles dans la fenêtre, écart documenté s'il existe).

## Épisodes
Barres d'expansion consécutives (débuts à +4 h, complètes) = un épisode (`EXPANSION_EPISODE_ID`) ; population primaire = première barre de chaque épisode ; population descriptive = toutes les barres qualifiées.

## Configurations (drapeaux non exclusifs, chevauchements tabulés)
A : expansion + `CLOSE_LOCATION` ≥ décile supérieur causal (direction descriptive +). B : expansion + `CLOSE_LOCATION` ≤ décile inférieur (direction −). C : expansion + position centrale (entre les deux déciles). D : expansion + `WICK_IMBALANCE` ≥ décile supérieur (rejet apparent vers le bas : sens du rejet = −, sens opposé = +). E : expansion + `WICK_IMBALANCE` ≤ décile inférieur (rejet apparent vers le haut : +).

## Futur (depuis le Close de la barre d'événement)
Excursions UP/DOWN et MFE/MAE 20-A réutilisés (horizons 1–4, barres complètes consécutives uniquement, sinon censuré). Déplacement terminal orienté = direction × `10000 ln(Close_{i+H}/Close_i)`. Temps jusqu'au MFE/MAE : première barre future atteignant l'extrême de l'horizon (résolution = la barre H4, sans précision intrabarre — les High/Low ne datent pas l'extrême à l'intérieur de la barre). Restitution = `(MFE_orienté − terminal_orienté) / MFE_orienté` si MFE > 0. ATR : sous-audit séparé sur les événements à `ATR14_H4_PREV` valide, sans exclure la population principale.

## Inférence
Comparaisons primaires A/B/D/E contre C sur le terminal orienté, horizons 1–4 (16 tests), bootstrap par épisode sur la population primaire (2 000 tirages, graine 2011), Benjamini-Hochberg q=0,05 ; minima d'interprétation : 50 événements et 20 semaines ISO, sinon `NON_EVALUABLE_INFERENTIAL`. Références 4,0/4,5 bp : `REFERENCE_COST_UNVERIFIED`, diagnostics d'amplitude uniquement.
