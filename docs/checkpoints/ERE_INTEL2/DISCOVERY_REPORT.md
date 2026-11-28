# ERE-INTELLIGENCE-002 — Rapport de découverte sur corpus certifié

## A. Corpus et couverture réellement atteinte

Campagne CI exécutée (run 46117842461, job ERE dédié `success`) sur
**12 partitions stratifiées** (1 sur 29) du corpus certifié : 19,5 M de
ticks analysés, partitions de 2010, 2011, 2014, 2017, 2020, 2023.
Limite déclarée : les premières partitions du corpus ne couvrent qu'un
jour chacune, donc 7 des 12 partitions sont des journées uniques de
2010 — la couverture est **substantielle mais inégale** (découverte
9 partitions, validation 2, confirmation 1). Inventaire revérifié :
348 partitions, 685 118 625 lignes (recalcul seq502). Les conclusions
ci-dessous portent cette limite ; aucune n'est extrapolée au corpus
entier. Ressources : minutes de CI par partition, aucun calcul local lourd.

## B/C. Registre de découverte (segments gelés seq510)

| Famille | Découverte (≤2016) | Validation (2017–22) | Confirmation (2023) | Verdict |
|---|---|---|---|---|
| Persistance de volatilité (acf1 des \|ret\| 5 min) | médiane 0,254 | 0,242 | 0,285 | **INVARIANTE : positive dans 12/12 partitions, tous segments** |
| Réversion après extrême 1 min (part inverse) | 51,2 % | 55,4 % | 54,8 % | faible excès descriptif au Mid (51–55 %), aucun test exécutable Bid/Ask à ce stade — **NON IDENTIFIÉE comme edge** |
| Persistance de signe (5 min) | 48,6 % | 46,9 % | 48,4 % | aucune — proche ou sous 50 % partout |
| Asymétrie de volatilité (hausse − baisse) | +0,27 bp | −0,22 bp | −0,01 bp | **signe instable : RÉFUTÉE comme structure stable** (confirme le test de nov. 2026) |
| Expansion après contraction | vol suivante < moyenne : 9/9 | 2/2 | 1/1 | **contredit l'idée « contraction → expansion »** : la persistance domine, les barres calmes suivent les barres calmes |
| Saisonnalité intrajournalière | pic de volatilité 13–16 UTC (mode 13 UTC), ratio max/min 2,4–10 | — | — | structure temporelle réelle et stable en direction, amplitude variable selon la taille de partition |

## Ce que nous avons appris sur XAUUSD (rapport exécutif)

1. La structure la plus solide du corpus échantillonné n'est pas
   directionnelle : c'est la **persistance de la volatilité** — les
   périodes agitées et calmes se regroupent, partout, de 2010 à 2023.
2. Aucune persistance de signe exploitable à 5 minutes ; les prix ne
   « continuent » ni ne « reviennent » de façon marquée au Mid à cet horizon.
3. L'asymétrie haussier/baissier de la volatilité n'existe pas comme
   fait stable : elle change de signe selon la période (deuxième
   réfutation indépendante après novembre 2026).
4. Le pic de volatilité de l'après-midi UTC (chevauchement
   Londres/New York) est la structure temporelle dominante.

## E. Candidates stratégiques

**Aucune.** La persistance de volatilité est un fait de régime, pas une
règle d'entrée : elle peut conditionner un futur moteur (quand ne pas
trader, comment dimensionner) mais ne prédit pas de direction. La
transformer en « stratégie » maintenant fabriquerait exactement ce que
la gouvernance interdit. Verdicts : faits de structure au niveau
N4 (signatures mesurées, segments multiples) ; aucun mécanisme N5,
aucune candidate H.

## F/G. Ce qui manque et demandes à l'agent externe

Données : une couverture par partitions *de durée comparable*
(échantillonnage par année civile plutôt que par indice) ; les coûts
d'exécution par époque (spreads déjà mesurés par partition : 1,7–4,4 bp
de moyenne au Mid, à intégrer avant toute lecture économique).
Demandes précises à un agent de recherche externe — uniquement si le
fondateur veut les poser : (1) méthodes de tests d'invariance
inter-régimes pour la persistance de volatilité sous dépendance
temporelle forte ; (2) littérature sur l'exploitation du *timing de
volatilité* sans prédiction directionnelle (dimensionnement
conditionnel) et ses conditions de validité après coûts.

## Prochaine expérience au meilleur potentiel discriminant

Re-échantillonner **par année civile** (2 partitions par an, 2012–2026,
durées comparables) et tester si la persistance de volatilité
conditionne la queue des épisodes ME-001 déjà catalogués — c'est le
pont le plus informatif entre cette découverte de structure et la seule
candidate économique vivante du programme, sans toucher à ses seuils
ni à sa collecte prospective.
