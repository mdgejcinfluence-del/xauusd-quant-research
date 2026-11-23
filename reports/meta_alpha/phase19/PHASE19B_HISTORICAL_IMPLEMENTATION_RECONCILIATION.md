# PHASE 19-B — RÉCONCILIATION HISTORIQUE (Phases 13 à 18, sans relecture de ticks)

| Génération | Entrée | Sortie | Slippage | Preuve de cohérence |
|---|---|---|---|---|
| 13-B | premier tick Ask/Bid après décision | clôture Bid/Ask de la dernière minute (bc/ac) | scénarios sur prix exécutables | rapport 13-B seq332 |
| 14 / 14.1 | idem 13-B | barrières aux prix de liquidation tick | deltas mesurés −1,0/−2,0 bp (S1/S2 − S0) | audit 14.1, 54 cellules à 0 écart |
| 15 / 16 | entrées E0–E3 comparées à coûts identiques | idem | sortie seule ou entrée+sortie selon la politique gelée | réconciliations E0 à l'identique (seq340/343) |
| 17-B | premier tick Ask/Bid | tick de franchissement ou dernier tick de liquidation | `remplir` S0/S1/S2 une fois par côté | réconciliation contre Phase 14 : 440/435 événements, écart max ~10⁻¹⁴ bp |
| 17-E / 18-C | (cibles 17-B reprises) | (idem) | hérité de PL_S2, aucune seconde déduction | reproduction 18-C des coefficients 17-E à écart nul |

Divergences documentation/implémentation recherchées : (i) le « coût additionnel 1,7 bp » de la Phase 10 est une hypothèse Mid historique explicitement marquée « à ne pas présenter comme observé » et n'a pas été réintroduite dans les calculs Bid/Ask ultérieurs ; (ii) la P&L en log-bp (uniforme depuis 13-B via les conventions héritées) face au risque en bp arithmétique de 17-D — mélange documenté dans l'audit des unités, gelé, sans anomalie de coût ; (iii) aucune commission, aucun swap, aucune seconde soustraction de spread retrouvée dans quelque génération que ce soit. Aucun résultat gelé n'est modifié par le présent audit.
