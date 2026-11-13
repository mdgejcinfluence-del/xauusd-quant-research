# META ALPHA — Préflight via le lien public Drive (référence de travail)

**Date :** 13 novembre 2026 · **Méthode :** lien de partage Drive fourni par le propriétaire
**Dossier racine :** `META_ALPHA_XAUUSD_DGP`
**ID Drive (référence permanente) :** `1dy4-3dobsaUQUOhIg3UTFaojD7IfhxxX`
**Lien :** https://drive.google.com/drive/folders/1dy4-3dobsaUQUOhIg3UTFaojD7IfhxxX?usp=sharing

> Ce lien devient la référence d'accès aux données pour la suite du travail.
> Aucun accès au Gmail du propriétaire n'est utilisé. Lecture seule, via le partage.

## 1. Structure vue à la racine (conforme à la passation)

`_DUCKDB_TEMP` · `00_PROJECT_KIT` · `00_RAW` · `01_PARQUET` · `02_REGISTRY` ·
`03_DGP_ANALYTICAL` · `03_MANIFESTS` · `03_REGISTRY` · `04_CHECKPOINTS` · `05_LOGS` ·
`05_REPORTS` · `05_STATE` · `06_REPORTS` · `06_RESULTS` · `07_ERRORS` · `07_LOGS` ·
`08_LOGS` · `08_SCRATCH` · `09_EXECUTIONS` · `99_AUDIT_READ_ONLY` ·
`RESEARCH_V1_XAUUSD_TICK_ONLY` · `ENVIRONMENT_CERTIFICATE.json` · `manifest.json` ·
`phase_state.json` · `PROJECT_STATE.md`

IDs utiles : `01_PARQUET`=`1NJefqb8Vzq2QlpJFXqhKDKnLK__aT1up` ·
`XAUUSD_DGP_CHRONOLOGICAL_V5R10`=`1DPHNlBBbVEPQ7G3qp7RsRNMtoo-zEa8N` ·
`PARTITIONS`=`1gQc_VjKSTDLzRZZa6B8mO071nf8XG28e` ·
`04_CHECKPOINTS`=`1bXER6yC1tGPX2lVFN9KfwE2kaUgTJnRy` ·
`00_PROJECT_KIT`=`1zh9j86S6jv0SIZwGYQ-mu3s7-GxNtLyx`

## 2. Certificats lus et vérifiés (contenu intégral lu, pas un résumé)

### Phase 1 — `PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json` (ID `1lIe3sUSfXpKVwjLiN3mIBesIY9mFJiCT`)
| Champ | Attendu (passation) | Lu | Verdict |
|---|---|---|---|
| status | CERTIFIED | CERTIFIED | ✅ |
| primary_truth | XAUUSD native Dukascopy Bid/Ask tick BI5 | idem | ✅ |
| raw / parquet files | 11 136 / 11 136 | 11 136 / 11 136 | ✅ |
| total_ticks_validated | 685 118 625 | 685 118 625 | ✅ |
| validated_raw_errors | 0 | 0 | ✅ |
| synthetic / interpolation / substitutions | false partout | false partout | ✅ |

### Phase 2 — `PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json` (ID `1NeCMJfiiGtOj8CIvif9vJOpgaL2kHJe6`)
| Champ | Attendu | Lu | Verdict |
|---|---|---|---|
| status / artifact / script | CERTIFIED / DGP_BASE / SCRIPT_2_V5R10_RESUME_R3 | idem | ✅ |
| input_files / input_ticks | 11 136 / 685 118 625 | idem | ✅ |
| output_partitions / output_rows | 348 / 685 118 625 | idem | ✅ |
| observation_unit | NATIVE_XAUUSD_TICK_EVENT | idem | ✅ |
| timestamp_min → max | 2010-01-04 00:01:10.457Z → 2026-09-30 23:59:58.864Z | idem | ✅ |
| observation_id | 1 → 685 118 625 | idem | ✅ |
| chronological / regressions | true / 0 | true / 0 | ✅ |
| mid / spread validation | PASS / PASS | PASS / PASS | ✅ |
| formula_registry_status | PARTIAL | PARTIAL | ✅ (hors périmètre, ne pas reconstruire) |
| scientific_families_undefined | 19 (champ hérité) | 19 | ✅ (ne pas confondre avec les 8 familles) |
| phase_3_started | false | false | ✅ |

**Conclusion : les deux certificats correspondent exactement, valeur par valeur, à la
passation. C'est la première lecture réelle du corpus : le rédacteur ne l'avait jamais eue.**

## 3. Partitions

Dossier `PARTITIONS` ouvert : les noms vont de `part_000001.parquet` à
`part_000348.parquet`, format exact attendu par le préflight de la passation.
(Comptage exhaustif ligne à ligne et empreintes : à produire lors de l'exécution
du préflight complet, pas estimés ici.)

## 4. Ce qui reste bloqué — formulé exactement

