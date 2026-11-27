# IDENTIFICATION INVERSE DES PARAMÈTRES

Problème posé : retrouver seuils d'entrée, de renforcement, de sortie et de
sizing à partir de 12 transactions. Résultat d'identification : l'ensemble des
paramètres compatibles est un **ensemble**, pas un point — par exemple tout seuil
de recul de 3e position dans [−6,6 ; −4,7] bp reproduit les 3 renforcements
observés, et tout seuil de sortie au voisinage du PWA dans une bande large
reproduit 4/5 clôtures (C borne la bande sous 0). Les méthodes lourdes (états
cachés, programmation génétique) choisiraient arbitrairement dans ces ensembles :
elles sont écartées par discipline, pas par incapacité. Paramètres estimables
sous conditions : recul de renforcement (intervalle ci-dessus, si la règle est
un seuil fixe — non prouvé) ; délai d'amorçage (16–40 s observés).
