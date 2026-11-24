# PHASE 21-D — RAPPORT FINAL : ANATOMIE TICK DES GRANDES AMPLITUDES D1

Statut : `EXPLORATORY_POST_HOC`. 224 360 143 ticks IS traités en CI (8 lots Kaggle), reconstruisant
**1 989 journées** certifiées 21-A (3 journées scindées entre deux lots exclues et documentées, jamais
fusionnées). Qualité : 0 doublon de timestamp, 0 bid>ask, 0 prix non positif ; gaps > 300 s présents
dans la majorité des journées (fermetures/pauses, cause non établie : `GAP_CAUSE_UNVERIFIED`), aucune
interpolation. Verdicts au registre seq379.

## 1. Ordre exact des extrêmes journaliers (rétrospectif uniquement)

Sur 1 989 journées : **LOW_FINAL_FIRST 1 006 / HIGH_FINAL_FIRST 983** — équilibre quasi parfait,
stable entre 2010-2015 (587/600) et 2016-2019 (413/373). Aucun extrême final ne précède
systématiquement l'autre. Médiane de ~194 records de High et ~198 records de Low par journée :
les extrêmes se construisent par très nombreux petits records successifs des deux côtés.

## 2. Extension après le premier passage

Après le passage de 30/60/100 bp, l'extrême déclencheur continue de s'étendre substantiellement
jusqu'à la fin de journée (médiane ~37–52 bp), mais l'extrême opposé s'étend aussi (médiane 0–15 bp
selon le seuil, distributions larges) et le déplacement terminal reste centré sur zéro
(−2,4 à +5,5 bp en médiane). Le range continue donc de croître des deux côtés après le franchissement.

## 3. Le côté déclencheur conserve-t-il un avantage ?

Non démontré. Famille préenregistrée de 36 tests (3 seuils × 4 horizons × extension déclencheur /
extension opposée / terminal aligné), bootstrap par grappes de semaines ISO (10 000 réplications,
graine 2115), BH q=0,05 : **aucun test significatif, q minimale = 0,137**. Les déclencheurs haut et bas
sont équilibrés (985/1 004 à 30 bp ; 870/1 005 à 60 bp ; 593/660 à 100 bp) et leurs comportements
futurs indiscernables.

## 4. Asymétrie tick ou expansion bidirectionnelle ?

Uniquement une **expansion bidirectionnelle**, désormais établie à la résolution tick : la granularité
fine confirme et clôt la limite de résolution de 21-C (ordre intra-barre inconnu) — l'ordre exact des
extrêmes est équilibré, les records alternent des deux côtés, le spread autour des passages est stable
(médiane ~2,3–2,5 bp avant/au/après, `REFERENCE_COST_UNVERIFIED` pour les références 4,0/4,5 bp).
Aucune asymétrie nouvelle n'émerge au niveau tick.

## Incidents corrigés avant interprétation

Échec mémoire de 2 lots (corrigé par ordinaux de jour), corruption de fragments CSV (basculés en
parquet), détection des records de Low (`diff<0`), exclusion documentée de 3 journées scindées, et
bug de suppression par étiquettes d'index après concaténation (16 journées récupérées). Tous les
chiffres ci-dessus proviennent de la version corrigée et reproduite localement.

## Verdicts

- `BIDIRECTIONAL_EXPANSION_CONFIRMED_DESCRIPTIVELY` (à la résolution tick).
- `NO_DIRECTIONAL_ASYMMETRY` (36/36 tests non significatifs).
- Aucun `TRIGGER_SIDE_EXTENSION_SUPPORTED` / `OPPOSITE_SIDE_EXTENSION_SUPPORTED`.
- Verdict global : **`TICK_LEVEL_AMPLITUDE_STRUCTURE_IDENTIFIED_BIDIRECTIONAL_ONLY`**.

Aucun edge, aucun entraînement ni stratégie automatique à la suite de cette phase.
