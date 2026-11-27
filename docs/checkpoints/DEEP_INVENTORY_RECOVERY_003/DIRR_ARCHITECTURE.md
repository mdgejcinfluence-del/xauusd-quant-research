# ARCHITECTURE DIRR (Dynamic Inventory and Recovery Reconstruction)

14 composants, statuts : Market State (CANDIDATE), Initial Entry (CANDIDATE),
Regime Classification (nouveau : trajectoire post-entrée, descriptif),
Inventory Accumulation (STRONGLY_SUPPORTED faible n), Dynamic Sizing
(NOT_IDENTIFIED), Weighted Average Price Engine (implémenté, référence de mesure),
Recovery Measurement (implémenté dans les trajectoires), Immediate Capture
(CANDIDATE), Basket Exit (NOT_IDENTIFIED), Risk & Tail (descriptif), Cost &
Execution (documenté), Behavioral Reproduction (moteurs gelés V1/V2-F2),
Economic Evaluation (séparée), Evidence & Audit (registre chaîné). Le replay DIRR
de ce cycle = classification des paniers des moteurs gelés en régimes +
trajectoires des paniers réels ; aucun seuil nouveau ajusté sur les réels.
