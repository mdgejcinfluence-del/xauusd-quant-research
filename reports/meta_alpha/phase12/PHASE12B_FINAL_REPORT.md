# PHASE 12-B — EXTRACTION BORNÉE ET ÉVALUATION PRÉDICTIVE POST-RÉINTÉGRATION

**RAPPORT SCIENTIFIQUE FINAL**
**Protocole de référence : `PHASE12A_PREDICTABILITY_PROTOCOL.md`,
GELÉ DÉFINITIVEMENT (`PHASE12A_FROZEN`, seq311), SHA-256
`580c39b114397143e6eaa7fc63e529afb79ad61ec3f9cbd843116d3484a4e99e`.**
**Autorisation d'exécution : seq312. Exécution : run CI
`45028022637` entièrement vert (8/8 lots M1 IS, tests synthétiques
temporels 5/5 en CI, job d'analyse vert), livrables committés par la
CI (`c033adf`).**
**Qualification obligatoire des résultats : `HISTORIQUEMENT
ÉVALUÉE — NON INDÉPENDAMMENT CONFIRMÉE`. Aucune rentabilité, aucun
backtest, aucune stratégie.**

## 1. Question et méthode gelée

À partir des informations disponibles à `t_reintegration` (clôture
de la minute M1 confirmant la première réintégration de P0,
définition 11-A gelée), les caractéristiques observées avant ou à
cet instant contiennent-elles une information prédictive
supplémentaire sur la reprise ultérieure (critère de continuation
gelé) ? Populations fermées, H1 (F10-01) et H4 (F10-03) séparés,
aucun pooling. Cible déjà matérialisée en Phase 11-C
(`reprise_apres_reintegration`), jamais redéfinie ; censurés
(horizon < 8) et ambigus (ordre intraminute) exclus des classes,
jamais convertis en succès ou échecs (6 censurés, 0 ambigu observé).

Modèle unique préspécifié par famille : logistique non pénalisée
(variables brutes, IRLS déterministe, aucun réglage, aucune
sélection) sur les cinq variables extraites de façon bornée ;
comparée sur exactement les mêmes observations d'évaluation à M0
(probabilité constante = fréquence de reprise du seul segment
d'apprentissage). Séparation chronologique par grappe entière,
affectée par la date de `t_reintegration` de son premier événement
réintégré : apprentissage 2010–2015, calibration 2016–2017,
évaluation 2018–2020 ; purge des événements d'apprentissage et de
calibration dont la fenêtre d'observation chevauche le segment
suivant (2 événements H1 purgés, 0 H4). Le segment de calibration
n'a servi ni à ajuster ni à sélectionner (aucune recalibration
n'était préspécifiée). Métriques principales : Brier score et
log-loss contre M0 (delta négatif = M1 meilleur) ; diagnostics :
AUC, calibration (pente, ordonnée, déciles), précision/rappel au
seuil fixe 0,5. Aucun test de significativité.

## 2. Extraction bornée et contrôles temporels

Pour chacun des 3 327 événements réintégrés (2 695 H1, 632 H4),
les cinq variables ont été recalculées à partir des seules minutes
M1 ≤ minute de réintégration incluse (conventions 11-C : clôtures
et extrema M1 Mid orientés en bp log vs P0) :

- `RATIO_REPLI_EXTENSION_A_TREINT` : profondeur du repli observée
  à `t_reintegration` (sommet favorable cumulé de la minute
  précédente vers l'extrême adverse de la minute, sans ordre
  intraminute inventé) divisée par le MFE intraminute atteint à
  `t_reintegration` ; valeurs > 100 % conservées sans
  plafonnement (3 295 événements au-dessus de 1 — attendu par
  construction, la réintégration impliquant un retour sous P0 ;
  la variable mesure l'ampleur du dépassement relatif) ;
- `DUREE_EXTREME_VERS_TREINT_MIN` : minutes entre la minute du
  meilleur extrême favorable et la minute de réintégration ;
- `MFE_A_TREINT_BP` : excursion favorable intraminute maximale
  atteinte à `t_reintegration` (jamais le MFE de fenêtre complète) ;
- `NB_TOUCHES_P0_AVANT_TREINT` : minutes strictement antérieures
  à la minute de réintégration dont l'extrême adverse franchit P0 ;
- `SESSION_REINTEGRATION` : catégorie UTC fixe de la minute de
  réintégration (revérifiée contre 11-C pour chaque événement).

Contrôles exécutés et conservés (`PHASE12B_FEATURE_AUDIT.json`,
`PHASE12B_LOG.txt`) : tests synthétiques temporels 5/5 (la mutation
absurde de toutes les minutes postérieures à `t_reintegration` ne
modifie aucune variable) ; réconciliation de l'indice de
réintégration recalculé en contrôle contre celui de 11-C pour les
3 327 événements (0 anomalie) ; MFE borné jamais supérieur au MFE
de fenêtre complète (0 violation) ; aucune valeur manquante sur
les cinq variables ; aucune colonne de fenêtre complète ni dérivé
de la cible dans la matrice (liste d'exclusion publiée) ; 0 grappe
partagée entre ensembles (2 977 grappes conservées) ; jointure par
`event_id` unique (3 327 lignes, unicité vérifiée). Aucune
anomalie d'extraction ou de fuite : liste des anomalies vide.

## 3. Effectifs par ensemble

| Famille | Réintégrés | Apprentissage (cl. 1) | Calibration | Évaluation (cl. 1 / cl. 0) | Censurés | Purgés |
|---|---|---|---|---|---|---|
| F10-01 (H1) | 2 695 | 1 640 (1 245) | 507 | 543 (410 / 133) | 3 | 2 |
| F10-03 (H4) | 632 | 379 (321) | 120 | 130 (112 / 18) | 3 | 0 |

Totaux étiquetés conformes à la réconciliation 11-C.1 : H1
2 032 reprises / 660 absences ; H4 539 / 90.

## 4. Résultats H1 (F10-01) — ÉVALUABLE

Critères d'insuffisance satisfaits (évaluation 543 ≥ 100,
minorité 133 ≥ 50). Probabilité M0 (fréquence d'apprentissage) :
0,7591.

| Métrique (évaluation 2018–2020, n = 543) | M0 | M1 | Delta M1 − M0 | Amélioration relative |
|---|---|---|---|---|
| Brier score | 0,1850 | 0,1654 | **−0,0196** | **+10,58 %** |
| Log-loss | 0,5567 | 0,5468 | **−0,0099** | **+1,78 %** |

Diagnostics : AUC M1 = 0,694 (M0 = 0,5 par construction) ;
précision au seuil 0,5 = 0,775, rappel = 0,990 ; calibration M1
(543 ≥ 200, publiée) : ordonnée 0,096, pente 0,750 — les déciles
prédits (0,509 → 0,927) suivent les fréquences observées
(0,400 → 0,909) de façon monotone croissante, avec une légère
sur-confiance aux extrêmes (pente < 1). Le modèle préenregistré
améliore les deux métriques principales contre M0, sans anomalie
de fuite : **verdict H1 =
`PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY`**. Conformément au
protocole, l'AUC seule n'aurait pas suffi à ce verdict ; il repose
sur l'amélioration conjointe du Brier score et de la log-loss.
L'amélioration de log-loss reste modeste (+1,78 %) : le signal est
réel au sens préenregistré mais d'amplitude limitée, et la
calibration indique des probabilités un peu trop extrêmes.

## 5. Résultats H4 (F10-03) — NON ÉVALUABLE

Segment d'évaluation : 130 événements étiquetés (≥ 100) mais
classe minoritaire = **18 absences de reprise < 50** : le critère
d'insuffisance gelé s'applique. Aucun modèle n'a été ajusté ni
évalué pour H4 ; aucune métrique n'est publiée. Conformément aux
interdictions, cette insuffisance n'a été contournée par aucun
pooling H1/H4, élargissement de période, oversampling ou
abaissement de seuil. **Verdict H4 = `NON_EVALUABLE`** — un
résultat de faisabilité, pas un échec d'exécution : avec 90
absences au total sur dix ans, la structure chronologique gelée ne
peut pas peupler suffisamment la classe minoritaire en évaluation.

## 6. Limites

1. Les hypothèses proviennent d'observations déjà réalisées sur
   ce même IS 2010–2020 : le résultat H1 est **historiquement
   évalué, non indépendamment confirmé** ; la partition
   chronologique interne ne constitue pas une confirmation
   indépendante. Le holdout 2020–2026 est resté intégralement
   scellé (jamais monté, listé, lu ni accédé).
2. Le ratio de repli est ≥ 1 pour la quasi-totalité des événements
   par construction de la réintégration ; son pouvoir discriminant
   éventuel porte sur l'ampleur du dépassement, pas sur son
   existence.
3. Amélioration de log-loss H1 modeste et calibration imparfaite
   (pente 0,750) : les probabilités prédites surestiment leur
   propre certitude aux extrêmes.
4. Aucune interprétation économique : une amélioration prédictive
   historique ne dit rien d'une rentabilité nette (coûts, spreads
   et exécution hors périmètre) et ne fonde aucune stratégie.

## 7. Conclusion et décision finale

- **H1 (F10-01) : `PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY`** —
  les cinq caractéristiques observables à `t_reintegration`
  contiennent, historiquement sur l'IS et selon le protocole gelé,
  une information prédictive supplémentaire sur la reprise par
  rapport à la fréquence de base.
- **H4 (F10-03) : `NON_EVALUABLE`** — critères d'effectifs gelés
  non satisfaits en évaluation (minorité 18 < 50), aucun modèle
  ajusté.
- **Décision globale : mixte par famille** (verdicts séparés
  ci-dessus, jamais fusionnés).

La Phase 12-B ne donne aucune autorisation automatique de
développer une stratégie, d'optimiser ce modèle ou d'ouvrir le
holdout. Toute étape ultérieure — en particulier une éventuelle
confirmation indépendante — exige une décision distincte du
responsable, postérieure au présent rapport.

## 8. Traçabilité

Protocole gelé (seq311, SHA-256 `580c39b1…f94`) inchangé ;
autorisation seq312 ; moteur `ci_tools/phase12b_engine.py`, tests
`ci_tools/phase12b_temporal_tests.py` (5/5 en local et en CI) ;
run CI `45028022637` vert, livrables committés par la CI en
`c033adf` : `PHASE12B_FEATURES.csv`,
`PHASE12B_FEATURE_AUDIT.json`, `PHASE12B_MODEL_EVALUATION.csv`,
`PHASE12B_RESULTS.json`, `PHASE12B_LOG.txt` (empreintes au
checkpoint d'exécution chaîné après seq312). Sources intactes
après exécution : manifeste définitif `57b7b8af…`, carte
événement-grappe `3281f594…`, `PHASE11C_EVENT_PATHS.csv`
`c487e389…`, protocole 12-A gelé `580c39b1…`. Note de périmètre :
comme lors des runs 11-C, le job historique de synthèse Phase 10
s'est exécuté dans le même run sans modifier aucun livrable
(anomalie de workflow déjà documentée, sans effet sur 12-B).
