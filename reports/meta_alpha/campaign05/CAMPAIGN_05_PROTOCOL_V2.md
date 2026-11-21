# CAMPAGNE 5 — PROTOCOLE CONSOLIDÉ (VERSION 2, À VALIDATION DÉFINITIVE)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE — AUCUN
CALCUL LANCÉ.** Version consolidée du blueprint, du dictionnaire et des
dix comparaisons, produite après approbation conditionnelle (seq 211).
Elle **remplace pour l'exécution** les documents de préparation seq 209
(conservés inchangés pour traçabilité) et reste soumise à validation
définitive : si elle est validée, son hash sera chaîné avant toute
extraction et aucune définition ne pourra changer après consultation des
résultats. Résumé des corrections au §8.

## 1. Conventions horaires complètes

- Horodatages **UTC** de bout en bout ; le corpus ne connaît **aucun
  changement d'heure** (UTC n'en a pas). Aucune convention d'heure locale
  n'est mélangée à celle-ci.
- Sessions en **fenêtres UTC fixes toute l'année** : ASIE [00:00, 08:00),
  LONDRES [08:00, 13:00), NEW YORK [13:00, 21:00), NUIT [21:00, 24:00).
  Il est explicitement publié que ces fenêtres UTC fixes ne coïncident
  pas toute l'année avec les heures locales d'ouverture des places de
  Londres ou de New York (qui se décalent d'une heure en UTC selon la
  saison) : la campagne décrit des **fenêtres UTC conventionnées et
  constantes**, choix assumé pour éviter toute rupture de définition dans
  le temps ; aucune lecture « heure locale de place » n'en sera tirée.
- Journée de cotation = date UTC [00:00, 24:00) ; semaine = lundi 00:00 au
  vendredi 24:00 UTC. Journée utilisable ≥ 300 barres M1 complètes ;
  session utilisable ≥ 60 barres ; semaine utilisable ≥ 4 journées
  utilisables.
- **Heure théorique d'ouverture** (00:00, 08:00, 13:00, 21:00 UTC) et
  **heure de la première barre réellement présente** sont deux grandeurs
  distinctes, toutes deux publiées pour chaque ouverture : le **retard**
  (minutes entre l'heure théorique et le début de la première barre) est
  une observable, **jamais** un décalage appliqué silencieusement. Les
  fenêtres d'observation sont ancrées à la première barre présente
  (instant d'événement), et le retard est publié en classes : PONCTUELLE
  (≤ 1 min), LEGER (2–5 min), DIFFEREE (6–30 min), **INELIGIBLE pour les
  fenêtres d'ouverture (> 30 min ou session absente — l'événement est
  compté, daté et exclu des fenêtres, jamais reconstitué)**.

## 2. Famille F-E — Sessions (définitions mathématiques figées)

- **Ouverture de session** : première barre M1 complète dont le début
  appartient à la session ; instant d'événement = début de cette barre ;
  disponibilité des variables d'ouverture = **clôture de chaque barre**
  de la fenêtre (aucune disponibilité intra-barre n'est revendiquée, §4).
- **Fenêtres** : +5, +15, +30, +60 minutes d'horloge à partir de l'instant
  d'événement, sur les barres présentes. Observables par fenêtre :
  amplitude = (max des hauts − min des bas)/prix d'ouverture × 10⁴ (bp) ;
  rendement signé = ln(clôture de fin de fenêtre / ouverture de la
  première barre) × 10⁴ ; RV = √(Σ r²) × 10⁴ sur les rendements log M1
  internes à la fenêtre ; excursions favorable/défavorable vs prix
  d'ouverture ; spread médian (contexte uniquement).
- **Référence causale** : médiane de la même observable, même session, sur
  les **60 journées de cotation précédentes** disposant de l'ouverture
  (min 40, jour courant exclu) ; ratio à la référence publié à côté du
  brut.
- **Mouvement pré-ouverture** : rendement log signé des 60 minutes
  d'horloge précédant l'instant d'événement, sur les barres présentes,
  premier rendement exclu ; connu à l'ouverture. **Issues** (mesurées,
  fenêtres +30/+60 strictement postérieures) : poursuite si l'extension
  dans le sens du mouvement atteint ≥ 50 % de son amplitude ; retournement
  si le franchissement inverse du prix d'ouverture atteint ≥ 50 % de
  cette amplitude ; sinon stagnation ; fenêtre tronquée par fin de journée
  ou trou > 15 min = censurée et comptée.
- **Ouverture d'Asie — classes exhaustives et mutuellement exclusives**,
  appliquées dans cet ordre de priorité (trou = durée entre la fin de la
  dernière barre de la veille et le début de la première barre du jour ;
  veille = journée de cotation précédente présente dans le corpus) :
  1. **REOUVERTURE_SEMAINE** : la veille est un vendredi (le trou enjambe
     le week-end), quel que soit le trou ;
  2. **FERMETURE_EXCEPTIONNELLE** : trou > 12 heures sans week-end
     enjambé — cette classe regroupe, **sans pouvoir les distinguer dans
     les données**, jours fériés et fermetures exceptionnelles ; elle est
     publiée sous ce nom et jamais interprétée au-delà ;
  3. **TROU_INTRA_SEMAINE** : trou > 5 minutes et ≤ 12 heures (pause
     quotidienne de cotation) ;
  4. **CONTINUITE** : trou ≤ 5 minutes.
  L'écart de prix du trou (ln(première ouverture / dernière clôture de
  la veille) × 10⁴) est publié ; aucune barre n'est reconstruite.
