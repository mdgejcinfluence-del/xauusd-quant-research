# PHASE 12.2 — AUDIT FINAL DES ÉQUATIONS, DE LA PUISSANCE ET DU PROTOCOLE DE VALIDATION

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**Statut : AUDIT MATHÉMATIQUE TERMINÉ — AUTORISATION DU PROPRIÉTAIRE EN ATTENTE.**
Mission strictement documentaire : zéro backtest, zéro `challenge_sim`, zéro essai,
zéro budget consommé, aucun holdout ouvert, aucune modification de code de stratégie.
Budgets vérifiés inchangés : tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 ·
NR 0/24 · P9 10/12. Le livrable audite le blueprint seq 144 tel que corrigé par la
validation seq 146 ; il ne le remplace pas.

---

## 1. Q_min — vérification algébrique complète

### 1.1 Définition de C, sans ambiguïté et sans double comptage

Prix d'exécution (long) : entrée à l'**Ask**, sortie au **Bid** (court : symétrique).
Les distances sont définies sur les prix effectivement payés/reçus :

- `Distance_SL_bp = 10 000 × (Ask_entrée − Bid_stop) / Ask_entrée` — la perte brute si
  le stop est touché, **déjà nette du spread de sortie** puisque le prix de stop est un
  Bid coté.
- `Distance_TP_bp = 10 000 × (Bid_cible − Ask_entrée) / Ask_entrée` — le gain brut si la
  cible est touchée, déjà net du spread de sortie.

Le spread est donc **dans** les distances, des deux côtés : à l'entrée (on paie
l'Ask, au-dessus du Mid) et à la sortie (on reçoit le Bid, au-dessous du Mid). Le
terme C de la relation de Phase 12.1 ne doit contenir que ce qui n'est **pas** déjà
dans ces prix :

**`C := commissions_RT + slippage_RT + autres_frais_RT`** (en bp), où :
- commissions_RT = commission d'entrée + commission de sortie (config V2 : 0,5 bp/côté,
  soit 1,0 bp RT, convention par côté déclarée non publiée par le courtier — rappel) ;
- slippage_RT = dégradation d'exécution à l'entrée + à la sortie, **au-delà** des
  cotations Bid/Ask utilisées (glissement du prix obtenu vs prix coté à la décision) ;
  inconnu mesuré, borné par les scénarios de stress seq 146 (0,3/0,6/1,5 bp par côté) ;
- autres_frais_RT = swap/financement si détention overnight, frais de plateforme
  éventuels : **UNKNOWN** à ce jour (swap déjà déclaré UNKNOWN seq 108) — toute
  détention franchissant un rollover ajoute un terme non chiffré, déclaré.

**Correction formelle à seq 146** : la validation écrivait `C = spread + commissions
+ slippage` dans `TP ≥ 2·SL + 3C` tout en définissant les distances sur Mid dans le
blueprint d'origine — les deux conventions mélangées comptaient le spread deux fois.
La convention **unique** retenue désormais : distances sur prix exécutables (ci-dessus),
et C sans spread. La relation devient, pour un long :

gain net = `Distance_TP − C` ; perte nette = `Distance_SL + C` ; ratio net ≥ 2 ⟺

**`Distance_TP ≥ 2 × Distance_SL + 3C`, avec C = commissions + slippage + autres frais (sans spread).**

### 1.2 D'où vient « 11 », et pourquoi il n'est pas universel

Phase 12.1 posait `Q_t = E|Δ_h| / C_total` (avec spread) et dérivait
`Q_required = 2·SL/C + 3` en évaluant SL = 20 bp, C = 4,7 bp (C1_BG) → ≈ 11,5 → 11.
L'audit établit trois choses :

1. **La formule est une identité géométrique, pas une loi** : `Q_required(t) =
   2·Distance_SL(t)/C(t) + 3` dépend des deux arguments au moment t. Tout seuil
   universel écrase cette dépendance ; il n'est défendable que comme **minorant
   calculé sur la géométrie la plus défavorable admise**, déclaré comme tel.
2. **La convention de C change la valeur** : avec C corrigé (§1.1, sans spread), pour
   la même géométrie SL = 20 bp et le scénario central de seq 146 (commissions 1,0 +
   slippage 2×0,6 = 2,2 bp), Q_required = 2×20/2,2 + 3 ≈ **21,2** ; au scénario
   défavorable (1,0 + 2×1,5 = 4,0) : **13,0**. Le « 11 » de seq 146 correspondait à
   l'ancienne convention (C incluant le spread à l'ancre C1_BG) : il est **retiré**
   comme seuil universel.
