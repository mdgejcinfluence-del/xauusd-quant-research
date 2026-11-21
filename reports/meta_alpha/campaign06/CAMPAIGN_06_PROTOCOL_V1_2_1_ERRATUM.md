# CAMPAGNE 6 — ERRATUM V1.2.1 AU PROTOCOLE F-G (avant gel)

**Statut : ERRATUM INDÉPENDANT, relié à la V1.1 (`0fdb3920…`) et à
l'addendum V1.2 (`046df8d9…`) — GEL ET EXÉCUTION TOUJOURS INTERDITS,
AUCUN CALCUL, AUCUNE EXTRACTION, AUCUNE CONSULTATION DE RÉSULTATS.**
L'erratum corrige trois points, et trois seulement. En cas de tension,
il prévaut sur la V1.2, qui prévaut sur la V1.1.

## 1. Correction B15 — convention horaire unique (OPTION A figée)

**L'équivalence « 21:00–22:00 UTC = 17:00–18:00 New York, été comme
hiver » de la V1.2 est retirée : elle est fausse** (17:00–18:00 à
New York correspond à 21:00–22:00 UTC en EDT mais à 22:00–23:00 UTC en
EST). Aucune identification de halte du protocole ne repose sur une
conversion horaire de ce type.

**Convention retenue et figée — OPTION A : fenêtre UTC fixe 21:00–
22:00, toute l'année.** Cette fenêtre est une **frontière
conventionnelle de segmentation en UTC**, définie dans le seul référentiel
du protocole (journées civiles UTC). Elle ne prétend coïncider avec
aucune heure locale constante, ni à New York ni ailleurs, et aucune
propriété du marché ne lui est attribuée : elle sert uniquement, avec
les autres conditions de la V1.2 (durée 45–75 min, unicité, barres des
deux côtés, tolérance d'horodatage ±5 min sur le début du trou, jours
lundi–vendredi), à classer un trou en FRONTIÈRE_PROGRAMMÉE au sens de
la convention. L'option B (fenêtre locale 17:00–18:00 New York
convertie date par date selon le calendrier historique EDT/EST) n'est
pas retenue : elle introduirait une dépendance à un calendrier externe
et à l'heure locale d'une place qui n'est pas nécessairement celle du
fournisseur du corpus, sans bénéfice pour une mesure définie en UTC.

Tout le reste de la règle B15 de la V1.2 est inchangé : cas multiples,
absents ou ambigus ⇒ HALTE_INDÉTERMINÉE, aucune exemption, aucune
continuité reconstruite, aucune « panne » classée, effectifs publiés
par ère.

## 2. D et ρ — définition définitive et cas L + D = 0

- **D = Σ |g_i|** : somme des **valeurs absolues des discontinuités
  observées**, où chaque g_i est le saut entre la dernière clôture du
  segment i et la première clôture du segment i+1. Confirmé sans
  changement.
- **ρ = D / (L + D)**, part relative des discontinuités observées dans
  le parcours mesuré (interprétation corrigée de la V1.2, conservée).
- **Cas L + D = 0** : cela signifie L = 0 et D = 0 (toutes les clôtures
  observées sont identiques et il n'existe aucun saut). Alors **ρ est
  indéfinie** (0/0) : **aucune valeur artificielle — ni 0, ni 1, ni
  aucune autre — n'est attribuée**, et ρ est publiée NaN. La journée
  conserve le statut **PLATE OBSERVÉE** (§3 de la V1.1) : ER et S y sont
  également indéfinies ; elle est comptée et publiée, exclue de tout
  ratio.
- Le seuil **ρ > 0,5** est conservé uniquement comme critère de
  déclassement (statut DOMINÉE PAR LES DISCONTINUITÉS OBSERVÉES) sous
  son interprétation corrigée ; il ne s'applique qu'aux journées où ρ
  est définie (L + D > 0).

## 3. C6-01 — ordre de priorité des statuts (figé)

Les statuts du contrôle par blocs sont évalués dans l'ordre strict
ci-dessous. **Un seul statut est attribué par comparaison : le premier
dont les conditions sont satisfaites dans cet ordre.** Les
chevauchements sont ainsi tranchés à l'avance, sans discrétion :

1. **CONTRÔLE_INDÉTERMINÉ** — si l'une des conditions minimales du
   contrôle n'est pas satisfaite : moins de 30 blocs de deux semaines
   disponibles, **ou** plus de 5 % de réplicats invalides, **ou**
   e = 0 exactement (pas de signe de référence). Ce statut prime sur
   tous les autres, y compris si l'intervalle contient aussi zéro ou
   inverse le signe : sans contrôle valide, aucune fragilité n'est
   diagnostiquée, et aucune lecture positive n'est retenue (règle de
   déclassement n° 3 de la V1.2).
