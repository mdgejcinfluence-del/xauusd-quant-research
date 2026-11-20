# PHASE 12 — BLUEPRINT SYSTÈME MULTI-CONDITION XAU/USD (V3)

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**Statut : formalisation documentaire uniquement (ordre Phase 12 V3, seq 143).**
0 essai · 0 budget consommé · aucun backtest · aucune optimisation · `challenge_sim`
non exécuté · holdouts non ouverts · budgets figés (tick 148/150, panel 28/60,
exo 6/60, P7 0/24, NR 0/24, P9 10/12). Instrument exclusif : XAU/USD.
**PHASE 12 BLUEPRINT LIVRÉ — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**

---

## A. Synthèse des acquis de P11-A1 — cinq leçons chiffrées (seq 140, 142)

1. **Spreads** : médiane de minute 2,28–2,68 bp avant annonce → 2,62–3,82 bp en minute 0
   → **2,37–2,91 bp dès T+1**, stables jusqu'à T+30 ; **0 minute en médiane** à spread
   > 2× le pré-annonce de l'événement sur T0→T+30 ; pointes tick > 20 bp confinées à la
   minute 0 (P90 des maxima FOMC/NFP).
2. **Cotations denses** : 258–329 ticks/minute à T0 (contre ~95–160 avant), intervalle
   inter-tick médian 0,10–0,14 s, trou maximal médian 2–3,6 s sur T0→T+5, couverture
   36/36 minutes sur 326/346 événements (94,2 %).
3. **Déplacement concentré en minute 0** : amplitudes médianes du premier mouvement
   11,4/12,3/6,8 bp (FOMC/NFP/CPI, M2 seq 116) — **aucun scénario du présent blueprint
   n'est conçu pour capter la minute 0** ; elle est exclue par design (§5).
4. **Ancres cohérentes avec le mesuré** : C1_NR 1,35 bp et C1_BG 4,7 bp encadrent les
   spreads réellement observés (médianes 2,3–2,9 bp en régime news normalisé, ancres
   incluant commissions) → la doctrine « prudemment haut » reste intacte (§3 Couche 2).
5. **Opens de session : NON MESURÉS.** P11-A1 a mesuré les fenêtres d'annonces, pas les
   ouvertures de session. Aucune mesure du programme ne caractérise le spread des
   premières minutes d'open → règle conservatrice : **aucune entrée pendant les
   15 premières minutes suivant l'ouverture d'une session autorisée** (paramètre
   proposé non calibré, durée fixée ici et justifiée par l'absence totale de mesure :
   en l'absence de données, la prudence se fixe a priori, elle ne s'optimise pas).

## B. Cartographie des briques réellement utilisables

| Brique | Ce qu'elle est (et n'est pas) | Statut |
|---|---|---|
| S3 Dukascopy (horaires, bougies 1 min/ticks, spreads) | Structure de prix et calendrier mesurés du corpus NR (seq 118–121) ; les **niveaux** (extrêmes de session/veille) sont des constructions déterministes sur ces prix, pas des signaux validés | Donnée qualifiée ; niveaux = définitions à préenregistrer |
| S2 Swissquote (spread snapshot + enregistreur cron) | Mesure de coût du régime NR (~1,35 bp, seq 119) ; flux d'observation, pas un flux d'exécution du compte cible | Mesure de coût |
| F3 HAR-RV | Prédit la **volatilité du lendemain** (jamais la direction) | Certifié L2 service (seq 64, 82) |
| F7 anticipation de sauts | Prédit la **probabilité de saut de l'heure suivante** (jamais un biais) | Certifié L2 service (seq 77, 83) |
| CUSUM (châssis durci) | Surveillance de stabilité d'une série de résultats ; protection, pas signal | Livré/testé (seq 107, 114) |
| `challenge_sim` + `meta_portfolio.py` | Moteurs de simulation/ingénierie prêts ; **non exécutés dans la présente mission** | Livrés (seq 84, 119) |
| Calendrier macro PIT (`available_at_utc`) | Horodatage réel des FOMC/NFP/CPI, DST date par date | Certifié ingénierie (seq 105) |

## C. Matrice de traçabilité

