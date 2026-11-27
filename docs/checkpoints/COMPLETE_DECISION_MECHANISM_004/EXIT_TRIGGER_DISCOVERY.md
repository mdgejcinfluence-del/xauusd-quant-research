# DÉCOUVERTE DU DÉCLENCHEUR DE CLÔTURE (X1, seq466)

Mesures dans `EXIT_TRAJECTORY_ANALYSIS.csv`. Traits présents aux 5 clôtures :
le PnL latent **monte sur 300 s** (+2,5 à +12,8 bp) et le prix clôture à
**−0,2 à −2,2 bp du sommet des 300 dernières secondes**. Traits absents ou
contradictoires : la vitesse à 30 s reste positive dans 4/5 cas (A : +3,9 bp —
la clôture survient *pendant* l'accélération, pas après son épuisement).
Verdicts par famille : **B (épuisement)** affaiblie — contredite par A ;
**A (récupération économique)** non tranchée — C clôture à −0,25 bp, sous tout
seuil de coûts positif plausible ; **C (mixte)** reste compatible mais vague.
Formulation candidate la plus simple compatible avec les 5 cas : *clôture pendant
une jambe favorable de récupération, lorsque le prix approche son maximum local
récent et que le panier est revenu au voisinage ou au-dessus du PWA* — statut
**CANDIDATE**, non identifiable plus finement sur 5 clôtures. Les instants
« comparables sans clôture » de C/E sont des artefacts du début de panier
(PWA = prix d'entrée) et ne départagent rien : limite consignée.
