# RAPPORT CONSOLIDÉ — Validation profonde ANOM-001 / ANOM-002 / Gaps
Exécutions: runs 43698945932 (échec téléchargement, reprise), 43709874500, 43711101548,
43712786159 (contournement quota Drive par ordre inverse), 43716623102 **succès,
282/282 partitions IS, 288M ticks**. Mesures brutes: deep/PARTITION_DEEP.csv
(déduplication par partition appliquée à l'agrégation après reprises).
Descriptif uniquement; aucun Holdout; aucune hypothèse testée.

## 1. ANOM-001 — preuve directe: le mécanisme supposé est RÉFUTÉ
- Classification des événements tick-à-tick (médianes): **les deux côtés changent
  dans 98,52% des ticks**; bid-seul 0,59%; ask-seul 0,59%; aucun changement 0,2%.
- Autocorrélations lag-1: **mid 0,487; bid 0,063; ask 0,060**.
- Même signe après un événement unilatéral: 0,61; après événement bilatéral: 0,65.
Conclusion: l'explication "mises à jour séparées créant deux demi-pas" est
**réfutée par les données**. Le phénomène (forte autocorrélation des rendements mid,
faible sur chaque jambe) subsiste et pointe vers une structure différente, non
encore mesurée: **corrélation croisée décalée bid<->ask** (une jambe mène, l'autre
suit au tick suivant). ANOM-001 reste OBSERVATION À VÉRIFIER, mécanisme ouvert.
C'est un résultat négatif sur notre propre explication — conservé comme tel.

## 2. ANOM-002 — regroupement de volatilité: DESCRIPTIF DOCUMENTÉ confirmé
Autocorrélation des |rendements|: 0,457 / 0,184 / 0,132 / 0,086 aux lags 1/5/20/50:
persistance longue à décroissance lente, stable en médiane sur 282 partitions.
Aucune capacité prédictive attribuée (aucun test indépendant à ce stade).

## 3. Gaps — aucun effet directionnel; volatilité de réouverture seulement
Effectifs IS: 24 525 gaps 60-300 s; 922 gaps 300-3600 s; 2 016 gaps > 3600 s.
Rendement signé moyen après gap: ~0 dans toutes les classes (part positive 47,6%
pour > 3600 s, écart-type ~7 bp). Après les longs gaps, l'amplitude est élevée
mais symétrique. Aucune asymétrie haussière/baissière retenue; ne pas transformer
une moyenne de volatilité en signal directionnel.

## 4. Observations complémentaires (descriptives)
- Réversion du spread: corrélation niveau->variation du spread ≈ -0,43 (le spread
  large tend à se resserrer au tick suivant, et inversement): propriété de la
  cotation, pas un signal.
- Sauts: continuation directionnelle au tick suivant ~0 (audit précédent confirmé).

## 5. Limites
Explorations répétées sur le même IS (sélection cumulative documentée: 148 tests +
3 vagues descriptives); médianes de partitions rapportées, pas de preuve;
la corrélation croisée bid/ask décalée reste à mesurer directement.

## 6. Pistes d'hypothèses réellement justifiées (NON lancées, autorisation requise)
- H-A: structure lead-lag bid/ask mesurée d'abord descriptivement (corrélation
  croisée aux lags -5..+5), puis seulement si elle est forte, stable et d'amplitude
  supérieure au spread, une hypothèse préenregistrée.
- H-B: aucun candidat directionnel issu des gaps (effet nul mesuré): ne pas en créer.
Conformément à la directive: **aucune vague P3-003 n'est lancée par ce rapport.**
