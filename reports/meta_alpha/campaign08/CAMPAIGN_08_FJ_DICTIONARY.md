# CAMPAGNE 8 — DICTIONNAIRE F-J : CHOCS CAUSAUX, REGROUPEMENT, SILLAGE

**Statut : PRÉPARATION — définitions proposées, non gelées, aucun calcul
effectué.** Constantes « à geler » soumises au propriétaire.

## 1. Variable de variation M1

Barres M1 (clôtures c_t, début de barre horodaté, disponible à sa
clôture). Variation minute : **r_t = ln(c_t / c_{t−1}) × 10⁴ (bp)**,
définie **uniquement entre barres consécutives d'un même segment
continu** (écart d'exactement 1 minute, même journée UTC pour
l'attribution). À travers un trou, aucune variation n'est calculée :
on ne fabrique pas un « choc » à partir d'un saut non observé (leçon
F-G/F-I) ; les reprises après trou sont publiées comme discontinuité,
hors détection.

## 2. Définition causale des chocs (livrable 3 — priorité absolue)

- **Fenêtre de référence causale** : pour chaque journée UTC D, le
  seuil est calculé sur les variations r des **20 journées de cotation
  précédentes** (à geler), toutes disponibles avant l'ouverture de D,
  et reste **fixe pendant toute la journée D**. Le choc de la minute t
  ne dépend donc que d'informations antérieures à t — et même
  antérieures à sa journée.
- **Seuil d'extrémalité** : **τ_D = quantile 99,5 % (à geler) des |r|
  de la fenêtre causale**, avec **plancher absolu de 10 bp (à geler)**
  pour éviter qu'une période morte ne déclare « extrêmes » des
  variations triviales : seuil effectif max(τ_D, 10 bp).
- **Choc** : |r_t| ≥ seuil effectif de sa journée. Direction :
  haussier si r_t > 0, baissier si r_t < 0 (r_t = 0 impossible au-delà
  du plancher). **Disponibilité : clôture de la barre t.**
- **Intensité relative** : ρ_t = |r_t| / seuil effectif (sans unité) ;
  classes proposées : **modéré** 1 ≤ ρ_t < 2, **majeur** ρ_t ≥ 2
  (constantes à geler).
- **Démarrage et inéligibilité** : minimum **10 journées de cotation
  antérieures et 10 000 variations antérieures** (à geler) avant le
  premier seuil publiable ; les journées antérieures sont
  **INÉLIGIBLES à la détection** (période d'amorçage publiée, aucune
  détection rétroactive). Aucun seuil poolé 2010–2020 ne sert à la
  détection ; une référence poolée rétrospective pourra être publiée
  à titre descriptif séparé, étiquetée non causale, jamais mélangée
  aux chocs causaux.

## 3. Regroupement des événements (livrable 4)

- **Épisode de chocs** : suite maximale de chocs dont les écarts
  successifs sont ≤ **15 minutes** (délai de regroupement, à geler).
  Un écart > 15 minutes ferme l'épisode au dernier choc.
- **Choc isolé** : épisode à exactement un choc. **Épisode regroupé** :
  ≥2 chocs. Les deux classes sont des partitions des épisodes, pas des
  chocs comptés plusieurs fois.
- **Unité statistique primaire : l'épisode**, daté à son premier choc
  (journée d'attribution = journée du premier choc), caractérisé par
  le **signe de son premier choc**, son intensité maximale, son nombre
  de chocs et sa durée. Les chocs individuels ultérieurs d'un épisode
  ne sont **jamais** des observations indépendantes ; ils sont publiés
  descriptivement (comptages), hors tests.
- Signe mixte dans un épisode (choc haussier puis baissier à ≤15 min) :
  épisode classé par son premier choc, drapeau **MIXTE** publié ; les
  épisodes mixtes sont conservés dans les populations (règle fermée à
  confirmer au consolidé) mais ventilés séparément.
- Regroupement statistique : bootstrap par **grappes-journées** (les
  épisodes d'une même journée, et leurs sillages, sont dépendants) ;
  les sillages d'épisodes d'une même journée qui se chevauchent sont
  ainsi traités par la grappe, jamais comme des indépendances.

## 4. Mesures de sillage (livrable 5)

Point de départ : **clôture de la barre du choc** pour un épisode
isolé ; pour un épisode regroupé, clôture du **dernier choc** de
l'épisode — l'épisode n'est connu comme terminé qu'après 15 minutes
sans choc, et son sillage est intégralement **rétrospectif**, publié
comme tel. Horizons : **+15, +30, +60 minutes** (à geler), en minutes
de cotation du même segment/journée ; fenêtre incomplète (trou > 15
min, fin de journée) ⇒ statut CENSURÉ publié, aucun observable
silencieux.

Soit s = signe du choc (ou du premier choc de l'épisode) et c₀ le prix
à la disponibilité :

- **Continuation signée à h** : R_h = s × ln(c_{t+h} / c₀) × 10⁴ (bp) ;
  positive = le prix a continué dans le sens du choc.
- **Retour partiel** : part retracée = max(0, −R_60) / |r_choc| sur
  l'épisode (pour un regroupé, |r| du choc maximal ; définition à
  fermer au consolidé).
- **Retournement** : R_h < −|r_choc| (le prix a dépassé, en sens
  inverse, l'amplitude du choc initial).
- **Excursions post-choc** : excursion maximale favorable et
  défavorable sur 60 minutes (bp, barres [haut/bas]).
- **Stabilisation** : ratio d'activité post/pré = (somme des |r| des
  60 minutes suivant la disponibilité) / (somme des |r| des 60 minutes
  précédant le premier choc), publié sans unité.
- **Nouveau choc** : survenue d'un choc (tout signe) dans les 60
  minutes suivant la disponibilité, hors épisode courant.
- Ordre indéterminé : si un trou traverse la fenêtre, les événements
  de sillage dont l'ordre dépend du parcours inobservé sont déclarés
  **indéterminés** et censurés, jamais reconstruits.

## 5. Disponibilité temporelle (livrable 6)

Le choc est connu à la clôture de sa barre ; l'appartenance à un
épisode regroupé n'est connue qu'à la clôture de l'épisode (dernier
choc + 15 minutes) ; toutes les mesures de sillage sont rétrospectives
à leur horizon. Rien dans F-J n'est présenté comme disponible « à T0 »
pendant l'événement. Le contexte causal pré-événement autorisé pour
les ventilations : session UTC du choc, ère, tercile d'activité
pré-événement (somme des |r| des 60 minutes antérieures, causale par
construction), jamais d'étiquette F3 poolée.
