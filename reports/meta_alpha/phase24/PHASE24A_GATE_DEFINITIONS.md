# PHASE 24-A — DÉFINITIONS GELÉES DES PERMISSIONS

**Directeur H4 (reproduction exacte 20-B)** : pour chaque décision (t_reintegration), dernière
barre H4 complète (`complete`) dont la fin est ≤ t_decision ; état EXPANSION si RANGE_BP de cette
barre ≥ Q90 des RANGE_BP des **250 barres précédentes** (barre courante exclue du dénominateur,
chauffe de 250 barres = NON_VALIDABLE). Timestamp de disponibilité : clôture de la barre.
Reproduction vérifiée ligne à ligne contre `phase20b_engine.regimes_h4()`.

**Directeur D1 (reproduction exacte 21-A)** : régime de la **dernière journée D1 certifiée
entièrement clôturée strictement avant la date de décision** ; D1_EXPANSION si RANGE_BP ≥ Q90 des
250 journées complètes précédentes (journée exclue de son propre calcul) ; chauffe ou journée non
certifiée = NON_VALIDABLE (339 événements). Une journée en cours n'autorise jamais sa propre
négociation.

**Horloge UTC** : `08:00 ≤ t_decision < 16:00` et même fenêtre pour l'entrée ; une décision avant
16:00 dont la première cotation admissible serait ≥ 16:00 = `ENTRY_OUTSIDE_ALLOWED_WINDOW`
(vérification tick réservée à la phase d'exécution ; ici l'horodatage d'entrée est assimilé à la
décision pour le comptage de faisabilité — limite documentée). Pas de liquidation forcée à 16:00.
Aucun créneau alternatif.

**Aucune fusion** : pas d'état `H4 OR D1` ni `H4 AND D1`. Les variantes étudiées sont
`CHAUFFEUR_H1_H4_GATE` (H4_TIME) et `CHAUFFEUR_H1_D1_GATE` (D1_TIME), séparément.

**Chauffeur (référence, non entraîné)** : événements H1 12-B, 5 variables gelées
(RATIO_REPLI_EXTENSION_A_TREINT, DUREE_EXTREME_VERS_TREINT_MIN, MFE_A_TREINT_BP,
NB_TOUCHES_P0_AVANT_TREINT, SESSION_REINTEGRATION), cible RESUMPTION inchangée, logistique M1
(9 paramètres avec indicatrices de session), seuil = probabilité majoritaire du train filtré
(méthode historique, à documenter avant tout examen d'évaluation dans une phase ultérieure).