| Composant | Définition technique (source) | Seq | Statut de validation |
|---|---|---|---|
| F3 HAR-RV | `RV(t+24h) ~ b0 + bd·moy(RV 24h) + bw·moy(5j) + bm·moy(22j)`, OLS roulant 500 j, origine journalière (`F3_PREREG.json`) ; QLIKE 0,0191 vs 0,0266, R² MZ 0,200 | 61–64, 82 | **Validé L2** (walk-forward 5/5 blocs) — service uniquement |
| F7 sauts | Logistique L2 sur vol/spread/activité causaux + heure sin/cos ; cible \|ret heure suivante\| > q90 causal ; AUC OOF 0,684, lift 2,85× à 5 % d'alerte (`F7_PREREG.json`) | 75–77, 83 | **Validé L2** (forward annuel 0,684/0,696/0,687) — service uniquement |
| Spread S2 NR | Snapshot Swissquote 50,4 ¢ @ 3 725 $ ≈ 1,35 bp ; enregistreur cron 14h10/22h10 UTC | 119 | Mesure ponctuelle + accumulation en cours |
| Spread S3 intraday | Médiane ≈ 2,2 bp sur S3 horaire 2020 (3 768 h) | 119–120 | Mesure descriptive |
| Ancres C1_NR / C1_BG | 1,35 bp RT mesurée NR ; 4,7 bp RT config challenge (`OWNER_CONFIG_V2.json`) | 108, 119 | Ancres de certification (doctrine deux ancres) |
| Niveaux de session | Extrêmes (plus haut/plus bas) calculés sur bougies S3 — **aucune définition de session n'est préenregistrée dans le programme à ce jour** | — (construction neuve) | **Hypothèse neuve** : convention §D.0 à geler au préreg |
| `challenge_sim` | Monte-Carlo règles 2-Step, arrêt au passage/échec, paramètres `CHALLENGE_CONFIG` | 84, 132–134 (conception) | Moteur livré ; valeurs Phase 10 = simulation à μ imposée, pas une validation |
| CUSUM | Somme cumulée des écarts standardisés, seuil de suspension (§E) | 107 | Composant de châssis testé synthétique |
| Calendrier news | FOMC 198 réunions + NFP/CPI PIT, `available_at_utc` | 105, 125 | Certifié ingénierie |

**Cimetière (rappel contraignant, seq de réfutation)** : F1 (70–72), F2 (73), F4 (65),
F5 (76), F6 (67–68), F9 (80–81, P), F10/F11 (90–91), F13 (94–97, P), F14 (107, P),
F15 (113), F16 (111, P), cellules M6 (116) et NR (120), B1 (128), paniers/grilles sans
stop (Phase 10 E2, seq 133). Aucune de ces hypothèses n'est réutilisée comme signal ;
les tables de non-collision du §D le démontrent scénario par scénario.

## D. Spécification des scénarios

### D.0 Conventions gelées pour tout le blueprint (à reprendre telles quelles au préreg)

- **Journée de référence** : journée calendaire UTC [00:00, 24:00). Justification :
  seule convention sans ambiguïté DST dans nos corpus (timestamps UTC natifs) ; le
  reset courtier 17 h ET du challenge est une règle de *risque* (§F), pas une borne
  de niveaux. Une seule convention, non modifiable après coup.
- **Sessions (paramètres proposés non calibrés — aucune borne de session n'existe dans
  le programme)** : Asie [00:00, 08:00) UTC ; Londres [08:00, 13:00) UTC ; New York
  [13:00, 21:00) UTC. Fenêtres d'entrée autorisées : Londres et New York uniquement,
  hors leurs 15 premières minutes (§A.5) et hors exclusion news (§5 de l'ordre = §F.1
  ci-dessous). Sans order book, on parle de **niveaux de référence / proxies de
  liquidité**, jamais de « liquidité observée ».
- **Niveaux de référence** : plus haut/bas de la session asiatique du jour ; plus
  haut/bas de la veille (journée UTC) ; extrêmes des sessions Londres/NY de la veille.
- **Exclusion news stricte** (arbitrage V3) : intervalle bloqué
  **[T−5 min, T+5 min] bornes incluses** pour FOMC/NFP/CPI horodatés `available_at_utc` :
  aucune nouvelle position, ordres en attente annulés, **positions existantes liquidées
  au plus tard à T−5** (non négociable : une pointe > 20 bp en minute 0, mesurée
  seq 142, traverse un stop et peut tuer le mur journalier de 4 %). Première entrée
  après la fenêtre seulement si le filtre S2 est satisfait. Stops et sorties d'urgence
  jamais désactivés.
