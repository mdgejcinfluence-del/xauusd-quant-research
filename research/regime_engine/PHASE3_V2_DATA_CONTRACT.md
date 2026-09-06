# PHASE 3 V2 — STEP 3.1 : DATA CONTRACT (FROZEN)

**Date :** 2026-09-06 (UTC) · **Statut final : `DATA_CONTRACT = FROZEN`**
**Contexte :** RESTART CLEAN. L'ancien moteur 31-features (Phase 3 V1, perdu lors
de la réinitialisation du 2026-09-06) est **définitivement abandonné** : aucune
tentative de récupération, aucune définition de feature antérieure n'est réutilisée.
Ce document est l'unique source de vérité du contrat de données Phase 3 V2,
figé AVANT tout feature engineering.

---

## 1. DATASET SOURCE

| Item | Valeur (exacte, vérifiée) |
|---|---|
| Nom | XAUUSD M1, prix spot or, unité USD/oz nominale telle que livrée |
| Fichier maître | `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet` |
| Assemblée | concaténation byte-exacte des 7 fragments committés `XAUUSD_part_01..07.parquet.part` (6 × 20 971 520 B + 1 × 14 363 472 B = 140 192 592 B) |
| `DATASET_SHA` | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` (recalculé et vérifié : identique au manifeste Phase 1 et aux enregistrements Phase 2B) |
| `DATASET_ROWS` | **5 874 003** |
| Période couverte | **2010-01-01T00:02:00Z → 2026-08-30T23:58:00Z** (UTC) |
| Colonnes | `timestamp` (ns, tz-aware UTC), `open`, `high`, `low`, `close` (float64), `volume` |
| Gaps inter-barres | 15 699 écarts > 1 min ; 3 708 écarts ≥ 50 min (ruptures de marché) ; écart maximal 4 591 min ; médiane 3 min, P90 61 min, P99 2942 min |
| Lignes par année | 2010 364 242 · 2011 361 187 · 2012 353 628 · 2013 338 469 · 2014 337 956 · 2015 345 408 · 2016 353 104 · 2017 352 788 · 2018 353 923 · 2019 351 913 · 2020 355 495 · 2021 354 226 · 2022 354 633 · 2023 352 969 · 2024 355 892 · 2025 354 415 · **2026 233 755 (année partielle — sanity only)** |

**GAP_POLICY :** `NONE` — aucun gap n'est comblé, aucune barre n'est inventée,
aucune interpolation ; les barres M1 sont utilisées telles que livrées (exigence
Phase 1 L2). `VOLUME_POLICY : EXCLUDED` — la colonne `volume` est présente dans le
fichier mais son unité est inconnue (L1) : elle n'est **jamais** chargée en mémoire,
jamais utilisée, jamais dérivée, jamais imputée.

---

## 2. TIMEFRAME HIERARCHY

| Résolution | Rôle | Statut |
|---|---|---|
| **M1** | substrate | grille source ; aucune agréation ne modifie le maître |
| **M3** | **primary behavioral timeframe** | grille validée ; référence de calcul des propriétés « comportementales » |
| **H1** | context timeframe | grille validée ; contexte de plus haut niveau, non décisionnel seul |

Utilisation exclusive des **grilles M3/H1 déjà validées contre la Phase 2B** :

| Grille | Barres | Premier bar | Dernier bar | M1/barre moyen | Barres à trou interne | SHA-256 |
|---|---|---|---|---|---|---|
| M3 | **1 963 826** | 2010-01-01T00:00:00Z | 2026-08-30T23:57:00Z | 2.9911 | 2 248 (0.1145 %) | `c1eb3e09532cb92f46d6753f3d0abeda9a810dc8208a78d7e7105f2593b8a06f` |
| H1 | **98 412** | 2010-01-01T00:00:00Z | 2026-08-30T23:00:00Z | 59.6879 | 3 110 (3.1602 %) | `0372b46dd26bfcca6b29375a7103e4862a56a1f6b70bb7a876c62f9c8b5e12b7` |

Ces chiffres recoupent exactement les enregistrements committés Phase 2B
(`XAUUSD_TIMEFRAME_COMPARISON.csv`, Block A/B) : barres, bornes temporelles,
M1/barre moyen, taux de trous internes (0.11447 % / 3.16018 %), rupture interne 0.00 %,
contiguïté 99.3151 % / 95.6987 %. Les grilles sont des artefacts de scratch
(`/tmp/xauusd_audit/regime_engine/`) régénérables ; le contrat pinne les **cibles de
vérification** ci-dessus, pas les fichiers éphémères.

---

## 3. BAR CONSTRUCTION (protocole figé)

Règle d'existence d'une barre : une barre agrégée **existe si et seulement si au
moins une barre M1 réelle** tombe dans son bucket. Aucune exigence de complétude,
aucun padding, aucune barre synthétique. Les bogues de complétude de la boîte ne
sont pas rétablis : la barre est l'agrégation des M1 réellement présents.

| Item | Règle |
|---|---|
| Origine du temps | 1970-01-01T00:00:00Z (epoch Unix) |
| Timezone | UTC partout ; aucun fuseau local |
| Mapping `bar_id` | `bar_id = floor(epoch_minutes / k)`, k = durée de la barre (M3 : 3 ; H1 : 60) |
| Horodatage de barre | bord de bucket (début, multiple de k) ; tz-aware ns UTC |
| M1 → M3 | bucket = `t_min // 3` ; `open` = premier open, `high` = max, `low` = min, `close` = dernier close des M1 du bucket |
| M1 → H1 | idem avec `t_min // 60` |
| Compteurs d'intégrité par barre | `n_m1` (nb de M1 réels), `internal_missing` (minutes manquantes strictement internes), `internal_breaks` (ruptures ≥ 50 min strictement internes — 0 dans les deux grilles validées), `contig_next` (pas de minute manquante entre la barre précédente et celle-ci) |
| Traitement des gaps | conservés : aucune fenêtre n'est ré-échantillonnée sur l'horloge murale ; les fenêtres portent sur la **séquence de barres** (positions), les trous restant des trous de séquence |
| Écriture | parquet, ne modifie jamais le maître (L7), ne produit que de nouveaux fichiers |

