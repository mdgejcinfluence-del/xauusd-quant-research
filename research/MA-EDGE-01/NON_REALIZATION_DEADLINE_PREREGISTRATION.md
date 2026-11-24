# MA-EDGE-01 — PRÉENREGISTREMENT DE LA RÈGLE CANDIDATE « DEADLINE DE NON-RÉALISATION »

Gelée avant toute observation nouvelle (registre seq407). Une seule règle principale ; aucune
variante ne sera comparée pour choisir la meilleure sur les mêmes données.

**Règle unique.** Population : événements M15 du Chauffeur gelé (M15_TIME_ONLY, seuil 0,560955,
Horloge 08:00-16:00 UTC, définition 24-B inchangée), décisions strictement postérieures à la
borne du holdout consommé (2026-09-30T23:59:58.864 UTC, manifeste 12-C.2).
Entrée : premier Ask (LONG) / Bid (SHORT) réel strictement après t_decision, délai ≤ 60 s, sinon
NON_EXECUTION. **Deadline : si, à t_decision + 120 minutes, aucune clôture M15 n'a confirmé le
label au sens du contrat 24-B (clôture au-delà du niveau de référence favorable), liquidation au
premier prix exécutable réel (Bid LONG / Ask SHORT) strictement postérieur à l'échéance, délai
≤ 60 s sinon EXIT_NONEXECUTABLE.** Si le label est confirmé à ou avant l'échéance : liquidation
selon le contrat de référence 24-D (t_decision + 32×15 min, premier tick). Aucun stop, aucun TP,
aucune autre échéance testée dans l'étude principale. Justification de 120 minutes : elle se
situe entre la médiane documentée (60 min) et le P75 (135 min) de la distribution publiée en
24-E — choisie *a priori* sur cette distribution historique gelée, non optimisée sur un P&L.
Comptabilité 19-B : spread une fois, S0/S1/S2, **S2 principal**, commissions exclues, résultats
nommés `HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`.
Comparaison principale préenregistrée : même population, même entrée, sortie fixe 8 h (contrat
24-D) ; différence appariée par événement ; bootstrap par grappes (10 000, graine à fixer dans
le contrat SHADOW) ; critères de succès cumulatifs : espérance S2 de la règle > espérance S2 de
la référence **et** borne inférieure IC95 de la différence > 0 sur l'échantillon prospectif.
Situation d'abstention : événement dont l'entrée tombe hors Horloge, cotation absente à
l'échéance, ou niveau de référence non reproductible — jamais de prix fictif.

Ce préenregistrement ne s'applique **pas** aux événements 2010-2019 consommés : les tester ici
serait un ajustement post-hoc. Son premier usage autorisé est le dispositif SHADOW.
