# PHASE 11-A — PROTOCOLE: ANATOMIE DES GRANDS MOUVEMENTS H1/H4

**Nature : étude descriptive et mécanistique (aucune rentabilité, aucune
règle de trading). Statut : SOUMIS À VALIDATION DU RESPONSABLE.**
**Gel : NON AUTORISÉ à ce stade. Exécution : NON AUTORISÉE.**
Aucun calcul ni aucune extraction ne sont autorisés par la présente
mission (conception documentaire uniquement). Les documents gelés de
Phase 10 ne sont ni modifiés ni remplacés. XAU/USD exclusivement.

## 1. Question et périmètre

Comment se distribuent les trajectoires postérieures aux grands
mouvements H1 et H4, depuis leur clôture jusqu'aux huit bougies
suivantes ? La Phase 11 décrit l'anatomie post-détection (évolution de
l'impulsion, premier recul, profondeur et datation du repli, retour au
niveau de départ, reprise éventuelle, variation selon l'heure/session
UTC). Elle ne modifie pas l'entrée de Phase 10, ne construit aucune
règle d'entrée/sortie, ne simule aucune position et ne calcule aucune
rentabilité (aucun coût, aucune commission, aucun rendement net).

Données autorisées (à l'exécution, sur ordre distinct) : corpus IS
2010–2020, 282 partitions, 3 540 993 barres M1 recensées ; trajectoires
reconstruites depuis les barres M1 existantes. Holdout 2020–2026
scellé ; aucune donnée externe.

## 2. Populations sources (manifestes Phase 10, correction seq289/294)

- F10-01 (H1, |r| > Q95 causal amendé) : 3 134 détectés, 3 107
  éligibles, 2 617 grappes — manifeste `PHASE10_EVENTS_CIBLE.csv.gz`.
- F10-03 (H4, |r| > Q95 causal amendé) : 762 détectés, 660 éligibles,
  597 grappes — même manifeste.

Aucun nouvel événement, aucun seuil modifié. Les inéligibles restent
au registre de couverture sans rejoindre la population principale.
H1 et H4 sont étudiées séparément, sans regroupement statistique.
Toute divergence d'effectifs lors de l'audit des manifestes
(livrable `PHASE11_EVENT_MANIFEST_AUDIT.md`) doit être expliquée
avant toute mesure. Identifiants de grappes : composantes connexes de
recouvrement [t_signal, fin de mesure] de Phase 10, reconstruites à
l'identique et réutilisées sans redéfinition.

## 3. Conventions de mesure

- t0 = clôture de la bougie déclencheuse ; P0 = Mid de clôture ;
  d = signe du rendement déclencheur (+1/−1), fixé à t0.
- Première bougie étudiée : première bougie complète après t0.
- Unité principale : Δbp = 10⁴ · ln(P1/P0) ; variations absolues du
  prix publiées en complément. Le terme « pip » est proscrit sans
  définition contractuelle de taille.
- Prix Mid pour l'anatomie ; Bid/Ask et spread observé publiés comme
  contexte uniquement lorsqu'ils figurent dans les artefacts
  autorisés. MFE/MAE = extrema de trajectoire, jamais des rendements
  réalisables.

## 4. Axe A — trajectoire barre par barre (t+1 … t+8)

Horizons : 8 bougies H1 (8 h nominales) ou 8 bougies H4 (32 h
nominales) ; temps calendaire écoulé enregistré séparément (fermetures
et week-ends distingués des interruptions anormales).

- **MFE(k)** : max(0, max_{j≤k} F_ij), F_ij depuis le plus haut/le plus
  bas Mid selon d. Publier valeurs cumulées t+1…t+8, incréments par
  étape, médiane/P25/P75/P90, proportion d'événements établissant un
  nouveau MFE à chaque étape.
- **MAE(k)** : max(0, max_{j≤k} A_ij), A_ij depuis le plus bas/le plus
  haut Mid selon d. Publier cumulées, progression par étape,
  médiane/P75/P90/P95, proportion d'aggravation à chaque étape.
- **Déplacement de clôture** orienté à chaque t+k vs P0 (distingue
  excursion momentanée, repli intrapériode, maintien au-delà de P0,
  retour à l'origine ou au-delà).
- **Chronologie des extrema** : instant et numéro de bougie du MFE
  maximal et du MAE maximal ; minute exacte de l'extrême dans les
  données M1 ; en cas d'égalité, premier horodatage retenu et règle
  publiée. Pour chaque extrême reconstruit à partir des barres M1,
  trois champs sont publiés explicitement :
  `extreme_minute_start_utc` (début de la minute contenant
  l'extrême), `extreme_available_at_utc` (clôture de cette minute)
  et `extreme_timestamp_resolution` (= `M1`). Aucun instant
  intraminute exact n'est déductible des seules barres M1 : l'extrême
  est localisé à la minute qui le contient, disponible à la clôture
  de cette minute, et aucune précision inférieure à la minute n'est
  revendiquée.
- **Repli depuis l'extrême favorable** (distinct du MAE depuis P0) :
  premier instant de repli après extension, profondeur maximale (bp),
  durée sommet/creux favorable → extrême du repli, instant de cet
  extrême, existence d'une nouvelle extension ultérieure. Si sommet et
  creux tombent dans la même minute : `INTRA_MINUTE_ORDER_UNKNOWN`,
  aucun ordre fictif.
- **Retracement de la bougie déclencheuse** : corps directionnel,
  range complète, recul depuis son extrême favorable, fraction du
  corps reprise (peut dépasser 100 %, jamais plafonnée).

## 5. Axe B — sessions UTC (catégories fixes, préenregistrées)

ASIE [00:00, 08:00) ; LONDRES SEULE [08:00, 13:00) ;
CHEVAUCHEMENT CONVENTIONNEL LONDRES/NY [13:00, 17:00) ;
NEW YORK APRÈS-MIDI [17:00, 21:00) ; NUIT/AUTRE [21:00, 24:00).
Fenêtres fixes en UTC sur tout l'IS, catégories conventionnelles (pas
une reconstitution des horaires locaux saisonniers). NUIT/AUTRE est
conservée contre toute exclusion silencieuse mais n'est pas une
famille confirmatoire. Aucune sélection d'heures après coup ; les
cinq catégories sont publiées intégralement.

- Session de l'événement : session UTC de clôture de la bougie
  déclencheuse ; pour H4, composition temporelle en minutes par
  catégorie publiée en complément.
- Session de réalisation : session du premier MFE, de chaque nouveau
  MFE, du MAE maximal, du premier repli, de l'extrême du repli, de la
  première réintégration éventuelle et de la reprise éventuelle.
- Par plage : effectifs, nouveaux extrema favorables/défavorables,
  amplitude favorable incrémentale, aggravation du MAE, profondeur et
  durée des replis, proportions de reprises et de retours à P0 —
  toujours avec dénominateurs.

## 6. Axe C — archétypes descriptifs (faux/vrais départs)

Distinguer **touch** du niveau P0 (extrême Mid M1 atteignant/dépassant
P0 dans le sens du retour) et **réintégration confirmée** (clôture M1
strictement de l'autre côté de P0 après une clôture M1 ayant confirmé
un déplacement dans le sens initial). Délais de première touche et de
première réintégration publiés en minutes et en bougies ; retour dans
la première bougie publié séparément (retour immédiat).

Repli/reprise sur clôtures M1 orientées : première extension
confirmée ; premier recul sous le meilleur niveau de clôture
favorable atteint ; clôture ultérieure au-delà de cet ancien meilleur
niveau (= reprise, terme purement descriptif).

Hiérarchie préétablie à t+8 (premier critère satisfait, dans cet
ordre) : `AUCUNE_EXTENSION_CONFIRMEE` ;
`REINTEGRATION_PUIS_REPRISE` ; `FAUX_DEPART_REINTEGRE_SANS_REPRISE` ;
`REPLI_PUIS_CONTINUATION` ; `REPLI_SANS_REPRISE` ;
`CONTINUATION_SANS_REPLI_CONFIRME`. Ambiguïtés intraminutes, censures
et données insuffisantes publiées séparément, jamais forcées dans une
catégorie. Aucune catégorie déclarée « rentable ».

## 7. Dépendance, couverture, censure

Grappes Phase 10 réutilisées sans redéfinition ; distributions
pondérées par événement ET résultats à poids égal par grappe. Nombre
de mouvements H1 situés à l'intérieur d'épisodes H4 publié, sans
fusion des populations. Complétude des huit bougies selon les règles
de construction H1/H4 de Phase 10 (barre valide à ≥ 50 % de ses
minutes attendues) ; barre manquante/incomplète : aucune imputation,
aucune prolongation, censure dès la première barre invalide,
effectifs conservés à chaque horizon. Temps calendaire et temps de
marché observé tous deux publiés.

## 8. Synthèse statistique (descriptive uniquement)

Aucune p-value confirmatoire, aucune sélection de sous-groupe, aucune
correction BY de confirmation, aucun classement de sessions par
rentabilité. Distributions, médianes, quantiles, fréquences
d'archétypes avec dénominateurs. Intervalles bootstrap à 95 % admis
comme mesures descriptives d'incertitude : rééchantillonnage des
**grappes** (jamais des événements indépendamment), **2 000
répétitions, graine fixée à 20261122 avant exécution**. Ces
intervalles ne constituent ni preuve d'alpha ni outil de sélection.

## 9. Livrables (à l'exécution, sur ordre distinct)

1. `PHASE11_PROTOCOL.md` (le présent document, à geler par décision
   ultérieure) ; 2. `PHASE11_EVENT_MANIFEST_AUDIT.md` ;
3. `PHASE11_H1_PATH_ANATOMY.md` ; 4. `PHASE11_H4_PATH_ANATOMY.md` ;
5. `PHASE11_SESSION_ANATOMY.md` ;
6. `PHASE11_FALSE_START_TRUE_START.md` ;
7. `PHASE11_COVERAGE_AND_CENSORING.md` ;
8. `PHASE11_FINAL_SYNTHESIS.md`. Aucun pourcentage sans dénominateur.

## 10. Interdictions

Holdout ; nouveaux événements ou seuils ; optimisation ; règles
d'entrée/sortie ; filtres de session sélectifs ; simulation de
position ; calcul de rentabilité ; backtest ; `challenge_sim` ;
promotion J2/J3 ; modification des 36 cellules S12 ; chantier T0 ;
dépenses ; modification des documents gelés de Phase 10.

## 11. Autorisation

La présente mission autorise uniquement la conception documentaire.
Le dossier est chaîné et présenté au responsable pour validation.

**PHASE 11-A : PROTOCOLE EN PRÉPARATION.**
**GEL DU PROTOCOLE : NON AUTORISÉ.**
**EXÉCUTION : NON AUTORISÉE.**
