# PHASE 17-A — PROTOCOLE DE LA CIBLE ÉCONOMIQUE ET DU META-MODÈLE M2 (CONCEPTION)

**Nature : conception et audit de faisabilité. Aucun entraînement
de M2, aucune construction d'étiquettes économiques nouvelles,
aucune nouvelle performance économique, aucune sélection B08/B09
ne sont effectués dans cette étape.**

## 1. Architecture à deux couches

- **M1 (gelé, intact)** : modèle H1 de la Phase 12-C.1
  (`PHASE12C1_MODEL_PARAMETERS.json`, `1bcb3b70…`), confirmé
  historiquement hors IS en 12-C.2. Il fournit la direction et la
  probabilité de reprise ; filtre primaire inchangé :
  `p_M1 > 0,7591463414634146`. Aucune modification, réestimation
  ou recalibrage.
- **M2 (`M2_ECONOMIC_META_LABELER`, à construire en Phase 17-B
  sous décision distincte)** : modèle secondaire qui, **étant
  donné un signal M1 filtré**, estime la probabilité que
  l'exploitation de cette opportunité sous un contrat d'exécution
  précis produise un résultat économique positif après les coûts
  modélisés. M2 ne prédit ni la direction ni la reprise : il
  prédit le résultat du contrat.
- **Décision d'exposition (future)** : exposition envisagée
  seulement si l'espérance économique estimée par M2 est
  strictement positive (seuil dérivé des gains/pertes moyens
  d'apprentissage uniquement, §6) — jamais un seuil optimisé sur
  l'évaluation.

## 2. Contrats économiques de référence (deux hypothèses distinctes)

Entrée **E0** pour les deux (premier Ask long / Bid court
strictement postérieur à `t_decision`, fenêtre 60 s, conventions
13-A.1) ; échéance verticale : fin de la fenêtre des huit bougies
H1 ; ATR14_H1 figé à `t_decision` (conventions Phase 14) :

- **M2-B08** : TP = 1,5 × ATR, SL = 1,0 × ATR ;
- **M2-B09** : TP = 1,5 × ATR, SL = 1,5 × ATR.

Aucune troisième configuration, aucun nouveau multiplicateur,
aucune optimisation d'ATR, **aucune sélection entre B08 et B09 en
fonction des résultats de la Phase 17** : les deux modèles seront
entraînés, évalués et rapportés en parallèle, intégralement.

## 3. Cible économique `Y_ECON` (définition complète au fichier JSON lié)

Pour chaque événement filtré par M1 et exécuté en entrée E0, le
P&L de liquidation est calculé aux prix Bid/Ask réels sous le
contrat (première barrière touchée ou échéance verticale, prix du
tick de franchissement, conventions Phase 14/14.1) :

- **Scénario primaire de labellisation : S2** (spread intégré une
  fois + slippage hypothétique 1,0 bp par côté appliqué
  défavorablement aux remplissages d'entrée et de sortie) ;
  étiquette obligatoire :
  `NET_OF_SPREAD_AND_HYPOTHETICAL_S2_SLIPPAGE_BEFORE_COMMISSION`.
- `Y_ECON = 1` si P&L strictement positif ; `Y_ECON = 0` si P&L
  nul ou négatif. Le mécanisme (`TP_FIRST`, `SL_FIRST`,
  `VERTICAL_FIRST`) est conservé à côté de l'étiquette.
- `CENSORED`, `GAP_CROSSING_UNRESOLVED`, `ORDER_UNRESOLVED` :
  **jamais transformés** en 0 ou 1 ; exclus de l'apprentissage et
  de l'évaluation du modèle, comptés et publiés séparément.
- S0 et S1 : analyses de sensibilité seulement (même mécanisme,
  slippage 0 / 0,5 bp par côté), jamais utilisées pour choisir le
  scénario primaire après coup. Commissions exclues par
  conception (`COMMISSION_EXCLUDED_BY_DESIGN`) ; la commission
  aller-retour théorique d'équilibre (moyenne des P&L
  d'apprentissage divisée par l'effectif, borne théorique) sera
  rapportée sans jamais l'assimiler à un tarif.

## 4. Variables M2 (toutes disponibles à `t_decision`, audit anti-fuite au dictionnaire)

Candidates gelées : les cinq variables causales de M1
(`RATIO_REPLI_EXTENSION_A_TREINT`, `DUREE_EXTREME_VERS_TREINT_MIN`,
`MFE_A_TREINT_BP`, `NB_TOUCHES_P0_AVANT_TREINT`,
`SESSION_REINTEGRATION`), `ATR14_H1` à `t_decision`,
`SPREAD_DECISION_BP` (spread médian de la minute M1 se terminant
à `t_decision`, issu des barres Bid/Ask 13-B).
**`p_M1` est EXCLU des variables M2** : aucune série de
prédictions M1 strictement hors échantillon n'existe pour les
observations d'apprentissage 2010–2015 (le modèle y a été ajusté) ;
utiliser ces probabilités en apprentissage comme si elles étaient
hors échantillon serait une fuite. `p_M1` reste utilisé
uniquement comme **filtre primaire séparé** (règle gelée), en
amont de M2, à tous les segments. Aucune variable postérieure à
`t_decision`, aucun MFE/MAE futur, aucun archétype final, aucun
dérivé de la cible.

## 5. Séparation chronologique, grappes, purge (existantes, réutilisées)

Ensembles de la Phase 12-B repris tels quels (colonne `ensemble`
des features, affectation par grappe entière au premier événement
réintégré, aucune grappe partagée — revérifié en 17-A : 0 grappe
multi-ensembles) : **APPRENTISSAGE 2010–2015** (1 640 étiquetés
directionnels F10-01 ; **1 143** passent le filtre M1 gelé),
**CALIBRATION 2016–2017** (507 ; 360 filtrés),
**EVALUATION 2018–2020** (543 ; **443 filtrés — exactement les
exposés des Phases 13-B à 16**, cohérence vérifiée). La purge des
chevauchements d'horizon est déjà matérialisée (événements dont
`fin_fenetre_observation` franchit le segment suivant exclus avec
motif, grappe entière) ; l'intervalle d'étiquetage complet
[`t_decision`, `fin_fenetre`] est ainsi contenu dans le segment
de la grappe. Aucune séparation aléatoire. L'évaluation 2018–2020,
déjà utilisée par les Phases 12-B à 16, ne pourra **jamais** être
qualifiée de confirmation indépendante : au mieux une évaluation
chronologique exploratoire ; le niveau 3 exigerait des données
postérieures au gel de la Phase 17.

