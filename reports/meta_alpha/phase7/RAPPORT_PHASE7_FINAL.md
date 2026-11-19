# RAPPORT PHASE 7 FINAL — CARTOGRAPHIE & DERNIÈRE RECHERCHE

## Issue (au sens du §6 de l'ordre)
**Atlas sans cellule survivante → clôture définitive et totale de la recherche d'avantages statistiques sur les actifs existants.** Budget Phase 7 : **0/24 essais consommés** — aucun candidat légal n'est né de la carte, donc rien n'a été testé. Les anciens budgets restent figés (tick 148/150, panel 28/60, exogène 6/60). Résurrection uniquement par : nouvelle source de données + préenregistrement + ordre explicite du propriétaire.

## Axe 1 — Atlas (0 essai, descriptif)
`ATLAS_XAUUSD.md` + `ATLAS_DATA.json` (code `ci_tools/phase7_atlas.py`). M1 : calendrier heure×semaine complet (vol, spread médian/p95, ticks, intensité de sauts). M2 : anatomie des événements aux amplitudes médianes (|ret| 15/60/240 min, spread d'entrée 2,3–3,1 bp — on décrit, on ne retrade pas F15). M3 : états macro (DFII10, pente, GVZ : distributions, persistance, co-variation avec la vol F3 et les sauts). M4 : corrélations panel et leur stabilité. M5 : carte des coûts par fenêtre×régime contre C1_BG = 4,7 bp.

**M6 — le crible : 0/30 cellules survivantes.** Le meilleur effet descriptif (|autocorrélation|×σ, fenêtre 12–16 UTC, régime nerveux, horizon 4 h) vaut **2,8 bp** contre un seuil requis de **9,4 bp** (plancher ECR≥2 ; les MDE cellulaires sont de 0,7–5,8 bp, ce n'est pas la puissance qui tue, c'est le coût). Partout ailleurs : 0,1–1,9 bp. La structure intraday de l'or est réelle (vol, spreads, sauts ont des calendriers marqués) mais son contenu directionnel descriptif est 3 à 30 fois sous le plancher de capturabilité. Aucune cellule n'avait le droit de naître comme candidate — et les pistes fermées (HMM, lead-lag, momentum daily, F15…) n'ont été ni rouvertes ni contournées.

## Axe 2 — Monétisation F3/F7 (0 essai, simulation pure)
`EDGE_MONETIZATION.md`. F3 : à espérance imposée μ ∈ {0, 2, 5} bp/j sur flux synthétiques déclarés calibrés par la vol prédite gelée, le sizing vol-cible F3 déplace P(passage phase 1) de **−0,1 / +1,5 / +1,4 points** — une régularisation du risque, pas de l'espérance ; à μ=0, P≈0,42 dans les deux cas (le hasard moins les règles). Incident consigné : `challenge_sim.simuler()` (gelé) déclare échec au premier DD −10 % sur 5 ans même après passage (P=0 mécanique) ; la comparaison utilise un simulateur de trajectoire déclaré (arrêt au passage/échec, règles V2), code gelé intact. F7 : éviter les fenêtres flaguées économise en médiane l'excès de spread des heures de saut par exécution reportée (chiffré dans le document) — un coût évité, pas un gain. **Verdict exigé par l'ordre, en toutes lettres : F3/F7 sont des actifs de service (timing/sizing/filtre) au profit d'une stratégie ; ils ne monétisent jamais seuls, et aucun frais de challenge ne peut être justifié par eux seuls.**

## Registre des 24 essais
| # | Candidat | Source | État |
|---|---|---|---|
| 1–24 | — aucun — | crible M6 : 0/30 cellules survivantes | jamais nés, 0 consommé |

BY(24) : sans objet (aucun test). Gates : M6 a joué le rôle de gate amont, comme prévu par l'ordre (« morte avant test — sans consommer d'essai »).

## Chaîne
seq 115 (MISSION) → seq 116 (Axe 1+2, M6) → seq 117 (CLOTURE). Intégrité vérifiée avant ce rapport. Holdouts jamais touchés.

## Conclusion
Sept phases, quatre corpus (tick, panel, exogène point-in-time, événements), des dizaines de familles et maintenant une cartographie exhaustive : le contenu directionnel capturable de XAUUSD aux coûts réels est nul là où nous avons regardé, et la carte montre qu'il n'y a pas d'endroit restant où regarder dans ces actifs. Le programme de recherche est clos — définitivement, proprement, et avec ses actifs permanents intacts : F3, F7, le châssis durci, le simulateur ancré, les packs scellés, la voie B démo (gratuite) comme seule activité encore rationnelle, et 117 entrées d'audit qui ne mentent pas.
