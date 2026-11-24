# PHASE 24-A — RÉCONCILIATION DES PREUVES ANTÉRIEURES

| Élément | Type | Résultat gelé |
|---|---|---|
| 12-B M1 H1 (F10-01) | Prédictif historique | Brier 0,185→0,165, AUC 0,694 ; `PREDICTIVE_SIGNAL_SUPPORTED_HISTORICALLY`. Train 2010-2015 (1 640), calibration 2016-2017 (507), évaluation 2018-2019 (543) |
| 12-C.2 holdout | Confirmation historique | Brier 0,148, AUC 0,742 — **holdout consommée, fermée définitivement** |
| 13-B (règles entrée/sortie Phase 13) | Économique | Net ≈ +0,11 bp (S0) à −1,89 bp (S2) ; `ECONOMICALLY_INCONCLUSIVE_EXPLORATORY_IS` : **le signal M1 n'a jamais produit d'économie démontrée** |
| 20-A/20-B | Descriptif + interaction testée | Amplitude H4 conditionnelle réelle ; **20-B : le régime H4 n'améliore pas la capture économique de M1** (`H4_REGIME_DOES_NOT_IMPROVE_M1_CAPTURE`) |
| 20-C | Interaction testée | Aucune asymétrie directionnelle des barres d'expansion (`H4_NO_DIRECTIONAL_ASYMMETRY_SUPPORTED`) |
| 21-A/21-C | Descriptif d'amplitude | Mémoire d'amplitude D1 (autocorrélation du range ≈ 0,34) ; construction intrajournalière progressive ; anomalies d'amplitude bidirectionnelles uniquement |
| 23-C | Événementiel | FOMC = régime d'amplitude (`FOMC_VOLATILITY_ONLY`), continuation post-15 = 52 % |
| M1 — composition | Fait structurel | Le dictionnaire M1 contient **SESSION_REINTEGRATION** (4 indicatrices, référence ASIA) : le M1 historique mélange déjà une information d'horloge catégorielle |

Interactions déjà testées (à ne pas redécouvrir) : régime H4 × capture M1 (20-B), régimes
d'amplitude × direction (20-C, 21-D, 21-B), multiples architectures archivées (22-A/22-B).
**Nouveauté réelle de 24-A** : uniquement l'idée d'un *réentraînement conditionnel* du Chauffeur
sur les seuls événements autorisés par un Directeur et l'Horloge — jamais testée. L'architecture
proposée n'est en aucun cas déjà validée ; l'échec économique de Phase 13 et le résultat nul de
Phase 20-B sont les références à battre, sur cohortes communes.
