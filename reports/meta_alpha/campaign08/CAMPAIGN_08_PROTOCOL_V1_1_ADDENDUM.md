# CAMPAGNE 8 — ADDENDUM V1.1 AU PROTOCOLE F-J : QUATRE FORMALISATIONS

**Statut : ADDENDUM SOUMIS — complète le protocole consolidé V1
(seq260, sha256 `022ca0dc…9af`, inchangé) selon la décision du
fondateur. NON GELÉ, AUCUN CALCUL.** Les définitions préservées sont
rappelées sans modification : détection causale Q₉₉,₅ sur 20 journées
précédentes, plancher 10 bp, prédicat strict, amorçage 10 journées /
10 000 variations, regroupement ≤ 15 minutes, clôture après
15 minutes sans choc, mixtes publiés séparément et exclus des
primaires, sillage +60 rétrospectif, matérialité 10 bp, BY à m = 5.

## 1. Continuation signée à +60 minutes (formule unique)

Pour un épisode non MIXTE de signe s ∈ {+1, −1} :

- **t_der** = horodatage de début de la **dernière barre de choc** de
  l'épisode ; son cours de clôture c(t_der) est disponible à
  **t_der + 1 minute** (fin de cette barre) : c'est le **prix
  d'ancrage c₀ = c(t_der)**.
- **Prix final** : c(t_der + 60) = clôture de la barre **débutant** à
  t_der + 60 minutes, disponible à **t_der + 61 minutes**.
- **Formule unique** :

  **R₆₀ = s × ln( c(t_der + 60) / c(t_der) ) × 10⁴ (bp).**

  R₆₀ > 0 : continuation dans le sens de l'épisode ; R₆₀ < 0 : retour
  contre le sens de l'épisode. Même formule, même ancrage et même
  orientation pour les pseudo-événements (s = signe de leur variation
  propre) et pour tous les bras de FJ-01…FJ-05.
- **Bornes et censure** : R₆₀ n'est défini que si la barre débutant à
  t_der + 60 existe **et** si l'intervalle (t_der, t_der + 60] ne
  contient aucun trou de cotation supérieur à 15 minutes ; sinon
  **CENSURE_FENÊTRE** pour cet épisode, taux publié par bras. Les
  horizons +15 et +30 suivent la même règle (barres t_der + 15,
  t_der + 30) à titre descriptif.
- **Disponibilité de l'épisode et du sillage** : l'épisode est
  définitivement identifiable à l'instant exact
  **t_der + 1 + 15 = t_der + 16 minutes** (clôture de la dernière barre
  de choc, puis 15 minutes sans nouveau choc) ; cet horodatage de
  disponibilité est publié pour chaque épisode. R₆₀ n'est connu qu'à
  t_der + 61 minutes. Aucune de ces grandeurs n'est présentée comme
  disponible pendant l'événement.

## 2. Intensité : mesure primaire unique pour FJ-03

**Mesure primaire d'intensité de l'épisode** :

**I_ép = max sur les chocs t de l'épisode de ( |r_t| / T_{D(t)} ),**

où T_{D(t)} est le seuil causal du jour propre à chaque choc — un
épisode traversant minuit rapporte donc chaque choc au seuil du jour
où il survient. Classes FJ-03 : **MODÉRÉ** si 1 < I_ép < 2,
**MAJEUR** si I_ép ≥ 2. Toute autre grandeur d'intensité — amplitude
maximale en bp A = max |r_t|, somme des |r_t| de l'épisode, nombre de
chocs, durée — est **descriptive seulement**, publiée mais jamais
testée ni substituée à I_ép.

## 3. Pseudo-événements : algorithme fermé

- **Activité antérieure (variable unique)** :
  **A_avant(x) = Σ_{k=1..60} |r_{x−k}|** (bp cumulés), somme des
  variations absolues des **60 minutes précédant** la minute x — la
  minute x elle-même exclue. Elle exige 60 barres consécutives
  segment-complètes avant x ; sinon x est inéligible (bassin comme
  épisode, dont le premier choc joue le rôle de x).
