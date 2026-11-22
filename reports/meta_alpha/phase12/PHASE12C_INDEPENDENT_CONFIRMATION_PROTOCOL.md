# PHASE 12-C — PROTOCOLE DE CONFIRMATION INDÉPENDANTE DU SIGNAL H1

**Nature : conception et préenregistrement documentaires. AUCUN
accès au holdout, aucune extraction, aucun entraînement, aucune
évaluation ne sont autorisés ni effectués par la présente mission.**
**Références : protocole 12-A gelé (`580c39b1…f94`, seq311),
résultats 12-B gelés (PHASE12B_FROZEN, présent chaînage).**
**Statut : BLOQUÉ à ce stade — voir §2 et le verdict §13.**

## 1. Question

Le signal prédictif H1 de la Phase 12-B
(`PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY` : Brier −0,0196,
log-loss −0,0099 contre M0, sur l'évaluation IS 2018–2020)
conserve-t-il son amélioration par rapport à M0 lorsqu'il est
évalué, en une unique évaluation préenregistrée, sur le segment
historique indépendant 2020–2026 qui n'a participé ni à sa
découverte, ni à son ajustement, ni à son évaluation ? Périmètre :
**H1 (F10-01) uniquement**. Une confirmation sur ce holdout reste
une confirmation historique hors IS, non une validation
prospective en temps réel.

## 2. Condition préalable bloquante (ANO-12B-01)

Les coefficients β et l'intercept du modèle M1 H1 n'ont été
archivés dans aucun artefact de la Phase 12-B (voir le
procès-verbal de gel 12-B, §3). Le modèle exact à confirmer
n'existe donc pas encore comme objet gelé reproductible. Avant
toute demande d'autorisation d'ouverture du holdout, une **étape
de reproduction déterministe, séparément autorisée et sans aucun
accès au holdout**, devra :

1. ré-exécuter l'ajustement IRLS du code gelé
   (`ci_tools/phase12b_engine.py`, `a1c9f52d…`) sur le seul
   segment APPRENTISSAGE H1 étiqueté de `PHASE12B_FEATURES.csv`
   (`6f684ee8…`), n = 1 640 ;
2. épingler et consigner les versions exactes de Python, pandas
   et numpy utilisées ;
3. vérifier que les métriques d'évaluation 12-B sont reproduites
   à la précision publiée (Brier M1 0,16538954947396367,
   log-loss M1 0,5468387473824291, AUC 0,6942967174032643) ; tout
   écart au-delà de l'arrondi publié arrête l'étape et doit être
   rapporté, jamais corrigé silencieusement ;
4. archiver β et l'intercept dans
   `PHASE12C_MODEL_FREEZE_MANIFEST.json` par amendement chaîné,
   rendant le modèle intégralement gelé.

Tant que cette étape n'est pas accomplie et chaînée, le verdict
de la Phase 12-C reste `PHASE12C_BLOCKED` et aucune autorisation
holdout ne peut être utilement demandée. Il est interdit de
réentraîner le modèle sur le holdout ou d'inventer ses paramètres.

## 3. Modèle figé à confirmer

Le modèle exact issu de la reproduction du §2 : logistique non
pénalisée (IRLS, tolérance 1e-10, ridge numérique 1e-8), variables
brutes dans l'ordre gelé — `RATIO_REPLI_EXTENSION_A_TREINT`,
`DUREE_EXTREME_VERS_TREINT_MIN`, `MFE_A_TREINT_BP`,
`NB_TOUCHES_P0_AVANT_TREINT`, indicatrices de
`SESSION_REINTEGRATION` (référence ASIA) — convention
`p = 1/(1+exp(−z))`, z écrêté à [−35, 35]. Aucune nouvelle
variable, aucun réglage, aucun changement de seuil, de définition
de cible ou de coefficients après observation des résultats du
holdout, aucune sélection de sous-groupes.

## 4. Population et construction des événements (future exécution)

Détection des événements F10-01 sur le holdout par la procédure
gelée de la Phase 10 (définitions et amendement causal seq289 :
fenêtre fixe de 250 barres précédentes, barre courante exclue,
NaN exclus, minimum 200 rendements valides, Q95 gelés), populations
et clustering par la méthode historique des composantes
(Phase 11-B.1) ; extraction des cinq variables strictement bornées
à `t_reintegration` par `features_bornees` du code gelé ; cible
RESUMPTION par la définition gelée identique à l'IS (fenêtre de
8 bougies H1), CENSORED/AMBIGUOUS exclus des classes et jamais
convertis. H4 est hors périmètre.

## 5. Modèle de référence M0

Probabilité constante **gelée à 0,7591463414634146** (= 1 245 /
1 640, fréquence de reprise du segment d'apprentissage H1
2010–2015 de la Phase 12-B, conservée dans les artefacts gelés).
Cette valeur sera appliquée telle quelle aux événements du
holdout ; elle ne sera jamais recalculée sur le holdout ni sur
aucune autre période. Aucune fréquence ni étiquette du holdout ne
peut influencer M0 ou M1.

## 6. Frontières IS / holdout et indépendance

