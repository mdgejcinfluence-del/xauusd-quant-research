# CAMPAGNE 2.1 — AUDIT DU BUG DE P-VALEUR DE LA CAMPAGNE 2

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Cause exacte

Première version de `boot_prop` / `boot_med` dans `ci_tools/campaign02_detection.py` :

```python
p = (np.sum(np.abs(reps) >= abs(obs)) + 1) / (NB + 1)   # INCORRECT
```

Les réplicats bootstrap `reps` sont, par construction, centrés autour de l'effet
**observé**, pas autour de zéro. La probabilité qu'un réplicat centré sur l'observé
dépasse l'observé en valeur absolue vaut ≈ 0,5 quel que soit l'effet : les 24
p-valeurs brutes sont toutes sorties entre 0,48 et 1,00, et après correction BY
toutes à 1,00 — la règle gelée ne pouvait déclarer **aucune** candidate, y compris
pour des intervalles de confiance excluant très largement zéro (p. ex. T01,
IC [0,316 ; 0,333]).

## Correction

```python
p = min(1.0, 2 * min(mean(reps <= 0), mean(reps >= 0)))        # proportions
p = min(1.0, 2 * min(mean(log(reps) <= 0), mean(log(reps) >= 0)))  # ratios
```

p bilatéral = deux fois la part des réplicats de l'autre côté de l'effet nul,
cohérent avec l'IC percentile publié. **Recalcul intégral des 24 comparaisons**
(seconde exécution complète du moteur corrigé, même graine 20261113, mêmes
données, même plan) : c'est cette seconde exécution qui fait foi et qui est
commitée.

## Avant / après

| | Avant correction | Après correction |
|---|---|---|
| p bruts (24) | 0,48 – 1,00 | 0,000 – 0,61 |
| p_BY | tous 1,00 | 14 tests < 0,001 ; le reste ≥ 0,37 (sauf T05 < 0,001 sous seuil matériel) |
| Candidates selon la règle gelée | 0 | 14 |
| IC 95 %, effectifs, écarts | inchangés (le bootstrap des IC n'était pas affecté) | identiques |

Le bug ne touchait que le calcul de p ; les écarts, intervalles, effectifs et
grappes de la première exécution étaient corrects et sont identiques après
correction — vérifié ligne à ligne sur les sorties.

## Protocole gelé (seq 164) — vérification

- Les 24 comparaisons, leurs bras, variables, seuils matériels et la règle J1 sont
  ceux du plan hashé (sha256 chaîné seq 164), à l'exception consignée du seuil de
  T22 (coquille « 9 » → 0,05, règle générale du plan, corrigée avant classification
  et documentée à l'audit statistique de la Campagne 2).
- Aucune sélection sur la nouvelle significativité : les 24 résultats corrigés sont
  publiés, positifs, négatifs et sous-seuil (fichier
  `CAMPAIGN_02_CONDITIONAL_BASELINES.csv` + document des résultats négatifs).
- Correction BY recalculée sur les p corrigés (fonction `by()` inchangée entre
  les deux exécutions ; seuls les p d'entrée ont changé).
- La cohérence d'ère des candidates a été vérifiée dans un calcul séparé publié
  (Campagne 2, rapport §audit) ; les fiches retenues la satisfont toutes.

## Portée

Le bug aurait produit un faux négatif global (« aucune anomalie détectée ») s'il
n'avait pas été repéré à la lecture des IC. Il est consigné ici pour que tout
réexamen puisse reproduire les deux exécutions : la première version du code est
dans l'historique git du fichier, la version corrigée est celle commitée.