- **Sélection** : pour chaque journée éligible à la détection et chaque
  session S1–S4, la **première minute m** de la session telle que :
  r_m défini et ≠ 0 ; m n'est pas un choc ; **aucun choc dans les
  60 minutes précédant m** ; A_avant(m) calculable. Au plus un
  pseudo-événement par (journée, session). Signe du pseudo-événement :
  signe de r_m.
- **Terciles d'activité** : terciles de A_avant calculés **au sein de
  chaque session**, sur l'ensemble du bassin des pseudo-événements et
  des épisodes isolés de cette session (quantiles descriptifs de
  stratification ; ils ne servent ni à détecter ni à tester).
- **Appariement sans remplacement** : les épisodes isolés non MIXTES
  sont traités par **ordre chronologique croissant de leur premier
  choc** ; chacun reçoit le pseudo-événement **encore inutilisé** de
  même session, même signe et même tercile d'A_avant dont
  l'horodatage (journée, minute) est **le plus petit** — règle de
  départage unique, sans aléa ni graine. Un pseudo-événement apparié
  est retiré du bassin. Épisode sans partenaire disponible : publié
  comme non apparié, jamais réaffecté.
- **Non-exclusion absolue** : un choc survenant dans les 60 minutes
  suivant un pseudo-événement ne l'exclut **jamais** ; il est publié
  via le drapeau NOUVEAU_CHOC du pseudo-événement, comme comportement
  observé après un instant non extrême.
- **Contrôle de composition** : pour les paires appariées, publication
  fermée des effectifs croisés **ère (2010–13 / 2014–16 / 2017–20) ×
  session (S1–S4)** pour les épisodes et leurs pseudo-événements ; si
  une ère représente moins de 10 % des paires ou si l'écart de part
  d'une ère entre les deux bras dépasse 10 points, FJ-05 est publiée
  avec le drapeau **COMPOSITION_SENSIBLE** et ne peut produire de
  lecture CANDIDATE_J1. Si les seuils d'éligibilité (§7 du protocole)
  ne sont pas atteints, FJ-05 est **NON_EVALUABLE**.

## 4. Dépendance statistique et unité de bootstrap

- Deux épisodes sont **dépendants par construction** si leurs fenêtres
  de sillage [t_der, t_der + 60] se chevauchent, si le sillage de l'un
  contient un choc de l'autre, ou s'ils partagent le même jour
  d'attribution (contexte journalier commun).
- **Grappe statistique** : composante connexe du graphe de dépendance
  ci-dessus (fermeture transitive). Elle coïncide le plus souvent avec
  les épisodes d'une même journée, mais elle **fusionne
  automatiquement les journées successives** lorsqu'un sillage
  traversant minuit rencontre l'épisode du lendemain : aucune
  dépendance inter-journalière n'est coupée par la frontière UTC.
- **Bootstrap par ces grappes** (2 000 réplicats, protocole §7) : les
  épisodes appariés de FJ-05 voyagent avec la grappe de leur épisode.
  Justification : la dépendance entre sillages naît du futur observé
  partagé et du contexte de journée commun ; la composante connexe
  est la plus petite unité qui les contient toutes.
- **Diagnostics de validité publiés** avant toute lecture : nombre de
  grappes, distribution de leur taille (épisodes par grappe),
  proportion de sillages chevauchants, proportion de sillages
  traversant minuit, taille de la plus grande grappe et nombre
  d'épisodes qu'elle contient, nombre de fusions inter-journalières.
  Si la plus grande grappe contient plus de 5 % des épisodes d'un
  bras, la comparaison concernée est publiée avec le drapeau
  **GRAPPE_DOMINANTE** et sa lecture est plafonnée à
  SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL (aucune CANDIDATE_J1).

## 5. Portée

Le présent addendum ne modifie ni les cinq comparaisons fermées
FJ-01…FJ-05, ni les dix constantes justifiées au §12 du protocole V1,
ni la matrice de couverture, le registre des biais D1–D12, le coût
(un run CI attendu) et les règles de suspension. Ensemble V1 + V1.1 =
protocole scientifique unique soumis à validation définitive et gel.