- **Limite d'identification à 00:00 UTC** : ouverture d'Asie et frontière
  de journée y coïncident ; aucun effet mesuré à cette frontière ne sera
  présenté comme un « effet asiatique » isolé — uniquement comme un
  effet de la frontière 00:00 UTC, ventilé par classe d'ancrage et mis en
  regard des frontières 08/13/21 (sans frontière de journée).
- **Inéligibilité F-E (exhaustif)** : retard > 30 min ; session absente ;
  fenêtre tronquée par un trou > 15 min (censure publiée) ; référence
  causale < 40 journées ; journée non utilisable. Tout événement inéligible
  est compté, daté et publié.

## 3. Famille F-F — Extrêmes datés (définitions mathématiques figées)

- **bp** : point de base relatif, 1 bp = 0,01 % du prix :
  écart en bp = (Δp / p) × 10⁴, p étant le niveau de référence indiqué.
- **Niveaux de référence** : journalier = plus haut H_{j−1} et plus bas
  B_{j−1} de la **journée précédente utilisable**, connus à 00:00 UTC du
  jour j ; hebdomadaire = plus haut/bas de la **semaine précédente
  utilisable**, connus au lundi 00:00 UTC. Semaine sans référence
  utilisable : aucune atteinte déclarée, semaine publiée censurée.
- **Première atteinte (HAUT)** : première barre M1 du jour dont le haut
  **dépasse strictement** H_{j−1} ; **touch** : première barre dont le
  haut égale H_{j−1} sans le dépasser (à la précision des prix
  enregistrés, comparaison stricte sur les valeurs Mid telles que
  stockées, **aucun arrondi ni tolérance ajoutés**) ; les deux catégories
  sont publiées séparément et jamais fusionnées. Symétrique en BAS.
- **Disponibilité et horodatage** : l'événement est **daté au début de la
  barre** M1 qui le réalise ; sa **disponibilité est la clôture de cette
  barre** (début + 1 minute) : avec des barres M1, l'ordre intrabarre est
  inconnu, et rien n'est antidaté à l'intérieur de la barre. Toute
  variable « extrême courant à t » vaut à la clôture de la dernière barre
  terminée à t ; les issues sont mesurées sur les barres **suivantes**.