3. **SL diffère par scénario** (buffers et structures différents), donc les deux
   démonstrations séparées exigées :

| Scénario | SL de référence (géométrie déclarée) | Q_required, scénario central (C = 2,2) | Q_required, défavorable (C = 4,0) |
|---|---|---|---|
| S12-01 sweep | Stop au-delà de l'extrême du balayage + buffer {2,5,10} ; SL typique **non mesuré** (distribution des balayages jamais extraite) — référence de conception 25 bp (paramètre proposé) | 2×25/2,2 + 3 ≈ **25,7** | ≈ **15,5** |
| S12-02 retest | Stop derrière l'extrême du retest + buffer {2,5,10} ; référence de conception 20 bp (paramètre proposé) | ≈ **21,2** | ≈ **13,0** |

**Règle finale proposée (paramètre de conception, à geler au préreg)** : pas de seuil
Q universel. À chaque décision, `Q_t = E|Δ_h|(t) / C_scénario` et l'entrée exige
`Q_t ≥ Q_required(t) = 2·Distance_SL(t)/C_scénario + 3`, évalué au scénario de coût
**central** pour l'admission et revérifié au scénario **défavorable** pour la
certification. Le garde-fou « 11 » disparaît de l'architecture. (SL « typiques »
ci-dessus : valeurs de conception pour l'arithmétique, **non mesurées** — les
distributions réelles des distances de stop sont une sortie de l'extraction
descriptive future, pas une donnée actuelle.)

## 2. F3 — de la variance au mouvement : trois objets distincts

Chaîne de définition exacte (aucune étape implicite) :

1. **Variance prévisionnelle intégrée** : `V(t0, h) = RV_prévue_F3(jour) × Σ_{u∈[t0,t0+h]} w_u`
   (profil saisonnier horaire IS seq 146, Σ journalière = 1). Horizon de prévision :
   le F3 gelé prédit la RV du **lendemain** (origine journalière) ; l'usage intraday
   suppose la prévision du jour constante sur la fenêtre — hypothèse déclarée, le
   modèle ne produit pas de prévision horaire propre.
2. **Volatilité** : `σ(t0,h) = sqrt(V(t0,h))` — une **échelle** de dispersion, en bp
   après multiplication par 10 000. Ce n'est ni un mouvement attendu ni une probabilité.
3. **Métriques de mouvement** (à ne jamais confondre) :
   - mouvement absolu attendu sous convention gaussienne : `E|Δ| = σ·√(2/π) ≈ 0,798σ` ;
   - quantile de mouvement : `q_p(|Δ|) = σ × z_{(1+p)/2}` sous la même convention
     (p. ex. q_0,9 ≈ 1,645σ) ;
   - la distribution réelle des rendements d'or a des queues plus épaisses : tout
     quantile gaussien **sous-estime** les extrêmes (déclaré seq 146, confirmé ici).

`Q_t` utilise `E|Δ|` : c'est un ratio de **capacité moyenne**, pas une probabilité
d'atteinte de la cible. **Reconnaissance explicite exigée par l'ordre : les données
du programme ne permettent pas de calibrer une probabilité d'atteinte du TP** — une
telle probabilité exigerait la loi jointe (premier passage, dépendance au chemin,
volatilité stochastique intraday) qu'aucun artefact ne fournit ; F3 ne prédit ni la
direction, ni le chemin, ni un temps d'atteinte. Aucun niveau de confiance n'est donc
attaché à Q_t au-delà de la convention distributive déclarée.

## 3. F7 — calibration du filtre conditionnel

- **Déciles** : calculés sur la distribution des probabilités prédites par le modèle
  gelé, **sur l'IS uniquement**, par quantiles empiriques (définition à geler au
  préreg : déciles annuels roulants ou distribution IS complète — le choix change les
  seuils ; recommandé : distribution IS complète, stabilité ci-dessous).
- **Nature du décile 10** : c'est une **alerte de classement** (les 10 % d'heures les
  plus risquées selon le modèle), pas une probabilité calibrée de saut. L'AUC de 0,684
  mesure un pouvoir de classement ; aucune calibration (courbe de fiabilité,
  Platt/isotonic) n'a jamais été produite ni exigée par le gate F7. Le taux de base
  des sauts est 10,1 % et le lift au top 5 % est 2,85× (seq 77) : dans le décile
  supérieur, la fréquence réalisée des sauts est élevée mais la probabilité ponctuelle
  exacte par heure est **inconnue**. Toute phrase du type « probabilité de saut de
  x % » est interdite ; seul « heure classée dans le décile d'alerte » est licite.
