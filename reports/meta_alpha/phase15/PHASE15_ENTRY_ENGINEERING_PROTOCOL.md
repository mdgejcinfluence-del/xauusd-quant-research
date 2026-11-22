# PHASE 15 — PROTOCOLE D'ENGINEERING DU POINT D'ENTRÉE (GELÉ AVANT TOUT CALCUL)

**Qualification : recherche exploratoire IS sur cohorte déjà
étudiée (hypothèses postérieures aux Phases 13-B/14). Ni stratégie
validée, ni confirmation indépendante. Modèle H1, M0, probabilités
`p_M1`, `event_id`, `grappe_id` repris sans aucun recalcul
(`PHASE13B_EVENT_EXECUTIONS.csv`, `20c5ae22…`). Holdout 2020–2026
strictement interdit. Commissions `COMMISSION_EXCLUDED_BY_DESIGN`.**

## 1. Cohorte et références figées

543 candidats F10-01 H1 EVALUATION 2018–2020 ; **443 exposés**
(`p_M1 > 0,7591463414634146`) ; 421 trajectoires complètes, 22
incomplètes (identifiées individuellement, jamais retirées des
dénominateurs de couverture). Échéance verticale commune : fin de
la fenêtre originale des huit bougies H1 (`fin_fenetre`), inchangée
même pour les entrées retardées. `P0` par événement :
`PHASE11C_EVENT_PATHS.csv` (disponible pour les 443 exposés).

## 2. Définitions causales gelées (aucune variable future)

- **Bougie M1** : barres M1 de la Phase 13-B (issues des ticks IS) ;
  sa clôture retenue pour les déclencheurs est la **clôture Mid
  (`mc`)**, son horodatage de clôture = début de minute + 60 s.
  Bougies candidates : début de minute ≥ `t_decision` (première
  clôture à `t_decision` + 60 s) et clôture ≤ `fin_fenetre`.
- **E0 (référence)** : entrée 13-B inchangée (premier Ask/Bid
  strictement après `t_decision`, < 60 s) — reprise des artefacts
  13-B/14, jamais recalculée.
- **E1 (récupération de P0)** : première bougie candidate entièrement
  clôturée telle que `direction × (clôture Mid − P0) > 0`
  (strict). Déclenchement à sa clôture ; entrée au premier tick
  réel (Ask long / Bid court) avec
  `clôture_déclenchante < timestamp_tick < clôture_déclenchante + 60 s`.
- **E2 (deux clôtures directionnelles)** : référence C0 = clôture
  Mid de la bougie se terminant à `t_decision`. On parcourt les
  bougies candidates dans l'ordre ; une progression est comptée
  entre deux bougies **adjacentes** (débuts distants de 60 s
  exactement) lorsque la clôture progresse dans la direction
  (LONG : strictement croissante ; SHORT : strictement
  décroissante), la première progression pouvant partir de C0 si
  la première bougie candidate est adjacente à la bougie de C0.
  Toute minute absente rompt la chaîne (la bougie suivant
  l'absence devient la nouvelle référence, sans progression
  comptée). Déclenchement à la clôture de la **deuxième**
  progression consécutive ; entrée comme E1 (60 s strictes).
- Si aucun déclenchement avant l'échéance : `NO_ENTRY_TRIGGER`
  (opportunité non capturée, **jamais une perte**). Si
  déclenchement mais aucun tick dans la fenêtre de 60 s, ou
  premier tick ≥ `fin_fenetre` : `NON_EXECUTION` (motif consigné).
- Prix d'entrée E1/E2 extraits des **ticks IS réels** (lots CI) ;
  horodatages exacts conservés. Aucune interpolation, aucun prix
  Mid pour l'exécution.

## 3. Anatomie du chemin post-signal (descriptive, temps relatif)

Depuis `t_decision`, aux prix de liquidation (Bid long / Ask
court) : séquence des extrêmes tick (artefacts Phase 14) —
premier extrême (type, valeur, horodatage), profondeur et durée du
premier repli (premier extrême adverse de la séquence alternée),
vitesse (profondeur/durée), instant de récupération (premier
extrême favorable ramenant l'excursion ≥ 0 après le premier
repli), nombre d'alternances d'extrêmes, distance à P0 et au prix
E0 à chaque entrée. Fenêtres relatives gelées : 0–1, 1–5, 5–15,
15–30, 30–60 min, 1–2 h, 2–4 h, 4–8 h : déplacement directionnel
(clôtures M1 de liquidation), excursions adverse/favorable
cumulées (extrêmes tick), spread médian des minutes, part des
clôtures M1 progressant dans la direction. Ces fenêtres décrivent
le chemin ; elles ne deviennent pas des délais optimisés.
Chronologie causale : chaque état ne dépend que des données
observées à son timestamp ; les extrêmes finaux MFE/MAE ne sont
jamais utilisés comme information d'entrée.

## 4. Sorties conservées (exactement trois) et matrice

