# CAMPAGNE 7 — DIAGNOSTICS DE COUVERTURE ET ÉVÉNEMENTS CENSURÉS

- Extraction : run corrigé (voir incidents) complet, 282/282 partitions,
  3 540 993 barres M1, 3 097 journées présentes ; validation temporelle
  synthétique verte en CI avant calcul (12/12 au run 1, 13/13 au run 2
  après ajout du test de simultanéité) ; chaîne vérifiée avant calcul.
- Épisodes par grille (bruts) : G50 2 359, P50 2 420, R100 1 290,
  P100 1 325, R10 9 958, P10 11 841.
- Terminaux toutes grilles : FRANCHISSEMENT 14 520 ; REJET 1 611 ;
  SAUT 306 (exclus du primaire, publiés) ; SANS_EFFET 99 ;
  CENSURE_JOUR 12 657 (fin de journée UTC avant résolution, publiés
  par grille : G50 1 029, P50 1 048, R100 577, P100 602, R10 4 347,
  P10 5 054) ; SIMULTANÉS 95 (après correctif ; voir incidents).
- Approches résolues (dénominateurs I-01/I-04) : G50 1 302 (745
  grappes-journées), P50 1 338 (798), R100 691 (415), R10 5 482 (2 101).
  Touches résolues (I-02) : G50 549, P50 632. Franchissements à suivi
  complet (I-03) : G50 1 114, P50 1 097.
- Aucun observable de suivi n'est calculé sur fenêtre incomplète
  (suivi_complet exigé pour I-03 et le maintien) ; aucun épisode censuré
  n'entre dans un dénominateur primaire.
- Fichiers : `CAMPAIGN_07_EPISODES.csv.gz` (tous épisodes, toutes
  grilles, statuts complets), `C7_COVERAGE.json`,
  `CAMPAIGN_07_DETAILS.json` (populations, taux bruts, compositions).
