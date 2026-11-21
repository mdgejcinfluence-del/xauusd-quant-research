# CAMPAGNE 2.4 — GEL DES SEUILS EXPANDING-WINDOW (PROPOSITION FIGÉE)

**DOCUMENT DE GEL — AUCUN CALCUL EXÉCUTÉ.** Les seuils historiques rétrospectifs
(fragment 2010–2014 : 1,4853/3,4476 bp ; décennie : 1,2499/2,9694 bp) restent
conservés pour les descriptions historiques et ne sont **pas** modifiés par le
présent document ; ils sont interdits comme seuils de confirmation.

## 1. Variable et instant de classification

Profondeur atteinte à T0 (`prof_max_jusqua_bp` à l'instantané 0 : excursion
maximale au-delà du niveau sur la seule barre de franchissement), connue à la
clôture de cette barre. Aucune information postérieure à T0 n'entre dans la
classification d'un épisode de confirmation.

## 2. Calibration initiale

- Amorçage (burn-in) : l'ensemble des épisodes du corpus IS consulté
  (2010–2020) sert uniquement à calculer les **seuils initiaux** et à estimer ρ
  (document de dimensionnement). Ces épisodes ne font pas partie de
  l'échantillon de confirmation.
- Seuils initiaux = quantiles 1/3 et 2/3 de la profondeur atteinte à T0 sur
  l'amorçage, calculés une fois, publiés dans l'ordre d'exécution.
- Aucun épisode prospectif n'est classé avant la publication de ces seuils.

## 3. Règles de mise à jour (figées)

- Schéma : **expanding window** (toute l'histoire disponible à chaque mise à
  jour). Le schéma rolling n'est pas retenu pour la décision ; il pourra figurer
  en sensibilité si l'ordre d'exécution le prévoit explicitement.
- Fréquence : **mensuelle**, le premier jour ouvré du mois, avant l'ouverture des
  sessions européennes.
- Données de mise à jour : tous les épisodes (amorçage + prospectifs déjà
  formés) dont **T0 est strictement antérieur** à la date de mise à jour. Seules
  les valeurs de la variable à T0 sont utilisées (aucune issue n'est consultée
  pour mettre à jour les seuils).
- Entre deux mises à jour, les seuils sont constants ; chaque version est
  horodatée, journalisée et publiée avec les résultats finaux (trajectoire
  complète des seuils).
- Ex æquo et arrondis : quantiles empiriques sur rangs (`method='first'`),
  valeurs en bp à 4 décimales, règle identique à celle des descriptions
  historiques pour rester comparable.
- Aucune modification du schéma, de la fréquence ou de la règle de calcul après
  le début de la collecte, sous peine d'invalidation de l'échantillon recueilli
  (qui deviendrait matériau consulté).

## 4. Ce que ce gel ne fait pas

Il ne lance aucune collecte, ne consulte aucun résultat de confirmation, ne
modifie aucun seuil historique et ne préjuge pas de la décision J2, qui restera
propriétaire et postérieure au calcul unique prévu par le protocole.
