# PHASE 17-D — PROTOCOLE DU MODÈLE DE PAYOFF CONTINU NORMALISÉ PAR LE RISQUE

**Statut : conception et préenregistrement. Aucun entraînement effectué ni autorisé par la présente phase.**
Qualification permanente de l'évaluation 2018–2020 : HISTORIQUE EXPLORATOIRE — POPULATION DÉJÀ ÉTUDIÉE. Holdout 2020–2026 définitivement exclu.

## 1. Question
Le meta-labeling binaire 17-B ne classait pas le signe économique (17-C : MEC-1 à MEC-4). La présente conception change uniquement la **représentation de la cible** : prédire `E[R_REALIZED_S2 | X]`, l'espérance du payoff continu normalisé par le risque initial, à dictionnaire de variables inchangé. Question : une cible continue normalisée capture-t-elle l'amplitude et le régime que la classification binaire a perdus ?

## 2. Population et filtre (inchangés)
Événements H1 du modèle M1 gelé, filtre `p_M1 > 0.7591463414634146`, direction et probabilité de reprise fournies par M1 sans aucune modification. `p_M1` reste **exclu** des variables (pas de série strictement hors échantillon sur 2010–2015). Biais hérité documenté : l'apprentissage est filtré par M1 en échantillon ; il n'est ni corrigé ni réentraîné.

## 3. Contrats (inchangés, séparés)
B08 : TP 1,5 ATR / SL 1,0 ATR ; B09 : TP 1,5 ATR / SL 1,5 ATR ; entrée E0, échéance 8 bougies H1. Aucun pooling, aucune sélection de contrat.

## 4. Cible
`R_REALIZED_S2 = PNL_S2_bp / INITIAL_RISK_BP`, `INITIAL_RISK_BP = k × ATR14_H1 / prix_entrée × 10000` (k = 1,0 B08 ; 1,5 B09 ; ATR connu à `t_decision`). Payoffs calculés aux prix exécutables gelés 17-B : aucun +1R/−1R automatique (franchissements et gaps font foi). Inclus : TP_FIRST, SL_FIRST, VERTICAL_FIRST. Exclus : CENSORED, GAP_CROSSING_UNRESOLVED, ORDER_UNRESOLVED, NON_EXECUTION. Aucune winsorisation ni plafonnement ; les extrêmes sont conservés et documentés. Les P&L en bp restent toujours rapportés à côté des R.

## 5. Modèle candidat (à entraîner uniquement sur décision distincte, Phase 17-E éventuelle)
Régression linéaire simple des moindres carrés `E[R|X]` sur les sept variables gelées (contrat `PHASE17D_FEATURE_CONTRACT.csv`), séparément par contrat (`M2R_B08`, `M2R_B09`), estimée sur le seul apprentissage. Référence `M0_R` = moyenne d'apprentissage de R, par contrat. Aucun modèle concurrent implémenté en 17-D ; l'intérêt documentaire de quantiles séparés est examiné dans le rapport de faisabilité, sans implémentation.

## 6. Segments
Apprentissage 2010–2015 (estimation M0_R et M2R) ; calibration 2016–2017 (validation chronologique et diagnostic uniquement — aucun ajustement, aucune calibration de paramètres, aucun choix) ; évaluation 2018–2020 (exploratoire). Grappes entières par segment, purge de chevauchement 12-B conservée (2 événements / 1 grappe exclus), aucune séparation aléatoire.

## 7. Règle de décision gelée
`PREDICTED_EXPECTED_R > 0` : espérance prédite strictement positive. Règle mathématique, non optimisée ; aucun seuil ne sera recherché sur calibration ou évaluation.

## 8. Limites connues d'emblée
Moyenne conditionnelle sensible aux queues (documentées dans l'audit de distribution, sans les tronquer) ; hétéroscédasticité résiduelle possible (corrélation ATR–|P&L| de 0,38 à 0,74 en bp, ramenée proche de zéro en R) ; dérive de moyenne de R entre segments non exclue par la normalisation (la normalisation stabilise l'échelle, pas nécessairement le niveau) ; population déjà étudiée ; commissions exclues par construction (`COMMISSION_EXCLUDED_BY_DESIGN`).

## 9. Interdictions perpétuées
Aucun accès holdout ; aucun recalcul de P&L depuis les ticks ; aucune nouvelle variable ; aucun MFE/MAE final, archétype ou mécanisme comme prédicteur ; aucune optimisation ; aucun sous-groupe ; H4 distinct et non entraîné ; S12, T0/J2/J3 intacts ; budget 0.
