# CAMPAGNE 6 — PROTOCOLE CONSOLIDÉ F-G « FORME DES TRAJECTOIRES JOURNALIÈRES » (V1)

**Statut : CONSOLIDATION AUTORISÉE (seq228) — SOUMIS À VALIDATION
DÉFINITIVE AVANT GEL. AUCUN CALCUL F-G EFFECTUÉ, AUCUNE EXTRACTION,
EXÉCUTION INTERDITE.** Ce document unique consolide le blueprint
(`67da7bc3…`), le dictionnaire (`156cf85a…`), les comparaisons
(`8744a1f2…`) et la méthode (`72a373aa…`) de la préparation seq227,
intègre les décisions du fondateur sur les constantes, et tranche les
points restés ouverts. En cas de tension avec les documents de
préparation, le présent protocole prévaut.

## 1. Objectif et doctrine

Décrire si la géométrie des trajectoires intrajournalières du XAU/USD
constitue une dimension comportementale distincte (formes
directionnelles, oscillantes, mixtes ou autres). Recherche descriptive
et exploratoire uniquement : aucune démonstration de rentabilité,
aucune stratégie, aucun déclencheur, aucune réutilisation des
candidates C5. Candidates éventuelles : catalogue J1, sans promotion
automatique. Résultats négatifs et indicateurs non exploitables publiés.

## 2. Conventions (journées, horaires, fréquence)

- Journée = journée civile **UTC** 00:00–23:59. Barres M1 horodatées par
  leur début, disponibles à leur clôture (début + 1 min).
