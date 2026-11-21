# CAMPAGNE 8 — PROTOCOLE SCIENTIFIQUE F-J « CHOCS MINUTE EXTRÊMES ET LEUR SILLAGE » — V1 PROPOSÉE

**Statut : CONSOLIDATION SOUMISE AU PROPRIÉTAIRE — NON GELÉE, AUCUN CALCUL
AUTORISÉ NI EFFECTUÉ.** Consolide le blueprint et le dictionnaire F-J
(seq257–258) selon la décision de consolidation du fondateur. XAU/USD,
corpus IS uniquement ; holdout scellé ; aucun backtest ni `challenge_sim` ;
aucun J2/J3 automatique ; aucun budget expérimental consommé ; FRED
suspendue ; 36 cellules S12 gelées ; T0 séparé et inactif ; aucune fiche
historique modifiée ; F-L et F-H en réserve.

## 1. Objet et identifiants

Anatomie événementielle des variations M1 exceptionnellement importantes :
fréquence, intensité, direction, regroupement, sillage (continuation,
retour partiel, retournement, stabilisation, nouveau choc), contextes
historiques et intrajournaliers. Comparaisons : **FJ-01…FJ-05** (la
numérotation « J-01…J-05 » des documents préparatoires désigne les mêmes
comparaisons ; seul le préfixe FJ fait foi à partir du présent protocole).
Aucun présupposé prédictif ou exploitable.

## 2. Données

Corpus IS constitué : 282 partitions mensuelles, 3 540 993 barres M1,
3 097 journées présentes. Barres : horodatage = début de barre ; clôture
c_t disponible à la fin de la minute t. Segments : suites de barres
consécutives sans écart supérieur à 1 minute.

## 3. Dictionnaire mathématique et détection causale

- Variation minute : **r_t = ln(c_t / c_{t−1}) × 10⁴ (bp)**, définie
  uniquement si la barre précédente termine exactement 1 minute avant,
  dans le même segment. Aucune variation n'est calculée à travers un
  trou ni à travers une reprise de cotation.
