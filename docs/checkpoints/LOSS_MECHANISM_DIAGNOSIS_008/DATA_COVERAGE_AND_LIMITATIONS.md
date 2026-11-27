# LMD-008 — COUVERTURE ET LIMITES

- Paniers : registres certifiés BACKTEST-2026-001 (V1 4 107, V2-F2
  3 275), réconciliés seq475. Janvier–septembre : partitions Dukascopy
  certifiées ; novembre : 7 jours partiels ; **octobre absent, non
  extrapolé** ; janvier (dès le 12), juillet (trou 17–19), septembre
  (zéro clôture) et novembre marqués PARTIAL/GAP.
- MFE/MAE et temps sous PWA : calculés a posteriori sur les ticks des
  mêmes segments (CI run 46043159310 pour janv.–sept., local pour
  novembre), par rapport au **PWA final** du panier — approximation
  déclarée (le PWA bougeait aux renforcements). Statistiques
  descriptives causales (fenêtre t0→clôture), pas une re-simulation.
- Rendements forward : depuis le tick d'entrée, censurés en fin de
  segment ; les horizons 4 h sont absents pour beaucoup de paniers de
  fin de journée (replay journalier en novembre : limites de frontière
  documentées, clôtures aux sauts de 23:00 visibles dans les extrêmes).
- Coûts : spread déjà payé via Bid/Ask dans le PnL moteur ; spread
  médian mesuré en CI (1,31–1,66 bp) utilisé uniquement pour
  l'estimation agrégée déclarée ; coût variable 1,2 bp (S0) à +2 bp
  (S3), chaque coût compté une fois.
- Paniers non clôturés : exclus du PnL réalisé (latent séparé, non
  chiffré faute d'enregistrement par le moteur gelé).
- Ces résultats décrivent nos moteurs, jamais la rentabilité du
  provider Colorful drops.
