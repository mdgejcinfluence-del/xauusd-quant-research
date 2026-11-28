# ERE — PHASES 3 À 7 : EXÉCUTION, MOTEURS, TRANCHE VERTICALE, RÉEL, DOSSIER 2

## Phase 3 — Infrastructure d'exécution (`ere/runner.py`)

`TaskRunner` : hash de tâche déterministe (spécification canonique),
checkpoints JSON par shard écrits atomiquement (.tmp → rename) et
relus après écriture, reprise idempotente (un shard terminé n'est
jamais recalculé — testé), manifeste de run avec SHA-256 du checkpoint.
Un checkpoint local n'est « durable » qu'après écriture + relecture
vérifiée ; en CI, la durabilité reste le commit sur la branche.

## Phase 4 — Neuf moteurs (`ere/engines.py`)

Fonctions pures sur les contrats, frontières appliquées par le code :
A force `verified=False` sur toute statistique publique ; B plafonne à
N2 ; C impose ≥2 hypothèses + inconnue et interdit tout posterior sans
likelihood ; E émet l'avis de testabilité avant F ; F est découpé en
catalog/index/signatures/execute ; G exige le contre-seing explicite
pour clore en NON DÉMONTRABLE et ne déclare jamais d'identification
sur une seule signature de fréquence ; H lève `PermissionError` sous
N5 ou sans approbation ; I-A refuse toute « VALIDATION RÉUSSIE » sans
mesures, critères pré-déclarés et segment indépendant ; I-B n'admet
que des verdicts I-A favorables. 12 tests passent (`tests/`).

## Phase 5 — Tranche verticale synthétique (`ere/vertical_slice.py`)

Preuve d'exécution : `vertical_slice_proof.json` (même dossier).
Parcours A→I sur ticks 100 % synthétiques : 3 transactions fictives,
claim « +2000 % » conservée non vérifiée, 4 hypothèses + inconnue,
plan gelé (hash), signature mesurée (1 920 épisodes, taux 0,784 sur le
générateur synthétique — sans aucune signification de marché),
verdict de G **COMPATIBLE MAIS NON IDENTIFIÉ**, porte H **fermée**,
portefeuille vide. Verdict final publié : **`NOT_IDENTIFIED`** —
le pipeline sait ne pas conclure.

## Phase 6 — Intégration aux données réelles (lecture seule, autorisée)

- F.catalog vérifié sur l'inventaire réel : **348 partitions,
  685 118 625 lignes, 0 erreur** (`INVENTORY_348_EXHAUSTIVE.json`,
  lu, non modifié). Les partitions elles-mêmes restent téléchargées
  par la CI ; aucun accès aux zones prospectives protégées ME-001,
  aucun backtest réel lancé dans cette phase.
- Les formats réels (Parquet Bid/Ask Dukascopy) sont compatibles avec
  le chemin `index_bars`/`signature_recovery` via DuckDB retenu en
  Phase 2. Un backtest réel ne constituerait de toute façon pas une
  validation (Constitution §6–§7).

## Phase 7 — Deuxième dossier trader : préparation seulement

Conformément à la mission, aucun nouveau dossier trader n'est lancé
avant consolidation. Préparation livrée : le moteur A accepte dès
maintenant tout dossier au format contrat (transactions partiellement
connues, claims non vérifiées, manques explicites) — le prochain
dossier n'exigera aucun code spécifique. Le choix du trader et la
collecte restent une décision du fondateur.

## Gouvernance

`main` inchangée, moteurs gelés intacts (tests de gouvernance
existants), aucun ordre, aucune dépense, aucun secret exposé,
registre chaîné tenu à chaque phase.
