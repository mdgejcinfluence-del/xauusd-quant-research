# EXIGENCES D'IMPLÉMENTATION ET D'EXÉCUTION

Pour la jambe prospective : chaîne déjà implémentée et auto-testée (collecteur Dukascopy,
détection 24-B, score gelé, règle 120 min, bootstrap par grappes, graines figées) ; collecte par
dispatch (cron limité à la branche par défaut) ; évaluation à ≈ 350 événements. Pour toute jambe
de fourniture de liquidité future : compte démo fondateur, journal de fills horodaté, markouts
10 s/1 min/5 min, taux de non-fill, inventaire temps réel — **avant** tout backtest, car le
backtest ne peut pas fabriquer ces nombres. Pour toute jambe options/futures : programme séparé
(instrument, base, marges, financement, rollover) et autorisation de dépense explicite. Aucun
ordre réel n'est autorisé par ce document.
