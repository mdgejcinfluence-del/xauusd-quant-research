# CAMPAGNE 7 — DICTIONNAIRE F-I : GRILLES, ÉVÉNEMENTS, VARIABLES

**Statut : PRÉPARATION — définitions proposées, non gelées, aucun calcul
effectué.** Constantes marquées « à geler » à fixer au protocole
consolidé validé.

## 1. Grilles de prix (livrable 3) — définies avant tout résultat

- **Grille principale G50** : multiples de 50 USD (…, 1 100, 1 150, …).
  Justification a priori : demi-centaines, figures de cotation usuelles
  de l'or au comptant, indépendante de toute observation du corpus.
- **Anneaux disjoints d'échelle** (pour l'effet d'échelle, sans double
  compte) : **R100** = multiples de 100 ; **R50** = multiples de 50 non
  multiples de 100 ; **R10** = multiples de 10 non multiples de 50.
  R100 ⊂ G50 ; l'union R100 ∪ R50 ∪ R10 = multiples de 10.
- **Grilles placebo décalées** : mêmes pas translatés d'un demi-pas :
  G50+25 (multiples de 50 décalés de +25 USD) et, pour l'anneau R10,
  G10+5. Un pseudo-niveau n'est jamais un multiple de 10.
- **Distances** : toujours publiées en **USD absolus** et en **bp
  relatifs** (distance / niveau × 10⁴). L'échelle absolue d'un pas de
  50 USD vaut ≈455 bp à 1 100 USD, ≈278 bp à 1 800, ≈192 bp à 2 600 :
  les grilles absolues « se resserrent » relativement quand le prix
  monte ; c'est un fait de conception, traité par la comparaison
  d'ères (I-05) et par la publication systématique des deux unités —
  jamais en redéfinissant la grille en cours de campagne.
- Aucune grille supplémentaire (25, 5 USD…) n'entre dans la famille
  fermée ; l'ajouter après coup serait une nouvelle famille.

## 2. Conventions temporelles et causalité (livrable 4)

- Barres M1 horodatées par leur début, **disponibles à leur clôture** ;
  journée civile UTC. Un événement daté par une barre n'est connu qu'à
  la clôture de cette barre ; aucun événement n'utilise de barre future
  par rapport à sa propre fenêtre (les suivis +60 min sont des mesures
  rétrospectives d'épisode, étiquetées comme telles).
- Côté d'approche : déterminé par la position du prix avant l'épisode
  (sous le niveau = approche par en dessous, symétrique au-dessus),
  figé à l'ouverture de l'épisode, jamais révisé.

## 3. Événements (définitions proposées)

- **Approche** : première barre dont l'intervalle [bas, haut] entre
  dans la bande de proximité du niveau (distance ≤ **25 bp**, à geler)
  alors qu'aucune barre des **60 minutes** précédentes (à geler) n'y
  était entrée. Ouvre un **épisode**, daté à la clôture de cette barre.
- **Touche** : première barre de l'épisode dont [bas, haut] contient le
  niveau, **sans franchissement strict** à cette barre.
- **Franchissement strict** : première barre dont la **clôture** est
  strictement au-delà du niveau par rapport au côté d'approche (clôture
  > niveau en approche par en dessous). Une barre qui touche et clôture
  au-delà est un franchissement, pas une touche (convention héritée de
  C5 : seuls les franchissements stricts entrent dans les comparaisons,
  les touches simples sont publiées séparément).
- **Franchissement par saut** : barre d'ouverture de l'épisode ou barre
  suivant un trou dont l'ouverture est déjà au-delà du niveau sans
  barre de contact : classé **SAUT**, publié séparément, exclu des
  franchissements stricts primaires (ordre temporel du contact non
  observable en M1).
- **Rejet** : après une touche, le prix s'éloigne du niveau d'au moins
  **25 bp** (à geler) en clôture, dans les **60 minutes** (à geler),
  sans franchissement strict préalable.
- **Retour de l'autre côté** : après un franchissement strict, une
  clôture revient au-delà du niveau (côté d'origine) dans les 60
  minutes ; sinon **maintien au-delà** à 60 minutes.
- **Distance post-franchissement** : excursion maximale au-delà du
  niveau dans les 60 minutes suivant le franchissement strict, en bp
  du niveau ; censurée si la fenêtre de suivi est incomplète (statut
  publié, jamais calculée silencieusement).
- **Événements simultanés / ordre indéterminé** : une barre ne peut
  toucher deux niveaux distincts que si son amplitude couvre deux pas
  de grille (possible en G10 lors de barres extrêmes) : l'épisode est
  alors marqué **SIMULTANÉ**, l'ordre entre niveaux est déclaré
  indéterminé, et l'épisode est exclu des comparaisons primaires
  (publié). Touche et franchissement « même barre » sont tranchés par
  la clôture (règle ci-dessus) : jamais d'indétermination résiduelle.
- Clôture d'épisode : premier événement terminal (rejet, retour,
  maintien constaté à 60 min, franchissement sans suivi complet =
  censuré) ou fin de journée UTC (censure publiée).

## 4. Variables publiées par épisode

Niveau et anneau (R100/R50/R10 ou placebo), côté d'approche, date,
heure d'approche, distance d'entrée (USD et bp), touche (oui/non,
délai), franchissement strict (oui/non, délai, barre), rejet, retour,
maintien, distance post-franchissement, statuts de censure et de
fenêtre, session de l'approche (ventilation uniquement), amplitude de
la journée (ventilation uniquement), ère.
