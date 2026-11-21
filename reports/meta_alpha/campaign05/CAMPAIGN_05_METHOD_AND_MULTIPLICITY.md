# CAMPAGNE 5 — MÉTHODE STATISTIQUE, REGROUPEMENT ET MULTIPLICITÉ

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** À figer
avec le dictionnaire validé, avant calcul.

## 1. Unités de regroupement et dépendances (livrable n° 7)

- **F-E** : jusqu'à 4 ouvertures et 4 transitions par journée — tous les
  événements d'une même journée partagent le contexte du jour ; les
  ouvertures d'une même journée sont donc regroupées en **grappe-journée**
  pour toute inférence (effectifs bruts et journées publiés côte à côte).
  Les fenêtres d'ouverture de sessions consécutives peuvent se chevaucher
  à 21:00/00:00 (fenêtre +60 de la nuit contre ouverture d'Asie) : les
  chevauchements sont comptés et signalés, jamais « corrigés » par
  suppression.
- **F-F journalier** : une journée peut porter une atteinte HAUT et une
  BAS (liées, même grappe-journée) ; les mises à jour d'une même
  atteinte sont des mesures répétées d'un seul événement — seule la
  première atteinte entre dans les comparaisons, les mises à jour sont
  descriptives.
- **F-F hebdomadaire** : grappe-**semaine** ; une même journée peut
  contribuer à l'atteinte journalière et hebdomadaire — les deux familles
  de niveaux restent publiées séparément et ne partagent aucune famille
  statistique.
- Dépendance temporelle entre journées voisines : traitée par le
  bootstrap en grappes (journées/semaines) ; aucun modèle de série n'est
  ajusté.

## 2. Inférence

- Bootstrap par grappes-journées (ou semaines) : 2 000 répétitions,
  graine figée au gel d'exécution ; p bilatérales par doublement de la
  plus petite queue de la distribution bootstrap ; IC95 percentiles.
- Correction **BY par famille de cinq comparaisons** (listes fermées du
  document compagnon) ; aucune correction inter-familles n'est appliquée
  car aucune lecture inter-familles n'est autorisée.
- Matérialité : 5 points (proportions), ratio 1,15 (médianes, taux) ;
  suffisance : ≥ 200 épisodes et ≥ 100 grappes par bras ; cohérence de
  signe dans ≥ 2 ères sur 3 hors comparaisons d'ère.
- Lectures possibles, toutes publiées : candidate J1 descriptive,
  significative sous le seuil matériel, négative, non éligible
  (effectifs insuffisants, publiés). Aucune promotion automatique.

## 3. Biais, limites et critères d'inéligibilité (livrable n° 9)

| Risque | Traitement préenregistré |
|---|---|
| Confusion ouverture d'Asie / frontière de journée (00:00 UTC) | Publiée comme confondue ; contrastes internes (frontières sans frontière) et classes d'ancrage par durée de trou ; aucune décomposition causale revendiquée au-delà |
| Trous de cotation et débuts de journée différés | Ouvertures différées datées et publiées ; fenêtres tronquées par un trou > 15 min censurées et comptées ; aucune barre reconstruite |
| Semaines ou journées incomplètes | Journée < 300 barres exclue ; semaine < 4 journées utilisables : niveau hebdomadaire et extrême final censurés ; bords du corpus comptés |
| Barres M1 englobant les deux niveaux (atteintes simultanées) | Datées à la même barre, marquées simultanées, jamais départagées ; publiées en nombre |
| Égalités exactes sur les niveaux | « Touches » comptées séparément des franchissements stricts ; jamais fusionnées |
| Dépendance mécanique possible (une grande journée produit à la fois ouverture ample et atteintes précoces) | Conditionnements contemporains étiquetés comme tels ; aucune antériorité revendiquée sans définition la garantissant ; avertissements mécaniques au registre le cas échéant (patron ANO-C4-002) |
| Inéligibilité | Bras sous les seuils, classe d'ancrage trop rare, semaine de référence censurée : publiés « non éligible » avec effectifs — jamais tus, jamais élargis après coup |

## 4. Ce que la méthode interdit

Comparer F-E et F-F dans une même famille statistique ; utiliser
l'extrême final comme classeur ; traiter des événements d'une même
grappe comme indépendants ; appliquer un coût ou un PnL ; conclure à une
direction. Les fiches éventuelles sont J1 descriptives au catalogue
commun, sans mécanisme inventé.
