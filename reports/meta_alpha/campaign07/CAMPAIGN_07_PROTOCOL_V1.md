# CAMPAGNE 7 — PROTOCOLE CONSOLIDÉ F-I « NOMBRES RONDS DU XAU/USD » (V1)

**Statut : CONSOLIDATION AUTORISÉE (seq247) — SOUMIS AU PROPRIÉTAIRE
AVANT TOUT GEL. AUCUN CALCUL F-I, AUCUNE EXTRACTION, AUCUNE
CONSULTATION DE RÉSULTATS.** Ce document unique consolide le blueprint
(`749d3456…`), le dictionnaire (`334c8939…`), les comparaisons
(`a89e5a2a…`) et la couverture/biais (`d8c06fe f…`) de la préparation
seq246, intègre la correction placebo par anneau et les constantes
validées par le fondateur. En cas de tension, le présent protocole
prévaut sur les documents de préparation.

## 1. Blueprint (objectif)

Déterminer si les niveaux de prix ronds du XAU/USD présentent des
comportements spécifiques **par rapport à des niveaux placebo
réellement comparables** : approche, première touche, franchissement
strict, rejet, retour de l'autre côté, maintien au-delà, distance
post-franchissement, et dépendance à l'échelle du nombre rond. Sans
présupposer l'influence des ronds : l'absence d'écart rond − placebo
est une conclusion publiable et utile. Descriptif uniquement ; aucune
stratégie, aucun déclencheur ; candidates éventuelles au catalogue J1
sans promotion automatique.

## 2. Grilles réelles et placebo (correction fondatrice intégrée)

Un décalage unique ne peut pas être le « demi-pas » d'anneaux
d'espacements différents. Constructions **séparées par anneau** :

| Anneau / grille | Niveaux réels | Espacement | Placebo | Nature du décalage | Chevauchement |
|---|---|---|---|---|---|
| **G50** (grille primaire) | multiples de 50 USD | 50 USD | **P50 = niveaux +25 USD** (≡25 mod 50) | **demi-pas exact** (25 = 50/2) | aucun : un niveau P50 n'est jamais multiple de 10 |
| **R100** | multiples de 100 USD | 100 USD | P100 = niveaux +25 USD (≡25 mod 100) | **translation non équivalente : quart de pas** — le demi-pas (+50) est interdit car il tomberait exactement sur R50, grille réelle | aucun : ≡25 mod 100 n'est jamais multiple de 10 |
| **R50** (anneau : multiples de 50 non multiples de 100) | ≡50 mod 100 | 100 USD entre niveaux de l'anneau (pas de la grille mère G50 : 50) | P50 (+25 USD) | demi-pas de la grille mère G50, référence validée par le fondateur | aucun (≡25 ou 75 mod 100, jamais multiple de 10) |
| **R10** (anneau : multiples de 10 non multiples de 50) | ≡10,20,30,40 mod 50 | 10 USD (rythme de la grille des multiples de 10) | P10 = niveaux +5 USD (≡5 mod 10) | **demi-pas exact** du pas 10 | aucun : ≡5 mod 10 n'est jamais multiple de 10 |