- **Coûts à l'entrée (arbitrage V3)** : le filtre temps réel utilise le **spread mesuré
  au moment de la décision** ; la certification future exigera les trois scénarios :
  C1_NR (1,35 bp RT), C1_BG (4,7 bp RT), distribution mesurée S2 stressée (×1,5 —
  facteur de stress proposé non calibré). Slippage : inconnue bornée étiquetée
  « hypothèse de stress » (scénarios 0 / +0,6 / +1,5 bp par côté — paramètres proposés
  non calibrés), jamais un chiffre « simulé » présenté comme mesuré.

### D.1 Gabarit commun — Couches 2 à 4

**Couche 2 (à chaque entrée, les trois contrôles).**
- **F3 / énergie** : `Q_t = Mouvement_prévu_F3(t,h) / Coût_total_estimé_S2(t,h)`, où
  `Mouvement_prévu_F3(t,h) = sqrt(RV_prévue_F3(t)) × sqrt(h / 24)` (RV journalière
  prévue par le HAR gelé, convertie sur l'horizon h en heures — conversion de la
  définition validée de F3, qui prédit la variance du lendemain) et
  `Coût_total_estimé_S2(t,h) = spread_observé(t) + commissions_RT + slippage_stress`.
  Entrée interdite si `Q_t < Q_min`. **Q_min = 4 (paramètre proposé non calibré, à
  fixer au préreg, jamais optimisé sur les résultats)** : le mouvement prévu doit
  couvrir au moins 4× le coût total estimé. F3 prédit la volatilité, jamais la
  direction.
- **F7 / risque de saut** : entrée interdite si la probabilité F7 de saut sur l'heure
  d'entrée dépasse le seuil d'alerte documenté du modèle gelé (top 5 % des probabilités
  = zone d'alerte de la validation seq 77 ; seuil opérationnel **proposé non calibré** :
  interdiction dans le décile supérieur F7) ou si un saut incompatible avec le stop
  retenu est probable (Distance_SL inférieure au saut q90 causal cible de F7). F7 ne
  fournit aucun biais directionnel.
- **S2 / coût réel** : entrée interdite si `spread_observé(t) > spread_max`, avec
  `spread_max = 4,0 bp` (paramètre proposé non calibré, cohérent avec le P95 mesuré des
  minutes post-news normalisées, seq 142) ; et interdite dans tous les cas si la cible
  structurelle ne couvre pas ≥ 2R **net** des coûts du scénario médian.