- Fréquence unique : **clôtures M1**, sur toute la campagne. Les mesures
  décrivent la trajectoire **des clôtures M1**, pas la totalité du
  parcours intraminute (les excursions entre clôtures ne sont visibles
  que via H/L de l'amplitude A, jamais dans le chemin L).
- p₀ = ouverture de la première barre observée du jour ; p_t = clôture
  de la t-ième barre observée ; H, L̄ = max des hauts / min des bas M1
  observés (L̄ noté ainsi pour ne pas confondre avec la longueur L).

## 3. Dictionnaire complet (formules, unités, cas limites)

Par journée, sur les **segments continus** de minutes observées (§4) :

- Déplacement net : Δ = p_n − p₀ ; Δ_bp = Δ / p₀ × 10⁴ (bp).
- Longueur de chemin : **L = Σ |p_t − p_{t−1}|** sommée **uniquement à
  l'intérieur des segments continus**. Le saut entre la dernière clôture
  avant un trou et la première clôture après un trou n'entre **jamais**
  dans L : deux clôtures séparées par un trou ne sont jamais reliées
  comme si elles étaient consécutives. Nombre de segments et minutes
  manquantes publiés par journée.
- Amplitude : A = H − L̄ ; A_bp = A / p₀ × 10⁴ (bp).
- **Efficience ER = |Δ| / L** ∈ [0, 1], sans unité, continue (discrétisée
  par le pas de cotation). L = 0 ⇒ ER **indéfinie** (0/0), jamais
  transformée en zéro ; journée classée PLATE, comptée et publiée.
  (Si L > 0, |Δ| ≤ L par construction sur segments — toute violation
  signale une incohérence de données et censure la journée.)
- **Sinuosité S = L / A**, sans unité, continue. A = 0 ⇒ S **indéfinie**,
  jamais zéro. (A = 0 avec L > 0 est une incohérence : censure publiée.)
- **Part directionnelle PD** = minutes intra-segment où
  signe(p_t − p_{t−1}) = signe(Δ), divisée par les minutes intra-segment
  où p_t ≠ p_{t−1} ; proportion continue dans [0, 1]. Indéfinie si
  Δ = 0 ou si aucune minute ne bouge.
- **Point médian de parcours τ** : premier instant t (début de barre,
  minutes depuis 00:00 UTC, **discret** à la minute) où la longueur
  cumulée intra-segment atteint ≥ L/2 ; indéfini si L = 0. L'égalité
  exacte à L/2 attribue τ à ce premier t.
- **Asymétrie AS = ER₁ − ER₂** (moitiés 00:00–11:59 / 12:00–23:59,
  chacune sur ses segments, son Δ et son L propres), continue dans
  [−1, 1] ; indéfinie si l'une des moitiés a L = 0.
- **Composantes conservées et publiées** par journée : p₀, p_n, Δ_bp,
  L (en bp de p₀), A_bp, |Δ|/A, ER, S, PD, τ, ER₁, ER₂, AS, n barres,
  n segments, minutes manquantes, trou maximal, statut de couverture.
  Toute dépendance entre indicateurs est publiée (§5), aucune n'est
  présentée comme une confirmation indépendante.

### Classes de forme (constantes validées par le fondateur)

- Δ_bp en valeur absolue **< 5 bp strictement** : **DÉPLACEMENT FAIBLE**,
  catégorie **prioritaire** sur les classes ER ; aucun signe imposé ;
  exclue des comparaisons par signe et de PD.
- Sinon : ER ≤ 0,10 **oscillante** ; 0,10 < ER < 0,30 **mixte** ;
  ER ≥ 0,30 **directionnelle**. (ER = 0,10 exactement : oscillante ;
  ER = 0,30 exactement : directionnelle.) Les classes sont secondaires ;
  les indicateurs continus restent primaires.

## 4. Couverture M1, trous, seuil de trou justifié

- Statuts de journée publiés comme en C5 (attendu/observé/taux, bornes
  première ≤00:10 / dernière ≥23:50, trou maximal) : COMPLETE
  (≥95 %, trou ≤30 min), PARTIELLE, EXCLUE. Aucun statut ne prouve une
  absence de mouvement ; aucune exigence 1 440/1 440 (leçon C5-10 : le
  marché a une halte quotidienne, l'attendu est celui du corpus, pas
  1 440 minutes actives).
- **Seuil de trou maximal pour l'éligibilité de forme : 15 minutes.**
  Justification (sans aucun calcul F-G) : (i) c'est le seuil déjà gelé
  en C5/V2.2 pour qu'une fenêtre de 60 minutes reste PARTIELLE plutôt
  que CENSUREE — la plus longue interruption qu'une mesure de parcours
  d'une heure tolérait sans censure ; une mesure de parcours de journée
  entière ne peut pas être plus laxiste que la mesure d'une heure dont
  elle agrège les segments ; (ii) au-delà de 15 minutes sans cotation
  en session active, le parcours inobservé peut contenir plusieurs
  renversements : relier les clôtures gonflerait ER d'une quantité non
  bornée et non mesurable ; (iii) le seuil reste très inférieur à la
  halte quotidienne programmée (~1 h), qui se traite comme frontière
  de segment ordinaire et non comme trou de session. En conséquence :
  trou intra-journée **> 15 min ⇒ journée CENSUREE des grandeurs de
  forme** (effectifs publiés) ; trou ≤ 15 min ⇒ segments séparés,
  saut inter-segment exclu de L et de PD (§3), nombre de segments
  publié. La population principale exige en outre taux ≥ 90 % des
  minutes attendues du corpus (à publier par statut).

## 5. Relations mathématiques publiées (anti-redondance)

- L/|Δ| = 1/ER exactement : interdit comme indicateur séparé.
- ER = (|Δ|/A) / S : ER, S et |Δ|/A partagent leurs composantes — une
  seule variable primaire par comparaison, les autres en décomposition
  descriptive sans p ni q.
- PD est mécaniquement lié au signe et à la taille de Δ : jamais
  primaire dans une comparaison par signe (C6-04).
- Toutes les grandeurs de journée complète sont **rétrospectives,
  disponibles uniquement à la clôture** (23:59 UTC) ; τ dépend de L
  total, donc rétrospectif aussi. Aucune lecture « à T0 » le jour même.

## 6. Les cinq comparaisons définitives (famille fermée F-G)

Matérialités : **0,05 d'ER** (5 points sur [0,1], échelle cohérente avec
les 5 points des campagnes 4–5 ; en dessous, « sous le seuil matériel »
même si significatif) ; **30 minutes pour τ** (§7). Inférence commune :
bootstrap percentile 95 %, 2 000 réplicats, graine publiée au gel ;
éligibilité ≥200 journées et ≥100 grappes par bras ; lectures fermées
CANDIDATE_J1 / SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL / NEGATIF /
NON_ELIGIBLE / STRUCTURELLEMENT_NON_EVALUABLE.

