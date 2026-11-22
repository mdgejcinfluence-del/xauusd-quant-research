# PHASE 12-B — PROCÈS-VERBAL DE GEL DÉFINITIF

**Date : 2026-11-13. Gel décidé par le responsable (mission de
clôture 12-B / conception 12-C). Aucun réentraînement, aucune
nouvelle évaluation pendant ce gel.**
**Qualification obligatoire : `HISTORIQUEMENT ÉVALUÉE — NON
INDÉPENDAMMENT CONFIRMÉE`.**

## 1. Résultats gelés

### H1 — F10-01 : `PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY`

Évaluation 2018–2020 : 543 observations étiquetées, 133 dans la
classe minoritaire (critères gelés satisfaits). Apprentissage
2010–2015 : 1 640 (1 245 reprises) ; calibration 2016–2017 : 507.

| Métrique | M0 | M1 | Delta M1 − M0 | Amélioration relative |
|---|---|---|---|---|
| Brier score | 0,1850 (0,18495878470019708) | 0,1654 (0,16538954947396367) | −0,0196 (−0,01956923522623341) | +10,58 % |
| Log-loss | 0,5567 (0,5567479510569909) | 0,5468 (0,5468387473824291) | −0,0099 (−0,009909203674561828) | +1,78 % |

Diagnostics : AUC M1 0,6942967174032643 (M0 = 0,5) ; précision au
seuil 0,5 : 0,7748 ; rappel : 0,9902 ; calibration (pente
0,7501785957184135, ordonnée 0,09589707234295108, déciles publiés
dans `PHASE12B_RESULTS.json`). Conclusion conservée, limitée :
amélioration historique par rapport au modèle de référence selon
les critères préenregistrés. Ni « rentabilité démontrée », ni
« alpha confirmé », ni « stratégie validée ».

### H4 — F10-03 : `NON_EVALUABLE`

Évaluation : 130 observations étiquetées, 18 dans la classe
minoritaire (< 50 préenregistrés). Aucun modèle H4 ajusté ni
validé ; aucun pooling, oversampling, élargissement ou
abaissement de seuil. Statut conservé : non évaluable.

Effectifs étiquetés totaux (conformes 11-C.1) : H1 2 032 reprises
/ 660 absences (+ 3 censurés) ; H4 539 / 90 (+ 3 censurés) ;
0 ambigu.

## 2. Contrôles de gel (tous vérifiés avant chaînage)

- Protocole 12-A gelé : SHA-256
  `580c39b114397143e6eaa7fc63e529afb79ad61ec3f9cbd843116d3484a4e99e`
  (identique au gel seq311) ; dictionnaire
  `933feff779e2f1a54ef1f538610a8fb2a481b48f702b72c6eedcf7f3d1df2519` ;
  préenregistrement JSON
  `005d1e69752141234132588e74d8d8eef699cedc31abb685628f0f77cd8f8bf2` ;
  faisabilité
  `6e8c26181639987085da703463cd131969fbd4bf32b57de6a703e4e9e8c367cb`.
- Livrables 12-B : `PHASE12B_FEATURES.csv`
  `6f684ee882b4c840ab27255864266729095b4fa4b52275821923f10a53c16485` ;
  `PHASE12B_FEATURE_AUDIT.json`
  `a16cb94ed5e03a6a48f2fb19ced07d4593835de4bb5001325b69df626f053a25` ;
  `PHASE12B_MODEL_EVALUATION.csv`
  `7d8ced8ae64fc64cf65b30004b6495173192deae7be13f7992f9ae0b5ccc0583` ;
  `PHASE12B_RESULTS.json`
  `93e7d5ca3a03496e61b5f160fa4a36e4ccfdedca8a93f0f5d57c7aaa65f5786b` ;
  `PHASE12B_FINAL_REPORT.md`
  `346a23d4b013901773f701b6fe427a929ee2b23575527dbc102c561b0145ef17`.
- Cohérence rapport final / fichiers de résultats : vérifiée
  (effectifs, métriques, verdicts concordent).
- Provenance : run CI `45028022637` entièrement vert — 8/8 lots
  M1 IS réussis, job « P12-B extraction bornée + évaluation
  prédictive » réussi, tests synthétiques temporels 5/5, livrables
  committés par la CI en `c033adf`.
- Chaîne continue depuis seq311 (seq312 autorisation, seq313
  exécution vérifiés) ; commit distant `46cc173` = HEAD local,
  arbre propre au moment du gel.

