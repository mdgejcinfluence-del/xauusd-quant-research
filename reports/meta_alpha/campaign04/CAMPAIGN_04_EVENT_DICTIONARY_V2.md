# CAMPAGNE 4 — DICTIONNAIRE DES ÉVÉNEMENTS ET DES ÉTATS (VERSION 2 RÉVISÉE)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Version 2
produite après validation **conditionnelle** du propriétaire (seq 195) ;
elle remplace la version 1 (seq 193, conservée inchangée pour traçabilité)
et reste **soumise à validation définitive : aucun calcul n'est autorisé à
ce stade.** Si elle est validée, son hash sera chaîné avant toute
extraction et aucune définition ne pourra être modifiée après consultation
des résultats. Résumé des changements en §9.

## 1. Conventions communes

- Corpus : barres M1 reconstruites depuis le tick IS (282 partitions,
  2010-01-04 → 2019-12-16), prix Mid, horodatages **UTC** de bout en bout.
- Journée de cotation = date UTC présente dans le corpus. Ères
  2010–13 / 2014–16 / 2017–20.
- Sessions (UTC fixes toute l'année, §7) : Asie 00–08, Londres 08–13,
  New York 13–21, nuit 21–24.
- « Journées précédentes » = les journées de cotation **immédiatement
  antérieures présentes dans le corpus**, jour courant toujours exclu des
  seuils. Quantiles : interpolation linéaire (défaut NumPy), précisé ici
  pour lever toute ambiguïté d'implémentation.
- Aucun état n'est un signal directionnel ; aucun seuil poolé sur
  l'échantillon entier n'est présenté comme une détection en temps réel
  (les seuls usages poolés sont étiquetés « référence rétrospective »).

## 2. F3 — causalité historique documentée (correction n° 1)

Faits établis par audit du code gelé (`ci_tools/f3_har.py`,
`reports/meta_alpha/phase2/F3_PREREG.json`, seq 75) :

| Propriété | Fait vérifié |
|---|---|
| Modèle | HAR-RV quotidien : X_j = [1, RV_j, moyenne 5 j de RV, moyenne 22 j de RV] ; cible RV_{j+1} (horizon **un jour**) |
| Entraînement | OLS **roulant** : pour prédire le jour j+1, ajustement sur les paires (X_s, RV_{s+1}) avec s+1 ≤ j, en retenant les **500 dernières journées** ; coefficients ré-estimés chaque jour (walk-forward strict, entraînement uniquement sur le passé de chaque origine) |
| Horodatage | La prédiction du jour j+1 utilise X_j, donc la RV complète du jour j : elle est connaissable à la **clôture du jour j**, c'est-à-dire à l'ouverture du jour j+1 — jamais avant la clôture de j |
| Données d'entrée | Série horaire historique (60 025 h), RV journalière = √(Σ sommes de carrés horaires) ; journées retenues si ≥ 12 heures de flux ; 2 572 journées, 2 071 avec prédiction (amorçage ≈ 500 journées sans prédiction) |
| Seuils de classement historiques | **Point de non-causalité identifié** : les terciles BAS/MOYEN/HAUT utilisés par les campagnes 1–3 ont été calculés sur la distribution **poolée de tout l'échantillon** de `pred_har`. La prédiction est causale ; son **étiquette de tercile poolée ne l'est pas** |

**Règle Campagne 4 qui en découle** : l'état-passé F3 est publié sous deux
formes distinguées et jamais confondues — (a) **prédiction F3 continue**
(causale, connue à l'ouverture du jour prédit au sens ci-dessus) et
tercile **causal roulant** de cette prédiction (quantiles 1/3–2/3 des
prédictions des 250 journées précédentes disposant d'une prédiction,
minimum 60, jour courant exclu) : c'est la seule forme autorisée à porter
la mention « connu à l'ouverture » ; (b) tercile poolé historique, étiqueté
partout « **référence rétrospective** », utilisé uniquement pour recouper
les campagnes antérieures. F3, son modèle et ses prédictions ne sont pas
modifiés ; le critère de qualification historique de F3 (évalué sur le
régime récent 2016–2020) est un jugement d'échantillon complet et n'est pas
présenté comme une propriété connue ex ante.

## 3. RV quotidienne — définition figée (correction n° 2)

- **Formule** : pour la journée j, RV_j = √( Σ_k r_k² ) × 10⁴ (bp), où les
  r_k sont les rendements logarithmiques entre clôtures M1 **consécutives
  à l'intérieur de la journée** (différences de log-clôtures M1 ; le
  premier rendement de la journée, qui exigerait la clôture de la veille,
  est exclu ; aucun rendement overnight n'entre dans RV_j).
- **Fréquence et délimitation** : barres M1 complètes, journée = date UTC
  [00:00, 24:00). La RV d'une journée n'existe qu'à sa clôture : **elle
  n'est jamais présentée comme disponible à son ouverture**, et toute
  conséquence conditionnée par l'état courant d'un jour commence au plus
  tôt le jour suivant.
- **Qualité** : journée utilisable si ≥ 300 barres M1 distinctes, sans
  horodatage dupliqué (déduplication sur l'horodatage, patron campagnes
  précédentes) ; journées exclues comptées et publiées. Session utilisable
  si ≥ 60 barres M1.
- **Fenêtre des seuils** : exactement les **60 journées de cotation
  précédentes** (présentes et utilisables), minimum 40 ; en deçà, aucun
  état (amorçage compté et publié).
- **Relatif vs absolu** (correction n° 4, partie 1) : les états terciles
  sont **relatifs** à la distribution roulante des 60 journées précédentes ;
  en parallèle, chaque journée publie son niveau **absolu** RV_j (bp) et le
  ratio log(RV_j / médiane causale des 60 journées précédentes), afin qu'un
  changement d'état relatif ne soit jamais confondu avec un changement
  absolu de volatilité. Les distributions absolues poolées éventuellement
  montrées sont étiquetées descriptives rétrospectives.

## 4. États journaliers (famille REG-J, principale)

| Élément | Définition figée |
|---|---|
| État-passé (ouverture de j) | Prédiction F3 continue pour j + son tercile **causal roulant** (§2a) ; NON_CLASSE publié à part |
| État courant (clôture de j) | BAS si RV_j ≤ q1/3 des RV des 60 journées précédentes ; HAUT si RV_j > q2/3 ; MOYEN sinon — seuils du passé, mesure du jour, conséquences à partir de j+1 |
| Discordance F3 | Matrice complète état-passé (tercile causal) × état courant, publiée avec la version référence rétrospective en regard, jamais fusionnées |

## 5. Transitions — premier franchissement, vitesse, confirmation (correction n° 3)

- **Épisode d'état** : run maximal de journées consécutives de même état
  courant (REG-J). **Premier franchissement** : la première journée dont
  l'état courant diffère de celui de l'épisode précédent (date candidate C).
- **Traversée** : nombre de journées de cotation entre la dernière journée
  de l'ancien épisode (exclue) et la première journée du nouvel épisode
  (incluse), en passant par les états intermédiaires éventuels (un passage
  BAS → MOYEN → HAUT compte les journées MOYEN dans la traversée).
  Classes figées : **rapide = 1–2 journées ; intermédiaire = 3–4 journées ;
  progressive = ≥ 5 journées** (la classe intermédiaire est publiée comme
  telle, jamais arbitrairement rattachée).
- **Confirmation** : la transition est confirmée si le nouvel état persiste
  **3 journées consécutives à partir de C** (C incluse) ; **date de
  confirmation D = C + 2 journées de cotation**. Si l'état quitte le nouvel
  état avant D, la transition est **non confirmée** : elle est conservée au
  catalogue avec sa date candidate, son sens, sa durée de persistance
  (1 ou 2 journées) et son motif de non-confirmation. Aucune confirmation
  n'est antidatée ; aucune transition non confirmée n'est supprimée ni
  reclassée a posteriori.
- **Durées** : durée d'un épisode = longueur de son run ; durées de
  traversée classées ci-dessus ; épisodes tronqués aux bords du corpus =
  censurés, comptés et publiés.
- **Retour à l'habituel** (correction n° 4, partie 2) : au premier jour
  d'un épisode HAUT, on fige la référence R* = médiane des RV des 60
  journées précédentes **antérieures au début de l'épisode** ; R* reste
  fixe pendant tout l'épisode (le seuil glissant ne peut donc pas fabriquer
  de retour). Le retour est la première journée postérieure à l'épisode où
  RV < R* ; temps de retour en journées de cotation, censuré à 60 journées
  ou fin de corpus, publié avec son taux de censure. La version à seuil
  glissant de la version 1 est **abandonnée**.
- **Conséquences** : fenêtres +1–5 et +6–20 journées de cotation **après D**
  (transitions confirmées) ou **après C** (non confirmées, publiées
  séparément). Une fenêtre est **tronquée à la veille de la prochaine date
  candidate** (toute transition, confirmée ou non) ; la troncature est
  signalée par fenêtre et comptée. Distributions publiées : quantiles des
  rendements journaliers (rendement = log-clôture M1 de fin de journée /
  log-clôture de fin de journée précédente, en bp), RV, asymétrie (§7),
  fréquence d'extrêmes (§7), fréquences d'impulsions IMP-M5 et de
  dépassements (définitions des campagnes 1–3, inchangées) par journée.

## 6. Échelle intrajournalière (famille REG-S, séparée)

RV de session = √(Σ r²) × 10⁴ sur les rendements M1 internes à la session
(premier rendement de session exclu, symétriquement au §3) ; seuils
terciles causaux propres à chaque session (60 journées précédentes, min
40) ; état de session connu à la clôture de la session, conséquences au
plus tôt à la session suivante. Publications : changements d'état entre
sessions consécutives (intra-journée et franchissement de nuit distingués),
part des journées où l'état de session maximal diffère de l'état courant
journalier (déphasage intrajournalier).

## 7. Dimensions non-F3 (famille DIM) — formules exactes (correction n° 6)

| Dimension | Formule figée |
|---|---|
| Asymétrie journalière | g1 = m₃ / m₂^{3/2} sur les rendements M1 internes du jour (moments empiriques centrés, **sans correction de biais**) ; état = tercile causal de g1 (60 journées précédentes, min 40) |
| Queues / extrêmes | Seuil du jour = quantile 99 des \|r\| M1 **poolés des 60 journées précédentes** (minimum 20 000 barres, sinon pas de mesure) ; fréquence du jour = part de ses barres M1 avec \|r\| > seuil (seuil du passé, mesure du jour) ; état de queue = tercile causal de cette fréquence (60 journées précédentes, min 40) |
| Volatilité de la volatilité | Mesure du jour j = écart-type des log(RV) sur les **20 dernières journées écoulées y compris j** ; état = tercile de cette mesure contre ses valeurs des 60 journées précédentes **excluant j** (min 40) |
| Dispersion intrajournalière | Ratio RV_session_max / RV_session_min du jour, calculé uniquement si **≥ 3 sessions utilisables** ; état = tercile causal (60 journées précédentes, min 40) ; jours non calculables comptés |
| Sessions et changements d'heure | Horaires **UTC fixes** (Asie 00–08, Londres 08–13, New York 13–21, nuit 21–24) toute l'année ; le corpus est horodaté UTC, **aucun changement d'heure n'existe dans les données** ; il est explicitement publié que ces fenêtres UTC fixes ne suivent pas les heures locales de Londres/New York lors de leurs changements d'heure — convention assumée et constante, donc sans rupture artificielle de définition dans le temps |

Chaque dimension publie aussi sa valeur continue ; le vocabulaire de
« régime » ne leur est pas appliqué.

## 8. Ce que le dictionnaire interdit

Présenter la RV ou l'état courant d'un jour comme connus à son ouverture ;
antidater une confirmation ; supprimer une transition non confirmée ;
faire glisser la référence d'un retour à l'habituel pendant l'épisode ;
présenter un tercile poolé (F3 ou autre) comme connu en temps réel ;
transformer un état, une transition ou une discordance en signal
directionnel ; modifier F3 ; appliquer le vocabulaire de régime aux
dimensions DIM. « Événements structurels » = internes uniquement (sessions,
frontières de journée, événements catalogués) ; aucun calendrier exogène
(FRED suspendue).

## 9. Résumé des changements par rapport à la version 1 (seq 193)

1. **F3** : causalité auditée et documentée (walk-forward 500 j, horizon
   1 j, connaissable à la clôture de la veille) ; **non-causalité des
   terciles poolés historiques explicitement constatée** ; double
   publication causal/rétrospectif, seul le causal porte « connu à
   l'ouverture ».
2. **RV** : formule, rendements intra-journée uniquement, délimitation
   UTC, qualité (≥ 300 barres), fenêtre exacte des 60 journées précédentes
   (min 40) figées ; conséquences au plus tôt le jour suivant.
3. **Transitions** : premier franchissement, traversée et classes de
   vitesse figées (**rapide 1–2 j, intermédiaire 3–4 j, progressive ≥ 5 j**),
   confirmation D = C + 2 explicitée, catalogue obligatoire des non
   confirmées avec motifs.
4. **Retour à l'habituel** : référence **figée au début de chaque épisode
   HAUT** (la version à seuil glissant est abandonnée) ; niveaux absolus
   publiés à côté des états relatifs.
5. **Comparaisons** : liste exacte des dix publiée dans le document
   compagnon `CAMPAIGN_04_COMPARISONS_FREEZE.md` (variables, populations,
   fenêtres, unités, matérialité) ; bootstrap par blocs de 20 journées
   figé y compris le sort des fenêtres chevauchantes ; le minimum de 30
   transitions par bras est qualifié d'**éligibilité descriptive**, non de
   garantie de puissance.
6. **DIM** : formules exactes (moments non corrigés, seuil de queue poolé
   causal avec minimum de barres, fenêtre 20 j de la volatilité de la
   volatilité, règle des 3 sessions) ; sessions UTC fixes et traitement des
   changements d'heure explicités (inexistants en UTC, convention publiée).
7. **T0** (chantier séparé) : clarification des 4 200 indépendants totaux
   dans le document compagnon `CAMPAIGN_2_4_TERC
...[truncated 911 chars]