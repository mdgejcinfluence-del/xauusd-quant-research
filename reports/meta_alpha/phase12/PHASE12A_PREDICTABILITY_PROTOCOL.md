# PHASE 12-A — PROTOCOLE DE RECHERCHE DE PRÉVISIBILITÉ POST-RÉINTÉGRATION

**Nature : conception et préenregistrement documentaires. Aucun calcul
prédictif, aucune corrélation, aucun entraînement, aucun test ne sont
autorisés ni effectués par la présente mission.**
**Statut : SOUMIS À VALIDATION DU RESPONSABLE (verdict §11).**
Références : protocole PHASE 11-A gelé définitivement (seq300),
résultats 11-C gelés (seq306) et réconciliés (11-C.1, seq307).
XAU/USD exclusivement ; holdout 2020–2026 scellé.

## 1. Question de recherche

À partir des informations disponibles au moment d'une réintégration
confirmée, peut-on distinguer les événements qui reprendront leur
mouvement initial de ceux qui ne le reprendront pas ? H1 (F10-01) et
H4 (F10-03) sont étudiés **séparément** ; aucune donnée n'est mélangée
entre les deux populations. L'objectif est la prévisibilité
statistique descriptive, pas la rentabilité : aucun coût, aucune
espérance nette, aucune règle de trading ne relèvent de cette phase.

## 2. Instant de décision et séparation temporelle des informations

`t_reintegration` = clôture de la minute M1 qui confirme la première
réintégration de P0 (définition gelée 11-A : clôture M1 strictement
de l'autre côté de P0 après une clôture M1 ayant confirmé le
déplacement initial). Toute variable explicative doit être calculable
à partir des seules minutes ≤ `t_reintegration`. Séparation obligatoire :

- **avant l'impulsion** : caractéristiques de la bougie déclencheuse
  (corps, range), session de déclenchement — connues à t0 ;
- **pendant l'extension** : amplitude favorable atteinte et sa durée,
  jusqu'à `t_reintegration` au plus tard ;
- **pendant le repli** : profondeur du repli et durées, arrêtées à
  `t_reintegration` ;
- **à la réintégration** : délai t0 → `t_reintegration`, session de
  réintégration, nombre de touches de P0 antérieures ;
- **futur (cible uniquement)** : tout ce qui suit `t_reintegration`
  sert exclusivement à déterminer `RESUMPTION`, jamais à construire
  une variable explicative.

Règle anti-fuite critique : plusieurs colonnes de
`PHASE11C_EVENT_PATHS.csv` sont calculées sur la **fenêtre complète**
de 8 bougies (ex. `repli_profondeur_max_bp`, `fraction_corps_reprise`,
`mfe_max_bp`, `nb_retours`). Elles sont **interdites comme variables
explicatives en l'état** (voir dictionnaire) : leurs versions bornées
à `t_reintegration` nécessiteront une extraction autorisée en
Phase 12-B. `archetype` et `reprise_apres_reintegration` sont des
dérivés de la cible : interdits comme variables.

## 3. Hypothèses préenregistrées (candidats, non des résultats)

- **H12-A Profondeur du repli** : le ratio profondeur du repli (depuis
  le meilleur extrême favorable) / extension favorable atteinte,
  mesuré à `t_reintegration`, retracements > 100 % conservés sans
  plafonnement, pourrait être associé à la reprise.
- **H12-B Vitesse du repli** : la durée entre le meilleur extrême
  favorable et `t_reintegration` (et le délai t0 → `t_reintegration`)
  pourrait différencier reprises et absences de reprise.
- **H12-C Structure de l'extension initiale** : l'amplitude favorable
  maximale atteinte avant la réintégration et la durée pour
  l'atteindre pourraient informer la continuation.
- **H12-D Structure des retours à P0** : le nombre de touches de P0
  avant la première réintégration confirmée et la séquence des
  clôtures M1 la précédant pourraient être associés au résultat.
- **H12-E Contexte temporel** : sessions UTC de l'impulsion et de la
  réintégration (catégories fixes 11-A) potentiellement associées.
- **H12-F Différences H1/H4** : comparaison descriptive des
  mécanismes entre populations, sans jamais mélanger les données.

Aucune hypothèse ne peut être sélectionnée, reformulée ou supprimée
après observation des résultats futurs.

## 4. Variable cible

Population d'analyse : événements **admissibles et réintégrés**
(la question est conditionnée à la réintégration). Pour chacun,
d'après la définition de continuation gelée (dépassement en clôture
M1 de l'ancien meilleur niveau de clôture favorable antérieur) :

- `RESUMPTION = 1` : critère atteint avant la fin de la fenêtre
  d'observation (8 bougies) ;
- `RESUMPTION = 0` : fenêtre complètement observable, critère non
  atteint ;
- `CENSORED` : fenêtre incomplète (horizon < 8) — exclus des classes
  principales, conservés au registre ;
- `AMBIGUOUS` : ordre intraminute indéterminable affectant la
  séquence réintégration/reprise (`INTRA_MINUTE_ORDER_UNKNOWN`) —
  exclus des classes principales (0 cas observés en 11-C).

La cible est identique pour tous les événements d'une famille ; une
simple excursion favorable (mèche) ne vaut jamais reprise.

