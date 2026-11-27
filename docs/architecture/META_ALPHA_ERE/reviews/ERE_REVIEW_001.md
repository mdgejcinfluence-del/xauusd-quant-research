# ERE-REVIEW-001 — Revue fonctionnelle du Visuel 1 et de l'architecture fonctionnelle

**Statut : revue de conception, présentée au fondateur pour validation.**
**Périmètre strict :** `diagrams/VISUEL_1_VUE_GLOBALE.svg`,
`FUNCTIONAL_ARCHITECTURE.md`, et — uniquement pour vérifier les
interfaces — `DATA_CONTRACTS.md` et `SYSTEM_INTERFACES.md`.
**Aucune modification de l'architecture n'a été faite dans cette revue.**
Toute correction proposée est listée en section 8 et attend la décision
du fondateur. Aucune implémentation, aucun moteur, aucun backtest.

---

## 1. Le Visuel 1 tel qu'il est (présentation avant audit)

Le diagramme montre META ALPHA comme une chaîne en trois rangées,
lue de gauche à droite puis en retour :

- **Rangée du haut (bleu — comprendre le trader) :** les ENTRÉES
  (3 à 6 transactions, biographie, statistiques publiques) entrent dans
  **A. Ingestion**, qui produit un dossier normalisé où chaque
  information est marquée présente, absente ou incertaine. Le dossier
  passe à **B. Comportement**, qui sépare les faits observables des
  interprétations. Puis **C. Hypothèses** formule plusieurs modèles
  économiques concurrents capables d'expliquer ces comportements.
- **Rangée du milieu (vert — confronter au marché) :** **E. Expériences**
  choisit le test le plus informatif et gèle son protocole ;
  **F. Découverte** cherche les signatures correspondantes dans le
  corpus certifié (685 millions de ticks) ; **G. Identification**
  assemble les preuves et rend un verdict qualifié dans un dossier de
  modèle.
- **Rangée du bas (orange — exploiter, prudemment) :** seulement si le
  verdict le permet, **H. Moteurs propres** conçoit nos propres règles
  (la mention « porte de gouvernance » est écrite dans le diagramme),
  puis **I. Validation** mesure l'avantage net après coûts et, à terme,
  compose un portefeuille de sources différentes.
- **À gauche (rouge — les fondations qui ne négocient pas) :** le
  **CORPUS** (Dukascopy certifié 2010-2026, plus le segment prospectif
  postérieur au gel) et le **GARDE-FOU** (Constitution, Drift Guard,
  registre chaîné SHA-256).
- Une note en bas du diagramme annonce la boucle de recherche :
  « verdicts → nouvelles hypothèses (jamais de réajustage) ».

Lecture en une phrase : **on reçoit peu d'informations sur un trader,
on les transforme en questions économiques, on répond à ces questions
avec le marché — pas avec le trader — et on ne construit un outil
d'exploitation qu'après un verdict, avec nos propres règles.**

Le diagramme est fidèle à l'esprit de l'architecture. L'audit
(section 4) relève cependant des écarts précis entre ce que le
diagramme dessine et ce que les documents définissent ; ils sont
consignés, pas corrigés.

---

## 2. Ce qui circule entre les moteurs, liaison par liaison