| ID | Hypothèse | Variable primaire | Population A vs B | Unité / grappe | Matérialité |
|---|---|---|---|---|---|
| C6-01 | La forme du jour dépend de celle du jour précédent | ER_j (diff. de médianes) | j−1 directionnel (ER ≥0,30) vs j−1 oscillant (ER ≤0,10), classes de j−1 hors DÉPLACEMENT FAIBLE | paire (j−1, j) ; **grappe = semaine civile de j** | 0,05 |
| C6-02 | La forme diffère selon l'amplitude du jour | ER (diff. de médianes) | tercile haut vs bas de A_bp, contemporains décennaux étiquetés rétrospectifs | journée / grappe-journée | 0,05 |
| C6-03 | La forme diffère selon le jour de semaine | ER (diff. de médianes) | lundis vs vendredis UTC | journée / grappe-journée | 0,05 |
| C6-04 | La localisation du parcours diffère selon le signe du déplacement | τ (diff. de médianes, minutes) | Δ_bp ≥ +5 vs Δ_bp ≤ −5 (DÉPLACEMENT FAIBLE exclu et compté ; Δ=0 publié) | journée / grappe-journée | 30 min |
| C6-05 | La forme a évolué entre ères | ER (diff. de médianes) | 2010–2013 vs 2017–2020 (2014–2016 publiée hors contraste) | journée / grappe-journée | 0,05 |

### C6-01 — construction exacte des paires (dépendance temporelle)

- Paire = (j−1, j) où j−1 est la **journée utilisable immédiatement
  précédente** de j dans le corpus (jours de cotation successifs). Les
  paires **vendredi → lundi** sont incluses au même titre (successivité
  de cotation), marquées VEN_LUN et leur effectif publié ; aucune paire
  ne saute une journée présente mais EXCLUE : si la journée intermédiaire
  est exclue, la paire n'est pas formée (pas de chaînage à travers une
  censure).
- Chaque journée peut être j dans une paire et j−1 dans la suivante :
  les paires se chevauchent par construction. Attribution : la paire
  appartient à la **semaine civile (lundi–dimanche UTC) de j**.
- Bootstrap : rééchantillonnage des **semaines entières** avec toutes
  leurs paires. Deux semaines adjacentes ne sont **pas** déclarées
  indépendantes : la dépendance résiduelle inter-semaines est traitée
  par un contrôle publié — IC recalculé par **blocs mobiles de deux
  semaines consécutives** (même effet, même nombre de réplicats) ; si
  les deux IC conduisent à des lectures différentes, la lecture la plus
  prudente (celle du bloc de deux semaines) prévaut et le désaccord est
  publié. Aucune p supplémentaire n'est créée par ce contrôle.

### C6-02 — contrôle de matérialité et déclassement (règle fermée)

- Variable primaire et **seul test inférentiel : ER**. **S ne produit
  aucune p-value ni q-value en C6-02** ; S, |Δ|/A, L et A_bp sont publiés
  par bras en décomposition descriptive (médianes, sans test).
- **Déclassement « forme → déplacement relatif »** : si le contraste ER
  est CANDIDATE_J1 ou SIGNIFICATIVE (q < 0,05 et |ΔER| ≥ 0,05) **et** que
  le ratio des médianes de |Δ|/A entre bras sort de [0,8696 ; 1,15] dans
  le même sens que ER **et** que le ratio des médianes de S reste dans
  [0,8696 ; 1,15], alors la lecture publiée est **DÉPLACEMENT RELATIF
  (déclassée — pas une forme pure)** et aucune fiche ANO « forme » n'est
  créée. Si S sort aussi de l'intervalle, la lecture « forme » est
  conservée avec la décomposition publiée. Bornes 1/1,15 = 0,8696,
  symétriques, héritées des campagnes précédentes.

## 7. Seuil de 30 minutes (point médian) — définition fermée

- **Fonction unique : seuil de matérialité** de C6-04. L'effet est la
  différence des médianes de τ entre bras, en minutes. Il est matériel
  si **|effet| ≥ 30** (30 exactement compte comme matériel) **et** la
  matérialité n'intervient qu'après le test (q BY < 0,05 pour
  CANDIDATE_J1, selon les lectures fermées communes).
