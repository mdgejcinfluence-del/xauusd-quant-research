# PHASE 12-A — PROCÈS-VERBAL DE GEL DÉFINITIF

**Date : 2026-11-13. Gel décidé par le responsable (ordre officiel de
gel Phase 12-A). Ce gel ne vaut pas autorisation d'exécution de la
Phase 12-B.**

## Documents gelés (SHA-256 complets, revérifiés avant gel)

- `PHASE12A_PREDICTABILITY_PROTOCOL.md` :
  `580c39b114397143e6eaa7fc63e529afb79ad61ec3f9cbd843116d3484a4e99e`
- `PHASE12A_FEATURE_DICTIONARY.csv` :
  `933feff779e2f1a54ef1f538610a8fb2a481b48f702b72c6eedcf7f3d1df2519`
- `PHASE12A_PREREGISTRATION.json` :
  `005d1e69752141234132588e74d8d8eef699cedc31abb685628f0f77cd8f8bf2`
- `PHASE12A_FEASIBILITY_REPORT.md` :
  `6e8c26181639987085da703463cd131969fbd4bf32b57de6a703e4e9e8c367cb`

## Rapport de vérification documentaire (avant gel)

- Les quatre empreintes recalculées sont **identiques à l'octet près**
  à celles enregistrées au checkpoint seq309 (préfixe annoncé du
  protocole : `580c39b1`, confirmé sur le hash complet).
- Commit de conception `b22b9d3` vérifié distant avant gel ;
  continuité documentaire depuis seq307 (11-C.1) assurée par la
  chaîne (seq308 mission, seq309 préenregistrement).
- Cohérence interne des livrables revérifiée : hypothèses H12-A à
  H12-F, cible RESUMPTION, variables et statuts d'extraction,
  séparations et métriques concordent entre le protocole, le
  dictionnaire, le préenregistrement JSON et le rapport de
  faisabilité.
- Aucune modification du contenu scientifique pendant le gel ;
  aucun accès aux données M1, aucune extraction, aucun calcul
  prédictif, aucun accès au holdout pendant l'opération.

## Décisions méthodologiques conservées sans modification

Instant de décision `t_reintegration` ; interdiction de toute
variable postérieure à cet instant ; exclusion des mesures de
fenêtre complète de 8 bougies comme variables ; exclusion de
`archetype` et de tout dérivé de la cible ; cinq variables candidates
à extraction bornée en Phase 12-B ; comparaison M0 (fréquence du
segment d'apprentissage) contre régression logistique simple sans
réglage ; analyses H1 et H4 séparées ; séparation chronologique par
grappe entière (apprentissage 2010–2015, calibration 2016–2017,
évaluation 2018–2020) avec purge des chevauchements ; métriques
principales Brier score et log-loss contre M0, calibration et AUC en
diagnostics jamais probants à eux seuls ; critères d'insuffisance
préenregistrés (évaluation < 100 étiquetés ou minorité < 50 →
NON ÉVALUABLE par famille) ; risques de sélection historiques
reconnus ; qualification obligatoire de toute évaluation future :
**`HISTORIQUEMENT ÉVALUÉE — NON INDÉPENDAMMENT CONFIRMÉE`**.
Effectifs de faisabilité et limites inchangés (H1 : 2 032 reprises /
660 absences sur réintégrés complets ; H4 : 539 / 90, famille à
risque de NON ÉVALUABLE).

## Traçabilité

seq307 : réconciliation 11-C.1 ; seq308 : mission 12-A ; seq309 :
préenregistrement (verdict PROTOCOL_READY_FOR_PHASE12B) ; seq310 :
ordre de gel ; seq311 : **GEL DÉFINITIF**. Commits : conception
`b22b9d3` (vérifié distant), gel : voir le commit associé au présent
procès-verbal, vérifié distant, arbre propre au moment du gel.

## Statuts après gel

- **PHASE 12-A : GELÉE DÉFINITIVEMENT (`PHASE12A_FROZEN`).** Aucune
  modification silencieuse du protocole gelé ; toute évolution
  exigera une nouvelle décision formelle chaînée.
- **PHASE 12-B : NON AUTORISÉE.** Ni l'extraction bornée des cinq
  variables ni le test prédictif ne sont autorisés par le présent
  gel ; décision distincte requise.
- Interdictions maintenues : accès M1 et holdout sans ordre, calcul
  prédictif, entraînement, stratégie, optimisation, analyse
  économique, cellules S12, T0/J2/J3, dépenses.
