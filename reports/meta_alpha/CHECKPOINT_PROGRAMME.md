# CHECKPOINT MAÎTRE — PROGRAMME META ALPHA XAUUSD DGP
Mis à jour automatiquement à chaque gate. Source de vérité de reprise.

- Autorisation: AUTORISATION GÉNÉRALE DE LANCEMENT (propriétaire, 13 nov. 2026)
- Interdits permanents: dépense, modification du corpus, ordres réels, optimisation Holdout.
- Holdout: SCELLÉ (ouverture unique réservée à l'évaluation finale préenregistrée).

| Phase | Statut | Preuve / checkpoint |
|---|---|---|
| P1 Corpus certifié | CERTIFIED (hérité, jamais reconstruit) | BASELINE_HASH_MANIFEST.json |
| P2 Inventaire 348 | CERTIFIED — COMPATIBLE SOUS CONDITIONS | RAPPORT_INVENTAIRE_348_EXHAUSTIF.md (ebd0ff1) |
| P2 Moteur L2-L4 (mesures par partition) | EN COURS — reprise depuis partition 002 (001 déjà faite) | phase2/STATE.json, phase2/PARTITION_MEASURES.csv |
| P2 Variables certifiées | 5/11 variables, 22 entrées SQL | RAPPORT_CONSOLIDE_PHASE2_V1.md |
| P2 Variables bloquées | ZSCORE_ROBUST, SPREAD_REGIME, REGIME_CLASS (traductions étagées), SUBPERIODE (sessions non documentées), MFE_H/MAE_H (convention direction) | motifs dans les rapports |
| P3 Exploration anomalies | EN ATTENTE du gate P2 mesures | préenregistrement obligatoire au Trial Ledger avant tout test |
| P4 Candidats déterministes | EN ATTENTE P3 | — |
| P5 Robustesse/coûts | EN ATTENTE P4 | coûts: GROSS/CONDITIONAL, jamais NET |
| P6 Qualification indépendante | EN ATTENTE P5 | IS/OOS calendaires, purge ≥ 1 h |
| P7 Portefeuille | EN ATTENTE P6 | NO_EDGE reste un résultat valide |
| P8 Holdout (évaluation finale) | SCELLÉ — autorisation distincte requise selon la passation | sceau à ouverture unique |
| P9 Robot (non réel) | EN ATTENTE P7/P8 | aucun ordre réel autorisé |

Conditions techniques permanentes (inventaire ebd0ff1): lecture des colonnes PAR NOM;
union_by_name=true pour tout glob multi-fichiers DuckDB; volumes jamais interprétés
comme volume de transactions; vérification de signature avant calcul.
