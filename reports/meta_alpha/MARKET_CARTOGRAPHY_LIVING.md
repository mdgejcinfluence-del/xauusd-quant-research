# CARTOGRAPHIE VIVANTE DU MARCHE XAUUSD (document permanent, mis a jour a chaque decouverte)

Perimetre: IS certifie 2010-2020, cotations Bid/Ask natives (pas des transactions).
Reference mensuelle: monthly_reference/MONTHLY_REFERENCE_SERIES.json (120 mois).

## Dimensions: etat de comprehension
| Dimension | Etat | Ce qui est etabli |
|---|---|---|
| Structure des cotations | COMPRISE (descriptif) | mecanique changee: bilateraux 99% (janv. 2010, mensuel) -> passage durable sous 50% des oct. 2012 -> ~31-37% (2019); unilaterales symetriques bid/ask |
| Prix construit (mid) | COMPRIS (descriptif) | ac1 tick era-dependante (0.497 T1 -> 0.034 T3), non conditionnee par le spread; s'eteint a 100 evt/60 s |
| Spread | COMPRIS (descriptif) | median ~4 bp (2010) -> ~1.9 bp (2019); persistance tick ac1 0.633 croissante entre tiers; relation a l'intensite negative aussi INTRA-regime de cotation (rho -0.60 bilateral, -0.47 unilateral; mixte n=15 non concluant) |
| Activite / inter-arrivees | PARTIEL | dt moyen mensuel 3.7 s (2010) -> 0.6-0.9 s (2019); distributions fines non cartographiees |
| Dependances croisees bid/ask | COMPRISES (descriptif) | aucun leader a aucune epoque; motif +/-1 evenement (ancien regime) -> contemporain (regime recent) |
| Volatilite | PARTIEL | memoire continue (ac|r| 0.457/0.184/0.132), era-dependante; mois extremes: 2010-04, 2012-05, 2012-06 (vol realisee mensuelle z>4); comparaison formelle de modeles continus NON faite (protocole gele a autoriser) |
| Distributions | PARTIEL | queues de rendements de barres symetriques (p99/|p1| 1.05-1.11); queues tick non cartographiees finement |
| Granularites naturelles | COMPRISE (descriptif) | microstructure <=10 evt/30 s; extinction ~100 evt/60 s; memoire de volatilite a toutes echelles |
| Episodes anormaux | EN COURS | voir registre |
| Regimes discrets | AUCUN DEMONTRE | les changements observes sont progressifs (cotation) ou continus (volatilite) |

## Registre des anomalies et episodes (contextuels, vs reference mensuelle)
- GD-06 CONFIRME DESCRIPTIVEMENT: transition de mecanique de cotation 2010-2015, durable sous 50% de bilateraux des 2012-10 (serie mensuelle ponderee ticks).
- GD-07 EPISODE A CARACTERISER: oct. 2012 - janv. 2013, part de ticks sans mouvement du mid 12-23% (reference ~0.5-1.5%), part d'evenements sans changement de prix elevee (12.4% en janv. 2013). Cotations repetees/figees? A caracteriser (durees, spread pendant l'episode) — piste ouverte par la cartographie, non tranchee.
- GD-08 EPISODES SECONDAIRES: parts de rendements nuls elevees (~7-8%) en grappes 2016-04/05, 2017-09 a 2018-01. Meme famille possible que GD-07.
- GD-09 MOIS DE VOLATILITE EXTREME (descriptif): 2010-04 (9.34%), 2012-05 (8.97%), 2012-06 (8.79%) de volatilite realisee mensuelle.
- Refutes/conserves: lead-lag directionnel (absent), reversion < spread (0/282), regimes discrets (non demontres), ac1 tick invariant (refute).

## Regle permanente heritee
Tout phenomene se rapporte a son contexte: mois, regime de cotation
(bilateral/mixte/unilateral), granularite. Les statistiques poolees 2010-2020
melangent au moins deux processus de cotation: a eviter sans mention explicite.

## Prochaines investigations (decidees en autonomie, perimetre IS)
1. Caracteriser GD-07/GD-08 (episodes de cotations sans mouvement): duree des repetitions, contexte spread/activite — requiert une lecture tick ciblee sur les mois concernes, a preenregistrer.
2. Distributions fines et inter-arrivees par regime de cotation.
3. Comparaison gelee de modeles continus de volatilite (front le plus solide) — protocole a soumettre car il engage la gouvernance des tests.
