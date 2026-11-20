# META ALPHA — MARKET BEHAVIOR ATLAS : BLUEPRINT DE CARTOGRAPHIE COMPORTEMENTALE XAU/USD

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**Doctrine directrice (rectification stratégique du propriétaire, seq 150) :**

> **LE MARCHÉ DOIT NOUS RÉVÉLER LES ANOMALIES. NOUS NE DEVONS PAS IMPOSER AU MARCHÉ LES STRATÉGIES QUE NOUS AVONS IMAGINÉES.**

**Statut du présent document : blueprint d'architecture, livraison documentaire
uniquement.** Aucun calcul expérimental nouveau n'est autorisé par la demande qui le
crée : aucun backtest, aucune optimisation, aucun `challenge_sim`, aucun accès au
holdout, aucun code de stratégie modifié, aucune nouvelle famille de trading imposée.
La cartographie elle-même (ses calculs descriptifs futurs) exigera un ordre distinct.
Budgets inchangés : tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 ·
P9 10/12 · enveloppe Phase 12 proposée non consommée.

---

## 1. Pourquoi ce blueprint existe — le diagnostic de la dérive

En 148 séquences, le programme a surtout posé une question — « où est l'edge
directionnel ? » — sous forme d'hypothèses isolées (F1–F16), de grilles
(heure × régime × horizon, 30 cellules M6 puis 30 NR), puis de stratégies composites
(S12-01/S12-02, 36 cellules). Ces travaux sont utiles et leurs verdicts tiennent.
Mais ils partagent un biais de conception : **ils partent de comportements imaginés
et demandent au marché de les confirmer.** Les atlas produits jusqu'ici (M1–M6,
seq 116 ; NR, seq 120) étaient des instruments au service d'un crible de stratégies :
on y mesurait ce qu'un crible avait besoin de savoir, pas le comportement du marché
pour lui-même.

La rectification inverse l'ordre : d'abord observer et décrire le comportement
normal, conditionnel au contexte ; ensuite seulement détecter ce qui s'en écarte ;
et ne parler de stratégie qu'au bout d'une chaîne où chaque étape a été franchie
avec ses propres preuves. Les 36 cellules de la Phase 12.3 **ne constituent plus
l'univers de découverte** : S12-01 et S12-02 restent des hypothèses candidates
gelées (seq 149), sans priorité exclusive, et aucune ne démarre sans nouvelle
décision du propriétaire.

## 2. Le pipeline obligatoire A → H (aucune étape sautable)

| Étape | Contenu | Produit | Ce qui est interdit à cette étape |
|---|---|---|---|
| **A. Observation** | Collecte/qualification des flux existants, sans question de recherche | Corpus qualifié, dictionnaire de données | Toute statistique de « performance » |
| **B. Comportement normal** | Distributions de référence **conditionnelles** (régime × session × horizon × structure) | Baselines (§4) | Parler d'« anomalie » |
| **C. Détection d'anomalies** | Écarts mesurés à la baseline, seuils préenregistrés | Catalogue J1 (§6) | Parler de prédiction |
| **D. Mécanisme** | Explication économique : qui paie, pourquoi ça persiste, pourquoi ça n'est pas arbitré | Fiche mécanisme par anomalie | Passer à la stratégie sans payeur identifié |
| **E. Prédictibilité** | L'anomalie informe-t-elle le futur au-delà de la baseline ? (test préenregistré, budget d'essais) | Promotion J1 → J2 ou rejet | Consommer le holdout ; réutiliser l'échantillon de découverte comme confirmation |
| **F. Capturabilité** | Après coûts mesurés (spread, commissions, slippage borné), exécution réelle (Bid/Ask, latence) | Promotion J2 → J3 ou rejet | Mid exécutable ; slippage supposé nul ou « mesuré » sans fills |
| **G. Conception de stratégie** | Une stratégie **adaptée à l'anomalie** (déclencheur, stop, cible, sizing issus du mécanisme) | Hypothèse préenregistrée | Imposer une famille préexistante à l'anomalie |
| **H. Validation & challenge** | Gates du programme (n ≥ 200 grappes, R3/MDE, BY, IC95 deux ancres, 3/3, ECR ≥ 2), puis simulation séquentielle du challenge sur μ mesurée | Certification ou cimetière | Ticket sans μ > 0 net démontré (règle permanente) |