X0 : échéance huit bougies H1 (prix de sortie 13-B pour les
trajectoires complètes ; entrée retardée ne déplace pas
l'échéance). X1 : ATR B08 (TP 1,5 × ATR14_H1, SL 1,0 × ATR14_H1) ;
X2 : ATR B09 (TP 1,5, SL 1,5) — ATR figé à `t_decision` (valeur
Phase 14), niveaux ancrés au **prix réel d'entrée de chaque
politique**, déclenchement au premier tick de liquidation
(conventions Phase 14 : prix du tick franchissant, gap au premier
prix observable, drapeau ; ordre intra-gap indéterminé :
`GAP_CROSSING_UNRESOLVED` conformément aux limites 14.1 ;
trajectoires incomplètes : barrière classée seulement si le
franchissement précède la première interruption, sinon
`CENSORED`). Matrice exacte : {E0,E1,E2} × {X0,X1,X2} × {S0,S1,S2}
= **27 cellules**, toutes présentées, aucune sélection.
**Réconciliations obligatoires avant toute conclusion** : E0/X0
contre Phase 13-B (421 clôtures : moyenne +0,11, médiane −0,89 bp
en S0) et E0/X1, E0/X2 contre la matrice Phase 14 gelée (B08 :
+1,6110 S0 / −0,3890 S2 ; B09 : +1,9407 / −0,0593, par événement) —
toute divergence arrête la phase pour audit.

## 5. Mesures et présentations gelées

Par politique : déclenchés, non déclenchés, exécutés,
non-exécutions (motifs), délai d'entrée (moyenne/médiane), retard
vs E0, **prix économisé vs E0** = `direction × ln(prix_E0 /
prix_Ek) × 10000` bp (positif = meilleur prix), excursions
post-entrée, durée. Par cellule : effectifs (opportunités,
déclenchements, exécutions, taux de capture), rendements moyens/
médians, part de positifs, quantiles P1/P5/P25/P75/P95/P99, perte
maximale, MFE/MAE, durée, TP/SL/VERTICAL/censures — pondérations
par événement **et** par grappe (moyenne intra-grappe puis
moyenne des grappes, effectifs affichés), et **résultats rapportés
à la cohorte initiale de 443** (non-déclenchés et non-exécutés
comptés 0 dans la moyenne de cohorte, présentés à côté des
statistiques sur exécutés — les deux lectures toujours ensemble).
Comparaison événement par événement E0/E1/E2 dans
`PHASE15_ENTRY_PATHS.csv`. Quartiles Q1–Q4 (construction Phase 14,
`p_M1` seul) : descriptif uniquement, jamais filtre.
**Commission théorique d'équilibre** : pour chaque cellule,
`commission aller-retour maximale compatible avec une moyenne
nulle` = moyenne S0 de la cellule (bp, pondération événement),
rapportée comme borne théorique — jamais comme un tarif réel.
Coûts : spread intégré une fois (Bid/Ask), slippage S0/S1/S2 aux
seuls remplissages (étiquettes Phase 14 exactes : S0
`NET_OF_SPREAD_BEFORE_COMMISSION_WITH_ZERO_ADDITIONAL_SLIPPAGE`,
S1 `…WITH_HYPOTHETICAL_0_5_BP_PER_SIDE`, S2
`…WITH_HYPOTHETICAL_1_0_BP_PER_SIDE`). Pas de courbe de capital,
pas de portefeuille simultané.

## 6. Critères de verdict gelés

- **Anatomie** : `ENTRY_STRUCTURE_IDENTIFIED` si (a) le premier
  extrême tick est du même type pour ≥ 60 % des 421 trajectoires
  complètes, ou (b) le délai médian de stabilisation (premier
  extrême adverse) se concentre dans une seule fenêtre relative
  gelée pour ≥ 50 % des complètes ; `ENTRY_STRUCTURE_NOT_IDENTIFIED`
  si ni (a) ni (b) ; `ENTRY_ANALYSIS_INCONCLUSIVE` si les données
  ne permettent pas de trancher ; `ENTRY_ANALYSIS_BLOCKED` si un
  contrôle critique échoue.
- **Économie (comparaison primaire = X0, entrée isolée)** :
  `EXPLORATORY_ENTRY_ADVANTAGE_FOUND` si E1 ou E2 présente, sur la
  cohorte 443 (moyennes de cohorte, non-déclenchés à 0), une
  moyenne strictement supérieure à E0 sous S0 **et** S1 **et** S2,
  avec une médiane sur exécutés non inférieure à celle d'E0 et un
  taux de capture ≥ 30 % ; `EXPLORATORY_ENTRY_ADVANTAGE_NOT_FOUND`
  si E1 et E2 sont inférieures ou égales à E0 en moyenne de
  cohorte sous les trois scénarios ; sinon
  `ECONOMICALLY_INCONCLUSIVE` ; `NON_MESURABLE` si les conditions
  d'arrêt héritées (non-exécution, spreads) sont franchies ;
  `BLOCKED` si une réconciliation de référence diverge.
  Ces critères sont fixés avant tout calcul Phase 15 ; une
  combinaison favorable resterait une hypothèse exploratoire IS.

## 7. Interdictions (rappel)

Aucun délai ou seuil supplémentaire testé ; pas de variantes à 3–5
clôtures ; aucune nouvelle barrière ; aucune sélection post-hoc ;
pas d'extension de population ; modèle/M0/grappes intouchables ;
holdout interdit ; aucune stratégie, aucun capital, aucune
dépense.
