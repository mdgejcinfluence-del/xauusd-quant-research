# MA-ALPHA-GOLD-01 — AUDIT MAÎTRE DU PROJET XAUUSD

Reconstitution vérifiée (rapports et registres originaux, phases 12→25-B, MA-EDGE-01/02,
EUR-EDGE-01/02 conservé hors périmètre). Faits structurants :
- Corpus : 685M+ ticks Bid/Ask certifiés 2010→2026-09-30 ; holdout 2020-2026 **consommé**
  (12-C.2), interdit à jamais. 2010-2019 = développement exploré (`EXPLORATORY_POST_HOC`).
- M1 (H1) et M15_TIME_ONLY prédisent des **labels de trajectoire** (Brier/AUC solides, holdout
  historique positif pour M1) mais la sélection à seuil gelé perd −3,31 bp S2 (IC95 excluant 0).
- Le payoff est détruit par les non-réalisations (−31,29 bp) face aux réalisations (+12,50 bp) ;
  la dérive après MFE en est la classe dominante (EXP-07).
- Tout ce qui prédit l'amplitude (H4/D1, FOMC, GVZ, COT intraday, spread) n'a jamais séparé
  économiquement les gagnants des perdants ; GVZ/COT échelonnent gains ET pertes ensemble.
- Modèles gelés intouchés (M1, M2, M2R, EXT_13, M15_TIME_ONLY) ; deadline 120 min préenregistrée
  (seq407), en observation prospective SHADOW, jamais rétro-optimisée.
Conclusion d'audit : le déficit n'est pas prédictif mais **économique** — aucune information
pré-entrée testée en 25 phases ne sépare le payoff net ; c'est le problème attaqué ici.
