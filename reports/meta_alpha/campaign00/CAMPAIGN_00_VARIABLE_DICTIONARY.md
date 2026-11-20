# CAMPAGNE 0 — DICTIONNAIRE DES VARIABLES (GELÉ AVANT CALCUL, seq 153)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Ce dictionnaire est
figé et chaîné avant toute exécution du moteur de baselines. Toute modification
ultérieure exige une nouvelle entrée de chaîne et ne peut pas porter sur une variable
dont les résultats auraient déjà été lus. Périmètre : corpus tick IS du programme
(282 partitions, borne 2020-01-20T09:36:27Z), XAU/USD uniquement. Holdout inaccessible.

## 1. Barres et horizons

Barres construites sur le **Mid** ((Bid+Ask)/2, déclaré — les niveaux de prix ne sont
pas des prix exécutables, et aucune mesure de cette campagne n'est un PnL) à partir des
ticks, par bucket UTC : **M1 (1 min), M5 (5 min), M15 (15 min), H1 (60 min)**. Une barre
exige ≥ 1 tick ; les buckets vides sont des données manquantes, jamais imputés.
OHLC de barre : premier/plus haut/plus bas/dernier Mid du bucket ; spread de barre =
médiane des spreads tick (Ask−Bid)/Mid × 10 000 (bp) des ticks du bucket.

## 2. Variables de résultat (par barre, par horizon)

| ID | Variable | Définition exacte |
|---|---|---|
| V1 | Rendement de barre | `r = 10 000 × (close/ouverture − 1)` en bp, barres consécutives au sein d'une même journée UTC uniquement (pas de rendement overnight entre barres) |
| V2 | Amplitude | `10 000 × (high − low)/ouverture` (bp) |
| V3 | Excursion haussière intra-barre | `10 000 × (high − ouverture)/ouverture` (bp) |
| V4 | Excursion baissière intra-barre | `10 000 × (ouverture − low)/ouverture` (bp) |
| V5 | Volatilité réalisée journalière | Par jour et horizon : `sqrt(Σ r²)` sur les barres du jour (bp) — descriptive |
| V6 | Persistance | Corrélation de Pearson entre r(t) et r(t−1) au sein du jour, poolée par horizon |
| V7 | Retournements | Part des paires de barres consécutives de signes strictement opposés (r(t)·r(t−1) < 0) |
| V8 | Retracement | Après une impulsion (barre avec \|r\| ≥ P90 de \|r\| du même horizon, seuil global calculé sur l'ensemble poolé — descriptif, déclaré), profondeur maximale du retour contre l'impulsion dans les 12 barres suivantes, en % de l'impulsion |
| V9 | Consolidation | Épisode = suite maximale de barres consécutives avec V2 < médiane globale de V2 de l'horizon (médiane poolée, déclarée) ; durée en barres |
| V10 | Compression/expansion | Par jour : ratio amplitude médiane du jour / amplitude médiane globale de l'horizon ; jours classés compression (< 0,7), normal (0,7–1,4), expansion (> 1,4) — seuils fixes déclarés |
| V11 | Événements extrêmes | Fréquence des barres avec \|r\| > seuils fixes {10, 20, 50} bp par horizon + part au-delà des quantiles P95/P99 poolés |
| V12 | Spread | Distribution de V-spread de barre (bp) |

## 3. Variables de contexte (causales uniquement)

- **Session** du timestamp de la barre (blocs UTC conventionnés seq 144/146) :
  Asie [00:00, 08:00), Londres [08:00, 13:00), New York [13:00, 21:00), Nuit [21:00, 24:00).
- **Régime de volatilité** : tercile de la **vol prédite F3 du jour** (série gelée
  `F3_DAILY_PRED.csv`, prévision formée avant le jour — aucune information future :
  la prédiction du jour j est calculée sur les données ≤ j−1 par construction du
  modèle gelé). Jours sans prédiction F3 : régime « non classé », exclus des
  décompositions par régime, conservés dans les références globales.
- **Jour d'annonce** (FOMC/NFP/CPI du calendrier PIT) : variable de contexte
  descriptive uniquement, hors toute fenêtre d'exécution.
- **Ères** : 2010–2013, 2014–2016, 2017–2020 (bornes fixes déclarées).

Variables de contexte et de résultat sont strictement disjointes : aucune variable de
résultat futur ne classe un régime (interdiction de fuite, doctrine du programme).

## 4. Statistiques produites par cellule

Cellule = variable × horizon × (global | session | régime | ère ; session×régime
seulement si effectifs suffisants). Pour chaque cellule : distribution empirique
résumée par n (barres), journées distinctes, couverture temporelle, % de données
manquantes, moyenne, écart-type, médiane, quantiles P50/P75/P90/P95/P99 des valeurs
signées pour V1 et des valeurs positives pour V2–V5/V8–V12, fréquences V7/V10/V11.
**Règle de suffisance (figée)** : cellule « renseignée » si n ≥ 1 000 barres et ≥ 100
journées distinctes ; sinon **« NON CONCLUANTE — effectifs insuffisants »**, publiée
telle quelle. Aucune combinaison non listée ici n'est produite (« ne pas produire
automatiquement toutes les combinaisons possibles »).

## 5. Qualité et comparaison

Critères de qualité figés : barre retenue si ≥ 1 tick (M1) ; journée retenue si ≥ 300
barres M1 ; doublons de timestamp conservés tels quels (ordre observation_id, patron
des moteurs du programme) ; trous = buckets absents (comptés, jamais comblés).
Règles de comparaison : les écarts entre cellules se décrivent en quantiles et en
points de fréquence, sans test confirmatoire (0 essai) ; toute observation atypique
éventuelle est consignée au registre des candidates J1 (étape C du blueprint) sans
mécanisme inventé et sans rentabilité attribuée.

*Gel : ce dictionnaire, sha256 chaîné en seq 153 avant exécution du moteur.*