- **Mises à jour (pas de 5 bp formalisé)** : soit E₀ = niveau franchi
  (H_{j−1}). La mise à jour n (n = 1, 2, …) survient à la première barre
  dont l'extrême courant dépasse strictement le **prix-seuil**
  S_n = E₀ × (1 + n × 5/10⁴). Le pas est donc relatif (5 bp du niveau
  d'ancrage E₀), sans arrondi (comparaisons sur les prix enregistrés).
  Si une même barre franchit plusieurs seuils S_n, toutes les mises à
  jour correspondantes sont datées à cette barre, comptées, et leur
  **ordre interne est déclaré indéterminé** (§5). Symétrique en BAS avec
  S_n = E₀ × (1 − n × 5/10⁴).
- **Extrêmes finaux** (journalier : haut/bas de la journée complète ;
  hebdomadaire : de la semaine complète) : connus à la clôture
  uniquement, publiés dans des tableaux étiquetés « final, rétrospectif »,
  **jamais** classeurs d'événements en cours. Semaines incomplètes
  (< 4 journées utilisables, bords de corpus) : extrême final censuré et
  publié comme tel ; la semaine peut néanmoins porter des atteintes si
  son niveau de référence, lui, est utilisable (les deux statuts sont
  distincts et publiés séparément).
- **Issues après première atteinte** (barres suivant celle de
  l'atteinte) : extension supplémentaire au-delà d'E₀ (bp relatif à E₀),
  retracement maximal sous E₀ (bp), retour éventuel de l'autre côté d'E₀
  daté, position de clôture de fenêtre vs E₀ ; horizons +15/+30/+60
  minutes d'horloge ; censure de fin de journée comptée.

## 4. Disponibilité temporelle (règles contraignantes, toutes variables)

| Variable | Disponible à | Interdit |
|---|---|---|
| Niveaux de référence (veille / semaine précédente) | Ouverture de la période | — |
| Références causales 60 journées | À l'instant de l'événement (passé seul) | Tout poolage incluant le présent ou le futur |
| Mouvement pré-ouverture, trou, écart de trou, retard d'ouverture | À l'ouverture (clôture des barres concernées) | Présenter une valeur intra-barre comme connue avant la clôture de sa barre |
| Première atteinte, touch, mises à jour | Clôture de la barre qui les réalise | Antidater dans la barre ; utiliser le haut/bas final du jour |
| Extrême courant à t | Clôture de la dernière barre terminée à t | Le confondre avec l'extrême final |
| Issues (poursuite, extension, retracement…) | Après leur fenêtre | Classer l'événement d'origine par ses issues |
| Extrêmes finaux | Clôture du jour / de la semaine | Classer, sélectionner ou dater quoi que ce soit en cours de période |

## 5. Événements à ordre temporel indéterminé (publication séparée)

Constituent une sortie dédiée, jamais départagés ni fusionnés aux
séries ordonnées : (i) première atteinte HAUT et BAS dans la même barre
M1 (barre englobant les deux niveaux) ; (ii) plusieurs seuils de mise à
jour franchis dans une même barre ; (iii) première atteinte et mise à
jour confondues dans la barre d'atteinte ; (iv) ouverture de session et
première atteinte dans la même première barre. Ils sont comptés,
horodatés (début de barre), et exclus des comparaisons exigeant un ordre
(C5-06 à C5-08 le cas échéant), avec effectifs publiés.

## 6. Les dix comparaisons — unités, regroupement, matérialité explicite

Deux **familles d'inférence distinctes** (F-E : C5-01 à C5-05 ; F-F :
C5-06 à C5-10), correction **BY séparée par famille de cinq** ; **aucune
conclusion globale sur les dix n'est formulée** (pas de p ni de lecture
poolée inter-familles). Bootstrap : grappes-**journées** (2 000
répétitions, graine figée au gel d'exécution) pour F-E et F-F journalier ;
grappes-**semaines** pour C5-09. Éligibilité descriptive : ≥ 200 épisodes
et ≥ 100 grappes par bras (lisibilité, non puissance) ; cohérence de signe
≥ 2 ères sur 3 hors dimension d'ère ; lectures : candidate J1 descriptive,
significative sous le seuil matériel, négative, non éligible — **toutes
conservées et publiées**.

| ID | Famille | Comparaison (variable) | Unité statistique / grappe | Matérialité |
|---|---|---|---|---|
| C5-01 | F-E | Amplitude d'ouverture 30 min (bp, médiane) : LONDRES vs ASIE | Ouverture / journée | **ratio 1,15** |
| C5-02 | F-E | P(poursuite à +30 min) : transition NEWYORK vs LONDRES | Transition / journée | **5 points** |
| C5-03 | F-E | Amplitude première heure d'Asie (bp, médiane) : CONTINUITE vs TROU_INTRA_SEMAINE | Ouverture / journée | **ratio 1,15** |
| C5-04 | F-E | Amplitude d'ouverture Londres 30 min (bp, médiane) : lundi vs vendredi | Ouverture / journée | **ratio 1,15** |
| C5-05 | F-E | Spread médian des 15 premières minutes (bp, médiane, contexte) : NEWYORK vs LONDRES | Ouverture / journée | **ratio 1,15** |
| C5-06 | F-F | P(première atteinte avant 08:00 UTC) : HAUT vs BAS | Atteinte / journée | **5 points** |
| C5-07 | F-F | Extension supplémentaire à +60 min (bp, médiane) : HAUT vs BAS | Atteinte / journée | **ratio 1,15** |
| C5-08 | F-F | Retracement maximal à +60 min (bp, médiane) : atteintes avant 13:00 vs dès 13:00 | Atteinte / journée | **ratio 1,15** |
| C5-09 | F-F | P(première atteinte hebdomadaire avant mercredi 00:00 UTC) : HAUT vs BAS | Atteinte / semaine | **5 points** |
| C5-10 | F-F | P(journée contenue, sans atteinte ni touch) : ère 2010–13 vs 2017–20 | Journée / journée | **5 points** |

## 7. Critères d'exclusion et de censure (récapitulatif contraignant)

Journée < 300 barres : exclue des mesures, comptée, et ne sert pas de
référence (on prend la précédente utilisable) ; retard d'ouverture
> 30 min ou session absente : ouverture inéligible aux fenêtres,
comptée ; fenêtre traversée par un trou > 15 min : issue censurée ;
référence causale < 40 journées : pas de ratio publié ; semaine
< 4 journées utilisables : extrême final hebdomadaire censuré ; semaine
sans référence utilisable : aucune atteinte hebdomadaire ; événements à
ordre indéterminé : sortie séparée (§5) ; bords du corpus : amorçages et
censures comptés et publiés. Aucune exclusion silencieuse ; aucun
élargissement de fenêtre après coup ; en cas de dépassement de coût, les
règles de suspension du document de couverture s'appliquent (suspension
documentée, aucune dégradation méthodologique sans nouvelle validation).

