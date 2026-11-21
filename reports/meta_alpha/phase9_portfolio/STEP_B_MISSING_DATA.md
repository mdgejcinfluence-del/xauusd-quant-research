# PHASE 9 ÉTAPE B — REGISTRE DES DONNÉES MANQUANTES ET HYPOTHÈSES

## Hypothèses (toutes étiquetées, aucune présentée comme observée)

| # | Hypothèse | Valeurs | Portée |
|---|---|---|---|
| H1 | Commission aller-retour | 0,0 / 0,7 / 1,4 bp (favorable/central/défavorable) | aucun contrat de courtage documenté dans le programme |
| H2 | Slippage aller-retour, latence incluse | 0,5 / 1,0 / 3,0 bp | aucun carnet d'ordres ni journal d'exécution disponible |
| H3 | Élargissement du spread en conditions défavorables | ×1,5 le spread observé | proxy déclaré pour stops/marchés rapides, pas une mesure |
| H4 | Swap/financement | 0 (positions ≤ 60 min intraday) | deviendrait obligatoire si une règle tenait la nuit |
| H5 | Sorties aux prix Mid des fichiers d'événements (niveau touché, clôture +60) | convention de mesure | les remplissages réels (file d'attente, partiels) sont inconnus |
| H6 | Spread à l'atteinte (P9-E) approché par le spread EV2 campagne 1 | 2,28 bp médian | la campagne 5 n'a pas stocké le spread par atteinte |
| H7 | Fréquences annuelles = événements/an, chevauchements inclus | descriptif | les positions simultanées (ex. 81 % en IMP-M5) ne sont pas indépendantes |

## Données manquantes (constatées, non comblées)

| # | Manque | Candidate | Effet sur l'audit |
|---|---|---|---|
| M1 | Excursions adverses **après retest** (seules positions +15/+30/+60 stockées) | P9-B | stop-loss non évaluable ; sans effet sur le verdict (brut +60 < 0) |
| M2 | Spread à l'événement des consolidations C3 | P9-D | coût du filtre non chiffrable directement |
| M3 | Spread par atteinte en campagne 5 | P9-E | proxy H6 utilisé et étiqueté |
| M4 | Commissions, swaps, slippage réels d'un courtier | toutes | scénarios H1–H3 ; tout passage en E1 exigerait des relevés réels |
| M5 | Bid/Ask au moment de l'entrée/sortie trade par trade (seuls spreads de barre médians sont stockés) | toutes | les espérances restent des bornes Mid, favorables par construction |
| M6 | Latence et profondeur du carnet aux heures d'événement | toutes | incluses forfaitairement dans H2, non mesurées |

## Ce que l'étape B n'a pas fait (par autorisation)

Aucun backtest stratégique, aucune optimisation de paramètre (horizon,
cible, stop, filtre), aucun `challenge_sim`, aucun accès au holdout,
aucune promotion J2/J3/E1/E2. Les espérances sont des mesures
descriptives sur fichiers d'événements validés, moins un modèle de
coûts explicite.
