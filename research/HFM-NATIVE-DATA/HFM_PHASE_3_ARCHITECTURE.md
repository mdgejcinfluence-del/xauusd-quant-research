# PHASE 3 — ARCHITECTURE DÉFINITIVE

Collecteur : `ci_tools/hfm_collector.py`, lecture seule, secrets par environnement uniquement.
- `probe` : specs serveur (`symbol_info` horodaté, versionné dans `manifests/`) + profondeur
  réelle (première observation par TF M1..D1 et ticks) → `audits/acquisition_audit.json`.
- `pilot` : 7 jours, raw préservé, normalisation (UTC ms, `available_at_utc` = ts tick,
  spread = Ask−Bid recalculé, aucun Ask déduit), qualité (Bid≥Ask, doublons, monotonie, trous).
- `collect AAAA-MM AAAA-MM` : lots mensuels ticks + barres M1..D1 dérivées **des barres serveur**
  (jamais reconstruites depuis un autre fournisseur), reprise par manifeste (lot OK jamais
  retéléchargé ; vide récent jamais figé — patron Dukascopy éprouvé), SHA-256 par fichier.
- Temps : timestamps MT5 traités comme UTC (convention MetaQuotes) **puis vérifiés** contre une
  fenêtre Dukascopy commune (décalage serveur éventuel documenté dans `manifests/`, versionné ;
  aucun décalage fixe appliqué à toutes les années sans preuve).
- Stockage Kaggle cible : dataset **distinct** `shalom5123/hfm-xauusd-native` (privé), structure
  `manifests/ raw/ normalized/{ticks,M1..D1}/ quality/ audits/ logs/` ; aucune écriture sur les
  datasets Dukascopy. Publication seulement après pilote validé, vérifiée par le journal Kaggle.
- Prospective `HFM LIVE/SHADOW` : processus séparé (collecte quotidienne incrémentale du terminal
  du fondateur), jamais mélangée à l'historique ni au corpus Dukascopy.
- Coûts : 0 € (ressources existantes). Dépendance assumée : terminal MT5 Windows allumé pour
  toute collecte ; une interruption = trous documentés, jamais comblés par une autre source.
