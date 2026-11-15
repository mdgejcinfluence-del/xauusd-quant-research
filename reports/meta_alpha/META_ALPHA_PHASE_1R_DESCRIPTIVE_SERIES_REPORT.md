# META ALPHA — PHASE 1R (tâche 1) : RAPPORT DES SÉRIES DESCRIPTIVES GRANULÉES

Cadre: protocole FINAL (commit 2fcb775 + gouvernance multiplicité ba9195e).
Préenregistrement verrouillé AVANT calcul (chaîne seq 6-7, tête fb65b4f2…):
`phase1r/PHASE_1R_PREREG.json`. Exécution distante: run **43752027483, succès
en 2 h 25 min 53 s**, GitHub Actions CPU, 0 Fcfa. Le workflow a vérifié la
chaîne du registre avant tout calcul.
Partitions lues: les **282 partitions IS** uniquement (288 086 588 ticks).
Aucun OOS, aucun Holdout, corpus intact (lecture seule).

## Séries construites (846 lignes partition x granularité; séries mensuelles jointes)
| Granularité | Barres totales | Volatilité médiane/barre | Spread moyen | Intensité médiane |
|---|---:|---:|---:|---:|
| G_EVT100 (100 événements) | 2 897 878 | 3,6 bp | 3,9 bp | 1,07 év/s |
| G_ACT500 (500 mises à jour) | 596 616 | 8,1 bp | 4,0 bp | 0,92 év/s |
| G_VOL10bp (budget |r| cumulé 10 bp) | 4 386 997 | 2,3 bp | 3,9 bp | 1,23 év/s |
Règles tenues: aucune barre ne franchit un gap > 60 s; aucune interpolation;
aucun OHLC; ordre = observation_id certifié. Livrables: PARTITION_GRANULARITY.csv
(quantiles par partition), MONTHLY_SERIES.csv (séries mensuelles par granularité),
STATE.json (checkpoints), hashes au §5.

## Résultat descriptif central: l'autocorrélation dépend de l'échelle — et disparaît
Famille préenregistrée (m=3, BY + stabilité): autocorrélation lag-1 des rendements
de barres, médiane des partitions, IC95 par bootstrap (blocs=partitions, graine 7):
| Granularité | ac1 médiane | IC95 | Par tiers (T1/T2/T3) | Statut |
|---|---:|---|---|---|
| G_EVT100 | -0,0003 | [-0,005; +0,006] | +0,010 / -0,005 / -0,009 | nul, aucun signal |
| G_ACT500 | -0,017 | [-0,026; -0,011] | -0,019 / -0,011 / -0,020 | négatif faible, stable |
| G_VOL10bp | -0,112 | [-0,134; -0,067] | **-0,152 / -0,005 / +0,001** | **instable: NON CONCLUANT** |
Lecture: l'autocorrélation tick spectaculaire (0,487, ANOM-001) **s'éteint dès
l'échelle de 100 événements** — elle vit à l'échelle du tick individuel, pas à
celle des barres. L'autocorrélation négative des barres de volatilité est
forte en T1 puis s'effondre (artefact probable du découpage par budget de
volatilité + retour à la moyenne à cette échelle): elle échoue au critère de
stabilité préenregistré et est classée NON CONCLUANTE, pas anomalie.
Parts d'événements: bid-seul ≈ ask-seul ≈ 0,59% à toutes les granularités
(confirmant la réfutation du mécanisme ANOM-001).

## Contrôles de qualité
Chaîne de registre vérifiée avant calcul (workflow); 282/282 partitions sans
erreur; barres jamais traversantes de gaps (construction par segments);
cohérence des comptes (barres x tailles vs ticks par construction).

## Limites
Médianes de partitions (pas de pooled tick-à-tick); bootstrap par partitions
(approximation des blocs mensuels préenregistrés, écart documenté);
G_VOL10bp définie par budget cumulé (découpage en quantiles de variation,
pas en franchissement événementiel exact); sélection cumulative permanente
(148 tests + vagues descriptives) — statut maximal atteint ici: **exploration
descriptive**; même le résultat stable G_ACT500 (-0,017) est économiquement
minuscule et ne constitue ni une découverte candidate promue, ni un signal.

## Conclusion de la tâche 1
Les séries existent, sont traçables et reproductibles (code + préenregistrement
+ hashes). Elles montrent que la structure ANOM-001 est un phénomène d'échelle
tick qui ne survit pas à l'agrégation — fait descriptif nouveau et utile.
Aucune anomalie candidate n'est déclarée à l'issue de cette tâche; aucune
hypothèse n'est créée. ARRÊT conformément à l'autorisation: la suite exige une
décision explicite du propriétaire.

## 5. Hashes SHA-256 (calculés au commit)
Voir empreintes jointes au commit de ce rapport: moteur ci_tools/phase1r_series.py,
PARTITION_GRANULARITY.csv, MONTHLY_SERIES.csv, PHASE_1R_PREREG.json.
049f238c7acd5f5e33f51f894bcc5120329bb48534398e6196f7cd93e31023e7  ci_tools/phase1r_series.py
df08a6ba002a04c0d27a14ea4762d10b7082a035984713ccd28fee946e785626  reports/meta_alpha/phase1r/PARTITION_GRANULARITY.csv
de97a9a06f62c1cfcdfa2bdb6a0642c3fd8bf22357279d49169f0068542871d0  reports/meta_alpha/phase1r/MONTHLY_SERIES.csv
ddd09ef3c0ed46e540b1930162a4b9262f69fd961a118e5f3f9fa32ca58fff1f  reports/meta_alpha/phase1r/PHASE_1R_PREREG.json
