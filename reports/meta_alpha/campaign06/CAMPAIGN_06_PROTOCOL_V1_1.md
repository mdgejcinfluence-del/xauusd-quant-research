# CAMPAGNE 6 — PROTOCOLE CONSOLIDÉ F-G « FORME DES TRAJECTOIRES JOURNALIÈRES » (V1.1)

**Statut : VERSION FINALE SOUMISE AU PROPRIÉTAIRE — GEL ET EXÉCUTION
INTERDITS, AUCUN CALCUL F-G EFFECTUÉ.** La V1.1 remplace la V1
(`241620ea…`) : elle intègre la clarification mathématique segments/Δ/L,
le contrôle de couverture cumulée et la règle prudente figée de C6-01
demandés par le fondateur. En cas de tension entre documents, la V1.1
prévaut. Architecture et constantes déjà validées inchangées : classes
ER (≤0,10 oscillante ; 0,10–0,30 mixte ; ≥0,30 directionnelle),
DÉPLACEMENT FAIBLE (|Δ|<5 bp, prioritaire, aucun signe imposé), trou
maximal 15 minutes, ER seule variable inférentielle de C6-02, seuil de
30 minutes = matérialité de C6-04, BY à m = 5 fixe.

## 1. Objectif et doctrine

Décrire si la géométrie observable des trajectoires intrajournalières
du XAU/USD constitue une dimension comportementale distincte.
Descriptif uniquement : aucune rentabilité comparée, aucune stratégie,
aucun déclencheur, aucune réutilisation des candidates C5. Candidates
éventuelles au catalogue J1, sans promotion automatique ; négatifs et
non éligibles publiés.

## 2. Conventions

Journée civile **UTC** 00:00–23:59 ; barres M1 horodatées par leur
début, disponibles à leur clôture ; fréquence unique : **clôtures M1**.
Les mesures décrivent la trajectoire **des clôtures M1**, jamais le
parcours intraminute complet (biais B13 : un aller-retour intraminute
est invisible dans le chemin ; H/L̄ ne servent qu'à l'amplitude).
p₀ = ouverture de la première barre observée ; clôtures observées
p₁…p_n ; H = max des hauts M1, L̄ = min des bas M1.

## 3. Segments, formules définitives (clarification fondatrice)

La journée est découpée en **segments continus** : suites maximales de
barres séparées d'exactement 1 minute. Entre deux segments : un **trou**
(gap > 1 min). On note, pour le segment i : première clôture a_i,
dernière clôture b_i, et le **saut inter-segments**
g_i = a_{i+1} − b_i, mouvement **non observé**, jamais traité comme un
mouvement connu.

- **Chemin observé : L = Σ_i Σ_{t intra-segment} |p_t − p_{t−1}|**
  (somme uniquement intra-segment ; aucun saut g_i n'entre dans L).
- **Déplacement net observé (référence de campagne) :
  Δ_seg = Σ_i (b_i − a_i)** — somme des déplacements nets de segments,
  calculé sur **exactement la même population de minutes que L**.
- **Déplacement brut de journée : Δ_jour = p_n − p₀ = Δ_seg + Σ g_i**,
  publié comme composante, **jamais** associé à L dans un ratio.
- **Masse de discontinuité : D = Σ |g_i|** ; part de discontinuité
  ρ = D / (L + D) ∈ [0, 1].
- **Amplitude : A = H − L̄** sur l'ensemble des barres observées (tous
  segments ; A décrit l'étendue verticale observée, y compris aux
  bornes de segments).
- **Efficience : ER = |Δ_seg| / L**. **Condition ER ≤ 1 garantie** :
  par segment, |b_i − a_i| ≤ L_i (inégalité triangulaire sur les pas
  intra-segment) ; en sommant, |Δ_seg| ≤ Σ|b_i − a_i| ≤ Σ L_i = L.
  ER ∈ [0, 1] est donc une propriété démontrée de cette définition, et
  d'elle seule : tout ratio utilisant Δ_jour avec L serait dépourvu de
  cette garantie et est interdit.
- **Sinuosité : S = L / A** (chemin observé par unité d'étendue
  observée). Relation publiée : ER = (|Δ_seg|/A) / S — ER, S et
  |Δ_seg|/A partagent leurs composantes ; une seule variable primaire
  par comparaison.
- **Part directionnelle PD** : minutes intra-segment où
  signe(p_t − p_{t−1}) = signe(Δ_seg), sur minutes intra-segment où
  p_t ≠ p_{t−1}. Indéfinie si Δ_seg = 0 ou aucune minute ne bouge ;
  jamais primaire dans une comparaison par signe (lien mécanique).
- **Point médian τ** : premier t (début de barre, minutes depuis 00:00,
  discret) où le chemin cumulé intra-segment atteint ≥ L/2 ; égalité
  exacte attribuée à ce premier t ; indéfini si L = 0.
- **Asymétrie AS = ER₁ − ER₂** par moitiés (00:00–11:59 / 12:00–23:59),
  chacune avec ses propres segments, Δ_seg et L.
