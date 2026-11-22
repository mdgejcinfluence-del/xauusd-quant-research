# PHASE 17-D — STABILITÉ DE RÉGIME : PAYOFF EN bp CONTRE PAYOFF EN R

*Statistiques descriptives agrégées à partir des artefacts gelés 17-B (labels, ATR à la décision, prix d'entrée) — voir `PHASE17D_PAYOFF_DISTRIBUTION_AUDIT.csv`. Aucune frontière de régime créée, aucun seuil d'ATR recherché, aucun sous-groupe formé. Valeurs extrêmes conservées, aucune winsorisation.*

## 1. En bp : l'échelle dérive fortement
Écart-type du P&L S2, B08 : 41,0 (apprentissage) → 33,6 (calibration) → 26,0 bp (évaluation) ; B09 : 46,7 → 37,1 → 29,2 bp. C'est la baisse d'environ 40 % des amplitudes G/L diagnostiquée en 17-C (MEC-3), parallèle à la dérive d'`ATR14_H1` (SMD −0,66 en évaluation). Corrélation ATR–|P&L| en bp : 0,74/0,65/0,56 (B08) et 0,64/0,53/0,38 (B09) : l'amplitude en bp est en grande partie une affaire d'échelle de volatilité.

## 2. En R : l'échelle se stabilise, le niveau reste à vérifier
Écart-type de R, B08 : **1,13 / 1,18 / 1,17** ; B09 : **0,88 / 0,89 / 0,89** — quasi constant entre segments, là où l'écart-type en bp chute de plus d'un tiers. Corrélation ATR–|R| proche de zéro (−0,05 à −0,19) : la normalisation par le risque initial retire l'essentiel de la dépendance d'échelle. La concentration extrême recule aussi (part du P&L absolu portée par les 5 % extrêmes : ~14 % en bp contre ~7 % en R en apprentissage), et la kurtosis en R est négative (distribution bornée par les barrières, environ −1,5 à −2,2 en R contre des valeurs positives en bp d'apprentissage) — la moyenne conditionnelle est donc moins exposée aux queues en R qu'en bp, sans que les extrêmes soient supprimés (min −2,17 R, max +2,64 R : franchissements de barrière et gaps conservés).

## 3. Ce que la normalisation ne règle pas
Les moyennes de R diffèrent encore entre segments (B08 : −0,21 / −0,00 / +0,00 ; B09 : −0,13 / +0,02 / −0,00) et les médianes restent très négatives pour B08 (−1,05 / −0,51 / −0,50) : la normalisation stabilise la dispersion, pas nécessairement le niveau ni la forme (asymétrie B08 persistante). La stabilité des coefficients et des erreurs devra être mesurée en 17-E sur calibration puis évaluation, sans aucune réestimation intermédiaire.

## 4. Conclusion de conception
La représentation R satisfait l'objectif fixé : comparer des payoffs entre régimes de volatilité sans inventer de frontières de régime. Elle ne préjuge ni d'un pouvoir prédictif des sept variables sur R, ni d'une espérance positive. Aucun entraînement n'est effectué dans la présente phase.