**Couche 3 (mécanique, par trade).** Formules (variables : Bid/Ask/Mid cotés à
l'instant de décision ; Entrée = Ask si long, Bid si court — jamais le Mid) :
`Spread_bp = 10 000 × (Ask − Bid) / Mid` ;
`Distance_SL_bp = 10 000 × |Entrée − Stop| / Entrée` ;
`Distance_TP_bp = 10 000 × |Cible − Entrée| / Entrée`.
Exigences : Stop Loss dur posé dès l'entrée, jamais supprimé ni déplacé dans le mauvais
sens ; invalidation structurelle = la condition qui annule le scénario (définie par
scénario) ; cible structurelle définie avant l'entrée ; horizon maximal de détention ;
sortie de sécurité à l'horizon ou à l'invalidation ; ratio brut
`Distance_TP / Distance_SL ≥ 2` **et** ratio net (après coût aller-retour du scénario)
≥ 2 ; la zone 30–80 bp est une zone de mouvement *recherchée*, non une cible
obligatoire — si aucune cible structurelle n'atteint le 2R net, le trade est ignoré.
**Interdictions définitives** : grille, martingale, moyennage à la baisse,
augmentation de risque pour récupérer une perte, stop supprimé/dégradé.

**Couche 4 (survie, conception).** `Risque_monétaire = Equity × Risque_par_transaction` ;
`Taille_position = Risque_monétaire / Risque_monétaire_par_lot`, le risque par lot
intégrant le contrat exact de la plateforme ciblée (inconnue déclarée : spec serveur
MT5 toujours absente, seq 55 — sizing définitif conditionnel), la distance du stop,
les coûts et le slippage de stress. Contrôles : perte journalière restante recalculée
avant chaque entrée (budget = 3,0 % paramètre proposé, mur 4 %) ; risque cumulé des
positions ouvertes plafonné au budget journalier restant ; surveillance du drawdown
total (plafond de conception 7 %, référence 8 %, §F) ; blocage automatique des entrées
budget épuisé. **CUSUM** : statistique `S_k = max(0, S_{k−1} + (−PnL_k/σ_PnL − 0,5))`
sur les PnL nets par trade (σ estimé sur l'IS de développement uniquement) ; suspension
des entrées si `S_k > 4` (paramètres proposés non calibrés) ; reprise uniquement après
revue documentée et 20 trades d'observation sans nouveau dépassement — surveillance et
protection, jamais un indicateur directionnel.

### D.2 S12-01 « SESSION LIQUIDITY SWEEP » (hypothèse neuve)

- **Mécanisme économique articulé** : un dépassement d'un niveau de référence très
  suivi (extrême asiatique/veille) déclenche les stops et les ordres d'exécution
  forcée au-delà du niveau ; si le prix est rejeté (réintégration confirmée), les
  exécutions forcées s'épuisent et le prix retourne vers le niveau structurel opposé.
  Payeur identifié : les positions stoppées et les suiveurs de cassure tardifs.
  **Ancrages** : niveaux S3 (construction neuve, §C) ; comportement des extrêmes et
  post-mouvements caractérisé descriptif (seq 30–45) ; **aucune brique directionnelle
  validée n'est invoquée** — l'hypothèse composite est neuve.
- **Définition (long, court symétrique)** : niveau L = plus bas asiatique du jour
  (variante : plus bas de la veille). Balayage : un tick/bougie 1 min clôture sous L.
  Confirmation : la bougie 1 min suivante clôture entièrement au-dessus de L
  (réintégration). Entrée : première cotation exécutable après la clôture de
  confirmation (Ask, jamais Mid, jamais une clôture indisponible à l'entrée).
  Stop : sous l'extrême du balayage − buffer. Cible : niveau structurel opposé
  (plus haut asiatique ou milieu de range de la veille — cible gelée au préreg),
  seulement si ≥ 2R net. Horizon maximal : fin de la session d'entrée.
- **Paramètres (grille pré-déclarée, ≤ 3 valeurs chacun)** : niveau ∈ {bas Asie, bas
  veille} (2) ; buffer stop ∈ {2, 5, 10} bp (3) ; Q_min ∈ {4} fixe ; spread_max ∈ {4,0}
  fixe ; seuil F7 ∈ {décile sup.} fixe. **Cellules = 2 × 3 = 6 par direction, 12 au
  total** (long/court comptés séparément, correction BY sur 12).
- **Non-collision** :

| Piste réfutée la plus proche | Différence structurelle précise | Verdict |
|---|---|---|
| F6 réversion horaire (R, seq 68) | F6 trade le retour horaire inconditionnel/conditionné sans niveau, sans confirmation de réintégration, à horizon horaire fixe ; S12-01 exige niveau + balayage + clôture de réintégration + cible structurelle ≥2R net + 3 filtres | Pas de recouvrement de définition ; hypothèse neuve (la proximité « retournement » est thématique, pas cellulaire) |
| F13-A/B gap week-end (P, seq 94–95) | Événement = gap d'ouverture hebdomadaire, jamais testé faute de n ; S12-01 = niveau intraday de session, autre événement, autre horizon | Aucune cellule commune |
| F15 retournement post-news (R, seq 113) | F15 entre ≥ T+5 min après annonce sur le premier mouvement ; S12-01 est interdit en fenêtre news (§F.1) et conditionné à un niveau de session | Aucune cellule commune (exclusion mutuelle temporelle) |

- **Arrêt propre au scénario** : voir §G (gates généraux) ; meurt si, au n prévu,
  l'IC95 % net aux deux ancres inclut 0 ou si le signe n'est pas 3/3.

### D.3 S12-02 « STRUCTURAL BREAKOUT RETEST » (hypothèse neuve)

- **Mécanisme économique articulé** : une clôture complète au-delà d'un niveau de
  référence engage les suiveurs et les rachats de stops ; le retest du niveau cassé
  trie les cassures réelles (le niveau tient comme support/résistance retourné) des
  fausses (réintégration immédiate = scénario S12-01, mutuellement exclusif). Payeur
  identifié : les entrées tardives sur retest et les stops du camp adverse.
  **Ancrages** : niveaux S3 (neufs) ; cassures/réintégrations = structures de prix
  définies au préreg ; aucune brique directionnelle validée invoquée.
- **Définition (long, court symétrique)** : niveau L identifié avant la cassure.
  Cassure : clôture 1 min complète au-delà de L + buffer de cassure. Retest : retour du
  prix à L ± tolérance sans clôture de réintégration complète. Confirmation : bougie
  1 min de rejet dans le sens de la cassure (clôture au-delà de L dans le sens initial).
  Entrée : première cotation exécutable après confirmation. Stop : derrière la
  structure de retest (extrême du retest − buffer). Cible : prochain niveau structurel
  ≥ 2R net ; extensions 30–80 bp uniquement si compatibles avec le mouvement prévu F3,
  la structure et le risque initial. Horizon maximal : fin de session + session
  suivante (paramètre proposé non calibré : détention ≤ 2 sessions).
- **Paramètres** : niveau ∈ {haut/bas Asie, haut/bas veille} (2 cellules directionnelles
  par niveau, comptées en 4) ; buffer de cassure ∈ {2, 5} bp (2) ; buffer stop ∈ {2, 5,
  10} bp (3) ; Q_min et spread_max fixes comme D.1. **Cellules = 4 × 2 × 3 = 24,
  correction BY sur 24.**
- **Non-collision** :

| Piste réfutée la plus proche | Différence structurelle précise | Verdict |
|---|---|---|
| F15 dérive post-news (R, seq 113) et B1 continuation (R, seq 128) | Continuations d'un premier mouvement d'annonce, entrées calendaires ; S12-02 exige cassure + retest + confirmation structurels, hors fenêtre news | Aucune cellule commune |
| F10/F11 momentum panel (R, seq 90–91) | Momentum journalier multi-actifs/temps, sans niveau ni retest ; horizons jours-semaines | Aucune cellule commune |
| F9 TSMOM or (P, seq 80–81) | Jamais testé (MDE) ; signal = tendance journalière, pas d'événement structurel intraday | Aucune cellule commune |
| M6 atlas (R, seq 116) | Le crible mesurait des autocorrélations fenêtre×régime×horizon sans niveaux ni confirmations ; aucune cellule M6 ne contient un déclencheur de retest | Aucune cellule commune |

- **Arrêt propre** : idem §G ; meurt en outre si la fréquence réalisée sort de la bande
  de viabilité 3–10 trades/sem sans qu'aucun paramètre pré-déclaré ne la ramène (la
  fréquence est un critère de viabilité, jamais un objectif forçant des trades).

### D.4 S12-03 « POST-NEWS STRUCTURAL RESPONSE » — examen d'admission (double condition)

1. **Mécanisme structurel documenté (séquences 1 à 136)** : les séquences fournissent
   une mécanique de **volatilité** post-news documentée (M2 : pas de retombée de
   l'amplitude sous le niveau de 15 min avant 240 min, seq 116 ; anatomie
   post-mouvements seq 37–39) mais **aucun mécanisme directionnel** de continuation ou
   de retracement post-news documenté : les deux seules mesures directionnelles
   post-annonce du programme sont des réfutations (F15 dérive et retournement, 0/6,
   seq 113) et la pré-annonce est réfutée (B1, seq 128). Le mécanisme directionnel
   exigé est donc **indocumenté** dans les séquences 1 à 136.
2. **Non-collision F15** : toute entrée post-news ≥ T+5 min dont le déclencheur dérive
   du premier mouvement recouvre les variantes F15 (dérive/retournement, sorties
   15/60/240, seq 113). Un déclencheur purement structurel (niveau préexistant cassé
   après T+5) réduirait le recouvrement sans l'annuler : la fenêtre, les familles
   d'événements et les ancres seraient identiques, et la différence reposerait sur le
   seul conditionnement — exactement le type de variante que le cimetière interdit de
   retester sans mécanisme nouveau. Collision **non résoluble** en l'état.

**Décision écrite : S12-03 écarté — mécanisme indocumenté (condition 1 non remplie),
collision F15 non résoluble (condition 2 non remplie).** P11-A1 (seq 142) a normalisé
le *spread* après T+1 ; conformément à l'ordre, cela ne démontre pas qu'un mouvement
directionnel persiste après T+5, et ne rouvre pas la cellule. S12-03 pourra être
reconsidéré uniquement si un mécanisme structurel directionnel **nouveau et documenté
hors des séquences réfutées** est apporté au propriétaire — pas par ce blueprint.

### D.5 Comptage global et correction (proposition §H)

S12-01 : 12 cellules · S12-02 : 24 cellules · S12-03 : 0 (écarté). **Total 36 cellules**,
correction **BY(36)** au niveau de la phase future, avant tout scénario de coût (les
trois scénarios de coût sont des conditions de certification appliquées à chaque
cellule retenue, pas des cellules multiplicatives — convention proposée, à valider).

## E. Règles d'entrée, de sortie, de coûts et de dimensionnement (synthèse normative)

Entrée : conditions D.2/D.3 + Couche 2 complète + hors exclusions (news, opens,
F7) + budget de risque Couche 4 disponible. Sortie : cible structurelle, stop dur,
invalidation, horizon maximal, liquidation pré-news T−5, sortie d'urgence toujours
armée. Coûts : filtre temps réel au spread mesuré ; certification aux trois scénarios
(C1_NR, C1_BG, S2 stressée) ; slippage en hypothèse de stress étiquetée.
Dimensionnement : formules Couche 4 ; grille de risque par transaction proposée
{0,25 % ; 0,50 %} de l'equity (paramètres proposés non calibrés, ≤ 2 valeurs) ;
aucune augmentation après perte ; risque cumulé plafonné au budget journalier restant.

## F. Gestion des risques et conformité Prop Firm 2-Step

### F.1 Calendrier économique — voir §D.0 (exclusion [T−5, T+5], liquidation T−5).

### F.2 Contrat mathématique du challenge (modèle générique, à formaliser avant tout test)

| Paramètre | Valeur (ordre V3) | Précision obligatoire |
|---|---|---|
| Objectif P1 | **+8 % et +10 % examinés séparément** | Deux configurations distinctes, jamais mélangées |
| Objectif P2 | +5 % | Base réinitialisée à l'entrée en P2 |
| Perte journalière maximale | 4 % | **Modèle générique déclaré** : perte calculée sur l'equity, positions ouvertes incluses (flottant compté), référence = equity de début de journée ; réinitialisation 17:00 America/New_York (DST date par date) — à confronter au règlement exact de la firme avant tout usage réel |
| Drawdown total | Référence 8 % ; sensibilité 10 % | **Modèle générique déclaré** : trailing sur le plus haut equity atteint, verrouillage éventuel = variante à déclarer ; conception plafonnée à 7 % (paramètre proposé) |
| Ratio net | ≥ 2:1 (3:1 recherché si la structure le permet) | Après coûts du scénario de certification |
| Fréquence | 3–10 trades/sem (viabilité, jamais objectif) | Comptée par scénario |
| Jours minimum / durée / consistance / détention news | **NON SPÉCIFIÉS par un règlement de firme à ce jour** | Sans prop firm identifiée et son règlement exact, tout résultat futur relève du **modèle générique de challenge 2-Step** ci-dessus — jamais d'une garantie de conformité à un fournisseur particulier |

Conditions courtier/prop firm inconnues (rappel permanent) : contrat exact, tick
size/value, volume min/pas, slippage typique, règles de détention week-end/news propres
à la firme — **aucune n'est estimée** (seq 55). Probabilité de réussite évaluée
**séquentiellement** P(P1 puis P2) par simulation du passage effectif de phase, jamais
comme produit de probabilités marginales indépendantes.

## G. Métriques de réussite et d'échec (protocole futur proposé — aucun test ici)

- **Hypothèses primaires** : 2 (S12-01, S12-02). Cellules : 36 (BY(36)).
- **Espérance nette** d'une variante = moyenne des PnL nets par trade (Bid/Ask,
  commissions, scénario de coût), en bp et en R.
- **Gates de certification (inchangés)** : préreg chaîné avant calcul ; n ≥ 200 trades
  par variante ; R3/MDE pré-calculée au n prévu (rejet au gate = 0 essai) ; BY(36) ;
  IC95 % net > 0 à **C1_NR et C1_BG** (et survie au scénario S2 stressé) ; signe stable
  3/3 sous-périodes ; ECR ≥ 2.
- **Critère d'arrêt challenge** : si la probabilité de passage simulée (μ = espérance
  **mesurée** de la variante certifiée, jamais imposée favorablement) ne dépasse pas
  celle de la politique de référence Phase 10 à μ ≤ 0 (seq 133–134 : P1×P2 ≈ 0,197 à
  μ = −2 bp), le scénario est déclaré loterie documentée et entre au cimetière.
