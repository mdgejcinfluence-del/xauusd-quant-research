# CAMPAGNE 2 — AUDIT STATISTIQUE DE LA DÉTECTION

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Procédure (gelée seq 162–164, avant calcul)

- Famille fermée de **24 comparaisons** énumérées dans le plan ; aucun test ajouté,
  retiré ou reformulé après calcul. Seule correction de saisie : le seuil matériel
  de T22, inscrit « 9 » par erreur dans la table machine, ramené à 0,05 (la règle
  générale du plan : 5 points) **avant** la classification, et consigné ici.
- Statistiques : différences de proportions (points) et ratios de médianes ;
  **bootstrap par grappes** (grappe jour×niveau, à défaut journée), 2 000
  répétitions, graine 20261113 ; IC 95 % percentile ; p bilatéral déduit de la
  distribution bootstrap centrée sur l'effet nul.
- Multiplicité : **Benjamini-Yekutieli** sur les 24 p (dépendance arbitraire entre
  tests — plusieurs partagent les mêmes épisodes, p. ex. T01/T03/T06).
- Règle J1 nouvelle : p_BY < 0,05 ET écart ≥ seuil matériel (5 points / ratio 1,15)
  ET ≥ 200 événements et ≥ 100 grappes par bras ET signe cohérent dans ≥ 2 ères
  (vérification par ère calculée séparément et publiée dans le rapport : toutes les
  candidates la satisfont ; T12 la satisfait dans le sens global en 2 ères sur 3,
  l'ère 2010–13 étant neutre).

## Incidents de procédure (consignés, corrigés avant livraison)

1. **Bug de p-valeur bootstrap** : la première exécution calculait p comme la part
   des réplicats dépassant l'effet observé *en valeur absolue* — avec des réplicats
   centrés sur l'observé, tous les p sortaient ≈ 0,5. Détecté à la lecture (aucun
   test ne pouvait être significatif malgré des IC excluant zéro), corrigé en
   p bilatéral centré sur zéro, seconde exécution complète. Le code livré
   (`ci_tools/campaign02_detection.py`) est celui de la seconde exécution.
2. **Intervalle dégénéré de T03** : le délai de réintégration est mesuré en minutes
   entières ; les médianes bootstrap valent presque toujours 2 et 3 min, d'où un IC
   du ratio réduit à [0,67 ; 0,67]. L'IC est publié tel quel ; la précision réelle
   est limitée par la granularité minute, pas par l'échantillon.

## Dépendances entre tests (déclarées)

T01/T03/T06 décrivent la même population de dépassements sous trois mesures (T06 est
le complément mécanique de T01 — il n'est pas compté comme découverte séparée).
T08/T09/T10 conditionnent sur le même sous-ensemble de retests. Les grappes se
recouvrent entre EV2 et EV3 (même jour×niveau). BY est choisi précisément parce
qu'il reste valide sous dépendance arbitraire ; le prix est une puissance moindre,
assumée.

## Ce que la procédure ne garantit pas

- Le bootstrap par grappes traite la dépendance intra-grappe, pas la dépendance
  temporelle entre journées voisines (volatilité persistante) : les IC sont donc
  potentiellement optimistes pour les contrastes d'ère, qui sont de toute façon lus
  comme des dérives descriptives, pas comme des effets.
- Les terciles de profondeur/amplitude sont calculés par ère sur l'ensemble de
  l'ère (quantiles d'ère connus seulement en fin d'ère) : la classification d'un
  événement de 2010 utilise des bornes calculées avec des données de 2011–13 du
  même bloc. C'est une limite de descriptif rétrospectif, écrite ici ; une
  détection temps réel exigerait des terciles strictement causaux roulants.
- Aucun test ne porte sur une variable de gain ; « significatif » signifie
  uniquement « écart descriptif documenté contre sa référence conditionnelle ».
