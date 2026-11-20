# CAMPAGNE 2.2 — ÉTAT DE COUVERTURE

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Matrice de couverture : corpus de référence (Campagne 1, décennal) vs reconstruction 2.2

| Famille | Corpus C1 2010–13 | Corpus C1 2014–16 | Corpus C1 2017–20 | Reconstruction 2.2 livrée |
|---|---|---|---|---|
| EV2 dépassements | 15 540 | 10 110 | 10 361 | **12 144 épisodes (2010 → 2014-03)** : 11 513 en ère 1, 631 en début d'ère 2, **0 en ère 3** |
| EV2 réintégrations | 13 244 | 8 579 | 8 767 | Incluses comme issues des instantanés (même périmètre) |
| EV3 cassures | 2 104 | 1 145 | 708 | Lignes T0–T+5 + RETEST sur le même périmètre restreint (1 328 retests confirmés) |
| EV3 retests | 1 709 | 886 | 533 | Idem |
| EV1 extrêmes | 4 140 | 3 096 | 3 052 | Hors périmètre de reconstruction 2.2 (non demandée) |
| EV5 impulsions | 39 510 | 20 112 | 10 099 | Hors périmètre 2.2 |
| EV6 consolidations | 19 768 | 23 694 | 27 591 | Hors périmètre 2.2 |
| EV4 / EV7 (C1.1) | voir seq 160 | — | — | Hors périmètre 2.2 |

Journées du corpus : 1 035 (ère 1), 774 (ère 2), 763 (ère 3). Journées reconstruites :
777, toutes en ères 1–2. **La couverture actuelle est insuffisante pour généraliser
le résultat T0 à l'ensemble du corpus** : en particulier, la stabilité de
l'association T0 en ère 2017–20 (marché le plus calme, profondeurs plus faibles)
est inconnue.

## Intégrité de la procédure (gel maintenu)

Définitions gelées (seq 157/170), instants T0/T+1/T+3/T+5, règles de classement,
fenêtres futures bornées à T0+60, bootstrap par grappes, traitement des censurés :
**inchangés**. Lorsque les données redeviendront accessibles, la reprise appliquera
la procédure identique, sans modification de paramètres après consultation des
résultats — le moteur par lots commité (`campaign022_engine.py`, garde
≥ 200 journées par lot) est l'instrument de cette reprise.