- **Ce qui tue un scénario** : échec à un gate, ou fréquence hors bande de viabilité,
  ou drawdown de conception > 7 % en simulation à μ mesurée. **Ce qui tue la phase** :
  mort des deux scénarios → entrée au cimetière documentée, jamais retestée, retour à
  l'état clos.
- **Validation** : walk-forward chronologique ; développement sur IS uniquement ;
  **holdout à usage unique**, ouvert uniquement sur autorisation distincte du
  propriétaire ; aucun retest après ouverture.

## H. Budget expérimental futur proposé (plafond soumis, non consommé)

Arithmétique exacte de la proposition : cellules retenues après gates
(≤ 36) × 3 scénarios de coût (certification, non multiplicatifs pour BY mais comptés
en runs) × 3 sous-périodes de robustesse + simulation séquentielle challenge
(2 configurations P1 × 2 DD × 2 risques = 8 runs par variante certifiée) + marge 20 %.
Plafond proposé au propriétaire : **36 essais statistiques maximum** (un par cellule,
BY(36)), les runs de coût/simulation étant des évaluations de certification chaînées
aux cellules, pas des essais supplémentaires — convention à valider explicitement.
Réserve holdout : 1 usage, jamais consommé sans ordre distinct. **Aucun de ces nombres
n'est consommé par le présent blueprint.**

