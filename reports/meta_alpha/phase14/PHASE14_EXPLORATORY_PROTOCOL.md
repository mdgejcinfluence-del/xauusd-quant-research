# PHASE 14 — PROTOCOLE EXPLORATOIRE (ÉTAPE 14-A, GELÉ AVANT TOUT CALCUL)

**Qualification obligatoire de tous les résultats : `EXPLORATOIRE_IS —
HYPOTHÈSES POSTÉRIEURES AUX RÉSULTATS DE PHASE 13-B`. Cette étude ne
constitue ni une confirmation indépendante, ni une preuve de
rentabilité, ni une stratégie. Le verdict
`ECONOMICALLY_CONFIRMED_INDEPENDENTLY` est interdit à l'issue de
cette phase. Commissions : `COMMISSION_EXCLUDED_BY_DESIGN` (étiquettes
de scénarios au §6). Holdout 2020–2026 : strictement exclu (ni monté,
ni listé, ni lu).**

## 1. Cohorte figée (aucune extension, aucune redétection)

Population de la Phase 13-B, reprise telle quelle depuis
`PHASE13B_EVENT_EXECUTIONS.csv` (`20c5ae22…`) : 543 candidats F10-01
H1 de l'ensemble EVALUATION 2018–2020 ; **443 événements exposés**
(`p_M1 > 0,7591463414634146`, M0 gelé, règle inchangée), tous
exécutés à l'entrée en 13-B (0 NON_EXECUTION), dont **421 clôtures
conformes** et **22 trajectoires incomplètes** individuellement
identifiées. Entrées réelles 13-B réutilisées telles quelles
(premier tick strictement postérieur à `t_decision`, prix et
horodatage exacts conservés) : aucune nouvelle entrée, aucun prix
recalculé. Modèle H1, coefficients, M0, grappes (`grappe_id`
existants, jamais recalculés) et populations sont intouchables.

## 2. Question A — Anatomie temporelle MFE/MAE

Pour chaque événement exposé, le chemin post-entrée est reconstruit
depuis les **ticks Bid/Ask IS** (partitions IS des datasets Kaggle
privés du propriétaire, lots CI comme en 13-B), évalué aux **prix de
liquidation** : Bid pour une position longue, Ask pour une position
courte. Les prix Mid ne remplacent jamais les prix de liquidation.
Aucun ordre n'est jamais déduit des haut/bas d'une même barre M1 :
les extrêmes et leurs horodatages proviennent de la séquence tick,
à sa résolution réelle.

Mesures par événement : MFE maximal et son premier horodatage
d'atteinte, MAE maximal et son premier horodatage, délais
entrée→MFE et entrée→MAE (secondes), délai entre extrêmes, statut
d'ordre : `MFE_BEFORE_MAE`, `MAE_BEFORE_MFE`,
`MFE_MAE_SAME_TIMESTAMP` (même horodatage tick, séquence fiable
absente pour départager au sein du même timestamp — conservé tel
quel), `ORDER_UNRESOLVED` (données insuffisantes pour ordonner),
`CENSORED` (trajectoire interrompue avant décision). Les 22
trajectoires incomplètes restent séparées ; elles ne reçoivent un
ordre que si les deux extrêmes sont atteints de façon certaine
avant l'interruption, sinon `CENSORED`.
**Distinction essentielle** : l'ordre MFE/MAE du chemin complet est
une description rétrospective ; il n'est pas disponible à l'entrée
et ne doit jamais être présenté ni utilisé comme filtre prédictif.

## 3. Confiance H1 (descriptif uniquement)

