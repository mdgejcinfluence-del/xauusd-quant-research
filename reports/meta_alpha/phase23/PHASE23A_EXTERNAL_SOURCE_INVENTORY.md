# PHASE 23-A — INVENTAIRE DES SOURCES EXTERNES XAU/USD

Statut : `EXPLORATORY_RESEARCH_DESIGN`. Audit documentaire uniquement : aucune extraction massive,
aucun modèle, aucun P&L, budget 0 FCFA. Holdout 2020-2026 fermé. Les mêmes événements XAU/USD
2010-2020 ayant déjà servi aux phases 20-22, toute association future restera post-hoc.

## Résumé par famille

| Famille | Source principale | Granularité | Horodatage de disponibilité | Verdict famille |
|---|---|---|---|---|
| A Dollar | FRED H.10 (DTWEXBGS, DEXUSEU) | quotidienne | publication J+1 ouvré (~16:15 ET), ALFRED | `HISTORICAL_TIMESTAMP_LIMITATION` |
| B Taux US | FRED H.15 (DGS2, DGS10, DFII10) | quotidienne | publication J+1 ouvré, ALFRED (vintages) | `HISTORICAL_TIMESTAMP_LIMITATION` |
| C Macro | BLS / BEA / Federal Reserve (calendriers + valeurs) | événementielle | heure officielle de publication documentée | `PARTIALLY_AVAILABLE` |
| C Consensus/surprise | fournisseurs commerciaux | événementielle | version contemporaine non libre | `SOURCE_OR_LICENSE_BLOCKED` |
| D Futures or GC | CME Group | tick/quotidienne | données historiques licenciées payantes | `SOURCE_OR_LICENSE_BLOCKED` |
| E Calendrier | NYSE / CME / Fed (public) | quotidienne/événementielle | connu à l'avance (programmé) | `CAUSAL_HISTORY_VERIFIABLE` |

## Faits vérifiés

- Les taux de change quotidiens H.10 (dont l'indice dollar large DTWEXBGS et EUR/USD DEXUSEU) sont
  publiés avec un décalage d'un jour ouvré ; FRED/ALFRED conserve les dates de vintage, ce qui permet
  de reconstruire ce qui était **connu** à une date donnée, mais uniquement à fréquence quotidienne
  et pour le lendemain — jamais intrajournalier le jour même.
- Les rendements Treasury quotidiens (H.15 : DGS2, DGS10 ; réel 10 ans DFII10) suivent le même régime :
  valeur du jour J disponible J+1, révisions tracées par ALFRED.
- Les heures de publication CPI/PCE/NFP (08:30 ET en règle générale) et FOMC (14:00 ET) sont publiques
  et archivées ; les valeurs initiales sont récupérables via ALFRED (première vintage), mais le
  **consensus historique contemporain** n'est pas librement disponible avec provenance vérifiable :
  toute « surprise » reconstruite a posteriori est interdite par le contrat de phase.
- Les données historiques CME (GC : prix, volume, open interest intrajournaliers) sont licenciées et
  tarifées (grille publique CME, historique par DataMine) : incompatibles avec un budget de 0 FCFA.
  Les flux « gratuits » sont différés (≥10 min) et sans historique tick libre vérifiable. Le volume GC
  ne doit jamais être assimilé à un volume spot XAU/USD.
- Les calendriers de jours fériés US, d'échéances futures et de publications sont publics et connus
  à l'avance : seuls candidats pleinement causaux sans risque de fuite, mais ce sont des variables
  de régime, pas des signaux directionnels nouveaux (chevauchements de séances et créneaux déjà
  cartographiés en 20-A/21-C — risque de doublon documenté).

## Risque de fuite temporelle (règle de phase)

Toute valeur quotidienne FRED du jour J utilisée pour « expliquer » un mouvement XAU/USD du jour J
constitue une fuite : elle n'était publiée que le jour J+1. Les usages causaux admissibles sont :
(i) valeur de J-1 ou antérieure connue avant l'ouverture de J ; (ii) heures d'événements publics
connues à l'avance ; (iii) vintages ALFRED pour les valeurs d'événements, à partir de l'heure de
publication exacte.