- Jour d'attribution d'une barre : sa journée UTC. Ères : 2010–2013,
  2014–2016, 2017–2020 (année de la journée d'attribution).
- Fenêtre de référence causale du jour D : variations valides des
  **20 journées présentes précédentes** (ou de toutes les journées
  précédentes disponibles si elles sont entre 10 et 19). Seuil :

  **T_D = max(10 bp, Q₉₉,₅(|r| sur la fenêtre causale))**

  où Q₉₉,₅ est le quantile à 99,5 % par **interpolation linéaire**
  (méthode « linear », type 7) sur l'ensemble poolé des |r| de la
  fenêtre. T_D est calculé avant l'ouverture de D et **fixe pendant
  toute la journée D**.
- Éligibilité de la référence : D est éligible à la détection si au
  moins **10 journées antérieures valides** existent et si la fenêtre
  contient au moins **10 000 variations valides**. Sinon, journée
  **INÉLIGIBLE_DÉTECTION** publiée ; aucun choc n'y est identifié, et
  aucun seuil rétroactif n'est substitué.
- Prédicat de choc (**strict**) : la barre t est un **choc** si et
  seulement si **|r_t| > T_D** (inégalité stricte), D étant le jour de
  t éligible. Signe : **+** si r_t > 0, **−** si r_t < 0. Disponibilité
  du choc : clôture de la barre t.
- Intensité relative du choc : **ρ_t = |r_t| / T_D**. Classes :
  **MODÉRÉ** si 1 < ρ_t < 2 ; **MAJEUR** si ρ_t ≥ 2.
- Aucun quantile poolé 2010–2020 ne sert à la détection. Une éventuelle
  référence poolée rétrospective ne peut être publiée qu'en descriptif
  séparé étiqueté non causal, sans mélange avec les chocs causaux.

## 4. Épisodes : classification et regroupement

- Tri chronologique de tous les chocs. **Règle de regroupement** : deux
  chocs consécutifs appartiennent au même épisode si l'écart entre
  leurs horodatages de début de barre est **≤ 15 minutes (borne
  inclusive)** ; un écart **> 15 minutes clôt** l'épisode au choc
  précédent et en ouvre un nouveau.
- Un épisode peut traverser une frontière UTC minuit (écart ≤ 15 min
  des deux côtés) ; son **jour d'attribution est le jour UTC de son
  premier choc**. Il peut de même traverser un trou inférieur ou égal
  à 15 minutes sans choc ; aucune variation n'est fabriquée dans le
  trou.
- **Clôture d'un épisode** : 15 minutes écoulées sans nouveau choc
  après son dernier choc. L'épisode n'est donc définitivement
  identifiable que rétrospectivement, à la clôture du dernier choc
  + 15 minutes ; **aucune disponibilité en temps réel n'est
  revendiquée** pour l'appartenance à un épisode.
- Classe de signe de l'épisode : **POSITIF** si tous ses chocs sont +,
  **NÉGATIF** si tous sont −, **MIXTE** s'il contient les deux signes.
  Les épisodes MIXTES sont publiés séparément (effectifs, intensités,
  sillages descriptifs) et **exclus des comparaisons directionnelles
  primaires** FJ-01…FJ-05.
- **Épisode isolé** : exactement 1 choc. **Épisode regroupé** : ≥2 chocs.
- Descripteurs publiés par épisode : premier et dernier horodatages de
  choc, nombre de chocs, **amplitude A = max des |r_t|** de ses chocs,
  intensité ρ_max = A / T du jour du choc maximal, durée
  (dernier − premier choc), classe de signe, drapeau MIXTE, jour
  d'attribution, ère et session du premier choc.
- **Unité statistique primaire : l'épisode.** Les chocs intra-épisode
  ne sont jamais des observations indépendantes ; ils alimentent des
  comptages descriptifs seulement.

Sessions UTC (ventilation fermée) : **S1 00:00–06:59, S2 07:00–12:59,
S3 13:00–20:59, S4 21:00–23:59**, selon l'horodatage du premier choc.

## 5. Sillage

Horodatages conservés pour tout épisode : **début du premier choc** et
**clôture du dernier choc**. Prix d'ancrage : **c₀ = clôture de la barre
du dernier choc**. Le sillage est mesuré depuis l'ancrage ; il est
intégralement rétrospectif.

- **Continuation signée à horizon h** : **R_h = s × ln(c_{t₀+h} / c₀)
  × 10⁴ (bp)**, où s est le signe de l'épisode (+1 POSITIF, −1 NÉGATIF),
  t₀ la minute du dernier choc, c_{t₀+h} la clôture de la barre débutant
  à t₀ + h. Horizons descriptifs : **+15, +30** ; **horizon principal :
  +60**. Positive : le prix a continué dans le sens de l'épisode.
- Disponibilité de R_h : la barre t₀ + h doit exister dans le même
  segment prolongé sans trou > 15 minutes sur (t₀, t₀ + h] ; sinon
  **CENSURE_FENÊTRE** publiée pour cet horizon (statuts par horizon,
  aucun observable silencieux). Un sillage peut traverser minuit si le
  segment le permet.
- **Retour partiel à 60 min** : part retracée = max(0, −R₆₀) / A.
  **Retournement à 60 min** : R₆₀ < −A (le prix a dépassé, en sens
  inverse, l'amplitude maximale de l'épisode).
- **Excursions à 60 min** : maximales favorable et défavorable (barres
  haut/bas) signées par s, en bp par rapport à c₀, si la fenêtre est
  complète au sens ci-dessus, sinon censurées.
- **Stabilisation** : ratio (somme des |r| sur les 60 minutes suivant
  l'ancrage, ancrage exclu) / (somme des |r| sur les 60 minutes
  précédant le premier choc, premier choc exclu) ; chaque somme exige
  son segment complet, sinon valeur manquante publiée.
- **Nouveau choc** : présence d'un choc appartenant à un épisode
  ultérieur dont le premier choc débute dans (t₀, t₀ + 60] ; publié
  pour tout épisode à fenêtre complète.
- **Chevauchement des sillages** : deux épisodes distincts sont séparés
  par > 15 minutes, mais leurs fenêtres de 60 minutes peuvent se
  chevaucher ; ces épisodes partagent alors une partie de leur futur
  observé. Ils restent des unités distinctes mais sont **regroupés
  statistiquement par la grappe-journée** (§7) ; les chevauchements
  sont comptés et publiés. Tout événement de sillage dont l'ordre
  dépend d'un parcours inobservé (trou) est **indéterminé** et censuré.

## 6. Pseudo-événements (FJ-05)

Algorithme déterministe, variables **antérieures uniquement**, aucun
appariement sur un résultat futur :

1. **Bassin** : pour chaque journée éligible et chaque session S1–S4,
   la **première minute m** telle que : r_m est défini et non nul ;
   m n'est pas un choc ; aucun choc dans les 60 minutes précédant m ;
   les 60 minutes précédant m sont segment-complètes (activité
   pré-événement calculable). Au plus un pseudo-événement par
   (journée, session).
2. Descripteurs causaux du pseudo-événement : signe = signe de r_m ;
   **activité pré-événement** = somme des |r| des 60 minutes précédant
   m ; tercile de cette activité calculé au sein de la même session
   sur le bassin (descriptif de stratification, jamais sur le sillage).
3. **Appariement** : épisodes isolés traités par ordre chronologique ;
   chacun est apparié au **premier pseudo-événement encore inutilisé**
   de même session, même signe et même tercile d'activité
   pré-événement (activité de l'épisode = somme des |r| des 60 minutes
   précédant son premier choc, mêmes terciles de session). Un
   pseudo-événement ne sert qu'une fois. Épisode sans partenaire :
   publié comme non apparié.
4. **Aucune exclusion rétrospective** : un choc survenant dans les
   60 minutes suivant un pseudo-événement **n'exclut pas** celui-ci ;
   il fait partie du comportement observé après le pseudo-événement et
   est publié (drapeau NOUVEAU_CHOC du pseudo-événement). Seules les
   règles de censure de fenêtre du §5 s'appliquent au sillage.
5. Si les appariements obtenus sont sous les seuils d'éligibilité du
   §7, FJ-05 est **NON ÉVALUABLE (comparabilité insuffisante)**,
   publiée comme telle, sans élargissement des strates ni réutilisation
   des pseudo-événements.

## 7. Comparaisons, méthode, multiplicité

Variable principale commune : **R₆₀**. Matérialité : **10 bp** sur la
différence de médianes. Inférence : **bootstrap par grappes-journées**
(grappe = jour d'attribution de l'épisode ; pour FJ-05, grappe = jour
de l'épisode, le pseudo-événement apparié suivant son épisode dans le
rééchantillonnage), 2 000 réplicats, graine publiée au gel ; différences
de médianes, IC percentile 95 %, p bilatérales. **BY à m = 5 fixe**
(H₅ = 2,283333) ; règle des p NaN STRUCTURELLEMENT_NON_EVALUABLE
héritée (aucune imputation, facteur 5 conservé). Éligibilité par bras :
**≥200 épisodes et ≥100 grappes-journées**, sinon NON_ELIGIBLE publiée
sans assouplissement. Lectures : CANDIDATE_J1 /
SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL / NÉGATIF / NON_ELIGIBLE /
STRUCTURELLEMENT_NON_EVALUABLE / NON_EVALUABLE (FJ-05).

| ID | Hypothèse | Populations (épisodes non MIXTES) | Exclusions et censure |
|---|---|---|---|
| FJ-01 | Le sillage diffère selon le signe | isolés POSITIFS vs isolés NÉGATIFS | MIXTES exclus ; R₆₀ censuré exclu, taux publiés |
| FJ-02 | Le sillage diffère selon le regroupement | regroupés vs isolés (R₆₀ depuis le dernier choc) | MIXTES exclus ; chevauchements de fenêtres publiés |
| FJ-03 | Le sillage dépend de l'intensité | isolés MAJEURS (ρ ≥ 2) vs isolés MODÉRÉS (1 < ρ < 2) | amplitudes en bp publiées (ρ est relatif au seuil du jour) |
| FJ-04 | Le sillage a évolué entre ères | isolés 2010–2013 vs 2017–2020 (2014–2016 publiée hors test) | fréquences et seuils par ère publiés |
| FJ-05 | Le sillage après un choc diffère de celui de minutes non extrêmes comparables | isolés appariés vs leurs pseudo-événements (§6) | non appariés publiés ; NON_EVALUABLE si comparabilité insuffisante |

Ventilation fermée publiée sans test supplémentaire : par session
S1–S4 de chaque bras (effectifs, médianes R₆₀), fréquences de chocs
par ère/session/signe, distributions d'intensité, part retracée,
retournements, taux de nouveau choc, stabilisation. Négatifs et non
éligibles publiés.

## 8. Matrice de couverture par ère

| Ère | Journées présentes (C6) | Remarque de conception |
|---|---|---|
| 2010–2013 | 1 245 | amorçage causal en tout début 2010 (jours inéligibles publiés) |
| 2014–2016 | 932 | publiée intégralement ; hors bras primaires de FJ-04 |
| 2017–2020 | 920 | — |

Le quantile 99,5 % causal implique par construction de l'ordre de
0,5 % des minutes au-dessus du seuil relatif (avant prédicat strict et
plancher), soit un ordre de grandeur de quelques milliers de chocs sur
la décennie : estimation de conception, pas un résultat.

## 9. Registre des biais et limites

D1–D11 du dossier préparatoire, inchangés, auxquels le présent
protocole répond : D1 seuil poolé (interdit, §3) ; D2 amorçage
(inéligibilité publiée) ; D3 indépendance (épisodes + grappes) ; D4
sillages chevauchants (grappes, comptages) ; D5 saut après trou
(aucune variation trans-trou) ; D6 plancher 10 bp et ρ publié avec les
bp ; D7 contexte d'activité (terciles causaux, FJ-05) ; D8 censures
publiées, ordre indéterminé déclaré ; D9 aucune lecture prédictive ;
D10 dérive microstructurelle (FJ-04, publications par ère) ; D11
MIXTES publiés séparément, exclus des primaires. S'ajoute : **D12** —
l'appartenance à un épisode regroupé n'est connue qu'après coup ; tout
sillage d'épisode regroupé est rétrospectif et étiqueté comme tel.

## 10. Coût et suspension

Un passage de détection causale et un passage épisodes/sillages sur le
corpus existant : **un run CI unique** attendu de l'ordre des
campagnes 5–7, synthèse locale, 0 FCFA, aucun budget expérimental
consommé. Suspension documentée en cas d'échec ou de dépassement, sans
dégradation (ni fenêtre raccourcie, ni seuil assoupli, ni population
réduite).

## 11. Audit de nouveauté (campagnes 0–7)

Première famille dont l'événement est une **variation statistiquement
extrême datée causalement** — ni niveau franchi (0–2, 5, 7), ni état
agrégé (4), ni épisode d'extension (3), ni ouverture (5), ni forme de
journée (6). Distincte de F3/HAR et F7 : aucun modèle, aucune
prévision, aucune classification ; le seuil causal date des
événements, il ne définit pas un régime exploitable. Le sillage
descriptif (continuation/retour/stabilisation/nouveau choc) n'a été
mesuré par aucune campagne close. Aucune fiche C3/C4/C5 modifiée ni
confirmée.

## 12. Les dix constantes — valeurs, formules, justifications

| # | Constante | Valeur retenue | Justification |
|---|---|---|---|
| 1 | Fenêtre causale | 20 journées précédentes | ≈ un mois de cotation : assez de variations pour un quantile 99,5 % stable, assez récente pour suivre la microstructure ; acceptée par le fondateur |
| 2 | Quantile et prédicat | Q₉₉,₅ interpolation linéaire ; choc si |r_t| > T_D (strict) | queue extrême (≈0,5 % des minutes) sans rareté ingérable ; méthode d'interpolation figée ; inégalité stricte acceptée |
| 3 | Plancher absolu | 10 bp dans T_D = max(10, Q₉₉,₅) | empêche qu'un calme exceptionnel déclare « extrêmes » des variations triviales ; formule du fondateur |
| 4 | Amorçage | ≥10 journées antérieures et ≥10 000 variations | en deçà, le quantile causal n'est pas estimable de façon défendable ; inéligibilité publiée plutôt que seuil rétroactif |
| 5 | Classes d'intensité | MODÉRÉ 1 < ρ < 2 ; MAJEUR ρ ≥ 2, ρ = |r_t|/T_D | un choc double de son seuil constitue un changement d'échelle lisible ; bras FJ-03 |
| 6 | Regroupement | écart ≤ 15 min (inclusif) entre chocs consécutifs | fenêtre minimale acceptée ; sépare l'impulsion unique de la séquence agitée sans fusionner des événements distants |
| 7 | Horizons de sillage | +15/+30 descriptifs ; **+60 principal** | une heure : horizon où continuation et retour se départagent à l'échelle minute sans dépendre de la fin de journée |
| 8 | Matérialité | 10 bp sur la différence de médianes de R₆₀ | du même ordre que le plancher de détection : en deçà, l'écart de continuation est déclaré sans matérialité pour un événement déjà ≥10 bp |
| 9 | Pseudo-événements | première minute éligible par (journée × session), appariement chronologique sans réutilisation sur session × signe × tercile d'activité causale | déterminisme total (reproductible sans graine), appariement antérieur uniquement, jamais d'exclusion pour choc ultérieur |
| 10 | Épisodes MIXTES | publiés séparément, exclus des primaires FJ-01…FJ-05 | leur signe net est indéfini ; les inclure forcerait un classement arbitraire par premier ou dernier choc |

Constantes de méthode associées (rappel, non négociables au gel
suivant) : bootstrap 2 000 réplicats par grappes-journées, BY m = 5,
éligibilité ≥200 épisodes et ≥100 grappes-journées par bras.
