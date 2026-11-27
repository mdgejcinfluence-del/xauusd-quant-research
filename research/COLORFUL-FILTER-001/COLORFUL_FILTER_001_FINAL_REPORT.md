# COLORFUL-FILTER-001 — RAPPORT CONSOLIDÉ (audit, filtre d'entrée, moteur expérimental V2)

Préenregistrement seq447 (avant tout calcul). Moteur gelé `colorful_replay.py` **intouché**
(vérifié par `git diff`) ; moteur expérimental séparé `colorful_replay_v2.py`. Page HFM
recontrôlée ce cycle : **inchangée** (49 595 fermés, dernières transactions 2026-11-27
11:01 serveur) — aucune observation nouvelle ; le fournisseur reste en pause.

## A. Correction d'audit majeure (traceable, seq446 non réécrit)
Le matching glouton ±120 s (recalculé, `FILTER_LAB_RESULTS.json`) donne : A **−15,4 s**,
B −22,6 s, C +0,1 s, D −13,0 s, E +154,5 s. Le rapport seq446 déclarait A manqué de
1 071 s — c'est l'écart vers le panier simulé de 11:49 UTC, alors que celui de
**11:31:04 UTC correspond à A** (prix et durée 1 078 s ≈ 1 152 s réels concordent).
**Fidélité d'entrée V1 corrigée : 4/5, non 3/5.** E est le seul manqué, et par un
mécanisme identifié : à 09:00 UTC le moteur était **occupé par un panier simulé
supplémentaire ouvert à 08:50:06** (clôturé 09:01:19). Les entrées manquées et les faux
paniers ne sont donc pas deux problèmes indépendants : les faux paniers *causent* le
manqué E. De même, le décompte « 8 paniers supplémentaires » de seq446 ne portait que
sur des sous-fenêtres ; sur les fenêtres de replay complètes, V1 génère **58 paniers
dont 54 non appariés** — l'absence réelle hors fenêtres couvertes n'étant pas prouvée,
ce chiffre mesure la suractivité du modèle, pas 54 « erreurs » prouvées.

## B. Anatomie des faux paniers (cause principale identifiée)
Les réentrées simulées suivent la clôture précédente de **0,1 à 9 s** (médiane) : le
moteur ferme au point mort dès 60 s puis rouvre immédiatement tant que l'impulsion
persiste. 53 des 58 entrées simulées tombent dans des bougies M15 contenant déjà une
entrée simulée. Le trader réel, lui, place ses 5 premières entrées dans **5 bougies
M15 distinctes** (A 11:30, B 11:45, C 08:30, D 08:45, E 09:00 UTC).

## C. Filtres testés (features causales au tick, en-échantillon, EXPLORATOIRE)
| Filtre | Réelles gardées | Fausses gardées | Verdict |
|---|---|---|---|
| F1 voie rapide + ret15m ≥ +5 bp | 4/5 (D perdu) | 46/54 | **Réfuté** comme condition universelle |
| F4 ret30m>0 et ret60m>0 | 5/5 | 43/54 | Non discriminant |
| reprise5m ≤ 13 bp | 5/5 | 18/54 | Piste exploratoire (seuil ajusté sur A–E : sur-ajustement possible, **non adoptée**) |
| **F2 unicité par bougie M15** | **5/5** | structurel | **Adoptée dans V2 (expérimental)** |

F3 (délai minimal post-clôture) est réfutée par B (réouverture réelle à +2 s).

## D. Moteur expérimental V2 (= V1 + F2, rien d'autre)
Sur les mêmes fenêtres : **15 paniers au lieu de 58 ; entrées réelles appariées 5/5**
(A +19,8 s, B +82,7 s, C +0,1 s, D +0,1 s, E **+0,6 s** — l'occupation parasite ayant
disparu) ; 10 paniers non appariés subsistent. PnL simulé : −0,087 (26) / +0,087 (27)
USD/unité, coûts centraux — descriptif, aucun intérêt économique démontré.
**Limites** : résultat en-échantillon sur les 5 paniers ayant inspiré F2 ; B se dégrade
(−23 s → +83 s) ; la fidélité de **gestion** reste faible (nombre de positions exact
2/5 : A, E ; durées simulées ~60 s contre 650–1 152 s réelles pour A/B/C — la clôture
au premier retour au point mort après 60 s est trop précoce ; D réel ne dure que 17 s
avec 1 position, ce que l'amorçage systématique à +30 s ne peut pas reproduire).

## E–J. Réponses consolidées
- **Comprises** : gestion en deux phases (amorçage 16–40 s ; renforcement au recul
  −4,7 à −6,6 bp), clôtures groupées au voisinage du prix moyen, réinitialisation
  immédiate (1 cas), Buy seulement observé.
- **Entrées** : H3 reste l'hypothèse de portail ; F2 (unicité M15) est le premier
  filtre qui explique *simultanément* une partie des faux paniers et le manqué E.
  Falsification F2 : tout futur panier réel dont la 1re entrée partage la bougie M15
  d'une autre 1re entrée réelle la réfute ; tout futur panier manqué par V2 alors que
  sa bougie était libre la fragilise.
- **Volumes / sorties / 4e position** : inchangés — formule des lots, déclencheur exact
  de clôture, positions 4+ : **NON DÉTERMINABLES** sur les preuves actuelles.
- **Économie/risque** : descriptif seulement ; exposition sans stop observé, queue
  inconnue ; aucune conclusion de rentabilité licite.
- **Preuves nouvelles** : aucune (page inchangée) ; couverture publique toujours
  limitée aux 6 dernières transactions.

## Conclusion stratégique (question imposée)
**Nous possédons un modèle candidat partiellement fidèle — nettement amélioré en
fidélité d'entrée en-échantillon (V2 : 5/5, faux paniers ÷5), mais non validé.** La
capacité à reproduire les *prochaines* décisions n'est pas établie : F2 et H3 doivent
être jugées sur les paniers futurs du fournisseur, classés d'abord selon les cas
discriminants préenregistrés (seq443/447), sans retoucher les seuils. La fidélité de
gestion (durées, comptage des positions) est le prochain écart documenté à expliquer.

Artefacts : `ci_tools/colorful_filter_lab.py`, `ci_tools/colorful_replay_v2.py`,
`FILTER_LAB_RESULTS.json`, `REPLAY_V2_RESULTS.json`, `TRACEABILITY_MATRIX.csv`.
Reproduction : `/tmp/metaalpha-venv/bin/python ci_tools/colorful_filter_lab.py` puis
`ci_tools/colorful_replay_v2.py` (ticks Dukascopy comparatifs, jamais HFM).
