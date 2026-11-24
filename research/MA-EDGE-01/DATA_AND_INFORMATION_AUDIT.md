# MA-EDGE-01 — 05 · AUDIT DES DONNÉES ET INFORMATIONS

Corpus actuel : ticks Bid/Ask XAUUSD IS 2010-2019 (224 M), barsets H4/D1/M15 committés,
événements et prédictions gelés, catalogue FOMC. Ce corpus permet de mesurer prix, spread et
temps — jamais tailles, transactions, profondeur ou positionnement.

Informations manquantes par ordre d'impact : (1) transactions et volume réels (COMEX, licence) ;
(2) volatilité implicite intraday et skew (licence) — mais le niveau quotidien GVZ est libre ;
(3) positionnement (COT, libre, retardé) ; (4) inter-marchés intraday (licences) ;
(5) spécifications broker et slippage réel (jamais vérifiés : toute rentabilité monétaire reste
indécidable, seuls les log-bp sont honnêtes).

Sources libres vérifiées en 25-A : GVZCLS (FRED, 2008+, J-1 strict) et COT (CFTC, publication
vendredi 15:30 ET). Aucune extraction n'a été faite dans cette mission : le canal d'extraction
FRED depuis l'environnement d'exécution est documenté comme restreint (Phase 23-B) ; les miroirs
GitHub utilisés alors pour les taux n'ont pas d'équivalent vérifié pour GVZCLS à ce jour.
C'est un problème de plomberie documenté, pas un problème scientifique — il se résout par le
canal d'extraction de la Phase 25-B si le fondateur l'autorise.
