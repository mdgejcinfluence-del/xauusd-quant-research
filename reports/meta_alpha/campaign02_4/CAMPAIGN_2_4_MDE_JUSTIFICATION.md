# CAMPAGNE 2.4 (CHANTIER A) — JUSTIFICATION EXACTE DU MDE DE 5 POINTS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Ce document
complète, à la demande du propriétaire (seq 188), la justification du
dimensionnement gelé (seq 183) et chiffré sur l'amorçage
(`CAMPAIGN_2_4_DESIGN_JUSTIFICATION.md`). **Aucun résultat prospectif n'existe,
n'est collecté ni consulté.** Les valeurs définitives seront recopiées dans
l'ordre d'exécution chaîné, seul acte d'activation possible.

## 1. Hypothèse et probabilités exactes sous l'alternative

- H0 : P(réintégration ≤ T0+60 | tercile BAS de profondeur atteinte à T0)
  = P(réintégration ≤ T0+60 | tercile HAUT), seuils expanding-window.
- H1 retenue pour le dimensionnement (MDE = 5 points, dans le sens observé sur
  l'amorçage mais dimensionnée sur l'écart minimal jugé matériel) :
  **p_BAS = 0,90 et p_HAUT = 0,85** (écart δ = 0,05). Les taux d'amorçage
  (0,902 / 0,769, écart 13,3 points) ne servent **pas** au dimensionnement :
  dimensionner sur l'écart observé reviendrait à présupposer l'effet.
- Scénario de variance conservateur également calculé : p_BAS = 0,77 /
  p_HAUT = 0,72 (même δ = 0,05, variance binomiale plus élevée loin des bords).

## 2. Formule de puissance utilisée

Test bilatéral de comparaison de deux proportions, approximation normale
(formule de référence, celle du gel) :

n/groupe = [ z_{1−α/2}·√(2·p̄·(1−p̄)) + z_{1−β}·√(p₁(1−p₁) + p₂(1−p₂)) ]² / δ²

avec α = 0,05 bilatéral (z = 1,959964), puissance 1−β = 0,90 (z = 1,281552),
p̄ = (p₁+p₂)/2. Résultats exacts par cette formule :

| Scénario H1 | n indépendant requis / groupe extrême | Puissance à n = 1 400 / groupe |
|---|---|---|
| p = 0,90 vs 0,85 (référence) | **917** | 0,980 |
| p = 0,85 vs 0,80 | 1 212 | 0,937 |
| p = 0,77 vs 0,72 (variance conservatrice) | 1 595 | 0,864 |

Lecture : la base de planification gelée de **1 400 épisodes indépendants par
groupe extrême** couvre le scénario de référence avec une marge de puissance
(0,98) et reste proche de l'exigence du scénario le plus défavorable (1 595,
puissance 0,864 à 1 400). C'est cette prudence intermédiaire — et non le seul
scénario favorable — qui justifie le maintien de 1 400 plutôt que 917. Après
inflation par l'effet de plan (DE ≈ 2,38 au ρ estimé de 0,121 ; fourchette de
planification 2,4–3,3) : **3 350 à 4 600 épisodes observés par groupe extrême**,
soit **~10 000 à 14 000 épisodes au total**.

## 3. Justification des 1 500 grappes

Le plancher de 1 500 grappes jour×niveau au total (dont ≥ 500 par groupe
extrême) ne double pas le calcul d'effectif : il contraint la **structure** de
l'échantillon.

1. **Stabilité du bootstrap par grappes** : avec des tailles de grappes très
   inégales (amorçage : médiane 5, P99 = 27, max 40), l'inférence par
   rééchantillonnage de grappes n'est fiable que si le nombre d'unités
   rééchantillonnées est grand devant la queue des tailles ; 500 grappes par
   groupe est le seuil retenu pour qu'aucune grappe géante ne porte le
   contraste.
2. **Hétérogénéité temporelle lisible** : l'analyse par blocs (semestres)
   prévue au protocole §5 exige des blocs conservant chacun ≥ ~100 grappes
   par groupe ; 500 grappes par groupe sur une collecte pluriannuelle est le
   minimum compatible.
3. **Couverture en journées** : à la structure d'amorçage (5 057 grappes pour
   2 515 journées IS), 1 500 grappes correspondent à ~700 journées distinctes
   au minimum — le plancher protège contre un échantillon « riche en épisodes,
   pauvre en journées », où l'effectif nominal serait atteint sans
   l'indépendance requise.
4. **Non-contrainte au scénario central** : 500 grappes × ~7 épisodes ≈
   3 500 épisodes ≈ l'effectif requis après effet de plan ; le plancher
   coïncide avec le dimensionnement sans le durcir artificiellement, et devient
   la contrainte active seulement si les grappes prospectives sont plus
   petites ou moins corrélées qu'à l'amorçage.

Le critère d'arrêt de collecte est donc **double et conjoint** : effectif
épisodes par groupe atteint **et** planchers de grappes atteints, sans lecture
intermédiaire des issues (protocole gelé).

## 4. Séparation exacte amorçage / confirmation

| Élément | Amorçage (IS consulté) | Confirmatoire (prospectif) |
|---|---|---|
| Données | Corpus 2010–2020 déjà consulté, extraction seq 179 | Épisodes postérieurs au gel définitif de l'ordre d'exécution, jamais consultés avant le dégel ordonné |
| Rôles licites | Taux de référence 0,90/0,77, ρ = 0,121, tailles de grappes, point de départ des seuils expanding-window | Unique test de l'hypothèse principale, une fois, à double critère d'effectif atteint |
| Interdits | Ne compte **jamais** dans l'effectif de confirmation ; ses seuils historiques (1,2499/2,9694 bp atteinte ; 0,6748/1,9879 bp initiale) sont interdits en confirmation | Aucune lecture d'issue, aucun arrêt opportuniste, aucune réutilisation pour une exploration concurrente ; toute dérogation requalifie les données en matériau consulté exclu |
| Réutilisation croisée | Le flux prospectif est interdit à la Campagne 3 et à toute exploration | Les explorations historiques (Campagne 3) n'utilisent que l'IS déjà consulté ; les deux chantiers sont disjoints par construction |

La collecte prospective ne bloque ni ne conditionne les recherches
historiques ; réciproquement, aucune exploration historique ne peut puiser
dans le flux réservé. **Activation : uniquement par ordre d'exécution chaîné
du propriétaire. Le présent document n'active rien.**
