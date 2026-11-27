# MACHINE À ÉTATS DYNAMIQUE (spécification)

IDLE --[contexte haussier + déclencheur candidat]--> INITIAL_POSITION_OPEN
INITIAL_POSITION_OPEN --[prix favorable rapide]--> IMMEDIATE_CAPTURE --> BASKET_CLOSED
INITIAL_POSITION_OPEN --[+16-40 s]--> amorçage (position 2)
INITIAL_POSITION_OPEN --[recul ≈ -5 bp]--> INVENTORY_ACCUMULATION (position 3)
INVENTORY_ACCUMULATION --[retour vers PWA]--> RECOVERY
RECOVERY --[condition inconnue au voisinage du PWA]--> BASKET_CLOSED
BASKET_CLOSED --[réévaluation immédiate (observé +2 s)]--> IDLE/ENTRY
États EXIT_CONDITION_MET et limites (durée/exposition/abandon) : NOT_IDENTIFIED.
Chaque transition porte son statut dans les spécifications DIRR jointes.
