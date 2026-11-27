# EMI-006 — MÉTHODOLOGIE

Préenregistrement seq470 avant calcul. Données : trajectoires tick
DIRR-003 gelées (`ts, mid, pwa, pnl_latent_bp`), 5 paniers, clôture =
dernier tick de chaque trajectoire. Tout état est calculé tick par tick,
passé seulement ; la clôture réelle ne sert qu'à scorer après rejeu.

- **Segments favorables** : runs contigus de `pnl_latent_bp ≥ θ`,
  θ ∈ {−1, −0,5, 0, +0,5, +1, +2, +3} bp. Interruptions = fins de runs
  avant clôture ; chaque segment interrompu est un faux candidat pour
  tout déclencheur de premier passage.
- **Persistance** : intervalle compatible par panier
  (max des durées interrompues ; durée du segment final], variantes
  continue / tolérance 0,5-1-2 s / cumulative / en ticks. Une durée
  commune exige une intersection non vide sur A–E.
- **Cadence** : grilles N = 1…300 s ancrées à l'ouverture du panier ;
  compatible si un point de grille tombe dans le segment final et que la
  clôture suit à ≤ 1 s. La variante à phase libre est déclarée non
  identifiable par construction (non testée comme « découverte »).
- **Condition supplémentaire** : statistiques à la clôture (détention,
  ticks depuis dernier changement de position, ΔPnL 30 s, volatilité
  30 s, distance au PWA) comparées qualitativement aux premiers passages
  d'EIDR-005 ; aucun seuil ajusté sur les clôtures n'est promu règle.
- **Robustesse** : perturbation de θ (±0,5 bp), rééchantillonnage 1 s,
  position de la clôture par rapport au segment final.
- **Moteur** : `EXIT_MECHANISM_ENGINE.py`, familles P/C/H/E/U
  interchangeables, décisions horodatées explicables, exécution au tick
  courant ; Mid seulement (spread à appliquer une fois sur Bid/Ask réel,
  jamais doublé ; aucun coût inventé).
- Limites : trajectoires Mid sans Bid/Ask ; n = 5 clôtures ; aucune
  validation indépendante possible (0 nouvelle clôture réelle).
