# RE-ENTRY-006 — DÉCLENCHEUR DE PRIX contre HORLOGE M15 : DISCRIMINATION SUR CAS PRÉENREGISTRÉS

Cas discriminants et seuils des modèles figés **avant** évaluation (seq443), définitions H1/H2
inchangées depuis RE-ENTRY-005. La page publique, contrôlée ce cycle, est toujours inchangée
(49 595 transactions ; dernière activité 2026-11-27 11:01 serveur) : aucun nouveau panier —
le fournisseur semble en pause, ce qui est signalé comme interruption d'observation, pas comme
absence d'activité prouvée.

## Phase A — Audit temporel (M15_BOUNDARY_AUDIT.csv)
Horodatages affichés à la seconde. Sous le fuseau fortement étayé UTC+2, les bougies M15
s'ouvrent aux minutes :00/:15/:30/:45 du temps serveur affiché. A : 13:31:20 (**80 s après**
l'ouverture M15) ; B : 13:50:34 (334 s après la frontière, **2 s après la clôture de A**) ;
C, D, E : **exactement :00** (10:30:00, 10:45:00, 11:00:00). L'alignement de C/D/E n'est pas un
arrondi : trois entrées indépendantes à la seconde zéro. Réserve : si le fuseau réel différait
d'un quart d'heure (non étayé), l'alignement M15 disparaîtrait — l'audit repose sur UTC+2,
toujours « fortement étayé », non prouvé.

## Phases B/E — Confrontation H1 contre H2 (cas classés selon seq443)
| Panier | Classe | H1 (impulsion+reprise) | H2 (frontière + fond ≥ +5 bp) |
|---|---|---|---|
| A | favorable H1 (hors frontière, +11,3 bp/5 min) | **expliqué** | non |
| B | favorable H1 (hors frontière, +11,9 bp) | **expliqué** | non |
| C | favorable H2 (frontière, +2,7 bp/5 min mais +13,2 bp/15 min) | non | **expliqué** |
| D | **ambigu** (frontière ET impulsion +12,0 bp) | expliqué | non (fond 15 min +1,1 bp) |
| E | favorable H2 (frontière, **−3,1 bp/5 min**, fond +6,8 bp) | non | **expliqué** |
H1 seule : 3/5 expliqués, contre-exemples C et E. H2 seule : 2/5, contre-exemples A, B (et D par
le fond). Les échecs sont **disjoints** : chaque hypothèse explique exactement les cas que
l'autre manque. Selon la règle préenregistrée, une combinaison n'est créée que si les données
l'exigent — c'est le cas : **H3 = évaluation à la clôture M15 d'un contexte haussier, avec voie
rapide d'impulsion hors frontière**, classée **HYPOTHÈSE À TESTER** (formulée ce cycle, à juger
sur les prochains paniers, pas sur ceux-ci).

## Phase D — Non-entrées aux frontières (fenêtres couvertes uniquement)
Dans les fenêtres couvertes, les frontières M15 où le système était libre (aucun panier ouvert)
sont 10:30, 10:45 et 11:00 le 2026-11-27 : **3/3 ont produit une entrée**, en fond 15 min
haussier (+13,2 / +1,1 / +6,8 bp). Les frontières 13:45 et 14:00 le 26 tombaient pendant des
paniers ouverts (système occupé) et ne comptent pas. Aucune frontière libre en fond non
haussier n'a été observée : la condition de fond de H2 ne peut pas être éprouvée en négatif.
Ces 3/3 renforcent l'horloge sans la confirmer (le fond était haussier à chaque fois).

## Phase F — Fidélité de reproduction (en-échantillon, seuils figés seq443)
Modèle H1 : déclenche A, B, D (écarts 0 sur les heures connues) ; manque C et E.
Modèle H2 : déclenche C, E ; manque A, B, D. Aucun modèle ne reproduit les 5 décisions ;
H1+H2 en union les reproduisent toutes, ce qui est précisément le profil attendu si H3 est le
mécanisme réel — mais les seuils ont été lus sur ces mêmes cas : la fidélité **hors échantillon**
reste entièrement à établir sur les paniers à venir, conservés séparément à cet effet.

## Classement final
| Conclusion | Statut | Cas |
|---|---|---|
| H1 seule comme déclencheur universel | RÉFUTÉE | contre-exemples C, E |
| H2 seule comme déclencheur universel | RÉFUTÉE | contre-exemples A, B |
| Alignement M15 exact de C/D/E | FORTEMENT ÉTAYÉ (sous réserve du fuseau) | 3 |
| Redémarrage événementiel (B, 2 s après clôture) | FORTEMENT ÉTAYÉ | 1 (mécanisme) |
| H3 combinée (clôture M15 en fond haussier + voie rapide d'impulsion) | HYPOTHÈSE À TESTER | formulée sur 5, à juger sur les suivants |
| Signal exact | NON DÉTERMINABLE | — |

## Limites et suite
Le fournisseur n'a rien publié de nouveau depuis le 2026-11-27 11:01 (serveur) : la discrimination
attend ses prochains paniers. Les cas qui trancheront H3 : une entrée hors frontière **sans**
impulsion la réfuterait ; une frontière libre en fond haussier **sans** entrée réfuterait sa
branche horloge ; une entrée sur frontière en fond non haussier réfuterait sa condition de fond.
La collecte continue selon RE-ENTRY-003 ; chaque nouveau panier sera classé d'abord, analysé ensuite.
