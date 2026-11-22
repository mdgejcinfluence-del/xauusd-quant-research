# PHASE 17-B — MODÈLES DE PRÉDICTION ÉCONOMIQUE M2-B08 ET M2-B09

**Qualification permanente : `HISTORIQUE EXPLORATOIRE — POPULATION
DÉJÀ ÉTUDIÉE`. Ni confirmation indépendante, ni rentabilité nette
(commissions `COMMISSION_EXCLUDED_BY_DESIGN` ; étiquette des labels :
`NET_OF_SPREAD_AND_HYPOTHETICAL_S2_SLIPPAGE_BEFORE_COMMISSION`).**

**Verdicts : M2-B08 `M2_PREDICTIVE_ECONOMIC_SIGNAL_SUPPORTED_HISTORICALLY`
(au sens formel du critère gelé, avec des grandeurs d'effet
négligeables — lire le §4) ; M2-B09
`M2_NO_ECONOMIC_PREDICTIVE_IMPROVEMENT`.**

## 1. Exécution et intégrité

Préflight conforme (chaîne seq345, commit `b43ec46`, huit livrables
17-A vérifiés par SHA-256) ; autorisation seq346. Exécution CI :
run final `45069518288` entièrement vert (exit 0), après deux
incidents consignés et corrigés dans le seul moteur (sérialisation
de l'audit ; premier/dernier tick réels pour la sortie verticale —
une première version censurait à tort les verticales, détectée par
la réconciliation avant toute conclusion). **Réconciliation avec
la Phase 14 gelée : parfaite** — pour l'évaluation, les P&L S2
reconstruits coïncident avec les résultats B08/B09 déjà gelés sur
440 et 435 événements communs, écart maximal ~10⁻¹⁴ bp. Le rôle de
la calibration est celui du préenregistrement 17-A : validation
chronologique (métriques rapportées), aucun entraînement, aucune
calibration de probabilité, aucun seuil.

## 2. Labels et populations (par contrat, jamais fusionnés)

Filtre M1 gelé appliqué sans recalcul de M1 : apprentissage
1 143, calibration 360, évaluation 443 événements. Après exclusions
préenregistrées (censures, 1 non-exécution par segment) :
**B08** — étiquetés 1 137 / 357 / 440 (positifs 402 / 156 / 203) ;
**B09** — 1 133 / 356 / 435 (positifs 474 / 180 / 227). Tous les
segments dépassent largement les critères 100/50 : aucun contrat
n'est `NON_EVALUABLE`. Mécanismes et P&L S0/S1 de sensibilité
conservés dans les fichiers de labels ; les censurés ne sont
jamais transformés en étiquettes.

## 3. Baselines, seuils et modèles

`M0_ECON` (apprentissage seul) : **B08 = 0,3536**, **B09 = 0,4184**
de résultats positifs sous S2 — à comparer à la fréquence de
reprise directionnelle : le contrat transforme une reprise
« probable » en issue positive minoritaire. Payoffs
d'apprentissage : B08 G = +41,2 bp, L = 32,0 bp ⇒ **P_BE = 0,437** ;
B09 G = +40,4, L = 38,4 ⇒ **P_BE = 0,487**. Deux régressions
logistiques simples et distinctes (implémentation IRLS gelée de
la Phase 12-B importée telle quelle ; sept variables préenregistrées,
`p_M1` exclu ; coefficients et environnements consignés dans les
fichiers de paramètres).

## 4. Évaluation (même sous-ensemble étiqueté par segment ; AUC diagnostic secondaire)

| Contrat / segment | Brier M0_ECON → M2 | Log-loss M0_ECON → M2 | AUC M2 | Pente de calibration |
|---|---|---|---|---|
| B08 calibration | 0,2530 → 0,2549 | 0,7000 → 0,7043 | 0,442 | **−0,767** |
| B08 évaluation | 0,2601 → 0,2596 | 0,7147 → 0,7138 | 0,490 | 0,148 |
| B09 calibration | 0,2576 → 0,2594 | 0,7085 → 0,7122 | 0,485 | −0,084 |
| B09 évaluation | 0,2602 → 0,2604 | 0,7139 → 0,7143 | 0,510 | 0,058 |

