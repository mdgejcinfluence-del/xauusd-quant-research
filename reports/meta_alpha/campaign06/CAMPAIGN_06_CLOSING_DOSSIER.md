# CAMPAGNE 6 — DOSSIER DE CLÔTURE F-G (descriptif)

Exécution autorisée par le propriétaire (seq241), protocole gelé
seq239 confirmé avant extraction (seq242), résultat chaîné seq243.
Un seul run CI, complet du premier coup : 282/282 partitions,
3 540 993 barres M1, 3 097 journées présentes, 2 772 éligibles de
forme, 325 censurées, validation temporelle 15/15 verte avant calcul.

## Verdict des cinq comparaisons gelées

| ID | Lecture finale | Effet | q BY (m=5) |
|---|---|---|---|
| C6-01 | **NON ÉLIGIBLE** — bras « j−1 directionnel » : 10 paires (classe directionnelle quasi vide à fréquence minute : 14 journées/2 772) ; contrôle par blocs FRAGILE_SIGNE, sans effet sur la lecture | −0,0007 [−0,0220 ; +0,0215] | 1,000 |
| C6-02 | **SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL** — pas de candidate ; déclassement non déclenché (condition \|ΔER\| ≥ 0,05 non remplie) | +0,0208 [+0,0169 ; +0,0241] | 0,0057 |
| C6-03 | NÉGATIF | −0,0018 | 1,000 |
| C6-04 | NÉGATIF — τ quasi identique selon le signe (771 vs 775 min) | −4 min | 1,000 |
| C6-05 | NÉGATIF | −0,0027 | 0,588 |

**Aucune candidate J1 issue de la Campagne 6** (catalogue ANO vide,
publié comme tel). Fait descriptif central : à granularité minute,
les journées XAU/USD sont massivement oscillantes au sens du
protocole (efficience médiane 0,0297, sinuosité médiane ~15,3).
Aucune promotion automatique ; toute suite (autre granularité,
mécanisme) exigerait un nouveau protocole et un ordre distinct.

## Livrables
1. `CAMPAIGN_06_REPORT.md` — rapport scientifique complet et résultats
   détaillés C6-01..C6-05.
2. `CAMPAIGN_06_COMPARISONS.csv` — tableau consolidé des cinq
   (effectifs, grappes, effets, IC, p, q BY m=5, matérialité, lectures).
3. `CAMPAIGN_06_ANOMALY_CATALOG.md` — catalogue : aucune candidate.
4. `CAMPAIGN_06_COVERAGE_DIAGNOSTICS.md` — couverture et qualité.
5. `CAMPAIGN_06_BOOTSTRAP_BY_DETAILS.md` — contrôles bootstrap, blocs
   C6-01, déclassement C6-02, BY.
6. `CAMPAIGN_06_INCIDENTS_LIMITS.md` — incidents (aucun) et limitations.
7. Présent dossier — hashes, checkpoint, chaîne.

## Hashes SHA-256 (extraits)
- `CAMPAIGN_06_COMPARISONS.csv` : `bff3b79e37ca741655b0e498ef6fab5b2cc1c4f41c85f8b2ea1a73ce536bd7fa`
- `CAMPAIGN_06_DAYS.csv` : `4877bad9a89e64e5a3e4b9426f93b78b354d432d2ac691dd15dc56a3708fe32f`
- `CAMPAIGN_06_PAIRES_C6_01.csv` : `e2ea41d219aeb94acb7d16764973529251ec485659fc04f3d5c29a44656dac6a`
- `C6_COVERAGE.json` : `53367f620598ce099c2a347b7f91cc7c66782723a6aff0b29506b967d5b47647`
- `CAMPAIGN_06_REPORT.md` : `152c31d1b324da63fa26963a2b344cb4f79b100e57c53900ed406aca6c208207`
- `CAMPAIGN_06_ANOMALY_CATALOG.md` : `de0430ddd52d6be7fca726e970453807f7aba31e4eef5ee59b49fe6e9b5519d1`
- Moteur : `2d40df51bb2f26c5d50bf207c2c3e30b25e9e35626d215a9f1479c07eb278e71` ; synthèse : `0404fe05474750ae21a69981d45a899eaab164ab5c76726265fea614b96cf87c`

Budgets expérimentaux inchangés, aucun consommé ; holdout scellé ;
aucune fiche historique modifiée ; aucun backtest ni `challenge_sim` ;
aucun J2/J3. **Campagne 6 close au descriptif.**