## 3. Paramètres du modèle H1 : inventaire et anomalie de conservation

Éléments **retrouvés dans des artefacts vérifiables** :

- Ordre et noms des variables (code d'entraînement gelé par
  hash, `ci_tools/phase12b_engine.py` SHA-256
  `a1c9f52d9ddeb7160e2113ded3ad95da29926518ccc7b50117922117e2ee597b`) :
  `RATIO_REPLI_EXTENSION_A_TREINT`,
  `DUREE_EXTREME_VERS_TREINT_MIN`, `MFE_A_TREINT_BP`,
  `NB_TOUCHES_P0_AVANT_TREINT`, puis indicatrices de
  `SESSION_REINTEGRATION` ;
- Encodage catégoriel : indicatrices binaires pour LONDON,
  LONDON_NY_OVERLAP, NY_AFTERNOON, NIGHT_OTHER, catégorie de
  référence ASIA (ordre fixe `SESSIONS_ORDRE` du code) ;
- Transformations : **aucune** (variables brutes, aucune
  standardisation, aucun plafonnement) ;
- Convention de prédiction : `p = 1/(1+exp(−z))`, z = intercept +
  Σ βᵢxᵢ, score linéaire écrêté à [−35, 35] (code) ; métriques
  calculées avec probabilités écrêtées à [1e-15, 1−1e-15],
  seuil fixe 0,5 pour précision/rappel ;
- Algorithme d'entraînement : logistique non pénalisée par
  Newton-Raphson amorti (IRLS), tolérance 1e-10, 200 itérations
  max, ridge purement numérique 1e-8 (code, lignes
  `logistique_irls`) ;
- **Fréquence M0 gelée : 0,7591463414634146** (= 1 245 / 1 640,
  segment d'apprentissage H1 2010–2015) — conservée dans
  `PHASE12B_RESULTS.json` et `PHASE12B_MODEL_EVALUATION.csv` ;
- Paramètres des métriques : formules Brier, log-loss, AUC de
  Mann-Whitney avec rangs moyens (code) ;
- Données d'entraînement exactes : `PHASE12B_FEATURES.csv`
  (hash ci-dessus), segment APPRENTISSAGE H1 identifiable par la
  colonne `ensemble`.

Élément **NON conservé** :

- **Les coefficients β et l'intercept du modèle M1 H1 n'ont été
  écrits dans aucun artefact** (ni `PHASE12B_RESULTS.json`, ni
  `PHASE12B_MODEL_EVALUATION.csv`, ni le journal : seules la
  pente et l'ordonnée de *calibration* y figurent, qui ne sont
  pas les coefficients du modèle). Les versions exactes des
  dépendances (pandas/numpy installées sans épinglage par
  `pip install -q pandas numpy` dans le workflow) ne sont pas
  davantage enregistrées.

**Conséquence (application de la règle de la mission, §3)** : le
signal historique H1 reste intégralement documenté et gelé, mais
le modèle **n'est pas, en l'état des artefacts, reproductible
comme objet gelé** pour une confirmation indépendante : ses
paramètres exacts devraient être régénérés par un nouvel
ajustement déterministe sur le segment d'apprentissage commité,
ce que la présente mission interdit (aucun réentraînement pendant
le gel). Cette anomalie de conservation est enregistrée
(ANO-12B-01, non bloquante pour le gel des résultats, bloquante
pour la confirmation tant qu'elle n'est pas levée par une étape
de reproduction séparément autorisée, sans aucun accès au
holdout : voir le protocole 12-C).

## 4. Anomalies et limites de preuve

- ANO-12B-01 : coefficients M1 et versions de dépendances non
  archivés (voir §3).
- Limites inchangées du rapport final : hypothèses issues du même
  IS ; partition chronologique interne ≠ confirmation
  indépendante ; ratio de repli ≥ 1 quasi par construction ;
  amélioration de log-loss modeste ; calibration imparfaite
  (pente 0,750) ; aucune interprétation économique.
- Anomalie de workflow déjà documentée : le job historique de
  synthèse Phase 10 s'exécute dans les runs d'analyse sans
  modifier les livrables (sans effet sur 12-B).

## 5. Statut

**PHASE 12-B : GELÉE DÉFINITIVEMENT (`PHASE12B_FROZEN`)** —
résultats, effectifs, métriques et verdicts ci-dessus font
référence officielle. Aucune modification silencieuse ; le
holdout 2020–2026 est resté intégralement scellé ; aucune
autorisation d'étape ultérieure ne découle de ce gel.