Conséquence directe : une anomalie peut légitimement mourir à chaque étape, et la
plupart mourront — c'est le fonctionnement normal du pipeline, pas un échec du
programme. Le cimetière actuel (F1–F16, M6, NR, B1) se relit d'ailleurs ainsi : ce
sont des hypothèses entrées en E sans être passées par B–D.

## 3. Architecture de la cartographie

### 3.1 Dimensions comportementales (périmètre minimal imposé, non fermé)

Chaque dimension est une *famille d'observation* : on y décrit le comportement, on
n'y teste rien. Toute dimension ajoutée ultérieurement doit être préenregistrée
avant son exploration (§7).

1. **Sessions** : comportement propre à l'Asie, Londres, New York (activité,
   amplitude, spread, persistance), sur les blocs UTC conventionnés (seq 144/146,
   correspondance locale/DST documentée seq 146 §4).
2. **Ouvertures et transitions de session** : premières minutes d'open (à ce jour
   **NON MESURÉES** à résolution utile, seq 146), chevauchements Londres–New York,
   fins de session, rollover.
3. **Extrêmes de session et de journée** : formation des plus hauts/plus bas
   (heure d'occurrence, ordre d'établissement haut vs bas, distance parcourue avant
   l'extrême).
4. **Dépassements et réintégrations** : profondeur du dépassement d'un niveau de
   référence, temps de réintégration, taux de réintégration vs poursuite —
   **en description** (fréquences conditionnelles), sans déclencheur de trade.
5. **Fausses cassures et continuations après cassure** : devenir descriptif des
   clôtures au-delà d'un niveau (part de poursuite, de retest, de réintégration),
   par horizon.
6. **Compression et expansion de volatilité** : épisodes de range étroit, durée,
   mode de sortie (direction de l'expansion décrite, pas prédite), lien au niveau
   de volatilité prévue F3.
7. **Impulsions, retracements, retournements** : anatomie des mouvements rapides
   (amplitude, durée, part retracée à horizons successifs).
8. **Persistance directionnelle** : autocorrélation conditionnelle décrite par
   horizon/régime (déjà partiellement mesurée : atlas, seq 30–33, 116 — à intégrer
   comme baseline, pas comme signal).
9. **Consolidations** : fréquence, durée, amplitude des plages sans tendance, par
   session et régime.
10. **Mouvements extrêmes et changements de régime** : queues de distribution,
    épisodes de saut (F7 en description), transitions entre régimes de volatilité.
11. **Comportement autour des niveaux précédents** : réactions descriptives aux
    extrêmes de la veille, de la semaine, aux seuils ronds (distance d'approche,
    taux de toucher/rejet) — langage imposé : niveaux de référence, jamais
    « liquidité observée » sans order book.
12. **Réactions post-événements économiques** : hors fenêtres d'exécution
    interdites [T−5, T+5] ; comportement du prix et du spread de T+5 à T+240
    décrit (la part directionnelle est déjà réfutée par F15, seq 113 — la
    cartographie décrit la *forme* de la réaction : temps de normalisation de la
    volatilité, pas un signal).
13. **Interactions F3 × F7 × sessions × coûts S2** : comment le risque de saut et
    la volatilité prévue se distribuent par session ; comment le spread S2 varie
    avec ces régimes (coût du contexte, pas coût d'une stratégie).

### 3.2 Variables observables (dictionnaire minimal, à geler avant calcul)

Par événement/épisode et par fenêtre : variation de prix (bp), amplitude
(haut−bas, bp), excursions favorable/défavorable (bp, définies sans position —
excursion maximale dans chaque sens depuis l'origine de la fenêtre), part retracée,
temps de formation (minutes jusqu'à l'extrême), durée de consolidation, profondeur
de dépassement (bp au-delà du niveau), temps de réintégration, spread coté
(médiane/P90/P95 par fenêtre), nombre de ticks, écarts inter-ticks, régime F3 du
jour (décile de vol prédite), décile d'alerte F7 de l'heure, session, distance au
niveau de référence le plus proche. Chaque variable porte : définition mathématique,
source (S3 tick/bougies, F3 gelé, F7 gelé, S2), résolution, et règle de traitement
des données manquantes (jamais d'imputation).

## 4. Construction des baselines (le « normal » avant l'« anormal »)

Pour chaque famille du §3.1 et chaque variable du §3.2 :

- **Conditionnement** : régime de volatilité (terciles/déciles F3 du jour), session,
  horizon, et structure pertinente (p. ex. distance au niveau). Une baseline non
  conditionnée est interdite : elle fabriquerait des « anomalies » qui ne sont que
  des changements de contexte.
- **Statistiques de référence** : médiane, quantiles 5/25/75/95, taux de base des
  événements décrits (p. ex. part des dépassements réintégrés sous 60 min), durées
  médianes — toujours avec n et couverture.
- **Stabilité de la baseline** : calculée par ères (2010–13, 2014–16, 2017–20 sur
  l'ancien corpus ; 2020+ sur le NR lorsque la résolution le permet) ; une baseline
  instable entre ères est signalée comme telle — l'« anomalie » mesurée contre elle
  hérite de cette fragilité (niveau de preuve plafonné, §6).
- **Règle d'or écrite** : une valeur extrême n'est pas une anomalie exploitable ;
  c'est d'abord une queue de la distribution de référence. L'anomalie commence à
  l'écart *systématique et conditionnel*, pas à l'événement spectaculaire.

Méthode de calcul autorisée à ce stade (sous ordre futur) : descriptif intégral sur
l'IS de développement, mention « DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE
PERFORMANCE » sur chaque tableau, dans la lignée de la dérogation cadrée seq 145.

## 5. Règles de détection des anomalies

1. **Seuils préenregistrés avant exploration** : pour chaque famille, l'écart
   constitutif d'une candidate (p. ex. fréquence conditionnelle s'écartant de la
   baseline d'au moins x points avec intervalle de confiance excluant la baseline)
   est écrit avant le calcul. Aucun seuil ajusté après avoir vu les distributions.
2. **N minimal d'occurrences** : une candidate exige un nombre d'épisodes
   indépendants (grappes jour×contexte, jamais des fenêtres chevauchantes comptées
   plusieurs fois) fixé au préreg — plancher proposé : 200 grappes, cohérent avec
   les gates du programme.
3. **Multiplicité interne à la cartographie** : le nombre de familles × variables ×
   conditionnements explorés est compté et publié avec l'atlas ; les candidates
   sont hiérarchisées par un critère déclaré (taille d'écart × n), et la sélection
   pour l'étape D est plafonnée à l'avance (proposé : au plus 10 fiches J1 par
   campagne) pour interdire le ratissage.
4. **Réplication interne minimale** : une candidate doit apparaître dans au moins
   deux ères disjointes de l'IS avec le même signe d'écart, faute de quoi elle est
   classée « épisode d'ère », non anomalie.
5. Toute candidate reçoit immédiatement son identifiant (§6) et sa fiche ; les
   explorations négatives (familles sans écart) sont publiées avec le même soin —
   une cartographie qui ne montre que ses anomalies est un biais de sélection.

## 6. Catalogue des anomalies — fiches et classification J1/J2/J3

Identifiants : `ANO-###` séquentiels, jamais réutilisés. Chaque fiche contient les
treize champs imposés par l'ordre : contexte d'apparition ; comportement normal de
référence (baseline chiffrée) ; écart statistique observé ; fréquence ; amplitude ;
durée ; régimes d'apparition ; stabilité historique (par ère) ; explication
économique éventuelle (ou « aucun mécanisme articulé à ce jour ») ; conséquence
statistique observable attendue si le mécanisme est vrai ; coût potentiel
d'exploitation (ancres et spreads mesurés du contexte) ; limites des données ;
niveau de preuve.

| Classe | Signification | Conditions de promotion (cumulatives) |
|---|---|---|
| **J1 — Anomalie descriptive** | Écart conditionnel mesuré à la baseline, répliqué sur ≥ 2 ères | Préreg de la famille + seuils §5 + n minimal + réplication |
| **J2 — Anomalie prédictive** | J1 **et** information mesurable sur les mouvements futurs | Mécanisme D articulé (payeur identifié) + test préenregistré sur budget d'essais distinct, échantillon de confirmation disjoint de la découverte, gates R3/n/BY de la famille |
| **J3 — Anomalie exploitable** | J2 **et** asymétrie démontrée après coûts et contraintes d'exécution | Capturabilité F : Bid/Ask réels, coûts mesurés du contexte, slippage borné par scénarios, IC95 net > 0 aux deux ancres, ECR ≥ 2, stabilité 3/3 |

Aucune promotion sur la foi d'un mouvement spectaculaire : l'amplitude d'un épisode
n'entre dans aucun critère. Une fiche peut être déclassée (J2 → J1 si la
confirmation échoue) ; elle ne peut jamais sauter une classe.

## 7. Contrôles anti-data-mining (le garde-fou central)

1. **Dimensions préenregistrées** : la liste des familles explorées par campagne est
   chaînée (seq) avant tout calcul descriptif de la campagne ; toute famille ajoutée
   en cours de campagne ouvre une campagne nouvelle.
2. **Budgets séparés** : le travail descriptif (B–C) consomme **0 essai** et est
   compté en « campagne descriptive » ; les essais ne commencent qu'en E, sur un
   budget neuf créé par ordre, avec sa correction de multiplicité propre (BY sur la
   famille des anomalies testées, jamais sur les 36 cellules de Phase 12 sauf si le
   propriétaire les y inclut explicitement).
3. **Dépendances documentées** : fenêtres chevauchantes interdites dans les comptes ;
   unité d'indépendance = grappe jour×contexte ; deux anomalies issues du même
   épisode sont fichées comme liées.
4. **Comparaisons multiples corrigées dès la détection** : le nombre total de
   comparaisons descriptives est publié ; les écarts retenus doivent survivre à
   une correction déclarée (BY sur les comparaisons de la campagne, ou seuil
   renforcé équivalent écrit au préreg).
5. **Découverte ≠ confirmation** : toute anomalie J1 est découverte sur l'IS de
   développement ; sa confirmation (E) utilise un échantillon disjoint (réserve
   temporelle interne ou walk-forward, seq 148) ; le holdout scellé n'est **jamais**
   ouvert pendant la cartographie, ni pour « vérifier vite ».
6. **Journal négatif** : chaque campagne publie ses familles sans écart et ses
   fiches rejetées, pour que le taux de base de la découverte soit auditable.

## 8. Ressources historiques existantes (ce que la cartographie peut utiliser dès son ouverture)

| Ressource | Contenu utile à la cartographie | Seq |
|---|---|---|
| Corpus tick ancien 282/282 | Barres 1 min/ticks IS 2010–2020, spreads, sauts | 53–59, 118 |
| Série horaire certifiée (60 025 h) | Volatilité, spread, activité par heure ; profil saisonnier mesuré | 40–42, 146 |
| S3 Dukascopy NR + S2 Swissquote | Régime 2020+ : bougies/ticks, spread ~1,35–2,2 bp | 119–120 |
| F3 HAR-RV gelé (L2) | Régime de volatilité du lendemain, conditionnement des baselines | 64, 82 |
| F7 sauts gelé (L2) | Décile d'alerte horaire (classement, pas probabilité calibrée) | 77, 83 |
| Atlas M1–M6 + NR | Calendriers, coûts par fenêtre×régime, anatomie d'événements M2 : **à reclasser comme baselines partielles existantes**, pas comme cribles | 116, 120 |
| P11-A1 | Forme des fenêtres news (spread, densité), minute 0 | 142 |
| Mesures B2/B3, GD07, DIST_REGIME, POST_EVENT, SPREAD_EPISODES | Anatomies descriptives existantes à verser au fonds de baselines | 22–45, 123 |
| Calendrier macro PIT | Conditionnement « jour d'annonce » hors fenêtres interdites | 105 |
| COVERAGE_MATRIX v2 | Ce qui est déjà R/P/I/J — la cartographie ne redécouvre pas ce qui est réfuté | 138 |

Limites des ressources : opens de session non mesurés à résolution tick (à inclure
comme dimension A/B si le propriétaire l'autorise) ; tick futures et order book
inaccessibles (classe I, seq 138) ; backfill S3 horaire 2021–2023 incomplet
(throttling) ; pas de données d'exécution (fills) — la capturabilité restera bornée
par scénarios tant qu'aucun journal réel n'existe.

## 9. Budget documentaire et expérimental proposé (soumis, non consommé)

- **Campagne descriptive (B–C)** : 0 essai ; proposé : 1 campagne chaînée couvrant
  les 13 familles du §3.1, livrables = baselines + catalogue J1 (≤ 10 fiches) +
  journal négatif. Ressources : calculs CI sur corpus existants uniquement.
- **Étape D (mécanismes)** : documentaire, 0 essai ; au plus les 10 fiches J1.
- **Étapes E–F** : budget d'essais **à créer par ordre explicite**, taille fonction
  du nombre de fiches promues en D (proposé : plafond 24 essais, BY sur la famille
  des anomalies effectivement testées) ; les 36 cellules Phase 12.3 restent un
  budget séparé, non autorisé, non consommé, et ne fusionnent avec celui-ci que sur
  décision propriétaire écrite.
- **Holdout** : usage unique éventuel, autorisation distincte, jamais pendant la
  cartographie.

## 10. Passage d'une anomalie à une stratégie (méthode G)

Quand une anomalie atteint J3, et seulement alors : la stratégie se **déduit** de
la fiche — le déclencheur est le contexte d'apparition documenté, le stop se place
là où le mécanisme dit que l'anomalie meurt (invalidation), la cible sur l'ampleur
conditionnelle mesurée de l'écart, le sizing sur F3 (service) et les budgets de
protection du challenge (3 %/7 %, paramètres proposés non garantis), l'exécution sur
les coûts mesurés du contexte de l'anomalie. La stratégie est alors une hypothèse
neuve préenregistrée (pipeline H), testée sur budget propre. À titre d'illustration
de la méthode — et non comme priorité : si la cartographie découvrait par exemple
que les dépassements asiatiques se réintègrent anormalement souvent dans un régime
précis, S12-01 deviendrait la traduction de *cette* anomalie-là, avec ses paramètres
issus des mesures ; sans cette découverte, S12-01 reste une candidate gelée parmi
d'autres, au même titre que S12-02.

## 11. Relation avec l'existant

- **Phase 12.3** : gel des 36 hypothèses et audit de faisabilité sans performance
  (comptage des configurations en cours en CI au moment du présent blueprint —
  aucun résultat de ce comptage n'a été consulté pour l'écrire). Les 36 cellules
  restent gelées, non testées, non prioritaires.
- **Cimetière** : inchangé et contraignant ; la cartographie décrit le marché, elle
  ne ressuscite aucune hypothèse réfutée — une « redécouverte » qui recouvrirait
  une cellule R du cimetière est rejetée à la fiche (collision documentée).
- **Actifs certifiés** : F3/F7 restent des services de conditionnement (étapes B et
  F/G) ; le carry BTC/ETH reste dormant hors exploitation (décision propriétaire
  séparée, seq 131) ; C-2 reste dormant.
- **Sécurité** : workflow FRED toujours suspendu (seq 145) ; rotation de la clé
  toujours pendante côté propriétaire ; purge d'historique avec mapping des SHA =
  opération distincte soumise à contrôle.

## 12. Décisions réservées au propriétaire

1. Acter la doctrine « cartographie avant conception » comme principe directeur
   (le présent blueprint la formalise, seq 150) ?
2. Autoriser la première campagne descriptive (familles §3.1, préreg chaîné,
   0 essai) — et avec quel périmètre exact (ancien corpus seul, ou + NR horaire
   partiel) ?
3. Valider les seuils de détection proposés (§5 : 200 grappes, réplication 2 ères,
   plafond 10 fiches J1/campagne) ?
4. Trancher le sort de l'inventaire de faisabilité Phase 12.3 en cours (le mener à
   terme comme document de puissance, ou l'arrêter au profit de la cartographie) ?
5. Confirmer que les 36 cellules restent gelées sans priorité jusqu'à une décision
   ultérieure éclairée par le catalogue J1 ?

**Validation du propriétaire obligatoire avant toute expérience. Le marché doit
nous révéler les anomalies ; nous ne devons pas imposer au marché les stratégies
que nous avons imaginées.**

*Fin du blueprint. Aucun calcul n'a été exécuté pour le produire.*
