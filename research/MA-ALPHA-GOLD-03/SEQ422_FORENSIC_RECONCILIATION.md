# RÉCONCILIATION FORENSIQUE SEQ422

Re-vérification des deux mesures fondatrices de GOLD-02, depuis les scripts et artefacts :
1) **+0,17 bp** : confirmé comme rendement brut (Mid, avant coûts) du fade d'impulsion à
1 barre (+0,168 bp en moyenne, N-EXP-01). GOLD-02 le présentait correctement comme brut ; le
présent cycle ajoute : médiane +1,17 bp, 55,5 % de positifs, et profil de markout **plat après
la barre 1** (0,168 → 0,140 → 0,169 → 0,084) : c'est un rebond de microstructure (Bid-Ask
bounce contenu dans le Mid reconstruit), pas un retour à la moyenne lent. Rapporté au spread
médian (2,33 bp), le reflux moyen ne vaut que ~7 % de l'écart : même un fournisseur exécuté au
prix touché ne capterait pas « le spread » grâce à ce seul effet ; il capterait le spread **moins**
la sélection adverse, que nos données ne mesurent pas.
2) **+2 points de volatilité** : confirmé et robuste (N-EXP-03) : écart médian IV−RV suivante
+1,99 (chevauchant), +1,91 (non-chevauchant), +2,01 (sans les 10 plus grands sauts) ; mais la
médiane par période décroît : +2,73 (2010-15) → +1,62 (2016-17) → +0,65 (2018-19) : la prime se
comprime. Aucune erreur de construction décelée (annualisation √252, fenêtres suivantes, J-1).
Corrections de GOLD-02 déjà inscrites au seq421 (deux règles positives sur trois périodes, dont
une sous les coûts) : maintenues. Aucun holdout touché dans GOLD-02/03 (barsets ≤ 2019-12-16).
