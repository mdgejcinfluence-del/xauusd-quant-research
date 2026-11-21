# CAMPAGNE 6 — ADDENDUM V1.2 AU PROTOCOLE F-G (trois précisions, avant gel)

**Statut : ADDENDUM INDÉPENDANT — GEL ET EXÉCUTION TOUJOURS INTERDITS,
AUCUN CALCUL F-G, AUCUNE EXTRACTION, AUCUNE CONSULTATION DE
RÉSULTATS.** L'addendum ne contient que les trois précisions exigées
par le fondateur après validation scientifique conditionnelle de la
V1.1 (`0fdb3920…`). Il modifie la V1.1 aux seuls articles ci-dessous ;
tout le reste de la V1.1 demeure inchangé. En cas de tension,
l'addendum prévaut.

## Précision 1 — Indicateur ρ : interprétation corrigée

Définition inchangée : **ρ = D / (L + D)**, avec L = chemin observé
intra-segments et D = Σ |g_i| la somme des valeurs absolues des sauts
entre clôtures bordant les trous.

**Interprétation obligatoire (remplace toute formulation de la V1.1)** :
ρ est la **part relative des discontinuités observées dans le parcours
mesuré**. Elle ne mesure **pas** la proportion réelle du mouvement total
non observé, et ne doit jamais être présentée ainsi : le chemin
réellement parcouru pendant une interruption est inconnu, il est au
moins égal à la valeur absolue du saut (inégalité triangulaire) et peut
être arbitrairement plus long (allers-retours invisibles). ρ est donc
une grandeur de la **mesure**, pas du marché pendant les trous.

En conséquence, le statut de la V1.1 est renommé et redéfini :
**DOMINÉE PAR LES DISCONTINUITÉS OBSERVÉES** = ρ > 0,5, c'est-à-dire que
les sauts observés excèdent la moitié du parcours **mesuré** (L + D).
Le seuil 0,5 est conservé à l'identique comme critère de déclassement
(exclusion des populations primaires, publication séparée), sous cette
seule interprétation. Aucune phrase du protocole ou des rapports futurs
ne peut affirmer qu'une journée déclassée a « réellement » bougé
principalement pendant ses interruptions.

## Précision 2 — Règle B15 (halte quotidienne) publiée intégralement

**Principe.** Aucune halte programmée n'est identifiée à partir de la
seule durée d'un trou. La segmentation en segments continus (§3 de la
V1.1) ne dépend d'ailleurs pas de cette identification : les sauts sont
toujours exclus de L, halte ou panne. L'identification ne sert qu'à
l'exemption éventuelle du plus long trou dans les seuils de couverture
cumulée (§4 de la V1.1). En cas de doute, le statut indéterminé
s'applique et **aucun trou n'est exempté** : on ne reconstruit jamais
artificiellement une continuité.

**Horaires UTC attendus.** Le marché au comptant de l'or suit une halte
quotidienne calée sur 17:00–18:00, heure de New York, soit en UTC :
**21:00–22:00 UTC** pendant l'heure d'été américaine (EDT) et
**22:00–23:00 UTC** pendant l'heure standard (EST). Fenêtre de début
attendue, toutes saisons confondues : **21:00–22:00 UTC** (tolérance
d'horodatage de ±5 minutes sur le début et la fin du trou). Ces horaires
sont une convention de marché connue a priori, indépendante du corpus ;
ils ne proviennent d'aucun calcul F-G.

**Conditions de détection — un trou est classé FRONTIÈRE PROGRAMMÉE
si et seulement si les quatre conditions sont réunies** :
1. son début (première minute manquante) tombe dans la fenêtre
   21:00–22:00 UTC (±5 min), un jour de cotation lundi–vendredi ;
2. sa durée est de 45 à 75 minutes (halte nominale de 60 min ± 15) ;
3. il est **unique** dans la journée à satisfaire 1 et 2 ;
4. la journée présente des barres avant et après le trou.
Le classement est publié tel quel : FRONTIÈRE_PROGRAMMÉE (identifiée
selon la règle), sans prétendre prouver la cause de l'interruption.

**Cas multiples, absents ou ambigus — statut indéterminé** :
- zéro trou satisfaisant les conditions (la halte peut être absente,
  masquée par des cotations éparses, ou décalée) ;
- deux trous ou plus satisfaisant les conditions ;
- trou dans la fenêtre horaire mais de durée hors 45–75 min ;
- trou de 45–75 min hors fenêtre horaire (candidat panne, fermeture
  exceptionnelle ou halte décalée — causes **non distinguables** dans
  les données M1).
Dans tous ces cas : statut **HALTE_INDÉTERMINÉE** publié, **aucune
exemption** : tous les trous sont traités comme trous de session pour
les seuils du §4 (trou maximal 15 min, cumul 30 min, taux 95 %) — avec
la conséquence assumée qu'une journée dont la halte n'est pas
identifiée selon la règle sera le plus souvent CENSURÉE des grandeurs
de forme. Cette sévérité est le prix pré-déclaré de l'incertitude ;
elle ne sera ni assouplie ni contournée après le gel.

**Distinction halte / panne.** Les données M1 ne permettent pas de
prouver la cause d'une interruption. Le protocole ne classe donc jamais
une « panne » : hors conditions ci-dessus, tout trou est un **trou de
session de cause indéterminée**. Les effectifs par classement
(FRONTIÈRE_PROGRAMMÉE / HALTE_INDÉTERMINÉE / aucun trou > 1 min) seront
publiés par ère dans les diagnostics de couverture.

## Précision 3 — C6-01 : critères ROBUSTE / FRAGILE figés à l'avance

Rappels : l'effet ponctuel e (différence de médianes d'ER entre bras),
la p-value (bootstrap hebdomadaire) et la q BY sont identiques dans la
méthode principale et dans le contrôle ; le contrôle par blocs mobiles
de deux semaines consécutives ne produit **que** un intervalle IC_b,
**aucune p-value ni q-value supplémentaire**, et ne peut modifier ni e
ni la matérialité ponctuelle. Le nombre de blocs de deux semaines et le
taux de réplicats valides (2 000 prévus) seront publiés.

