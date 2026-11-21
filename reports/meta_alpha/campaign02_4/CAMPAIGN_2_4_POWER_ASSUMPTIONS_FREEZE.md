# CAMPAGNE 2.4 — HYPOTHÈSES EXACTES DU DIMENSIONNEMENT (GEL DE PRINCIPE)

**DOCUMENT DE GEL — AUCUN CALCUL SUR DONNÉES NOUVELLES, AUCUNE CONSULTATION
INTERMÉDIAIRE.** Ce document complète `CAMPAIGN_2_4_POWER_REQUIREMENTS.md` en
figeant les hypothèses chiffrées. Le gel devient définitif uniquement par l'ordre
d'exécution chaîné qui précédera la collecte ; d'ici là, aucune valeur ci-dessous
ne peut être modifiée sans décision propriétaire explicite.

## 1. Paramètres du test principal

| Paramètre | Valeur gelée (proposition) |
|---|---|
| Hypothèse | Contraste de réintégration sous 60 min, tercile BAS − HAUT de la profondeur atteinte à T0 (seuils causaux expanding-window) |
| α | 0,05 bilatéral, test unique (pas de correction sur le test principal ; secondaires en famille BY séparée) |
| Puissance cible | 0,90 (0,80 en analyse de sensibilité documentée, sans valeur de décision) |
| MDE de décision | **5 points** de pourcentage |
| Taux de référence (planification, corpus consulté) | p_BAS ≈ 0,90 ; p_HAUT ≈ 0,77 — utilisés uniquement pour dimensionner, jamais comme résultats |
| Unité d'indépendance | **Grappe jour×niveau** — les épisodes d'une même grappe ne sont jamais comptés comme indépendants |
| Intervalle | Bootstrap par grappes, 2 000 répétitions, graine figée dans l'ordre d'exécution |

## 2. Épisodes ≠ observations indépendantes

Sur le corpus consulté : 36 011 épisodes pour 5 057 grappes, soit **m ≈ 7,1
épisodes par grappe** en moyenne. L'effectif qui pilote la puissance est le
nombre de grappes, pas le nombre d'épisodes. Toute communication d'effectif
devra publier les deux, par groupe.

## 3. Corrélation intragrappe et effet de plan

L'effet de plan vaut DE = 1 + (m − 1)·ρ, où ρ est la corrélation intragrappe de
l'issue (réintégration) au sein d'une grappe jour×niveau. ρ n'est pas connu ex
ante ; il sera **estimé sur la seule période d'amorçage** (données de
calibration, features et issues d'amorçage déjà historiques au moment du gel
définitif) et la valeur retenue sera inscrite dans l'ordre d'exécution avant le
début de la collecte. Table de planification (m = 7,1) :

| ρ supposé | DE | Épisodes requis / groupe extrême (MDE 5, puissance 90 %, base 1 400 indépendants) | Épisodes totaux (3 terciles) | Grappes totales correspondantes |
|---|---|---|---|---|
| 0,10 | 1,6 | ~2 250 | ~6 750 | ~950 |
| 0,20 | 2,2 | ~3 100 | ~9 300 | ~1 300 |
| 0,30 | 2,8 | ~3 950 | ~11 850 | ~1 650 |
| 0,50 | 4,1 | ~5 700 | ~17 100 | ~2 400 |

**Garde-fous gelés** : au moins **500 grappes par groupe extrême** et **1 500
grappes au total**, quel que soit ρ ; si l'estimation d'amorçage donne DE > 4,
l'effectif est révisé **avant** la collecte, jamais pendant. Au rythme
historique (~14 épisodes/journée), la durée indicative reste de ~2,5 à 5 ans ;
ce constat n'autorise ni raccourci ni lecture anticipée.

## 4. Traitement des événements censurés

- Convention principale (gelée) : pas de réintégration à T0+60 = **non-réintégration**
  (censure à droite absorbée dans l'issue) — les taux de référence §1 incluent
  déjà cette convention, donc aucun gonflage supplémentaire de l'effectif.
- Taux de censure attendu (descriptif consulté) : ~10 % (tercile BAS) à ~23 %
  (tercile HAUT) ; il sera publié par groupe avec les résultats.
- Sensibilité préenregistrée (sans valeur de décision) : exclusion des épisodes
  tronqués par la fin de journée (< 60 barres disponibles après T0) et analyse
  restreinte aux épisodes à fenêtre complète.
- Aucun modèle de survie dans le test principal (descriptif confirmé seulement).

## 5. Aveuglement et réserve des données

Les données prospectives collectées pour cette hypothèse sont **réservées** :
aucune réutilisation pour des explorations concurrentes, aucune statistique
d'issue calculée avant l'atteinte de l'effectif cible, features collectées par
un pipeline qui ne calcule pas l'issue avant le dégel ordonné. Toute dérogation
exige un nouvel ordre et transforme les données concernées en matériau consulté,
définitivement exclu de la confirmation.
