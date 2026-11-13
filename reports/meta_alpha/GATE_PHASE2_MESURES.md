# GATE PHASE 2 — Mesures L2/L3/L4 sur les 348 partitions : PASS

Exécution: GitHub Actions (runs 43452759007, 43456180352, 43458775276), reprise par
checkpoints Git toutes les 20 partitions (STATE.json). Deux échecs de téléchargement
transitoires (partitions 220 et 257, limites gdown) diagnostiqués depuis ERROR.txt
committé, corrigés de manière contrôlée (retry, puis repli HTTP direct vérifié
PAR1 + taille d'inventaire), reprises sans retraiter les partitions certifiées.

## Critères préenregistrés et résultats (PARTITION_MEASURES.csv, 348 lignes)

| Critère | Résultat | Statut |
|---|---|---|
| Partitions mesurées | 348/348 | ✅ |
| Somme des lignes | 685 118 625 = certificat, écart 0 | ✅ |
| Régressions temporelles intra-partition | 0 | ✅ |
| Timestamps dupliqués consécutifs | 0 | ✅ |
| Quotes invalides (bid<=0 ou ask<bid) | 0 | ✅ |
| Reconstruction mid=(bid+ask)/2, spread=ask-bid | écart max 0,0 sur 348 partitions | ✅ |
| Trous > 60 s | 30 804 (fermetures de marché/week-ends; max 275 470 s ≈ 3,2 j) | documenté, attendu |

Verdict: **GATE P2-MESURES = PASS**. Le corpus mesuré est conforme au certificat.
Les trous temporels sont des fermetures de marché, pas des pertes: ils devront être
traités comme ruptures (aucune fenêtre ne doit les traverser silencieusement).

## État Phase 2 restant (honnête)
- Variables certifiées: 5/11 (22 entrées SQL). Bloquées, motifs documentés:
  ZSCORE_ROBUST, SPREAD_REGIME, REGIME_CLASS (traductions étagées), SUBPERIODE
  (sessions non documentées — ne pas inventer), MFE_H/MAE_H (convention direction).
- Prochaine étape automatique: préenregistrement P3 au Trial Ledger, puis exploration
  sur IS uniquement (splits calendaires 60/20/20, purge >= 1 h, Holdout scellé).