## I. Risques méthodologiques et inconnues non résolues (déclarées)

1. Les deux scénarios reposent sur des **mécanismes articulés mais jamais mesurés** sur
   nos corpus : ni le sweep ni le retest n'ont de mesure descriptive préalable dans le
   programme (les niveaux eux-mêmes sont des constructions neuves). Le risque de
   « narration structurelle » est le risque principal de la phase.
2. Seuils Q_min, spread_max, décile F7, buffers, 15 min d'open, marges 3 %/7 %, CUSUM :
   **paramètres proposés non calibrés** — leur fixation au préreg les gèle, elle ne les
   valide pas.
3. Slippage réel : structurellement inconnu (aucun fill dans le programme) ; les
   scénarios de stress bornent, ils ne mesurent pas.
4. Sessions : bornes UTC proposées, non issues d'une mesure du programme ; un flux
   courtier en heure serveur peut décaler les extrêmes effectifs.
5. F3 est journalier : sa conversion intraday `sqrt(h/24)` suppose une diffusion
   homogène que les calendriers mesurés (M1, seq 116) contredisent partiellement —
   biais déclaré, à traiter au préreg (pondération par le calendrier horaire mesuré
   serait une variante à déclarer, pas un ajustement libre).
6. Différence flux corpus (Dukascopy/Swissquote) vs flux d'exécution d'une prop firm
   donnée : inconnue, non mesurable à ce stade.