## 8. Résumé des corrections par rapport à la préparation seq 209

1. Heure **théorique** et première barre présente séparées partout ;
   retard publié en classes, fenêtres ancrées à l'événement réel sans
   décalage automatique ; **seuil d'inéligibilité explicite à 30 min**.
2. Conventions horaires tranchées : **fenêtres UTC fixes** assumées et
   publiées comme telles face aux heures locales saisonnières de
   Londres/New York ; aucun mélange de conventions.
3. Limite d'identification à 00:00 UTC maintenue et durcie : aucun effet
   de cette frontière ne sera nommé « effet asiatique » isolé.
4. Classes d'ancrage de l'ouverture d'Asie rendues **exhaustives** avec
   ordre de priorité explicite, incluant une classe
   FERMETURE_EXCEPTIONNELLE (> 12 h hors week-end) qui regroupe fériés et
   fermetures sans prétendre les distinguer.
5. Disponibilité des extrêmes horodatée au niveau de la barre M1 :
   datation au début de barre, **disponibilité à la clôture de la
   barre**, aucun ordre intrabarre revendiqué.
6. Pas de mise à jour de 5 bp intégralement formalisé : bp relatif,
   ancrage E₀ au niveau franchi, seuils S_n = E₀(1 ± n·5/10⁴) sans
   arrondi, franchissements multiples dans une même barre comptés et
   déclarés d'ordre indéterminé.
7. Frontières journalière/hebdomadaire UTC et statuts d'incomplétude
   figés, en distinguant censure de l'extrême final et validité du
   niveau de référence.
8. Séparation première atteinte / touch / franchissement / extrême final
   renforcée ; **sortie dédiée aux événements à ordre indéterminé**.
9. Matérialité (5 points ou ratio 1,15) associée explicitement à chacune
   des dix comparaisons ; unités et grappes confirmées ligne à ligne ;
   **deux familles d'inférence distinctes, BY séparée, aucune conclusion
   globale sur les dix** ; négatives, insuffisantes et inéligibles
   conservées dans les rapports.

**STATUT : PROTOCOLE CONSOLIDÉ V2 — EN ATTENTE DE VALIDATION DÉFINITIVE.
AUCUN CALCUL N'A ÉTÉ LANCÉ.**
