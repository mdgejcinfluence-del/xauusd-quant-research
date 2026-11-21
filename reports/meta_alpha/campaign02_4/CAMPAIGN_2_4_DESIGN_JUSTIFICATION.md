# CAMPAGNE 2.4 (CHANTIER A) — JUSTIFICATION COMPLÈTE DU DIMENSIONNEMENT

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Calculs de
dimensionnement et statistiques de dépendance sur l'échantillon d'**amorçage**
(corpus IS déjà consulté) ; aucun résultat de confirmation n'existe ni n'est
consulté. Ce document complète le gel de principe
(`CAMPAIGN_2_4_POWER_ASSUMPTIONS_FREEZE.md`) ; les valeurs définitives seront
recopiées dans l'ordre d'exécution chaîné.

## 1. Distribution des tailles de grappes (amorçage, 35 988 épisodes à issue mesurable)

| Statistique | Valeur |
|---|---|
| Grappes jour×niveau | 5 057 |
| Épisodes par grappe : moyenne / médiane | 7,12 / 5 |
| P90 / P99 / max | 16 / 27 / 40 |
| Coefficient de variation des tailles | 0,86 |
| Grappes de taille 1 | 884 (17,5 %) |
| Grappes de taille ≥ 10 | 1 417 (28,0 %) |

Les tailles sont fortement inégales : l'effet de plan doit donc utiliser la
taille ajustée m* = (CV² + 1)·m̄ ≈ **12,4**, et non la seule moyenne 7,1 — utiliser
7,1 sous-estimerait l'inflation de variance d'environ 40 %.

## 2. Corrélation intragrappe (estimée sur l'amorçage)

Estimateur ANOVA à un facteur (groupes = grappes) sur l'issue binaire de
réintégration : **ρ ≈ 0,121** (MSB 0,2217 ; MSW 0,1121 ; m₀ 7,12 ; taux global
d'amorçage 0,850). Lecture : deux dépassements de la même journée et du même
niveau se ressemblent modestement dans leur issue — la dépendance existe, elle
est loin de l'identité. Cette valeur est une propriété de l'amorçage ; elle sera
ré-estimée et **figée dans l'ordre d'exécution** avant la collecte, sans être
révisée ensuite.

## 3. Sensibilité de l'effet de plan (DE = 1 + (m* − 1)·ρ, m* = 12,4)

| ρ | DE | Épisodes requis par groupe extrême (base 1 400 indépendants, MDE 5 pts, puissance 90 %, α 0,05) |
|---|---|---|
| 0,05 | 1,57 | ~2 200 |
| 0,10 | 2,14 | ~3 000 |
| **0,121 (estimé)** | **2,38** | **~3 350** |
| 0,20 | 3,28 | ~4 600 |
| 0,30 | 4,42 | ~6 200 |
| 0,50 | 6,70 | ~9 400 |

Le dimensionnement retient le scénario ρ estimé majoré : planification sur
**DE ≈ 2,4–3,3**, soit **3 350 à 4 600 épisodes par groupe extrême** et, les trois
terciles confondus, **~10 000 à 14 000 épisodes** au total. Si l'estimation figée
à l'exécution dépasse ρ = 0,30, l'effectif est recalculé avant collecte (jamais
pendant).

## 4. Justification des planchers de grappes (500 par groupe, 1 500 au total)

- **500 grappes par groupe extrême** : (i) le bootstrap par grappes n'est stable
  que si le nombre d'unités rééchantillonnées est grand devant la queue de la
  distribution des tailles (P99 = 27 épisodes : quelques grappes géantes ne
  doivent pas porter le contraste) ; (ii) l'analyse d'hétérogénéité exige des
  blocs temporels (semestres) conservant chacun un ordre de grandeur de
  ≥ 100 grappes par groupe ; (iii) à taille moyenne de grappe ~7 et ρ ≈ 0,12,
  500 grappes ≈ 3 500 épisodes ≈ l'effectif requis au scénario central — le
  plancher n'est donc pas contraignant au-delà du dimensionnement, il le
  protège contre un échantillon « gros en épisodes, pauvre en journées ».
- **1 500 grappes au total** : somme des planchers des deux groupes extrêmes
  plus le tercile médian observé (non décisionnel mais nécessaire à la
  classification et aux descriptions par bloc) ; il garantit aussi la couverture
  d'au moins ~700 journées distinctes aux densités historiques.

## 5. Séparation amorçage / confirmatoire

| | Amorçage | Confirmatoire |
|---|---|---|
| Période | IS 2010–2020 (déjà consulté) | Postérieure au gel définitif, jamais consultée |
| Usage licite | Seuils initiaux expanding-window, estimation de ρ et des tailles de grappes, taux de référence de planification | Test de l'hypothèse principale, une seule fois, à effectif cible atteint |
| Interdits | Ne compte jamais dans l'effectif de confirmation | Aucune lecture d'issue avant le dégel ordonné ; aucune réutilisation exploratoire |

La collecte prospective ne bloque pas les recherches historiques : les deux
chantiers consomment des données disjointes par construction.
