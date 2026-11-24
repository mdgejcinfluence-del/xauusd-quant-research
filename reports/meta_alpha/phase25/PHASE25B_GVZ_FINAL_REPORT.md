# PHASE 25-B — GVZ (volatilité implicite J-1) : RAPPORT

Extraction : GVZCLS via deux miroirs GitHub indépendants de la série FRED/CBOE, **2 706
observations communes, écart maximal 0,0** (2010-2019 couvert). Affectation causale J-1 strict :
dernière clôture GVZ strictement antérieure à la date de décision. Terciles fixés sur la
calibration 2016-2017 (frontières ≈ 13,9 / 17,9), appliqués sans modification à 2018-2019.

Résultat (espérance S2 par tercile) : calibration **−2,87 / −4,45 / −4,01 bp** ; évaluation
−4,62 / +1,34 / −0,21 bp. La fréquence de réalisation ne croît pas avec le GVZ (0,60 / 0,59 /
0,56 en calibration). Le mécanisme espéré se vérifie en partie sur les amplitudes : G croît avec
le GVZ (13,2 → 22,1 en calibration) et le MAE médian aussi (23,7 → 42,8 bp) — mais **L croît
autant** (26,7 → 37,1), donc l'espérance ne se sépare jamais. Le régime de volatilité implicite
échelonne la taille des gains *et* des pertes ; il ne dit pas qui gagne.

Verdict GVZ : information d'amplitude confirmée, **aucune information économique séparable** sur
cette population. Aucun filtre n'est proposé.