- **Stabilité temporelle** : AUC forward annuel 0,684/0,696/0,687 (2017–2019, seq 83)
  — le *classement* est stable sur ces trois années ; la stabilité des **seuils de
  décile** (les valeurs de probabilité coupant le décile 10) n'a jamais été mesurée
  et dériverait avec le régime de volatilité : à documenter au préreg (dérive des
  seuils par année), sans recalibrer le modèle gelé.
- **Réduction de risque de 50 %** (branche du filtre conditionnel seq 146) : aucune
  dérivation ne la fonde ; c'est une règle candidate parmi {25 %, 50 %, 75 %}, et le
  programme n'a aucun moyen documentaire de la choisir. **Statut : paramètre proposé
  non calibré, non validé**, à figer au préreg comme *une* valeur de la grille
  déclarée ou comme constante de conception — jamais présenté comme optimal.

## 4. Indépendance des observations et puissance (36 cellules)

### 4.1 Ce qui comptera comme observation — définitions contraignantes

- **Opportunité brute** : chaque déclenchement des conditions d'une cellule.
- **Événement distinct** : un déclenchement rattaché à un niveau et une session donnés ;
  plusieurs cellules déclenchées par le même balayage/la même cassure (buffers
  différents, directions opposées exclues par construction) forment **un seul
  événement grappé**. Ne jamais compter les variantes d'un même événement comme des
  observations indépendantes : dans le test, les variantes d'une grappe partagent le
  même devenir de prix.
- **Journée indépendante** : les trades d'une même journée partagent le régime
  (F3 du jour, calendrier news) : l'unité d'indépendance conservative est le
  **jour × niveau**. `n_eff` sera estimé par grappes (jours distincts porteurs) et,
  pour le gate, `n_eff = nombre de grappes jour×niveau` — jamais le nombre brut.
- **Dépendances entre signaux simultanés** : cellules d'un même scénario (même
  événement, paramètres voisins) fortement dépendantes ; S12-01 vs S12-02 sur le même
  niveau mutuellement exclusifs par définition (réintégration vs retest réussi) mais
  pas indépendants (même niveau, même journée) ; dépendance inter-jours faible hors
  régime F3 persistant (autocorrélation de la vol prédite documentée seq 116 M3).

### 4.2 N ≥ 200 : par cellule — tranché

Le gate du programme (« n ≥ 200 ») s'applique **par cellule testée** (chaque cellule
est une hypothèse de la famille BY(36)) : une cellule sans 200 **grappes**
indépendantes au n prévu est NON TESTABLE à 0 essai (précédents F13 : n_eff < 200,
seq 94–97). La famille ne peut pas « prêter » ses observations à une cellule pauvre.
Comptes bruts/distincts/jours/n_eff par cellule : **non produits dans le présent
audit** — les produire exige l'extraction descriptive des déclencheurs sur l'IS
(étape de préreg, hors mandat documentaire) ; toute valeur avancée ici serait
fabriquée. Le protocole futur devra livrer, avant tout test, le tableau par cellule :
opportunités brutes / événements distincts / journées / n_eff estimé / MDE au n_eff.

### 4.3 MDE et puissance prévus (méthode, chiffres au préreg)

`MDE_80% = (z_{1−α_BY} + z_{0,80}) × σ_trade / √n_eff`, avec α_BY = seuil par test
après correction (§5) et σ_trade = écart-type des PnL nets par trade au scénario
central — inconnu avant extraction (les σ de géométrie F15, 19,4 bp à 60 min, sont
des ordres de grandeur voisins, pas des substituts). Puissance annoncée sans σ ni n
serait fictive : le gate R3 comparera, cellule par cellule, MDE à l'effet minimal
économique `2R net à l'ancre haute` dérivé en §1 ; MDE > effet ⟹ NON TESTABLE, 0 essai.

## 5. BY(36), FDR/FWER, et confirmation sans ouvrir le holdout scellé

### 5.1 Ce que chaque discipline contrôle

- **BY(36)** (Benjamini-Yekutieli) : contrôle le **FDR** — l'espérance de la
  proportion de fausses découvertes parmi les cellules rejetées — sous dépendance
  arbitraire. Procédure : p_i triées, rejet des p_(k) ≤ (k/36)·(q / H_36),
  H_36 = Σ 1/i ≈ 4,25, au niveau q fixé au préreg (doctrine programme : q = 0,05).
