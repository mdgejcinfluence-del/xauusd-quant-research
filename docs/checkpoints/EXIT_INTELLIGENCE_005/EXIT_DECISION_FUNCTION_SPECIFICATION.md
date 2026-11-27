# FONCTION DE DÉCISION DE SORTIE — SPÉCIFICATION

Forme de recherche EXIT_t = f(PNL, PWA, dPNL, d2PNL, V, sigma, T, N, E).
Résultats d'identification : aucun premier passage d'une fonction simple de ces
variables ne coïncide avec les clôtures (toutes trop précoces de 19–246 s, ou
absentes chez C). La famille compatible minimale ajoute une **composante de
persistance/confirmation** : l'état favorable doit se maintenir, ou être
réévalué après un délai d'état, avant liquidation — paramètres non identifiables
sur 5 clôtures (intervalles ouverts). Variables sans effet identifiable :
sigma, T, N au-delà de leur rôle d'état. Spécification livrée comme famille
paramétrique bornée, pas comme règle ponctuelle.
