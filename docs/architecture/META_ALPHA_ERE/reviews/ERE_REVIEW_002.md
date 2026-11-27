# ERE-REVIEW-002 — Dossier de décision : consolidation des corrections architecturales

**Statut : dossier préparé pour décision du fondateur. Aucune correction
n'est appliquée à l'architecture existante par ce document.**
Les documents `FUNCTIONAL_ARCHITECTURE.md`, `DATA_CONTRACTS.md`,
`SYSTEM_INTERFACES.md` et le SVG original du Visuel 1 restent
strictement inchangés. Ce dossier fournit : le détail des sept
corrections d'ERE-REVIEW-001 (§1), la taxonomie fermée des niveaux de
preuve (§2), la distinction formelle des verdicts E et G (§3), le
contrat de fenêtre de ticks de B et la liste exhaustive des entrées de
G (§4), la séparation proposée I-A / I-B (§5), le traitement du Visuel 1
(§6) et la matrice de traçabilité constitutionnelle (§7).

---

## 1. Les sept corrections, une par une

### Correction 1 — Retouche de fidélité du Visuel 1

- **Problème constaté :** cinq écarts entre le diagramme et les
  documents (constats C1–C5 d'ERE-REVIEW-001) : le moteur D est absent ;
  la flèche « ticks » semble alimenter G au lieu de F ; les boucles
  G → C et F → E ne sont pas dessinées ; le garde-fou est dessiné comme
  une dépendance du corpus au lieu d'un cadre contraignant chaque
  transition ; aucune sortie du système n'est visible.
- **Risque si non corrigé :** le fondateur — et tout futur lecteur —
  valide une image fausse du système : connaissance scientifique
  invisible, jugement apparemment nourri directement par les données,
  boucles de recherche et produits finaux absents. Le diagramme est
  l'outil de validation ; son infidélité contamine la décision.
- **Correction proposée :** produire une **proposition distincte**
  (`reviews/VISUEL_1_PROPOSITION_CORRECTION.svg`, §6) ajoutant D,
  redirigeant les ticks vers F (et une fenêtre typée vers B), dessinant
  les deux boucles autorisées, encadrant la chaîne par le garde-fou et
  ajoutant les trois sorties (dossier de modèle, verdict de validation,
  portefeuille). L'original n'est remplacé qu'après validation.
- **Composants concernés :** documentation visuelle uniquement.
- **Conséquences contrats :** aucune (les contrats portent déjà les
  bonnes définitions) ; la proposition doit rester cohérente avec eux.

### Correction 2 — Fermer la liste des entrées de G (constat B1)

- **Problème constaté :** `FUNCTIONAL_ARCHITECTURE.md` attribue à G les
  entrées « A–F », sans liste fermée, alors que le flux principal ne
  transmet formellement que le `SignatureReport` de F.
- **Risque si non corrigé :** le moteur de jugement pourrait s'appuyer
  sur des éléments non mesurés ou non enregistrés (une impression, une
  statistique publique non vérifiée), et personne ne pourrait auditer
  *sur quoi* un verdict repose.
- **Correction proposée :** adopter la liste exhaustive du §4.2 :
  G ne reçoit que des objets nommés et versionnés ; tout le reste est
  du contexte documentaire explicitement non probant.
- **Composants concernés :** G (entrées), socle (registre des objets
  d'un dossier).
- **Conséquences contrats :** `ModelDossier` devra citer l'identifiant
  et le hash de chaque objet reçu ; un verdict référençant un objet
  hors liste est invalide.

### Correction 3 — Contre-seing de G pour le « non démontrable » de E (constat B2)

- **Problème constaté :** E peut émettre « NON DÉMONTRABLE » et
  court-circuiter F et G, sans qu'aucun texte ne dise qui qualifie
  cette conclusion.
- **Risque si non corrigé :** une conclusion — même prudente — naît
  hors du moteur de jugement ; symétriquement, un « non démontrable »
  hâtif pourrait enterrer un dossier sans revue.
- **Correction proposée :** distinguer formellement le **verdict
  expérimental** de E (un avis de testabilité, §3) du **verdict
  économique** de G (seule qualification d'un modèle). L'avis de E ne
  devient un verdict du dossier qu'après contre-seing de G, consigné.
- **Composants concernés :** E (sortie renommée), G (contre-seing),
  journal des décisions.
- **Conséquences contrats :** `ExperimentPlan` gagne un champ
  `avis_testabilite` ; `ModelDossier` gagne un champ
  `contre_seing_non_demontrable` (identifiant de l'avis, motif, date).

### Correction 4 — Contrat de la fenêtre de ticks consommée par B (constat B3)

- **Problème constaté :** B consomme des ticks autour des transactions
  du trader, mais aucun objet ne nomme cette consommation (source,
  durée, champs, statut probant).
- **Risque si non corrigé :** c'est la seule ingestion de marché non
  typée du système ; des fenêtres choisies librement après coup
  permettraient de « voir » le comportement que l'on cherche.
- **Correction proposée :** adopter le contrat `MarketWindow` du §4.1 :
  fenêtre déclarée **avant** extraction, bornes et source figées dans
  l'objet, statut probant limité à la description (jamais à la
  validation).
- **Composants concernés :** B (entrée nouvelle), A (référence aux
  transactions), corpus (extraction).
- **Conséquences contrats :** nouvel objet `MarketWindow` dans
  `DATA_CONTRACTS.md` ; `BehaviorProfile` cite les identifiants des
  fenêtres utilisées pour chaque fait observé.

### Correction 5 — Taxonomie fermée des niveaux de preuve (constat B4)

- **Problème constaté :** les contrats exigent qu'un « niveau de
  preuve » voyage avec chaque objet, sans énumération fermée pour les
  objets intermédiaires.
- **Risque si non corrigé :** c'est le risque central du système (R1
  d'ERE-REVIEW-001) : une interprétation « plausible » peut devenir un
  « fait » en traversant deux modules, sans qu'aucune règle ne soit
  violée — puisqu'aucune règle n'existe encore.
- **Correction proposée :** adopter la taxonomie fermée et les règles
  de transition du §2 (huit niveaux, promotion réservée à des moteurs
  nommés, agrégation au niveau le plus faible).
- **Composants concernés :** tous (champ obligatoire de chaque objet).
- **Conséquences contrats :** chaque objet porte `niveau_preuve` parmi
  les huit valeurs du §2 ; toute transition de niveau est journalisée
  avec le moteur qui l'opère et sa justification.

### Correction 6 — Objet « état de dossier » pour la reprise (constat B5)

- **Problème constaté :** la reprise après interruption repose sur le
  journal seul ; aucun objet ne définit l'état d'avancement d'un
  dossier (étape, objets produits, expériences ouvertes).
- **Risque si non corrigé :** reprise reconstruite à la main, avec
  risque de réutiliser un objet supersédé ou de rouvrir une expérience
  déjà conclue — la pratique actuelle l'évite par discipline, pas par
  structure.
- **Correction proposée :** définir un objet `DossierState` : dossier,
  étape courante, liste des objets produits (identifiant, version,
  hash, niveau de preuve), expériences ouvertes/closes, segments de
  données consommés, prochaine action autorisée.
- **Composants concernés :** socle transversal (registre des dossiers),
  tous les moteurs (lecture/écriture à chaque transition).
- **Conséquences contrats :** nouvel objet `DossierState` ; chaque
  transition de moteur met à jour l'état dans la même écriture
  journalisée que la production de l'objet de sortie.

### Correction 7 — Estimation de coût d'ordre de grandeur dès F (constat B7)

- **Problème constaté :** aucun moteur avant I n'estimant le coût
  d'exécution, un phénomène réel mais inférieur aux coûts ne serait
  découvert que tardivement (précédent réel : marge brute par panier
  ~0,026 contre coût ~0,033, découvert au diagnostic après construction
  de moteurs copiés).
- **Risque si non corrigé :** investir construction et validation sur
  des signatures déjà mangées par le spread ; répéter l'erreur la plus
  coûteuse du programme jusqu'ici.
- **Correction proposée :** charger F d'ajouter à chaque
  `SignatureReport` une **fourchette de coût d'ordre de grandeur**
  (spread typique du segment + scénario de coût déclaré), présentée
  comme un filtre d'élimination, jamais comme une mesure d'edge.
- **Composants concernés :** F (sortie enrichie), G (peut classer
  « phénomène réel mais sous les coûts »), H (ne reçoit pas ces cas).
- **Conséquences contrats :** `SignatureReport` gagne un bloc
  `couts_ordre_de_grandeur` (source du spread, scénario, fourchette) ;
  ce bloc ne peut pas porter un niveau de preuve supérieur à
  SIGNATURE_MESURÉE (§2).

---

## 2. Taxonomie fermée des niveaux de preuve (proposition)

Huit niveaux, et huit seulement. Tout objet du système porte l'un
d'eux ; aucun moteur ne peut en inventer un neuvième.

| Niveau | Nom | Signification | Qui peut l'attribuer | Exemple d'objet |
|---|---|---|---|---|
| N0 | `SOURCE_NON_VERIFIEE` | information reçue, non contrôlée (statistique publique, biographie) | A, à l'ingestion | rendement annoncé de 2 000 % |
| N1 | `FAIT_OBSERVE` | constat directement pointable dans les données reçues ou le corpus | B (transactions), F (comptages) | « 3 achats, 0 vente » |
| N2 | `INFERENCE` | lecture raisonnée d'un fait, réfutable, avec pointeurs | B | « sortie groupée proche du prix moyen » |
| N3 | `HYPOTHESE` | mécanisme économique candidat, concurrent d'au moins un autre | C | récupération d'inventaire |
| N4 | `SIGNATURE_MESUREE` | phénomène quantifié sur un segment déclaré, définitions gelées | F | récupération complète dans 68–94 % des épisodes |
| N5 | `MECANISME_ETAYE` | hypothèse survivant à au moins une expérience discriminante, concurrentes affaiblies mais pas toutes éliminées | **G uniquement** | filtre de volatilité pré-entrée (ME-001.3) |
| N6 | `MECANISME_IDENTIFIE` | concurrentes éliminées par des expériences discriminantes sur données autorisées ; conditions et queue caractérisées | **G uniquement** | (aucun cas à ce jour) |
| N7 | `AVANTAGE_VALIDE` | rendement net après coûts démontré sur données indépendantes du segment de construction, critères pré-déclarés | **I-A uniquement** (§5) | (aucun cas à ce jour) |

**Correspondance avec les qualifications de la Constitution (§9)** :
les verdicts de G s'expriment dans le vocabulaire constitutionnel —
DÉMONTRÉ (≈ N6 avec réplication), FORTEMENT ÉTAYÉ (N5 haut),
COMPATIBLE MAIS NON IDENTIFIÉ (N3–N4 sans discrimination),
NON DÉMONTRABLE (plafond atteint, §3), RÉFUTÉ (hypothèse éliminée,
conservée au registre avec sa preuve). N7 est la seule forme admise
de « VALIDATED » ; il ne peut jamais être attribué sur les données de
construction (Constitution §10).

**Règles de transition (obligatoires) :**

1. **Aucune promotion silencieuse.** Passer d'un niveau au niveau
   supérieur exige une action nommée (expérience, verdict), un moteur
   autorisé (colonne 4) et une entrée de journal citant l'objet source.
2. **Le producteur ne se promeut pas.** F produit du N4, jamais du
   N5 ; B produit du N1/N2, jamais du N3 « confirmé ».
3. **Agrégation au plus faible.** Un objet composite hérite du niveau
   le plus faible de ses ingrédients probants (un dossier mêlant N0
   et N4 reste limité par ce que le N0 peut soutenir : rien).
4. **Le contexte n'est pas une preuve.** Un objet N0 peut motiver un
   dossier ; il ne peut entrer dans la chaîne probante d'un verdict.
5. **Rétrogradation toujours permise, consignée.** Une preuve nouvelle
   peut faire descendre un niveau (précédent : des hypothèses passées
   de candidates à RÉFUTÉES) ; la descente est journalisée comme la
   montée.
6. **Stabilité en transit.** Hors action de promotion/rétrogradation
   journalisée, le niveau d'un objet ne change jamais — c'est
   l'invariant A2 d'ERE-REVIEW-001, rendu testable par cette liste.
7. **Le segment voyage avec le niveau.** Un N4 porte son segment
   (découverte/construction/validation/prospectif) ; un N4 de
   découverte ne peut pas être promu N5 sans mesure sur un segment
   autorisé pour la discrimination visée.

---

## 3. Verdict expérimental (E) contre verdict économique (G)

| Dimension | Verdict expérimental — moteur E | Verdict économique — moteur G |
|---|---|---|
| Question à laquelle il répond | « Peut-on tester ce qui départagerait ces hypothèses, avec les données autorisées ? » | « Que sait-on du mécanisme économique, au vu de toutes les preuves ? » |
| Objet produit | `AvisDeTestabilite` joint à l'`ExperimentPlan` | `ModelDossier` avec qualification constitutionnelle |
| Valeurs possibles | `TESTABLE` (expérience discriminante spécifiée) ; `TESTABLE_SOUS_CONDITION` (donnée manquante nommée) ; `NON_TESTABLE_EN_L_ETAT` (aucune observation autorisée ne discrimine) | DÉMONTRÉ ; FORTEMENT ÉTAYÉ ; COMPATIBLE MAIS NON IDENTIFIÉ ; NON DÉMONTRABLE AVEC LES DONNÉES DISPONIBLES ; RÉFUTÉ |
| Portée | procédurale : autorise ou bloque un calcul | scientifique : qualifie un modèle au registre |
| Qui peut le rendre définitif | E le propose ; **G le contre-signe** quand il vaut conclusion du dossier (Correction 3) | G uniquement |
| Effet | `TESTABLE` → F peut exécuter le plan gelé ; `NON_TESTABLE` contre-signé → dossier clos ou en attente de la donnée nommée | détermine l'accès à la porte de H (N5 minimum requis, N6 visé) |
| Révision | un avis peut être révisé si une donnée nouvelle apparaît (journalisé) | un verdict ne change que sur preuve nouvelle référencée |

Précédents réels qui illustrent la distinction : l'avis de E aurait
été `TESTABLE_SOUS_CONDITION` pour la fourniture de liquidité
(ME-004 : cotations du lieu d'exécution absentes) ; le verdict de G
pour ME-002 est RÉFUTÉ *sous la forme testée* — le verdict économique
qualifie toujours une forme précise, pas une famille entière.

---

## 4. Contrat `MarketWindow` (B) et entrées exhaustives de G

### 4.1 Fenêtre de ticks consommée par B — objet `MarketWindow`

| Champ | Contenu | Règle |
|---|---|---|
| `window_id` | identifiant unique | cité par chaque fait de B qui l'utilise |
| `dossier_id`, `transaction_ref` | dossier et transaction concernée | pointeur vers `TraderDossier` (N1) |
| `source` | corpus et partitions exactes (ex. Dukascopy certifié, partition datée) | source non certifiée interdite |
| `bornes` | début/fin UTC de la fenêtre, déclarés **avant** extraction | toute modification crée une nouvelle fenêtre |
| `justification_bornes` | pourquoi cette durée (ex. couvrir détention + marge) | écrite avant extraction, journalisée |
| `champs` | Bid/Ask/Mid disponibles, pas d'agrégation éventuel | l'absence d'un champ est explicite |
| `qualite` | trous, heures indisponibles, fuseau de la transaction (confiance) | les trous sont déclarés, jamais comblés |
| `segment` | toujours « contexte descriptif » pour B | ne peut servir ni à valider ni à mesurer un edge |
| `niveau_preuve_max` | N2 (les faits tirés restent N1, leurs lectures N2) | aucune promotion possible via B |

### 4.2 Liste exhaustive des entrées recevables par G

G ne peut fonder un verdict **que** sur :

1. `BehaviorProfile` versionné du dossier (N1/N2) ;
2. `HypothesisSet` versionné, avec l'historique des hypothèses
   éliminées et leurs preuves ;
3. `ExperimentPlan`(s) gelés et leurs `AvisDeTestabilite` ;
4. `SignatureReport`(s) correspondants (N4), avec segments et hashes ;
5. `MarketWindow`(s) citées par B (contexte descriptif borné) ;
6. `KnowledgeRef`(s) invoquées (méthodes et limites, jamais des
   résultats) ;
7. l'état du registre des modèles (verdicts antérieurs du même
   phénomène, dépendances connues) ;
8. `DossierState` (objets produits, segments consommés).

**Explicitement non recevables comme preuves :** statistiques
publiques du trader (N0 — contexte de motivation uniquement),
résultats non enregistrés ou sans hash, calculs hors protocole gelé,
données du segment prospectif protégé avant sa règle d'arrêt,
généralités de la littérature sans `KnowledgeRef`. Le `ModelDossier`
cite l'identifiant et le hash de chaque objet reçu ; toute pièce hors
liste rend le verdict invalide.

---

## 5. Séparation proposée : I-A (validation individuelle) et I-B (portefeuille)

| Dimension | **I-A — Validation individuelle** | **I-B — Composition du portefeuille** |
|---|---|---|
| Question | « Ce moteur, seul, produit-il un avantage net réel ? » | « Ces moteurs validés forment-ils un ensemble de risques acceptables et réellement diversifié ? » |
| Entrées | `EngineSpec` gelée ; segment de validation indépendant ; coûts complets du lieu d'exécution | `ValidationVerdict` favorables de I-A ; historiques de rendements des moteurs validés |
| Sorties | `ValidationVerdict` (VALIDATION RÉUSSIE / PARTIELLEMENT FAVORABLE / NON CONCLUANT / RÉFUTÉE / DONNÉES INSUFFISANTES) ; seul émetteur du niveau N7 | `PortfolioAllocation` : budgets de risque par source, limites communes, conditions de révision |
| Critères | pré-déclarés avant ouverture du segment ; espérance nette, PF, drawdown, ES, stabilité par régime, sensibilité aux coûts | corrélations, pertes simultanées, régimes communs, queues partagées, capacité ; deux moteurs du même phénomène = une seule source |
| Interdits propres | retoucher l'`EngineSpec` après résultat ; valider sur la construction | agréger un moteur non validé « pour diversifier » ; compter deux fois la même source économique |
| Boucles | échec → diagnostic via E (jamais réajustage direct) | un verdict I-A révisé à la baisse force la révision de l'allocation |

Aujourd'hui : I-A n'a aucun dossier à traiter et I-B gère un
portefeuille vide. La séparation est proposée **dès la conception**
pour éviter que le moteur qui juge un outil soit demain celui qui
décide de son poids — conflit d'intérêts structurel que le constat B6
avait signalé comme « provisoire » ; cette proposition le rend caduc.

---

## 6. Visuel 1 : original fourni, proposition distincte

- **Original (inchangé, faisant foi) :**
  `docs/architecture/META_ALPHA_ERE/diagrams/VISUEL_1_VUE_GLOBALE.svg`
  — SHA-256 consigné au manifeste et vérifié à la clôture de cette
  mission ; ce dossier n'y touche pas.
- **Proposition (nouveau fichier, sans valeur normative) :**
  `docs/architecture/META_ALPHA_ERE/reviews/VISUEL_1_PROPOSITION_CORRECTION.svg`
  — elle dessine : le module D alimentant C, E, F, G ; les ticks du
  corpus vers F et une `MarketWindow` vers B ; les boucles autorisées
  G → C et F → E ; le garde-fou comme cadre entourant toute la chaîne ;
  la porte de gouvernance entre G et H ; la séparation I-A / I-B du
  §5 ; et les sorties (dossier de modèle, verdict de validation,
  portefeuille). Les boucles interdites y sont mentionnées en note,
  non dessinées comme des flux.

Si le fondateur approuve la proposition, une mission ultérieure la
promouvra à la place de l'original (avec entrée au journal) ; s'il la
rejette, elle restera archivée comme trace de la décision.

---

## 7. Matrice de traçabilité — corrections × Constitution META ALPHA

| Correction | Exigence constitutionnelle servie | Article |
|---|---|---|
| 1. Visuel 1 fidèle | le fondateur valide sur une représentation exacte ; GitHub source de vérité | §11 |
| 2. Entrées de G fermées | distinguer fait observé / inférence / hypothèse / mécanisme ; jamais de modèle « identifié » sans preuves | §9, §10 |
| 3. Contre-seing E par G | ne pas conclure hors du moteur de jugement ; énumérer les modèles compatibles plutôt que trancher sans test | §9 |
| 4. `MarketWindow` typée | données jamais mélangées, provenance et distinctions explicites | §6 |
| 5. Taxonomie des preuves | chaîne FAIT → INFÉRENCE → HYPOTHÈSE → MÉCANISME → AVANTAGE VALIDÉ ; jamais VALIDATED sur la construction | §9, §10 |
| 6. `DossierState` | gouvernance et traçabilité : registre, journal, reprise auditable | §11 |
| 7. Coût dès F | l'edge se juge net après tous les coûts ; un avantage brut inférieur aux coûts n'est pas un edge | §6, §7 |
| §5. Séparation I-A / I-B | portefeuille de sources suffisamment différentes, risques communs étudiés | §8 |
| §3. E ≠ G | ne pas multiplier les campagnes sur un problème non identifiable ; chaque mission réduit une incertitude nommée | §9 |

---

## 8. Décisions demandées au fondateur

1. Approuver, amender ou rejeter **chacune** des Corrections 1 à 7
   (elles sont indépendantes ; un accord partiel est possible).
2. Approuver la taxonomie des niveaux de preuve (§2) et ses sept
   règles de transition, en particulier la promotion N5/N6 réservée
   à G et N7 réservée à I-A.
3. Approuver la distinction verdict expérimental / verdict économique
   et le contre-seing de G (§3).
4. Approuver le contrat `MarketWindow` et la liste exhaustive des
   entrées de G (§4), y compris la liste des pièces non recevables.
5. Approuver la séparation I-A / I-B (§5) dès la conception, ou la
   reporter explicitement.
6. Décider du sort de la proposition Visuel 1 (§6) : promotion,
   amendement ou archivage.

**Aucune de ces propositions n'est appliquée à l'architecture
existante. Aucune implémentation, aucun backtest, aucune modification
de ME-001 n'a eu lieu. La suite — application des corrections
approuvées, puis revue du Visuel 2 — attend la validation explicite
du fondateur.**
