# PHASE 18-A — INVENTAIRE DES SCHÉMAS SOURCES (preuves techniques)

*Audit documentaire uniquement : en-têtes, requêtes committées, manifestes et rapports. Aucune valeur de tick lue, aucun calcul nouveau.*

## 1. Partitions tick brutes IS 2010–2020 (Kaggle privé du propriétaire)
Schéma prouvé par l'inventaire exhaustif `reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json` (footers, 348 partitions ; IS = 282 partitions documentées en 13-A) et par toutes les requêtes DuckDB committées (`ci_tools/phase13b_engine.py` l.121-131, `phase17b_engine.py` l.77-112, `phase10_engine.charger`) : par observation, **`timestamp_utc`** (résolution milliseconde), **`bid`**, **`ask`**, et `mid` dérivé ((bid+ask)/2). **Absents de toutes les sources** : prix de transactions exécutées, volume, taille de cotation, profondeur de carnet, file d'attente, identifiant d'ordre ou de contrepartie (déjà établi en Phase 16, `PHASE16_FILLABILITY_AUDIT.md` §1). Toute mesure de « flux d'ordres » ou de « volume » est donc **impossible** ; seules des statistiques de cotations Bid/Ask sont constructibles.

## 2. Artefacts committés exploitables sans nouvelle extraction
- **Barres M1 Bid/Ask** `reports/meta_alpha/phase13/P13B_BARS_*.csv.gz` (8 lots IS) : schéma `ts, bo,bh,bl,bc, ao,ah,al,ac, mo,mh,ml,mc, sp, first_tick_ts, last_tick_ts` — OHLC Bid, Ask et Mid par minute, spread médian de minute en bp, horodatages exacts du premier et du dernier tick de chaque minute. Couverture : minutes des fenêtres d'événements IS.
- **Ticks d'entrée** `P13B_TICKS_*.csv` : schéma `event_id, quote_timestamp, bid, ask, partition` — **uniquement le premier tick après `t_decision`** par événement. Aucune série tick pré-décision n'existe dans les artefacts committés.
- **Features/labels 17-B et cibles 17-E** : les sept variables gelées, `ATR14_H1`, prix et P&L par événement (`event_id`, `grappe_id`).
- **Chemins d'événements 14/17** (`P14_PATH_*`, `P17_PATH_*`) : extrêmes du flux filtré post-entrée — postérieurs à la décision, **inutilisables comme variables** (fuite), cités uniquement pour mémoire.

## 3. Ce qui n'existe pas dans le périmètre
Aucune série tick pré-décision committée ; aucune donnée exogène horodatée alignée (les budgets exo historiques sont gelés et hors périmètre) ; aucune profondeur/volume (cf. §1) ; holdout 2020–2026 interdit et non consulté.

## 4. Conséquence pour les candidats
Deux classes d'accessibilité : (i) candidats calculables depuis les **barres M1 committées** (dynamique et géométrie pré-décision à la minute) ; (ii) candidats exigeant une **extraction future** des partitions tick IS (microstructure des cotations), dont le schéma source est prouvé mais dont aucune valeur n'est présente dans les artefacts. Cette extraction n'est pas autorisée par la présente phase.