7. Fréquence réelle des configurations : inconnue avant extraction descriptive
   éventuelle — la bande 3–10/sem peut rendre un scénario non viable sans aucun test.

## J. Décisions nécessitant la validation du propriétaire

1. Admettre S12-01 et S12-02 comme hypothèses neuves préenregistrables (et acter
   l'écartement de S12-03) ?
2. Valider les conventions gelées §D.0 (journée UTC, sessions, exclusion news avec
   liquidation T−5) et les paramètres proposés non calibrés (Q_min = 4, spread_max
   = 4,0 bp, seuils F7, buffers, marges 3 %/7 %) ?
3. Valider la convention de comptage (36 cellules, BY(36), coûts = certification non
   multiplicative) et le plafond de 36 essais proposé ?
4. Identifier (ou non) une prop firm et son règlement exact pour sortir du modèle
   générique — et fournir la spec serveur MT5 toujours absente (sizing définitif) ?
5. Autoriser, le cas échéant, un préenregistrement + micro-budget Phase 12 réelle —
   ou clore le programme sur ce blueprint ?
6. **Rotation de la clé FRED** (toujours pendante, seq 105/140) : à effectuer avant
   tout usage FRED futur ; noter que la purge ultérieure de l'historique Git réécrira
   les SHA et exigera un mapping ancien→nouveau des 142+ checkpoints.

*Fin du blueprint. Aucune stratégie n'est présentée comme gagnante. Aucun essai n'est
créé dans la chaîne expérimentale par le présent document.*
