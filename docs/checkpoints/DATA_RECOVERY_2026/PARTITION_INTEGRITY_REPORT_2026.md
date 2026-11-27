# PARTITION INTEGRITY REPORT 2026

Récupération via `gdown` en CI (run 46024838552), mécanisme autorisé déjà utilisé par
les moteurs historiques du dépôt ; connecteur Drive utilisé pour confirmer les
métadonnées (part_000342 : 469 669 819 octets, md5 Drive concordant avec la taille
de l'inventaire). **7/7 partitions récupérées et classées VERIFIED** : taille exacte,
nombre de lignes exact, bornes temporelles exactes vs `INVENTORY_348_EXHAUSTIVE`,
schéma homogène (16 colonnes), ordre chronologique vrai, 0 doublon de timestamp,
0 valeur nulle, spread médian 1,31–1,66 bp. SHA-256 calculés à la récupération
(`PARTITION_INTEGRITY_AUDIT_2026.csv`). Total : **66 938 889 ticks, 2 442 245 830
octets**, 2026-01-12 → 2026-09-30. Les partitions n'ont pas été commitées dans Git
(traitement éphémère CI, suppression après rejeu) ; leurs empreintes permettent de
vérifier toute récupération ultérieure. Trou inter-partitions documenté :
2026-07-17 20:59 → 2026-07-19 22:00. Janvier 1–11 : absent du corpus (aucune autre
source dans le dépôt) — janvier reste partiel. Octobre : backfill Kaggle non
récupéré ce cycle (voir `DATA_RECOVERY_BLOCKERS.md`).
