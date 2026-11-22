# PHASE 17-C — RAPPORT FINAL

## Décomposition des résultats économiques et diagnostic du meta-labeling M2

**Qualification permanente : HISTORIQUE EXPLORATOIRE — POPULATION DÉJÀ ÉTUDIÉE.**
Diagnostic conduit exclusivement sur les artefacts committés des Phases 17-A et 17-B
(sources retrouvées et agrégations nouvelles distinguées ci-dessous). Aucune lecture de
ticks, aucun nouveau label, aucun entraînement, aucun seuil modifié. Phase 17-B
intégralement gelée ; verdicts 17-B conservés sans altération.

## 1. Réconciliation (retrouvée dans les sources, dénominateurs restitués)

Candidats par segment : 1 143 / 360 / 443 (apprentissage / calibration / évaluation),
identiques pour les deux contrats. Étiquetés : B08 1 137 / 357 / 440 (succès 402 / 156 /
203 ; échecs 735 / 201 / 237 ; censurés 5 / 2 / 3 ; NON_EXECUTION 1 / 1 / 0) ; B09
1 133 / 356 / 435 (succès 474 / 180 / 227 ; échecs 659 / 176 / 208 ; censurés 9 / 3 / 8 ;
NON_EXECUTION 1 / 1 / 0). Décisions d'évaluation au seuil gelé : B08 **19 retenues /
421 rejetées** (4,32 %, espérance réalisée +3,46 bp) ; B09 **52 / 383** (11,95 %,
−1,24 bp). En calibration (agrégats 17-B retrouvés) : B08 10 retenues (−7,93 bp), B09 38
(+7,44 bp) — signe opposé à l'évaluation pour chaque contrat. Métriques 17-B retrouvées
à l'identique ; le statut B08 est conservé avec la mention obligatoire
`FORMAL_METRIC_PASS_WITH_NEGLIGIBLE_EFFECT_NO_USABLE_ECONOMIC_INFORMATION_DEMONSTRATED`.

Les probabilités des segments sans fichier de décisions (apprentissage, calibration) ont
été **restituées par application déterministe des paramètres gelés** aux features
committées : écart maximal 1,1×10⁻¹⁶ contre les probabilités livrées en évaluation
(440 + 435 événements). Aucun coefficient n'a été touché.

## 2. Où se perd l'information économique — quatre mécanismes

**MEC-1 — Le modèle ne classe pas.** Les probabilités prédites sont comprimées autour de
la moyenne (écart-type 0,036 à 0,057 ; en évaluation B08, 80 % des q tiennent entre
0,325 et 0,409 alors que le seuil est à 0,437 : la décision ne porte que sur une queue).
Les déciles d'évaluation, formés sur les seules probabilités, ne montrent aucun gradient
(taux positifs observés entre 0,34 et 0,59 sans monotonie ; AUC 0,490 et 0,510 ; pentes
de calibration 0,148 et 0,058, négative en calibration pour B08). Les sept variables
causales ne séparent pas le signe économique. Le diagnostic ne peut pas trancher si cela
tient à l'insuffisance de ces variables ou à l'imprévisibilité intrinsèque du signe —
d'où le caractère partiel du verdict.

**MEC-2 — Le label prédit une course de barrières, pas une espérance.** Dans tous les
segments : tout `TP_FIRST` est positif, tout `SL_FIRST` est négatif ; seules les sorties
`VERTICAL_FIRST` sont mixtes (B08 évaluation : +1,72 bp en moyenne, 46/79 positifs). Les
positifs proviennent donc presque exclusivement des TP (157/203 en évaluation B08), et
l'amplitude est détruite par la binarisation : positifs de +0,03 à +219,96 bp en
apprentissage sous le même label (cf. audit dédié, exemples par identifiant).

**MEC-3 — L'échelle des payoffs n'est pas stationnaire, le seuil fixe ne voyage pas.**
G/L passent de 41,2/32,0 bp (B08, apprentissage) à 25,3/22,4 en évaluation ; de
40,4/38,4 à 24,9/27,3 pour B09 — parallèlement à la dérive d'`ATR14_H1` (SMD −0,66) et du
spread à la décision (SMD −0,88), les barrières étant exprimées en multiples d'ATR. Le
`P_BE` implicite des payoffs réalisés d'évaluation (0,470 et 0,523, calcul descriptif
seul) dépasse le seuil gelé issu de l'apprentissage (0,437 et 0,487). Aucun seuil n'a été
recalculé à des fins de décision ; le constat suffit : la représentation « gains et pertes
constants » n'est pas transportable entre régimes de volatilité.

**MEC-4 — Dérive conjointe et biais de sélection hérité.** La fréquence positive monte de
+10,7 points (B08) et +10,4 points (B09) entre l'apprentissage filtré en échantillon par
M1 et l'évaluation hors entraînement M1, pendant que les amplitudes chutent d'environ
40 % et que le segment 2016-2017 contredit le modèle B08. Signe et amplitude dérivent en
sens opposés. Aucune correction, aucun réentraînement de M1, populations intactes ;
aucune interprétation causale n'est tirée de ces corrélations descriptives.

La pondération égale par grappe ne change pratiquement rien (grappes de 1,08 événement en
moyenne ; top-5 grappes = 2,6 à 6,7 % du P&L absolu) : l'échec n'est pas un artefact de
concentration. H4 conserve son statut `NON_EVALUABLE_IN_PHASE12B`, sans pooling.

## 3. Verdict

**`M2_FAILURE_MECHANISM_PARTIALLY_IDENTIFIED`** — MEC-2, MEC-3 et MEC-4 sont établis ;
MEC-1 est établi comme absence de classement, sans pouvoir séparer insuffisance des
variables et imprévisibilité intrinsèque du signe. Aucun verdict de rentabilité n'est émis.

## 4. Frontière

Ce diagnostic identifie ce qu'une représentation économique future devrait traiter — le
signe seul ne suffit pas, l'amplitude et son régime comptent — mais il **n'autorise ni
nouveau modèle, ni nouvelle cible, ni nouveau seuil**. Toute suite exige une décision
distincte et des données n'ayant servi ni à la conception, ni à l'ajustement, ni à la
sélection ; le holdout 2020-2026 reste définitivement exclu.

*Empreintes SHA-256 des livrables : voir `PHASE17C_RESULTS.json` (section
`sha256_livrables`) et le corps du présent dépôt.*
