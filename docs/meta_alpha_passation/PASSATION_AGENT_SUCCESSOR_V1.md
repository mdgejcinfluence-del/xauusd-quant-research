# META ALPHA — DOSSIER DE PASSATION

**Destinataire :** agent autonome successeur, disposant d'un accès Google Drive réel et d'un accès GitHub.
**Rédacteur :** agent précédent, qui n'a **pas** eu cet accès.
**Date :** 13 novembre 2026.
**Version du dossier :** 1.0

---

## 0. Comment lire ce document

Ce document est une **passation**, pas un tutoriel. Il contient tout ce qu'un agent successeur doit savoir pour reprendre le projet sans rien casser et sans rien réinventer : l'objectif, les contraintes, l'architecture, ce qui existe déjà, ce qui reste à faire, les erreurs déjà commises, et les pièges qui ont coûté du temps.

**Lis-le en entier avant d'écrire une ligne de code.** L'ordre des sections suit l'ordre dans lequel tu as besoin de l'information.

Trois règles de lecture :

1. **Tout ce qui est marqué « INTERDIT » l'est absolument.** Ce ne sont pas des recommandations. Plusieurs sont implémentées dans le code et lèveront une exception si tu les contournes. Ne les désactive pas.
2. **Tout ce qui est marqué « VÉRIFIÉ » a été exécuté et testé.** Tout ce qui est marqué « NON VÉRIFIÉ » ne l'a pas été — traite-le comme une hypothèse à contrôler.
3. **Quand ce document dit « ne devine pas », ne devine pas.** Le projet tout entier repose sur le refus de combler un trou par une valeur plausible. C'est ce qui le rend crédible. Si tu combles un trou, tu détruis la valeur du projet, même si le résultat semble meilleur.

---

## 1. Le projet en une page

### 1.1 Objet

**META ALPHA** est une recherche quantitative sur les cotations natives XAUUSD Bid/Ask, tick par tick, de 2010 à 2026. L'objectif final n'est pas un backtest séduisant : c'est de déterminer, avec rigueur, s'il existe des avantages statistiques (**edges**) dans ces données, de les qualifier, puis — seulement s'ils existent — de construire un portefeuille et d'étudier sa compatibilité avec un challenge de prop firm (Blue Guardian 2-Step Pro 5K).

**Le nombre d'edges est inconnu à l'avance.** Il peut y en avoir plusieurs, un seul, ou aucun. `NO_EDGE` est une conclusion scientifique valide et complète. **Il est formellement interdit de fabriquer un portefeuille pour satisfaire une cible prédéfinie.**

### 1.2 Ce que le propriétaire veut vraiment

Le propriétaire (un humain, non-technicien, basé à Cotonou) ne veut pas un rapport. Il veut **un système qui travaille sans lui**. Sa phrase exacte : *« Il pourra travailler de façon automatisée, parce que c'est ce que je veux. »*

Cela a une conséquence architecturale précise : **toute tâche qui peut être automatisée doit l'être**, et le propriétaire ne doit être sollicité que pour ce qui n'appartient qu'à lui — des décisions de définition scientifique, des autorisations, des acceptations de phase. Pas de travail mécanique.

Il a explicitement corrigé une erreur du rédacteur sur ce point : quand le système a besoin de définir des familles de variables, **ce n'est pas au propriétaire de les définir** — elles sont extraites du dossier de spécification, et le système les instancie lui-même. Retiens cette leçon : **avant de poser une question au propriétaire, vérifie si la réponse n'est pas déjà dans les documents.**

### 1.3 Le budget

**6 000 FCFA ≈ 9,95 USD**, une seule fois. Ce n'est pas un budget mensuel.

Contrainte associée, **explicitement saluée par le propriétaire comme une qualité du projet** : **l'infrastructure doit coûter 0 FCFA par mois**. GitHub Actions, Kaggle et Google Drive (déjà en place) suffisent. Les 6 000 FCFA restent une marge non dépensée. **N'ajoute aucun composant payant.** Si tu penses qu'un composant payant est nécessaire, tu te trompes : cherche la solution gratuite ou dis clairement que c'est impossible.

### 1.4 La contrainte matérielle

**CPU uniquement. Aucun GPU.**

Ce n'est pas une préférence, c'est une mesure. Les traitements sont : des statistiques de séries temporelles, du bootstrap, des tests de permutation, du replay événementiel, des corrélations. Rien de tout cela n'est du calcul matriciel dense. Un GPU n'accélérerait rien d'utile et introduirait une dépendance, un coût et une contrainte de disponibilité.

C'est implémenté :
- `metaalpha/dispatch.py` : `"enable_gpu": False` avec le commentaire `# AUCUN GPU : inutile pour ce projet`
- `.github/workflows/ci.yml` : une étape casse le build si `cuda`, `torch`, `cupy` ou `nvidia-smi` apparaît dans le code de calcul.

**Si tu introduis une dépendance GPU, la CI échoue. C'est voulu.**

### 1.5 L'état réel au moment de la passation

| Élément | État |
|---|---|
| Code de l'infrastructure | **écrit et testé** — 143 tests verts |
| Accès au corpus réel (348 partitions) | **JAMAIS RÉALISÉ** — le rédacteur n'avait pas d'accès Drive au bon compte |
| Vérification des certificats Phase 1 et 2 | **JAMAIS RÉALISÉE** — en attente de l'accès |
| Dépôt GitHub | **N'EXISTE PAS** — pas d'accès GitHub pour le rédacteur |
| Moteurs scientifiques P3 à P7 | **NON ÉCRITS** — décision volontaire, voir §9 |
| Phases 1 et 2 historiques | **CERTIFIÉES, jamais reconstruites** |

**Tu es le premier agent à avoir réellement accès aux données.** C'est ta responsabilité principale, et c'est ce qui rend cette passation nécessaire : tout ce qui précède a été prouvé sur données synthétiques de structure identique, jamais sur le corpus réel.

---

## 2. Les documents de référence

Deux documents existent et font autorité. Ils sont dans `/home/user/uploads/` sur la machine du rédacteur ; ils ont été fournis par le propriétaire.

### 2.1 `META_ALPHA_MISSION_SCIENTIFIQUE_BLUE_GUARDIAN_AGENT_V2.md` (717 lignes)

**C'est le document le plus important.** Il définit les 9 phases, ce que chaque phase doit produire, les gates, les interdictions, et la spécification Blue Guardian. Lis-le en entier.

Points structurants à ne pas manquer :
- §2 : les trois couches à ne jamais confondre (recherche / portefeuille / adaptateur challenge)
- §3 : les deux certificats existants et leurs valeurs exactes
- §4.2 : ce que les ticks **ne peuvent pas** prouver
- §5 : le contenu détaillé des phases 2 à 9
- §6 : les règles Blue Guardian rapportées, dont la règle des 2 minutes
- §9 : les 14 erreurs historiques à ne pas répéter
- §12 : l'ordre exact du travail
- §13 : ce que le propriétaire ne doit **jamais** avoir à fournir

### 2.2 `META_ALPHA_DOSSIER_STRATEGIE_ET_FEUILLE_DE_ROUTE_V1.md` (772 lignes)

Le dossier de stratégie originel. Contient la roadmap, le budget, les contraintes. **Attention :** il contient aussi des chiffres d'un état antérieur du projet qu'il ne faut **pas** reprendre aveuglément. Voir §4.3 sur le compteur `19`.

Section clé : **§4.2** — les **8 familles** admissibles de variables. C'est la source de `metaalpha/families.py`.

---

## 3. Les données — ce qui existe et ce qui est vrai

### 3.1 Racine logique

```
META_ALPHA_XAUUSD_DGP
```

Sur le Drive du propriétaire. C'est **un Drive distinct** de celui de la conversation où ce dossier a été rédigé. Le propriétaire a insisté sur ce point. Ne présume pas du compte.

### 3.2 Phase 1 — Source primaire (CERTIFIED)

Certificat : `04_CHECKPOINTS/PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json`

| Champ | Valeur |
|---|---|
| status | `CERTIFIED` |
| symbol | XAUUSD |
| primary_truth | XAUUSD native Dukascopy Bid/Ask tick BI5 |
| fichiers bruts | 11 136 |
| fichiers Parquet | 11 136 |
| ticks validés | **685 118 625** |
| erreurs brutes validées | 0 |
| données synthétiques | aucune |
| interpolation | aucune |
| substitution OHLC | aucune |
| substitution de source | aucune |
| créé le | 6 octobre 2026 |