- **FWER** (probabilité d'au moins un faux positif) : **non** contrôlé par BY ; le
  contrôler exigerait Bonferroni (α/36 ≈ 0,0014 par test à α = 5 %). Le programme a
  choisi le FDR (doctrine historique « BY jamais BH ») : conséquence assumée et écrite —
  avec plusieurs rejets, une fraction attendue q d'entre eux peut être fausse ; c'est
  la confirmation (§5.2), pas la correction, qui tranche les survivants.
- **Confirmation indépendante** : ni FDR ni FWER — une évaluation sur des données non
  utilisées pour la sélection, qui seule transforme un rejet statistique en candidat.

### 5.2 Règles anti-sélection rétroactive

1. Les 36 cellules, leurs paramètres et l'ordre des gates sont **préenregistrés et
   chaînés avant tout calcul** ; aucune cellule supplémentaire après préreg (ordre
   12.1 §7) ; les fusions sont documentées avant lecture des résultats, jamais après.
2. Le scénario « retenu » est celui qui passe **tous** les gates, pas le meilleur
   PnL ; rapporter les 36 résultats, y compris négatifs, dans un tableau unique.
3. Interdiction de re-paramétrer après lecture : toute modification = nouvelle
   hypothèse, nouveau budget, nouvel ordre (règle permanente).

### 5.3 Confirmation hors échantillon **sans ouvrir le holdout scellé**

Mécanisme proposé : **walk-forward chronologique à origine roulante à l'intérieur de
l'IS de développement** (blocs annuels successifs, entraînement < évaluation, dans
l'esprit de la validation F3/F7 L2, seq 82–83), complété par une **réserve temporelle
interne** : la dernière année de l'IS est exclue du développement par le préreg et ne
sert qu'une fois, à la confirmation des cellules survivantes. Le holdout scellé
(ancien et NR) n'est ni ouvert ni approché ; son usage éventuel reste à usage unique
et à autorisation distincte (blueprint §G). Limite écrite : une réserve interne à
l'IS confirme la stabilité temporelle, pas la nouveauté de régime — elle ne vaut pas
le holdout, et ne doit pas être présentée comme telle.

## 6. Exécution et dimensionnement — modèle abstrait maintenu

Spec MT5 toujours absente (seq 55) : le sizing reste **abstrait** —
`Taille = (Equity × r) / (Distance_SL_bp × V_bp + Coûts_lot)`, où `V_bp` (valeur
monétaire d'1 bp par lot) et les coûts par lot sont des **symboles**, pas des nombres.
Aucune taille de lot chiffrée n'est présentée comme exacte sans contrat, valeur du
tick, pas de volume et règles de plateforme connus ; la convention générique de
seq 146 (100 oz) reste étiquetée « hypothèse générique ». Limites internes **3 %/jour
et 7 % de drawdown : paramètres de protection proposés, non des garanties** — un
dépassement reste possible par gap/pointe (minute 0 news > 20 bp, seq 142), slippage
inconnu et latence ; elles réduisent l'exposition, elles ne bornent pas le réel.

## 7. Sécurité FRED — état et conditions de réactivation

Le workflow `exogenous_pack_v2.yml` **reste suspendu** (seq 145 : déclencheur retiré,
job `if: ${{ false }}`). Réactivation subordonnée aux quatre conditions cumulatives
de l'ordre, toutes côté propriétaire ou à documenter avant réactivation :
1. confirmation de rotation de l'ancienne clé ;
2. vérification de l'injection du nouveau secret (sans jamais l'afficher) ;
3. contrôle des expositions restantes (arbre HEAD propre vérifié seq 140 ; historique
   contenant encore la valeur dans `cfd3df5/833f13b/b144080`) ;
4. **plan de purge de l'historique Git documenté avant exécution** : réécriture
   (filter-repo) des commits porteurs, table de mapping ancien SHA → nouveau SHA pour
   les 144+ checkpoints chaînés, re-vérification de la chaîne d'audit après purge, et
   consignation du mapping dans une nouvelle entrée seq. Aucune de ces étapes n'est
   entreprise par le présent audit ; la clé n'a été ni touchée ni réutilisée.

## 8. Conclusion de l'audit

Trois corrections subsistent après audit et devront être actées avant tout
préreg : (i) C est redéfini sans le spread (double comptage supprimé) et **le seuil
Q universel de 11 est retiré** au profit de `Q_required(t)` par scénario (§1) ;
(ii) Q_t est un ratio de capacité moyenne sans probabilité d'atteinte calibrable
(§2) ; (iii) le n ≥ 200 s'entend en **grappes indépendantes par cellule**, comptes à
produire au préreg (§4). Le reste de l'architecture seq 144/146 est algébriquement
cohérent une fois ces corrections appliquées. Aucune autorisation n'est demandée ni
accordée par ce document.

**STATUT : AUDIT MATHÉMATIQUE TERMINÉ — AUTORISATION DU PROPRIÉTAIRE EN ATTENTE.**
