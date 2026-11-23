# PHASE 19-B — VERDICT FINAL DE L'AUDIT COMPTABLE

## Verdict : `BROKER_SPECIFICATION_UNVERIFIED`
avec comptabilité des coûts internes **vérifiée** sur tous les points contrôlables dans le code :

1. **Spread** : intégré exactement une fois, par les prix exécutables (entrée Ask/Bid, sortie au prix de liquidation Bid/Ask du tick réel de franchissement ou de clôture) ; démontré mathématiquement et par tests synthétiques (perte = spread exact sans mouvement du Mid) ; aucune seconde déduction dans P&L, bp, S0/S1/S2, `Y_ECON`, `R_REALIZED_S2`, B08/B09 ni dans les Phases 17–18.
2. **Slippage** : S0/S1/S2 = 0/0,5/1 bp par côté, sens défavorable, une fois par côté, proportionnel au prix ; corroboré par les deltas historiques mesurés (−1,0/−2,0 bp). Nature : hypothèse de sensibilité, jamais une mesure.
3. **Unités** : chaîne dollars → log-bp → R traçable et cohérente ; mélange log/arithmétique du dénominateur de R documenté (approximation gelée 17-D). Aucun pip universel supposé.
4. **Commissions et spécification broker** : commissions exclues partout et toujours libellées comme telles ; broker, contrat, taille de lot et barèmes **absents de tous les artefacts** — toute conversion monétaire par lot est donc invérifiable, d'où le verdict. Aucun tarif inventé.

Conséquence pour la lecture des Phases 13–18 : les résultats historiques ne sont **pas** entachés d'une double comptabilisation du spread ; leurs limites économiques tiennent au signal et aux représentations testés, pas à une erreur de comptabilité des coûts identifiée. Ils restent bruts de commissions et fondés sur un slippage hypothétique.

## Étape suivante préparée (sans exécution) : expérience H8 contre H16
Protocole proposé, à soumettre à autorisation distincte : sur les cohortes historiques de référence (événements filtrés M1 gelé, entrée exécutable E0 premier tick Ask/Bid), comparer deux sorties temporelles fixes à coûts identiques — **H8** : liquidation au prix Bid/Ask du dernier tick de la 8ᵉ barre H1 complète après l'entrée ; **H16** : même règle à la 16ᵉ barre. Aucune barrière, aucun modèle M2, aucune variable nouvelle, aucun seuil optimisé ; mêmes conventions de spread (prix exécutables) et de slippage S0/S1/S2 que l'audit vient de vérifier ; résultats en bp et en R (risque = distance ATR gelée à titre de normalisation descriptive uniquement), séparés par direction et par grappe, avec qualification permanente exploratoire et post-hoc. Question unique : la durée de détention, à signal et coûts identiques, change-t-elle l'espérance réalisée ? Aucune exécution de cette expérience n'est autorisée par la présente phase.
