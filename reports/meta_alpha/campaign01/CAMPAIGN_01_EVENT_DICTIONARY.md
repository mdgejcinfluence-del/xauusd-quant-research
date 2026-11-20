# CAMPAGNE 1 — DICTIONNAIRE DES ÉVÉNEMENTS STRUCTURELS (GELÉ AVANT CALCUL)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Gelé et chaîné avant
toute exécution du moteur (sha256 en chaîne). Corpus : tick IS 282 partitions
(borne 2020-01-20), barres **M1 sur Mid** (déclaré, campagne 0) avec spread médian de
barre. Aucune définition n'utilise d'information future pour *détecter* un événement :
le déclencheur n'emploie que les barres ≤ timestamp de détection. Les mesures « après »
(fenêtres +1/+5/+15/+30/+60 min) sont des **conséquences descriptives**, jamais des
rendements de stratégie : aucune entrée, aucun coût appliqué à un trade, aucun PnL.

## Conventions communes

Sessions UTC : Asie [00,08), Londres [08,13), New York [13,21), Nuit [21,24). Niveaux de
référence : extrêmes Asie du jour (haut/bas sur Mid de barre, déclarés), extrêmes de la
veille UTC. Régime : tercile F3 du jour (causal, campagne 0). Ères : 2010–13, 2014–16,
2017–20. **F7 : NON MESURÉ dans cette campagne** — la série horaire des probabilités du
modèle gelé n'est pas versionnée (seq 146) ; le croisement « risque de saut » est donc
absent des comparaisons, écrit tel quel, non substitué. Regroupement : événements d'une
même famille, même jour, même niveau, à moins de 60 min d'intervalle = **une grappe**
(unité d'indépendance avec le jour×niveau) ; les chevauchements sont comptés et publiés.

## Les sept familles

| ID | Événement | Niveau / déclencheur (causal) | Détection (timestamp) | Invalidation descriptive | Horizon d'observation | Métriques |
|---|---|---|---|---|---|---|
| EV1 | Extrêmes de session et transitions | Plus haut/bas de chaque session et de la journée | Heure (barre) où l'extrême final de session/journée est atteint pour la première fois | n/a (fait descriptif) | n/a | Heure médiane de formation, part des extrêmes par session, ordre haut vs bas |
| EV2 | Dépassement-balayage-réintégration | Clôture M1 au-delà d'un niveau (Asie ou veille), puis clôture repassant du bon côté ≤ 60 min | Barre de réintégration (le dépassement seul = EV2a compté à part) | Pas de réintégration sous 60 min → classé « dépassement poursuivi » | +60 min | Profondeur max au-delà (bp), délai de réintégration (min), fréquence de réintégration, amplitude future 1/5/15/30/60 après réintégration |
| EV3 | Cassure et retest | Clôture M1 au-delà du niveau + 5 bp (buffer fixe déclaré), puis retour à ±0,05 % du niveau ≤ 60 min avec clôture du bon côté | Barre de confirmation du retest (cassure sans retest = EV3a compté à part) | Clôture de réintégration complète avant retest | +60 min | Fréquence de retest, délai cassure→retest, fréquence « encore au-delà du niveau à +60 min », amplitudes futures |
| EV4 | Compression puis expansion | Range des 60 dernières min < 0,6 × médiane des ranges 60 min des 5 jours précédents (causal, jours du même fichier) | Première barre sous le seuil | Range repassant au-dessus du seuil avant 120 min sans expansion | +120 min | Durée de compression, range des 60 min suivantes (expansion), fréquence d'expansion ≥ 1,5× le range comprimé |
| EV5 | Impulsion et retracement | Barre M5 avec \|r\| ≥ P90 global de \|r\| M5 (seuil poolé, descriptif déclaré) | Clôture de la barre d'impulsion | n/a | +60 min (12 barres M5) | Profondeur du retour contraire maximal (% de l'impulsion, peut dépasser 100 %), délai du retour maximal, fréquence de retour ≥ 50 % / ≥ 100 %, amplitude future |
| EV6 | Consolidation | Suite maximale de barres M1 d'amplitude < médiane globale M1 (campagne 0), durée ≥ 6 barres | Fin de la suite | n/a | +60 min | Durée (barres), range des 60 min suivantes rapporté au range de la consolidation |
| EV7 | Extrêmes journaliers/hebdomadaires | Journée dont le range dépasse le P95 des ranges journaliers poolés ; extrême hebdomadaire (jour de formation du haut/bas de la semaine) | Clôture du jour | n/a | Semaine suivante exclue (description intra-semaine) | Fréquence, jour de semaine médian de formation des extrêmes hebdomadaires, part des journées extrêmes par ère/session dominante |

## Comparaisons conditionnelles pré-définies (les seules produites)

Par famille : global ; par session de détection ; par régime F3 ; par ère ; par
tercile d'amplitude initiale (EV2 profondeur, EV5 amplitude d'impulsion) ; par régime
de spread à l'événement (spread médian de la barre de détection, terciles poolés).
Règle de suffisance : cellule publiée « renseignée » si ≥ 200 événements **et** ≥ 100
grappes jour×niveau ; sinon « NON CONCLUANTE — effectifs ». Référence adaptée : chaque
famille est comparée (i) à sa propre distribution entre contextes et (ii) pour les
amplitudes futures, à la baseline campagne 0 du même horizon (amplitude médiane des
barres M5/M15/H1 du même régime) — jamais à un mouvement « quelconque » d'une autre
session. Biais de sélection documenté : détecter un événement conditionne sur
l'amplitude déjà réalisée ; les fréquences de continuation/retournement sont des
fréquences **descriptives conditionnelles**, pas des probabilités exploitables.

## Mesures pendant vs après

« Pendant » : profondeur, durée, spread à l'événement, amplitude initiale.
« Après » : amplitudes futures (range haut−bas des fenêtres +1/+5/+15/+30/+60, en bp),
délais, fréquences de retour/continuation définies mécaniquement ci-dessus. Aucune des
deux catégories n'est un rendement : pas de prix d'entrée, pas de sens de position,
pas de coût déduit — le « coût S2 au moment de l'événement » est le spread coté
mesuré de la barre de détection, rapporté comme contexte.

*Gel : sha256 de ce fichier chaîné avant exécution du moteur de campagne 1.*
