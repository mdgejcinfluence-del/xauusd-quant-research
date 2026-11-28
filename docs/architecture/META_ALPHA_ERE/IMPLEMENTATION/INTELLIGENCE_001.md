# ERE-INTELLIGENCE-001 — Inférence sous incertitude et découverte indépendante

## A/B. Architecture et méthodes retenues (justification)

Nouveau module `ere/uncertainty.py` (23/23 tests au total) :
**identification partielle** (bornes de Manski à travers les scénarios
admissibles — jamais de point inventé), **conclusions conditionnelles**
(chaque énoncé étiqueté par son scénario, plafond N2 tant que
l'incertitude n'est pas levée), **analyse de sensibilité** (invariant
sous tous les scénarios vs fragile selon le scénario), classification
de fiabilité des dossiers (`UTILISABLE`, `UTILISABLE_AVEC_RESERVES`,
`INSUFFISANT_POUR_IDENTIFICATION`) et **priorisation des expériences**
par hypothèses départagées par unité de coût, bloquée à zéro sans
segment autorisé. Méthodes écartées pour l'instant, avec motif : le
bayésien complet (aucun modèle génératif calibré — nos contrats
l'interdisent déjà), les modèles hiérarchiques (n=3 épisodes), le GPU
et toute bibliothèque nouvelle (aucun bénéfice mesuré).

## D. TRADER-CANDIDATE-002 enrichie (scénarios, jamais de déduction)

Mouvements du Mid pendant les détentions selon le fuseau supposé
(ticks Dukascopy 2026-11-27 ; `scenarios_fuseau.json` au checkpoint) :

| Scénario | Ép. 04:05 | Ép. 07:22 | Ép. 10:19 | Lecture conditionnelle |
|---|---|---|---|---|
| UTC | −0,1 bp | +6,0 bp | fenêtre vide | incohérent avec le profit de l'épisode 1 |
| **GMT+2** | **+25,6 bp** | **+7,0 bp** | **+9,7 bp** | directionnellement cohérent avec 3/3 profits acheteurs |
| GMT+3 | −2,0 bp | −1,6 bp | −2,9 bp | incohérent avec 3/3 profits acheteurs |

**Conclusions, exactement calibrées :** le scénario GMT+3 est
*fragilisé* (incompatible avec le sens des profits affichés, sauf
coûts ou artefact d'affichage inconnus) ; GMT+2 est le seul scénario
sous lequel l'ensemble des observations est cohérent, et il est aussi
le mieux documenté (hiver) ; **le fuseau officiel reste UNKNOWN** —
une cohérence directionnelle n'est pas une preuve documentaire, et la
sélection du fuseau « qui fait coller » les profits est précisément le
raisonnement circulaire interdit. Ce qui est **invariant** (vrai sous
tous les scénarios) : 3 épisodes de paires simultanées acheteuses,
détentions de 14/60/81 s, aucun prix observé donc aucun rendement en
bp calculable. Verdict du dossier : **NOT_IDENTIFIED, N2** — mais
l'incertitude est désormais structurée : une seule pièce (fuseau
documenté ou export avec prix) lève l'essentiel.

## E/F. Recherche économique indépendante (premiers résultats)

Deux familles **nouvelles** (hors ME-001/002/003), préenregistrées
seq508, sur ticks locaux novembre 2026 (découverte 20–24, validation
25–27 ; résultats `discovery_independante_nov2026.json`) :

- **H-ASYM** (la volatilité suivante dépend du sens de la barre 5 min) :
  découverte 9,52 bp après hausses contre 9,78 après baisses ;
  validation 9,26 contre 8,76 — **le signe s'inverse entre segments** :
  pas d'asymétrie stable sur cet échantillon. RÉFUTÉE sous cette forme
  (échantillon de 7 jours : portée limitée, à retester sur corpus si
  une raison nouvelle le justifie).
- **H-BOUNCE** (réversion après mouvement extrême d'1 minute ≥ 10 bp) :
  la minute suivante part dans le sens inverse dans 49,0 %
  (découverte) et 54,1 % (validation) des cas — indiscernable d'un
  pile ou face. Aucune signature directionnelle au Mid à cet horizon
  sur cet échantillon. NON DÉTECTÉE.

Aucun de ces résultats n'est un edge ; ce sont des bornes honnêtes
posées par le système, sur données autorisées, avec coûts non encore
en jeu puisque rien n'a survécu au stade descriptif.

## G. Prochaines expériences préenregistrées

1. TR002 : dès réception du fuseau documenté ou d'un export avec prix,
   exécuter l'alignement (protocole prêt, seq507) — coût minimal,
   lève 3 hypothèses d'un coup (score de priorisation maximal).
2. Corpus certifié (CI) : étendre H-ASYM/H-BOUNCE à 12 partitions
   étalées 2012–2026 avant tout classement définitif des familles.
3. Nouvelle famille candidate à formuler par C : relation entre
   intensité des ticks (activité) et volatilité réalisée suivante —
   non encore testée, à préenregistrer avant calcul.

## H/I. Ressources et état des moteurs

Calcul local : secondes par jour de ticks (DuckDB/pandas) ; aucune
ressource nouvelle. État : A durci (dédup, fiabilité), B inchangé,
C alimenté par les scénarios, D inchangé, E doté de la priorisation,
F capable de conclusions conditionnelles, G conserve ses gates,
H fermé, I-A/I-B inchangés. La philosophie est désormais codée :
**ni inventer ce qu'on ignore, ni renoncer à apprendre ce qui reste
identifiable.**
