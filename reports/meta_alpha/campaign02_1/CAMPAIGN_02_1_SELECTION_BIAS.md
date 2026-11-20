# CAMPAGNE 2.1 — BIAIS DE SÉLECTION DES DEUX ANOMALIES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Biais n°1 — Le classeur contient le futur (A et B)

`profondeur_bp` = excursion maximale sur les 61 barres suivant le début de
l'épisode, y compris après réintégration (A) et sur une fenêtre chevauchant
l'issue à +60 min du retest (B). Conséquence mécanique : trier par profondeur
trie par « chemin qui s'est éloigné et n'est pas revenu tôt ». Le test causal de
contrôle R01 (ampleur initiale observable au déclenchement, +5 bp ou non) donne un
écart de réintégration de −0,8 point, non significatif : **à information égale à
celle du déclenchement, l'effet disparaît**. Toute réutilisation future des
fiches ANO-C2-001/002/004 doit citer cette requalification.

## Biais n°2 — Conditionner sur le retest (B)

Le sous-échantillon des cassures retestées (3 128) exclut précisément les
traversées qui ne reviennent jamais toucher le niveau (profondeur médiane
50,7 bp, réintégration 8,4 %). L'issue « encore au-delà » n'existe que pour les
retestées. Deux lectures interdites : (i) appliquer 55 % (ou 26,9/80,7 %) à
« une cassure » en général ; (ii) comparer l'après-retest à l'après-réintégration
sans appariement (cf. T24, déjà classé contexte biaisé en Campagne 2).

## Biais n°3 — Appariement par grappes (comptage)

La liaison cassures↔retests utilise la grappe `date|niveau|côté` : plusieurs débuts
de cassure dans la même grappe sont appariés au même retest (3 350 cassures
« retestées » par appariement contre 3 128 lignes de retest). Les effectifs par
grappe, publiés par test, sont l'unité d'indépendance correcte ; les n bruts
surestiment l'information. N effectif indicatif (grappes) : A — 5 057 grappes pour
36 011 dépassements ; B — 2 763 grappes pour 3 957 cassures.

## Biais n°4 — Censure informative

Les 5 421 non-réintégrations sous 60 min ne sont pas des manquants aléatoires :
leur profondeur médiane (30,8 bp) est 3,5× celle des réintégrations rapides. Tout
taux de réintégration publié est donc un taux **sous fenêtre de 60 min**, et le
délai médian de 3 min ne vaut que pour les réintégrés. Aucun modèle de survie n'a
été ajusté (campagne descriptive).

## Biais n°5 — Terciles rétrospectifs d'ère

Les bornes de terciles/quartiles sont calculées sur chaque ère entière : classer
un épisode de 2010 utilise des quantiles incluant 2011–2013. Limite déjà écrite à
l'audit statistique de la Campagne 2 ; les tests de sensibilité (médiane, quartiles)
montrent que l'association descriptive ne dépend pas du découpage — mais aucun de
ces découpages n'est causal au sens temporel strict. Le seul classeur strictement
causal testé ici est R01 (seuil fixe +5 bp, connu ex ante) : négatif.
