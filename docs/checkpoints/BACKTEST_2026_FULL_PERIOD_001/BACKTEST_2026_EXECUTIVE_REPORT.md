# BACKTEST-2026-001 — RAPPORT EXÉCUTIF

**Question : les moteurs reconstruits auraient-ils gagné de l'argent entre
janvier et le 27 novembre 2026, après coûts, sans aucun réajustement ?**

## Verdict : NÉGATIF

Sur toute la couverture réellement disponible (12 janvier – 30 septembre
certifiée, plus 7 jours de novembre ; octobre absent, jamais simulé) :

| Moteur | Paniers | Net S0 (USD modèle) | PF | Gagnants | Drawdown max | Espérance/panier |
|---|---|---|---|---|---|---|
| V1 gelé | 4 107 | **−30,40** | 0,528 | 22,9 % | −31,09 | −0,0074 |
| V2-F2 gelé | 3 275 | **−33,24** | 0,371 | 20,5 % | −33,45 | −0,0101 |

Janvier–septembre seul : V1 −29,97 (rejeu archivé seq457), V2-F2 −32,31
(rejeu CI de cette mission, run 46040242849, partitions VERIFIED).
Novembre partiel : V1 −0,432, V2-F2 −0,930 (réconciliations exactes avec
seq455/seq459). Un seul mois positif sur onze : juin pour V1 (+0,83) ;
aucun pour V2-F2. La robustesse aux coûts (scénario C) aggrave tout :
à S3, V1 −131,16 et V2-F2 −112,99.

Faits saillants : les deux moteurs restent bloqués des semaines par des
paniers sans stop (septembre : données complètes, **zéro clôture**) ;
séries de pertes jusqu'à 40 (V1) et 62 (V2-F2) paniers consécutifs ;
durée maximale d'un panier ≈ 13,6 jours. V1 domine V2-F2 sur le net, le
PF, l'espérance et le drawdown ; F2 améliore la fidélité d'entrée
en-échantillon mais dégrade l'économie — fidélité ≠ rentabilité, une
nouvelle fois.

Ces résultats sont ceux de **nos moteurs reconstruits**, pas ceux de
Colorful drops (voir comparaison séparée dans `ENGINE_COMPARISON.md`).
Un résultat positif n'aurait de toute façon rien prouvé sur le provider ;
le résultat négatif, lui, est sans ambiguïté pour nos moteurs.