### 3.3 Phase 2 DGP Base chronologique V5R10 (CERTIFIED)

Certificat : `04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json`

| Champ | Valeur |
|---|---|
| status | `CERTIFIED` |
| artifact | DGP_BASE |
| script | SCRIPT_2_V5R10_RESUME_R3 |
| fichiers d'entrée | 11 136 |
| ticks d'entrée | 685 118 625 |
| partitions de sortie | **348** |
| lignes de sortie | 685 118 625 |
| unité | `NATIVE_XAUUSD_TICK_EVENT` |
| début | `2010-01-04 00:01:10.457000+00:00` |
| fin | `2026-09-30 23:59:58.864000+00:00` |
| observation IDs | 1 à 685 118 625 |
| ordre chronologique | vrai |
| régression temporelle | 0 |
| validations Mid et spread | `PASS` |
| traitement | out-of-core |
| moteur | DuckDB + PyArrow Parquet |
| reprise | oui |
| `formula_registry_status` | `PARTIAL` |
| `scientific_families_undefined` | `19` |
| `phase_3_started` | `false` |

### 3.4 Emplacement des partitions

```
01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS
```

Fichiers `part_000001.parquet` à `part_000348.parquet`. Ces noms sont **exacts** et vérifiés par le préflight.

### 3.5 Deux avertissements critiques sur les données

**Avertissement 1 — ne construis pas d'image de ce corpus.** 685 millions de lignes. Il ne doit **jamais** être chargé en mémoire d'un coup. Le module `metaalpha/duck.py` refuse une connexion sans limite de mémoire, par conception (`UnboundedConnectionError`). Ne contourne pas ce refus.

**Avertissement 2 — un tick n'est pas une transaction.** C'est un changement de cotation. Tu ne peux pas en déduire le volume échangé, le delta acheteur/vendeur, la profondeur du carnet, ni le taux de remplissage d'ordres limites. Ces informations sont classées `UNAVAILABLE` dans `metaalpha/mission.py` et le resteront.

### 3.6 Schéma des partitions — NON VÉRIFIÉ

**Personne n'a vu le schéma réel.** Le rédacteur n'avait pas d'accès. Ne présume **rien**. Ce n'est pas grave : `metaalpha/inventory.py` le découvre.

Ce que tu dois faire à ta première exécution :

```python
from metaalpha.inventory import build_inventory
inv = build_inventory("/chemin/vers/PARTITIONS")
print(inv["schema_signatures"])
print(inv["partitions"][0]["field_mapping"])
```

`build_inventory` lit **uniquement les footers Parquet** — aucun octet de donnée. Il est rapide même sur 348 fichiers. Il te dira :
- les colonnes réelles de chaque partition
- si le schéma est homogène ou non
- le nombre de lignes par partition
- la détection des champs canoniques (`timestamp`, `bid`, `ask`) via `FIELD_ALIASES`

**Résultat attendu d'après le certificat :** 348 fichiers, 685 118 625 lignes au total, un schéma unique. Si tu obtiens autre chose, **arrête-toi** et rapporte l'écart au propriétaire. Ne « corrige » pas un écart en supposant qu'il est bénin.

---

## 4. Les corrections de cadrage — erreurs déjà commises, à ne pas répéter

Cette section existe parce que le rédacteur a réellement commis ces erreurs, et que le propriétaire l'a corrigé. Elles coûteraient du temps et de la crédibilité à un agent qui les referait.

### 4.1 « 19 familles à définir » — FAUX

Le certificat Phase 2 contient `scientific_families_undefined = 19`. Le rédacteur a un jour interprété cela comme « il y a 19 familles de variables à créer, il faut demander au propriétaire de les définir ».

**C'est une erreur.** Ce compteur est un **champ du certificat hérité**, décrivant l'ancien Formula Registry, classé `PARTIAL` et **hors périmètre** (consigne explicite : ne pas reconstruire les Phases 1 et 2).

Les familles du livrable sont les **8** du §4.2 du dossier de stratégie, déjà écrites. Elles sont dans `metaalpha/families.py`. Le système les instancie seul.

**Ne pose jamais la question « quelles sont les 19 familles » au propriétaire.** C'est exactement le genre de question qui le fait perdre confiance.

### 4.2 « Colab n'a pas d'API d'exécution » — TROP ABSOLU

Le rédacteur a affirmé cela. C'est inexact : Colab n'a pas d'API **officielle** sans navigateur, mais un fork communautaire existe et exécute sans onglet. Il reste non officiel et fragile. La formulation correcte est « pas d'API officielle headless ; un fork communautaire existe, non officiel ».

**Kaggle, en revanche, est officiellement pilotable à distance** : CLI qui crée-ou-met-à-jour un kernel et le lance, tokens `KGAT…` documentés pour les workflows automatisés et la CI/CD, et un serveur MCP distant officiel. Un système muni d'un token peut le piloter sans navigateur.

### 4.3 Vidage du Drive précédent — impasse

Le rédacteur a cherché le corpus sur le Drive connecté à sa conversation. Il n'y est pas. **N'en conclus pas que les données n'existent pas** : elles sont sur un autre compte. Tu as accès, toi. C'est précisément ton avantage.

### 4.4 Benchmark 112 M ticks/s — FAUX

Un benchmark antérieur annonçait 112 M de lignes par seconde. C'était **37 fois faux** : la requête ne touchait qu'une colonne, donc DuckDB élidait le reste. Les chiffres réels, mesurés honnêtement, sont **18,5 M lignes/s** en agrégation simple et **3,02 M ticks/s** pour des fenêtres glissantes.

**Mesure toujours sur les colonnes réellement nécessaires.** Un benchmark qui ne lit pas les données ne mesure rien.

### 4.5 Autres pièges techniques rencontrés

| Piège | Symptôme | Solution |
|---|---|---|
| DuckDB `parquet_schema` | la pseudo-colonne `schema` casse `count(DISTINCT …)` | ne pas l'utiliser comme colonne |
| Préfixe de chemin doublé | fichier écrit au mauvais endroit | `Storage._resolve_write` — ne pas revenir en arrière |
| Sous-chaîne `"sk-"` | faux positif sur `sys.exit` | motifs précis, voir `secrets_guard.py` |
| Garde-fou disque | faux positif en sandbox (~1 GB) | fixture `test_cfg` dans les tests, **pas** une baisse des valeurs de production |

---

## 5. L'architecture

### 5.1 La chaîne

```
TICKS BID/ASK → DGP ANALYTIQUE → VARIABLES → HYPOTHÈSES → ANOMALIES
  → STRATÉGIES CANDIDATES → EDGES QUALIFIÉS → PORTEFEUILLE
  → VALIDATION FINALE → ADAPTATEUR BLUE GUARDIAN → ROBOT
```

Onze étapes. **Rien ne saute d'étape.** Le robot n'est jamais atteignable directement depuis un backtest.

### 5.2 Les trois couches étanches

C'est la contrainte structurante du projet. Ne les mélange jamais.

| Couche | Objet | Phases | Influence externe |
|---|---|---|---|
| **A** — Recherche | `META_ALPHA_RESEARCH_PORTFOLIO` | P2 → P6 | **AUCUNE.** Le challenge ne dicte pas ce que le moteur trouve. |
| **B** — Portefeuille | `META_ALPHA_PORTFOLIO` | P7 | **AUCUNE.** Les poids viennent des données autorisées, jamais du challenge. |
| **C** — Adaptateur | `BLUE_GUARDIAN_CHALLENGE_ADAPTER` | P8 → P9 | Règles du challenge, **postérieures**, jamais rétroactives. |

**Conséquence opérationnelle :** si une règle Blue Guardian est incompatible avec une règle de portefeuille, tu **signales l'incompatibilité** et tu crées une **version d'adaptation séparée**, elle-même testée. Tu ne modifies **jamais** silencieusement le résultat scientifique pour qu'il rentre dans le challenge.

### 5.3 Les 9 phases et leurs gates

Source de vérité : `metaalpha/mission.py` (structure) et `docs/ARCHITECTURE_COMPLETE_V2.html` (rendu).