- Unités : Δ_seg, L, A convertis en bp de p₀ (×10⁴/p₀) pour la
  publication ; ER, S, PD, ρ sans unité, continus (discrétisés par le
  pas de cotation) ; τ en minutes, discret.
- Grandeurs de journée complète **rétrospectives, disponibles à la
  clôture** ; aucune lecture intraday.

### Statuts de journée liés aux discontinuités (remplacent « PLATE » de la V1)

- **PLATE OBSERVÉE** : L = 0 **et** D = 0 (toutes les clôtures observées
  identiques, aucun saut) ⇒ ER et S **indéfinies** (0/0), jamais zéro ;
  journée comptée et publiée, exclue des ratios.
- **INDÉTERMINÉE — DISCONTINUITÉS** : L = 0 et D > 0 (le prix a changé
  uniquement par sauts non observés) ⇒ ER indéfinie ; **jamais ER = 0
  artificiel** ; exclue des populations de forme, publiée séparément.
- **DOMINÉE PAR LES DISCONTINUITÉS** : L > 0 et ρ > 0,5 (la majorité du
  mouvement total est non observée) ⇒ ER calculable mais **exclue des
  populations primaires** de toutes les comparaisons, publiée à part.
- A = 0 avec (L > 0 ou D > 0) : incohérence de données ⇒ censure publiée.
- **Classes de forme** (sur les journées non exclues ci-dessus) :
  |Δ_seg| en bp < 5 strictement ⇒ **DÉPLACEMENT FAIBLE** (prioritaire,
  aucun signe, exclue des comparaisons par signe et de PD) ; sinon
  ER ≤ 0,10 oscillante, 0,10 < ER < 0,30 mixte, ER ≥ 0,30 directionnelle
  (bornes exactes incluses comme indiqué).

## 4. Couverture cumulée (contrôle complémentaire au trou maximal)

Publiés **par journée** : nombre de trous, durée cumulée des trous,
minutes attendues, minutes observées, taux de couverture. Définitions :
la **frontière de segment programmée** = le plus long trou de la journée
s'il est unique et ≥ 30 min (halte quotidienne du marché, dont
l'existence est établie par les diagnostics C5) ; les autres trous sont
des **trous de session**. Minutes attendues = minutes observées + durée
cumulée des trous de session à l'intérieur du span première–dernière
barre (la frontière programmée est exclue de l'attendu comme du
numérateur) ; taux = observées / attendues.

