# CAMPAGNE 2.2 — PREUVE T0 : QUALIFICATION SCIENTIFIQUE

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Formulation qui fait foi (décision du propriétaire, seq 172)

Partout où les livraisons antérieures pouvaient suggérer une causalité démontrée,
la formulation correcte est :

> **« Association conditionnelle fondée sur des variables disponibles à T0, sans anticipation temporelle. »**

Cette association n'est **pas** un avantage prédictif confirmé : aucune direction,
aucune probabilité exploitable, aucune confirmation chronologique disjointe n'a été
produite. Elle décrit comment les issues ultérieures se répartissent selon une
grandeur connue à la clôture de la barre de franchissement, sur un périmètre
restreint (2010 → mars 2014).

## Effectifs et intervalles (périmètre restreint, bootstrap par grappes, 2 000 répétitions, graine 20261113)

Source : `CAMPAIGN_02_2_T0_STATS.csv`, calculé sur les 12 144 épisodes à T0 de
`CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv` (777 journées : 11 513 épisodes en ère
2010–13, 631 en début d'ère 2014–16 ; sessions New York 6 400, Londres 4 934,
nuit 810).

| Groupe (à T0) | n épisodes | Journées | Grappes | Profondeur médiane | Réintégration ultérieure [IC 95 %] |
|---|---|---|---|---|---|
| Profondeur atteinte (barre T0), tercile BAS | 4 048 | 676 | 1 104 | 0,78 bp | 90,6 % [89,7 ; 91,6] |
| Profondeur atteinte, tercile MOYEN | 4 048 | 714 | 1 220 | 2,28 bp | 88,2 % [87,2 ; 89,2] |
| Profondeur atteinte, tercile HAUT | 4 048 | 751 | 1 450 | 5,65 bp | 77,0 % [75,7 ; 78,3] |
| **Contraste BAS − HAUT** | 8 096 | 777 | 2 554 | — | **+13,6 pts [12,0 ; 15,2]** |
| Profondeur initiale (clôture), tercile BAS | 4 048 | 689 | 1 144 | 0,36 bp | 91,5 % [90,6 ; 92,3] |
| Profondeur initiale, tercile HAUT | 4 048 | 755 | 1 454 | 4,27 bp | 76,4 % [74,9 ; 77,7] |

Lecture : l'association existe dès T0 avec la seule barre de franchissement
(profondeur atteinte ou distance de clôture), à +13,6 points entre terciles
extrêmes — contre +32,4 points pour la classification rétrospective par profondeur
maximale sur 60 minutes (98,2/65,8). Les deux tiers environ de l'ancien écart
étaient donc le chemin ultérieur se résumant lui-même ; le tiers restant est une
association conditionnelle à T0, **non généralisable au-delà du périmètre** tant
que la couverture décennale n'est pas rétablie, et dont la stabilité hors ère
2010–13 n'est pas établie (631 épisodes seulement en 2014–16, aucun en 2017–20).