| # | Liaison | Objet transmis | Pourquoi cette liaison existe | Ce qui ne doit pas passer |
|---|---|---|---|---|
| 1 | Entrées → A | transactions brutes, biographie, statistiques publiques, contexte plateforme | sans normalisation, aucun calcul ultérieur n'est comparable | une information reconstruite « de mémoire » |
| 2 | A → B | `TraderDossier` : transactions normalisées (UTC, unités documentées), inventaire présent/absent/incertain/contradictoire, performances marquées NON VÉRIFIÉES | B doit reconstruire des comportements, pas réinterpréter des formats | les statistiques affichées comme des faits |
| 3 | Marché → B | ticks autour des transactions du dossier | un comportement (renforcement, sortie) ne se voit que contre le prix du moment | des ticks hors fenêtre sans justification |
| 4 | B → C | `BehaviorProfile` : faits observés (avec pointeurs vers les transactions) séparés des interprétations | C explique des comportements ; il ne doit pas expliquer des bruits de formatage | un mécanisme déguisé en « fait » |
| 5 | D → C, E, F, G | `KnowledgeRef` : méthodes et connaissances sourcées, avec leurs limites | chaque moteur emprunte des méthodes justifiées au lieu de les improviser | une méthode choisie par popularité |
| 6 | C → E | `HypothesisSet` : au moins deux hypothèses concurrentes, chacune avec ses prédictions divergentes et l'expérience qui les départagerait | E ne peut choisir un test que si les hypothèses prédisent des choses différentes | une hypothèse unique présentée comme « la » réponse |
| 7 | E → F | `ExperimentPlan` : protocole gelé (définitions, grilles fixées à l'avance, segment de données autorisé, critères de succès/échec pré-déclarés), enregistré et hashé avant tout calcul | F exécute ; il ne choisit ni les seuils ni le terrain après avoir vu les résultats | un plan modifiable en cours d'exécution |
| 8 | Corpus → F | ticks du seul segment autorisé par le plan (découverte, construction, validation ou prospectif) | la valeur d'un résultat dépend du segment qui l'a produit | un mélange de segments, ou un segment prospectif ouvert avant sa règle d'arrêt |
| 9 | F → G | `SignatureReport` : mesures par segment, définitions exactes, parts censurées, intervalles, fichiers et leurs empreintes SHA-256 | G juge sur des mesures traçables, pas sur des impressions | une conclusion (« ça marche ») à la place des mesures |
| 10 | F → E (boucle) | signal qu'une signature reste ambiguë | E peut alors concevoir l'expérience discriminante suivante | une relance automatique sans nouveau préenregistrement |
| 11 | G → C (boucle) | verdict qui rouvre une question (nouvelle hypothèse) | la recherche avance par élimination ; un verdict peut faire naître une hypothèse nouvelle | la modification d'une hypothèse déjà gelée dans une expérience en cours |
| 12 | G → H (porte) | `ModelDossier` au niveau de preuve suffisant, queue de risque caractérisée | on ne construit un outil que sur un mécanisme suffisamment établi | un dossier « compatible » ou une ressemblance avec le trader |
| 13 | H → I | `EngineSpec` : nos règles propres, paramètres gelés et hashés, budget de risque | I évalue un objet figé ; sinon il évaluerait une cible mouvante | un réglage retouché après avoir vu un résultat |
| 14 | I → E (boucle) | échec de validation demandant un diagnostic | comprendre un échec est légitime (précédent réel : diagnostic LMD-008 après le backtest négatif de 2026) | un réajustage déguisé en « diagnostic » |
| 15 | I → portefeuille | `ValidationVerdict` favorable + analyse d'indépendance économique | deux outils gagnants sur le même phénomène restent un seul risque | l'addition de sources corrélées présentée comme de la diversification |
| 16 | Socle → tous | enregistrement chaîné de chaque transition (qui, quoi, quand, empreinte) | sans journal, aucune reprise ni aucun audit n'est possible | un résultat sans protocole retrouvable |

---

## 3. Responsabilités, dépendances et points de contrôle

**Responsabilité unique de chaque moteur** (vérifié : aucune n'en
chevauche une autre) : A structure, B décrit, C propose, D documente,
E décide du test, F mesure, G juge, H construit, I valide et agrège.
La frontière la plus importante est triple : **décrire n'est pas
expliquer** (B≠C), **expliquer n'est pas prouver** (C≠G),
**prouver un phénomène n'est pas prouver un profit** (G≠I).

**Dépendances :** la chaîne est séquentielle par dossier, mais le
système ne l'est pas : D alimente quatre moteurs en continu ; le
corpus alimente B (fenêtres courtes) et F (recherche massive) ; le
socle écrit à chaque transition. Un dossier peut donc être repris à
n'importe quelle étape sans refaire les précédentes, à condition que
les objets intermédiaires soient conservés — c'est le rôle du journal.

**Points de contrôle scientifique (là où le système peut dire non) :**

1. **À l'entrée (A) :** un dossier trop pauvre est accepté, mais ses
   absences deviennent des limites explicites de tout l'aval.
2. **Au préenregistrement (E) :** aucun calcul avant protocole gelé,
   critères et segment déclarés.
3. **Au verdict (G) :** cinq issues possibles, dont COMPATIBLE MAIS
   NON IDENTIFIÉ et NON DÉMONTRABLE — le système a le droit de ne pas
   conclure.
4. **À la porte de H :** aucun modèle ne la franchit sans niveau de
   preuve suffisant ; aujourd'hui, **aucun** ne la franchit.
5. **À la validation (I) :** critères déclarés avant l'ouverture du
   segment de validation ; un positif obtenu sur les données de
   construction n'est jamais une validation.
6. **Au portefeuille (I) :** l'indépendance économique prime sur la
   performance individuelle.

**Séparation identification / exploitation :** elle est structurelle,
pas déclarative. Tout ce qui est à gauche de la porte (A–G) parle du
trader et du marché ; tout ce qui est à droite (H–I) parle de nous.
L'échec historique de nos moteurs copiés sur le comportement observé
(−30,40 et −33,24 en backtest, avant identification du mécanisme) est
la justification documentée de cette frontière.

---

## 4. Audit fonctionnel — constats numérotés

Échelle : **OK** (correctement défini), **AMBIGUÏTÉ** (deux lectures
possibles), **MANQUE** (interface insuffisamment spécifiée),
**ÉCART VISUEL** (le diagramme ne dessine pas ce que le texte définit).

### Ce qui est correctement défini

- **A1 — OK.** Unicité des responsabilités : aucun couple de moteurs ne
  revendique la même décision. En particulier, F mesure et G juge :
  le moteur qui produit un chiffre n'est pas celui qui rend le verdict.
- **A2 — OK.** Conservation des niveaux de preuve : les contrats
  imposent que le niveau voyage avec l'objet et qu'aucun objet ne
  change de niveau en transit ; le verdict n'appartient qu'à G.
- **A3 — OK.** Informations manquantes : un champ absent est explicite
  (`ABSENT`), les statistiques publiques sont typées NON VÉRIFIÉES, et
  le réel, l'affiché, le simulé et le contrefactuel sont des types
  distincts non mélangeables dans un même total.
- **A4 — OK.** Hypothèses concurrentes : minimum deux, chacune devant
  prédire au moins une observation que les autres ne prédisent pas ;
  les hypothèses réfutées restent au registre et bornent les suivantes.
- **A5 — OK.** Séparation historique / validation : la segmentation
  découverte-construction-validation-prospectif est un invariant des
  contrats, avec interdiction d'ouvrir le prospectif avant sa règle
  d'arrêt.
- **A6 — OK.** Traçabilité et reprise : chaque transition est
  enregistrée dans le registre chaîné ; les précédents réels
  (protocoles gelés depuis seq149) montrent que la reprise après
  interruption fonctionne.
- **A7 — OK.** Porte de H : condition d'entrée écrite, état actuel
  consigné (aucun modèle ne la franchit), activation réservée au
  fondateur.

### Ambiguïtés et manques (à trancher, non corrigés ici)

- **B1 — AMBIGUÏTÉ (G).** `FUNCTIONAL_ARCHITECTURE.md` donne à G les
  entrées « A–F », alors que le flux principal ne lui transmet que le
  `SignatureReport` de F. Lecture bénigne : G consulte tout l'historique
  du dossier. Mais « assembler les preuves » sans liste fermée
  d'entrées autorisées laisse une porte ouverte à l'usage d'éléments
  non mesurés. **Il faut décider** si G reçoit une liste fermée
  d'objets ou un accès documentaire complet au dossier.
- **B2 — MANQUE (E).** Le module E peut produire un verdict
  « NON DÉMONTRABLE » qui court-circuite F et G. Qui qualifie ce
  verdict, et avec quelle revue ? Le texte ne dit pas si G doit le
  contresigner. Sans cela, une conclusion (même prudente) peut naître
  hors du moteur de jugement.
- **B3 — MANQUE (B↔corpus).** B consomme des ticks autour des
  transactions, mais aucun contrat ne nomme cet objet (fenêtre ?
  durée ? source ?). C'est la seule consommation de marché non
  typée de l'architecture.
- **B4 — AMBIGUÏTÉ (niveaux de preuve).** Les contrats parlent de
  « niveau de preuve » sans énumération fermée partagée par tous les
  objets : la constitution en définit cinq pour les verdicts, mais les
  niveaux des objets intermédiaires (par exemple une interprétation de
  B « plausible ») ne sont pas normalisés. C'est le point le plus
  important à préciser avant toute implémentation des schémas.
- **B5 — MANQUE (reprise formelle).** La reprise repose sur le journal,
  mais aucun objet ne définit l'« état d'un dossier » (étape atteinte,
  objets produits, expériences ouvertes). La pratique l'a toujours
  reconstruit à la main ; l'architecture devrait le nommer.
- **B6 — AMBIGUÏTÉ (I, double rôle).** I valide les moteurs **et**
  compose le portefeuille. Si demain plusieurs moteurs existent, le
  même moteur jugerait et allouerait. Une séparation ultérieure est
  envisageable ; à ce stade (portefeuille vide), le regroupement est
  défendable mais doit être assumé comme provisoire.
- **B7 — MANQUE (coûts avant H).** Les contrats imposent des coûts
  détaillés, mais aucun moteur avant I n'est chargé d'estimer le
  spread réel du lieu d'exécution visé. Précédent réel : la marge
  brute par panier (~0,026) inférieure au coût par panier (~0,033)
  n'a été découverte qu'au diagnostic, après construction. Une
  estimation de coût « d'ordre de grandeur » dès F éviterait de
  construire sur un phénomène déjà mangé par les coûts.

### Écarts entre le Visuel 1 et les documents

- **C1 — ÉCART VISUEL (module D absent).** Le moteur D (bibliothèque
  scientifique) n'apparaît pas dans le diagramme, alors qu'il alimente
  C, E, F et G. Le Visuel 2 le couvre, mais le Visuel 1 se présente
  comme la vue globale : un lecteur pressé conclura que le système
  fonctionne sans connaissances externes.
- **C2 — ÉCART VISUEL (flèche corpus).** La flèche étiquetée « ticks »
  part du CORPUS vers la rangée du milieu au niveau de G, alors que
  les ticks alimentent F (et B). Telle que dessinée, elle peut se lire
  « le corpus nourrit le jugement », ce qui contredit A1.
- **C3 — ÉCART VISUEL (boucle non dessinée).** La boucle
  « verdicts → nouvelles hypothèses » existe comme note textuelle,
  sans flèche G → C ni F → E. Les boucles autorisées et interdites
  (pourtant centrales dans `SYSTEM_INTERFACES.md`) sont invisibles.
- **C4 — ÉCART VISUEL (garde-fou).** Le GARDE-FOU est dessiné sous le
  CORPUS avec une flèche verticale montant vers lui, ce qui suggère
  une dépendance du corpus au garde-fou ; en réalité le garde-fou
  contraint **chaque** transition.
- **C5 — ÉCART VISUEL (sorties).** Le diagramme ne montre aucune
  sortie : ni le dossier de modèle, ni le verdict de validation, ni
  le portefeuille. Le fondateur ne voit pas ce que le système produit
  au bout de la chaîne.

Ces cinq écarts sont des défauts de **représentation**, pas de
conception : les documents portent les bonnes définitions. Ils
justifient néanmoins une retouche du Visuel 1 — si le fondateur
l'approuve (section 8), car la mission interdit de corriger
silencieusement.

### Risques de conception résiduels

- **R1.** Le niveau de preuve (B4) est le mécanisme qui empêche une
  hypothèse de devenir un « fait » en traversant les modules ; tant
  qu'il n'est pas une énumération fermée et testable, c'est le maillon
  le plus fragile de l'architecture.
- **R2.** L'orchestration repose sur un agent supervisé : les
  contrôles sont des documents et un journal, pas encore des
  vérifications automatiques (étape ultérieure, hors périmètre).
- **R3.** Dépendance à un corpus principal unique (Dukascopy via
  Drive) : déjà documentée, sans solution engagée.
- **R4.** Le jugement d'hypothèse (C) et de verdict (G) reste humain/
  agent : assumé dans la conception, à ne pas « automatiser » par
  génération de texte.

---

## 5. Test conceptuel obligatoire — dossier entièrement fictif

> **Dossier « EXEMPLE-ALPHA » — 100 % fictif, inventé pour cette
> revue.** Quatre transactions XAUUSD fictives, une biographie fictive
> (« robot de retour à la moyenne, grille légère »), un rendement
> **annoncé** de 2 000 % et un drawdown **annoncé** de 10 %. Rien de
> tout cela n'est un fait réel ; les chiffres ci-dessous illustrent le
> fonctionnement du système et ne décrivent aucun marché.

Transactions fictives supposées reçues : deux achats rapprochés, un
troisième achat plus tard après un recul de prix, une clôture unique
des trois positions. Aucun prix ni aucune date réels.

**Passage dans les neuf moteurs :**

1. **A** normalise : 4 transactions, 1 instrument, 0 vente ; biographie
   présente mais succincte ; rendement et drawdown enregistrés comme
   **annoncés, non vérifiés** ; informations absentes déclarées :
   capital, effet de levier, commissions, historique complet, fuseau
   horaire confirmé incertain. Le 2 000 % n'entre dans aucun calcul.
2. **B** décrit des faits : achats groupés, un renforcement après
   recul, une sortie commune. Interprétations (étiquetées comme
   telles) : « accumulation pendant l'adversité », « sortie sur
   retour vers le prix moyen ». B ne dit pas pourquoi.
3. **C** génère trois hypothèses concurrentes : (i) récupération
   d'inventaire après chute depuis un plus haut ; (ii) grille de
   retour à la moyenne autour d'un prix d'ancrage ; (iii) simple
   martingale sans ancrage économique. Chacune prédit quelque chose
   que les autres ne prédisent pas : (i) exige un plus haut antérieur
   récent comme cible, (ii) prédit des renforcements aussi après des
   hausses symétriques, (iii) ne prédit aucune cible de sortie.
4. **D** fournit les méthodes : temps de premier retour, distributions
   conditionnelles, analyse de queue, avertissements sur la censure
   des trajectoires inachevées.
5. **E** choisit l'expérience la plus discriminante : mesurer, sur un
   segment de découverte déclaré, si les renforcements suivent des
   reculs depuis un plus haut (i) ou tout écart symétrique (ii) ;
   protocole gelé avant calcul. E note que (iii) ne pourra être
   écartée que par les trajectoires de sortie.
6. **F** exécute sur le segment autorisé et produit des mesures —
   par hypothèse fictive de cette revue : les écarts se résorbent
   souvent, mais une minorité s'aggrave fortement.
7. **G** assemble : (ii) est affaiblie si aucun renforcement après
   hausse n'est observable dans les données du marché autour de
   signatures comparables ; (i) reste compatible ; (iii) reste
   compatible aussi, faute d'observation discriminante disponible.
   **Verdict rendu : COMPATIBLE MAIS NON IDENTIFIÉ**, avec
   l'observation minimale qui départagerait (i) et (iii). Le système
   ne déclare ni modèle identifié, ni rentabilité : le 2 000 %
   annoncé n'a servi à rien d'autre qu'à motiver le dossier.
8. **H** ne reçoit rien : la porte reste fermée.
9. **I** ne reçoit rien : rien à valider, portefeuille toujours vide.

**Ce que ce test démontre :** le système travaille avec quatre
transactions sans en exiger davantage ; il conserve plusieurs
hypothèses vivantes ; il sait terminer sur une non-conclusion
motivée, qui est ici la réponse scientifiquement correcte.

---

## 6. Ce qui attend le fondateur

### Corrections proposées (aucune appliquée)

1. **Visuel 1** : ajouter le module D, rediriger la flèche « ticks »
   vers F (et une fenêtre vers B), dessiner les boucles autorisées
   G → C et F → E, représenter le garde-fou comme un cadre entourant
   la chaîne, ajouter les sorties (dossier de modèle, verdict,
   portefeuille). Justification : écarts C1–C5 — le diagramme doit
   montrer ce que les documents définissent déjà.
2. **B1** : fermer la liste des entrées de G (objets nommés, pas
   « A–F »).
3. **B2** : faire contresigner par G tout verdict NON DÉMONTRABLE
   émis par E.
4. **B3** : nommer le contrat de « fenêtre de marché autour d'une
   transaction » consommée par B.
5. **B4** : définir l'énumération fermée des niveaux de preuve pour
   tous les objets, pas seulement pour les verdicts.
6. **B5** : définir un objet « état de dossier » pour la reprise.
7. **B7** : charger F d'une estimation de coût d'ordre de grandeur
   avant toute éventuelle construction en H.

### Décisions demandées

- Approuver ou amender ces sept corrections (le Visuel 1 retouché ne
  sera produit qu'après accord).
- Confirmer que le double rôle de I (validation + portefeuille) est
  accepté comme provisoire (B6), ou demander sa séparation dès la
  conception.
- Valider ensuite l'architecture fonctionnelle comme base, avant
  toute revue du Visuel 2 et, plus tard, toute implémentation.

---

## 7. Conclusion de la revue

L'architecture fonctionnelle est cohérente dans ses responsabilités,
ses contrats et ses points de contrôle ; ses faiblesses sont
localisées (niveaux de preuve à fermer, deux interfaces à nommer, un
contre-seing à ajouter) et son diagramme global mérite une retouche
de fidélité. Rien de tout cela ne touche aux principes : décrire
avant d'expliquer, expliquer avant de prouver, prouver avant de
construire — et le droit, à chaque étape, de répondre « pas encore
démontrable ».

**Cette revue attend explicitement la validation du fondateur.
Aucune poursuite vers le Visuel 2 ni aucune implémentation n'aura
lieu sans elle.**