- **Aucune catégorie, classe ou éligibilité ne dépend de ce seuil** :
  τ n'est jamais découpé en « tôt/tard » ; aucune journée n'est exclue
  au motif de son τ. Éligibilité de τ : L > 0 suffit (τ indéfini si
  L = 0, journée PLATE comptée). Pas de cas limite autre que l'égalité
  ci-dessus ; τ étant discret à la minute, une différence de médianes
  peut être fractionnaire (médiane interpolée) — la comparaison à 30 se
  fait sur la valeur publiée non arrondie.

## 8. Multiplicité (règle fermée, leçon seq223 intégrée)

- Famille préenregistrée **F-G de cinq** comparaisons (C6-01..C6-05),
  correction **Benjamini–Yekutieli avec m = 5 fixe et H₅ = 2,283333**,
  que toutes les hypothèses soient testables ou non.
- Formule explicite : p calculables triées p₍₁₎ ≤ … ≤ p₍ₖ₎ (k ≤ 5) ;
  q₍ᵣ₎ = min_{s ≥ r} (5 · H₅ · p₍ₛ₎ / s), plafonnée à 1. Le facteur de
  famille reste 5 même si k < 5 (borne conservative).
- Hypothèse structurellement impossible : p = NaN publié, **aucune
  valeur imputée**, q = NaN, statut **STRUCTURELLEMENT_NON_EVALUABLE**
  publié ; elle continue de compter dans le facteur m = 5.

## 9. Matrice de couverture par ère (déjà publiée, aucune nouvelle extraction)

Corpus constitué : 282 partitions, 3 540 993 barres M1, 3 097 journées
présentes, 2 572 utilisables (C4/C5). Journées à usage F-F OK publiées
en C5 : 2010–2013 : 1 034 ; 2014–2016 : 774 ; 2017–2020 : 763. La
population F-G appliquera ses propres censures (§4) après gel seulement ;
tout bras sous les seuils d'éligibilité sera déclaré NON_ELIGIBLE avec
effectifs. Holdout 2020–2026 scellé, hors matrice.

## 10. Registre des biais et limites

Reprise du registre B1–B11 de la préparation (effet de fréquence,
trous gonflant ER — traité par segments et censure > 15 min, halte
quotidienne, redondances algébriques, déplacement faible, persistance
de volatilité confondante en C6-01 — ventilation par amplitude de j
exigée en publication —, terciles rétrospectifs de C6-02, dérive de
microstructure en C6-05, ER bornée/bimodale traitée par médianes,
rétrospectivité des grandeurs, constantes de classes fixées a priori),
auquel s'ajoute : **B12** — chevauchement des paires de C6-01 et
dépendance inter-semaines (contrôle par blocs de deux semaines, §6) ;
**B13** — parcours intraminute invisible : ER/S décrivent les clôtures,
un aller-retour intraminute complet est invisible dans L (limite de
mesure publiée, A en garde-fou descriptif).

## 11. Coûts, suspension, restrictions

Un run CI d'extraction unique attendu (ordre de grandeur C4/C5),
synthèse locale ; coût financier 0 FCFA ; aucun budget expérimental
consommé. Échec ou incohérence ⇒ suspension du calcul concerné,
blocage documenté, comparaisons non exécutées conservées comme telles,
aucun remplacement méthodologique sans autorisation. XAU/USD
exclusivement ; holdout scellé ; aucun backtest ni `challenge_sim` ;
aucun J2/J3 ; FRED suspendue ; 36 cellules S12 gelées ; T0 séparé et
inactif ; fiches historiques non modifiées ; F-H/F-I en réserve.

## 12. Points soumis à validation définitive

Le fondateur est invité à valider : le seuil de trou de 15 minutes
(§4), la règle de segments (saut inter-trou exclu de L), la définition
fermée du seuil de 30 minutes (§7), la construction des paires et le
contrôle par blocs de deux semaines (C6-01), la règle de déclassement
(C6-02), la multiplicité à m = 5 fixe (§8), et les lectures fermées.
Après validation : gel chaîné du présent protocole, puis — seulement
sur ordre d'exécution séparé — calcul descriptif.
