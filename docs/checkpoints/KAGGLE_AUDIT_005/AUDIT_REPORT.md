# MISSION 005 — Audit physique du corpus Kaggle (seq525–526)

Preuve : listing API Kaggle réel, paginé complètement (le défaut API de
20 fichiers/page avait d'abord fait croire à 153 fichiers — corrigé).
Artefacts : `KAGGLE_PHYSICAL_INVENTORY.csv` (348 lignes),
`KAGGLE_AUDIT_SUMMARY.json`, `AUDIT_LOG.txt`.

## Résultat physique
- **282/348 partitions PRÉSENTES ET VÉRIFIÉES sur Kaggle** : présentes
  dans les 8 datasets du compte (b01–b07 + missing13, 40+40+40+40+40+40
  +29+13 fichiers), taille conforme au manifeste, SHA-256 enregistrés
  lors de la migration certifiée. Couverture : **2010–2019**,
  288 086 588 ticks selon le manifeste certifié.
- **66/348 ABSENTES de Kaggle** : les partitions 2020–2026 (postérieures
  à la fenêtre de migration IS ≤ 2020-01-20). Aucune partition corrompue,
  aucun doublon détecté dans le listing physique.
- Limite honnête : le « ticks » est celui du manifeste certifié et les
  SHA sont ceux calculés à la migration ; un recomptage physique ligne
  à ligne des 282 partitions exigerait leur téléchargement (non fait,
  inutile : la vérification SHA à chaque usage, déjà implémentée,
  couvre l'intégrité au moment de l'emploi). La découverte de datasets
  par `dataset_list(mine)` a échoué sur la version CI de l'API ;
  l'inventaire couvre les 8 datasets de la migration, seule source
  Kaggle créée par META ALPHA.

## Correction de la stratégie d'accès (appliquée)
`ci_tools/ere_golive_ci.py` : Drive n'est plus la source par défaut —
une seule tentative Drive, puis récupération Kaggle certifiée (SHA
vérifié à chaque téléchargement) pour toute partition migrée ; Drive
reste l'unique source des 66 partitions 2020–2026, actuellement
bloquées par ses interstitiels de quota (2 040 octets).

## Conséquence scientifique
Découverte et validation (≤2019) sont intégralement servis par Kaggle.
Les partitions manquantes de GO-LIVE-001 se réduisent aux années
2021–2026 (validation partielle 2020–2022, confirmation 2023–2026),
absentes de Kaggle comme de Drive aujourd'hui. La migration Kaggle de
ces 66 partitions (depuis une source autorisée, quand Drive répondra)
est la voie de complétion inscrite au portefeuille. Aucun verdict
inter-segments avant complétion. Missions A et B : OPEN.
