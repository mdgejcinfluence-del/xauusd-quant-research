# AESR-002 — MASTER RESEARCH REPORT

Question posée : l'avantage de Colorful drops est-il directionnel ? Réponse
mesurée : **non, pas principalement**. Le signal d'entrée de type H3 n'a aucun
avantage directionnel forward détectable (379 entrées simulées : +0,1 à +0,8 bp
en moyenne, ~50 % de positifs), et les paniers réels longs gagnent en survivant
sous l'eau (81–97 % de leur vie sous le premier prix d'entrée, excursions de
−7 à −18 bp) grâce à l'accumulation sur recul et à la sortie au voisinage du
prix moyen. Le mécanisme le mieux compatible est un **hybride : contexte
haussier, accumulation d'inventaire en excursion adverse, récupération vers le
prix moyen — avec un régime secondaire de scalp immédiat** quand le prix part
favorablement (D : 17 s, E : 87 s). La signature du profil (67,4 % de gagnants,
gain moyen < perte moyenne, espérance affichée +6,01 ¥/transaction) est celle
d'un mécanisme à petits gains fréquents portant un risque de queue que notre
échantillon ne montre jamais — et que le DD affiché de 31,81 % rend crédible.

Séparation maintenue : ce mécanisme explique mieux le comportement observé,
mais nos moteurs qui l'imitent partiellement **perdent de l'argent après coûts**
sur toutes les périodes testées ; fidélité et rentabilité restent deux verdicts
distincts, tous deux documentés sans embellissement. Détail :
ECONOMIC_MECHANISM_ANALYSIS.md, COMPETING_MECHANISM_REGISTER.csv,
MECHANISM_RESULTS.json ; reproduction : `ci_tools/mechanism_lab.py`.
