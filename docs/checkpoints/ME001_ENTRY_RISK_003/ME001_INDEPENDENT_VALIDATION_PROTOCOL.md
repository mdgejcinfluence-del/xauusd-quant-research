# ME-001.3 — PROTOCOLE DE VALIDATION INDÉPENDANTE (prospectif)

Contamination déclarée : les partitions 2012–2026 utilisées ont servi
à la découverte (2012/2016) et à une validation à protocole gelé
(2020/2024/2026) ; ce ne sont pas des holdouts vierges pour les
politiques P1/P2, dont les formes ont été gelées en seq484 mais
évaluées sur ces mêmes segments.

Validation recevable à l'avenir, sans réajustement :
1. Geler P2 exactement comme en seq484 (seuils d'exclusion = Q75 de
   volatilité pré-entrée calculés sur 2012/2016 : 7,76 / 7,88 / 5,32 bp
   pour les seuils 5/10/20 bp) et la définition d'épisode seq480.
2. L'appliquer aux partitions postérieures à 2026-09-30 (octobre 2026
   et au-delà, lorsqu'elles seront certifiées) ou à des données HFM
   Bid/Ask collectées prospectivement.
3. Critères pré-déclarés : espérance nette par épisode actif > 0, PF
   > 1,2, ES95 meilleur que P0 sur le même jeu, pire perte bornée par
   le budget de 1 % par −200 bp. Tout écart = rejet, pas de re-calage.
4. ME-001 ne passera VALIDATED que si ces critères tiennent sur ce
   jeu neuf, avec les coûts réels du lieu d'exécution.
