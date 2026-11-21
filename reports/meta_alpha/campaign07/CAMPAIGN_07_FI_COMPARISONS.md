# CAMPAGNE 7 — COMPARAISONS PRÉENREGISTRÉES F-I (provisoires, pré-gel) ET MÉTHODE

**Statut : PRÉPARATION — aucun calcul.** Famille fermée proposée de cinq
comparaisons. Pour chacune : hypothèse, variable, population, unité,
matérialité, dépendances et inférence (livrables 5 et 6).

| ID | Hypothèse descriptive | Variable principale | Population (A vs B) | Unité / grappe | Matérialité |
|---|---|---|---|---|---|
| I-01 | Au contact d'un niveau rond, le prix franchit strictement plus (ou moins) souvent qu'au contact d'un niveau quelconque comparable | P(franchissement strict \| approche) | approches G50 vs approches placebo G50+25 | épisode d'approche / grappe-journée | 5 points |
| I-02 | Après une touche sans franchissement, le rejet est plus fréquent aux niveaux ronds | P(rejet \| touche) | touches G50 vs touches placebo | épisode / grappe-journée | 5 points |
| I-03 | Après franchissement strict, le prix parcourt une distance différente selon que le niveau est rond | distance post-franchissement à 60 min (médiane, bp) | franchissements G50 vs placebo | épisode / grappe-journée | ratio 1,15 |
| I-04 | L'effet de rondité dépend de l'échelle du nombre rond | P(franchissement strict \| approche) | approches R100 vs approches R10 (anneaux disjoints, grilles réelles seules) | épisode / grappe-journée | 5 points |
| I-05 | L'écart rond − placebo a évolué avec le niveau historique du prix | différence des P(franchissement) rond − placebo, 2010–13 moins 2017–20 (interaction) | approches des deux grilles, par ère | épisode / grappe-journée | 5 points |

## Garde-fous intégrés aux comparaisons

- **Placebo systématique** (I-01, I-02, I-03, I-05) : toute différence
  rond − placebo est la seule lecture « effet de rondité » autorisée ;
  les taux bruts aux niveaux ronds seuls ne sont jamais interprétés.
- **Confusions publiées, pas ajustées après coup** : ventilation des
  taux par session d'approche et par tercile d'amplitude contemporain
  (rétrospectif, étiqueté) pour chaque bras ; si les bras diffèrent
  fortement en composition, la lecture est déclassée en conséquence
  selon une règle à fermer au protocole consolidé.
- **Échelle et ères** : I-04 compare des anneaux disjoints (pas de
  niveau compté deux fois) ; I-05 teste si l'écart de rondité survit
  au resserrement relatif de la grille absolue quand le prix monte
  (50 USD ≈ 455 bp à 1 100 USD, ≈192 bp à 2 600).
- Touches simples, franchissements par saut, épisodes SIMULTANÉS et
  censures de suivi : publiés séparément, jamais dans les dénominateurs
  primaires au-delà de ce que les définitions prévoient.

## Méthode statistique et multiplicité (livrable 6)

- Unité : épisode d'approche ; **bootstrap par grappes-journées**
  (2 000 réplicats, graine publiée au gel) ; effets : différences de
  proportions (points) ou de médianes (ratio pour I-03), IC percentile
  95 %, p bootstrap bilatérales. I-05 : bootstrap de la différence des
  différences, mêmes grappes.
- **BY famille fermée de cinq, m = 5 fixe** (H₅ = 2,283333), formule et
  traitement des p NaN selon la règle gelée en Campagne 6
  (STRUCTURELLEMENT_NON_EVALUABLE publié, aucune imputation, facteur 5
  conservé).
- **Éligibilité pré-déclarée** : ≥200 épisodes et ≥100 grappes par bras
  (convention des campagnes 4–6) ; en dessous : NON_ELIGIBLE publiée,
  aucun assouplissement, aucune fusion d'anneaux après coup.
- **Matérialités** : 5 points de pourcentage (échelle des campagnes
  4–6) ; ratio 1,15 symétrique pour les distances (borne exacte
  1/1,15 = 0,8695652173913043, formulation logarithmique ln 1,15).
- Lectures fermées : CANDIDATE_J1 / SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL /
  NÉGATIF / NON_ELIGIBLE / STRUCTURELLEMENT_NON_EVALUABLE. Publication
  intégrale : effectifs initiaux/éligibles/censurés, couvertures,
  effets, IC, p brutes, q BY, matérialités, négatifs et non concluants.
