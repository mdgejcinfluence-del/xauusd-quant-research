# PHASE 0 — AUDIT INTÉGRAL DU CORPUS EXISTANT (vérifié, pas repris de mémoire)

Source d'audit : `reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json` (footers Parquet lus un à un,
13 nov. 2026) revérifié ce cycle par recalcul local, et `kaggle_migration/VERIFY.json`.
1. Partitions : **348/348** lues, 0 erreur de footer. 2. Ticks : **685 118 625** (somme exacte,
écart 0 avec le certificat Phase 2). 3. Première observation : **2010-01-04T00:01:10.457Z**.
4. Dernière : **2026-09-30T23:59:58.864Z**. 5. Bid/Ask : colonnes `bid`/`ask` séparées dans les
deux signatures de schéma (294 + 54 partitions), plus mid, spread_abs/rel, volumes Bid/Ask —
aucun Ask reconstruit. 6. Couverture annuelle : matrice `COVERAGE_MATRIX.csv` (13,1 M ticks en
2010 → 73,7 M en 2025 ; 2026 partiel 66,9 M jusqu'au 30 sept.). 7. Granularité native : ticks ;
les barres M15/H4/D1 du projet en sont dérivées et bornées ≤ 2019-12-16 pour l'IS historique.
8. Lacunes : 29 intervalles > 1 h entre partitions adjacentes, **tous** des fermetures de
week-end/jours fériés (vendredi ~21 h → dimanche ~22 h) — aucune journée ouvrée absente détectée
au niveau partitions. 9. Doublons : `observation_id` continu 1 → 685 118 625, chevauchements
temporels inter-partitions : 0. 10. Non-conformes : 0 (deux signatures de schéma documentées,
créateur DuckDB homogène). 11. Empreintes : listing SHA-256 du corpus
(`partitions_sha256_listing`) + SHA-256 par fichier migré dans `kaggle_migration/STATE.json`.
12. Certification : corpus certifié intact ; **aucune partition touchée par cette mission**.
Attention de périmètre : la migration Kaggle vérifiée porte sur 282 fichiers (lots IS) ; les 348
partitions restent l'actif de référence (Drive d'origine + inventaire) — distinction consignée,
aucune confusion entre « inventorié » et « migré ».