Les 443 exposés sont répartis en quatre groupes ordonnés **sur le
seul `p_M1`** (aucune consultation des performances, MFE, MAE ou
cibles) : classement croissant par (`p_M1`, `event_id`) comme
départage déterministe en cas d'égalité, groupes de tailles
111/111/111/110 (Q1 = quart inférieur … Q4 = quart supérieur).
Les seuils de `p_M1` réellement obtenus à chaque frontière sont
consignés dans les résultats. Par groupe : effectif, distribution
de `p_M1`, fréquences des ordres, MFE/MAE médians, délais médians,
résultats de barrières (§5). **Q4 est un groupe descriptif de forte
confiance, jamais une nouvelle règle d'exposition** ; aucun
cinquième groupe, aucun seuil de confiance optimal, aucun filtre
supplémentaire. La règle d'exposition reste exclusivement
`p_M1 > 0,7591463414634146`.

## 4. Échelles de risque (connues à `t_decision`, aucune donnée future)

- **Normalisation A — `R_EVENT = MFE_A_TREINT_BP`** : variable gelée
  de la Phase 12-B (`PHASE12B_FEATURES.csv`, `6f684ee8…`), excursion
  favorable atteinte au plus tard à `t_reintegration`, en bp log.
  Utilisée exactement dans son unité gelée, jamais remplacée par le
  MFE final de fenêtre. Distances de barrières converties en prix
  par la convention exponentielle des rendements log :
  niveau = prix d'ancrage × exp(± multiplicateur × R_EVENT / 10000).
- **Normalisation B — `ATR14_H1` (Wilder)** : bougies H1 Mid
  reconstruites depuis les barres M1 Bid/Ask 13-B (Mid = séries
  mo/mh/ml/mc issues des ticks) ; seules les bougies H1 **entièrement
  clôturées** à `t_decision` (fin de bougie ≤ `t_decision`) ;
  True Range = max(High−Low, |High−PreviousClose|,
  |Low−PreviousClose|) ; initialisation = moyenne arithmétique des
  14 premiers TR ; lissage de Wilder `(13×ATR + TR)/14`. L'ATR sert
  uniquement d'unité de distance (en prix) ; détection et exécution
  restent sur Bid/Ask réels. Si l'historique H1 disponible avant
  `t_decision` compte moins de 15 bougies, la branche ATR est
  `UNAVAILABLE` pour l'événement (consigné, aucune substitution,
  aucune troisième normalisation).

## 5. Trois barrières — grille gelée (18 configurations, toutes rapportées)

