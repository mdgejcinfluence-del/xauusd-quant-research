# PHASE 24-C — STABILITÉ TEMPORELLE (diagnostics, jamais des validations)

- TIME_ONLY : Brier 0,213 (calibration 2016-2017) puis 0,222 (évaluation 2018-2019) ; AUC 0,706
  puis 0,712 ; pentes de calibration 1,37 puis 1,60 (probabilités trop prudentes, pas d'inversion).
- H4_TIME : Brier 0,200 puis 0,210 ; AUC 0,744 sur les deux segments ; pentes 1,99 puis 1,66.
- D1_TIME : Brier 0,237 puis 0,227 ; AUC 0,629 puis 0,712 — segment de calibration plus faible,
  rapporté sans correction.
Aucune inversion négative de calibration ; les performances ne s'effondrent pas entre segments,
mais ces découpages internes ne constituent pas des validations indépendantes.
