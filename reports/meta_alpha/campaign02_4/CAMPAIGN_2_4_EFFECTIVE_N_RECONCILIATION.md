# CAMPAGNE 2.4 (CHANTIER A) — RÉCONCILIATION DES EFFECTIFS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Document de
réconciliation demandé par le propriétaire (seq 192) entre les quatre
grandeurs du dimensionnement gelé. Il ne modifie aucun paramètre gelé
(seq 183), n'active rien, et **ne consulte aucun flux prospectif** (il
n'en existe pas). Tous les chiffres d'amorçage proviennent de l'extraction
IS déjà consultée (seq 179) et de la justification seq 187.

## 1. Les quatre grandeurs et leurs rôles

| Grandeur | Définition | Rôle dans le gel |
|---|---|---|
| Épisode brut | Un dépassement T0 éligible à l'issue mesurable | Unité de comptage de la collecte |
| Grappe jour × niveau | Tous les épisodes d'une même journée et d'un même niveau (2 sources × 2 côtés au maximum par jour) | Unité d'indépendance statistique (bootstrap et effet de plan) |
| Effectif indépendant équivalent | N_épisodes / DE, avec DE = 1 + (m* − 1)·ρ (m* ≈ 12,4 ; ρ estimé 0,121 → DE ≈ 2,38) | Unité du calcul de puissance |
| Planchers de grappes | ≥ 500 par groupe extrême ; ≥ 1 500 au total | Contrainte de structure, indépendante du calcul de puissance |

## 2. Réconciliation chiffrée (par groupe extrême, scénario central ρ = 0,121)

| Étape de conversion | Valeur | Origine |
|---|---|---|
| Indépendants requis par groupe | **1 400** | Gel seq 183 (MDE 5 pts, α 5 % bilatéral, puissance 90 % ; justification `CAMPAIGN_2_4_MDE_JUSTIFICATION.md` : 917 au scénario de référence 0,90/0,85, 1 595 au scénario conservateur 0,77/0,72 — 1 400 est la base prudente intermédiaire maintenue) |
| × effet de plan central (DE = 2,38) | **≈ 3 330 épisodes bruts par groupe** | 1 400 × 2,38 |
| Plancher de grappes du groupe | 500 grappes | Gel seq 183 |
| Épisodes attendus à 500 grappes (taille moyenne d'amorçage 7,12) | ≈ 3 560 épisodes | 500 × 7,12 |
| Indépendant équivalent de ces 3 560 épisodes | **≈ 1 496** (= 3 560 / 2,38) | ≥ 1 400 requis ✓ |

**Lecture** : au scénario central, le plancher de 500 grappes et
l'exigence de 1 400 indépendants **coïncident** (1 496 ≈ 1 400 à la marge
d'arrondi des paramètres d'amorçage). Aucun des deux critères n'est
redondant : ils sont deux expressions du même besoin tant que la structure
prospective ressemble à l'amorçage — et ils divergent dès qu'elle s'en
écarte, ce qui est précisément la protection recherchée.

## 3. Réconciliation au total (trois terciles)

| Grandeur | Valeur |
|---|---|
| Indépendants requis, 3 groupes | 3 × 1 400 = 4 200 |
| Épisodes bruts au scénario central | 4 200 × 2,38 ≈ **10 000** (fourchette de planification gelée : 10 000–14 000) |
| Plancher total de grappes | **1 500** |
| Épisodes attendus à 1 500 grappes | 1 500 × 7,12 ≈ 10 680 ✓ (dans la fourchette) |
| Indépendant équivalent correspondant | 10 680 / 2,38 ≈ 4 487 ≥ 4 200 ✓ |
| Journées minimales implicites | 1 500 grappes ÷ 2,01 grappes/journée (rythme d'amorçage : 5 057 grappes / 2 515 journées) ≈ **746 journées** |

## 4. Quand les critères divergent (sensibilité)

| Scénario | DE | Épisodes requis / groupe (pour 1 400 indép.) | Le critère actif devient |
|---|---|---|---|
| ρ = 0,05 (grappes quasi indépendantes) | 1,57 | ≈ 2 200 | **Grappes** : 500 grappes × 7,12 ≈ 3 560 épisodes donneraient 2 270 indépendants — la collecte continuerait jusqu'aux planchers de structure même si la puissance nominale est atteinte plus tôt |
| ρ = 0,121 (estimé, central) | 2,38 | ≈ 3 330 | Les deux critères coïncident (≈ 3 330–3 560 épisodes) |
| ρ = 0,20 | 3,28 | ≈ 4 590 | **Épisodes** : 500 grappes ne fourniraient que ≈ 1 086 indépendants ; la collecte continuerait au-delà du plancher de grappes jusqu'à l'effectif épisodes requis |
| ρ = 0,30 | 4,42 | ≈ 6 190 | **Épisodes**, nettement ; conformément au gel, si l'estimation figée à l'exécution dépasse ρ = 0,30, l'effectif est recalculé **avant** collecte, jamais pendant |

Le critère d'arrêt gelé est donc bien **conjoint** : pour chaque groupe
extrême, épisodes bruts ≥ (1 400 × DE figé) **et** grappes ≥ 500 ; au
total, grappes ≥ 1 500. Aucune lecture d'issue n'intervient dans l'arrêt.

## 5. Où se situe l'amorçage dans cette réconciliation (à ne pas confondre)

L'amorçage IS compte 35 988 épisodes à issue mesurable, 5 057 grappes,
2 515 journées — soit, divisé par le DE central, un équivalent de
≈ 15 100 indépendants au total (≈ 5 040 par tercile extrême de 11 996
épisodes). Cet échantillon **dépasserait** à lui seul les exigences
chiffrées, et il ne comptera **jamais** dans l'effectif de confirmation :
il est intégralement consulté. La réconciliation ci-dessus ne sert qu'à
démontrer que les planchers gelés sont mutuellement cohérents et atteignables
dans une collecte prospective de structure comparable (≈ 2,5 à 5 ans au
rythme historique de ~14 épisodes/journée, estimation de planification déjà
publiée seq 187). **Activation : uniquement par ordre d'exécution chaîné du
propriétaire.**
