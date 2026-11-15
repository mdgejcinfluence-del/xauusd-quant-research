# RAPPORT PHASE 0 — Documentation et hygiène du corpus (lecture seule)

Périmètre de ce balayage: **282 partitions IS** (2010-01-04 -> 2020-01-20), 288 086 588
ticks. Aucune donnée Holdout lue par cette phase; les chiffres corpus complet (348)
proviennent des mesures Phase 2 déjà figées. Corpus jamais modifié.
Exécutions: run 43722302113 (succès, mais livrable CSV tronqué par un bug de
descripteur — voir Incohérences), puis run 43733297346 (succès 1 h 59, livrable complet).

## 1. Réconciliation des chiffres
- IS: 282 partitions, 288 086 588 ticks (cohérent avec l'inventaire exhaustif).
- Corpus: 348 partitions, 685 118 625 ticks, écart 0 vs certificat (déjà figé).

## 2. Interruptions (gaps > 60 s): 27 463 sur IS — liste exhaustive dans GAPS_IS.csv
| Classe (règle documentée) | Effectif |
|---|---:|
| Intraday courte (<= 1 h) | 25 447 |
| Longue hors week-end (1-4 h) | 1 460 |
| Fermeture calendaire week-end (> 12 h, ven/sam -> lun) | 495 |
| Fermeture longue autre (> 4 h) | 61 |
Durée médiane 70 s; p95 = 1,0 h; max 76,5 h (jours fériés/réouvertures exceptionnelles).
La règle de classification est une convention documentée, pas une vérité de session:
les horaires de session restent NON documentés (SUBPERIODE toujours bloquée).

## 3. Intégrité des cotations (IS, 288M ticks)
| Contrôle | Résultat |
|---|---|
| Quotes croisées (ask < bid) | **0** |
| Quotes verrouillées (ask = bid) | **0** |
| Prix non positifs | **0** |
| Événements à timestamp dupliqué | **0** |
| spread_rel max observé | 0,00272 (27,2 bp) — extrême isolé, p99,9 max par partition 0,00152 |

## 4. Résolution et limites
- Horodatages: microseconde UTC (schéma certifié), aucun doublon IS.
- Prix: le plus petit écart positif de mid observé descend à ~1e-13, artefact de la
  représentation double des prix sources: il n'existe pas de quantum de prix propre
  déductible du mid stocké; toute analyse de "tick size" doit travailler sur bid/ask
  bruts avec tolérance explicite. Limite documentée, aucune correction appliquée.

## 5. Incohérences identifiées (dont une des nôtres)
1. **Bug de notre moteur Phase 0 (première exécution)**: les CSV ouverts en continu
   ont été remplacés par `git pull --rebase` lors des checkpoints; les écritures
   postérieures partaient dans un inode orphelin. Livrable tronqué à 20 partitions,
   archivé comme preuve (`*_INCOMPLET_20P.csv`), moteur corrigé (écritures
   ouverture/fermeture par partition), ré-exécution complète vérifiée ligne à ligne
   (282 lignes d'hygiène, 27 463 gaps uniques après déduplication des reprises).
2. Deux signatures de schéma (connues, K6): aucun impact sur ces contrôles (lecture par nom).
3. Aucune incohérence de cotation détectée sur IS (0 croisée, 0 verrouillée, 0 doublon).

## 6. Empreintes des livrables (SHA-256)
Voir les valeurs calculées au commit de ce rapport (fichiers ci-dessous).
- phase0/PARTITION_HYGIENE.csv, phase0/GAPS_IS.csv, ci_tools/phase0_hygiene.py.

## 7. Suite
Aucune phase suivante n'est commencée. Le protocole corrigé
(PROTOCOLE_EXECUTION_CORRIGE.md) définit l'ordre simulation -> réel, la matrice
d'accès IS/OOS/Holdout, les définitions T4, P1 et la règle des 270 cellules.
Autorisations requises: acceptation de ce rapport, puis Phase S (simulation) séparée.
795a2dc9cb048e4ed507b9edaecbcff026d209ce44bf8793ae56440eecfff433  reports/meta_alpha/phase0/PARTITION_HYGIENE.csv
72eeb2159e0db4e9a3cf88e39b61bcc3af9b3e171500c5c67ec9c21a1f3d6877  reports/meta_alpha/phase0/GAPS_IS.csv
15d2d9f860b3707b29d80a897c93216172c9c329b41fd36776d60ba6ab3ab190  ci_tools/phase0_hygiene.py
