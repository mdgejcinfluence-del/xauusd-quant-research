# PHASE 14 — ANATOMIE TEMPORELLE MFE/MAE, CONFIANCE DU SIGNAL ET TROIS BARRIÈRES STRUCTURELLES

**Qualification obligatoire : `EXPLORATOIRE_IS — HYPOTHÈSES
POSTÉRIEURES AUX RÉSULTATS DE PHASE 13-B`. Ni confirmation
indépendante, ni preuve de rentabilité, ni stratégie. Commissions
`COMMISSION_EXCLUDED_BY_DESIGN` ; étiquettes par scénario :
S0 `NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE`,
S1 `…WITH_HYPOTHETICAL_0_5_BP_PER_SIDE`, S2
`…WITH_HYPOTHETICAL_1_0_BP_PER_SIDE`. Aucun résultat n'est « net
après tous les coûts ».**

**Verdicts : `MFE_MAE_SEQUENCE_ANALYZED` ;
`BARRIER_MATRIX_COMPLETED_EXPLORATORY_IS`.**

## 1. Cadre, gel et exécution

Préenregistrement gelé **avant tout calcul** (étape 14-A, seq333–334,
commit `7137b60`) : protocole `da9e52a5…`, grille `791424f4…`,
préenregistrement `e1cc412d…`, dictionnaire `3f6c5674…`. Cohorte
figée 13-B : 443 exposés (`p_M1 > 0,7591463414634146`), entrées
tick 13-B réutilisées telles quelles — **contrôle : 443/443 prix
d'entrée retrouvés à l'identique au premier tick du chemin, 0
divergent**. Chemins reconstruits depuis les ticks Bid/Ask IS
(8 lots CI, run final `45054081666` vert, exit 0 ; incidents
consignés aux journaux : import manquant, formats d'horodatage —
corrections du moteur seul, grille et protocole intacts). Liquidation
Bid (long) / Ask (court) partout ; aucun prix Mid pour la
liquidation ; aucun ordre déduit d'une barre M1. Le holdout n'a
été ni monté, ni listé, ni lu. La comparaison à la sortie fixe
13-B a été restreinte, conformément au protocole gelé, au
sous-ensemble comparable identique (421 clôtures conformes 13-B
classées ; les 22 incomplètes sont traitées séparément).

## 2. Question A — L'ordre MFE/MAE est une pièce d'anatomie, pas un signal

Sur les 443 trajectoires (toutes ordonnées, aucune ambiguïté de
timestamp, aucune censure d'ordre — les 22 incomplètes avaient
leurs deux extrêmes avant la première interruption) :

- **`MAE_BEFORE_MFE` : 223 (50,3 %) ; `MFE_BEFORE_MAE` : 220
  (49,7 %).** Le pire mouvement défavorable précède le meilleur
  mouvement favorable une fois sur deux : il n'existe pas
  d'« avance favorable » systématique à capturer tôt.
- MFE médian 24,9 bp atteint après un délai médian de ≈ 2,7 h ;
  MAE médian 21,5 bp après ≈ 2,7 h également. Les deux extrêmes
  surviennent à des horizons comparables et tardifs dans la
  fenêtre — la valeur favorable ne se matérialise pas avant le
  risque, elle coexiste avec lui.
- Cette description est **rétrospective** (chemin complet) : elle
  n'est pas disponible à l'entrée et ne fonde aucun filtre.

## 3. Confiance H1 (quartiles sur le seul `p_M1`, descriptif)

Seuils obtenus (consignés) : Q1 [0,7599 ; 0,7961], Q2 [0,7963 ;
0,8228], Q3 [0,8228 ; 0,8660], Q4 [0,8666 ; 0,9996] (111/111/111/110).

| Quartile | MFE avant MAE | MFE médian | MAE médian | Délai MFE médian | Délai MAE médian |
|---|---|---|---|---|---|
| Q1 | 37,8 % | 23,4 bp | 18,1 bp | ≈ 2,7 h | ≈ 1,6 h |
| Q2 | 58,6 % | 18,3 bp | 25,1 bp | ≈ 2,3 h | ≈ 3,1 h |
| Q3 | 55,0 % | 25,3 bp | 27,7 bp | ≈ 2,4 h | ≈ 3,2 h |
| Q4 | 47,3 % | 30,8 bp | 18,0 bp | ≈ 3,6 h | ≈ 2,9 h |

La relation confiance/anatomie n'est **pas monotone** : Q1 voit le
MAE arriver tôt (délai médian 1,6 h) et précéder le MFE dans
62 % des cas ; Q4 combine le MFE médian le plus élevé (30,8 bp)
et le MAE médian le plus faible (18,0 bp), mais sans avantage
d'ordre (47 % seulement de MFE d'abord, et plus tardivement).
Conformément au gel : Q4 reste un groupe descriptif, **pas une
règle d'exposition** ; aucun seuil de confiance n'est créé.

## 4. Question B — Les trois barrières sur la grille gelée (18 configurations, toutes rapportées)

Résultats S0 par événement (bp log, nets de spread, avant
commissions ; S1 = S0 − 1 bp et S2 = S0 − 2 bp par construction
des remplissages, aux arrondis près — voir matrice complète) :

