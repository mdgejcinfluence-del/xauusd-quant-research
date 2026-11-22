# PHASE 12-C.2-R — PROVENANCE DU HOLDOUT ET INSTRUCTIONS DE TRANSFERT

## 1. Provenance établie (sans aucun accès nouveau aux données)

- Inventaire de référence déjà commité :
  `reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json` (348 partitions,
  métadonnées historiques : nom, `drive_id`, taille, périodes).
- Périmètre holdout résolu sans supposition : **66 partitions,
  `part_000283.parquet` à `part_000348.parquet` consécutives**
  (celles dont la fin de période dépasse la borne IS historique
  2020-01-20T09:36:27 UTC), 13,66 Go au total. La plage « 282–348 »
  (67 numéros) mentionnée dans les premiers rapports incluait
  `part_000282` (2019-11-10 → 2019-12-16), qui est une partition
  **IS déjà migrée** (dataset Kaggle `xauusd-is-missing13`) et sert
  uniquement de contexte au détecteur causal ; elle ne fait pas
  partie du transfert.
- Frontière analytique inchangée : 2020-01-01T00:00 UTC ;
  `part_000283` débute le 2019-12-17 et chevauche donc la
  frontière — elle est transférée telle quelle, et les exclusions
  préenregistrées (fenêtres et grappes traversant la frontière)
  s'appliqueront à l'analyse, jamais au transfert.
- Empreintes source : l'inventaire historique ne contient **aucun
  SHA-256** ; les empreintes de référence devront être établies au
  moment du transfert authentifié et consignées avant toute
  comparaison (voir §3).
- Liste exacte et destinations : `PHASE12C2_HOLDOUT_TRANSFER_MANIFEST.csv`
  (66 lignes : identifiant, fichier, `drive_id`, taille attendue,
  période, dataset de destination).

## 2. État des voies d'accès (preuves commitées)

| Voie | Résultat | Preuve |
|---|---|---|
| Drive anonyme (gdown) | Bloqué, quota Google | runs 45030043384 / 45030489413, `PHASE12C2_LOTLOG_h01..h08.txt` |
| Drive anonyme (URL directe `drive.usercontent`, repli historique) | Bloqué, même quota | run 45031240112, journaux de lots |
| Drive authentifié par compte de service | **Secret `GDRIVE_SA_JSON` absent du dépôt** | sonde run 45032424958, `PHASE12C2_PROBE.json` (`gdrive_sa_present: false`) |
| Kaggle (écriture/lecture) | Authentifié, joignable | sonde idem (`kaggle_auth_ok: true`) ; datasets IS `shalom5123/xauusd-is-*` |

Verdict de migration à ce stade : **`HOLDOUT_MIGRATION_BLOCKED`**
(audit : `PHASE12C2_HOLDOUT_TRANSFER_AUDIT.json`). Aucune migration
n'est prétendue réalisée.

## 3. Instructions exactes de transfert (propriétaire des données)

1. Depuis votre propre accès Google Drive (celui qui détient les
   fichiers d'origine), télécharger — ou transférer directement —
   les **66 fichiers originaux listés dans
   `PHASE12C2_HOLDOUT_TRANSFER_MANIFEST.csv`**, sans les ouvrir dans
   un tableur, sans conversion, sans recompression, en conservant
   exactement les noms `part_000NNN.parquet`.
2. Créer sur Kaggle (compte `shalom5123`) **six datasets privés**
   et y déposer les fichiers selon la colonne
   `destination_kaggle` du manifeste :
   `xauusd-ho-b01` (part_000283–293), `xauusd-ho-b02` (294–304),
   `xauusd-ho-b03` (305–315), `xauusd-ho-b04` (316–326),
   `xauusd-ho-b05` (327–337), `xauusd-ho-b06` (338–348).
   Visibilité : **privée**, sans exception.
3. Ne modifier, renommer, supprimer ni remplacer aucun fichier
   d'origine sur Drive.
4. Confirmer l'achèvement dans le fil de la mission (aucun secret,
   aucun token à communiquer en conversation).

Après cette confirmation, une reprise technique contrôlée pourra,
sous votre validation : calculer le SHA-256 de chaque fichier
source au moment d'un transfert authentifié (ou reprendre les
empreintes que vous fournirez par un canal vérifiable), télécharger
chaque copie Kaggle, comparer individuellement les 66 empreintes
et tailles (66 attendues / 66 présentes / 66 correspondances, zéro
manquante, zéro supplémentaire, zéro divergence), puis seulement
exécuter la reprise unique de la confirmation H1 (protocole 12-C,
modèle gelé 12-C.1, M0 gelé), dont les résultats seront terminaux.

## 4. Frontières et interdictions conservées

Période autorisée : 2020-01-01T00:00 UTC jusqu'à la dernière date
couverte par les partitions validées (fin de `part_000348` :
2026-09-30 selon l'inventaire). Données IS jamais introduites dans
la population d'évaluation (contexte détecteur seul pour les
barres antérieures à la frontière) ; H1 seule famille ; aucune
sélection d'événements selon une performance ; aucun seuil
recalculé ; holdout inutilisable pour toute autre recherche ;
aucune partition dans Git ni dans un artefact public.

---

## Addendum R2 (seq322) — dossier partagé : même blocage de quota

La sonde du dossier partagé (run `45034907980`,
`PHASE12C2R2_PROBE.json`) établit : dossier lisible, 348 partitions
énumérables, **66/66 noms et `drive_id` conformes au manifeste** —
mais ce sont les mêmes objets Drive que ceux déjà bloqués, et le
test de téléchargement réel (plus petit fichier du périmètre) a
reproduit le message de quota Google. Le partage en lecture seule
n'a pas créé de copies ni levé le quota par fichier. Aucun
contournement n'a été tenté (ordre exprès). Les trois voies de
déblocage restantes sont consignées dans
`PHASE12C2_TRANSFER_EXECUTION.json` (attente du quota puis nouvelle
sonde ; transfert propriétaire ; restauration du secret
`GDRIVE_SA_JSON` par le propriétaire). Point technique annexe : le
CLI Kaggle du runner exige le paquet `six` (absent lors de la
sonde) — à inclure dans l'installation avant toute reprise.
