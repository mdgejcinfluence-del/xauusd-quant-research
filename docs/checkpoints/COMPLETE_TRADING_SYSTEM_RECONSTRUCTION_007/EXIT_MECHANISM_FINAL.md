# CTRS-007 — MÉCANISME DE CLÔTURE FINAL

## Étapes et horloges

- **Horloge 1 (décision)** : non observable directement.
- **Horloge 2 (transmission)** : non observable (aucun journal).
- **Horloge 3 (exécution)** : seule observable — timestamps des clôtures.
  Intervalles inter-ticks autour des clôtures : 0,05–0,25 s (médiane
  0,05–0,10 s) : toute latence décision→exécution inférieure à ~0,25 s
  est indiscernable de zéro, et les trois horloges **ne sont pas
  séparables** avec le corpus actuel (pas de Bid/Ask HFM réel, pas de
  logs). Les écarts de 19–246 s des premiers passages ne peuvent pas
  être de la latence : ils exigent un mécanisme de décision différée.

## État final des familles

- Réfutées : premiers passages (PWA, momentum, décélération,
  retracement, seuil +3 bp) ; persistance unique (intersection vide,
  35 combinaisons) ; cadence fixe ancrée > 1 s ; épuisement au sommet.
- Signature pré-clôture 5/5 : PnL en hausse 300 s, ΔPnL 30 s +1,6 à
  +7,2 bp, prix à −0,2/−2,2 bp du sommet local 300 s (conséquence
  géométrique, pas déclencheur) ; C clôture marginale à −0,25 bp.
- Restent équivalentes : cadence à phase libre, condition hybride,
  variable hors trajectoire Mid. Moteur de recherche : EMI-006
  `EXIT_MECHANISM_ENGINE.py` (familles P/C/H/E/U ; U n'exécute jamais).
- Rapides et récupérations : même famille compatible ; aucune règle de
  capture séparée démontrable (D : seuil +3 bp à 0,4 s, n=1).
