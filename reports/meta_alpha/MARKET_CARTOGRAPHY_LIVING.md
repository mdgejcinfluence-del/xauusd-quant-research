# CARTOGRAPHIE VIVANTE DU MARCHE XAUUSD (document permanent, mis a jour a chaque decouverte)

Perimetre: IS certifie 2010-2020, cotations Bid/Ask natives (pas des transactions).
Reference mensuelle: monthly_reference/MONTHLY_REFERENCE_SERIES.json (120 mois).

## Dimensions: etat de comprehension
| Dimension | Etat | Ce qui est etabli |
|---|---|---|
| Structure des cotations | COMPRISE (descriptif) | mecanique changee: bilateraux 99% (janv. 2010, mensuel) -> passage durable sous 50% des oct. 2012 -> ~31-37% (2019); unilaterales symetriques bid/ask |
| Prix construit (mid) | COMPRIS (descriptif) | ac1 tick era-dependante (0.497 T1 -> 0.034 T3), non conditionnee par le spread; s'eteint a 100 evt/60 s |
| Spread | COMPRIS (descriptif) | median ~4 bp (2010) -> ~1.9 bp (2019); persistance tick ac1 0.633 croissante entre tiers; relation a l'intensite negative aussi INTRA-regime de cotation (rho -0.60 bilateral, -0.47 unilateral; mixte n=15 non concluant) |
| Activite / inter-arrivees | COMPRISE (descriptif) | queue lourde dans les 3 regimes: p50 0.26-0.49 s, p95 2.5-7.9 s, p99 6.7-19.5 s; activite en rafales et silences, aucun calendrier suppose |
| Dependances croisees bid/ask | COMPRISES (descriptif) | aucun leader a aucune epoque; motif +/-1 evenement (ancien regime) -> contemporain (regime recent) |
| Volatilite | COMPAREE (etape 1 IS) | memoire reelle mais forme NON DEPARTAGEE entre GARCH/FIGARCH/ARFIMA/SV (protocole gele, QLIKE journalier, 3 perimetres: aucun modele a 4/5 blocs); avantage des modeles a memoire mince en regime recent; mois extremes 2010-04, 2012-05/06 |
| Distributions | COMPRISE par regime (run DIST 43920488453, republications filtrees) | amplitude |r| p50: 0.214 (bilateral) -> 0.124 (mixte) -> 0.066 bp (unilateral); queues symetriques partout (0.97-0.99); epaisseur relative de queue croissante 10.4 -> 18.5; filtrage des republications sans effet sur quantiles/ac1 |
| Granularites naturelles | COMPRISE (descriptif) | microstructure <=10 evt/30 s; extinction ~100 evt/60 s; memoire de volatilite a toutes echelles |
| Episodes anormaux | EN COURS | voir registre |
| Regimes discrets | AUCUN DEMONTRE | les changements observes sont progressifs (cotation) ou continus (volatilite) |

## Registre des anomalies et episodes (contextuels, vs reference mensuelle)
- GD-06 CONFIRME DESCRIPTIVEMENT: transition de mecanique de cotation 2010-2015, durable sous 50% de bilateraux des 2012-10 (serie mensuelle ponderee ticks).
- GD-07 CARACTERISE (run GD07 43913545702, 55 partitions): oct.-dec. 2012, 18-23% de ticks sans mouvement du mid sont des REPUBLICATIONS EXACTES de la meme cotation (bid et ask inchanges: parts identiques 18.1/22.6/18.8%); sequences courtes (p95 = 5 evenements, max 37-98, duree max 3-7 min), spread inchange (2.29 vs 2.19 bp), inter-arrivees plus courtes (0.89 vs 1.39 s). Qualification: artefact de flux (republication de cotations), PAS un marche fige — les prix continuent entre les repetitions.
- GD-08 CARACTERISE, MECANISME DIFFERENT: grappes 2015-12 a 2018-01 (et 2016-04/05, 2017-08 a 2018-01), rendements mid nuls 5-8% mais republications ~0.1%: le mid reste fixe pendant que bid/ask bougent de maniere compensatrice (ajustements de spread a mid constant). Sequences p95 4-12 evenements. Deux familles distinctes que la seule part de rendements nuls confondait.
- GD-09 MOIS DE VOLATILITE EXTREME (descriptif): 2010-04 (9.34%), 2012-05 (8.97%), 2012-06 (8.79%) de volatilite realisee mensuelle.
- Refutes/conserves: lead-lag directionnel (absent), reversion < spread (0/282), regimes discrets (non demontres), ac1 tick invariant (refute).

## Regle permanente heritee
Tout phenomene se rapporte a son contexte: mois, regime de cotation
(bilateral/mixte/unilateral), granularite. Les statistiques poolees 2010-2020
melangent au moins deux processus de cotation: a eviter sans mention explicite.

## Dimensions ajoutees (run MARKET_DIMENSIONS, couverture 268/282, 2010-2018)
- Cycle horaire UTC marque: pic 13h-15h (spread minimal 2.24 bp, dt 0.4 s), creux 21h-23h (dt 8-21 s, spread jusqu'a 3.50 bp). Aucune session nommee (UTC natif).
- Queues tick: le top 1% des mouvements porte ~18.7% de la variance.
- Asymetrie: pas de levier tick; levier journalier faible (-0.054) et era-dependant (ancien -0.108, recent -0.028). Continuation d'amplitude tick (corr signe/carre signe suivant +0.213, descriptif).
- Echelles M5/M15/H1: ac1 -0.011/-0.021/-0.049, queues de barres symetriques.
- REPRISE EXACTE: 14 partitions (part_000269-000282) manquent (quota Drive); relancer import_trigger/market_dimensions.txt ulterieurement, le moteur reprend aux manquantes.

## Prochaines investigations (decidees en autonomie, perimetre IS)
1. FAIT: GD-07/GD-08 caracterises (deux mecanismes separes ci-dessus). Toute statistique tick future devrait exclure ou flaguer les republications exactes (GD-07) pour ne pas gonfler les effectifs.
2. FAIT: distributions fines et inter-arrivees par regime (ci-dessus).
3. FAIT: comparaison gelee executee apres validation proprietaire — verdict NON DEPARTAGE (META_ALPHA_VOL_MODELS_STEP1_REPORT.md). Etape 2 OOS: ordre explicite requis, non engagee.