2. **FRAGILE_SIGNE** — sinon, si l'IC par blocs contient 0 (bornes
   fermées : une borne à exactement 0 compte comme contenant) **ou**
   est entièrement du signe opposé à e (inversion, drapeau
   INVERSION_CONTRÔLE publié). Ce statut prime sur
   FRAGILE_MATÉRIALITÉ : un intervalle contenant 0 contient
   mécaniquement aussi des valeurs sous le seuil matériel, mais il est
   classé une seule fois, comme FRAGILE_SIGNE (déclassement en
   NEGATIF selon la règle n° 1 de la V1.2).
3. **FRAGILE_MATÉRIALITÉ** — sinon (IC excluant 0 et du signe de e), si
   la lecture hebdomadaire est CANDIDATE_J1 **et** que l'IC contient
   des valeurs sous le seuil matériel (borne la plus proche de 0 à
   |·| < 0,05 ; une borne à exactement 0,05 est au seuil inclus, donc
   pas fragile). Ne s'applique qu'à une lecture CANDIDATE_J1 : pour
   toute autre lecture hebdomadaire, cette condition est sans objet et
   l'évaluation passe au statut suivant. Déclassement d'un cran selon
   la règle n° 2 de la V1.2.
4. **ROBUSTE** — dans tous les autres cas satisfaisant les conditions
   de validation : contrôle valide, IC excluant 0, du signe de e, et
   (pour une lecture CANDIDATE_J1) entièrement au-delà du seuil matériel.

Aucune p-value ni q-value supplémentaire n'est créée par le contrôle ;
e, q BY et la matérialité ponctuelle restent ceux du bootstrap
hebdomadaire. Aucune règle de décision ne sera choisie après
consultation des résultats.

## Résumé des changements V1.2 → V1.2.1

| # | Changement | Nature |
|---|---|---|
| 1 | B15 : équivalence New York retirée ; **OPTION A figée** — fenêtre UTC fixe 21:00–22:00 toute l'année, frontière conventionnelle de segmentation UTC sans équivalence locale | correction horaire, autres conditions B15 inchangées |
| 2 | D confirmée (somme des valeurs absolues des sauts observés) ; **L + D = 0 ⇒ ρ indéfinie (NaN publié), statut PLATE OBSERVÉE conservé, aucune valeur artificielle** ; seuil ρ > 0,5 inchangé sous interprétation corrigée | cas limite fermé |
| 3 | C6-01 : **ordre de priorité strict** CONTRÔLE_INDÉTERMINÉ → FRAGILE_SIGNE → FRAGILE_MATÉRIALITÉ → ROBUSTE, un seul statut attribué, chevauchements tranchés à l'avance | règle de décision fermée |

Aucune formule de L, Δ_seg, A, ER, S, PD, τ, AS, aucune constante de
classe, aucun seuil de couverture, d'éligibilité, de matérialité ni
règle BY n'est modifié par le présent erratum.

## Soumission

Dossier final soumis au propriétaire pour validation du gel :
protocole V1.1 (`0fdb3920…`) + addendum V1.2 (`046df8d9…`) + présent
erratum V1.2.1. Après validation seulement : gel chaîné des trois
documents, puis ordre d'exécution séparé. Restrictions inchangées :
XAU/USD exclusivement, holdout scellé, aucun calcul ni extraction,
aucun backtest ni `challenge_sim`, aucun J2/J3 automatique, aucun
budget expérimental consommé, FRED suspendue, 36 cellules S12 gelées,
T0 séparé et inactif, aucune modification des fiches historiques,
F-H/F-I en réserve.