## 6. Baseline, modèle et seuil économique (à exécuter en 17-B)

- `M0_ECON` (par contrat) : fréquence de `Y_ECON = 1` sur le seul
  apprentissage filtré ; jamais le M0 directionnel de M1.
- M2 : **régression logistique simple** (variables du §4 brutes,
  encodage SESSION identique à M1, référence ASIA), aucun réglage
  automatique, aucune recherche de variables, aucune sélection de
  modèle après observation des performances. Métriques contre
  `M0_ECON` : Brier (primaire), log-loss, calibration (pente,
  ordonnée, déciles), AUC en diagnostic secondaire seulement.
- **Seuil de décision économique** : à partir des seuls P&L
  d'apprentissage — gain moyen conditionnel `G` (P&L > 0) et perte
  moyenne conditionnelle `L` (P&L ≤ 0, en valeur absolue) ;
  exposition si `q × G − (1 − q) × L > 0`, soit `q > L / (G + L)`
  où `q` est la probabilité M2. Seuil calculé et gelé sur
  l'apprentissage avant toute évaluation ; si `G` ou `L` n'est pas
  estimable (classe absente ou effectif insuffisant) :
  `NON_EVALUABLE`.
- **Critères de non-évaluabilité préenregistrés** (par contrat et
  par segment d'évaluation) : moins de 100 observations étiquetées
  `Y_ECON` ou classe minoritaire inférieure à 50 ⇒
  `NON_EVALUABLE`, sans pooling ni assouplissement.

## 7. Ce que la Phase 17 ne fera jamais

Modifier M1 ou son seuil ; réintroduire E1/E2/E3 ; créer un
troisième contrat ; optimiser multiplicateurs, seuil M2 ou
variables sur l'évaluation ; qualifier l'IS de confirmation ;
entraîner un modèle H4 (branche distincte, cf. bilan documentaire
lié) ; engager un capital ou une stratégie.
