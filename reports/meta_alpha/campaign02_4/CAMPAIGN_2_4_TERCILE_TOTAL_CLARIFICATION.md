# CAMPAGNE 2.4 (CHANTIER A) — POURQUOI 4 200 INDÉPENDANTS AU TOTAL ?

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Clarification
demandée par le propriétaire (seq 195). Chantier séparé et **inactif** :
ce document n'active rien, ne modifie aucun paramètre gelé (seq 183), ne
consulte aucun flux prospectif (il n'en existe pas).

## La question

L'hypothèse principale compare les terciles **extrêmes** (BAS vs HAUT de la
profondeur atteinte à T0), dimensionnés à 1 400 indépendants par groupe —
soit 2 800 indépendants décisionnels. Pourquoi la réconciliation
(`CAMPAIGN_2_4_EFFECTIVE_N_RECONCILIATION.md`) parle-t-elle alors de
**4 200 indépendants au total** ?

## La réponse, en trois points

1. **Le tercile médian est collecté, pas choisi.** La classification d'un
   épisode prospectif dans un tercile se fait par seuils expanding-window
   calculés sur le passé : au moment où un épisode survient, on ne peut ni
   décider de son tercile, ni refuser les épisodes qui tombent dans le
   tercile médian. La collecte accumule donc mécaniquement les trois
   terciles en proportions voisines ; dimensionner la collecte aux seuls
   extrêmes reviendrait à feindre qu'on peut ne pas collecter le tiers
   médian des épisodes.
2. **4 200 = 3 × 1 400 est un total de collecte, pas une exigence
   décisionnelle.** Le test principal ne consommera que les deux groupes
   extrêmes (2 × 1 400). Les ≈ 1 400 indépendants du tercile médian sont
   **non décisionnels** : ils servent aux descriptions par bloc
   (hétérogénéité temporelle du protocole), à la vérification des seuils
   expanding-window et à l'estimation de la structure de grappes en cours
   de collecte — jamais à un test supplémentaire de l'hypothèse
   principale, qui reste unique.
3. **Le critère d'arrêt reste ancré sur les extrêmes.** Formellement :
   collecte close lorsque **chaque groupe extrême** atteint son double
   critère (épisodes ≥ 1 400 × DE figé **et** grappes ≥ 500) **et** que le
   total atteint 1 500 grappes. À structure d'amorçage, ces conditions
   convergent vers ≈ 10 000–10 700 épisodes bruts au total (≈ 4 200
   indépendants équivalents au DE central), dont le tiers médian est le
   sous-produit attendu de la classification — pas un troisième groupe à
   « remplir » activement. Si, en fin de collecte, le tercile médian
   comptait moins d'épisodes que les extrêmes (dérive des seuils), cela
   ne retarderait pas la clôture dès lors que les critères des extrêmes et
   le plancher total de grappes sont atteints : la règle écrite ici, avant
   tout ordre d'exécution, tranche ce cas.

Aucune puissance n'est dimensionnée sur 4 200 ; la puissance de 90 % ne
porte que sur le contraste extrême contre extrême (2 × 1 400
indépendants), conformément au gel.
