# EUR-EDGE-02 — DESIGN DU MOTEUR DE RECHERCHE EUR/USD (payoff-first)

Pipeline : ticks canoniques → barres (par TF, Mid, complétude contrôlée) → événements
(définitions propres à EUR/USD, jamais copiées de XAUUSD) → décisions LONG/SHORT/FLAT →
exécutions simulées sur Bid/Ask réels → comptabilité nette → registre.

Composants obligatoires avant toute expérience :
- **Coûts** : spread réel au tick d'entrée/sortie ; slippage en scénarios explicites ;
  commission par contrat économique déclaré (0 par défaut, nommé) ; financement overnight
  calculé pour toute position traversant 17:00 NY (taux différentiel documenté, sinon
  position exclue des conclusions « nettes de financement »).
- **TP/SL** : distances en pips (1 pip = 0,0001), grille préenregistrée par expérience,
  jamais choisie sur le test final ; premier passage mesuré au tick (Bid/Ask directionnels),
  événements censurés comptés, trades non exécutés comptés.
- **Validation chronologique** : développement 2010-2015, calibration 2016-2018, validation
  2019-2022, test final réservé 2023-2026 (bornes à confirmer après audit de couverture ;
  le test final ne sert ni à choisir ni à régler).
- **Registres** : hypothèses et expériences avec mécanisme, population, dates d'usage,
  coûts, verdict et décision suivante ; les échecs restent publiés.
- **Fréquence** : mesurée séparément de l'espérance ; une espérance positive à 2 événements
  par an sera classée « fréquence insuffisante » par rapport à l'objectif.
