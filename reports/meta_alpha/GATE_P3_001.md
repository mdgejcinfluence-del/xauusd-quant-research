# GATE P3-001 — Exploration conditionnelle IS : hypothèses générées, AUCUN edge qualifié

Exécution: workflow `P3-001 exploration conditionnelle IS`, run 43495787484,
**succès en 4 h 41 min 52 s**, GitHub Actions CPU, 0 Fcfa. Reprise par checkpoints
Git (STATE.json, passes A/B). Périmètre strict: 282 partitions entièrement dans
l'IS calendaire gelé (2010-01-04 -> 2020-01-20 09:36:27, 60% calendaire).
Aucun accès OOS/Holdout. Origines: observation_id % 500 = 0 (n~115 000 par cellule).
Features causales certifiées; labels RET_H_ALIGN_V1 (ASOF premier tick >= t+H).

## Résultat principal (brut, conservé intégralement dans p3/P3_001_RESULTS.json)
Sur 15 contrastes (5 features x 3 horizons, écart Q5-Q1 des rendements mid futurs):
- 9/15 passent BH-FDR q<0,05 avec des t naïfs de +1,9 à +5,1, tous dans le même sens:
  les quintiles élevés de volatilité (ROLL_STD/ROLL_RANGE), de spread relatif et
  d'intensité sont suivis de rendements mid LÉGÈREMENT positifs.
- Amplitudes: +0,07e-4 à +0,51e-4 (0,007 à 0,051 point de base... soit ~0,5 bp max à 1 h),
  à comparer au spread_rel typique ~2,0e-4 à 2,7e-4 (2+ bp): **l'écart brut est très
  inférieur au seul coût de spread**. Aucune exploitation directe n'est démontrée.

## Limites obligatoires de lecture (pourquoi ce n'est PAS un edge)
1. t-statistiques NAÏVES: les labels 15 min/1 h d'origines espacées de 500 ticks se
   chevauchent massivement -> erreurs-types sous-estimées, significativité gonflée.
2. Rendements MID-TO-MID BRUTS: aucun coût (spread, slippage) appliqué; un aller-retour
   coûte ~le spread entier, plusieurs fois l'effet mesuré.
3. Période IS 2010-2020 haussière pour l'or: un biais de dérive positive concentré dans
   les régimes volatils (souvent haussiers) peut expliquer le pattern.
4. Quintiles globaux IS: seuils appris sur tout l'IS (protocole d'exploration assumé,
   à refaire en walk-forward causal en P4/P6).

## Verdict de gate
**P3-001 = TERMINÉ, hypothèse H-P3-A générée** (à tester, non adoptée):
« le rendement mid futur conditionnel au quintile supérieur de volatilité/spread est
légèrement positif en IS ». Prochaine étape préenregistrée P4/P6: candidats
déterministes explicites, inférence par blocs (bootstrap temporel), échantillons
non chevauchants, validation OOS chronologique, coûts Bid/Ask réels. Si l'effet ne
survit pas à ces tests: rejet documenté, conservation du négatif. NO_EDGE reste possible.

## Orchestration automatique — état réel et limites (vérifiées pendant ce run)
- ✅ Checkpoints Git périodiques + reprise exacte: prouvés (passes A/B, STATE.json).
- ✅ Enchaînement intra-workflow et commit automatique des résultats: prouvé.
- ⚠️ `workflow_run` et `workflow_dispatch` exigent que le workflow existe sur la
  **branche par défaut (main)**: notre orchestrateur vit sur la branche de session,
  le dispatch de fin de P3 n'a donc pas créé de run visible (confirmé: aucun run
  orchestrateur dans l'historique). Ce n'est pas un dysfonctionnement caché:
  la continuité inter-workflows deviendra active lors de la fusion vers main
  (décision de branche du propriétaire), ou immédiatement si l'on déclenche
  l'orchestrateur depuis main. En attendant, la continuité est assurée par
  checkpoints + relance à la reprise de session, sans perte.
- Limites GitHub Actions constatées: job <= 6 h (P3: 4 h 41, proche), pas de
  processus permanent; Kaggle: sessions jetables, pas d'arrière-plan continu.