## 5. Variables explicatives préspécifiées (modèle unique, simple)

Modèle préspécifié par famille (régression logistique sans réglage,
variables sous leur forme brute, aucune recherche de combinaisons) :

1. `RATIO_REPLI_EXTENSION_A_TREINT` (H12-A) — extraction bornée requise ;
2. `DUREE_EXTREME_VERS_TREINT_MIN` (H12-B) — extraction bornée requise ;
3. `MFE_A_TREINT_BP` (H12-C) — extraction bornée requise ;
4. `NB_TOUCHES_P0_AVANT_TREINT` (H12-D) — extraction bornée requise ;
5. `SESSION_REINTEGRATION` (H12-E, catégorielle, 5 modalités fixes).

Covariables de contexte connues à t0, hors modèle principal,
publiées en descriptif : `direction`, `corps_declencheur_bp`,
`range_declencheur_bp`, `SESSION_DECLENCHEMENT`,
`DUREE_T0_TREINT_MIN` (= `reintegration_delai_minutes`, disponible).
Le dictionnaire `PHASE12A_FEATURE_DICTIONARY.csv` documente chaque
variable (colonne existante ou extraction requise, unité,
disponibilité, valeurs absentes, risque de fuite).

## 6. Architecture du test futur (Phase 12-B, non autorisée ici)

- **Modèle de référence M0** : probabilité constante = fréquence de
  reprise du segment d'apprentissage. Toute amélioration se mesure
  contre M0, jamais dans l'absolu.
- **Modèle M1** : logistique préspécifiée du §5, identique pour les
  deux familles, aucun hyperparamètre optimisé.
- **Séparation chronologique** par grappe : apprentissage
  2010–2015, calibration 2016–2017, évaluation 2018–2020, la grappe
  étant affectée entièrement au segment de la date de
  `t_reintegration` de son premier événement réintégré ; aucune
  grappe partagée entre segments ; purge des événements
  d'apprentissage dont la fenêtre d'observation chevauche le début
  du segment suivant. H1 et H4 séparés à chaque étape.
- **Métriques** : principales = **Brier score** et **log-loss**
  (amélioration relative contre M0) ; secondaires = AUC (jamais
  présentée seule comme preuve), calibration (pente/ordonnée,
  courbe par déciles prédits), précision/rappel au seuil fixe 0,5.
  Justification : classes déséquilibrées (reprises majoritaires,
  surtout en H4) — les métriques de probabilité et la calibration
  priment sur l'exactitude brute.
- **Critères d'insuffisance** (par famille, fixés avant exécution) :
  segment d'évaluation < 100 événements étiquetés ou classe
  minoritaire < 50 → famille déclarée **NON ÉVALUABLE** pour le test
  prédictif (descriptif seul publié) ; calibration non publiée si
  < 200 événements d'évaluation. Aucune modification des populations
  pour atteindre ces seuils.

## 7. Niveau de preuve et risques de sélection

Les hypothèses sont inspirées d'observations déjà réalisées sur
l'IS 2010–2020 (Phase 11) : toute évaluation future sur ces mêmes
données sera qualifiée **`HISTORIQUEMENT ÉVALUÉE — NON
INDÉPENDAMMENT CONFIRMÉE`**. Une partition chronologique interne
n'est pas une confirmation indépendante. Le holdout 2020–2026 reste
scellé ; son ouverture éventuelle exigera une autorisation distincte,
explicite et **postérieure au gel du présent protocole**.

## 8. Effectifs (comptes publiés 11-C/11-C.1, sans nouveau calcul)

H1 : 2 695 réintégrés, 2 033 reprises / 662 absences (dont, sur
trajectoires complètes : 2 692 réintégrés, 2 032 / 660 ; 3 censurés).
H4 : 632 réintégrés, 542 / 90 (complets : 629 ; 539 / 90 ; 3
censurés). Faisabilité détaillée : `PHASE12A_FEASIBILITY_REPORT.md`
— la classe minoritaire H4 (90 absences au total) rend le critère
d'insuffisance du §6 vraisemblablement contraignant en évaluation.

## 9. Interdictions

Aucun calcul prédictif, corrélation, entraînement, test de
significativité, optimisation, extraction M1, reconstruction de
trajectoire, détection, recalcul Q95 ou de clustering, stratégie,
backtest, analyse économique ; cellules S12, T0/J2/J3, holdout,
dépenses. Phases 11-C et 11-A gelées ; populations et manifestes
inchangés.

## 10. Livrables de la présente mission

`PHASE12A_PREDICTABILITY_PROTOCOL.md` (présent document),
`PHASE12A_FEATURE_DICTIONARY.csv`, `PHASE12A_PREREGISTRATION.json`,
`PHASE12A_FEASIBILITY_REPORT.md` ; checkpoint chaîné après seq307.

## 11. Verdict

Définitions, cible, horizons, variables (avec statut d'extraction),
séparations temporelles, métriques, règles anti-fuite et critères
d'insuffisance sont fixés sans ambiguïté : **PROTOCOL_READY_FOR_PHASE12B**.
Ce verdict ne lance pas la Phase 12-B : extraction bornée des
variables et test prédictif exigeront une décision distincte, et le
présent protocole devra d'abord être gelé par décision formelle.
