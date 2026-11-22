# PHASE 12-C.2 — CONFIRMATION INDÉPENDANTE H1 SUR LE HOLDOUT 2020–2026

**RAPPORT SCIENTIFIQUE FINAL (mission 12-C.2-R3)**
**Verdict migration : `HOLDOUT_MIGRATION_VERIFIED` (66/66).**
**Verdict évaluation : `CONFIRMED_HISTORICAL_HOLDOUT`.**
**Qualification obligatoire : CONFIRMATION HISTORIQUE HORS IS —
NON VALIDATION PROSPECTIVE. Aucune conclusion de rentabilité :
une confirmation prédictive hors IS ne prouve ni la résistance aux
spreads, commissions et slippage, ni une exploitabilité économique.**

## 1. Provenance et intégrité des sources

Chaîne réalisée : Drive authentifié par le propriétaire → Colab
(SHA-256 source sur les originaux) → six datasets Kaggle privés →
runner CI. Le manifeste source du propriétaire
(`SOURCE_SHA256_66_PARTITIONS.json`, SHA-256 du fichier
`5191e301070fb8f10c5ce7c0b1d407b900246947cd5bbd06cf6a45e5d9b1265d`)
a été validé avant tout contrôle (66 entrées uniques, noms,
tailles et datasets 100 % conformes au manifeste gelé
`b112b7ab…`). Vérification CI en lecture seule (aucun accès
Drive) : les 66 fichiers Kaggle ont été récupérés un dataset à la
fois ; pour chacun, nom exact, taille conforme (source Colab =
manifeste = copie), signatures PAR1 en début et fin, et
**SHA-256 de la copie identique au SHA-256 source Colab — 66/66,
zéro manquant, zéro supplémentaire, zéro doublon, zéro
divergence**. Les six datasets sont privés (`isPrivate: true`),
en version 1, avec exactement leurs 11 partitions attribuées
(détail : `PHASE12C2_SHA256_VERIFICATION.csv`,
`PHASE12C2_KAGGLE_INVENTORY.json`,
`PHASE12C2_HOLDOUT_TRANSFER_AUDIT.json`). Les empreintes de
référence restent celles du propriétaire (Colab authentifié) ;
la CI ne prétend pas avoir relu Drive. Historique d'accès
conservé : blocages Drive seq319–323 (quota Google, secret SA
absent, dossier partagé sur les mêmes objets Drive) résolus par
le transfert propriétaire, sans qu'aucune métrique n'ait jamais
été produite pendant ces incidents — l'évaluation n'a été
consommée qu'au run terminal ci-dessous.

## 2. Population de confirmation

Barres M1 reconstruites depuis les copies Kaggle vérifiées
(2 441 904 barres, 2019-11-10 → 2026-09-30 ; la période antérieure
à 2020 ne sert que de contexte au détecteur causal). Détecteur
F10-01 historique gelé (amendement causal seq289, Q95 gelés,
fenêtre fixe de 250 barres) appliqué tel quel ; clustering par la
méthode historique des composantes, combiné IS+holdout uniquement
pour détecter les grappes mixtes.

- Détectés holdout (déclenchement ≥ 2020-01-01) : 2 140 ;
  contexte avant frontière : 29 (exclus) ;
- Admissibles : 2 126 (14 non admissibles) ;
- Grappes mixtes IS/holdout : **0** ; non réintégrés : 281 (hors
  population conditionnelle) ; censurés : 2 ; ambigus : 0 ;
- **Étiquetés pour l'évaluation : 1 843 — 1 410 reprises /
  433 absences.** Critères préenregistrés satisfaits
  (≥ 100 étiquetés, minorité 433 ≥ 50) : famille **ÉVALUABLE**.

## 3. Méthode (strictement le préenregistrement)

Modèle gelé de la Phase 12-C.1 chargé depuis
`PHASE12C1_MODEL_PARAMETERS.json` (`1bcb3b70…`, coefficients
jamais recopiés ni réestimés) ; cinq variables extraites de façon
strictement bornée à `t_reintegration` par le code gelé
(preuves : `PHASE12C2_FEATURE_AUDIT.json`) ; cible gelée
(fenêtre de 8 bougies, censurés/ambigus exclus des classes) ;
M0 **gelé à 0,7591463414634146**, jamais recalculé sur le holdout ;
M0 et M1 appliqués sur exactement les mêmes 1 843 observations ;
prédictions individuelles conservées
(`PHASE12C2_HOLDOUT_PREDICTIONS.csv`, `event_id` uniques).

