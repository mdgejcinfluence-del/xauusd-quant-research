# PHASE 21-C — RAPPORT FINAL : ANATOMIE INTRAJOURNALIÈRE DES GRANDES AMPLITUDES D1

Statut : `EXPLORATORY_POST_HOC`. 1 992 journées complètes décomposées en 6 tranches H4 (artefacts 20-A/21-A).
Verdicts au registre seq377.

## 1. À quel moment les grandes amplitudes se construisent-elles ?

Construction graduelle, stable sur toutes les années et les deux sous-périodes (fraction médiane du range
final) : **31 % à 04:00, 47 % à 08:00, 63 % à 12:00, ~100 % (médiane) à 16:00**, puis extensions rares
(nouveaux extrêmes en tranche 6 : ~9 % des journées seulement). Le plus fort incrément médian survient en
**tranche 4 (12:00–16:00 UTC)** : range cumulé médian 68 → 103 bp. Ni purement précoce ni purement tardive :
l'amplitude se construit toute la journée, avec un pic de construction en début d'après-midi UTC
(cohérent avec le créneau 12:00 déjà le plus ample en 20-A).

## 2. Amplitude supplémentaire après un premier passage

Après le passage de 60 bp, le range additionnel médian décroît mécaniquement avec le temps restant :
90 bp (passage tranche 1) → 61 (T2) → 36 (T3) → 4 (T4) → 0 (T5). Le test précoce vs tardif (+75,5 bp,
q≈0) reflète d'abord le nombre de barres restantes — effet en partie mécanique, **pas un candidat**.
Après 100 bp atteint en tranche 4 (cas le plus fréquent, n=601), le range additionnel médian est 0 bp :
l'amplitude est le plus souvent constituée à 16:00.

## 3. Nouveaux extrêmes : prolongés ou opposés ?

Les deux. Après un nouvel extrême (tranches 2–5) comparé à l'absence d'extrême, les excursions futures
vers le haut **et** vers le bas sont toutes significativement plus grandes (+9,6 à +14,4 bp, q≈0,
bootstrap par semaines ISO, 10 000 réplications) alors que le déplacement terminal est nul
(+0,0/−2,2 bp, q 0,42–0,99). Un nouvel extrême signale donc une **amplitude qui continue de s'étendre
dans les deux directions**, pas une continuation directionnelle : le même extrême et l'extrême opposé
s'étendent conjointement. Ni `D1_FIRST_EXTREME_CONTINUATION_CANDIDATE` ni
`D1_OPPOSITE_EXTREME_EXPANSION_CANDIDATE` directionnel ne sont attribués.

## 4. Direction partielle vs déplacement restant

Aucune asymétrie : aux passages 60/100 bp, PARTIAL_POSITIVE vs PARTIAL_NEGATIVE — terminal aligné
−2,2/−1,1 bp (q 0,69/0,85), asymétrie favorable−adverse non significative après BH (q 0,086/0,38).
Le signe du déplacement partiel connu à une clôture H4 n'informe pas le déplacement restant.

## 5. Structures justifiant une recherche économique distincte

Aucune structure directionnelle. Seule subsiste, à tous les niveaux (H4 20-A, D1 21-A/21-B, intrajournalier
21-C), une **mémoire d'amplitude symétrique**. Les ordres d'extrêmes finaux sont équilibrés
(High d'abord 916, Low d'abord 932, même barre 144 — anatomie rétrospective uniquement).

## Verdicts

- **`D1_AMPLITUDE_WITHOUT_DIRECTION`** (principal, tous horizons intrajournaliers).
- Anatomie descriptive stable : construction maximale en tranche 12:00–16:00 UTC (`LATE_RANGE_EXPANSION`
  relatif, descriptif uniquement, non testé comme candidat).
- Aucun candidat de continuation/opposition/premier passage directionnel. Aucun edge, aucun P&L,
  aucune stratégie construite automatiquement.
