# PHASE 16 — PROTOCOLE D'ENTRÉE PASSIVE E3 (GELÉ AVANT TOUT CALCUL)

**Qualification : exploratoire IS, cohorte déjà étudiée. Ni
stratégie validée, ni confirmation indépendante. Modèle H1, M0,
probabilités, identifiants et grappes inchangés (cohorte figée :
443 exposés, 421 complètes, 22 incomplètes). Holdout interdit.
Commissions `COMMISSION_EXCLUDED_BY_DESIGN`.**

## 1. Politique unique E3 (aucune variante)

Après `t_decision` (clôture M1 de confirmation, définition gelée) :

1. **Cotation de référence** : première cotation Bid/Ask réelle
   strictement postérieure à `t_decision` — matériellement le tick
   d'entrée E0 de la Phase 13-B (`Bid_0`, `Ask_0`, horodatage
   conservés). `P_limit = (Bid_0 + Ask_0) / 2`.
2. **Ordre limite unique et fixe** : Buy Limit (long) / Sell Limit
   (court) à `P_limit`, actif après la réception de la cotation de
   référence, **expirant à `t_decision + 60 secondes`** (fenêtre
   stricte : observations de franchissement cherchées pour
   `timestamp_référence < ts ≤ t_decision + 60 s`). Jamais déplacé,
   jamais prolongé, jamais réessayé.
3. **Remplissage candidat** : première observation ultérieure dans
   la validité avec `Ask < P_limit` (long) ou `Bid > P_limit`
   (court) — inégalités **strictes** (une égalité n'est pas un
   franchissement). Prix de remplissage retenu : **`P_limit`**, sans
   amélioration de prix supposée (le prix de la cotation de
   franchissement n'est pas encaissé).
4. Sinon : **`NO_FILL`** — ni perte ni gain ; l'événement reste
   dans tous les dénominateurs de cohorte et n'est jamais masqué.

Statut de preuve du remplissage (voir
`PHASE16_FILLABILITY_AUDIT.md`) : les ticks disponibles sont des
**cotations Bid/Ask** — ni transactions exécutées, ni volume, ni
profondeur, ni priorité de file ne sont observables. Tous les
remplissages de cette étude portent donc le statut
**`QUOTE_CROSSING_PROXY_ONLY`** : franchissement de cotation
observé, exécution réelle **non prouvée**. Aucun résultat ne sera
présenté comme celui d'un ordre réellement exécutable.

## 2. Sorties, coûts et matrice (gelés)

Sorties conservées uniquement : **X0** (échéance originale des
huit bougies H1, prix 13-B), **X1** (ATR B08 : TP 1,5 × ATR /
SL 1,0 × ATR), **X2** (ATR B09 : 1,5 / 1,5) — ATR figé à
`t_decision` (valeur Phase 14), barrières ancrées sur `P_limit`
(prix de remplissage de référence), déclenchement au premier tick
de liquidation après le remplissage (conventions Phase 14/14.1 :
gap au premier prix observable, drapeau ; trajectoires
incomplètes : barrière classée seulement avant la première
interruption, sinon `CENSORED` ; verticale indisponible pour une
trajectoire incomplète sans franchissement : `CENSORED`).
Matrice exacte : E3 × {X0, X1, X2} × {S0, S1, S2} = **9 cellules**,
toutes présentées, aucune sélection, aucun offset ni délai
supplémentaire testé.
**Coûts — différence assumée avec l'entrée au marché** : l'entrée
limite n'est jamais remplie moins favorablement que `P_limit`
(aucun slippage d'entrée) ; les scénarios portent sur la seule
sortie : S0 = 0, S1 = 0,5 bp, S2 = 1,0 bp de slippage défavorable
à la liquidation (formules de dégradation 13-A.1 appliquées au
seul prix de sortie). Étiquettes : S0
`NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE`,
S1 `NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_0_5_BP_EXIT_SLIPPAGE`,
S2 `NET_OF_SPREAD_BEFORE_COMMISSION_WITH_HYPOTHETICAL_1_0_BP_EXIT_SLIPPAGE`.
Spread intégré une fois (le prix d'entrée `P_limit` est intérieur
au spread de référence : l'amélioration comptée est exactement la
demi-largeur du spread initial lorsque le franchissement a lieu —
elle sera présentée comme telle, mécanique et non comme un gain
d'exécution prouvé). Jamais de rentabilité nette complète.

## 3. Comparaisons et présentations gelées

Présentations obligatoires, toujours ensemble : (1) conditionnel
aux événements remplis et mesurés ; (2) **cohorte entière de 443**
(non-remplis comptés 0 dans les moyennes de cohorte) ; (3)
opportunités non capturées (`NO_FILL`, délais, événements dont le
marché a continué sans revenir). Comparaison à E0 : (a) référence
standard réconciliée (13-B/Phase 14, prix et scénarios d'origine) ;
(b) **référence E0 rendue comparable** : rendements E0 recalculés
depuis les prix 13-B avec slippage de sortie seule (0 / 0,5 / 1,0
bp), pour comparer à convention de coûts identique. Mesures :
taux de franchissement, taux `NO_FILL`, délai de franchissement
(médiane, distribution), amélioration de prix vs E0
(`direction × ln(prix_E0 / P_limit) × 10000` bp), MFE/MAE après
remplissage, durée restante jusqu'à l'échéance, TP/SL/VERTICAL/
censures, quantiles et perte maximale par cellule, pondérations
événement et grappe (moyenne intra-grappe puis moyenne des
grappes), commission théorique d'équilibre (moyenne S0, borne
théorique, jamais un tarif). Quartiles Q1–Q4 descriptifs
uniquement. Aucune courbe de capital.

## 4. Critères de verdict gelés

- **Structure passive** : `PASSIVE_ENTRY_STRUCTURE_IDENTIFIED` si
  le taux de franchissement (remplissages proxy / 443) est
  ≥ 50 % ; `PASSIVE_ENTRY_STRUCTURE_NOT_IDENTIFIED` s'il est
  < 25 % ; sinon `PASSIVE_ENTRY_ANALYSIS_INCONCLUSIVE`.
- **Qualité d'exécution** : `QUOTE_CROSSING_PROXY_ONLY` (établi
  par l'audit de remplissabilité, §1) ; `TRADE_FILL_SUPPORTED`
  exigerait des preuves de transactions indisponibles ;
  `FILLABILITY_NOT_MEASURABLE` si même les franchissements
  n'étaient pas observables.
- **Économie (comparaison primaire X0, cohorte 443, convention de
  sortie seule comparable)** :
  `EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_FOUND` si la moyenne de
  cohorte E3 dépasse celle d'E0 sous S0 **et** S1 **et** S2 avec,
  sur le sous-ensemble rempli et complet, une médiane non
  inférieure à celle d'E0 sur le même sous-ensemble ;
  `EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_NOT_FOUND` si E3 est
  inférieure ou égale à E0 en moyenne de cohorte sous les trois
  scénarios ; sinon `ECONOMICALLY_INCONCLUSIVE` ; `NON_MESURABLE`
  / `BLOCKED` selon les contrôles hérités et les réconciliations.
  Même « trouvé », l'avantage resterait un proxy de franchissement
  sur IS, jamais une stratégie validée.

## 5. Interdictions (rappel)

Aucun repositionnement ni second essai ; aucun autre offset de
limite ; aucun autre délai ; aucune autre politique ; aucune
nouvelle barrière ; aucune sélection post-hoc ; modèle, M0,
probabilités, populations, grappes intouchables ; holdout
interdit ; aucune dépense.