## 4. Résultats (évaluation unique terminale, run 45044400978)

| Métrique (holdout, n = 1 843) | M0 | M1 | Delta M1 − M0 | Amélioration relative |
|---|---|---|---|---|
| **Brier score** | 0,1798 | **0,1482** | **−0,0316** | **+17,6 %** |
| **Log-loss** | 0,5453 | **0,4850** | **−0,0603** | **+11,1 %** |

Diagnostics : AUC M1 = 0,742 (M0 = 0,5) ; précision au seuil 0,5
= 0,805, rappel = 0,971 ; calibration publiée (n ≥ 200) :
ordonnée 0,152, **pente 0,942** — déciles prédits (0,321 → 0,918)
proches des fréquences observées (0,303 → 0,930), nettement mieux
calibrés que sur l'évaluation IS (pente 0,750). Les deux
métriques principales s'améliorent contre M0, sans anomalie de
fuite : la règle de décision préenregistrée donne
**`CONFIRMED_HISTORICAL_HOLDOUT`**.

## 5. Incidents techniques (tous avant métriques, tous documentés)

Tentatives Drive bloquées par quota (seq319–323) ; runs
`45039898675` et `45042946592` : échec du job d'analyse avant tout
calcul — d'abord un rejet de push du commit des livrables (corrigé
par un commit robuste), puis la cause racine établie par le
journal committé : dépendance `scipy` absente du job d'analyse
(crash à l'import, aucune sortie) ; correction minimale de la
liste de dépendances, puis run terminal `45044400978` entièrement
vert. Aucun paramètre du test n'a été modifié lors de ces
reprises ; aucune métrique n'a été consultée avant le run
terminal. Les journaux antérieurs (seq319, seq321, seq323 et
`PHASE12C2R3_VERIFY_LOG.txt`, `PHASE12C2_LOG.txt`) sont conservés.

## 6. Limites

1. Confirmation **historique hors IS**, pas une validation
   prospective en temps réel : le holdout est une période passée,
   désormais consommée pour ce modèle — toute réutilisation
   future de ces données pour sélectionner ou ajuster quoi que ce
   soit détruirait leur valeur de confirmation.
2. Les empreintes source proviennent du calcul du propriétaire
   dans Colab authentifié (provenance documentaire consignée,
   non une relecture Drive par la CI).
3. Le ratio de repli reste ≥ 1 quasi par construction de la
   réintégration ; le signal confirmé porte sur l'ensemble des
   cinq variables du modèle gelé, sans attribution causale.
4. Aucune portée économique : spreads, commissions, slippage,
   exécution et capacité sont hors périmètre ; rien ici ne fonde
   une stratégie.

## 7. Conclusion

- Migration : **`HOLDOUT_MIGRATION_VERIFIED`** (66/66).
- Évaluation H1 : **`CONFIRMED_HISTORICAL_HOLDOUT`** — le modèle
  H1 gelé, avec ses coefficients de la Phase 12-C.1 et M0 gelé,
  conserve et amplifie son amélioration prédictive (Brier
  +17,6 %, log-loss +11,1 % contre M0) sur la période indépendante
  2020–2026, avec une calibration quasi correcte (pente 0,942).
- H4 : inchangé, `NON_EVALUABLE_IN_PHASE12B`, hors périmètre.

Cette confirmation termine l'évaluation préenregistrée. Aucune
étape ultérieure — stratégie, exploitation économique, nouveau
test sur ce holdout — n'est autorisée automatiquement ; chacune
exigerait une décision distincte du responsable.

## 8. Traçabilité

Préflight et autorisations chaînées seq318–324 ; vérification et
évaluation : run terminal `45044400978` (vérification 66/66,
7/7 lots, analyse — tous verts), livrables committés par la CI ;
empreintes des livrables au checkpoint terminal chaîné après
seq324. Sources gelées intactes : protocole 12-A `580c39b1…`,
paramètres du modèle `1bcb3b70…`, manifeste de transfert
`b112b7ab…` inchangé.
