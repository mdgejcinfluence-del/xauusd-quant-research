# DATA RECOVERY — BLOCAGES ET LIMITES

1. **Partitions Drive** : aucun blocage résiduel (7/7 récupérées en CI via gdown ;
   le connecteur Drive seul plafonne à 100 Mo, d'où la voie CI, autorisée et déjà
   éprouvée dans ce dépôt).
2. **Octobre 2026** : le backfill complémentaire (3 942 897 ticks annoncés seq432)
   réside dans le dataset Kaggle `xauusd-dukascopy-completion-2026q4` ; sa
   récupération exige le jeton Kaggle du CI (secret existant côté workflow, non
   vérifié ce cycle). Octobre = NOT_TESTABLE dans ce recalcul.
3. **Novembre** : seuls les 7 jours locaux Dukascopy sont exploités (seq455,
   réconciliés à l'identique ce cycle : 379 paniers, 898 positions, −0,432).
4. **Continuité inter-partitions** : le moteur gelé est relancé par partition ;
   un panier ouvert en fin de partition n'est pas prolongé artificiellement
   (aucune clôture inventée) — effet borné aux 6 frontières, documenté dans le
   manifeste.