---

## 4. PIT POLICY (verrouillée)

1. **Aucune donnée future** : la valeur d'une feature au bar `t` n'utilise que des
   informations disponibles après la fermeture du bar `t` — soit les barres
   d'indice `≤ t` (OHLC complétés du bar `t` inclus), jamais `t+1` ni au-delà.
2. **Aucune fenêtre centrée** : toute fenêtre glissante est de la forme
   `[t − W + 1, t]` (past-only, incluse en `t`), jamais `[t − W/2, t + W/2]`.
3. **Aucun décalage futur** : interdiction explicite de tout `shift(-k)`, accès
   `[t+k]`, `rolling(..., center=True)`, lead/lag positif, ou toute fonction
   utilisant des valeurs d'indice supérieur à `t`.
4. **Normalisation PIT** : toute statistique de normalisation (mesure de
   localisation/dispersion) est calculée sur le passé du bar `t` uniquement.
5. **Protocole de vérification obligatoire** (avant tout usage, pour chaque
   feature) :
   - scan statique : recherche des motifs interdits (lead, centre, `t+1`) ; toute
     occurrence doit être justifiée ou corrigée ;
   - audit de troncature dynamique : recalcul de la feature sur l'historique
     complet vs historique tronqué à des horodatages-sondes antérieurs (≥ 3
     sondes, ≥ 1 en 2013, ≥ 1 en 2026) ; l'écart doit être **exactement nul** ;
   - vérification d'identité : re-calcul sur un sous-échantillon disjoint,
     comparaison bit-à-bit (tolérance zéro).
