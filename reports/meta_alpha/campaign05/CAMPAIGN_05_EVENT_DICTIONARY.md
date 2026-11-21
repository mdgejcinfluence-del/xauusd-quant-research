# CAMPAGNE 5 — DICTIONNAIRE DES ÉVÉNEMENTS (À VALIDER, AUCUN CALCUL)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Soumis à
validation propriétaire ; hash chaîné avant toute extraction si validé.
Prix Mid de barres M1 (corpus campagnes 1–4) ; horodatages UTC ; seuils
toujours causaux (passé seul) ; aucun extrême final ne classe un événement
en cours de journée ou de semaine.

## 1. Conventions communes

- Sessions UTC fixes (aucun changement d'heure n'existe en UTC ;
  convention constante publiée) : **ASIE 00–08, LONDRES 08–13,
  NEW YORK 13–21, NUIT 21–24**.
- Journée de cotation = date UTC présente dans le corpus ; journée
  utilisable si ≥ 300 barres M1 complètes ; session utilisable si ≥ 60
  barres ; semaine = lundi–vendredi UTC, utilisable si ≥ 4 journées
  utilisables. Ères 2010–13 / 2014–16 / 2017–20. Jour de semaine = jour
  UTC de la date (descriptif, sans seuil importé).
- Unité d'indépendance : **journée** (F-E et F-F journalier), **semaine**
  (F-F hebdomadaire). Quatre ouvertures ou deux côtés d'extrêmes d'une
  même journée ne sont jamais traités comme indépendants.

## 2. Famille F-E — Sessions

