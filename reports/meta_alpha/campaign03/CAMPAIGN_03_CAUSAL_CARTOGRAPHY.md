# CAMPAGNE 3 — CARTOGRAPHIE CAUSALE IMPULSIONS / CONSOLIDATIONS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE. CAMPAGNE
EXÉCUTÉE** sur autorisation propriétaire (seq 188), dictionnaire gelé
seq 185–186 (sha256 `76490c40…`), 12 comparaisons gelées seq 189
(`CAMPAIGN_03_COMPARISONS_FREEZE.md`, sha256 `ac151cb8…`). Aucun backtest,
aucun `challenge_sim`, aucune optimisation, aucune promotion J2/J3, holdout
scellé, flux prospectif T0 jamais touché, FRED suspendue, 36 cellules S12
intactes. **Aucune comparaison n'a été ajoutée après consultation des
résultats** ; les lectures ci-dessous appliquent mécaniquement la règle gelée
(suffisance, seuil matériel, q BY sur les 12, cohérence de signe par ère),
avec les décisions de lecture documentées au registre.

## 1. Couverture et validation temporelle

- Extraction CI séquentielle à commit unique : **282/282 partitions**,
  3 540 993 barres M1, 702 397 barres M5, 231 875 barres M15 (barres
  complètes uniquement), 3 097 dates UTC présentes dans le corpus, période
  2010–2019 (IS déjà consulté). Garde d'intégrité satisfaite.
- Validation temporelle **avant calcul**, tests synthétiques verts
  (`ci_tools/campaign03_temporal_tests.py`, rejoués en CI avant extraction) :
  seuil IMP = quantile 90 de |r| sur **[T0 − 60 jours calendaires, T0)**, barre
  courante exclue, minimum 2 000 barres ; seuil CONS = 0,5 × médiane poolée
  des ranges M1 des **5 journées de cotation précédentes**, jour courant
  exclu, minimum 1 000 barres ; variables d'instantané closes à
  l'instantané ; conséquences strictement postérieures.
- Unités d'instantanés, jamais mélangées : IMP-M5 T0/+1/+3/+6/+12 barres =
  0/+5/+15/+30/+60 min ; IMP-M15 = 0/+15/+45/+90/+180 min ; CONS = 0/+3/+6/+12
  min. Zones d'amorçage publiées : 2 000 premières barres de chaque famille
  IMP sans seuil (par construction), 1 journée CONS sans seuil.
- Épisodes : **IMP-M5 70 493**, **IMP-M15 23 075**, **CONS 15 973**.
  Chevauchements comptés, jamais supprimés : 57 401 épisodes IMP-M5 (81 %)
  et 12 724 IMP-M15 (55 %) se déclenchent dans la fenêtre d'issue d'un
  épisode précédent ; toutes les inférences utilisent le bootstrap par
  journées (2 000 répétitions, graine 20261113) et les effectifs bruts comme
  indépendants (journées) sont publiés côte à côte.

## 2. Anatomie des impulsions (issues mesurées, jamais des anticipations)

Classes de trajectoires sur (T0, T0+60 min], définitions exclusives gelées :

| Classe | IMP-M5 | IMP-M15 |
|---|---|---|
| Continuation (extension à 2A ≤ 30 min) | 37,5 % | 22,7 % |
| Retournement (retracement 100 % puis excursion opposée ≥ 0,5A) | 31,5 % | 15,9 % |
| Retracement complet (100 %, excursion opposée < 0,5A) | 13,3 % | 14,1 % |
| Retracement partiel (50 % sans 100 % ni extension) | 8,5 % | 21,6 % |
| Extension tardive (2A après 30 min) | 5,9 % | 9,5 % |
| Stagnation (ni 50 % ni 2A) | 2,7 % | 14,8 % |
| Censurée (fenêtre tronquée par la fin de journée) | 0,7 % | 1,4 % |

