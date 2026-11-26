# FAISABILITÉ DE LA FOURNITURE DE LIQUIDITÉ — BORNES MESURÉES (P-EXP-01)

Protocole préenregistré (seq425) : limite passive fade posée au bord Bid/Ask à la clôture
d'impulsion, fenêtre de remplissage 4 barres, sortie Mid à +2 barres. Borne OPTIMISTE (fill dès
le touché, taux de remplissage 91,7 %) : **−0,43 bp en moyenne avant même le spread de sortie**
(−0,47/−0,22/−0,50 par période). Borne PRUDENTE (fill seulement si traversée ≥ 1 bp, 87,0 %) :
**−1,48 bp**. Le preneur de référence : −2,40 bp. Lecture : passer de preneur à fournisseur
récupère ≈ 2 bp, mais la sélection adverse (on est rempli quand le prix continue) coûte ≈ 2 bp
de plus que le reflux ne rapporte : l'activité « fournir contre les impulsions » est perdante
dans toutes les bornes honnêtes. Ce qui resterait à tester chez un vrai fournisseur — retrait
aux annonces, cotation hors impulsion, gestion d'inventaire — exige fills et file réels :
non démontré, et non simulable avec notre corpus. Sur CFD de détail, l'« ordre limite » est
exécuté par le courtier contre son propre prix : ce n'est pas un accès au carnet COMEX.
