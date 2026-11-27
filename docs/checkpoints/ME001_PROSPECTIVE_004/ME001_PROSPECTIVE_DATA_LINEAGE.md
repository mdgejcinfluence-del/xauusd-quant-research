# ME-001.4 — LIGNAGE DES DONNÉES PROSPECTIVES

- Gel du protocole : seq484 (commit `4b361ec`), seuils d'exclusion
  7,76/7,88/5,32 bp (Q75 volatilité pré-entrée, découverte 2012/2016).
- Règle d'arrêt ajoutée avant toute donnée prospective : seq486.
- Collecte : `ci_tools/me001_prospective_collect.py`, exécutée en CI
  (job `me001prosp`, manuel ou planifié quotidien), source Dukascopy
  `datafeed.dukascopy.com` (Bid/Ask natifs, jamais mélangés à HFM).
- Registre : `ME001_PROSPECTIVE_REGISTRY.csv` — une ligne par jour de
  marché : nombre de ticks, SHA-256 du parquet journalier reconstruit,
  timestamp UTC de collecte, catégorie (D si jour > 2026-11-27, sinon
  C), statut. Les ticks eux-mêmes ne sont pas commités ; ils sont
  re-téléchargeables et leur identité est vérifiable par le hash.
- Séparation : données collectées (registre) ≠ données validées
  (aucune) ; aucun calcul de performance n'est autorisé avant la
  règle d'arrêt (≥ 60 jours D et ≥ 150 épisodes admissibles).
- Heures non publiées (503 Dukascopy) : tracées dans
  `CI_COLLECT_LOG.txt`, jamais comblées.
