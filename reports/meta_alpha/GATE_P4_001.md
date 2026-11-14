# GATE P4-001 — Candidat H-P3-A : **REJETÉ** (critère préenregistré appliqué)

Protocole exécuté sans modification: règle « ROLL_STD_100 au-dessus du quintile
supérieur causal walk-forward » (seuils expansifs par partition, warm-up 20 000
valeurs, jamais de seuil global), entrée longue au ASK, sortie au BID du premier
tick >= t+H (15 min / 1 h), origines non chevauchantes, purge 1 h aux frontières,
IS 2010->2020-01-20, OOS 2020-01-20->2023-05-31 (41 mois), Holdout jamais lu
(315 partitions, aucune au-delà de la fin OOS). 33 243 trades réels simulés tick à tick.

## Résultats (p4/P4_001_RESULTS.json, trades bruts dans p4/trades.csv)
| Segment | Horizon | n trades | Mid brut (bp) | Net de spread Bid/Ask (bp) | IC95 bootstrap par blocs mensuels (bp) | Taux gagnant |
|---|---|---:|---:|---:|---|---:|
| IS | 15 min | 7 184 | +0,34 | **-2,01** | [-2,44 ; -1,58] | 40,6 % |
| IS | 1 h | 4 987 | +0,14 | **-2,27** | [-2,93 ; -1,64] | 42,7 % |
| OOS | 15 min | 14 005 | +0,27 | **-2,90** | [-3,78 ; -1,92] | 40,0 % |
| OOS | 1 h | 7 067 | +0,45 | **-2,47** | [-3,18 ; -1,76] | 45,2 % |

## Lecture
Le pattern P3 existe bien en mid (+0,1 à +0,5 bp) mais il est **5 à 10 fois plus
petit que le coût du spread** payé à l'aller-retour. Nets de spread, les rendements
sont négatifs partout, et en OOS les intervalles bootstrap (blocs mensuels,
2 000 réplications, graine 42) sont **entièrement sous zéro**.
Critère préenregistré: « si l'intervalle bootstrap du rendement net de spread
inclut 0 en OOS -> REJETÉ ». Ici le critère est dépassé dans le sens du rejet
(IC entièrement négatif). **P4-001 = REJECTED, conservé comme résultat négatif.**
Coûts inconnus (slippage, commissions) non comptés: ils aggraveraient le résultat;
le classement reste CONDITIONAL, jamais NET au sens complet.

## Exécution et ressources (réelles)
Runs GitHub: 43573278780 (annulé par l'agent à 48 min: risque de rejet de push
détecté), 43577156705 (échec YAML 0 s, corrigé), 43577181228 (échec téléchargement
partition 261 après 2 h 06, 10 714 trades saufs par checkpoint), 43588264414
(confirmation de l'erreur), 43589913445 (repli Range, échec 263), 43592672180
(bug de shadowing corrigé), 43594784236 (**succès, 39 min 17 s**, collecte complète).
Total: ~5 h 20 de calcul GitHub Actions CPU sur 3 jours calendaires de session,
**0 Fcfa** (quotas gratuits), 0 accès Holdout, corpus intact.
Corrections techniques en cours de route (toutes journalisées dans les commits):
rebase-avant-push des checkpoints, anti-duplication des trades en reprise,
3 voies de téléchargement (gdown, HTTP direct vérifié, Range séquentiel).

## Suite autorisée (sans nouvel ordre requis)
H-P3-A est morte comme stratégie longue systématique. Travaux restant valides:
explorer d'autres familles indépendantes (P3-002: asymétries, extrêmes de spread,
dynamique d'inter-arrivée) avec le même protocole préenregistré, en gardant
l'exigence « effet mid >> spread » comme filtre d'ordre de grandeur dès P3.
Aucun portefeuille ne peut être construit sur un candidat rejeté: P7 reste vide.
NO_EDGE reste le résultat si aucune famille ne passe P4/P6.