**Normalisation A (`R_EVENT`) — échec net.** Les 9 configurations
sont négatives en moyenne (−1,7 à −2,5 bp) et en médiane, par
événement comme par grappe, dès S0. Le stop proportionnel à
l'amplitude pré-événement est atteint avant le take-profit dans
la grande majorité des cas (p. ex. B01 : 370 SL contre 73 TP) :
l'échelle `R_EVENT` est trop courte face à l'excursion défavorable
médiane (21,5 bp), et la barrière transforme le bruit adverse en
pertes réalisées systématiques. Comparée à la sortie fixe 13-B
(+0,11 bp sur le même sous-ensemble de 421), **chaque
configuration A dégrade le résultat**.

**Normalisation B (`ATR14_H1`) — hétérogène, jamais démontrée.**
Moyennes S0 de −1,5 à +1,9 bp selon la configuration. Les
configurations à barrières larges et symétriques ou asymétriques
favorables (B09 : TP 1,5×ATR / SL 1,5×ATR, moyenne +1,94,
médiane +4,25 ; B08 : +1,61 mais médiane −8,88 ; B06 : +0,34,
médiane +13,27) dépassent la moyenne de la sortie fixe sur le
sous-ensemble comparable (421 : p. ex. B09 +2,19 contre +0,11,
pondération grappe +2,36 contre +0,77), tandis que les
configurations serrées (B01, B04, B07) restent nettement
négatives avec des médianes vers −9 bp. **Sensibilité au
slippage** : à S1, B09 tombe à +0,94 et B08 à +0,61 ; à S2, B09
≈ −0,06 et B08 ≈ −0,39 — la fragilité aux coûts constatée en
13-B persiste, avant même toute commission. **Queues de perte** :
les stops ATR plafonnent la perte maximale entre −32 et −66 bp
selon la largeur (contre −203,5 bp en sortie fixe) — c'est le
bénéfice structurel réel des barrières : elles tronquent la
queue gauche, au prix de réaliser beaucoup de petites pertes
(médianes souvent négatives). Aucune configuration n'est
sélectionnée ni déclarée meilleure : ces écarts sont des
observations exploratoires sur une cohorte déjà étudiée, avec
18 configurations examinées (multiplicité assumée et rapportée
intégralement), et les configurations « favorables » ne le sont
que sous certains scénarios de slippage.

Par quartile (S0, ATR) : les moyennes de Q4 sont positives pour
les 9 configurations (jusqu'à +7,3 bp en B09), celles de Q2
presque toutes négatives — contraste descriptif cohérent avec le
§3, qui ne fonde **aucun filtre** : choisir Q4 après coup serait
exactement la sélection post-hoc interdite.

## 5. Couverture et ambiguïtés

209 trous de cotation > 5 min recensés ; 84 franchissements
déterminés au premier tick suivant un trou (prix réel utilisé,
drapeau consigné par événement) ; 0 ordre indéterminé, 0 censure
d'ordre, branche ATR disponible pour les 443 événements ; les 22
trajectoires incomplètes sont classées par barrière uniquement
lorsque le franchissement précède la première interruption (14 à
22 d'entre elles selon la configuration, comptées séparément
dans `PHASE14_CLUSTER_WEIGHTING.csv`), sinon censurées. Aucune
trajectoire complétée artificiellement. Détails :
`PHASE14_COVERAGE_AND_AMBIGUITIES.csv`.

## 6. Conclusions autorisées

1. Anatomie : le mouvement favorable ne précède pas
   systématiquement le mouvement défavorable (50/50), et les deux
   extrêmes sont tardifs et d'amplitudes comparables — la fenêtre
   de capture « propre » espérée n'existe pas dans cette cohorte.
2. Barrières : l'échelle `R_EVENT` est structurellement trop
   courte (dégradation universelle) ; l'échelle ATR tronque
   efficacement les pertes extrêmes et, pour ses configurations
   larges, affiche des moyennes S0 supérieures à la sortie fixe,
   mais avec des médianes souvent négatives et une fragilité
   immédiate au slippage (S2 ≈ 0 ou négatif), avant commissions.
3. **Aucune configuration n'est validée, sélectionnée ou
   recommandée.** Tout au plus, les configurations ATR larges
   constituent des candidates à une future évaluation
   prospective, après décision distincte et nouveau
   préenregistrement — sur des données n'ayant servi ni à la
   conception ni à la sélection, le holdout étant définitivement
   exclu. Le verdict `ECONOMICALLY_CONFIRMED_INDEPENDENTLY` reste
   interdit et n'est pas prononcé.

## 7. Livrables et traçabilité

`PHASE14_EVENT_PATH_SEQUENCE.csv` (`470c90aa…`, 443 lignes :
extrêmes, horodatages tick, délais, ordre, quartile) ;
`PHASE14_TRIPLE_BARRIER_EVENTS.csv` (`7d332e7e…`, événement ×
configuration × scénario) ; `PHASE14_BARRIER_MATRIX.csv`
(`f02b5d0b…`, 18 configurations × 3 scénarios, pondérations
événement et grappe) ; `PHASE14_CONFIDENCE_ANALYSIS.csv`
(`fcd25e7a…`) ; `PHASE14_CLUSTER_WEIGHTING.csv` (`29a61511…`,
comparaison à la sortie fixe sur sous-ensemble comparable) ;
`PHASE14_COVERAGE_AND_AMBIGUITIES.csv` (`ab36784c…`) ;
`PHASE14_RESULTS.json` (`e02b3ff2…`). Moteur
`ci_tools/phase14_engine.py`, jobs `lots14`/`analyse14`, run CI
`45054081666` (exit 0) ; chemins tick par lot et journaux
conservés dans le même répertoire.