| Phase | Rang | Couche | Entrée | Sortie |
|---|---|---|---|---|
| `P1_CERTIFIED` | 0 | A | — | déjà CERTIFIED, ne pas reconstruire |
| `P2H_CERTIFIED` | 1 | A | — | déjà CERTIFIED, ne pas reconstruire |
| `P2_ANALYTICAL` | 2 | A | P1+P2H CERTIFIED, hashes reconfirmés, 348 partitions lisibles | `P2_TO_P3_GATE_V1` : toutes les variables `AVAILABLE_FOR_MINING` ont un audit causal PASS |
| `P3_MINING` | 3 | A | gate P2 PASS + revue propriétaire | tous les essais enregistrés, candidats listés |
| `P4_VALIDATION` | 4 | A | P3 acceptée | chaque candidat a un contrat d'exécution + anti-look-ahead PASS |
| `P5_STRESS` | 5 | A | P4 acceptée | stress préenregistrés exécutés |
| `P6_QUALIFICATION` | 6 | A | P5 acceptée | chaque candidat porte `LOCKED_FOR_HOLDOUT`, `REJECTED` ou `DEFERRED` |
| `P7_PORTFOLIO` | 7 | B | P6 acceptée, ≥1 edge LOCKED | poids estimés puis **gelés** |
| `P8_HOLDOUT` | 8 | C | **AUTORISATION EXPLICITE** + `FINAL_LOCK_MANIFEST` | Holdout ouvert **une fois**, miroir sans écart |
| `P9_MQL5` | 9 | C | P8 validée + **AUTORISATION DISTINCTE** | parité prouvée + shadow/demo + readiness |

**Statuts terminaux** (`metaalpha/governance.py`) :
`PHASE_COMPLETE_AWAITING_OWNER_REVIEW` · `BLOCKED_WITH_RESUME` · `FAILED_TECHNICAL` · `INCOMPLETE` · `NO_EDGE`

**Deux autorisations distinctes, jamais confondues :** l'ouverture du Holdout (P8) et le déploiement réel (P9). Obtenir l'une ne donne pas l'autre.

### 5.4 Qui exécute quoi

| Composant | Rôle | Ce qu'il ne fait pas |
|---|---|---|
| **GitHub Actions** | orchestrateur déterministe : déclenche, vérifie les gates, écrit les checkpoints, reprend | ne calcule pas, ne décide pas, jamais plus de 6 h par job |
| **Kaggle** | calcul jetable : une partition ou un segment, écrit résultat + hash | rien d'irremplaçable n'y vit |
| **Google Drive** | stockage durable : certificats, partitions, registres, checkpoints | n'est pas un système de calcul |
| **Propriétaire** | 11 points de décision, voir §5.5 | ne fournit ni formule, ni poids, ni edge |

### 5.5 Les 11 points où le propriétaire est requis

Ce sont les seuls. Tout le reste est automatisable et **doit** l'être.

1. `P2_ANALYTICAL` — répondre aux 9 décisions de définition (~10 min, une fois)
2. `P2_ANALYTICAL` — accepter ou refuser la phase après revue
3. `P3_MINING` — accepter
4. `P4_VALIDATION` — accepter
5. `P5_STRESS` — accepter
6. `P6_QUALIFICATION` — accepter
7. `P7_PORTFOLIO` — accepter
8. `P8_HOLDOUT` — **autoriser l'ouverture du Holdout** (jamais automatique)
9. `P8_HOLDOUT` — accepter
10. `P9_MQL5` — fournir `BLUE_GUARDIAN_ACCOUNT_SPEC` (donnée propriétaire)
11. `P9_MQL5` — **autoriser le déploiement réel** (distinct de l'autorisation Holdout)

### 5.6 Le cycle autonome

Une fois une phase autorisée, le système doit tourner seul :

```
03:00 UTC  ORCHESTRATEUR réveille la phase autorisée
           ├── vérifie KILL_SWITCH, budget, leases
           ├── recalcule le SHA-256 des 2 certificats
           ├── confirme 348 partitions + schéma inchangé
03:05      ├── découpe en unités (partition / segment d'hypothèses)
03:06      ├── dispatch vers le runtime jetable, N unités en parallèle
           │      chaque unité écrit : résultat + hash + checkpoint
           │      une unité perdue est replanifiée, jamais dupliquée
04:20      ├── agrège, vérifie la cohérence, écrit les rapports
           ├── évalue le gate de sortie
           │
           ├── GATE PASS → PHASE_COMPLETE_AWAITING_OWNER_REVIEW
           │               et ATTEND. N'enchaîne pas seul.
           └── GATE FAIL → BLOCKED_WITH_RESUME
                           cause exacte écrite, phase suivante fermée
```

**Point capital :** le système avance seul **à l'intérieur** d'une phase autorisée. Il s'arrête de lui-même au gate. Il ne franchit jamais un gate sans acceptation humaine.

---

## 6. Le code existant — inventaire complet

**Localisation chez le rédacteur :** `/home/user/META_ALPHA`
**Volume :** 8 330 lignes de Python, 143 tests verts, 0 échec.

Tu dois d'abord récupérer ce code. Voir §7.

### 6.1 Modules, par rôle

#### Fondations

| Module | Lignes | Rôle |
|---|---|---|
| `config.py` | 110 | hash, JSON canonique, constantes |
| `fs.py` | 198 | `Storage` : écriture atomique, allowlist, refus d'écrire dans le corpus certifié |
| `duck.py` | ~60 | connexion DuckDB **bornée** — refuse toute connexion sans limite mémoire |
| `remote.py` | 219 | `Remote` Protocol · `LocalRemote` · `DriveRemote` (compte de service) |

`fs.py` mérite une lecture. Trois garanties : allowlist d'écriture (impossible d'écrire hors zone de recherche), écriture atomique (`.tmp` → validation → rename), hash systématique. `PROTECTED_DIRS = ("00_RAW", "01_PARQUET", "04_CHECKPOINTS", "02_", "03_")`.

#### Gouvernance

| Module | Lignes | Rôle |
|---|---|---|
| `governance.py` | 294 | `Phase` enum, `assert_phase_authorized`, sceau Holdout, `assert_not_killed`, budget, `CostKind` |
| `leases.py` | 86 | verrous d'exécution — un seul agent écrit à la fois |
| `checkpoints.py` | 106 | reprise : ne rejoue que les unités inachevées |
| `preflight.py` | 158 | contrôles préalables d'environnement |

`governance.py` contient le sceau du Holdout : `seal_holdout()` / `open_holdout_once()`. Le second refuse une seconde ouverture. **Ne le contourne jamais.**

#### Science — couche analytique

| Module | Lignes | Rôle |
|---|---|---|
| `families.py` | 358 | les **8 familles** du §4.2, les **9 décisions** sans défaut, les 8 dépendances externes différées |
| `contracts_engine.py` | 318 | `detect_fields`, `instantiate_families`, `derive_sample`, `extract_questions` |
| `decisions.py` | 236 | `record_answers` (refuse `answered_by != "HUMAN"`), instanciation, CLI |
| `registry.py` | 177 | Variable Registry, Formula Registry, Trial Ledger — **immuables** |
| `inventory.py` | 125 | L0/L1 : énumération, lecture de footers, signatures de schéma |
| `extraction_ladder.py` | 301 | les 8 barreaux L0→L7 et l'avancement automatique |
| `extract.py` | 308 | L6/L7 : extraction de la matrice par partition, manifeste |

#### Exécution

| Module | Lignes | Rôle |
|---|---|---|
| `dispatch.py` | 385 | répartition en unités, `enable_gpu: False` |
| `segment.py` | 246 | exécution d'un segment, garde-fou disque, publication |
| `orchestrator.py` | 260 | boucle principale |
| `bench.py` | 141 | benchmarks honnêtes |
| `ai_supervisor.py` | 150 | superviseur IA optionnel, **jamais requis** pour un calcul |

#### Accès et sécurité

| Module | Lignes | Rôle |
|---|---|---|
| `drive_preflight.py` | 166 | vérifie certificats + SHA-256 + 348 partitions. **Point d'entrée n°1.** |
| `oauth_drive.py` | 190 | OAuth utilisateur, scope `drive.readonly` strict |
| `connect_app.py` | 367 | serveur du bouton « Se connecter à Drive » |
| `secrets_guard.py` | 147 | détection de secrets dans l'arbre |
| `mission.py` | 566 | **le contrat de mission** : phases, gates, règles BG, catalogue des secrets |

`mission.py` est le fichier à lire en premier après ce document. Il contient la structure exécutable de tout le projet, et `docs/ARCHITECTURE_COMPLETE_V2.html` en est le rendu généré — un test vérifie qu'ils ne peuvent pas diverger.

### 6.2 Les 28 artéfacts et leur phase propriétaire

