# DATA-RECOVERY-2026-001 — RAPPORT FINAL

## A. Récupération
7 partitions identifiées dans `INVENTORY_348_EXHAUSTIVE.json` (part_000342–348,
IDs Drive documentés, jamais devinés), **7 récupérées, 7 VERIFIED, 0 inaccessible**
(2 442 245 830 octets, 66 938 889 ticks, SHA-256 calculés et archivés). Voie
d'accès : `gdown` en CI GitHub Actions (run 46024838552), mécanisme autorisé déjà
éprouvé par les moteurs historiques ; les partitions n'ont jamais été commitées.
Deux échecs techniques initiaux (répertoire de journal, course de push, API
pyarrow) ont été corrigés et documentés dans les commits — correctifs neutres,
moteur gelé intact (empreinte revérifiée).

## B. Couverture
Janvier : partiel (à partir du 12 ; 1–11 absent de toute source du dépôt).
Février–août : flux des partitions (trou 17→19 juillet documenté). Septembre :
couvert par part_000348 jusqu'au 30 (aucun panier clos en septembre dans le rejeu
par partition). Octobre : NOT_TESTABLE (backfill Kaggle non récupéré ce cycle).
Novembre : partiel 7 jours (seq455).

## C–F
Rejeu, diagnostic, fidélité et verdict : voir
`docs/checkpoints/FULL_REPLAY_2026/FULL_REPLAY_2026_FINAL_REPORT.md`.
Conclusion stratégique : la récupération est un succès technique complet ; le
rejeu confirme et amplifie le diagnostic économique négatif du moteur gelé. La
prochaine preuve utile n'est ni un seuil ni un filtre : ce sont les transactions
réelles prospectives du fournisseur et, pour octobre, la récupération du backfill
Kaggle par le CI.
