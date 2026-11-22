# PHASE 11-C.1 — RÉCONCILIATION NUMÉRIQUE, CONTRÔLE DES DÉNOMINATEURS ET GEL DES RÉSULTATS

**Verdict : `RECONCILIATION_CONFORME`**

Contrôle de cohérence indépendant, réalisé **exclusivement à partir
des livrables committés de la Phase 11-C** (`PHASE11C_EVENT_PATHS.csv`,
`PHASE11C_ARCHETYPES.csv`, `PHASE11C_HORIZON_METRICS.csv`,
`PHASE11C_RESULTS.json`). Aucune relance du moteur, aucune extraction
M1, aucune reconstruction de trajectoire, aucun recalcul de grappe,
aucun accès au holdout. Anciens livrables et protocole 11-A inchangés.

## 1. Réintégration et reprise — numérateurs et dénominateurs exacts

### F10-01 (H1)

| Grandeur | Numérateur | Dénominateur | Recalculé | Communiqué |
|---|---|---|---|---|
| Réintégration confirmée | 2 695 | 3 107 admissibles | **86,74 %** | 86,7 % |
| — sur complets seuls | 2 692 | 3 104 | 86,73 % | — |
| Reprise après réintégration | 2 033 | 2 695 réintégrés | **75,44 %** | 75,4 % |
| — sur complets seuls | 2 032 | 2 692 | 75,48 % | — |
| Archétype REINTEGRATION_PUIS_REPRISE | 2 032 | 3 107 | **65,40 %** | 65,4 % |

Produit des deux taux : 86,74 % × 75,44 % = **65,43 %**, contre
65,40 % d'archétype. **Écart = 1 événement**, entièrement expliqué :
un événement H1 réintégré avec reprise mais **censuré** (horizon
< 8, lacune anormale) est classé `CENSURE` par la hiérarchie gelée ;
le produit des taux le compte (ses indicateurs de réintégration et
de reprise sont présents sur sa trajectoire partielle), la
proportion d'archétype ne le compte pas. Les dénominateurs ne sont
pas identiques (3 107 admissibles pour les taux de réintégration —
trajectoires partielles incluses — contre population complète pour
l'archétype), et aucun chiffre n'a été modifié pour forcer la
concordance.

### F10-03 (H4)

| Grandeur | Numérateur | Dénominateur | Recalculé | Communiqué |
|---|---|---|---|---|
| Réintégration confirmée | 632 | 660 admissibles | **95,76 %** | 95,8 % |
| — sur complets seuls | 629 | 657 | 95,74 % | — |
| Reprise après réintégration | 542 | 632 réintégrés | **85,76 %** | 85,8 % |
| — sur complets seuls | 539 | 629 | 85,69 % | — |
| Archétype REINTEGRATION_PUIS_REPRISE | 539 | 660 | **81,67 %** | 81,7 % |

Produit des taux : **82,12 %** contre 81,67 %. **Écart = 3
événements**, même mécanisme : les 3 événements H4 censurés étaient
tous réintégrés avec reprise sur leur trajectoire partielle.

Effectifs de contrôle : admissibles 3 107 / 660 ; complets 3 104 /
657 ; censurés 3 / 3 (`LACUNE_ANORMALE` dans les deux cas) ; touches
de P0 : 3 071 / 658 ; extensions confirmées : 2 945 / 648.

## 2. Archétype `CONTINUATION_SANS_REPLI_CONFIRME` à 0 %

Numérateur **0** pour les deux populations — sur les 3 107 / 660
admissibles comme sur les seuls complets (3 104 / 657). Le zéro est
réel : tout événement complet ayant une extension confirmée
présente un repli sur clôtures ou une réintégration. Les cas
censurés (3 + 3) sont classés `CENSURE`, hors des six archétypes,
et les cas ambigus intraminutes sont à **0** des deux côtés ; aucun
événement n'est donc masqué par le dénominateur. Distributions
complètes recalculées conformes à `PHASE11C_ARCHETYPES.csv`
(H1 : 2 032 / 660 / 248 / 162 / 3 / 2 ; H4 : 539 / 90 / 16 / 12 / 3,
somme = population admissible).

## 3. Cohérence MFE / clôture finale

Aucune contradiction à réconcilier : les deux grandeurs ne mesurent
pas la même chose. Le **MFE** est le maximum cumulé de l'excursion
favorable (extrema Mid intrabougies) depuis P0 sur toute la
fenêtre ; la **clôture** est le déplacement directionnel terminal
à t+8 (clôture Mid vs P0, en bp relatifs, même horizon, mêmes
ensembles complets n = 3 104 / 657). Par événement, MFE ≥ déplacement
terminal par construction. Les médianes peuvent donc coexister sans
incohérence : H1 MFE médian 32,88 bp contre clôture médiane −2,24 bp ;
H4 65,22 bp contre −4,64 bp. La trajectoire médiane s'étend
fortement puis revient sous son point de départ. Aucune mesure de
performance ou d'exploitabilité n'est ajoutée.

## 4. Pondération par grappe

Les statistiques « grappe » de `PHASE11C_HORIZON_METRICS.csv` sont
la médiane intra-grappe des événements puis les quantiles entre
grappes, calculées avec les `grappe_id` de la carte PHASE 11-B.1
(jointure du moteur sur la carte ; aucun recalcul de clustering —
vérifié : 2 617 / 597 grappes distinctes dans les trajectoires,
dont 2 614 / 594 parmi les complets, 3 grappes par population ne
contenant que l'événement censuré). Différences événement vs
grappe, faibles et sans changement de conclusion : H1 MFE t+8
32,88 vs 32,60 bp, clôture −2,24 vs −4,20 bp ; H4 65,22 vs 64,72 bp,
clôture −4,64 vs −6,65 bp. Les grappes étant petites (max 7
événements H1, 4 H4), aucune domination par les grandes grappes
n'est observée.

## 5. Limites de preuve (conservées, registre inchangé)

Absence d'artefacts traçables des tests synthétiques 11-C ;
anomalie du job historique de synthèse Phase 10 pouvant échouer à
son commit lors des runs 11-C (sans effet sur les livrables 11-C) ;
3 censures H1 et 3 H4 ; corpus IS 2010–2020 uniquement, aucune
validation indépendante sur holdout (jamais accédé) ; aucune
démonstration d'exploitabilité économique. Aucune anomalie n'est
supprimée du registre.

## 6. Verdict et procès-verbal

Aucune incohérence numérique non expliquée : tous les pourcentages
communiqués sont retrouvés à l'arrondi près à partir des effectifs
entiers des livrables, avec dénominateurs explicites et écart
produit/archétype expliqué événement par événement.

**Verdict : `RECONCILIATION_CONFORME`.** Les résultats de la Phase
11-C sont gelés en l'état à compter du présent addendum. Résultat
machine-readable : `PHASE11C_RECONCILIATION.json`. Checkpoint
chaîné seq307 ; empreintes des deux livrables dans la chaîne ;
commit distant et arbre vérifiés (voir le commit associé).