Lecture descriptive : à horizon d'une heure, une impulsion M5 se resorbe
entièrement (retracement complet + retournement) dans ~45 % des cas et
n'atteint le doublement d'amplitude que dans ~43 % — **la continuation n'est
pas le cas par défaut**, contrairement au présupposé interdit, et la
stagnation est rare en M5 (2,7 %) mais fréquente en M15 (14,8 %). Le
retracement maximal déjà atteint croît mécaniquement avec l'instantané
(médiane M5 : 14,1 bp à T0 → 26,4 bp à +12 barres) pendant que le retracement
ultérieur médian décroît (13,0 → 11,2 bp) et que l'extension supplémentaire
médiane s'éteint (12,2 → 5,4 bp) : l'essentiel du devenir d'une impulsion se
joue tôt, sans que rien, à ce stade descriptif, ne dise ce qui était
connaissable à T0 au-delà des variables d'instantané publiées.

## 3. Anatomie des consolidations (aucune expansion présupposée)

Issues de formation (6 barres calmes sous seuil causal) : sortie par
**clôture hors du range cumulé 87,1 %**, par barre de range > 2× le range de
formation 12,3 %, **censurée à +120 min 0,6 %**. Durée médiane 8 minutes. Le
range cumulé médian passe de 1,46 bp à la formation à 4,75 bp à +12 min
(ratio de compression 0,69 → 2,27) : la « consolidation » ainsi définie est
un état bref et fragile, et le range des 60 minutes suivant la sortie
(médiane 11,8 bp) ne diffère pas, au seuil matériel gelé, selon le type de
sortie (C3-10, ratio 0,91) — **l'expansion post-consolidation n'est pas un
fait descriptif établi de cette campagne**.

## 4. Les 12 comparaisons gelées — résultats complets

Détail chiffré : `CAMPAIGN_03_COMPARISONS.csv` (n et journées par bras,
estimations, différences, IC95 par bootstrap-journées, p brutes, q BY,
suffisance, lecture mécanique). Synthèse :

- **3 candidates J1** (q BY < 0,05, seuil matériel atteint, signe cohérent
  dans les 3 ères) : ANO-C3-001 (retracement complet M5, Londres > Asie,
  +7,2 pts [6,0 ; 8,3]) ; ANO-C3-002 (retracement ultérieur après +12 barres
  plus faible pour amplitude initiale causale basse, ratio 0,81) ;
  ANO-C3-003 (sorties CONS par barre de range plus fréquentes à petit range
  de formation, +13,3 pts — **avec avertissement de mécanique de
  construction** : un petit range abaisse le seuil de déclenchement de
  sortie ; voir registre).
- **3 significatives sous le seuil matériel** (conservées, non fichées) :
  C3-01 (−1,3 pt par direction), C3-08 (+4,0 pts session M15), C3-10
  (ratio 0,91 par type de sortie).
- **6 négatives ou non concluantes**, toutes conservées au registre
  (NEG-C3-001 à NEG-C3-009, incluant le contraste d'ère C3-05 reclassé
  contraste de contexte : une ère n'est pas une condition observable à T0).
- Aucune fiche n'est promue ; les candidates sont **J1 descriptives**, au
  catalogue commun, sans mécanisme inventé et sans exigence de ressemblance
  avec ANO-C1/C2.

## 5. Livrables

`CAMPAIGN_03_EVENT_METRICS.csv` (distributions par famille, trajectoire,
session, ère, direction, type de sortie), `CAMPAIGN_03_SNAPSHOT_STATS.csv`
(anatomies par instantané et contexte prédéfini : session, ère, régime F3),
`CAMPAIGN_03_COMPARISONS.csv`, `CAMPAIGN_03_ANOMALY_REGISTER.csv` (3
candidates J1 + 9 négatifs documentés), `CAMPAIGN_03_DATA_QUALITY.md`,
bruts gzip `CAMPAIGN_03_EPISODES_*.csv.gz` / `CAMPAIGN_03_SNAPSHOTS_*.csv.gz`,
journal `CI_LOG.txt`, couverture `C3_COVERAGE.json`.

**STATUT : CAMPAGNE 3 EXÉCUTÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
La suite de l'exploration générale (familles du plan de reprise seq 183)
reste à ordonner séparément ; la confirmation T0 demeure un chantier
parallèle indépendant, non activé par la présente livraison.
