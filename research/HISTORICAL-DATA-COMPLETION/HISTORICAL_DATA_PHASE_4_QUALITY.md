# PHASE 4 — NORMALISATION ET QUALITÉ

Corpus certifié 348 partitions : schéma historique inchangé (deux signatures documentées,
Bid/Ask/volumes séparés, `observation_id` continu) — aucune réécriture. Lots de complétion :
schéma `ts/bid/ask/source/spread`, contrôles exécutés à l'ingestion (`bid_lt_ask_violations = 0`,
timestamps croissants, doublons supprimés sur `ts`, source `DUKASCOPY_PRIMARY` par ligne),
SHA-256 par lot au manifeste. Aucune suppression destructive ; les heures en échec restent des
trous documentés, distincts des week-ends (fermetures normales vendredi→dimanche, Phase 0 §8).
Réponses au rapport final : (1) 685 118 625 ticks certifiés + 3 942 897 de complétion vérifiée ;
(2) 2010-01-04 → 2026-09-30 certifié, complétion 2026Q4 en cours vers le 2026-11-26 ;
(3) Bid/Ask 100 % des ticks ; (4) unique lacune : heures 2026Q4 non encore servies (503) ;
(5-6) complété : lots 2026-10/11 partiels, source Dukascopy uniquement ; (7) qualité contrôlée
par lot ; (8) partitions certifiées intégralement inventoriées, complétion partielle assumée ;
(9) Kaggle : lots IS/HO existants + dataset de complétion créé ; (10) coûts paramétrables oui
(Phase 5) ; (11) replay prêt et prouvé mécaniquement (Phase 6) ; (12) dépendance restante :
patience fournisseur (relances) — aucun compte, aucun achat ; (13) mission de réplication
distincte : possible dès sa spécification préenregistrée, sur IS et descriptif récent cadré.
