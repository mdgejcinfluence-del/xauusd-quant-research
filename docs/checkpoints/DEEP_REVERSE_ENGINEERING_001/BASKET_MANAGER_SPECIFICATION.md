# BASKET MANAGER — SPÉCIFICATION

États : INACTIF → OUVERT(1) → AMORCE(2) → RENFORCE(3) → CLOTURE → REINITIALISATION.
Transitions soutenues : amorçage 16–40 s (STRONGLY_SUPPORTED, mais clôture précoce
possible avant amorçage, cas réel D) ; réentrée immédiate après clôture (1 cas, B).
Inconnus : mémoire inter-paniers, suspension, types de paniers multiples
(aucune preuve de régimes distincts), plafond. Le manager du moteur (un panier à
la fois) est une construction de simulation, pas une règle du trader établie.
