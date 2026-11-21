# ÉTAPE B — RAPPORT ÉCONOMIQUE P9-B : CASSURE CONFIRMÉE ET RETEST

**Source** : `CAMPAIGN_02_2_BREAKOUT_TIMELINE.csv`, instantanés RETEST
(cassure +5 bp puis retour au niveau), **n = 3 128** retests, 1 543
journées, ≈ 511 événements/an. Entrée examinée : clôture de la barre de
retest, dans le sens de la cassure, sortie à +60 min (Mid).

## Mesures du phénomène

- Délai cassure → retest : médiane **1 minute**.
- Encore au-delà du niveau à +60 min : **54,4 %** (fréquence publiée
  ANO-C1-002 : ~55 % — confirmée).
- Mais la **magnitude** signée fait défaut à la fréquence : position
  médiane à +15/+30 min +3,93/+3,76 bp au-delà du niveau, et espérance
  du gain momentum (position à +60 moins position au retest) :
  **−1,09 bp en moyenne, médiane −2,71 bp**. Le prix, revenu tester le
  niveau, se trouve en médiane *plus près ou au-delà en sens inverse*
  une heure plus tard : la persistance de position ne se convertit pas
  en progression depuis le prix du retest.
- Sensibilité : brut par ère −1,10 / −0,36 / −2,28 bp ; Londres −1,13,
  New York −1,07 bp. Négatif dans toutes les cellules.

## Économie (modèle commun)

| | Favorable | Central | Défavorable |
|---|---|---|---|
| Spread observé | 2,44 bp |||
| Coût total (bp) | 2,94 | 4,14 | 8,06 |
| **Espérance nette (bp)** | **−4,03** | **−5,23** | **−9,15** |

**Coût maximal supportable : −1,09 bp — négatif avant coûts.**

## Donnée manquante (consignée, non comblée par hypothèse)

Les excursions adverses *après le retest* ne sont pas stockées dans
les fichiers validés (positions +15/+30/+60 seulement) : un stop-loss
n'aurait pas pu être évalué proprement. Cette lacune est sans effet
sur le verdict, l'espérance à +60 étant déjà négative en Mid.

## Verdict P9-B : **ABANDONNER**

La fréquence de 55 % « encore au-delà » était un fait de position, pas
un gain depuis le prix d'entrée au retest. Ne pas supposer que les
retests sont des entrées exploitables : mesurés, ils ne le sont pas à
l'horizon descriptif gelé, et aucune optimisation d'horizon n'est
autorisée pour les sauver.
