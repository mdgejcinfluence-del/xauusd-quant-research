# PHASE 21-A — CARTE STRUCTURELLE FINALE D1 (XAU/USD, IS 2010-2020)

Statut : `EXPLORATORY_POST_HOC`. Radiographie descriptive uniquement — aucune stratégie, aucun modèle,
aucune prétention de rentabilité. Verdicts au registre seq373.

## Population

1 992 journées D1 complètes (2010-01-04 → 2019-12-16 UTC), construites depuis les barres H4 certifiées 20-A.
Amplitude journalière médiane : RANGE_BP 115,4 bp (P99 433,2) ; corps absolu médian 49,1 bp.

## Résultats

| Famille | Résultat | Qualification |
|---|---|---|
| D1_EXPANSION → amplitude future (H1/2/3/5) | +64,4 / +84,6 / +100,0 / +112,5 bp (UP+DOWN), q BH ≈ 0–0,007, 4 tests significatifs ; présent dans les deux sous-périodes (amp. H1 moy. 235 bp en 2010-2015, 138 bp en 2016-2019) | `D1_VOLATILITY_ANOMALY_CANDIDATE` (descriptif) |
| D1_COMPRESSION → amplitude future | −21,5 à −53,3 bp, p 0,026–0,047 mais q BH 0,095–0,105 (non significatif après BH) | `RARE_D1_STRUCTURAL_OBSERVATION` |
| Terminaux directionnels (régimes) | q BH 0,39–1,00, aucun significatif | `RARE_D1_STRUCTURAL_OBSERVATION` |
| Séquences ≥ 3 jours (fin de séquence) | effet apparent −75 bp = **artefact d'identification ex post** ; contrôle causal nul (+2,7/+6,0 bp) | `ARTEFACT_IDENTIFICATION_EX_POST_NON_CAUSAL` |

- Mémoire d'amplitude sans mémoire directionnelle : autocorrélation RANGE_BP 0,343 (retard 1) → 0,237 (retard 20) ;
  rendements signés et directions ≈ 0 à tous les retards — cohérent avec 20-A à l'échelle H4.
- Transitions de régime : persistance faible (COMPRESSION→COMPRESSION 0,197 ; EXPANSION→EXPANSION 0,304 ;
  retour à NORMAL 0,67–0,79 dès la journée suivante).
- Couvertures d'amplitude vs références coûts non vérifiées (4,0/4,5 bp) : diagnostics uniquement.

## Verdict global

`D1_AMPLITUDE_STRUCTURE_SUPPORTED_DESCRIPTIVE` pour le seul candidat D1_EXPANSION (mémoire de volatilité
journalière) ; aucune asymétrie directionnelle D1 démontrée ; famille séquences rejetée comme artefact.
Aucun `PROFITABLE_EDGE`, aucune promotion automatique. Toute suite exigerait une autorisation nouvelle et
une confirmation indépendante (J2/J3), la holdout 2020-2026 étant consommée et exclue.
