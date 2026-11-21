# CAMPAGNE 5 — DOSSIER DE CLÔTURE (descriptif)

Exécution descriptive autorisée par le fondateur (seq220), gel chaîné
seq221 (V2 `818837fd…8331`, V2.1 `509a2863…bd45`, V2.2 `4ce1ee9b…1b0e`),
résultat chaîné seq222. Deux runs CI : 44892050419 (bug d'initialisation
des niveaux journaliers, atteintes à zéro — incident documenté, aucune
sortie F-F journalière de ce run utilisée) puis 44892455679 corrigé et
complet (282/282 partitions, 3 540 993 barres M1, 2 572 journées
utilisables, 10 288 ouvertures, 2 375 atteintes journalières, 504 lignes
d'atteintes hebdomadaires).

## Verdict des dix comparaisons gelées

| ID | Lecture | Fiche |
|---|---|---|
| C5-01 | CANDIDATE_J1 — ratio 1,189 [1,148 ; 1,236], q BY 0,0042 | ANO-C5-001 |
| C5-02 | NÉGATIF — +2,24 pts [−0,45 ; +4,89], q 0,281 | — |
| C5-03 | NON ÉLIGIBLE — bras TROU 2 initiaux, 0 éligible (retards gelés) | — |
| C5-04 | NÉGATIF — ratio 0,912 [0,857 ; 1,000], q 0,217 | — |
| C5-05 | NÉGATIF — ratio 1,002 [0,990 ; 1,014], q 1,000 | — |
| C5-06 | CANDIDATE_J1 — +8,08 pts [+3,80 ; +12,59], q BY 0,0029 | ANO-C5-002 |
| C5-07 | NÉGATIF — ratio 0,916 [0,807 ; 1,050], q 0,891 | — |
| C5-08 | CANDIDATE_J1 — ratio 0,615 [0,538 ; 0,732], q BY 0,0029, avertissement de composition | ANO-C5-003 |
| C5-09 | NON ÉLIGIBLE — 106/81 atteintes réelles (<200 gelés), différence dégénérée 0 | — |
| C5-10 | NÉGATIF dégénéré — 0 journée CONTENUE ETABLIE (1 440/1 440) sur aucune ère | — |

Trois candidates J1 au catalogue commun (ANO-C5-001/002/003), sans
promotion automatique, sans priorité, sans J2/J3. Aucune association
descriptive n'est une preuve prédictive ni une opportunité exploitable.

## Livrables
1. `CAMPAIGN_05_REPORT_FE.md` — rapport famille F-E.
2. `CAMPAIGN_05_REPORT_FF.md` — rapport famille F-F.
3. `CAMPAIGN_05_COMPARISONS.csv` — tableau consolidé des dix
   (effectifs, grappes, effets, IC, p brutes, q BY par famille,
   matérialités, lectures).
4. `CAMPAIGN_05_ANOMALY_CATALOG.md` — catalogue ANO-C5-001..003.
5. `CAMPAIGN_05_CENSURE_REGISTRY.md` — censures et données manquantes.
6. `CAMPAIGN_05_QUALITY_COVERAGE_DIAGNOSTICS.md` — qualité/couverture.
7. `CAMPAIGN_05_INCIDENTS_LIMITS_COSTS.md` — incidents, limites, coûts.
8. Présent dossier — hashes, checkpoint, vérification de chaîne.

## Hashes SHA-256 (extraits)
- `CAMPAIGN_05_COMPARISONS.csv` : `0db427a9f4421826a4335456ab4499e81d9dc8c446698aceb311396fec4bfd3f`
- `C5_COVERAGE.json` : `54a365e0ce6b9e126c0ea3adf80b41b63cd509d64cea48045f716db6af48579d`
- `CAMPAIGN_05_OPENINGS.csv.gz` : `682c83a45ee26adf24242cf7043989e0dd6ff1cce86577c8f807b2288025ff67`
- `CAMPAIGN_05_ATTEINTES_JOUR.csv.gz` : `33ca0704bf4fac2348a8fda7c73f6de24477f927fbc282abab7d07ea20c1b2e7`
- `CAMPAIGN_05_ATTEINTES_SEMAINE.csv` : `d628dd3ccc9e5713166c0cba9cf4b6f24103cac9feed637836857ff10d15c9e5`
- `CAMPAIGN_05_REPORT_FE.md` : `d1e486315d229966fbd6b7742c583fdda8767dca9b79533d89132aed04da481f`
- `CAMPAIGN_05_REPORT_FF.md` : `af42fd8d8951757fb8ba88001254ef5bb9556c92d0772477a6b4e0a2d8f7f85e`
- `CAMPAIGN_05_ANOMALY_CATALOG.md` : `e4b45596ae7b0787261947fd8db40c2ba5a128742e943ae83bf595a14442db22`
- `CAMPAIGN_05_CENSURE_REGISTRY.md` : `e37f139d9aabad5fcb73c31e901446ff3eb42a842d200abd261278b1c95ea98b`
- Moteur : `c364dfeca9a4d6b50fedfbf2e1d83f84101294b618526c9bd92d13e259b48d9b` ; synthèse : `71021545d74732ba233876a020726311616504fcc996558e75c7a60ba5ea887a`

Budgets expérimentaux inchangés, aucun consommé ; holdout scellé ;
aucune fiche des campagnes 0–4 modifiée. **Campagne 5 close au
descriptif.**
