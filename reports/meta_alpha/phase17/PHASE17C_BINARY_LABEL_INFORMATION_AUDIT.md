# PHASE 17-C — AUDIT D'INFORMATION DU LABEL BINAIRE `Y_ECON`

*Diagnostic sur artefacts committés 17-A/17-B uniquement. Aucun nouveau modèle, aucune régression sur le P&L continu, aucun entraînement.*

## 1. Ce que le label retient, ce qu'il détruit

`Y_ECON = 1{PL_S2 > 0}`. Par construction, le label ne retient que le **signe** du P&L.
L'indice eta2 du label (part de variance du P&L « entre classes ») est élevé (0,69 à 0,84)
mais **mécanique** : il reflète la séparation signe positif / signe négatif, pas une
information prédictive. L'information économiquement pertinente — l'**amplitude** — est
intégralement détruite à l'intérieur de chaque classe :

| Contrat / segment | Ecart-type PL positifs (bp) | Ecart-type PL negatifs (bp) | PL positif min -> max (bp) | PL negatif min -> max (bp) |
|---|---|---|---|---|
| B08 / APPRENTISSAGE | 28.7 | 16.1 | 0.03 -> 220.0 | -143.7 -> -0.05 |
| B08 / CALIBRATION | 18.6 | 12.1 | 0.58 -> 114.9 | -109.7 -> -0.39 |
| B08 / EVALUATION | 12.2 | 8.8 | 0.63 -> 67.1 | -56.0 -> -0.19 |
| B09 / APPRENTISSAGE | 27.8 | 24.6 | 0.03 -> 220.0 | -214.6 -> -0.05 |
| B09 / CALIBRATION | 19.2 | 16.7 | 0.58 -> 114.9 | -105.7 -> -0.39 |
| B09 / EVALUATION | 12.7 | 13.3 | 0.33 -> 67.1 | -65.9 -> -0.19 |

## 2. Exemples vérifiables (même label, P&L incomparables)

Evaluation B08 : `EV-e994263b...` label 1 avec **+0,63 bp** ; `EV-2b3938ec...` label 1
avec **+67,06 bp** — deux « succès » dont l'un vaut 106 fois l'autre. A l'inverse
`EV-d9f45de8...` label 0 avec **-0,19 bp** est économiquement quasi neutre mais classé
échec, au même titre que `EV-b458785f...` à **-55,99 bp**. En apprentissage, l'éventail
atteint +0,03 bp à +219,96 bp dans la seule classe positive. La décision économique au
seuil `P_BE` traite pourtant tous ces événements comme des payoffs constants G et L.

## 3. Le label est presque une fonction du mécanisme de sortie

Dans les trois segments et les deux contrats : **tout** `TP_FIRST` est positif, **tout**
`SL_FIRST` est négatif ; seule la sortie `VERTICAL_FIRST` est mixte. Le label binaire
revient donc essentiellement à prédire « TP avant SL », une course de barrières, sans
aucune représentation de l'amplitude réalisée ni du résultat des sorties verticales
(qui portent l'essentiel de l'ambiguïté : B08 évaluation, 46 positifs / 33 négatifs).

## 4. Conséquence

La cible binaire est **trop pauvre pour la décision visée** : la règle `q > L/(G+L)`
suppose des gains et pertes homogènes alors que, dans chaque classe, l'écart interquartile
des amplitudes atteint 8,5 à 25 bp et les extrêmes dépassent 100 bp en apprentissage.
Cela n'établit pas qu'une cible continue ferait mieux — aucun modèle continu n'a été
construit ni autorisé — mais cela établit que la représentation binaire + payoffs moyens
fixes ne peut pas représenter fidèlement l'espérance conditionnelle des événements.

## 5. Stabilité du label

La fréquence du label n'est pas stable entre segments (B08 : 35,4 % -> 43,7 % -> 46,1 % ;
B09 : 41,8 % -> 50,6 % -> 52,2 %), alors même que les amplitudes moyennes reculent
fortement (cf. `PHASE17C_PAYOFF_DISTRIBUTION.csv`). Le signe et l'amplitude dérivent
donc en sens opposés : un modèle de signe calibré sur 2010-2015 ne transporte ni la
fréquence ni l'échelle économique vers 2018-2020.