Barrière verticale : **échéance 13-B inchangée** (fin de la fenêtre
des huit bougies H1 suivant l'événement ; jamais huit heures après
l'entrée, jamais déplacée). Barrières horizontales ancrées au prix
exécutable d'entrée 13-B (avant slippage hypothétique) :

- Long : TP déclenché quand le **Bid** ≥ niveau TP ; SL quand le
  **Bid** ≤ niveau SL. Niveaux : ancrage Ask d'entrée, distances
  §4 (A : multiplicateur × R_EVENT en bp log ; B : multiplicateur ×
  ATR en prix).
- Court : TP quand l'**Ask** ≤ niveau TP ; SL quand l'**Ask** ≥
  niveau SL. Ancrage Bid d'entrée, symétrique.

Grille (`PHASE14_BARRIER_GRID.json`) : TP, SL ∈ {0,5 ; 1,0 ; 1,5} ×
R — 9 configurations par normalisation, **18 au maximum, toutes
rapportées**, aucune supprimée pour résultat défavorable, aucune
déclarée « meilleure » pour un usage réel.
Franchissement détecté sur le **premier tick réel** dont le prix de
liquidation atteint ou dépasse le niveau (dans le sens défavorable
au franchissement : en cas de gap au-delà du niveau, le prix de
sortie est le premier prix exécutable réellement observé à son
horodatage — jamais le niveau théorique). Statuts par
événement/configuration : `TP_FIRST`, `SL_FIRST`, `VERTICAL_FIRST`,
`CENSORED`, `GAP_CROSSING_UNRESOLVED`, `ORDER_UNRESOLVED`.
Définitions opérationnelles gelées : un **trou de cotation** est un
intervalle > 5 minutes sans tick dans la fenêtre ; si le premier
tick suivant un trou franchit une barrière, le franchissement est
déterminable (une seule barrière peut être franchie par un prix
unique) et le prix de ce tick est utilisé, avec drapeau
`GAP_AVANT_FRANCHISSEMENT` ; `GAP_CROSSING_UNRESOLVED` est réservé
aux cas où la trajectoire disponible ne permet pas de localiser le
franchissement (données interrompues avant toute décision) ;
`ORDER_UNRESOLVED` aux égalités de timestamp intratick
indépartageables. Pour les 22 trajectoires incomplètes : une
barrière n'est classée que si son tick de franchissement est
strictement antérieur à la première interruption de la trajectoire
(premier trou de cotation ou fin des ticks disponibles) ; sinon
`CENSORED`. Aucune trajectoire n'est complétée artificiellement.

## 6. Coûts (conventions 13-A.1 inchangées)

Spread intégré une seule fois aux prix Bid/Ask. Les barrières sont
déclenchées sur les cotations réelles **non ajustées** du slippage ;
le slippage ne modifie que les prix de remplissage économiques
(entrée et sortie dégradées défavorablement selon la direction,
formules 13-A.1). Scénarios gelés S0/S1/S2 = 0 / 0,5 / 1,0 bp par
côté, étiquettes obligatoires : S0
`NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE`,
S1 `NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_0_5_BP_PER_SIDE`,
S2 `NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_1_0_BP_PER_SIDE`.
Jamais « net après tous les coûts » ni « rentabilité nette
complète ».

## 7. Calculs et comparaisons (tous préenregistrés)

Par configuration (18) × scénario (3) : effectifs TP/SL/VERTICAL/
censures/indéterminés, durée de détention, rendement moyen et
médian, part de positifs, quantiles P1/P5/P25/P75/P95/P99, perte et
gain maximaux, MFE/MAE. Deux pondérations : par événement, et par
grappe (moyenne intra-grappe puis moyenne des grappes à poids égal,
distributions présentées séparément). **Comparaison obligatoire** :
chaque configuration est comparée à la sortie fixe huit H1 de 13-B
sur **exactement le même sous-ensemble d'événements comparables**
(événements à la fois clôturés conformes en 13-B et classés sans
ambiguïté pour la configuration) ; les 22 incomplètes sont
présentées séparément ; aucune amélioration ne peut provenir d'un
changement de dénominateur. Présentations : ensemble des 443, et
par quartile Q1–Q4 avec effectifs de chaque cellule (descriptif ;
aucun quartile choisi, aucun déclaré règle).
Contrôles de validité : intégrité et ordre chronologique des ticks,
doublons, UTC, Bid/Ask finis et positifs, trous de cotation,
cohérence des prix d'entrée/sortie avec 13-B, disponibilité ATR et
R_EVENT, intégrité des identifiants et des grappes, absence de
fuite temporelle (toute quantité utilisée à la décision est
disponible à `t_decision`). Seuils 13-A.1 préservés (NON_EXECUTION
et spreads non finis — hérités de 13-B : 0/443 et 0/842, reconstatés
à l'identique). **Aucun nouveau seuil de réussite n'est ajouté.**

## 8. Verdicts autorisés

Anatomie : `MFE_MAE_SEQUENCE_ANALYZED` ou `SEQUENCE_ANALYSIS_BLOCKED`.
Barrières : `BARRIER_MATRIX_COMPLETED_EXPLORATORY_IS`,
`BARRIER_MATRIX_INCONCLUSIVE`, `BARRIER_MATRIX_NON_MESURABLE` ou
`BARRIER_MATRIX_BLOCKED`. Aucune configuration « gagnante » ne sera
sélectionnée ; une configuration éventuellement favorable ne pourra
être que candidate à une future évaluation prospective, après
décision distincte et nouveau préenregistrement.
