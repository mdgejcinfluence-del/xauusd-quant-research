# CAMPAGNE 6 — DIAGNOSTICS DE COUVERTURE ET DE QUALITÉ

- Extraction (run CI unique) : 282/282 partitions, 3 540 993 barres M1,
  3 097 journées présentes. Validation temporelle synthétique 15/15
  verte en CI avant calcul ; chaîne du registre vérifiée avant calcul.
- Statuts de forme (priorité V1.2.2) : ELIGIBLE 2 772 ; CENSUREE_FORME
  325 ; PLATE OBSERVÉE 0 ; INDÉTERMINÉE — DISCONTINUITÉS 0 ; DOMINÉE
  PAR LES DISCONTINUITÉS OBSERVÉES 0 ; INCOHÉRENTE 0.
- Éligibles par ère : 990 (2010–13, sur 1 245 présentes), 884
  (2014–16, sur 932), 898 (2017–20, sur 920). Taux de couverture
  cumulée médian des éligibles : 99,78 % (2010–13), 100 % ensuite.
- Règle B15 (option A, fenêtre UTC fixe) par ère — FRONTIÈRE_PROGRAMMÉE /
  HALTE_INDÉTERMINÉE / AUCUN_TROU : 2010–13 : 399 / 680 / 166 ;
  2014–16 : 573 / 94 / 265 ; 2017–20 : 589 / 76 / 255. La forte part de
  HALTE_INDÉTERMINÉE en 2010–13 explique l'essentiel des 255 censures
  de cette ère (aucune exemption en cas de doute, règle gelée appliquée
  sans assouplissement).
- Statuts généraux (hérités, jamais preuve d'absence) : COMPLETE 395,
  PARTIELLE 2 177, EXCLUE 525.
- Fichiers publiés : `CAMPAIGN_06_DAYS.csv` (toutes les journées,
  composantes complètes : Δ_seg, Δ_jour, L, A, D, ρ, ER, S, PD, τ,
  ER1/ER2/AS, segments, trous, couvertures), `CAMPAIGN_06_DAY_COVERAGE.csv`,
  `C6_COVERAGE.json`, `CAMPAIGN_06_PAIRES_C6_01.csv` (2 147 paires).
