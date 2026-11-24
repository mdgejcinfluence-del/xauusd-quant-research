# MA-EDGE-01 — 02 · REFORMULATION DU PROBLÈME ÉCONOMIQUE

La question n'est plus « le prix va-t-il reprendre ? » mais, à t_decision :

**existe-t-il une action dans {LONG, SHORT, FLAT} dont l'espérance du payoff net exécutable,
sous un contrat de sortie verrouillé avant observation, est positive après spread et slippage,
avec une distribution de pertes supportable ?**

Contrat économique type désormais exigé pour toute expérience du programme : instant de
décision ; informations disponibles à cet instant (avec horodatage de publication) ; direction
autorisée ; premier prix exécutable (Ask/Bid, délai maximal) ; invalidation et sortie définies
avant le test ; durée maximale ; comptabilité 19-B (spread une fois, S0/S1/S2, commissions
exclues et signalées) ; conditions de non-exécution ; résultat en log-bp ; risque maximal
(MAE, quantiles de perte) ; coût aller-retour maximal annulant l'espérance (break-even de coût).

Cibles admissibles, par ordre de préférence : (1) espérance conditionnelle du payoff net sous
le contrat ; (2) probabilité que le payoff net dépasse le coût ; (3) probabilité qu'une barrière
favorable soit atteinte avant l'invalidation ; (4) décision optimale LONG/SHORT/FLAT. Les labels
de trajectoire (Y_RESUMPTION et apparentés) sont relégués au rang de diagnostics : la Phase 24-E
a montré qu'un label peut être réalisé tôt, capturable, et pourtant économiquement neutre une
fois la sélection complète comptée.
