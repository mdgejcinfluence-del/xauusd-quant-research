# PHASE 19-B — AUDIT DE COMPTABILISATION DU SPREAD

## Preuves dans le code exécuté
- **Entrée** (`ci_tools/phase17b_engine.py` l.168) : `entree = ask si direction=1 (LONG) sinon bid (SHORT)`, premier tick strictement postérieur à `t_decision`.
- **Sortie** : prix de liquidation `liq = bid si LONG sinon ask` (l.76 du moteur de lot), qu'il s'agisse du tick de franchissement TP/SL (l.174-179 : comparaison `direction*(liq-entree)` aux barrières en unités de prix) ou du dernier tick avant échéance pour les sorties verticales. Le prix retenu est celui du **tick de franchissement réel**, jamais le niveau théorique de barrière : gaps et dépassements sont inclus.
- **P&L** (fonction gelée `remplir`, l.130-133) : `direction * log(ps/pe) * 10000`, où `pe`/`ps` sont les prix exécutables ci-dessus, seulement ajustés du slippage de scénario.

## Démonstration
Pour un LONG : P&L ∝ log(Bid_sortie / Ask_entrée). Si le Mid est inchangé (Bid = Mid − s/2, Ask = Mid + s/2), P&L = log((Mid−s/2)/(Mid+s/2)) < 0 : la perte égale exactement le spread traversé deux fois (achat au Ask, vente au Bid). Le spread est donc intégré **une fois, par les prix**, à l'entrée comme à la sortie. Même démonstration symétrique pour le SHORT (entrée Bid, sortie Ask).

## Recherche d'une seconde déduction
Aucune soustraction de spread n'existe en aval : ni dans `remplir` (seul le facteur de slippage de scénario y figure), ni dans la conversion en bp (même formule), ni dans `Y_ECON` (signe de PL_S2), ni dans `R_REALIZED_S2` (division par la distance de risque, Phase 17-E), ni dans les barrières B08/B09 (comparaisons en prix sur le prix de liquidation). La convention 13-B d'origine est identique (entrée `ask/bid`, clôture `bc/ac` = Bid/Ask de clôture selon le sens, `phase13b_engine.py` l.239-249), et la réconciliation 17-B contre les résultats gelés de Phase 14 est exacte à 10⁻¹⁴ bp (440/435 événements communs), ce qui exclut une divergence silencieuse entre générations du calcul.

**Conclusion : spread comptabilisé exactement une fois. Aucune anomalie de double déduction identifiée.**