**Éligibilité de forme (primaire), les trois conditions réunies** :
(i) trou de session maximal ≤ **15 min** (justification V1 conservée :
seuil C5/V2.2 d'une fenêtre de 60 min partielle, parcours inobservé au-
delà) ; (ii) durée cumulée des trous de session ≤ **30 min** (au plus
deux interruptions maximales : le chemin inobservé reste marginal à
l'échelle d'une journée de cotation d'environ 23 h) ; (iii) taux de
couverture cumulée ≥ **95 %** (seuil du statut général COMPLETE des
campagnes C4/C5 : en dessous, plus d'un vingtième du parcours actif est
invisible, ce qu'une mesure de géométrie ne peut absorber alors qu'une
mesure d'amplitude le pouvait). Ces seuils sont justifiés par les
diagnostics et seuils déjà publiés des campagnes précédentes ; **aucun
calcul F-G n'a servi à les choisir**. Journées sous un seuil : CENSURÉES
des grandeurs de forme, effectifs publiés par statut et par ère.
Statuts généraux COMPLETE/PARTIELLE/EXCLUE (bornes 00:10/23:50, taux)
publiés en parallèle, jamais comme preuve d'absence.

## 5. Les cinq comparaisons définitives (famille fermée F-G)

Inférence commune : bootstrap percentile 95 %, 2 000 réplicats, graine
publiée au gel ; éligibilité ≥ 200 journées et ≥ 100 grappes par bras ;
matérialités 0,05 d'ER et 30 minutes (τ, §7) ; lectures fermées
CANDIDATE_J1 / SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL / NEGATIF /
NON_ELIGIBLE / STRUCTURELLEMENT_NON_EVALUABLE.

| ID | Hypothèse | Variable primaire | Population A vs B | Unité / grappe | Matérialité |
|---|---|---|---|---|---|
| C6-01 | La forme du jour dépend de celle du jour précédent | ER_j | j−1 directionnel vs j−1 oscillant (classes fermées §3) | paire (j−1,j), grappe = semaine civile de j | 0,05 |
| C6-02 | La forme diffère selon l'amplitude du jour | ER | tercile haut vs bas de A_bp, contemporains décennaux rétrospectifs | journée / grappe-journée | 0,05 |
| C6-03 | La forme diffère selon le jour de semaine | ER | lundis vs vendredis UTC | journée / grappe-journée | 0,05 |
| C6-04 | La localisation du parcours diffère selon le signe du déplacement | τ | Δ_seg ≥ +5 bp vs ≤ −5 bp (DÉPLACEMENT FAIBLE exclu, compté) | journée / grappe-journée | 30 min |
| C6-05 | La forme a évolué entre ères | ER | 2010–2013 vs 2017–2020 (2014–2016 publiée) | journée / grappe-journée | 0,05 |

### C6-01 — pairs et règle prudente figée

Paires : jours de cotation utilisables successifs, vendredi→lundi inclus
et marqué VEN_LUN ; **aucun chaînage à travers une journée censurée** ;
chaque journée peut figurer dans deux paires (chevauchement publié) ;
attribution à la semaine civile de j ; bootstrap par **semaines
entières**. Contrôle par **blocs mobiles de deux semaines consécutives**
(sans p-value additionnelle, sans comparaison supplémentaire).

**Règle de décision déterministe** (ordre de prudence :
CANDIDATE_J1 ≻ SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL ≻ NEGATIF) :
1. Lecture hebdomadaire L_sem obtenue par les règles communes (q BY sur
   la p du bootstrap hebdomadaire, effet ponctuel identique dans les
   deux méthodes).
2. Statut du contrôle : ROBUSTE si l'IC 95 % par blocs exclut 0 **et**
   garde le signe de l'effet ; FRAGILE sinon (IC incluant 0 ou signe
   ambigu).
3. Lecture finale = L_sem si ROBUSTE ; = **NEGATIF (non robuste au
   contrôle par blocs)** si FRAGILE et L_sem ∈ {CANDIDATE_J1,
   SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL} ; = L_sem si FRAGILE et L_sem
   déjà NEGATIF ou NON_ELIGIBLE. La matérialité (effet ponctuel,
   identique dans les deux méthodes) n'est jamais révisée par le
   contrôle ; seuls l'intervalle et donc la lecture peuvent être
   déclassés. Les deux IC sont toujours publiés.

### C6-02 — matérialité exacte et déclassement

ER unique variable inférentielle ; **S : aucune p-value, aucune q-value**
(décomposition descriptive par bras : médianes de S, |Δ_seg|/A, L, A_bp).
Borne symétrique exacte : ratio dans [1/1,15 ; 1,15] =
[0,8695652173913043 ; 1,15], soit en formulation logarithmique
|ln(ratio)| ≤ ln(1,15) = 0,13976194237515866 réputé « sans écart
matériel ». **Déclassement « forme → déplacement relatif »** : si le
contraste ER atteint q < 0,05 avec |ΔER| ≥ 0,05, **et** |ln(ratio des
médianes |Δ_seg|/A)| > ln(1,15) dans le même sens que ER, **et**
|ln(ratio des médianes S)| ≤ ln(1,15), alors lecture publiée
**DÉPLACEMENT RELATIF (déclassée)** et aucune fiche ANO « forme ». Si S
sort aussi de l'intervalle, lecture « forme » conservée, décomposition
publiée.

## 6. Point médian — seuil de 30 minutes (définition fermée, inchangée)

Fonction unique : matérialité de C6-04, |effet| ≥ 30 (égalité comptée),
appliquée après le test, sur la valeur non arrondie. Aucune catégorie
ni éligibilité n'en dépend ; τ jamais découpé en tôt/tard ; éligibilité
de τ : L > 0 (hors statuts d'exclusion §3).

## 7. Multiplicité (fermée)

Famille préenregistrée de **cinq** ; BY avec **m = 5 fixe, H₅ =
2,283333** : p calculables triées p₍₁₎≤…≤p₍ₖ₎ (k≤5),
q₍ᵣ₎ = min_{s≥r}(5·H₅·p₍ₛ₎/s), plafonnée à 1. Hypothèse structurellement
impossible : p = q = NaN publiés, aucune imputation, statut
STRUCTURELLEMENT_NON_EVALUABLE, et elle **continue de compter dans le
facteur m = 5**.

## 8. Couverture historique, biais, coûts, restrictions

Matrice (déjà publiée, aucune nouvelle extraction) : 282 partitions,
3 540 993 barres M1, 3 097 journées présentes, 2 572 utilisables ;
journées OK C5 par ère : 1 034 (2010–13), 774 (2014–16), 763 (2017–20) ;
la population F-G appliquera §§3–4 après gel seulement. Holdout scellé.
Biais B1–B13 de la préparation et de la V1, complétés par : **B14** —
sauts inter-segments exclus du chemin : ER mesure la géométrie
**observable**, et ρ publié par journée et par bras rend visible ce que
la mesure ne voit pas ; **B15** — frontière programmée définie par le
plus long trou unique ≥ 30 min : si un jour présente deux trous ≥ 30 min
ou aucun, aucun n'est exempté et les seuils s'appliquent à tous
(déterministe, effectifs publiés). Coût : un run CI unique attendu,
0 FCFA, aucun budget expérimental ; suspension documentée en cas
d'échec, aucune substitution méthodologique. XAU/USD exclusivement ;
aucun backtest ni `challenge_sim` ; aucun J2/J3 ; FRED suspendue ;
36 cellules S12 gelées ; T0 inactif ; fiches historiques inchangées ;
F-H/F-I en réserve.

## 9. Soumission

Le propriétaire est invité à valider la V1.1 comme protocole final.
Après validation seulement : gel chaîné (hash du présent document dans
le registre), puis ordre d'exécution séparé pour le calcul descriptif.
Aucune formule ne sera modifiée après le gel.
