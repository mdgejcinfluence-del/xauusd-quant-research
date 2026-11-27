# MODULE F — MARKET INTELLIGENCE & DATA DISCOVERY (conception)

## Responsabilité

Rechercher dans le corpus les signatures prédites par les hypothèses
et mesurer le rendement économiquement disponible, segment par segment.

## Corpus et segmentation (invariant)

348 partitions Parquet certifiées (685 118 625 ticks Bid/Ask
Dukascopy, 2010-01-04 → 2026-09-30, inventaire
`INVENTORY_348_EXHAUSTIVE.json`, hashes vérifiés en CI par gdown — les
partitions ne sont jamais commitées). Segments fonctionnels :
**découverte** (formuler), **construction** (définir), **validation**
(protocole gelé, jamais de recalage), **prospectif** (postérieur au
gel, catégorie D de ME-001.4). Les cotations HFM et tout autre corpus
restent séparés, avec leurs propres contrats.

## Capacités

Détection d'épisodes causale sur barres ou ticks (précédents :
ME-001.1 épisodes de récupération, ME-002 écarts à la médiane,
ME-003 impulsions) ; statistiques de trajectoire (profondeur, durées,
retracements, MFE/MAE) ; distributions conditionnelles par régime de
volatilité ; mesures d'edge exécutable ask→bid, coûts comptés une
fois ; analyses de queue (quantiles, expected shortfall) ; contrôles
de censure (fin de partition, horizons) et de dépendance temporelle.

## Architecture technique cible

Lecture Parquet par partition (jamais de chargement global), calcul
vectorisé NumPy/pandas éprouvé en CI (replays de 67 M de ticks en
minutes), DuckDB/Polars candidats pour les requêtes transversales —
adoption seulement après benchmark sur une tâche réelle du projet.
Chaque run produit : script versionné, journal de console, sorties
CSV, manifeste SHA-256, entrée au registre chaîné.

## Interdits propres au module

Réutiliser le segment prospectif ME-001 pour modifier une hypothèse ;
extrapoler les trous (octobre 2026 absent reste absent) ; présenter
2012–2026 comme un holdout vierge alors qu'il a servi à la découverte.
