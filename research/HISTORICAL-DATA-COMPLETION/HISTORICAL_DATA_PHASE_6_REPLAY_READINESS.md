# PHASE 6 — MOTEUR DE REPLAY : PRÊT ET PROUVÉ MÉCANIQUEMENT

`ci_tools/replay_engine.py` : lecture chronologique de ticks Bid/Ask UTC, exécution au prix du
bon côté (spread compté une fois), scénarios de coûts paramétrés (Phase 5), positions multiples
et clôture de panier groupée, journal horodaté de chaque décision (ouverture, clôture, motif,
brut/coûts/net en bp, durée). Preuve exécutée ce cycle sur ticks réels Dukascopy
(`duka_2026-11-24.parquet`, 439 453 ticks) : panier de deux BUY (0,10 + 0,05) ouvert au premier
tick, clôturé groupé — journal complet produit, brut −151,34 bp, coûts CENTRAL 1,2 bp, net
−152,54 bp. C'est une **preuve mécanique**, pas un test de stratégie : aucune règle d'entrée
n'est évaluée, aucune optimisation n'est lancée. Reste à brancher : lecture directe des lots
Kaggle/348 partitions en streaming, swaps par nuit calendaire, et la future spécification de
stratégie préenregistrée (mission distincte).
