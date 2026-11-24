# PHASE 23-C — RÉCONCILIATION DES TRAJECTOIRES FOMC

Population : 73 événements FOMC + 73 témoins 23-B (développement uniquement, consommés).
Chaîne tick : 8 lots IS, traitement borné par journée (DuckDB), fragments `P23C_PATH_*`.
Qualité : âge médian de P0 = 0,42 s ; retard médian du point P15 = 0,13 s ; délai médian d'entrée
après décision = 0,13 s ; aucune NON_EXECUTION parmi les 73 événements directionnels.
Points de référence t0+{5,15,30,45,60,120,240} min = premier Mid réel à/après la cible, retards
conservés dans `PHASE23C_EVENT_PATH_METRICS.parquet` ; règle de fraîcheur figée avant calcul :
P0 > 300 s ou retard de point > 300 s = non validable (aucun cas rencontré sur les événements).
Excursions post-15 mesurées uniquement sur ticks strictement postérieurs à t0+15 min.
Réaction initiale médiane : 21,9 bp en valeur absolue. MFE et MAE post-15 quasi symétriques
(60 min : 22,2 contre 22,3 bp ; 120 min : 34,2 contre 32,2 bp) ; temps médians jusqu'au MFE/MAE
≈ 17 min des deux côtés. Amplitude conservée médiane à 60 min : 1,08 (le déplacement initial est
en médiane intégralement conservé par rapport à P0) — cohérent avec l'audit des 71 %, sans
progression directionnelle après P15 (52,1 %).
