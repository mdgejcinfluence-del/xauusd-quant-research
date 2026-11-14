# BASE DE CONNAISSANCES PHASE 2 — phénomènes certifiés (source unique des justifications)

Toute hypothèse future doit citer un identifiant K de cette base. Aucun phénomène
hors de cette base ne peut justifier une hypothèse. Sources entre parenthèses.

- **K1 Structure des cotations** : tick = cotation Bid/Ask native Dukascopy, pas une
  transaction; mid=(bid+ask)/2 et spread=ask-bid reconstruits avec écart max 0,0 sur
  348 partitions (GATE_PHASE2_MESURES.md). Volumes bid/ask = UNAVAILABLE comme volume réel.
- **K2 Spread** : spread_rel moyen pondéré corpus ≈ 2,09 bp; seuils IS mesurés
  (P3-001): q20=1,83 bp, q40=2,05, q60=2,29, q80=2,69. Le spread est le coût dominant
  de tout aller-retour (P4-001: effet mid +0,3 bp contre -2,0 à -2,9 bp nets).
- **K3 Volatilité tick** : écart-type du rendement tick médian par partition ≈ 3,85e-5;
  ROLL_STD_100 IS: q20=1,32e-5 ... q80=2,72e-5 (seuils P3-001).
- **K4 Activité/rythme** : UPDATE_INTENSITY et INTERARRIVAL_MEAN certifiés; inter-arrivée
  moyenne sur 100 ticks IS: q20=0,28 s ... (seuils P3-001, fichier résultats).
- **K5 Trous temporels** : 30 804 trous > 60 s (fermetures; max ≈ 3,2 j): aucune fenêtre
  ne doit les traverser silencieusement (GATE_PHASE2_MESURES.md).
- **K6 Schéma** : 2 signatures bornées (001-294 / 295-348), lecture par nom obligatoire
  (RAPPORT_INVENTAIRE_348_EXHAUSTIF.md).
- **K7 Pattern conditionnel IS (exploratoire, NON qualifié)** : rendements mid futurs
  légèrement positifs après quintiles élevés de volatilité/spread/intensité
  (9/15 contrastes FDR en P3-001), amplitude ≈ 0,1-0,5 bp << spread.
- **K8 Leçon P4-001 (REJETÉ, immuable)** : transformé en règle longue systématique
  Bid/Ask, ce pattern perd -2,0 à -2,9 bp nets, IS et OOS, IC bootstrap entièrement
  négatifs. Filtre permanent: aucun candidat dont l'effet mid attendu n'excède pas
  nettement le spread ne doit passer en P4.
- **K9 Splits** : IS 2010-01-04->2020-01-20 (60%), OOS ->2023-05-31 (20%), Holdout
  scellé (20% final). Purge >= 1 h (= plus long label).
- **K10 Variables certifiées** : RET_H (label), ROLL_STD_MID, ROLL_RANGE_MID,
  UPDATE_INTENSITY, INTERARRIVAL_MEAN + base. Bloquées avec motifs: ZSCORE_ROBUST,
  SPREAD_REGIME, REGIME_CLASS, SUBPERIODE (sessions non documentées), MFE/MAE.
