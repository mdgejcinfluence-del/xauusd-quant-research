# CAMPAGNE 1.1 — CONTEXTE F7 SUR LES ÉVÉNEMENTS STRUCTURELS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Ce qui est réellement disponible du modèle gelé

- Définition (seq 75) : logistique L2 sur états causaux (volatilité, spread, activité,
  |ret| passé, heure sin/cos) ; cible : |rendement de l'heure suivante| > quantile 90
  causal de son passé.
- Résultats versionnés (`F7_RESULTS.json`) : AUC out-of-fold **0,684**, lift **2,85×**
  au taux d'alerte de 5 %, taux de base des sauts **10,1 %**, n = 23 429 heures ;
  validation forward annuelle L2 : AUC 0,684/0,696/0,687 (2017–2019, seq 83).
- **Ce qui n'existe pas dans le dépôt** : la série horaire des probabilités prédites,
  les coefficients du modèle sous forme réutilisable horodatée, et toute table
  croisant ces probabilités avec des événements structurels.

## Conséquence pour cette campagne

**Aucune mesure « F7 » par événement n'est produite.** En particulier :
- aucun décile F7 n'est attaché aux épisodes EV2/EV3/EV5/EV6 ;
- la volatilité réalisée autour des événements n'est **pas** présentée comme un
  substitut de F7 (ce serait une approximation déguisée en mesure du modèle) ;
- aucune direction n'est attribuée aux alertes de saut — F7 est et reste un
  classement de risque d'amplitude, sans signe (doctrine depuis seq 77).

Ce qui peut être dit descriptement sans le modèle : les événements structurels de la
campagne 1 surviennent dans des contextes d'amplitude contrastés (profondeurs
médianes 10,5 bp pour les réintégrations contre 24,3 bp pour les retests), et les
régimes F3 (volatilité prévue, disponible) ordonnent ces amplitudes — mais ce
conditionnement est celui de **F3**, pas de F7, et il est rapporté sous son propre
nom dans les comparaisons conditionnelles.

## Ce qu'exigerait un vrai contexte F7 (à autoriser séparément)

1. Ré-exécuter l'**inférence** du modèle gelé sur la série horaire IS (sans aucun
   réentraînement : mêmes features causales, mêmes coefficients — si les coefficients
   ne sont pas récupérables des artefacts, l'étape est impossible sans rouvrir le
   modèle, ce qui exigerait un ordre explicite distinct).
2. Produire la série des probabilités + déciles IS (alerte de classement, pas
   probabilité calibrée, seq 148).
3. Croiser, en descriptif, la distribution des déciles aux timestamps des événements
   des campagnes 1/1.1, avec grappes jour×niveau comme unité.

Aucune de ces étapes n'est entreprise ici ; elles sont listées pour que la décision
du propriétaire porte sur un périmètre exact.
