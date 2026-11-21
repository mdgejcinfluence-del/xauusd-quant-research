# CAMPAGNE 7 — DOSSIER DE CLÔTURE F-I (descriptif)

Exécution autorisée par le propriétaire (seq251), protocole gelé
seq250 confirmé avant extraction (seq252), résultat chaîné seq253.
Deux runs CI : 44903810557 (marquage SIMULTANÉ erroné, épisodes
G50/R100 exclus à tort — aucune sortie utilisée) puis 44906521704
corrigé et complet (282/282, 3 540 993 barres M1, validation
temporelle 13/13 verte avant calcul).

## Verdict des cinq comparaisons gelées

| ID | Lecture finale | Effet | q BY (m=5) |
|---|---|---|---|
| I-01 | NÉGATIF (composition sensible, sans effet sur la lecture) | +1,84 pt [−1,23 ; +4,93] | 0,883 |
| I-02 | **NON ÉVALUABLE — COMPOSITION** (47–51 % d'épisodes sans strate comparable) | −0,29 pt [−6,54 ; +6,05] | 1,000 |
| I-03 | **ASSOCIATION SENSIBLE À LA COMPOSITION** — déclassée par le contrôle gelé, **pas de candidate** | ratio 1,449 [1,247 ; 1,695] | 0,0057 |
| I-04 | NÉGATIF | +1,88 pt [−1,05 ; +4,54] | 0,883 |
| I-05 | **NON ÉVALUABLE — COMPOSITION** (ère 2017–20 : 28,9 % sans strate comparable) | −0,98 pt [−7,61 ; +5,98] | 1,000 |

**Aucune candidate J1 issue de la Campagne 7.** Conclusion descriptive :
sous les définitions gelées, les nombres ronds ne forment pas une
famille de comportements distincte démontrée — franchissements
quasi identiques aux placebos (~89–92 % partout), rejet rare et non
évaluable, seul l'écart de distance post-franchissement (I-03) est
significatif et matériel, mais déclassé pour composition. Aucune
promotion automatique ; aucune preuve de mécanisme psychologique ni
de capturabilité.

## Livrables
1. `CAMPAIGN_07_REPORT.md` — rapport complet, résultats détaillés,
   comparaisons par anneau, exposition.
2. `CAMPAIGN_07_COMPARISONS.csv` — tableau consolidé des cinq.
3. `CAMPAIGN_07_ANOMALY_CATALOG.md` — catalogue : aucune candidate.
4. `CAMPAIGN_07_COVERAGE_DIAGNOSTICS.md` — couverture et censures.
5. `CAMPAIGN_07_INCIDENTS_LIMITS.md` — incidents (run 1 simultanéité,
   statut de composition en synthèse, lenteur bootstrap) et limites.
6. Présent dossier — hashes, checkpoint, chaîne.

## Hashes SHA-256 (extraits)
- `CAMPAIGN_07_COMPARISONS.csv` : `7ee21cf63838f5297577b8ea14376526ed1c7613730c77a108ea0228dc7c440f`
- `CAMPAIGN_07_EPISODES.csv.gz` : `9c352f2f32288e79da0ccb05b83e82ba4b9762a4994b7286b89b611c6788a18e`
- `C7_COVERAGE.json` : `ac458c174266850660912c208c90296d3d3d96ab6eab4ee370477d408efc0c51`
- `CAMPAIGN_07_REPORT.md` : `f308a733544c863ad331f8ef31c6f6243f028ba4f843bf0f1e9cdeba8de4336e`
- `CAMPAIGN_07_ANOMALY_CATALOG.md` : `c4dbd62ccf9e6d5df0b46e4c85229d40f5ff82e32492dd1a96e3303f5717c7eb`
- Moteur : `e12c23391894cbaf86cf0242708b17884961cb2f1815ae604735f16bcb085893` ; synthèse : `2d71fa1caf92c5cf5d24932daec4be1858ddffd7ac2b74199fefca9ae5a3a192`

Budgets expérimentaux inchangés, aucun consommé ; holdout scellé ;
aucune fiche historique modifiée ; aucun backtest ni `challenge_sim` ;
coquille cosmétique du protocole gelé laissée intacte. **Campagne 7
close au descriptif.**
