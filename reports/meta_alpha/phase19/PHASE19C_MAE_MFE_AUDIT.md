# PHASE 19-C — AUDIT MAE / MFE ET RISQUE DE DURÉE

Excursions calculées sur le prix de liquidation tick (Bid LONG / Ask SHORT) entre l'entrée commune et la liquidation de chaque horizon (prix, dollars) :

| Mesure | H8 (n=442) | H16 (n=437) |
|---|---|---|
| MAE médian | −2,78 | −3,64 |
| MFE médian | +3,17 | +3,80 |
| Temps médian passé en perte | 4,81 h | 9,78 h |
| Part des événements avec MAE < −50 dollars | 0,2 % | 0,2 % |

Lecture : prolonger la détention approfondit modérément l'excursion défavorable médiane et **double le temps médian passé en perte**, pour un gain final non démontré (rapport final). Les pertes maximales finales sont comparables (−221,6 bp contre −215,2 bp en S2) : le risque supplémentaire de H16 est principalement un risque de **durée d'exposition** (nuits, fermetures, voir audit des délais), pas une explosion des extrêmes sur cette cohorte. Aucune position ne franchit de barrière : il n'y a ni TP ni SL dans cette expérience.