6. Ces règles s'appliquent à **toutes** les transformations, y compris les
   agrégations multi-échelles M3/H1 alignées sur le bar `t` (hierarchie
   représentative seulement — le temps ne « saute » jamais vers l'avant).

---

## 5. MARKET-TIME / EXTREME POLICY

| Point | Politique |
|---|---|
| Horaires | UTC exclusivement ; bucket borders epoch-aligned ; aucune conversion locale, aucune notion de « session » ajoutée — les 5 fenêtres UTC de la Phase 2B sont descriptives et non héritées dans le contrat |
| Rupture/convention ~2013 | documentée et **non corrigée** (L4) : la rupture de convention de session reste dans les données ; toute analyse de stabilité doit rapporter séparément pré-2013 (2010–2012) et post-2013 (2013–2025), sans réparation/fusion |
| 2026 | année partielle (233 755 barres M1, jusqu'au 2026-08-30T23:58Z) ; jamais un critère de sélection ; signalée et analysée séparément (L5) |
| Extrêmes M1 | **conservés** dans le maître : aucune suppression, aucun remplacement, aucun nettoyage (L6) ; le maître reste byte-identique (`DATASET_SHA`) |
| Règles d'extrêmes | aucune règle de classification d'extrême n'est figée dans ce contrat ; si une analyse future en définit une, la règle doit être déclarée ex ante (seuil, fenêtre, past-only) et ne jamais modifier les données |
| Volume | jamais utilisé (VOLUME_POLICY = EXCLUDED, L1) |

---

## 6. VERSIONING

| Item | Valeur |
|---|---|
| Fichier de contrat | `research/regime_engine/PHASE3_V2_DATA_CONTRACT.md` (unique) |
| Version | V2.0 — figée le 2026-09-06 |
| Statut | `DATA_CONTRACT = FROZEN` |
| Invalidation | toute modification des valeurs ou règles du présent document exige une nouvelle version numérotée + état non-FROZEN explicite ; toute feature de la Phase 3 V2 doit être conforme à ce contrat, sinon elle est rejetée |
| Héritage | l'ancien moteur 31-features (V1) est hors périmètre ; ses fichiers historiques restent dans le dépôt à titre de trace, sans aucune valeur contractuelle |

---

## 7. HYPOTHÈSES EXPLICITES

| # | Hypothèse | Caractère |
|---|---|---|
| A1 | L'ancre de ligne des futures features V2 est la grille **M3** (primary behavioral timeframe) : 1 ligne = 1 barre M3, `bar_id` M3 | Décision (dérivée de la hiérarchie) |
| A2 | Le bar `t` est considéré fermé à l'instant du **dernier** M1 réel de son bucket ; le PIT inclut l'OHLC complété du bar `t` | Décision |
| A3 | Les fenêtres portent sur la séquence de barres (positions), les gaps sont préservés comme ruptures de séquence | Décision |
| A4 | Le maître est byte-stable : seule la `DATASET_SHA` ci-dessus est acceptée ; toute reconstruction doit la reproduire exactement | Contrainte |
| A5 | « Rupture de marché » = écart ≥ 50 min entre barres M1 consécutives (définition Phase 1/2B) | Contrainte |
| A6 | La règle 3σ/1440 min de la Phase 2B est un outil descriptif de la Phase 2B ; la Phase 3 V2 ne l'hérite pas comme flag de feature | Décision |
| A7 | Aucune stratégie, aucun backtest, aucune performance, aucun retour, aucun coût réel dans le périmètre V2 à ce stade | Contrainte |
| A8 | Aucun héritage EURUSD : aucune donnée, filière, constante ou conclusion EURUSD | Contrainte |
| A9 | Les grilles régénérées doivent reproduire les cibles de vérification du §2 ; en cas d'écart, STOP et ré-audit avant tout usage | Contrainte |
| A10 | Toute statistique de style (horaire, session) est calculée sur les barres existantes uniquement, sans hypothèse d'occupation des minutes manquantes | Décision |

---

```
DATASET_SHA = fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0
DATASET_ROWS = 5874003
TIMEFRAME_POLICY = M1_SUBSTRATE / M3_PRIMARY / H1_CONTEXT
GAP_POLICY = NONE (no fill, no padding, no synthetic bar, no interpolation)
PIT_POLICY = PAST_ONLY (no future, no centered window, no t+1, verification protocol mandatory)
EXTREME_POLICY = RETAINED (no deletion, no modification, master byte-identical)
VOLUME_POLICY = EXCLUDED (never loaded, never used, never derived)
DATA_CONTRACT = FROZEN
```
