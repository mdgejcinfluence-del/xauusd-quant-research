# CTRS-007 — FRONTIÈRE D'IDENTIFIABILITÉ

**Démontré** : mécanique du PWA et déplacement par renforcement ;
trajectoires de récupération (bornes chiffrées) ; non-rentabilité de
nos moteurs gelés sur 2026 ; écarts exacts des déclencheurs simples.

**Fortement contraint** : entrée H3+F2 (fidélité en-échantillon) ;
intervalles de renforcement ; signature pré-clôture (état favorable sur
jambe haussière, 5/5) ; patience comme conséquence d'état.

**Compatible, non identifié** : seuils ponctuels H3 ; sizing (familles
bornées) ; déclencheur de sortie : cadence à phase libre / hybride /
variable hors-Mid — preuve d'équivalence : chaque famille reproduit les
cinq instants sans contredire aucun contre-exemple, et les paramètres
qui les séparent ne sont contraints par aucune observation (une
clôture par panier ne contraint ni (N, φ), ni un seuil hybride).

**Réfuté** : H1/H2 ; premiers passages de sortie ; persistance unique
(35 intersections vides) ; cadence ancrée > 1 s ; doublement universel ;
épuisement au sommet ; fidélité = rentabilité.

**Impossible avec le corpus actuel** : séparer décision / transmission
/ exécution (résolution tick 0,05–0,25 s, pas de Bid/Ask, pas de logs) ;
comportement Sell, stop, plafond, positions 4+ (absents) ; rentabilité
du provider ; effet causal du renforcement (censure 126/140).

**Observations minimales pour franchir la frontière** :
≥ 10–20 clôtures réelles indépendantes horodatées avec Bid/Ask
(départage des familles de sortie et contrainte de (N, φ)), des paniers
Sell et en régime adverse (direction, stop, queue). Voir
`MISSING_EVIDENCE_REGISTER.csv`.
