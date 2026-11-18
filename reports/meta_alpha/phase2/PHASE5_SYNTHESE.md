# PHASE 5 « DERNIÈRE CARTOUCHE » — SYNTHÈSE (IS seul, OOS/HOLDOUT fermés)

## Verdict : les quatre cellules sont NON TESTABLES au gate de puissance (R1/R3)
Les comptages ont été calculés et consignés **avant** toute agrégation de performance ; aucune moyenne de cellule n'a été produite ni lue. Les retours bruts existent dans les artefacts (`F13_GAP.csv` : 157 événements ; `F13_JUMP.csv` : 2 845 sauts), mais les agréger après un gate négatif violerait le protocole gelé.

| Cellule | Événements | n_eff | Seuil | Verdict |
|---|---|---|---|---|
| F13-A gap week-end FADE | 157 | 135 | ≥ 200 | **NON TESTABLE** |
| F13-B gap week-end SUIVI | 157 | 135 | ≥ 200 | **NON TESTABLE** |
| F13-C ORI dans fenêtres F7 | 80 | 38 | ≥ 200 | **NON TESTABLE** |
| F13-D post-saut dans fenêtres F7 | 111 | 153* | ≥ 200 | **NON TESTABLE** |

\* n_eff de F13-D calculé par la formule R2 (autocorrélation négative des événements en rafale inverse) ; même au n brut (111) le seuil n'est pas atteint.

## Pourquoi c'est le bon résultat
En dix ans d'IS, il n'existe que ~157 week-ends avec un gap ≥ 2× le spread d'ouverture dominical, et le conditionnement F7 × spread ne laisse que 80–111 sauts exploitables en 2017–2019. Aucune statistique honnête ne distingue un edge d'un bruit sur ces effectifs (±14–25 points d'intervalle à ces tailles, échelle R6). Élargir les seuils après coup pour « faire passer » le gate serait exactement le re-grillage interdit. Les cellules sont fermées **sans avoir été regardées** — c'est la forme la plus propre de résultat négatif.

## Arrêt définitif (instruction Phase 5, §3)
- La recherche directionnelle systématique sur ce corpus est **close**, quelle que soit l'échelle (tick, heure, jour, panel) : 4 phases, ~150 essais budgétés et comptés, chaque piste testée une fois, proprement, ou fermée au gate sans être testée.
- Budget final : tick 148/150 déclarés (les 2 derniers essais restent intacts à jamais, comme preuve d'arrêt par discipline) ; panel 28/60 (solde non dépensé).
- **Voie B (le produit restant)** : le châssis + F3 (volatilité, validée L2) + F7 (sauts, validée L2) comme couche de discipline pour un trading discrétionnaire du propriétaire — sizing par la volatilité prévue, évitement des fenêtres à saut, kill-switch et gouverneur du châssis. C'est un outil de gestion du risque, pas un générateur de signaux, et il n'a jamais été présenté autrement.
- OOS et HOLDOUT (XAUUSD et panel) restent fermés et intacts. Si un jour une hypothèse nouvelle naît d'une source nouvelle (pas d'un re-grillage), elle pourra les ouvrir sur ordre explicite, avec un préenregistrement neuf.

## Le programme, en une phrase
Nous savons comment ce marché fonctionne, nous savons qu'il ne révèle pas sa direction à qui la demande par les prix, nous savons prévoir quand il devient dangereux — et nous savons, désormais de manière définitive et chiffrée, que c'est tout ce que ces données gratuites contiennent.