1. **Le code** (`metaalpha/`, 24 modules, 143 tests) : le propriétaire a annoncé deux
   liens, mais **les deux liens reçus sont identiques** (le dossier DGP ci-dessus).
   Le second lien — celui du dossier « pour arena » contenant `META_ALPHA_CODE_V1.zip` —
   n'a pas été reçu. Dans le dossier DGP, seul `00_PROJECT_KIT/META_ALPHA_PROJECT_KIT.zip`
   (8 octobre, kit documentaire antérieur) est présent : ce n'est pas le code V1.
2. **Les SHA-256 canoniques des certificats** : le contenu est lu et vérifié, mais
   l'empreinte opposable (`BASELINE_HASH_MANIFEST.json`) exige les octets exacts des
   fichiers — elle sera calculée au premier téléchargement complet, pas reconstruite
   depuis un texte recopié. Aucune valeur devinée.
3. **Le schéma réel des partitions** : inconnu tant qu'un Parquet n'est pas téléchargé
   (`build_inventory` lit les footers). Non présommé.

## 5. Dépôt GitHub public — décision consignée, exécution différée à raison

Le propriétaire demande un **nouveau dépôt GitHub public** (décision déjà actée dans la
passation §7, nom suggéré `meta-alpha-xauusd`). Il ne sera créé/poussé qu'avec le code V1,
après les trois barrières du §8 (`.gitignore`, hook pre-commit, scan `secrets_guard`) :
créer un dépôt public vide maintenant n'apporterait rien, et pousser avant le scan
serait exactement le risque que la passation interdit. Le présent dépôt de session reste
le lieu de travail jusqu'à cette bascule.

## 6. Code V1 récupéré et vérifié (13 novembre, suite)

- Lien « pour arena » reçu : dossier `1SY-2KGuHc66HDQfbCs1BcoQtnkJwRYyd`,
  fichier `META_ALPHA_CODE_V1.zip`, ID `1jL206TGVv0H-akAcZEJpPdxXI2h9Y4l9`.
- Téléchargement réalisé par GitHub Actions (la sandbox n'a pas d'accès sortant Drive) :
  SHA-256 du ZIP `0511a7d47665f74c69d5cccefc47027115b7bd817b096ea990a13c21d1fb0a76`,
  extraction 77 fichiers, pré-scan secrets propre, code commité sous `META_ALPHA_CODE_V1/`.
- **Tests : `143 passed` — conforme exactement à la passation (§7 étape 1).**
- Écart mineur trouvé et corrigé (reproductibilité d'installation, pas de logique) :
  deux dépendances non déclarées — `google-auth-oauthlib` (utilisée par
  `oauth_drive.py`, absente de `requirements-drive.txt`) et `pytz` (requise par
  DuckDB sur les colonnes timezone). Sans elles : 8 échecs d'import. Avec : 143/143.

## 7. Schéma réel découvert (étape 5) — ÉCART CONSTATÉ, ARRÊT PROTOCOLE

Sonde par footers Parquet uniquement (GitHub Actions + gdown, aucun chargement complet) :

| | part_000001 | part_000348 |
|---|---|---|
| SHA-256 | `66954ecc…c8708b9` | `aa18a682…fbe42c` |
| Taille | 1 763 664 o | 291 913 210 o |
| Lignes (footer) | 40 112 | 7 896 153 |
| Row groups | 1 | 65 |
| Créé par | DuckDB v1.3.2 | DuckDB v1.3.2 |
| Colonnes | 16 | 16 (mêmes noms) |
| `bid_volume`/`ask_volume` | **double** | **uint32** |
| Ordre des colonnes | observation_id en tête | observation_id en fin |

Colonnes : observation_id, timestamp_utc (us, UTC), bid, ask, mid, spread_abs,
spread_rel, bid_volume, ask_volume, symbol, source_file, file_row_number,
previous_timestamp, previous_mid, log_return, abs_log_return.

**Écarts par rapport à l'attendu « un schéma unique » (§3.6 de la passation) :**
1. Signatures de schéma **différentes** entre la première et la dernière partition
   (ordre des colonnes + type de `bid_volume`/`ask_volume`).
2. Tailles/nombre de lignes très inégaux entre partitions extrêmes (40 k vs 7,9 M lignes) —
   le total certifié de 685 118 625 lignes reste à confirmer par l'inventaire complet
   des 348 footers (somme des `num_rows`), pas par extrapolation.
3. Présence de `bid_volume`/`ask_volume` : conformément aux pièges §11, ces champs ne
   seront **pas** appelés « volume réel » sans preuve de sémantique ; un tick reste
   un changement de cotation, pas une transaction.

**Décision (protocole §3.6) : STOP.** Aucune correction silencieuse, aucune hypothèse
bénigne. La prochaine étape légitime est l'inventaire complet des 348 footers
(noms, lignes, signatures) pour mesurer l'ampleur exacte de l'hétérogénéité, puis
rapport au propriétaire avant toute montée de l'échelle L2+.
