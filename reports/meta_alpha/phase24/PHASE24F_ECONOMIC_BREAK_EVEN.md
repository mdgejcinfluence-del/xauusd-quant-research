# PHASE 24-F — FRONTIÈRE ÉCONOMIQUE DE POINT MORT (calibration 2016-2017 uniquement)

Sur les 1 372 événements de calibration avec sortie complète : gain moyen S2 des labels réalisés
G = **+18,01 bp** ; perte moyenne absolue des non-réalisés L = **34,05 bp**. Point mort :
`P_BE = L / (G + L) = 0,654`. Il faudrait donc une probabilité de réalisation d'au moins 65,4 %
pour que l'espérance, à gains et pertes moyens constants, soit nulle.

Trois faits empêchent d'en faire une règle :

1. Le score prédit dépasse rarement ce niveau : la quasi-totalité de la masse sélectionnée se
   situe entre 0,56 et 0,75, et le score maximal observé est ≈ 0,76.
2. Même là où la fréquence réelle dépasse P_BE — classe [0,70 ; 0,75) : fréquence 0,770 en
   calibration — le P&L moyen reste **négatif (−4,36 bp)**. Les G et L globaux ne se transportent
   pas à l'intérieur des classes : dans les classes à haut score, les gains réalisés sont plus
   petits et les pertes restent entières. La frontière fondée sur les moyennes globales est donc
   infirmée par la stratification elle-même.
3. La référence descriptive 2018-2019 (P_BE = 71,45 %, calculée sur +12,50/−31,29) n'a servi à
   aucune sélection, conformément à l'interdiction ; elle illustre l'instabilité de G et L entre
   périodes (G passe de 18,0 à 12,5 bp).

`ECONOMIC_BREAK_EVEN_NOT_ESTIMABLE` n'est pas retenu (les effectifs de calibration suffisent à
calculer la frontière) ; le verdict pertinent est `M15_ECONOMIC_BREAK_EVEN_NOT_REACHED` : aucune
classe évaluable n'atteint une espérance positive et stable.
