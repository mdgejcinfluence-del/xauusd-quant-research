# MODULE I — ECONOMIC VALIDATION & PORTFOLIO ENGINE (conception)

## Responsabilité

Décider si un moteur indépendant produit un avantage net réel, puis
agréger les sources validées en portefeuille de rendements
effectivement différents.

## Validation économique

Coûts complets comptés une fois (spread réel du lieu d'exécution,
commission, slippage mesuré ou scénarios déclarés, financement) ;
mesures : espérance nette, PF, drawdown, expected shortfall, séries de
pertes, durée et exposition, rendement par unité de capital et de
risque ; stabilité par période et par régime ; sensibilité aux coûts
(précédent : scénarios S0–S3 de BACKTEST-2026-001) ; critères de
succès/échec **pré-déclarés** avant l'ouverture du segment de
validation (précédent : protocole prospectif ME-001.4, seq486).
Un positif sur les données de construction n'est jamais une validation.

## Portefeuille

Indépendance économique avant tout : corrélation des rendements,
pertes simultanées, régimes communs, queues partagées (deux moteurs
acheteurs d'or en excursion adverse portent le même risque, quels que
soient leurs indicateurs). Allocation par budget de risque et
capacité, réexamen à chaque nouveau modèle validé. État actuel du
portefeuille : **vide** — aucun modèle VALIDATED ; ME-001 est la seule
candidate en cours d'épreuve, ME-002 et ME-003 sont des réfutations
documentées qui bornent l'espace.

## Sorties

`ValidationVerdict` par moteur (VALIDATION RÉUSSIE / PARTIELLEMENT
FAVORABLE / NON CONCLUANT / RÉFUTÉE / DONNÉES INSUFFISANTES) et, à
terme, une allocation de portefeuille traçable au registre.
