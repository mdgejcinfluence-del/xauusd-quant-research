# CDME-004 — MASTER REPORT

Le verrou prioritaire était la clôture. Les fenêtres pré-clôture des 5 paniers
montrent un trait commun mesuré : le PnL latent monte sur 300 s et le prix
clôture à moins de 2,2 bp de son sommet local récent, au voisinage du PWA.
L'hypothèse « épuisement » est affaiblie par le panier A, clôturé en pleine
accélération (+3,9 bp/30 s) ; l'hypothèse « récupération économique » est bornée
par C, clôturé sous tout seuil de coûts positif. Il reste une formulation
candidate simple (M-D : sortie pendant la jambe favorable de récupération, près
du sommet local) — **candidate, pas découverte**. Le sizing a livré deux
contraintes mathématiques (doublement d'inventaire compatible chez A/B, contredit
chez C) sans formule. La patience est expliquée comme conséquence d'état, ce qui
désigne exactement pourquoi nos moteurs clôturent trop vite : leur règle de
sortie, pas un paramètre de durée. Rapport complet des niveaux et des ensembles
de paramètres compatibles : FINAL_STRATEGY_RECONSTRUCTION.md et
INVERSE_PARAMETER_IDENTIFICATION.md.
