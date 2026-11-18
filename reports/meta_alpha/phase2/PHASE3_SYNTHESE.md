# PHASE 3 « ÉCHELLE » — SYNTHÈSE (IS seul, OOS/HOLDOUT fermés)

## F9 TSMOM journalier : NON TESTABLE EN L'ÉTAT (gate MDE, budget intact)
Calculé AVANT tout test (instruction §2 / R3) : 2 572 jours de flux ≈ 10,2 ans, ~10 à 43 paris indépendants selon le lookback (60/120/250 j). SE(Sharpe | 0,5) = 0,33 → **MDE (puissance 80 %) = 0,93**, supérieur à l'effet visé (Sharpe ≥ 0,5). Verdict gelé appliqué : NON TESTABLE — aucune des 6 variantes n'a été exécutée, **les 6 essais restent au budget (144/150)**. Tester quand même n'aurait produit qu'un faux verdict dans un sens ou l'autre. F9 n'est ni un succès ni un échec : c'est une question à laquelle un seul actif sur 10 ans ne peut pas répondre au seuil exigé.

## Consolidation hors budget (§4) — les deux composants de gestion sont désormais L2
- **F3 HAR-RV → CANDIDATE VALIDÉE L2** : walk-forward rolling-origin déjà out-of-fold (5/5 blocs QLIKE gagnés, R² MZ médian 0,200). PBO/DSR non applicables à une famille à variante unique (N=1, rien à déflater) — adaptation consignée.
- **F7 anticipation de sauts → CANDIDATE VALIDÉE L2** : forward-chaining annuel strict — AUC 2017 : 0,684 ; 2018 : 0,696 ; 2019 : 0,687. Stabilité 3/3, aucune année sous 0,68.

## Châssis permanent (construit, testé, agnostique au moteur)
`ci_tools/meta_chassis.py` : vol targeting (§5.1), gates spread/vol/tod, Kelly plafonné 0,25, gouverneur DD (−3 % → ×0,5 ; −5 % → flat), kill-switch journalier −2 %. Tests de sanité déterministes passés. `ci_tools/challenge_sim.py` : Monte Carlo bootstrap stationnaire paramétré par CHALLENGE_CONFIG, prêt à recevoir la première composante directionnelle L2 venue.

## Compatibilité challenge (rapportée AVANT tout frais, §5 Phase 3)
Blue Guardian 2-Step Pro 5k : durée **illimitée** → aucune incompatibilité d'horloge avec un moteur basse fréquence (c'est le format rationnel pour ce programme ; ne jamais forcer un moteur lent dans une horloge rapide). Kill-switch −2 % < perte journalière −4 % ; gouverneur −5 % < perte totale −10 % : marges cohérentes. **Décision frais : AUCUN frais engageable** — il n'existe aucune composante directionnelle qualifiée à simuler ; P(passer) est incalculable, pas faible : incalculable. Le classement d'une compétition ne change ni le spread ni cette arithmétique.

## Pivot externe (§6) — documenté, non lancé
Si vous l'ordonnez : nouveau programme, nouveau préenregistrement, budget neuf — momentum cross-sectionnel multi-actifs journalier (argent, devises/DXY, indices, taux ; données publiques gratuites) sur le châssis existant + F3 (vol targeting) + protection type F7. C'est là que la littérature est la plus forte et que le problème de puissance (1 actif × 10 ans) disparaît par construction (panel cross-sectionnel). Le lancement d'un nouveau périmètre de données est un changement de périmètre stratégique : il attend votre ordre explicite, comme l'OOS.