- Frontière : **2020-01-01T00:00 UTC**. Événements IS : bougie
  déclencheuse clôturée avant la frontière ; événements holdout :
  bougie déclencheuse clôturée à partir de la frontière.
- Événements dont la fenêtre d'observation de 8 bougies chevauche
  la frontière : exclus de la confirmation (motif consigné), des
  deux côtés.
- Grappes : toute grappe contenant à la fois un événement IS (ou
  dont la fenêtre chevauche la frontière) et un événement holdout
  exclut ses événements holdout de la confirmation (contamination
  par grappe) ; les grappes du holdout sont construites
  indépendamment, sans jamais fusionner avec les grappes IS.
- Événements voisins : la purge des fenêtres chevauchant la
  frontière et l'exclusion par grappe tiennent lieu de protection ;
  aucun événement étiqueté du holdout ne peut partager une fenêtre
  d'observation avec un événement IS conservé.
- Chronologie : l'évaluation est unique et terminale ; le holdout
  ne sert jamais à sélectionner un modèle, régler des
  coefficients, choisir des variables, modifier la cible, ajuster
  M0, corriger des seuils ou sélectionner des périodes/sessions.
  Aucune boucle de correction à partir des performances observées.
- Provenance : sources holdout identifiées par manifeste et
  empreintes au moment de l'exécution future, corpus IS limité
  aux 282 partitions documentées ; tout écart de provenance
  arrête l'exécution (BLOCKED).

## 7. Réestimation IS complet : non retenue

Réestimer le modèle sur l'intégralité de l'IS 2010–2020 ne serait
pas équivalent au modèle évalué en Phase 12-B et exigerait une
justification méthodologique explicite et un préenregistrement
distinct avant tout accès au holdout. Le présent protocole retient
donc le modèle exact évalué en 12-B (apprentissage 2010–2015),
sous réserve du §2.

## 8. Données manquantes et anomalies

Toute variable parmi les cinq manquante ou non finie sur un
événement du holdout exclut cet événement des observations
étiquetées (motif consigné, comptage publié) ; aucune imputation.
Toute anomalie d'extraction, de jointure, de borne temporelle ou
de provenance arrête l'exécution avec verdict BLOCKED pour le
test ; aucune correction silencieuse.

## 9. Métriques et règle de décision (fixées avant exécution)

Sur exactement les mêmes événements étiquetés du holdout pour M0
et M1 : métriques principales **Brier score** et **log-loss**
(formules, écrêtages et delta M1 − M0 identiques à la Phase 12-B ;
delta négatif = M1 meilleur) ; diagnostics secondaires : AUC
(jamais probante seule), calibration (pente, ordonnée, déciles ;
non publiée si < 200 événements étiquetés), précision/rappel au
seuil fixe 0,5. Aucune nouvelle métrique principale, aucun seuil
nouveau, aucun test de significativité.

Verdicts possibles, par construction uniques et terminaux :

- `CONFIRMED_HISTORICAL_HOLDOUT` : critères d'évaluabilité
  satisfaits, aucune anomalie, et Brier **et** log-loss de M1
  strictement inférieurs à ceux de M0 ;
- `NO_PREDICTIVE_IMPROVEMENT_HOLDOUT` : critères satisfaits, aucune
  anomalie, et au moins une des deux métriques principales non
  améliorée ;
- `NON_EVALUABLE` : < 100 observations étiquetées ou classe
  minoritaire < 50 sur le holdout (censurés/ambigus jamais
  convertis ; aucun pooling, oversampling ou élargissement) ;
- `BLOCKED` : provenance, indépendance, extraction ou intégrité
  non garanties.

## 10. Calibration

Publiée uniquement si ≥ 200 événements étiquetés (pente, ordonnée,
déciles prédits comme en 12-B) ; jamais utilisée pour recaler le
modèle (aucune recalibration n'est préenregistrée).

## 11. H4 : statut distinct

`NON_EVALUABLE_IN_PHASE12B`. Aucun modèle H4 ne sera fabriqué à
partir du modèle H1, aucune combinaison des populations, aucune
évaluation H4 sous ce protocole. Toute recherche H4 ultérieure
exigera une étude de faisabilité distincte préenregistrée sans
consultation préalable des étiquettes du holdout.

## 12. Interdictions

Pendant la conception (présente mission) : aucun accès, montage,
listage, lecture de données ou de métadonnées du holdout ; aucune
extraction M1 ; aucun entraînement ni réestimation ; aucune
nouvelle évaluation ; optimisation, stratégie, backtest, analyse
économique, S12, T0/J2/J3, dépenses interdits. Pendant la future
exécution : mêmes interdictions, plus l'interdiction absolue
d'utiliser le holdout pour toute sélection ou correction (§6).

## 13. Verdict de conception

Le modèle H1 à confirmer n'est pas intégralement gelé tant que
ses coefficients ne sont pas archivés (ANO-12B-01, §2) :
**`PHASE12C_BLOCKED`** — blocage documenté et levable uniquement
par l'étape de reproduction déterministe séparément autorisée du
§2 (sans holdout), suivie du gel des coefficients par amendement
chaîné. Ce n'est qu'ensuite qu'une autorisation distincte
d'ouverture du holdout pourra être demandée ; elle n'est ni
accordée ni préjugée par le présent protocole.