| Élément | Définition proposée (à valider) |
|---|---|
| Ouverture de session | Première barre M1 complète dont l'horodatage de début appartient à la session ; instant d'ouverture = début de cette barre. Sessions attendues à 00:00, 08:00, 13:00, 21:00 UTC ; si la première barre présente est postérieure de plus de 5 minutes à la frontière, l'ouverture est datée à cette barre et le retard est publié (ouverture différée) |
| Fenêtres d'ouverture | +5, +15, +30, +60 minutes après l'instant d'ouverture (barres présentes uniquement) ; observables : amplitude (haut−bas, bp), rendement signé de clôture à clôture (bp), RV de la fenêtre (bp), spread médian des barres de la fenêtre (contexte), excursion favorable/défavorable par rapport au prix d'ouverture (bp) |
| Référence causale d'ouverture | Médiane de la même observable, à la même session, sur les **60 journées de cotation précédentes** disposant de l'ouverture (min 40) ; ratio observable/référence publié à côté de l'observable brute ; aucune référence poolée présentée comme temps réel |
| Mouvement pré-ouverture | Rendement signé des 60 minutes précédant l'instant d'ouverture, sur les barres présentes (connu à l'ouverture, passé seul) ; publié en bp et en tercile causal (60 journées précédentes, même frontière) |
| Issues après ouverture (mesurées) | Sur +30 et +60 minutes : poursuite = extension dans le sens du mouvement pré-ouverture d'au moins la moitié de son amplitude ; retournement = franchissement du prix d'ouverture de plus de la moitié de cette amplitude en sens inverse ; sinon stagnation ; événements censurés si la fenêtre est tronquée par une fin de journée ou un trou > 15 minutes (comptés) |
| Ouverture d'Asie (ancrage inter-jours) | Ouverture de la session ASIE, publiée en trois classes mutuellement exclusives selon le trou mesuré entre la dernière barre de la veille et la première barre du jour : **CONTINUITE** (trou ≤ 5 min), **TROU_INTRA_SEMAINE** (trou > 5 min, veille = journée de semaine précédente), **REOUVERTURE_SEMAINE** (veille = vendredi ou trou > 12 heures) ; l'écart de prix du trou (première ouverture moins dernière clôture de la veille, bp signé) est publié ; aucune barre n'est reconstruite dans le trou |
| Cœur de session | Fenêtre médiane de la session hors première et dernière heures, mêmes observables agrégés par journée, pour les descriptions « session vs frontière » |
| Transition de session | Toute frontière de session ; statistiques avant (−30 min) / après (+30 min) : RV, amplitude, spread médian ; la frontière de 00:00 est toujours publiée avec sa classe d'ancrage d'Asie et jamais fusionnée aux autres sans mention |

## 3. Famille F-F — Extrêmes datés

| Élément | Définition proposée (à valider) |
|---|---|
| Niveaux de référence journaliers | Plus haut H_{j−1} et plus bas B_{j−1} (M1, prix Mid) de la **journée précédente utilisable** — connus à l'ouverture du jour j |
| Première atteinte journalière (HAUT) | Première barre M1 du jour dont le haut **dépasse strictement** H_{j−1} ; horodatage = début de la barre. Égalité exacte (touche sans dépassement) : comptée séparément (« touche »), jamais fusionnée. Symétrique BAS avec le bas < B_{j−1} |
| Mises à jour | Après une première atteinte, chaque extension de l'extrême courant d'au moins **+5 bp** au-delà du dernier niveau de mise à jour enregistré définit une mise à jour datée (la première atteinte constitue le niveau 0) |
| Extrême courant / final | Extrême courant à t = extrême observé jusqu'à t (seul autorisé en variable d'instantané). Extrême final = haut/bas de la journée complète (hebdomadaire : de la semaine complète), publié uniquement dans des tableaux de clôture étiquetés « final, connu à la clôture » |
| Instantanés et issues | À la première atteinte : heure de formation, sens, niveau franchi, retard depuis l'ouverture. Issues sur +15/+30/+60 minutes après l'atteinte : extension supplémentaire au-delà du niveau (bp), retracement maximal sous le niveau franchi (bp et retour éventuel sous H_{j−1} daté), position de clôture de fenêtre par rapport au niveau (bp signée) ; censure en fin de journée comptée |
| Niveaux hebdomadaires | Plus haut / plus bas de la **semaine précédente utilisable** (lun–ven) ; première atteinte dans la semaine courante, datée au jour et à la barre ; semaines incomplètes (moins de 4 journées utilisables, bords du corpus, semaines sans semaine précédente utilisable) : extrême final hebdomadaire censuré et publié comme tel ; aucune atteinte n'est déclarée sur une semaine dont le niveau de référence est censuré |
| Départages et cas limites | Premier franchissement simultané HAUT et BAS dans la même barre M1 (barre engulfing les deux niveaux) : les deux atteintes sont datées à la même barre et marquées « simultanées », jamais départagées arbitrairement ; journées sans première atteinte ni touche : comptées (« journée contenue ») |
| Chevauchement intra-journée | Une journée peut porter une atteinte HAUT et une atteinte BAS : les deux sont conservées, marquées liées (même grappe-journée) ; la seconde atteinte est signalée « postérieure à l'atteinte opposée » sans être exclue |

## 4. Disponibilité temporelle de chaque variable (extrait contraignant)

| Variable | Disponible à | Interdit |
|---|---|---|
| Niveaux H_{j−1}, B_{j−1} et hebdomadaires | Ouverture du jour / de la semaine | — |
| Références causales (60 journées précédentes) | À l'instant de l'événement | Tout poolage sur le futur |
| Mouvement pré-ouverture, trou inter-jours, écart du trou | À l'instant d'ouverture | — |
| Extrême courant à t | À t | Le présenter comme extrême final |
| Issues (+15/+30/+60, poursuite/retournement) | Après la fenêtre | Classer l'ouverture ou l'atteinte par ces issues |
| Extrêmes finaux (jour/semaine) | À la clôture uniquement | Classer, sélectionner ou dater un événement intrajournalier |

## 5. Ce que le dictionnaire interdit

Classer une première atteinte par l'extrême final ; sélectionner les
journées « à extrême précoce » à l'aide de l'heure de l'extrême final ;
reconstruire des barres dans un trou de cotation ; fusionner les classes
d'ancrage de l'ouverture d'Asie ; présenter une référence poolée comme
connue en temps réel ; fusionner les effectifs F-E et F-F ; traiter des
événements d'une même journée comme indépendants.
