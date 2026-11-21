# CAMPAGNE 7 — RAPPORT SCIENTIFIQUE F-I « NOMBRES RONDS DU XAU/USD »

**Statut : EXÉCUTION DESCRIPTIVE TERMINÉE** selon le protocole gelé
V1 (`25090931…`, seq250 ; exécution autorisée seq251, gel confirmé
seq252). Aucune formule, grille, placebo, constante ou méthode n'a été
modifiée après le gel (deux correctifs de **code** postérieurs au gel,
sans portée méthodologique, sont documentés au registre des incidents :
ils réparaient l'implémentation des définitions gelées, pas les
définitions). Corpus IS : 282/282 partitions, 3 540 993 barres M1,
3 097 journées présentes.

## Populations (publiées intégralement)

Épisodes bruts par grille : G50 2 359 ; P50 (placebo +25) 2 420 ;
R100 1 290 ; P100 (descriptif) 1 325 ; R10 9 958 ; P10 (descriptif)
11 841. Événements terminaux toutes grilles : franchissements 14 520,
rejets 1 611, sauts 306, sans effet 99, **censures de fin de journée
12 657** (épisodes ouverts trop tard pour être résolus avant 23:59,
publiés, jamais complétés). Approches résolues primaires : G50 1 302,
P50 1 338, R100 691, R10 5 482. Épisodes simultanés (corrigés) : 95.

## Résultats détaillés I-01 à I-05

Bootstrap grappes-journées (2 000 réplicats, graine 20261113) ; BY
famille de cinq à **m = 5 fixe** ; matérialité 5 points / ratio 1,15 ;
éligibilité ≥200 épisodes et ≥100 grappes par bras (satisfaite partout
où la comparaison est évaluable).

| ID | Comparaison | Effet | IC 95 % | p | q BY (m=5) | n A/B | Composition | Lecture |
|---|---|---|---|---|---|---|---|---|
| I-01 | P(franch. \| approche) G50 vs P50 (90,5 % vs 88,6 %) | +1,84 pt | [−1,23 ; +4,93] | 0,232 | 0,883 | 1 302 / 1 338 | SENSIBLE (écart d'ère 5,1 pts) | **NÉGATIF** |
| I-02 | P(rejet \| touche) G50 vs P50 (21,9 % vs 22,2 %) | −0,29 pt | [−6,54 ; +6,05] | 0,938 | 1,000 | 549 / 632 | **NON ÉVALUABLE** (47–51 % d'épisodes sans strate comparable) | **NON ÉVALUABLE — COMPOSITION** |
| I-03 | Distance post-franchissement G50 vs P50 (médianes 26,96 vs 18,60 bp) | ratio 1,449 | [1,247 ; 1,695] | 0,0005 | 0,0057 | 1 114 / 1 097 | SENSIBLE (écart d'ère 7,0 pts) | **ASSOCIATION SENSIBLE À LA COMPOSITION (pas de candidate)** |
| I-04 | P(franch. \| approche) R100 vs R10 (91,6 % vs 89,7 %) | +1,88 pt | [−1,05 ; +4,54] | 0,212 | 0,883 | 691 / 5 482 | n/a (anneaux réels) | **NÉGATIF** |
| I-05 | Écart (G50−P50) entre ères : +0,26 pt (2010–13) vs +1,24 pt (2017–20) | −0,98 pt | [−7,61 ; +5,98] | 0,776 | 1,000 | 1 412 / 540 | **NON ÉVALUABLE** en 2017–20 (28,9 % sans strate comparable) | **NON ÉVALUABLE — COMPOSITION** |

### Lecture d'ensemble
- **Aux niveaux ronds comme aux placebos, une approche se termine par
  un franchissement strict dans ~89–92 % des cas** (bande d'entrée de
  25 bp, très étroite) ; ni la probabilité de franchissement (I-01),
  ni son évolution entre ères (I-05, effet quasi nul), ni l'échelle du
  rond (I-04) ne distinguent les grilles. Le rejet après touche est
  rare (~22 % des touches dans les deux grilles) et sa comparaison est
  non évaluable faute de strates de composition comparables (I-02).
- **I-03 est le seul signal** : après un franchissement strict d'un
  niveau multiple de 50, l'excursion médiane dans l'heure suivante est
  ~45 % plus grande qu'après un niveau placebo (26,96 vs 18,60 bp).
  Mais le contrôle de composition gelé le déclasse : la composition
  par ère des deux bras diffère de 7,0 points (au-dessus du seuil de
  5), donc la lecture fermée est **ASSOCIATION SENSIBLE À LA
  COMPOSITION — pas de candidate**, aucune fiche ANO. Conformément au
  protocole, cet écart peut refléter la composition (époque, contexte)
  des franchissements plutôt qu'une propriété des nombres ronds ; il
  ne démontre ni un mécanisme « psychologique » ni une capturabilité.

## Comparaisons par anneau et exposition (descriptif, sans test)

| Grille | Épisodes bruts | Résolus | P(franchissement) brute | Touches | Rejets |
|---|---|---|---|---|---|
| G50 (réel) | 2 359 | 1 302 | 0,905 | 553 | 120 |
| P50 (+25) | 2 420 | 1 338 | 0,886 | 645 | 141 |
| R100 (réel) | 1 290 | 691 | 0,916 | 283 | 56 |
| P100 (+25, quart de pas) | 1 325 | 704 | 0,891 | 332 | 66 |
| R10 (réel) | 9 958 | 5 482 | 0,897 | 2 394 | 557 |
| P10 (+5) | 11 841 | 6 618 | 0,894 | 3 011 | 671 |

Distances initiales médianes quasi identiques entre grilles réelles et
placebo (22,4–22,7 bp) ; expositions comparables (ratio épisodes
G50/P50 : 0,97 en I-01, 1,02 en I-03). Répartitions détaillées par ère,
session, sens et distance publiées dans `CAMPAIGN_07_DETAILS.json`
(contrôle de composition ligne par ligne).

## Conclusion descriptive

Dans ce corpus et sous les définitions gelées, **les nombres ronds ne
forment pas une famille de comportements distincte démontrée** : quatre
comparaisons sur cinq sont négatives ou non évaluables, et la seule
association significative et matérielle (distance post-franchissement)
est déclassée par le contrôle de composition préenregistré. Aucune
candidate J1, aucune promotion automatique. Ce résultat négatif
documenté clôt la question telle qu'elle a été posée ; toute reprise
(autres bandes, autres suivis, mécanisme explicite) serait un nouveau
protocole sur ordre distinct.
