# LMD-008 — DIAGNOSTIC DES PERTES V1 / V2-F2

Réconciliations de départ intactes (seq475) : V1 −30,40, V2-F2 −33,24 USD
modèle. Aucun moteur modifié, aucune optimisation, aucune V3.

## 1. Principale source démontrée des pertes : l'interaction accumulation × coûts

**DÉMONTRÉ.** Le déficit est concentré dans les paniers à 3 positions :
V1 y perd **−31,96** (les paniers à 2 positions gagnent +1,56) ; V2-F2
y perd **−28,23** sur −33,24. Ces paniers ne gagnent que 7,2 % (V1) et
5,7 % (V2-F2) du temps. Le passage à 3 positions est déclenché par un
recul de −5,5 bp : il sélectionne mécaniquement les trajectoires
adverses (rendements forward médians après entrée des futurs paniers
à 3 positions : −4,7 bp à 5 min, V1) et triple l'exposition
précisément là où la récupération échoue le plus souvent. L'effet
*causal* du renforcement reste néanmoins **NON IDENTIFIÉ** (seq459 :
126/140 contrefactuels censurés) — ce qui est démontré est
l'association massive et le mécanisme de sélection, pas le contrefactuel.

## 2. Les entrées ne sont pas le problème principal — leurs gains sont trop petits pour les coûts

**FORTEMENT ÉTAYÉ.** Les paniers à 2 positions ont des rendements
forward médians positifs (+2,6 bp à 5 min, +6,5 bp à 1 h, V1 janv.–sept.)
et les paniers clôturés en ≤ 60 s gagnent +12,99 (V1). Mais le gain brut
estimé avant spread et coût variable n'est que de ≈ +105 (V1) /
+74 (V2) USD sur toute la période, contre ≈ 136 / 108 USD de coûts
totaux estimés (spread médian CI 1,31–1,66 bp + 1,2 bp variables,
comptés une fois). **Les moteurs sont positifs avant coûts et négatifs
dès le scénario central S0** : la marge brute par panier (~+0,026 USD)
est structurellement inférieure au coût par panier (~0,033 USD).
MFE médiane des perdants : 2,9 bp — 47 % des perdants V1 ont pourtant
revu +3 bp au-dessus de leur PWA final sans que la sortie (au premier
retour Mid ≥ PWA, qui plafonne le gain au voisinage de l'équilibre)
transforme cette excursion en gain net suffisant après coûts.

## 3. Sortie et durée : le plafonnement au PWA + l'absence de stop

**DÉMONTRÉ (mécanique).** La sortie au premier retour au PWA borne le
gain des gagnants (gain moyen +0,035) pendant que les perdants
accumulent durées et renforcements ; les paniers de 1–10 min concentrent
−37,0 (V1). Sans stop, la durée maximale atteint ~13,6 jours et la
politique « un seul panier à la fois » transforme un panier bloqué en
arrêt complet du système : **septembre 2026, données complètes, zéro
clôture** (dernier panier bloquant non enregistré par le moteur gelé —
son identité exacte est **NON DÉMONTRABLE** depuis les sorties
archivées ; le mécanisme structurel, lui, est démontré). Le PnL latent
des paniers non clôturés est exclu des résultats : le déficit réalisé
sous-estime donc l'exposition réelle en fin de segments.

## 4. Pourquoi V2-F2 est plus mauvais

**DÉMONTRÉ (sur mêmes périodes).** F2 supprime des entrées M15
répétées : moins de paniers (3 275 vs 4 107), mais une part de paniers
à 3 positions comparable et une espérance par panier inférieure
(−0,0101 vs −0,0074), un PF de 0,371 (vs 0,528) et 62 pertes
consécutives (vs 40). En novembre comme en janv.–sept., V2-F2 perd
davantage avec moins d'activité : le filtrage retire
proportionnellement plus de paniers courts gagnants (≤ 60 s : +6,53
sur 422 paniers) que de perdants. F2 optimise la fidélité au provider,
pas l'économie.

## 5. Attribution et part quantifiable

La segmentation complète du net S0 est quantifiée (`LOSS_ATTRIBUTION.csv`,
décomposition par segments chevauchants, **non additive**) : paniers
3 positions, paniers 1–10 min, coûts. L'attribution *causale* entre
entrée/renforcement/sortie reste **NON IDENTIFIÉE** : les mécanismes
interagissent (le renforcement est sélectionné par l'adversité, la
sortie plafonne les gains qui paieraient les coûts). Les 100 pires
paniers n'expliquent que 7,5 % (V1) / 9,5 % (V2) des pertes : le déficit
est **diffus et structurel**, pas un problème de queue.

## Verdict aux questions de la mission

1. Source principale : interaction renforcement-en-adversité × coûts,
   sur une sortie plafonnée au PWA sans stop.
2. Part quantifiable : 100 % du net est segmenté ; la part causale par
   mécanisme est non identifiable avec ces données.
3. Ni les entrées seules (forward positifs), ni les coûts seuls (brut
   positif) : leur **interaction avec l'accumulation**.
4. Blocages : sortie conditionnée au retour au PWA + aucun stop +
   panier unique.
5. Faiblesse distinctive de V2-F2 : il filtre les petits gagnants
   rapides plus que les perdants accumulés.
6. Manques : trajectoire du panier bloquant de septembre (non
   enregistrée), Bid/Ask HFM réel, contrefactuels non censurés.
7. À comprendre avant toute nouvelle architecture : comment sortir
   d'un panier dont le PWA n'est plus atteint — c'est-à-dire la gestion
   de l'échec de récupération, que ni V1 ni V2-F2 ne possèdent.

**Aucune V3 n'est proposée, conformément à la mission.**
