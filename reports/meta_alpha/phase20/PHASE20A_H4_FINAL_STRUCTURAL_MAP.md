# PHASE 20-A — CARTE STRUCTURELLE FINALE H4 (IS 2010–2020)

**`EXPLORATORY_POST_HOC` — aucune stratégie, aucun modèle, aucun P&L. Aucun comportement n'est déclaré `PROFITABLE_EDGE`.**
Barres : 15 942 (13 191 complètes), 2010-01-04 → 2019-12-16 UTC. Références de coûts 4,0/4,5 bp classées `REFERENCE_COST_UNVERIFIED` (provenance historique non certifiée comme coût broker, Phase 19-B) et conservées en parallèle à titre descriptif ; spread source observé : médiane par barre 2,36 bp (P90 3,81).

## 1. Anatomie des amplitudes
Corps médian 15,0 bp (P90 54,6 ; P99 139,2) ; range médian 38,7 bp (P90 94,4 ; P99 203,1) ; dépassements de 100 bp : 2,6 % des corps, 8,7 % des ranges. L'amplitude intrabarre domine largement le déplacement terminal : une grande bougie H4 est le plus souvent une excursion, pas un déplacement conservé — les MFE/MAE futurs (depuis chaque clôture, 1–4 barres) le confirment dans `PHASE20A_H4_FORWARD_MFE_MAE.parquet`.

## 2. Mémoire : volatilité oui, direction non
Autocorrélations des rendements signés ≈ 0 à tous les retards (1–24) ; signe des corps ≈ 0 (−0,033 au retard 1). En revanche mémoire d'amplitude nette : RANGE_BP 0,345 au retard 1, 0,429 au retard 6 (rythme journalier), rendements absolus 0,145. Le marché H4 **regroupe sa volatilité sans persistance directionnelle mesurable** sur cette population.

## 3. Anomalies qualifiées (56 tests, décalage circulaire par semaines entières ≥ 2, 10 000 réplications, contrôle synthétique p=0,727 sous le nul, Benjamini-Hochberg q=0,05)
- **Persistance d'amplitude après expansion** (`EXPANSION_Q90_ROULANT`, 1 612 occurrences) : excursion future supérieure de +13,6 à +29,2 bp aux horizons 1–4, q ≈ 0 à tous les horizons, signe stable sur 2010–2015 et 2016–2019 → `AMPLITUDE_SUPPORTED_ANOMALY` au sens descriptif : l'amplitude favorable future (MFE médian documenté dans le registre) est notable face aux références de coûts, **avec MAE conjointement élevé** — ce n'est ni une direction ni un rendement capturable.
- **Persistance de calme après compression** (`COMPRESSION_Q10_ROULANT`, 1 737 occurrences) : excursion future inférieure de −16,1/−18,4 bp aux horizons 1–2 (q ≈ 0), effet atténué ensuite et plus faible en 2016–2019 → `STATISTICAL_ANOMALY_CANDIDATE` (amplitude, pas direction).
- **Toutes les familles directionnelles** — cassures précédentes et de 24 h (intrabarre et clôture), séquences de 2 à 5+ bougies : aucun test ne survit à la correction (q ≥ 0,52) → `RARE_STRUCTURAL_OBSERVATION`. Les fins de séquences sont identifiées ex post (la barre suivante confirme la fin de la série) : lecture descriptive uniquement, jamais un signal causal.

## 4. Carte horaire
Le créneau 12:00 UTC domine l'amplitude (range médian 75,2 bp, 28,3 % > 100 bp) ; le créneau 20:00 est le plus calme (22,1 bp) avec le ratio spread/range le plus défavorable (0,126 contre 0,030 à 12:00). Le spread médian par barre varie peu (2,24–2,79 bp) : c'est l'amplitude, pas le spread, qui fait la géographie horaire. Aucun créneau n'est sélectionné comme « meilleur » : volatilité supérieure ne signifie pas avantage.

## 5. Couverture d'amplitude contre coûts (diagnostic `AMPLITUDE_COST_COVERAGE_DIAGNOSTIC`)
Les ranges médians représentent ~9–10× le spread médian observé et les excursions futures après expansion dépassent largement les références 4,0/4,5 bp en médiane ; mais les déplacements **terminaux** restent centrés près de zéro et les MAE accompagnent les MFE. L'amplitude brute est donc réelle et supérieure aux coûts de cotation observés, sans constituer un rendement capturable démontré.

## Verdict global : `H4_AMPLITUDE_SUPPORTED_CANDIDATES_IDENTIFIED`
au sens strictement descriptif : deux états de volatilité (expansion et compression roulantes) présentent une persistance d'amplitude corrigée, stable et d'amplitude notable ; **aucune anomalie directionnelle robuste** n'est identifiée. Toute étude économique ultérieure sur ces états devra être préenregistrée avant tout calcul de performance, sur décision distincte, et rester consciente du statut post-hoc de cette carte.
