# SPÉCIFICATION CANDIDATE V2 (formalisée, gelée à ce checkpoint)

Architecture en composants, chacun étiqueté par son statut de preuve :
- **A. Entry Selection** : portail H3 (frontière M15 si ret15m ≥ +5 bp, OU voie
  rapide ret5m ≥ +10 bp et reprise 5m ≥ +7 bp), Buy seulement observé.
  Statut : NEEDS_INDEPENDENT_VALIDATION.
- **B. Market Context** : unicité F2 — au plus une première entrée par bougie M15.
  Statut : NEEDS_INDEPENDENT_VALIDATION (soutien en-échantillon 5/5).
- **C. Basket Manager** : identité du panier, un panier à la fois (construction du
  moteur ; mémoire réelle inconnue). Statut : PARTIEL.
- **D. Reinforcement** : amorçage +30 s (0,01), 3e sur recul ≤ −5,5 bp depuis la
  1re. Statut : SUPPORTED faible n côté réel ; effet causal NOT_IDENTIFIED.
- **E. Position Sizing** : placeholder moteur 0,01/0,01/0,02. Statut :
  **NON RECONSTRUIT** (formule réelle inconnue).
- **F. Exit** : placeholder moteur (Mid ≥ prix moyen après 60 s). Statut :
  **NON RECONSTRUIT** (3 hypothèses réelles réfutées, déclencheur inconnu).
- **G. Exposure & Risk** : plafond moteur 3 positions, aucun stop — reflète
  l'absence d'observation, pas une règle du trader. Statut : INCONNU côté réel.
- **H. Cost** : spread payé une fois via Bid/Ask + CENTRAL 1,2 bp. Statut :
  documenté (scénarios seq429).
- **I. Evidence & Audit** : chaque panier simulé journalisé (règle, entrées,
  prix moyen, PnL) dans les CSV de replay. Statut : implémenté.
Moteur : `ci_tools/colorful_replay_v2.py` (V1 gelé intact). V2 n'est pas une
stratégie validée ; c'est le candidat formel à soumettre aux observations
prospectives.
