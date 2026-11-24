# PHASE 21-A — AUDIT DE CONSTRUCTION D1

Statut : `EXPLORATORY_POST_HOC`, radiographie structurelle descriptive. Échantillon IS 2010-2020 uniquement ;
holdout 2020-2026 consommée et définitivement exclue. Source : barres H4 certifiées Phase 20-A (ticks non relus).

## Construction

- Journée D1 = [00:00, 00:00) UTC, OHLC Mid agrégés depuis les 6 barres H4 (00/04/08/12/16/20 UTC).
- Complétude au niveau journée : six barres présentes, couverture ≥ 3,5 h par barre. Correction documentée par
  rapport au drapeau H4 `complete` (écart ≤ 1 800 s) : la barre de 20:00 contient la pause nocturne structurelle
  (écart médian 3 600 s ; taux `complete` du slot 20:00 = 0,669 en 2010, 0,637 en 2011, 0,000 dès 2012), ce qui
  rendait toute journée impossible dès 2012. Les artefacts 20-A sont inchangés ; le trou intrajournalier est
  signalé (`trou_intrajournalier`, majoritairement la pause nocturne de la barre 20:00), jamais masqué.
- Résultat : **1 992 journées complètes, 2010-01-04 → 2019-12-16 UTC**.
- ATR14_D1 causal (14 journées complètes précédentes) ; True Range en log-bp vs clôture précédente ;
  `LOG_BP = 10000×ln(P2/P1)`. Horizons futurs : 1/2/3/5 journées complètes.
- Régimes roulants 250 journées (Q10/Q90 du RANGE_BP, journée courante exclue, 250 journées de chauffe) :
  D1_COMPRESSION 209, D1_NORMAL 1 352, D1_EXPANSION 181 journées.
- Tests de randomisation : décalage circulaire de semaines ISO entières ≥ 2, 10 000 réplications, graine 2107 ;
  famille préenregistrée de 18 tests ; BH q = 0,05 ; minima 50 occurrences / 20 semaines ISO.
  Contrôle synthétique du test : p = 0,351 (conforme).

## Défaut identifié et corrigé avant interprétation

Le test « fin de séquence ≥ 3 jours » identifiait l'événement ex post : la fin d'une séquence n'est connue
qu'après la journée suivante, de sens différent par construction (92,9 % de journées suivantes de sens non
identique). L'effet apparent (−75 bp, q ≈ 0) est un **artefact mécanique**. Contrôle causal (3e journée
consécutive de même sens, connu à sa clôture, n = 513) : +2,7 bp (H1) / +6,0 bp (H5) — aucun effet.
Qualification au registre : `ARTEFACT_IDENTIFICATION_EX_POST_NON_CAUSAL`. Aucun candidat de séquence retenu.

## Limites

- Références coûts 4,0/4,5 bp = `REFERENCE_COST_UNVERIFIED` ; couvertures 1×–5× = diagnostics uniquement.
- Aucun M1/M2, aucun modèle, aucune stratégie, aucun backtest, aucun seuil optimisé. Aucun `PROFITABLE_EDGE`.