Lecture sans complaisance :

- **B08 franchit formellement le critère gelé** en évaluation
  (Brier et log-loss inférieurs à `M0_ECON`) — d'où le verdict
  `M2_PREDICTIVE_ECONOMIC_SIGNAL_SUPPORTED_HISTORICALLY`. Mais
  l'amélioration est de **0,0005 point de Brier et 0,0009 de
  log-loss (≈ 0,2 % relatifs)**, avec un AUC de 0,490 (inférieur à
  0,5) et une pente de calibration de 0,148 : les probabilités M2
  ne discriminent pratiquement pas et sont très mal étalonnées.
  Sur la calibration 2016–2017, le même modèle est **moins bon**
  que la baseline (AUC 0,442, pente négative) : le « signal »
  d'évaluation n'est corroboré par aucun segment indépendant du
  même IS.
- **B09 n'améliore rien** sur aucun segment (verdict
  `M2_NO_ECONOMIC_PREDICTIVE_IMPROVEMENT`).
- **Décisions au seuil P_BE** : couverture très faible en
  évaluation (B08 : 4,3 % des opportunités retenues, espérance
  réalisée +3,5 bp sur 19 événements, précision 0,526 ; B09 :
  12,0 %, espérance réalisée **−1,2 bp** malgré le seuil
  d'espérance positive). En calibration, les retenues B08 perdent
  −7,9 bp en moyenne. Le filtre économique, tel que construit,
  ne sélectionne pas un sous-ensemble profitable de façon stable.

**Conclusion scientifique** : à variables causales égales, la
couche meta-labeling n'apporte pas d'information économique
supplémentaire utilisable sur cette cohorte — le verdict formel
B08 tient à des écarts inférieurs au bruit d'arrondi des
métriques, contredits par la calibration et par les décisions
réalisées. Aucune des deux couches ne doit être utilisée pour
exposer un capital.

## 5. Limites (obligatoires, inchangées)

Biais de sélection en échantillon du filtre M1 sur
l'apprentissage (M0_ECON, seuils et coefficients en héritent) ;
`p_M1` exclu des variables par hygiène anti-fuite ; période
2018–2020 déjà étudiée par toutes les phases antérieures
(jamais une confirmation) ; commissions exclues et slippage S2
hypothétique (les labels eux-mêmes en dépendent) ; remplissage
des cotations sans preuve de profondeur (limites Phase 16) ;
censures publiées par contrat et segment. Aucune extrapolation
au compte réel ; un résultat favorable n'aurait de toute façon
constitué qu'une hypothèse à tester prospectivement.

## 6. Livrables et traçabilité

Labels et features séparés par contrat
(`PHASE17B_LABELS/FEATURES_B08/B09.csv`), paramètres des deux
modèles (`PHASE17B_M2_B08/B09_PARAMETERS.json`), évaluation
(`PHASE17B_MODEL_EVALUATION.csv`), décisions d'évaluation
(`PHASE17B_ECONOMIC_DECISIONS.csv`), audits variables et labels
(`PHASE17B_FEATURE_AUDIT.json`, `PHASE17B_LABEL_AUDIT.json`),
résultats (`PHASE17B_RESULTS.json`) ; chemins tick par lot
(`P17_PATH_*.csv`), journaux et code de sortie conservés. Moteur
`ci_tools/phase17b_engine.py`, jobs `lots17b`/`analyse17b`. Toute
étape suivante (par exemple évaluation prospective d'un filtre
M2) exigerait une décision distincte et des données n'ayant servi
ni à la conception, ni à l'ajustement, ni à la sélection ; le
holdout reste définitivement exclu.