**Définitions déterministes** (les bornes fermées comptent comme
« contenant » : un IC dont une borne vaut exactement 0 contient 0 ; une
borne dont la valeur absolue vaut exactement 0,05 est au seuil
matériel inclus) :

- **ROBUSTE** : IC_b exclut strictement 0, est entièrement du signe
  de e, et — si la lecture hebdomadaire est CANDIDATE_J1 — IC_b est
  entièrement au-delà du seuil matériel dans le sens de e
  (borne la plus proche de 0 à |·| ≥ 0,05).
- **FRAGILE_SIGNE** : IC_b contient 0, **ou** IC_b est entièrement du
  signe opposé à e (**inversion de signe** du contrôle, publiée avec le
  drapeau INVERSION_CONTRÔLE).
- **FRAGILE_MATÉRIALITÉ** : IC_b exclut 0 et garde le signe de e, mais
  contient des valeurs sous le seuil matériel (|·| < 0,05) alors que la
  lecture hebdomadaire est CANDIDATE_J1. (La « perte de matérialité »
  ne peut porter que sur l'intervalle : la matérialité ponctuelle,
  définie sur e, est par construction identique dans les deux
  méthodes et n'est jamais révisée.)
- **CONTRÔLE_INDÉTERMINÉ** : moins de 30 blocs de deux semaines
  disponibles, ou plus de 5 % de réplicats du contrôle invalides, ou
  e = 0 exactement (aucun signe de référence).

**Règle de lecture finale (ordre de prudence figé)** :
1. FRAGILE_SIGNE ⇒ toute lecture CANDIDATE_J1 ou
   SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL est déclassée en
   **NEGATIF (non robuste au contrôle par blocs)**.
2. FRAGILE_MATÉRIALITÉ ⇒ CANDIDATE_J1 est déclassée d'un cran en
   **SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL (robustesse de matérialité
   non établie au contrôle par blocs)**.
3. CONTRÔLE_INDÉTERMINÉ ⇒ aucune lecture positive n'est retenue :
   CANDIDATE_J1 ou SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL deviennent
   **NON_ELIGIBLE (contrôle indéterminé)**.
4. ROBUSTE, ou contrôle fragile sans lecture positive à déclasser ⇒
   lecture hebdomadaire inchangée.
Les deux intervalles (hebdomadaire et blocs), le statut du contrôle et
tout déclassement seront publiés ligne à ligne. Aucune règle de
décision ne sera choisie ou ajustée après consultation des résultats —
c'est l'objet du présent addendum pré-gel.

## Résumé des changements V1.1 → V1.2

| # | Changement | Nature |
|---|---|---|
| 1 | ρ redéfinie comme part des discontinuités **observées** dans le parcours **mesuré** ; statut renommé DOMINÉE PAR LES DISCONTINUITÉS OBSERVÉES ; seuil 0,5 inchangé | interprétation corrigée, formule et seuil inchangés |
| 2 | Règle B15 publiée intégralement : fenêtre UTC 21:00–23:00 selon saison (début 21:00–22:00 ±5 min), durée 45–75 min, unicité, statut HALTE_INDÉTERMINÉE sans exemption en cas de doute, aucune « panne » classée | règle fermée, aucun seuil de couverture modifié |
| 3 | C6-01 : critères ROBUSTE / FRAGILE_SIGNE / FRAGILE_MATÉRIALITÉ / CONTRÔLE_INDÉTERMINÉ et règle de déclassement figés avant tout calcul, sans p additionnelle | règle de décision fermée |

Aucune formule de L, Δ_seg, A, ER, S, PD, τ, AS, aucune constante de
classe, aucun seuil de couverture, de matérialité ou d'éligibilité,
aucune règle BY n'est modifié par le présent addendum.

## Soumission

Dossier final soumis au propriétaire : protocole V1.1 (`0fdb3920…`)
plus le présent addendum V1.2. Après validation seulement : gel chaîné
des deux documents (hashes dans le registre), puis ordre d'exécution
séparé. Restrictions inchangées : XAU/USD exclusivement, holdout
scellé, aucun calcul ni extraction, aucun backtest ni `challenge_sim`,
aucun J2/J3 automatique, aucun budget expérimental consommé, FRED
suspendue, 36 cellules S12 gelées, T0 séparé et inactif, aucune
modification des fiches historiques, F-H/F-I en réserve.
