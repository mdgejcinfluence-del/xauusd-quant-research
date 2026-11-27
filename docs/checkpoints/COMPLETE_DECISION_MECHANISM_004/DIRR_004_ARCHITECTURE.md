# ARCHITECTURE DIRR-004 (16 composants, statuts)

Initial Entry (CANDIDATE) ; Post-Entry Regime Detector (CANDIDATE descriptif) ;
Inventory Accumulation (STRONGLY_SUPPORTED faible n) ; Dynamic Sizing
(NOT_IDENTIFIED, contraintes dérivées) ; Weighted Average Price Engine
(MATHEMATICALLY_DERIVED, implémenté) ; Recovery State (OBSERVED sur trajectoires) ;
Recovery Progress (OBSERVED) ; Patience and Holding (mécanisme d'état,
STRONGLY_SUPPORTED) ; Immediate Capture (CANDIDATE) ; Exit Trigger (CANDIDATE
M-D, non identifié finement) ; Risk and Exposure (NOT_IDENTIFIED côté réel) ;
Basket State Machine (spécifiée) ; Execution and Cost (documenté) ; Behavioral
Fidelity (mesurée, partielle) ; Economic Performance (mesurée, négative pour
nos moteurs) ; Evidence and Audit (implémenté, registre chaîné).
Implémentation : pas de nouveau moteur à seuils inventés — DIRR-004 est livrée
comme spécification + instruments de mesure (trajectoires, fenêtres de sortie,
classifieur de régimes) appliqués aux moteurs gelés ; coder M-D comme règle
dure serait présenter un paramètre ajusté comme découvert.