Règles fermées : les placebos géométriquement différents (demi-pas
exact pour G50 et R10, quart de pas pour R100) **ne sont jamais
présentés comme une même expérience parfaitement appariée** ; chaque
comparaison n'utilise que le placebo de sa propre grille ; aucune
comparaison croisée entre placebos. Les comparaisons primaires
(I-01, I-02, I-03, I-05) portent sur **G50 contre P50** (seul couple à
demi-pas exact à l'échelle principale) ; P100 et P10 ne servent qu'aux
publications descriptives d'exposition, jamais à un test non
préenregistré. Distances toujours publiées en USD **et** en bp
(distance/niveau × 10⁴) ; le pas de 50 USD vaut ≈455 bp à 1 100 USD,
≈278 bp à 1 800, ≈192 bp à 2 600 USD (resserrrement relatif documenté,
traité par I-05, jamais par redéfinition de grille).

**Comparabilité des occasions de contact (contrôle d'exposition)** —
publié par bras avant toute lecture : nombre d'approches par journée
présente, distribution des distances initiales (bp à l'entrée
d'épisode), répartition par ère et par session. Si les occasions de
contact des deux grilles diffèrent structurellement, la règle de
composition du §7 s'applique.

## 3. Dictionnaire mathématique et événements (constantes validées)

Conventions : barres M1 horodatées par leur début, **disponibles à
leur clôture** ; journée civile UTC ; niveau noté Λ (USD) ; prix
d'une barre : [bas, haut], clôture c.

- **Distance au niveau** d'une barre : d = 0 si bas ≤ Λ ≤ haut, sinon
  min(|bas − Λ|, |haut − Λ|) ; en bp : d_bp = d / Λ × 10⁴.
- **Approche** (constante gelée : bande **25 bp**) : première barre
  avec d_bp ≤ 25 alors qu'**aucune** des barres des **60 minutes**
  précédentes (washout gelé) n'avait d_bp ≤ 25. L'épisode s'ouvre à la
  clôture de cette barre ; distance initiale = d_bp de cette barre
  (≤25 par construction, réalisée publiée). Côté d'approche figé :
  clôture de la barre précédente sous Λ = par en dessous (symétrique).
- **Touche** : première barre de l'épisode avec d = 0 **sans**
  franchissement strict à cette même barre.
- **Franchissement strict** : première barre dont la **clôture** est
  strictement au-delà de Λ par rapport au côté d'approche. Une barre
  qui touche et clôture au-delà est un franchissement (convention C5) ;
  connu à la clôture de la barre.
- **Franchissement par saut (SAUT)** : ouverture d'une barre déjà
  au-delà de Λ sans barre de contact préalable dans l'épisode (trou ou
  ouverture de journée) : classé à part, exclu du primaire, publié.
- **Rejet** (constante gelée : seuil **25 bp**) : après une touche,
  première clôture revenue à d_bp ≥ 25 du côté d'approche, dans les
  **60 minutes** suivant la barre de touche, sans franchissement strict
  préalable.
- **Retour / maintien** : après un franchissement strict, première
  clôture revenue du côté d'origine (**retour**) dans la fenêtre de
  suivi de **60 minutes** (constante gelée) ; à défaut, **maintien
  au-delà** constaté à la clôture de la 60e minute.
- **Distance post-franchissement** : max, sur la fenêtre de suivi, de
  l'excursion au-delà de Λ (haut − Λ en approche par en dessous,
  symétrique), en bp de Λ ; disponible à la fin de la fenêtre.
- **Fenêtre de suivi** : les 60 minutes suivant la barre d'événement ;
  statut COMPLETE si les 60 barres y sont présentes sans trou > 15 min
  (hérité C5/C6), sinon CENSURÉE : aucun observable de suivi n'est
  calculé silencieusement sur fenêtre incomplète.
- **SIMULTANÉ** : barre dont [bas, haut] contient deux niveaux réels
  distincts de la grille testée : ordre entre niveaux indéterminé,
  épisode exclu du primaire, publié. Fin de journée UTC sans événement
  terminal : censure publiée.
- Variables par épisode : grille/anneau, Λ, côté, date, heure, distance
  initiale (USD et bp), touche et délai, franchissement strict et
  délai, SAUT, rejet, retour, maintien, distance post-franchissement,
  statuts de censure/fenêtre, ère, session UTC d'approche (§7), journée
  (grappe). Aucune variable n'utilise d'information postérieure à sa
  fenêtre ; les suivis sont rétrospectifs à l'épisode.

## 4. Règles de causalité et de disponibilité

Tout événement est daté à la **clôture** de la barre qui le réalise ;
approche, touche et franchissement ne sont connus qu'à cette clôture.
Aucune reconstruction de donnée manquante, aucune interpolation : un
trou dans la bande ou dans le suivi produit SAUT ou censure, jamais un
contact supposé.

## 5. Les cinq comparaisons préenregistrées (architecture conservée)

Matérialité commune : 5 points de pourcentage ; ratio 1,15 pour I-03
(borne exacte 1/1,15 = 0,8695652173913043, |ln ratio| vs ln 1,15).
Unité : épisode d'approche ; grappe : journée. Éligibilité : ≥200
épisodes et ≥100 grappes par bras. Exclusions communes du primaire :
épisodes SAUT, SIMULTANÉS, à suivi censuré (pour les variables de
suivi), publiés séparément.

| ID | Hypothèse exacte | Anneau / grilles | Population A vs B | Matérialité | Dépendances potentielles |
|---|---|---|---|---|---|
| I-01 | P(franchissement strict \| approche) diffère entre niveaux ronds et placebo comparable | G50 vs P50 (+25, demi-pas) | approches G50 vs approches P50 | 5 pts | occasions de contact inégales entre grilles (§2, §7) ; épisodes d'une même journée corrélés (grappes) |
| I-02 | P(rejet \| touche) diffère entre ronds et placebo | G50 vs P50 | touches G50 vs touches P50 (franchissements même barre exclus par définition) | 5 pts | conditionnement sur la touche (les deux bras subissent la même définition) ; composition des touches |
| I-03 | La distance post-franchissement diffère entre ronds et placebo | G50 vs P50 | franchissements stricts G50 vs P50 à suivi complet | ratio 1,15 | volatilité du moment confondue possible ; ventilation de composition ; distances en bp relatives au niveau |
| I-04 | P(franchissement strict \| approche) diffère selon l'échelle du rond | anneaux réels disjoints R100 vs R10 (aucun placebo) | approches R100 vs approches R10 | 5 pts | pas d'anneau très différents (100 vs 10 USD) : en bp, l'écart d'échelle varie avec l'ère ; aucun niveau compté deux fois |
| I-05 | L'écart (G50 − P50) de P(franchissement) a changé entre ères | G50 vs P50, par ère | approches 2010–13 vs 2017–20 (différence des différences ; 2014–16 publiée) | 5 pts | resserrement relatif de la grille absolue quand le prix monte ; couverture et composition par ère |

## 6. Méthode statistique et multiplicité

Bootstrap par **grappes-journées**, 2 000 réplicats, graine publiée au
gel ; IC percentile 95 % ; p bilatérales ; I-05 en différence des
différences sur les mêmes grappes. **BY famille fermée de cinq à m = 5
fixe** (H₅ = 2,283333 ; p NaN publiée sans imputation si une hypothèse
devient structurellement impossible ; statut
STRUCTURELLEMENT_NON_EVALUABLE). Lectures fermées : CANDIDATE_J1 /
SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL / NEGATIF / NON_ELIGIBLE /
STRUCTURELLEMENT_NON_EVALUABLE, plus le déclassement de composition du
§7. Publication intégrale des effectifs, censures, couvertures, effets,
IC, p, q, matérialités, négatifs et non éligibles.

## 7. Contrôle de composition (règle déterministe, sans p ajoutée)

Variables de contexte **connues au moment de l'approche** uniquement :
ère (2010–13 / 2014–16 / 2017–20), fenêtre de session UTC de l'approche
(ASIE 00–08, LONDRES 08–13, NEWYORK 13–21, NUIT 21–24 — convention C5),
sens d'approche (par en dessous / par au-dessus), distance initiale
réalisée (bp), exposition (approches de la grille par journée).
**Aucune étiquette F3 poolée** ; aucune variable de journée complète
(amplitude du jour notamment, inconnue à l'approche) dans la règle.

Pour chaque comparaison rond vs placebo, écarts de composition entre
bras (différences de proportions par catégorie ; différence de
médianes pour la distance initiale ; ratio des expositions médianes) :

- **ASSOCIATION CONSERVÉE** : tous les écarts sous les seuils —
  proportions par ère, session et sens : < 5 points par catégorie ;
  distance initiale médiane : < 2 bp ; ratio d'exposition dans
  [0,8696 ; 1,15]. La lecture suit les règles communes.
- **ASSOCIATION SENSIBLE À LA COMPOSITION** : au moins un écart
  au-dessus d'un seuil, mais chaque strate ère × session × sens
  nécessaire à la lecture conserve ≥30 épisodes par bras : les écarts
  rond − placebo **par strate** sont publiés (descriptif, sans test),
  et toute lecture CANDIDATE_J1 est déclassée en
  **ASSOCIATION_SENSIBLE_A_LA_COMPOSITION (pas de candidate)** ; les
  lectures déjà négatives ou sous le seuil restent, avec le drapeau.
- **NON ÉVALUABLE — COMPOSITION** : plus de 25 % des épisodes d'un bras
  tombent dans des strates à <30 épisodes dans l'autre bras, ou les
  distributions de distance initiale sont disjointes (médianes
  distantes de >10 bp) : la comparaison est déclarée non évaluable
  faute de données comparables, effectifs publiés.

Aucun test, aucune p-value, aucune comparaison supplémentaire n'est
créé par ce contrôle ; il ne produit que des écarts publiés et le
déclassement ci-dessus.

## 8. Matrice de couverture (déjà publiée)

282 partitions, 3 540 993 barres M1, 3 097 journées présentes, 2 572
utilisables (C4/C5) ; ères et pas relatifs approximatifs : 2010–13
(prix ~1 000–1 900, pas de 50 ≈ 260–500 bp), 2014–16 (~1 050–1 400,
≈360–480 bp), 2017–20 IS (~1 150–1 650, ≈300–430 bp) ; holdout scellé
hors matrice. Effectifs d'épisodes inconnus avant extraction ; tout
bras sous les seuils sera NON_ELIGIBLE sans fusion d'anneaux.

## 9. Registre des biais

C1 snooping de grille (grilles a priori + placebo) ; C2 effet de
parcours général (placebo seul interprété) ; C3 volatilité/session/
amplitude (ventilations + §7, variables connues à l'événement
uniquement) ; C4 échelle absolue vs relative (double unité, I-05) ;
C5 touche vs franchissement (clôture stricte) ; C6 ordre intra-barre
(SAUT/SIMULTANÉ publiés) ; C7 épisodes répétés (washout 60 min,
grappes-journées) ; C8 suivi incomplet (statuts, rien de silencieux) ;
C9 dérive décennale du prix (côtés publiés, côté figé à l'épisode) ;
C10 mécanisme « psychologique » non démontrable par le seul contact
(limite énoncée dans toute candidate éventuelle) ; **C11** —
placebos d'anneaux géométriquement non équivalents (quart de pas
R100) : jamais présentés comme l'expérience appariée de G50, usage
primaire limité au couple G50/P50 à demi-pas exact.

## 10. Budget, suspension, restrictions, nouveauté

Un run CI unique attendu, synthèse locale, 0 FCFA, aucun budget
expérimental ; suspension documentée en cas d'échec, aucune
dégradation méthodologique pour terminer. Nouveauté vs campagnes 0–6 :
niveaux **exogènes** (contre extrêmes endogènes des campagnes 0–2 et
atteintes de la veille en C5), question de **contact** (contre
dépassement-réintégration), **placebo décalé intégré** (absent de tout
le programme antérieur), aucune grandeur de forme F-G. Restrictions
inchangées : XAU/USD, holdout scellé, aucun backtest ni
`challenge_sim`, aucun J2/J3, FRED suspendue, S12 gelées, T0 inactif,
fiches historiques inchangées, candidates C5 sans priorité, F-H en
réserve.

## 11. Soumission

Protocole consolidé soumis au propriétaire pour validation avant gel.
Après validation seulement : gel chaîné, puis ordre d'exécution
séparé. Aucune constante (25 bp, 60 min, 25 bp, 60 min, grilles,
seuils de composition) ne sera optimisée ni modifiée après le gel.
