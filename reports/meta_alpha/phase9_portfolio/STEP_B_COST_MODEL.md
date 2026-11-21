# PHASE 9 ÉTAPE B — MODÈLE COMMUN DE COÛTS

**Nature des chiffres : espérances brutes calculées sur prix Mid
(fichiers d'événements validés des campagnes 1–5) — ce ne sont pas des
preuves de remplissage réel. Aucun backtest stratégique n'a été réalisé.**

## Coûts OBSERVÉS (corpus IS tick Bid/Ask)

- **Spread à l'événement** : médiane du spread coté (bp) de la barre de
  l'événement, stockée par les moteurs des campagnes 1–3 (colonnes
  `spread_bp` / `spread_median_bp`). Valeurs par candidate dans chaque
  rapport (2,25–2,44 bp selon la candidate). Aller-retour : entrer et
  sortir paient chacun un demi-spread vis-à-vis du Mid, soit **un spread
  complet par transaction** — compté une seule fois, jamais deux.
- Référence indépendante : ANO-C2-013 (spread médian après ouverture de
  Londres : 2,40 bp en 2010–13 → 1,87 bp en 2017–20).

## Coûts HYPOTHÉTIQUES (jamais observés dans le corpus, jamais présentés comme réels)

Trois scénarios gelés pour l'étape B, identiques pour toutes les
candidates (aller-retour, en bp) :

| Scénario | Spread | Commission | Slippage (latence incluse) | Total hors spread |
|---|---|---|---|---|
| Favorable | ×1,0 observé | 0,0 | 0,5 | 0,5 |
| Central | ×1,0 observé | 0,7 | 1,0 | 1,7 |
| Défavorable | ×1,5 observé | 1,4 | 3,0 | 4,4 |

Swap/financement : **0 dans les trois scénarios** — toutes les
positions examinées durent ≤ 60 minutes et se clôturent en intraday ;
si une règle future devait tenir une position la nuit, le swap devrait
être documenté avant toute estimation. Exécution des stops et
remplissages partiels : non modélisés (données absentes) ; le scénario
défavorable (spread élargi ×1,5, slippage 3,0 bp) en est le proxy
déclaré, pas une mesure.

## Définitions

Espérance brute (Mid) ; coût total = spread ajusté + commission +
slippage ; **espérance nette = brute − coût total** ; **coût maximal
supportable = espérance brute** (au-delà, la candidate perd de l'argent
avant même tout autre frais) ; marge de sécurité = espérance nette du
scénario central. Sensibilité : par ère et par session quand les
fichiers la portent. Fréquences : événements par an sur le périmètre,
**chevauchements inclus** — ce ne sont pas des positions indépendantes.
