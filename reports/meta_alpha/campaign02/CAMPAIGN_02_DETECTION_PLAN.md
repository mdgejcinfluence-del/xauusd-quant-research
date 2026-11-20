# CAMPAGNE 2 — PLAN DE DÉTECTION GELÉ (seq 162, avant calcul)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Famille fermée de
**24 comparaisons** ; aucun test ajouté après calcul. Unité d'indépendance : grappe
jour×niveau (à défaut, journée). Bootstrap par grappes, 2 000 répétitions, graine
20261113 ; IC 95 % percentile ; correction **BY** sur les 24. **Règle J1 nouvelle** :
p_BY < 0,05 ET écart ≥ seuil matériel (5 points pour une proportion, 15 % pour un
ratio de médianes) ET n ≥ 200 événements et ≥ 100 grappes par bras ET signe cohérent
dans ≥ 2 ères sur 3 (quand la dimension testée n'est pas l'ère). Sinon : queue de
distribution ou non concluant, conservé dans les résultats négatifs.

| # | Famille | Comparaison (bras A vs B) | Variable |
|---|---|---|---|
| T01 | EV2 | Réintégration, profondeur tercile bas vs haut (par ère, causal) | taux de réintégration < 60 min |
| T02 | EV2 | Réintégration, ère 2010–13 vs 2017–20 | taux de réintégration |
| T03 | EV2 | Délai de réintégration, profondeur bas vs haut | médiane du délai (réintégrés) |
| T04 | EV2 | Réintégration, régime F3 BAS vs HAUT | taux de réintégration |
| T05 | EV2 | Réintégration, Londres vs New York | taux de réintégration |
| T06 | EV2 | Censure (> 60 min), profondeur bas vs haut | taux de censure |
| T07 | EV3 | Retest, régime F3 BAS vs HAUT | fréquence de retest |
| T08 | EV3 | Encore au-delà +60, régime BAS vs HAUT | fréquence (parmi retests) |
| T09 | EV3 | Encore au-delà +60, ère 2010–13 vs 2017–20 | fréquence (parmi retests) |
| T10 | EV3 | Encore au-delà +60, amplitude cassure bas vs haut | fréquence (parmi retests) |
| T11 | EV5 | Retracement ≥ 100 %, ère 2010–13 vs 2017–20 | fréquence |
| T12 | EV5 | Retracement médian, régime BAS vs HAUT | médiane du ratio |
| T13 | EV5 | Retracement ≥ 100 %, Asie vs New York (session de l'impulsion) | fréquence |
| T14 | EV6 | Range suivant 60 min, régime BAS vs HAUT | médiane |
| T15 | EV6 | Range suivant, ère 2010–13 vs 2017–20 | médiane |
| T16 | EV4 | Expansion ≥ 1,5×, régime BAS vs HAUT | fréquence |
| T17 | EV4 | Range d'expansion médian, ère 2010–13 vs 2017–20 | médiane |
| T18 | EV4 | Expansion ≥ 1,5×, durée compression courte vs longue (médiane) | fréquence |
| T19 | Ouvertures | Range 60 min New York, ère 2010–13 vs 2017–20 | médiane |
| T20 | Ouvertures | Mouvements extrêmes 5 min New York, régime BAS vs HAUT | fréquence |
| T21 | Ouvertures | Spread après ouverture Londres, ère 2010–13 vs 2017–20 | médiane |
| T22 | EV1 | Extrêmes de session formés dans le dernier tiers, Asie vs New York | fréquence (heure relative) |
| T23 | EV2 | Spread à l'événement, réintégrés vs censurés | médiane du spread |
| T24 | EV3 | Amplitude future 60 min après retest vs après réintégration (contextes appariés par régime, descriptif) | médiane |

Notes gelées : T22 utilise les heures de formation rapportées à la fenêtre de session
(Asie 00–08, New York 13–21) ; T24 est une comparaison de contextes documentée comme
biaisée en sélection (les deux bras ne partagent pas la même distribution
d'amplitude) — elle ne peut produire qu'une fiche « contexte », jamais une anomalie
directionnelle. Les profondeurs/amplitudes en terciles sont calculées **par ère**
(causalité d'époque : aucun quantile poolé futur ne classe un événement passé).
