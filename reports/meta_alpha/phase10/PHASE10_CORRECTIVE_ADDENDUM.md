# PHASE 10 — ADDENDUM CORRECTIF CIBLÉ F10-01 / F10-03 (amendement, seq289)

**Statut : amendement ciblé autorisé par décision formelle du
responsable (ordre correctif Phase 10). Les sept documents gelés
PHASE 10-A (seq283) ne sont ni modifiés ni remplacés ; leurs SHA-256
restent ceux du procès-verbal de gel `PHASE10A_FREEZE_RECORD.md`.
Le présent addendum ne vaut que pour l'implémentation du seuil causal
des familles F10-01 (H1) et F10-03 (H4).**

## A. Règle amendée (implémentation des seuils Q95 de F10-01/F10-03)

- Fenêtre causale **fixe de 250 barres précédentes** (barre courante
  strictement exclue), séparée par timeframe, sans pooling.
- Les rendements **NaN et non finis sont exclus** de la fenêtre ; aucune
  imputation, aucune interpolation de valeurs manquantes, aucun
  remplacement par zéro.
- **Minimum de 200 rendements valides** dans la fenêtre de 250 ;
  en dessous : fenêtre **INELIGIBLE_CAUSAL_WINDOW**, aucun seuil,
  aucun événement.
- **Aucune extension de la fenêtre vers le passé** pour compenser les
  valeurs invalides : la fenêtre reste les 250 barres précédentes.
- Quantile Q95 calculé **uniquement sur les valeurs valides**, par
  interpolation linéaire (type 7, convention du protocole gelé).
- Toutes les autres définitions gelées sont maintenues : Q95, horizons,
  entrée à la première cotation exécutable de la barre suivante,
  délai maximal de 120 s, comptabilité Bid/Ask, portes économiques
  avant inférence, BY à **m = 6 fixe** (jamais réduit à 2).

## B. Correction technique et validation synthétique

Correction exclusive de l'implémentation du seuil de F10-01/F10-03.
Avant tout accès aux artefacts de production, des tests synthétiques
vérifient : fenêtre contenant des NaN ; exactement 200 valeurs
valides ; 199 valeurs valides (inéligible) ; absence de fuite de la
barre courante ; quantile calculé sur les seules valeurs valides ;
absence d'extension silencieuse de fenêtre.

## C. Relance ciblée et artefacts

Vérification préalable des artefacts du run moteur 44919631588
(intégrité, provenance, couverture des 282 partitions IS). Ces
artefacts contiennent les sorties événementielles du moteur, pas les
séries de barres : s'ils s'avèrent incomplets pour recalculer les
seuils, seule la recomputation ciblée F10-01/F10-03 sur le même corpus
IS est autorisée (aucun autre test relancé, aucune modification de
paramètres, aucun accès au holdout).

## D–G. Multiplicité, livrables, interdictions, statuts

BY m = 6 conservé ; aucune p-value pour une hypothèse arrêtée aux
portes. Livrables par test : barres examinées, rendements valides,
NaN/non-finis (nombre et proportion), fenêtres inéligibles, événements
détectés et éligibles, seuils Q95, brut et net, C_ref, MAE/P90/ES90
par événement et par grappe, portes, p-value si inférence autorisée,
verdict ; plus comparaison avant/après correction. F10-02, F10-04,
F10-05, F10-06 : verdicts conservés. Phase 10 non clôturée jusqu'au
rapport final des deux tests.