Chaque artéfact a **une et une seule** phase propriétaire. `mission.py` lève une erreur si deux phases revendiquent le même.

**Données et spécifications :** `BASELINE_HASH_MANIFEST.json` · `QUOTE_DGP_SPEC_V1.md` · `GRANULARITY_SPEC_V1.json` · `VALIDATION_SPLITS_V1.json`
**Variables et hypothèses :** `DGP_VARIABLE_REGISTRY_V1.json` · `FORMULA_REGISTRY_V1.json` · `TRIAL_LEDGER.csv` · `ANOMALY_CANDIDATE_REGISTRY.json` · `REJECTED_AND_INCONCLUSIVE.csv`
**Validation :** `CAUSALITY_REPORT.json` · `WALK_FORWARD_RESULTS.parquet` · `TRADE_LEDGER.parquet` · `TRIAL_STATISTICS.json` · `STRESS_RESULTS.parquet` · `COST_SENSITIVITY.json` · `REGIME_STABILITY.parquet` · `NEGATIVE_CONTROLS.json`
**Edges et portefeuille :** `QUALIFIED_EDGE_REGISTRY.json` · `REJECTED_AND_DEFERRED.csv` · `SLEEVE_RETURNS.parquet` · `CORRELATION_EXPOSURE_REPORT.json` · `PORTFOLIO_POLICY.json` · `PORTFOLIO_LEDGER.parquet` · `PORTFOLIO_REPORT.json` · `FINAL_LOCK_MANIFEST.json`
**Blue Guardian :** `BLUE_GUARDIAN_RULES_UNCERTAINTY_REGISTER.json` · `BLUE_GUARDIAN_ACCOUNT_SPEC.json` · `BLUE_GUARDIAN_CHALLENGE_SIMULATION.json` · `EXECUTION_COST_MODEL.json` · `SYMBOL_RUNTIME_SPEC.json`
**Finalisation :** `FINAL_HOLDOUT_REPORT.json` · `GOLDEN_VECTORS.parquet` · `INDEPENDENT_MIRROR_REPORT.json` · `FINAL_CERTIFICATE.json` · `EA_SPEC.json` · `MQL5_PARITY_REPORT.json` · `DEPLOYMENT_READINESS.json`

**Un artéfact n'est créé qu'à sa phase.** Ne pré-génère rien.

### 6.3 Les 8 familles et les 11 variables

Source : §4.2 du dossier de stratégie. Encodées dans `families.py`.

| Famille | Variables | Statut initial |
|---|---|---|
| F1 Prix & cotations | `SPREAD_ABS`, `SPREAD_REL`, `MID` | **`SPECIFIED` immédiatement** — aucun paramètre libre |
| F2 Rendements | `RET_TICK`, `RET_H` | `RET_TICK` dérivable ; `RET_H` bloqué par `D_HORIZONS` |
| F3 Volatilité | `ROLL_STD_MID`, `ROLL_RANGE_MID` | bloqués par `D_FENETRES_VOL` + `D_WARMUP_NULL` |
| F4 Sauts & extrêmes | `ZSCORE_ROBUST` | bloqué par `D_SEUIL_SAUT` + `D_FENETRES_VOL` |
| F5 Microstructure | `UPDATE_INTENSITY`, `INTERARRIVAL_MEAN`, `SPREAD_REGIME` | bloqués par `D_INTENSITE_T` + `D_REGIME_SPREAD` |
| F6 Structure temporelle | `SUBPERIODE` | bloqué par `D_TIMEZONE_SESSIONS` |
| F7 Régimes | `REGIME_CLASS` | bloqué par `D_METHODE_REGIME` |
| F8 Labels | `MFE_H`, `MAE_H` | bloqués par `D_HORIZON_LABEL` |

**Dérivables sans aucune décision :** `SPREAD_ABS`, `SPREAD_REL`, `MID`, `RET_TICK`. La famille F1 est donc `SPECIFIED` dès le départ — le système travaille sans attendre personne.

**Les 8 dépendances externes, différées et jamais remplacées par un proxy** (`replaced_by_proxy: INTERDIT`) : COMEX/GC futures · DXY exact · LBMA fixings · Macro point-in-time · Taux d'intérêt · VIX · Indices actions · Autres marchés.

### 6.4 Les 9 décisions irréductibles

Toutes ont `default_is = "AUCUN_DEFAUT"`. **Aucune n'a de valeur par défaut.** Une décision non répondue laisse la variable bloquée — c'est le comportement voulu.

| ID | Question | Bloque | Exemples |
|---|---|---|---|
| `D_HORIZONS` | Quels horizons temporels de label préenregistrer ? | `RET_H` | `1s`, `5s`, `30s`, `1min`, `5min` |
| `D_FENETRES_VOL` | Quelles fenêtres pour la volatilité roulante ? | `ROLL_STD_MID`, `ROLL_RANGE_MID`, `ZSCORE_ROBUST` | `50`, `100`, `500`, `1000` |
| `D_WARMUP_NULL` | Politique de warm-up : NULL ou suppression de lignes ? | toutes les roulantes | `NULL`, `DROP_ROWS` |
| `D_SEUIL_SAUT` | Quel seuil pour qualifier un saut ? | `ZSCORE_ROBUST` | `3`, `4`, `5`, `6` |
| `D_INTENSITE_T` | Quelle durée pour mesurer l'intensité des quotes ? | `UPDATE_INTENSITY`, `INTERARRIVAL_MEAN`, `SPREAD_REGIME` | `1s`, `5s`, `30s` |
| `D_REGIME_SPREAD` | Combien de classes de spread, sur quelle fenêtre ? | `INTERARRIVAL_MEAN`, `SPREAD_REGIME`, `UPDATE_INTENSITY` | `3 classes / 1 jour`, `3 classes / 1 semaine`, `5 classes / 1 jour` |
| `D_TIMEZONE_SESSIONS` | Fuseau et découpage des sessions ? | `SUBPERIODE` (sinon F6 entière passe `DEFERRED`) | `UTC + aucune session`, `UTC + sessions documentées`, `DEFERRED` |
| `D_METHODE_REGIME` | Méthode de classification de régime ? | `REGIME_CLASS` | `quantiles de volatilité / 3`, `HMM / 3`, `DEFERRED` |
| `D_HORIZON_LABEL` | Horizon pour MFE/MAE ? | `MFE_H`, `MAE_H` (fixe aussi le purge §7.2) | `30s`, `5min`, `1h` |

**Mécanisme de réponse :**

```bash
python -m metaalpha.decisions --template        # écrit un gabarit, tous les champs à null
# le propriétaire remplit le fichier
python -m metaalpha.decisions --apply answers.json
```

`record_answers` **refuse** toute attribution autre que `HUMAN` (`OwnerAttributionError`). Un agent ne peut pas répondre à la place du propriétaire. **Ne cherche pas à contourner cela.** Si le propriétaire ne répond pas, le système reste bloqué à `L5_ENRICHISSEMENT` — et c'est correct.

### 6.5 Les 8 barreaux de l'extraction

`extraction_ladder.py`. Ce sont les étapes L0→L7, distinctes des phases P2→P9.

| Barreau | Question | Critère | Auto ? |
|---|---|---|---|
| `L0_DECOUVERTE` | qu'y a-t-il sous la racine ? | ≥1 Parquet lisible | oui |
| `L1_TOPOLOGIE` | combien de partitions, quels schémas ? | `total_rows > 0`, un schéma canonique | oui |
| `L2_INTEGRITE` | chaque partition est-elle utilisable ? | 0 illisible, timestamp croissant, spread ≥ 0 | oui |
| `L3_DERIVATION` | le prix reconstruit est-il cohérent ? | `MID`, `SPREAD_ABS`, `SPREAD_REL`, `RET_TICK` calculés | oui |
| `L4_MESURE` | à quoi ressemblent les distributions ? | quantiles, inter-arrivées, doublons, trous | oui |
| `L5_ENRICHISSEMENT` | quelles variables paramétrées existent ? | 9 décisions → 11 variables | **NON — humain** |
| `L6_EXTRACTION` | peut-on produire la matrice ? | matrice écrite par partition, checkpoints | oui |
| `L7_CONTRAT` | la matrice est-elle opposable ? | manifeste + sha256 + lignée | oui |

**L'échelle a été exécutée de bout en bout sur corpus synthétique** : L0→L4 sans intervention, arrêt net à L5 avec la cause exacte, puis L6→L7 après réponses. Relance : 0 unité refaite, 3 ignorées (idempotence prouvée).

