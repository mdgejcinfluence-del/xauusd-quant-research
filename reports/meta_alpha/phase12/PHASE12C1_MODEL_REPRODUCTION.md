# PHASE 12-C.1 — RECONSTRUCTION DÉTERMINISTE DU MODÈLE H1

**Verdict : `MODEL_RECONSTRUCTION_CONFORME`.**
**Objet : résoudre ANO-12B-01 (coefficients du modèle M1 H1 non
archivés en Phase 12-B). Qualification des résultats sous-jacents,
inchangée : `HISTORIQUEMENT ÉVALUÉE — NON INDÉPENDAMMENT
CONFIRMÉE`. Aucun accès au holdout ; H4 hors périmètre.**

## 1. Provenance du code et des données

- Code historique importé **tel quel**, sans copie ni modification :
  `ci_tools/phase12b_engine.py`, SHA-256
  `a1c9f52d9ddeb7160e2113ded3ad95da29926518ccc7b50117922117e2ee597b`
  (fonctions `logistique_irls`, `metriques`, `calibration`) ;
  script de reconstruction : `ci_tools/phase12c1_reproduce.py`
  (matrice strictement identique à celle du moteur : quatre
  variables numériques brutes puis indicatrices de session dans
  l'ordre fixe `SESSIONS_ORDRE`, référence ASIA).
- Données : `PHASE12B_FEATURES.csv` commité, SHA-256
  `6f684ee882b4c840ab27255864266729095b4fa4b52275821923f10a53c16485`,
  segment `F10-01 / APPRENTISSAGE / étiqueté` : **1 640
  observations, 1 245 reprises / 395 absences** (contrôlés par
  assertion avant ajustement), M0 reproduit sans consulter
  l'évaluation : 1 245/1 640 = **0,7591463414634146**.
- Aucune reconstruction de population, d'événement, de grappe ni
  d'extraction : seuls les artefacts committés ont été utilisés.

## 2. Environnement et dépendances

Les versions historiques exactes du run CI `45028022637` n'ont
**pas été retrouvées** : l'installation s'y faisait par
`pip install -q pandas numpy` et les journaux CI accessibles ne
contiennent aucune version (vérifié sur le journal du job
d'analyse). Elles ne sont donc pas prétendues retrouvées. La
reconstruction est une **reconstruction numérique contrôlée**,
exécutée dans un environnement épinglé et consigné :
Python 3.11.2, pandas 3.1.1, numpy 2.4.6 (voir
`PHASE12C1_MODEL_PARAMETERS.json`). Que cet environnement diffère
éventuellement du runtime original est une limite déclarée ; elle
est levée empiriquement par la concordance exacte du §4.

## 3. Méthode et paramètres retrouvés

Logistique non pénalisée par Newton-Raphson amorti (IRLS) du code
gelé : initialisation β = 0, tolérance 1e-10 sur le pas maximal,
200 itérations maximum, ridge purement numérique 1e-8, aucune
transformation des variables, aucune imputation (aucune valeur
manquante), convention `p = 1/(1+exp(−z))`, z écrêté à [−35, 35].
Paramètres reconstruits (ordre définitif : intercept, puis
variables) :

| Paramètre | Valeur |
|---|---|
| Intercept | 1,682585515770129 |
| RATIO_REPLI_EXTENSION_A_TREINT | 0,11131670535544635 |
| DUREE_EXTREME_VERS_TREINT_MIN | −0,008882903513982094 |
| MFE_A_TREINT_BP | −0,026100748302110385 |
| NB_TOUCHES_P0_AVANT_TREINT | 0,0010678267238513 |
| SESSION = LONDON | 0,2780303741498772 |
| SESSION = LONDON_NY_OVERLAP | −0,34122969210402093 |
| SESSION = NY_AFTERNOON | −0,25555560769720237 |
| SESSION = NIGHT_OTHER | −0,30759954837396397 |

## 4. Validation numérique contre les résultats 12-B gelés

Une seule reconstruction conforme a été exécutée (aucune tentative
corrective, aucun réglage) ; l'ensemble d'évaluation IS commité
(543 événements, 410/133) n'a servi qu'à vérifier :

| Mesure | Référence publiée (pleine précision) | Reconstruit | Concordance |
|---|---|---|---|
| Brier M0 | 0,18495878470019708 | 0,18495878470019708 | exacte |
| Brier M1 | 0,16538954947396367 | 0,16538954947396367 | exacte |
| Log-loss M0 | 0,5567479510569909 | 0,5567479510569909 | exacte |
| Log-loss M1 | 0,5468387473824291 | 0,5468387473824291 | exacte |
| AUC M1 | 0,6942967174032643 | 0,6942967174032643 | exacte |
| Calibration pente / ordonnée | 0,7501785957184135 / 0,09589707234295108 | identiques | exacte |
| M0 | 0,7591463414634146 | 0,7591463414634146 | exacte |

Après arrondi à quatre décimales : 0,1850 / 0,1654 / 0,5567 /
0,5468, conformément aux références. La concordance est exacte à
la pleine précision float64 publiée — supérieure à l'exigence
d'arrondi de la mission.

## 5. Reproductibilité

Seconde exécution indépendante du même script, même environnement
épinglé : coefficients, 543 prédictions et métriques **identiques**
au bit près ; empreinte SHA-256 du fichier de sortie identique
entre les deux exécutions
(`fcffb41a5904251dbe4f2f45728457ae870a067f2d0b695b2be9195416b21f86`).

## 6. Limites

1. Versions historiques du runtime CI non consignées (défaut
   documentaire) : la reconstruction est contrôlée et épinglée,
   non « bit à bit du runtime original » revendiquée ; la
   concordance float64 exacte obtenue démontre néanmoins que les
   paramètres retrouvés sont ceux du modèle évalué en 12-B.
2. La reproductibilité est démontrée dans l'environnement épinglé
   consigné ; tout futur environnement devra reproduire ces
   mêmes contrôles avant usage.

## 7. Verdict et frontière

**`MODEL_RECONSTRUCTION_CONFORME`** : sources intègres,
spécification historique exacte, reconstruction unique sur les
1 640 observations d'apprentissage, métriques principales
reproduites exactement, seconde reproduction identique. Les
coefficients H1 deviennent un objet modèle gelable (manifeste
`PHASE12C1_MODEL_MANIFEST.json`, gel par le checkpoint chaîné
après seq316). La Phase 12-C de confirmation indépendante reste
suspendue : la présente mission ne donne **aucune** autorisation
d'ouvrir le holdout ; une demande distincte est requise.
