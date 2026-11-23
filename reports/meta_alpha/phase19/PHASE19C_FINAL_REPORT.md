# PHASE 19-C — RAPPORT FINAL : SORTIES TEMPORELLES H8 CONTRE H16

**Qualification permanente : exploratoire et post-hoc, cohorte d'évaluation déjà étudiée ; aucune validation indépendante.** Entrée unique commune vérifiée à l'identique contre 17-B (écart 0,0 ; 443 exposés), comptabilité 19-B (spread une fois par les prix Bid/Ask, slippage S0/S1/S2 une fois par côté, commissions exclues), aucune barrière, aucun modèle, aucun seuil. Run CI final `45235937089` vert ; 437 paires complètes.

## Résultats (scénario principal S2)
| | H8 (n=442) | H16 (n=437) | Δ apparié H16−H8 (n=437) |
|---|---|---|---|
| P&L moyen | −2,386 bp | −1,802 bp | **+0,436 bp** |
| P&L médian | −2,681 bp | −2,867 bp | 0,000 bp |
| Part de positifs | 45,9 % | 46,2 % | 42,6 % de deltas > 0 |
| Perte maximale | −221,6 bp | −215,2 bp | — |

## Lecture
Les deux horizons sont **négatifs en S2** ; H16 perd un peu moins en moyenne, mais la différence appariée (+0,44 bp par événement, +0,34 par grappe) a un intervalle de confiance par grappe de **[−2,25 ; +2,69] bp**, avec une médiane à zéro et seulement 42,6 % de deltas positifs : compatible avec l'absence d'effet. En contrepartie, H16 double le temps médian passé en perte (4,8 h → 9,8 h), approfondit le MAE médian (−2,78 → −3,64 dollars) et expose 104 sorties à des délais de fermeture de marché (jusqu'à 69,9 h). La sensibilité S0/S1 ne change aucune conclusion (deltas identiques de +0,436 bp, le slippage s'annulant dans la différence à horizon égal de transaction).

## Verdict : `NO_MATERIAL_HOLDING_TIME_ADVANTAGE`
À signal M1 et entrée identiques, passer de huit à seize heures ne démontre pas d'amélioration économique matérielle et accroît l'exposition en durée. Aucun autre horizon ne doit être testé sur la base de ce rapport sans décision distincte ; aucune stratégie n'en découle.
