# PHASE 24-D — RAPPORT FINAL : CONVERSION ÉCONOMIQUE DU CHAUFFEUR M15

Statut : `EXPLORATORY_POST_HOC`. Modèle, seuil (0,560955) et prédictions gelés de Phase 24-C ;
Directeurs appliqués comme permissions seules, sans réentraînement ; sortie unique à 8 h ;
comptabilité 19-B, S2 principal. Réponses aux quatre questions de clôture :

1. **Non.** Le généraliste ne convertit pas son signal prédictif en espérance positive : P0 donne
   **−3,31 bp en S2 (IC95 par grappes [−5,97 ; −0,61], entièrement négatif)**, médiane −4,95 bp,
   43,8 % d'événements positifs — et même −1,31 bp en S0. Prédire correctement l'étiquette
   « reprise au-delà de l'ancien meilleur niveau de clôture » ne revient pas à gagner sur une
   détention de 8 heures dans le sens de l'impulsion : le label et le rendement terminal mesurent
   deux choses différentes.
2. **Non.** Permission H4 (P1, 86 événements) : −7,01 bp, pire que P0 sur sa population ;
   `M15_H4_GATE_NO_INCREMENTAL_VALUE`.
3. **Non.** Permission D1 (P2, 133 événements) : −0,40 bp, IC95 [−9,81 ; +10,78], avec inversion
   de signe entre 2018 (−7,88) et 2019 (+5,05) ; `M15_D1_GATE_NO_INCREMENTAL_VALUE`.
4. **Non établi.** Sans stop : MAE P99 ≈ 124 bp (P0), pire perte −216 bp, durée médiane en perte
   flottante de 295 minutes sur 480. Aucune compatibilité avec une architecture de risque
   réaliste n'est démontrée.

Verdicts : P0 `M15_TIME_ONLY_PREDICTIVE_BUT_NOT_ECONOMIC` ; P1
`M15_H4_GATE_NO_INCREMENTAL_VALUE` ; P2 `M15_D1_GATE_NO_INCREMENTAL_VALUE` ; global
**`M15_PREDICTIVE_SIGNAL_WITHOUT_ECONOMIC_EDGE`**. Aucun candidat économique n'est inscrit au
registre. Le Chauffeur M15 rejoint le motif récurrent du programme : information prédictive
réelle sur un label de trajectoire, conversion économique négative une fois l'exécution et les
coûts comptabilisés. Aucune politique n'est prête à l'exploitation.
