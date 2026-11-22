# PHASE 12-C.2 — RAPPORT D'INCIDENT ET VERDICT `BLOCKED`

**Aucune métrique de confirmation n'a été produite ni consultée.
Le modèle gelé n'a pas été modifié. Verdict : `BLOCKED`
(provenance/accès aux sources holdout non garantis), conformément
à la règle d'arrêt de la mission et au préenregistrement 12-C.**

## 1. Préflight (conforme, avant tout accès)

Chaîne valide à seq317 ; commit distant `f1ba282` ; protocole 12-A
gelé `580c39b1…f94` ; protocole 12-C `bf3b9adf…` ;
`PHASE12C1_MODEL_PARAMETERS.json` `1bcb3b70…` et manifeste
`be2d0b23…` intègres ; code gelé `a1c9f52d…` ; données
d'apprentissage `6f684ee8…` ; coefficients chargés depuis le JSON
(jamais recopiés) ; M0 gelé 0,7591463414634146. Autorisation
chaînée seq318.

## 2. Sources holdout identifiées et tentative d'accès

Sources identifiées uniquement depuis l'inventaire déjà commité
(`INVENTORY_348_EXHAUSTIVE.json`, aucune exploration nouvelle du
holdout) : partitions `part_000282` à `part_000348` (les partitions
282–283, nov. 2019–janv. 2020, en contexte du détecteur causal
seul ; aucun événement IS importé dans la population). Ces
partitions n'existent que sur Google Drive (`drive_id` de
l'inventaire) ; elles n'ont jamais été migrées vers Kaggle, à la
différence des 282 partitions IS.

Trois runs CI identiques quant au test (aucun paramètre du test
modifié, aucune métrique produite) :

- run `45030043384` : 8/8 lots en échec au téléchargement Drive
  (gdown) ;
- run `45030489413` : idem (journaux de lots committés, cause
  établie) ;
- run `45031240112` : idem après ajout du repli historique direct
  `drive.usercontent.google.com` (celui de
  `ci_tools/kaggle_migrate.py:dl`).

Message d'erreur conservé dans les journaux de lots committés
(`PHASE12C2_LOTLOG_h01..h08.txt`) : *« Too many users have viewed
or downloaded this file recently… it may take up to 24 hours… »*
— blocage de quota/partage Google Drive, identique au blocage
historique qui avait imposé la migration Kaggle pour l'IS. Les
deux voies d'accès connues (gdown et URL directe) sont bloquées.

## 3. Conséquences et conformité

- Aucune partition holdout n'a été lue ; aucune barre, aucun
  événement, aucune variable, aucune prédiction, aucune métrique
  de confirmation n'existe. Les livrables
  `PHASE12C2_HOLDOUT_FEATURES.csv`,
  `PHASE12C2_HOLDOUT_PREDICTIONS.csv` et
  `PHASE12C2_FEATURE_AUDIT.json` n'ont donc pas été produits (les
  fabriquer serait une falsification) ; `PHASE12C2_EVALUATION.json`
  consigne le verdict BLOCKED et les effectifs à zéro.
- L'évaluation préenregistrée n'a **pas** été consommée : aucun
  résultat du holdout n'ayant été observé, une reprise reste
  possible sans biais dès que l'accès aux sources sera rétabli,
  sous une nouvelle autorisation ou la confirmation que la
  présente autorisation couvre la reprise technique (la mission
  autorise une reprise identique si aucune métrique n'a été
  consultée — c'est le cas — mais les trois tentatives montrent un
  blocage d'infrastructure persistant, non un incident ponctuel).
- Aucun paramètre du test n'a été modifié entre les tentatives :
  seuls l'instrumentation des journaux et le repli historique de
  téléchargement ont été ajoutés.

## 4. Voies de déblocage (décision du responsable requise)

1. **Migration Kaggle des partitions holdout** (voie historique
   éprouvée pour l'IS) : mais elle suppose elle-même un accès
   Drive fonctionnel depuis la CI, actuellement bloqué — à
   réessayer après expiration du quota Google (24 h annoncées,
   blocage historiquement persistant), ou migration effectuée par
   le propriétaire depuis son propre accès Drive.
2. **Rétablissement de l'accès Drive** par le propriétaire
   (partage/quota des fichiers sources).
3. Toute autre source de données exigerait une vérification de
   provenance et un amendement chaîné avant usage ; aucune source
   de substitution n'a été utilisée.

## 5. Verdict

**`BLOCKED`** — accès aux sources holdout impossible par les voies
autorisées connues ; intégrité du test préservée (aucune métrique
consultée, modèle et critères intacts). La Phase 12-C reste
suspendue jusqu'à décision du responsable sur la voie de
déblocage. Qualification inchangée des résultats 12-B :
`HISTORIQUEMENT ÉVALUÉE — NON INDÉPENDAMMENT CONFIRMÉE`.
Aucune autorisation ultérieure ne découle du présent rapport.

---

## Addendum Phase 12-C.2-R (migration contrôlée, seq320)

La migration autorisée par la mission 12-C.2-R a été instruite :
manifeste exact des 66 partitions (`part_000283`–`part_000348`,
13,66 Go ; ambiguïté 66/67 résolue au §1 de
`PHASE12C2_HOLDOUT_PROVENANCE.md`), puis sonde d'accès authentifié
en CI (run `45032424958`, métadonnées seules, aucun secret exposé,
preuve `PHASE12C2_PROBE.json`). Résultat : l'accès Kaggle est
authentifié, mais le secret de compte de service Drive
(`GDRIVE_SA_JSON`) est **absent du dépôt** — la modalité B
(transfert authentifié direct) n'existe donc pas, et la modalité
Drive anonyme reste bloquée par quota (trois runs documentés).
**Verdict de migration : `HOLDOUT_MIGRATION_BLOCKED`** (audit
`PHASE12C2_HOLDOUT_TRANSFER_AUDIT.json` : 0/66 vérifiées, aucune
comparaison présentée comme réussie, l'inventaire historique ne
contenant aucun SHA-256 source). Les instructions exactes de
transfert par le propriétaire (six datasets Kaggle privés
`xauusd-ho-b01..b06`, fichiers originaux inchangés) figurent dans
`PHASE12C2_HOLDOUT_PROVENANCE.md`. L'évaluation de confirmation
reste **non consommée** ; le verdict d'évaluation demeure
`BLOCKED` jusqu'à transfert vérifié (66/66 correspondances
cryptographiques) suivi d'une reprise unique validée.
