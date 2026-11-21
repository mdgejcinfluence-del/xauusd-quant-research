# ÉTAPE B — RAPPORT ÉCONOMIQUE P9-C : FADE DES IMPULSIONS M5 DE Londres

**Source** : `CAMPAIGN_03_SNAPSHOTS_IMP.csv.gz` (IMP-M5, instantanés à
T0 et à +12 barres = +60 min), session de Londres **n = 16 169**
impulsions (≈ 1 500–2 000 événements/an, chevauchements d'épisodes
81 % — positions non indépendantes). Entrée examinée : clôture T0,
contre l'impulsion, sortie à +60 min (Mid). Référence Asie calculée à
l'identique (n = 14 018).

## Mesures du phénomène

- Amplitude initiale médiane (Londres) : 10,34 bp. Retracement complet
  sous 60 min : 57,9 % (fiche ANO-C3-001) — une **fréquence**.
- Espérance brute du fade à +60 min : **+0,79 bp en moyenne, médiane
  +1,53 bp** (Londres), contre −0,17 bp en Asie : l'avantage relatif de
  Londres existe en Mid, mais il vaut moins d'un dixième de l'amplitude
  initiale médiane. Par ère (Londres) : +0,98 / +0,73 / +0,60 bp —
  positif partout, décroissant, et partout minuscule.

## Économie (modèle commun)

| | Favorable | Central | Défavorable |
|---|---|---|---|
| Spread observé à T0 | 2,27 bp |||
| Coût total (bp) | 2,77 | 3,97 | 7,80 |
| **Espérance nette (bp)** | **−1,97** | **−3,17** | **−7,01** |

**Coût maximal supportable : +0,79 bp**, inférieur au seul spread
observé (2,27 bp). Même à commission et slippage nuls, la candidate ne
couvre pas l'écart Bid/Ask médian de ses propres événements.

## Verdict P9-C : **ABANDONNER** (conversion directe)

La confusion à éviter est exactement celle que l'ordre signalait :
57,9 % de retracements complets n'impliquent pas une espérance
positive après coûts, car le fade encaisse les continuations
(42,1 % des cas, excursions adverses pleines) et ne gagne en moyenne
que 0,79 bp en Mid. Aucune optimisation (cible de retracement, stop,
filtre d'amplitude) n'a été tentée pour la sauver : ce serait de la
construction de stratégie, hors autorisation. La fiche reste J1
descriptive ; l'écart Londres/Asie demeure un fait de cartographie.
