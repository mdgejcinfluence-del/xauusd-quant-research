# META ALPHA — PHASE S : RAPPORT DE VALIDATION SUR SIMULATION

Périmètre strictement respecté: **aucune donnée réelle lue** (ni IS, ni OOS, ni
Holdout), aucune dépense, aucune vague créée. Code: `ci_tools/phase_s_sim.py`
(générateurs à vérité connue, critères préenregistrés dans le code avant exécution).
Résultats bruts: `phaseS/PHASE_S_RESULTS.json`; tentative 1 conservée:
`phaseS/PHASE_S_RESULTS_TENTATIVE1.json`. Coût total mesuré: ~1 minute CPU local
par passe complète (29-30 s), 0 Fcfa.

## Résultats par contrôle (vérité -> obtenu -> écart)
| Contrôle | Vérité simulée | Résultat (tentative 2) | Verdict |
|---|---|---|---|
| S1 GARCH sans régime (négatif, impératif) | Aucun régime discret; volatilité GARCH(0,05/0,10/0,85) | Tentative 1 (pénalité BIC): **5/8 séries avec ruptures fallacieuses -> ÉCHEC**. Tentative 2 (pénalité renforcée x3 + segment min 50): 0/8; **validation hors calibration: 0/20** nouvelles graines | PASS après correction, tentatives conservées |
| S2 Processus fractionnaire | H = 0,7 (fGn par blocs, approximation documentée) | H estimé 0,686; stabilité inter-moitiés max 0,066 | PASS (critères: <0,10 et <0,20) |
| S3 MSM 2 échelles | Volatilité produit de 2 interrupteurs markoviens (échelles 0,999/0,98) | Exactitude d'état de volatilité HMM: 0,775 | PASS partiel: les états de volatilité sont récupérés; **les deux échelles séparément ne sont pas identifiées** par cette brique |
| S4 Sticky HMM volatilité | 2 états sigma 1x/3x, persistance 0,995 | Exactitude 0,887; ratios de volatilité estimés 2,74-3,44 (vrai 3,0) | PASS |
| S5 Régimes de spread à volatilité égale | Spread 2 bp vs 4 bp, même bruit | HMM exactitude **1,000**; segmentation DP: 9-15 ruptures détectées (vérité ~20 bascules attendues) | PASS: la chaîne détecte des régimes qui ne sont pas de volatilité |

## Limite majeure découverte (le résultat le plus important de la phase)
La segmentation par programmation dynamique sur la volatilité **ne sait pas
distinguer** un regroupement GARCH continu de régimes discrets de volatilité:
à pénalité BIC elle hallucine des régimes dans du GARCH pur (S1 tentative 1);
à pénalité renforcée elle ne détecte plus les vrais régimes de volatilité par
segmentation (0/8 à >= 3 ruptures sur graines neuves), alors qu'elle détecte
toujours correctement les changements de **niveau** (spread, S5).
Conséquence gravée pour la suite: sur données réelles, une segmentation de la
volatilité ne pourra jamais, seule, établir l'existence de régimes; la brique
validée pour les états de volatilité est le HMM (S3/S4), et toute "rupture" de
volatilité segmentée devra être traitée comme une approximation descriptive,
jamais comme une preuve de régime.

## Autres limites
- fGn généré par blocs de 200 (mémoire exacte intra-bloc seulement): S2 valide
  l'estimateur à cette approximation près.
- HMM testé à K=2 états connus: la sélection du nombre d'états sur inconnu reste
  un problème ouvert (critère prédictif à préenregistrer en Phase 1R).
- La pénalité renforcée a été calibrée SUR les contrôles simulés: c'est le rôle
  de la Phase S, mais son transfert au réel n'est pas garanti; elle est figée
  dès maintenant (PEN_FACTOR=6,0, MIN_SEG=50) et ne sera pas réajustée sur IS.

## Verdict global Phase S
**CHAÎNE PARTIELLEMENT VALIDÉE**: estimation de mémoire (S2), états HMM de
volatilité et de spread (S3 partiel, S4, S5), segmentation des changements de
niveau (S5), contrôle négatif GARCH après correction (S1, confirmé hors
calibration 0/20). **Non validé**: la segmentation comme détecteur de régimes
de volatilité. Aucune Phase 1R n'est commencée; elle exigera une décision
explicite intégrant cette limite (rôle du HMM central, segmentation réservée
aux niveaux).
