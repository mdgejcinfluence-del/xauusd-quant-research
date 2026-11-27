# PHASE 3 — COMPLÉTION HISTORIQUE : PARTIELLE, EN COURS, CHIFFRÉE

Période cible : 2026-10-01 → 2026-11-26 (1 331 heures suivies au manifeste).
État vérifié (manifeste commité) : **200 heures OK, 3 942 897 ticks Bid/Ask réels** en deux lots
mensuels (2026-10 : 1 554 685 ticks, SHA-256 `843134c2…` ; 2026-11 : 2 388 212 ticks, SHA-256
`2a13252c…`), Bid<Ask à 100 %, publiés sur le dataset Kaggle privé distinct
`shalom5123/xauusd-dukascopy-completion-2026q4` (création confirmée par le journal Kaggle).
Cause de lenteur, documentée par l'échantillon CI (`ECHantillon.json`) : le flux Dukascopy
répond de façon intermittente **503** et parfois 200 vide sous requêtes répétées (rate-limiting
côté fournisseur, déjà observé en seq407+) ; les heures non servies restent au statut
`ECHEC_OU_VIDE_A_REESSAYER` — jamais figées, jamais comblées par une autre source.
La complétion continue par relances idempotentes du même collecteur (manifeste par heure ;
aucun doublon possible, aucune partition certifiée touchée). Couverture finale du corpus après
complétion complète : 2010-01-04 → 2026-11-26. En l'état : corpus certifié jusqu'au 2026-09-30,
plus 3,94 M de ticks 2026Q4 vérifiés, plus la collecte prospective 2026-11-20→26 en dépôt.