**Note importante sur L6 :** sur 11 variables instanciées, **9 sont refusées** par `plan_extraction` avec la cause `FORMULE_NON_CERTIFIEE` — leur formule n'est pas encore traduite en SQL de façon certifiée. Seules `MID`, `SPREAD_ABS`, `RET_TICK`, `SPREAD_REL`, `ROLL_STD_MID`, `ROLL_RANGE_MID` sont traduisibles à ce jour. **Ce n'est pas un bug.** Le système préfère ne pas extraire plutôt qu'extraire faux. Compléter les traductions manquantes est un travail légitime — mais chaque traduction doit être écrite, testée, et **la formule doit venir du Formula Registry**, jamais inventée sur place.

---

## 7. Ta première heure — procédure exacte

### Étape 1 — Récupérer le code

Le code est chez le rédacteur, dans `/home/user/META_ALPHA`. Demande-le au propriétaire (il peut te l'envoyer en archive). Si tu ne l'as pas, **ne réécris pas tout** : demande-le. Ce serait des heures perdues et un risque de divergence.

Structure attendue :

```
META_ALPHA/
├── metaalpha/            # 24 modules
├── tests/                # 11 fichiers, 143 tests
├── scripts/              # démos, rendu du schéma, installation du hook
├── config/execution_config.json
├── contracts/            # préautorisation, politique propriétaire
├── docs/                 # 6 documents dont 2 rendus générés
├── .github/workflows/    # 5 workflows
├── .githooks/pre-commit
├── README.md
├── SECURITY.md
└── requirements*.txt
```

Vérifie immédiatement :

```bash
cd META_ALPHA
pip install -r requirements.txt
python -m pytest tests/ -q          # attendu : 143 passed
```

Si ce n'est pas 143, **arrête-toi et rapporte**. Ne « répare » pas à l'aveugle.

### Étape 2 — Créer le dépôt GitHub

Le propriétaire veut le projet **public**. C'est une décision explicite, prise en connaissance de cause, assumée par lui et son conseil (« c'est un risque que je suis d'accord de prendre »). Ne discute pas cette décision, mais **applique les contre-mesures du §8**.

Procédure :

1. Créer un dépôt **public**, nom suggéré `meta-alpha-xauusd`, **sans** README ni `.gitignore` ni licence (le code les apporte).
2. Le code part sur la branche `main`.
3. **Avant le premier push**, exécuter les trois vérifications du §8.3.

```bash
cd META_ALPHA
python scripts/install_hooks.py       # hook pre-commit anti-secret
git init -b main
git add -A
git commit -m "META ALPHA: infrastructure de recherche, 143 tests"
git remote add origin git@github.com:<compte>/meta-alpha-xauusd.git
git push -u origin main
```

Si le hook refuse le commit, **c'est qu'il a raison** : un secret est présent. Corrige, ne désactive pas le hook.

### Étape 3 — Configurer l'accès aux données

Deux chemins. **Le second est obligatoire pour du 24/7**, le premier ne suffit pas.

#### 3.a — Le bouton de connexion (pour choisir et confirmer le Drive)

Le rédacteur a écrit un serveur : `metaalpha/connect_app.py`.

```bash
python -m metaalpha.connect_app --port 8000
```

La page propose un formulaire de configuration initiale, puis le bouton « Se connecter à Drive ». Google affiche son propre sélecteur de compte. La page déduit automatiquement son URI de redirection de l'en-tête `Host` (fonctionne derrière un proxy).

**Si tu as un accès Drive direct et que tu sais déjà quel compte contient le corpus, tu peux sauter cette étape.** Elle existe pour un humain qui doit choisir un compte. Toi, tu peux aller directement au préflight.

Le scope est `drive.readonly` **strictement**. Un test vérifie qu'aucun scope d'écriture n'existe (`tests/test_oauth_drive.py::test_scope_is_readonly_only`). Ne l'élargis pas.

#### 3.b — Le compte de service (obligatoire pour l'exploitation)

Un robot Google sans mot de passe, qui n'a accès qu'au dossier partagé avec lui.

1. Le propriétaire (ou toi, si tu as les droits) crée un compte de service dans Google Cloud, active l'API Drive, génère une clé JSON.
2. Le dossier `META_ALPHA_XAUUSD_DGP` est partagé avec l'email du compte de service, permission **Lecteur**.
3. Deux secrets GitHub : `GDRIVE_SA_JSON` (tout le JSON) et `GDRIVE_ROOT_FOLDER_ID` (l'ID du dossier racine).

Ces secrets vont dans **GitHub Secrets**, jamais dans le dépôt. `metaalpha/secrets_guard.py` refuse leur présence dans l'arbre.

### Étape 4 — Le préflight, et c'est le moment de vérité

```bash
export GDRIVE_SA_JSON="$(cat sa.json)"
export GDRIVE_ROOT_FOLDER_ID="<id>"
python -m metaalpha.drive_preflight
```

**Résultat attendu :**

```json
{
  "status": "PASS",
  "baseline_manifest": {
    "p1_sha256_canonical": "…",
    "p2_sha256_canonical": "…",
    "partitions_count": 348,
    "ticks_expected": 685118625
  }
}
```

**Si ce n'est pas PASS**, `drive_preflight.py` te dit exactement pourquoi, avec un code :

| Code | Signification | Action |
|---|---|---|
| `NO_REMOTE_BACKEND` | variables d'environnement absentes | les exporter dans le même shell |
| `CERTIFICATE_MISSING` | mauvais dossier racine | vérifier `GDRIVE_ROOT_FOLDER_ID` : c'est le dossier qui **contient** `04_CHECKPOINTS/`, pas un sous-dossier |
| `CERTIFICATE_NOT_CERTIFIED` | un certificat porte un statut ≠ CERTIFIED | **ARRÊT.** Ne continue pas. Rapporte. |
| `PARTITION_COUNT_MISMATCH` | 347 ou 349 partitions | **ARRÊT.** Le corpus ne correspond pas au certificat. Rapporte l'écart exact. |
| `PARTITION_NAMING_UNEXPECTED` | noms de fichiers différents | **ARRÊT.** Rapporte. |

**Ces refus sont la fonctionnalité, pas un obstacle.** Un système qui accepte 347 partitions en disant « presque 348 » n'est pas un système scientifique.

Les deux `sha256_canonical` obtenus deviennent la **référence inviolable**. Écris-les dans `BASELINE_HASH_MANIFEST.json`. Toute exécution ultérieure les recalcule et refuse d'avancer si l'un a changé.

### Étape 5 — Découvrir le schéma réel

Jamais fait. C'est ta première contribution scientifique.

```python
from metaalpha.inventory import build_inventory
inv = build_inventory("<chemin>/PARTITIONS")
print(f"{inv['files_found']} fichiers, {inv['total_rows']:,} lignes")
print(f"{len(inv['schema_signatures'])} signature(s) de schéma")
print(inv["partitions"][0]["field_mapping"])
print(inv["partitions"][0]["unmapped_columns"])
```

Vérifie :
- `files_found == 348`
- `total_rows == 685_118_625` ← **si ce total diffère, arrête-toi**
- `schema_heterogeneous == False`
- le mapping `timestamp` / `bid` / `ask` est complet

Puis regarde les **colonnes non mappées** (`unmapped_columns`). Elles peuvent contenir des champs utiles (volume de ticks, flags) ou des champs interdits. `FIELD_ALIASES` dans `contracts_engine.py` gère les alias courants. Si tu découvres un alias légitime, ajoute-le **avec un test**.

**Documente ce que tu trouves dans `QUOTE_DGP_SPEC_V1.md`** : fuseau, précision, doublons, égalités de timestamp, gaps, quotes invalides, champs supplémentaires. C'est un livrable de la phase 2 analytique, pas une note informelle.

### Étape 6 — Faire monter l'échelle

```python
from metaalpha.extraction_ladder import advance
rep = advance(storage, "<racine du corpus>")
print(rep["ladder"]["current_level"])
print(rep["ladder"]["why"])
```

Le système monte seul jusqu'à **L4_MESURE**, puis s'arrête à **L5_ENRICHISSEMENT** en disant : « il me manque 9 décisions de définition, voici lesquelles, avec leur conséquence ».

**C'est ici, et seulement ici, que tu vas voir le propriétaire.** Tu lui présentes les 9 questions du §6.4 avec leurs exemples et leurs conséquences. Il répond en ~10 minutes. Tu enregistres ses réponses avec `record_answers`, qui refuse toute autre attribution que `HUMAN`.

Puis tu relances `advance`, et le système repart seul jusqu'à L7.

**Ne réponds jamais à sa place**, même si une valeur te semble évidente. Même si tu penses qu'il dirait « 500 ». C'est sa décision scientifique, et le système entier repose sur le fait qu'elle soit traçable jusqu'à lui.

---

## 8. Sécurité — le dépôt public

Le projet est public par décision du propriétaire. C'est assumé. **Ta responsabilité est que cela ne coûte rien.**

### 8.1 Ce qui ne doit JAMAIS être versionné

| Élément | Où il vit |
|---|---|
| `sa.json`, toute clé de compte de service | GitHub Secret `GDRIVE_SA_JSON` |
| ID du dossier racine Drive | GitHub Secret `GDRIVE_ROOT_FOLDER_ID` |
| Token Kaggle (`KGAT…`) | GitHub Secrets `KAGGLE_USERNAME` + `KAGGLE_KEY` |
| Certificats Phase 1 / Phase 2 | Drive, lecture seule |
| 348 partitions Parquet | Drive |
| État de gouvernance, décisions, approbations | Drive, `RESEARCH_V1_XAUUSD_TICK_ONLY/00_GOVERNANCE/` |
| Résultats non publiés | Drive |

### 8.2 Trois barrières indépendantes, déjà en place

1. **`.gitignore`** — bloque `*.parquet`, `sa.json`, `service_account*.json`, `.env*`, `*.pem`, `*.key`, `00_RAW/`, `01_PARQUET/`, `04_CHECKPOINTS/`.
2. **Hook pre-commit** (`.githooks/pre-commit`, installé par `python scripts/install_hooks.py`) — refuse le commit sur motif de secret.
3. **CI** (`.github/workflows/ci.yml`, job `secrets`) — scanne l'arbre à chaque push et pull request.

Motifs détectés par `secrets_guard.py` : `KGAT_` (Kaggle) · `AIza` (Google) · `GOCSPX-` (OAuth) · `ghp_`/`gho_`/`ghs_`/`ghu_`/`ghr_` (GitHub) · `AKIA` (AWS) · `-----BEGIN … PRIVATE KEY-----` · `xox[baprs]-` (Slack) · `Bearer eyJ…` · forme JSON de compte de service.

15 tests couvrent la détection **et** les faux positifs. Exécution manuelle : `python metaalpha/secrets_guard.py .`

### 8.3 Ce que le garde-fou ne peut PAS faire — à savoir

- Il ne détecte pas une clé **reformatée** ou **encodée** hors motifs connus.
- Il ne protège pas un secret commité puis supprimé : **l'historique git le garde**. Sur un dépôt public, réécrire l'historique ne sert à rien — l'information est déjà copiée. **La seule réponse correcte est de révoquer la clé.**
- Il ne peut pas empêcher quelqu'un de coller une clé dans une issue ou une pull request, qui sont publiques.

### 8.4 Si une clé fuite

1. Révoquer chez le fournisseur — **immédiatement**.
2. Émettre une nouvelle clé.
3. Mettre à jour le GitHub Secret.
4. Écrire l'incident dans `00_GOVERNANCE/INCIDENTS.md`.

Rien d'autre n'est utile.

### 8.5 Ce que tu ne dois jamais faire avec les identifiants

- Jamais demander un mot de passe Google au propriétaire.
- Jamais coller un secret dans une conversation, un notebook, un rapport, un commit.
- Jamais écrire un jeton sur disque : `oauth_drive.py` les garde en mémoire, un test le vérifie.
- Jamais élargir le scope OAuth au-delà de `drive.readonly`.

---

## 9. Les moteurs qui restent à écrire

Le rédacteur ne les a **pas** écrits. C'était volontaire, et voici pourquoi : les écrire contre un schéma de corpus qu'il n'avait pas vu aurait figé des hypothèses fausses, qu'il aurait fallu défaire ensuite. **Toi, tu auras vu le corpus. Écris-les après l'étape 5 du §7.**

Chaque moteur suit le même contrat : entrée = unités de travail + état de gouvernance ; sortie = artéfacts de la phase + statut honnête ; jamais d'écriture hors zone de recherche.

### 9.1 P3 — Mining préenregistré

**Fichier à créer :** `metaalpha/mining.py`
**Artéfacts :** `ANOMALY_CANDIDATE_REGISTRY.json`, `REJECTED_AND_INCONCLUSIVE.csv`, `TRIAL_LEDGER.csv`, `MINING_REPORT.json`

Contrat :
1. **Inscrire chaque essai au Trial Ledger AVANT de l'exécuter.** ID, hypothèse falsifiable, famille, formule/version, variables, paramètres, label/horizon, baseline, test nul, contrôle négatif, métrique, période autorisée, critères d'acceptation/rejet, hashes du code et de la config.
2. N'utiliser **que** les variables `AVAILABLE_FOR_MINING`.
3. Calculer baseline et contrôle négatif pour **chaque** essai. Un essai sans contrôle négatif est invalide.
4. **Conserver tous les essais** : positifs, négatifs, nuls, non concluants, erreurs. `TRIAL_LEDGER.csv` est append-only.
5. Un candidat de P3 n'est **pas** un edge. Ne l'appelle jamais ainsi.

`registry.py` fournit déjà `log_trial()` et `count_trials()`. Le Trial Ledger existe et est immuable.

**La multiplicité des tests est le piège central de cette phase.** Si tu testes 200 hypothèses, tu trouveras des résultats « significatifs » par hasard. Le Trial Ledger existe pour rendre ce nombre visible et pour l'intégrer aux statistiques. Ne le contourne pas en testant ailleurs.

### 9.2 P4 — Validation et causalité

**Fichier à créer :** `metaalpha/validation.py`
**Artéfacts :** `CAUSALITY_REPORT.json`, `WALK_FORWARD_RESULTS.parquet`, `TRADE_LEDGER.parquet`, `TRIAL_STATISTICS.json`

Contrat :
1. Pour chaque candidat, spécifier : activation, direction, timestamp de décision, entrée, sortie, horizon de détention, invalidation, absence de signal, exposition, règle de risque, coûts, modèle d'exécution.
2. **Vérifier que chaque feature est disponible au timestamp de décision.** Anti-look-ahead : une variable calculée avec `lag()` ou une fenêtre `ROWS BETWEEN n PRECEDING AND CURRENT ROW` est causale ; une fenêtre qui inclut `FOLLOWING` ne l'est pas. `derive_sample` n'utilise que `lag()` — vérifié par construction.
3. IS, OOS chronologique, walk-forward. **Jamais de split aléatoire.**
4. Statistiques adaptées à la dépendance temporelle et à la multiplicité : block bootstrap, ou test de permutation préservant l'ordre, pas un t-test naïf.
5. **Replay événementiel Bid/Ask :** achat à l'Ask, vente au Bid, sortie sur le côté opposé. Distinguer le timestamp du signal, l'arrivée de l'ordre, et le fill. **Ne remplis pas au même quote que le signal** sans un modèle de latence préenregistré.
6. Séparer spread, commission, swap, slippage, latence.

**Règle économique absolue :** coût inconnu ≠ zéro. Sans coût complet confirmé, étiquette `GROSS` ou `CONDITIONAL`. **Jamais `NET`.** `governance.py` expose `CostKind` et `assert_cost_semantics` pour cela.

### 9.3 P5 — Stress et stabilité

**Fichier à créer :** `metaalpha/stress.py`
**Artéfacts :** `STRESS_RESULTS.parquet`, `COST_SENSITIVITY.json`, `REGIME_STABILITY.parquet`, `NEGATIVE_CONTROLS.json`

Stress **préenregistrés uniquement** : spread observé et scénarios adverses, commission, swap, slippage, latence, stabilité par sous-période, stabilité par régime, contrôles négatifs.

**Un scénario hypothétique est marqué comme scénario**, jamais présenté comme un fait historique.

### 9.4 P6 — Qualification

**Fichier à créer :** `metaalpha/qualification.py`
**Artéfacts :** `QUALIFIED_EDGE_REGISTRY.json`, `REJECTED_AND_DEFERRED.csv`, `CANDIDATE_LOCK_MANIFEST.json`

Appliquer les critères **gelés** de `OWNER_POLICY_V1.json`. **Pas de nouveau tuning.** Chaque candidat reçoit `LOCKED_FOR_HOLDOUT`, `REJECTED` ou `DEFERRED`, avec son motif.

`NO_EDGE` est un résultat valide et complet. Si aucun candidat ne survit, produis `NO_EDGE` et arrête-toi. Ne cherche pas une variante qui passerait.

### 9.5 P7 — Portefeuille

**Fichier à créer :** `metaalpha/portfolio.py`
**Artéfacts :** `SLEEVE_RETURNS.parquet`, `CORRELATION_EXPOSURE_REPORT.json`, `PORTFOLIO_POLICY.json`, `PORTFOLIO_LEDGER.parquet`, `PORTFOLIO_REPORT.json`, `FINAL_LOCK_MANIFEST.json`

Analyser : corrélation des rendements par période et régime, corrélation conditionnelle, chevauchement des signaux et positions, pertes simultanées et co-drawdowns, concentration temporelle, turnover, contribution marginale au risque et au rendement, stabilité des poids.

Évaluer chaque sleeve seule, puis les combinaisons. Vérifier qu'une sleeve ajoute une **diversification réelle** — pas une variante corrélée.

**Poids estimés sur données autorisées par une méthode documentée, puis GELÉS avant le test final.** Pas d'optimisation full-sample, pas de réglage sur le Holdout.

Si un seul edge survit, le portefeuille est une seule sleeve. Si aucun, portefeuille inactif + `NO_EDGE`.

### 9.6 P8 — Holdout et miroir

**Fichier à créer :** `metaalpha/holdout.py`
**Artéfacts :** `FINAL_HOLDOUT_REPORT.json`, `GOLDEN_VECTORS.parquet`, `INDEPENDENT_MIRROR_REPORT.json`, `FINAL_CERTIFICATE.json`

**N'exécute cette phase qu'après autorisation explicite du propriétaire.** `governance.py` fournit `seal_holdout()` et `open_holdout_once()` — le second refuse une seconde ouverture.

Ouvrir le dernier segment Holdout **une seule fois**, tester le système entièrement gelé, **ne rien retuner**, produire performance, incertitude, coûts, risques.

Construire une implémentation **indépendante** des éléments critiques, puis comparer timestamps, signaux, directions, fills, coûts, P&L. **Tout écart inexpliqué sur un ordre, un timestamp, un fill ou le P&L est un échec du miroir.**

Le split est 60 % IS / 20 % OOS / 20 % Holdout, calculé par durée calendaire, avec purge/embargo fondé sur le plus long horizon pertinent. **Aucun split aléatoire.**

### 9.7 P9 — Robot MQL5 et adaptateur Blue Guardian

**Fichiers à créer :** `metaalpha/bg_adapter.py`, `metaalpha/ea_spec.py`
**Artéfacts :** les 5 de Blue Guardian + `EA_SPEC.json`, `MQL5_PARITY_REPORT.json`, `DEPLOYMENT_READINESS.json`

**Traduction mécanique** de la logique gelée. Aucune réinterprétation.

Comparer Python et MQL5 sur les mêmes quotes. Tester rejets serveur, redémarrage, état, quotes périmées, limites de volume, clôtures. Shadow/demo avant toute readiness.

**Une compilation ne prouve pas la parité.** Aucun déploiement réel sans autorisation distincte de celle du Holdout.

---

## 10. Blue Guardian — la couche C

**Le challenge ne dicte pas ce que le moteur trouve.** Il intervient après la recherche, pour évaluer l'exécutabilité.

### 10.1 Les règles rapportées (PDF daté du 20/09/2026)

23 règles dans `mission.py::BG_REPORTED_RULES`. **Aucune n'est une vérité actuelle.** Le registre d'incertitude les marque.

| Règle | Valeur | Statut |
|---|---|---|
| Phase 1 objectif | 10 % | REPORTED |
| Phase 2 objectif | 4 % | REPORTED |
| Durée | illimitée | REPORTED |
| Jours rentables | 4 jours à 0,5 %/jour | REPORTED |
| Daily loss | 4 % du solde initial, reset 17:00 EST | REPORTED |
| **Drawdown maximum** | 10 % trailing puis verrouillage au solde de départ | **CONTRADICTION_DOCUMENTAIRE** |
| Profit split | 85 % / add-on 90 % | REPORTED |
| Premier payout | 14 jours (add-on 7) | REPORTED |
| Consistency funded | 25 % | REPORTED |
| Retrait minimum | 100 USD crypto / 500 USD Rise | REPORTED |
| EA | autorisés | REPORTED |
| Overnight / week-end | autorisé | REPORTED |
| News challenge | autorisé | REPORTED |
| News funded | restreint, fenêtre 5 min | REPORTED |
| **Durée minimale de détention** | **2 minutes** | **BLOQUANT_POUR_L_ARCHITECTURE** |
| **HFT / tick scalping / arbitrage** | **interdits** | **BLOQUANT** |
| Commission Commodities | 5 USD/lot | REPORTED |
| Mode de facturation commission | non publié | NOT_PUBLIC |
| Swap et taux | non publiés | NOT_PUBLIC |
| Stop Out | 100 % | REPORTED |
| Guardian Shield funded | 2 % de PnL flottant global | REPORTED |
| Compte personnel, appareil non partagé | exigé | REPORTED |
| Changement de plateforme | impossible après le premier trade | REPORTED |

**Ne tranche pas la contradiction sur le drawdown par supposition.** Demande la confirmation documentaire applicable au compte, ou marque la règle bloquante.

### 10.2 La règle des 2 minutes — conséquence architecturale majeure

La stratégie est **tick-informed** : elle observe des ticks. Elle ne doit **pas** trader au tick.

Conséquences concrètes :
- Distinguer **fréquence d'observation** et **fréquence d'ordres**.
- **Exclure** les règles dont la détention prévue est < 2 minutes, pour ce challenge.
- **Ne jamais** fractionner des ordres pour contourner la règle.
- **Ne jamais** chercher à masquer du HFT, du tick scalping ou de l'arbitrage.
- Étudier des horizons compatibles avec les règles publiées.

Une stratégie tick-informed avec une détention > 2 minutes est légitime. Sa conformité doit être vérifiée au regard de **l'ensemble** des règles, pas seulement de la durée.

**Cette exclusion s'applique au périmètre Blue Guardian. Elle ne supprime rien de la recherche scientifique, qui reste indépendante.** Tu exclus de l'adaptateur, tu ne jettes pas le résultat.

### 10.3 Les 18 paramètres serveur NOT_PUBLIC

Ne les invente **jamais**. Ils se lisent dans le MT5 du compte réellement attribué, ou marquent la règle bloquante.

`taille de contrat` · `digits` · `tick size` · `tick value` · `volume minimum` · `volume maximum` · `volume step` · `stops level` · `freeze level` · `mode d'exécution` · `types d'ordres` · `modes de remplissage` · `heures de cotation/trading` · `conversion risque → volume` · `règles de slippage/deviation` · `politique retry` · `limites de fréquence` · `causes et règles de rejet/requote`

En attendant, le modèle d'exécution est `CONDITIONAL` ou `GROSS`, **jamais `NET`**.

---

## 11. Les 8 interdictions absolues

Implémentées dans `mission.py::NEVER_AUTOMATED`. Chacune doit rester impossible, y compris pour toi.

1. **Aucune formule inventée** pour remplir une famille.
2. **Aucune modification silencieuse** d'un paramètre scientifique.
3. **Aucune suppression** d'un résultat négatif.
4. **Aucune ouverture du Holdout** sans autorisation explicite.
5. **Aucune modification** d'un certificat hérité.
6. **Aucune valeur serveur inventée.**
7. **Aucun déploiement réel** sans autorisation distincte.
8. **Aucune acceptation de phase à la place du propriétaire.**

Et les 14 erreurs historiques de la fiche §9, en particulier :
- ne pas compter les ticks comme des transactions ;
- ne pas appeler un champ « volume réel » sans preuve de sa sémantique ;
- les données synthétiques sont autorisées comme **fixtures de test uniquement**, jamais comme preuve d'edge ;
- ne pas confondre calcul correct et pouvoir prédictif ;
- ne pas confondre exécution sans erreur et validation scientifique ;
- ne pas confondre backtest positif, OOS, Holdout et certification ;
- ne pas confondre stratégie validée seule et sleeve utile au portefeuille ;
- ne pas modifier une hypothèse après avoir vu ses résultats sans nouvelle préinscription.

---

## 12. Les commandes utiles

```bash
# Tests
python -m pytest tests/ -q                        # 143 attendus
python -m pytest tests/ -q -k extraction          # un sous-ensemble

# Sécurité
python scripts/install_hooks.py                   # installer le hook
python metaalpha/secrets_guard.py .                # scan manuel

# Accès aux données
export GDRIVE_SA_JSON="$(cat sa.json)"
export GDRIVE_ROOT_FOLDER_ID="…"
python -m metaalpha.drive_preflight               # L'ÉTAPE CRITIQUE

# Bouton de connexion (si nécessaire)
python -m metaalpha.connect_app --port 8000

# Décisions du propriétaire
python -m metaalpha.decisions --template
python -m metaalpha.decisions --apply answers.json

# Architecture
PYTHONPATH=. python scripts/render_architecture.py # régénère le HTML depuis mission.py

# Démos exécutables (prouvent que ça tourne)
PYTHONPATH=. python scripts/demo_contracts.py
PYTHONPATH=. python scripts/demo_ladder.py
PYTHONPATH=. python scripts/demo_dispatch.py
PYTHONPATH=. python scripts/demo_end_to_end.py
```

---

## 13. Ce que tu dois faire, dans l'ordre

Numéroté, sans ambiguïté.

1. **Lis** ce document en entier, puis la fiche mission V2 (717 lignes) en entier.
2. **Récupère** le code de `/home/user/META_ALPHA`. Vérifie `143 passed`. Si ce n'est pas 143, rapporte.
3. **Crée** le dépôt GitHub public. Installe le hook. Pousse le code. Vérifie que la CI est verte.
4. **Configure** l'accès aux données : compte de service + partage du dossier en Lecteur + GitHub Secrets.
5. **Exécute le préflight.** C'est le moment de vérité. `PASS` avec 348 partitions, ou rapport d'écart au propriétaire. **Ne force rien.**
6. **Écris** `BASELINE_HASH_MANIFEST.json` avec les deux SHA-256 obtenus. Ils deviennent la référence.
7. **Découvre** le schéma réel via `build_inventory`. Documente-le dans `QUOTE_DGP_SPEC_V1.md`.
8. **Fais monter l'échelle** via `advance`. Le système va jusqu'à L4 seul.
9. **Présente les 9 décisions** au propriétaire, avec exemples et conséquences. Enregistre ses réponses. Ne réponds jamais à sa place.
10. **Termine la phase 2 analytique** : variables instanciées, split 60/20/20 gelé, purge/embargo, audit causal, `P2_TO_P3_GATE_V1.json`.
11. **Demande l'acceptation** de la phase 2 au propriétaire. **Attends.**
12. **Écris les moteurs P3→P7** contre le schéma réel que tu connais maintenant. Un par un, testés.
13. **Avance phase par phase**, en demandant l'acceptation à chaque gate. **Ne franchis jamais un gate seul.**
14. **P8 et P9 uniquement sur autorisation explicite**, distincte à chaque fois.

---

## 14. Comment travailler avec ce propriétaire

Il n'est pas développeur. Il pense en système et en résultats. Ce qui a fonctionné :

- **Montrer que ça tourne, pas que c'est prévu.** Une sortie de programme réelle vaut mieux qu'un schéma.
- **Dire les limites avant qu'il les découvre.** Chaque fois que le rédacteur a annoncé une limite en même temps qu'un résultat, la confiance a augmenté. Chaque fois qu'il a enjolivé, il a été corrigé.
- **Ne jamais poser une question dont la réponse est dans un document.** Il l'a explicitement reproché. Avant de demander, cherche.
- **Ne pas le solliciter pour du travail mécanique.** Il veut un système autonome. S'il doit trier des fichiers ou remplir des tableaux, le système est mal conçu.
- **Parler en français**, simplement, sans jargon inutile. Les termes techniques restent en anglais quand ils sont standards (`gate`, `checkpoint`, `walk-forward`).
- **Il accepte `NO_EDGE`.** Il l'a dit et redit. Ne cherche pas à lui faire plaisir avec un résultat. Un `NO_EDGE` propre est un succès du système.
- **Il assume le risque du dépôt public.** Ne le lui repropose pas de le rendre privé. Applique les contre-mesures et avance.
- **Il a un conseil.** Certaines décisions ont été prises collectivement. Ne les rouvre pas sans raison.

Et une chose à ne jamais faire : **ne jamais lui dire qu'un résultat est prometteur avant qu'il ne soit qualifié.** Pas de « ça a l'air de marcher ». Pas de courbe montrée avant validation. C'est la seule façon de tenir dans le temps.

---

## 15. Ce qui est prouvé, et ce qui ne l'est pas

Honnêteté finale, sans laquelle ce document ne vaut rien.

### Prouvé, exécuté, testé

- 143 tests verts, 0 échec. 8 330 lignes de Python.
- Les 8 familles et les 9 décisions sont encodées, sans valeur par défaut.
- `record_answers` refuse une attribution non humaine (`OwnerAttributionError`) — testé.
- L'échelle L0→L7 a été gravie de bout en bout sur corpus synthétique : montée automatique jusqu'à L4, arrêt net avec la cause, reprise jusqu'à L7, idempotence prouvée à la relance.
- L'extraction refuse 9 variables sur 11 avec la cause `FORMULE_NON_CERTIFIEE`, et le dit.
- Le préflight refuse de démarrer sur 347 partitions, sur un certificat non CERTIFIED, sur un nom de fichier inattendu — 8 tests.
- Le garde-fou secrets détecte 6 formes de clés et rejette 5 faux positifs — 15 tests.
- Le scope OAuth est `drive.readonly` strictement — test dédié.
- Aucun jeton écrit sur disque — test dédié.
- Le schéma HTML ne peut pas diverger de `mission.py` — vérifié en CI.
- Aucune dépendance GPU — vérifié en CI, qui casse le build sinon.
- Le système refuse de charger tout le corpus en mémoire (`UnboundedConnectionError`).
- Budget mensuel d'infrastructure : 0 FCFA.

### NON prouvé — à ta charge

- **Le corpus réel n'a jamais été lu.** Ni les 348 partitions, ni les certificats. Tout ce qui précède a été prouvé sur des données synthétiques de structure identique.
- **Le schéma réel est inconnu.** Colonnes, fuseau, précision, doublons, gaps : inconnus.
- **Les deux SHA-256 des certificats sont inconnus.** Ils seront obtenus au premier préflight réussi.
- **Aucune phase scientifique n'a été exécutée.** Aucune variable n'a été calculée sur données réelles. Aucun edge n'a été cherché. Aucun backtest n'existe.
- **Les moteurs P3 à P7 n'existent pas.** Ils sont spécifiés au §9, pas écrits.
- **Le dépôt GitHub n'existe pas.**
- **Aucun compte de service n'a été créé.**

### Formulé correctement, pour ne pas induire en erreur

Il n'existe **aucune preuve d'edge** aujourd'hui. Il existe une infrastructure qui permet de chercher, de falsifier et de rejeter — ce qui est exactement ce qui a été demandé. Si les données ne contiennent aucun avantage exploitable, le système le dira, et ce sera un résultat.

**Un backtest positif n'est pas une preuve. Un OOS positif n'est pas une certification. Seul le Holdout ouvert une fois, avec un miroir indépendant, sur un système entièrement gelé, approche d'une validation — et ce n'est toujours pas une garantie de performance future.**

---

## 16. Dernier mot

Ce projet a une qualité rare : il accepte de perdre. Il est construit pour dire `NO_EDGE` si `NO_EDGE` est vrai, pour conserver les essais négatifs, pour refuser de deviner un paramètre, pour s'arrêter quand la baseline ne correspond pas.

Cette rigueur est fragile. Elle tient dans des choix concrets : une exception levée au bon endroit, un refus de continuer sur 347 partitions, une table de correspondance explicite plutôt qu'une inférence. Il suffit d'un agent qui « améliore » en contournant un garde-fou pour que tout cela ne vaille plus rien.

**Ne l'améliore pas en le contournant. Améliore-le en le renforçant.**

Si tu trouves une erreur dans ce document, corrige-la et note la correction. Si tu trouves une erreur dans le code, corrige-la avec un test qui échouait avant. Si tu ne peux pas faire quelque chose, dis-le clairement plutôt que de produire un résultat approximatif.

C'est comme ça que ce projet réussira — quelle que soit la réponse des données.

---

*Fin du dossier de passation. Version 1.0 — 13 novembre 2026.*
