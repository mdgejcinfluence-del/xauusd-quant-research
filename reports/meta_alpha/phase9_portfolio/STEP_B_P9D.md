# ÉTAPE B — RAPPORT ÉCONOMIQUE P9-D : EXPANSION APRÈS CONSOLIDATION (FILTRE DE VOLATILITÉ)

**Nature gelée : pas une stratégie directionnelle.** Source :
`CAMPAIGN_03_EPISODES_CONS.csv.gz` (consolidations M1, sorties non
censurées), groupes causaux de range de formation BAS (n = 8 250) et
HAUT (n = 7 603).

## Ce que le filtre sait — et ne sait pas — faire

- Range des 60 min post-sortie (médiane) : **11,03 bp (formation BAS)
  contre 12,59 bp (formation HAUT)**. En bp absolus, la formation
  étroite est suivie d'un mouvement légèrement *moindre*, pas plus
  grand : l'effet ANO-C3-003 (+13,3 pts) porte sur la fréquence des
  sorties par barre >2× le range de formation — un **ratio** mécanique
  quand le dénominateur est petit (fréquence de « >2× » : 98,4 % contre
  96,1 % sur le range cumulé, quasi saturée des deux côtés).
- Position signée à +60 min : médiane absolue 4,92 bp (BAS) — aucune
  direction associée, par construction du phénomène.
- Durée de consolidation médiane : 8 min dans les deux groupes.

## Économie

Aucune espérance directionnelle n'existe à chiffrer : appliquer le
modèle de coûts à un « trade » inventé violerait l'ordre (« ne pas
inventer une règle directionnelle »). La valeur éventuelle du filtre
serait indirecte (dimensionnement, choix d'horaires), et elle n'est
pas démontrée par les grandeurs ci-dessus : en absolu, le mouvement
postérieur n'est pas plus ample après formation étroite.

## Verdict P9-D : **SUSPENDRE**

Ni tradable ni réfuté comme contexte : conservé comme paramètre de
cartographie (les consolidations précèdent des ranges d'environ
11–13 bp quelle que soit la formation). Toute utilisation comme filtre
d'une future stratégie devra être redémontrée à l'intérieur du
protocole de cette stratégie, pas héritée de la présente fiche.
Donnée manquante consignée : le spread à l'événement n'est pas stocké
pour les consolidations C3.
