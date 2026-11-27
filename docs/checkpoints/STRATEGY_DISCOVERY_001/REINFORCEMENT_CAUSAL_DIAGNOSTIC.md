# DIAGNOSTIC CAUSAL — RENFORCEMENTS (D1, préenregistré seq458)

Association agrégée (janv.–sept. 2026, moteur gelé) : paniers à 3 positions
−30,68 USD contre +0,71 USD à 2 positions. **Cette association ne démontre pas un
effet causal** : la 3e position n'est ajoutée que si le prix a déjà reculé d'environ
−5,5 bp — les paniers renforcés sont sélectionnés parmi les situations défavorables.
Contrefactuel descriptif sur trajectoires (nov. 2026, 140 paniers à 3 positions) :
pour seulement **14 paniers**, le panier tronqué à 2 positions aurait clôturé selon la
règle V1 avant la clôture réelle ; sur ce sous-ensemble, le résultat sans 3e
(+0,64 USD) est **inférieur** au résultat réel avec 3e (+1,72 USD) — la 3e a aidé la
récupération là où la récupération était accessible. Les **126 autres paniers sont
censurés** (pas de clôture tronquée observable dans la fenêtre) : sans issue
contrefactuelle, leur effet est inconnu. **Verdict : `CAUSAL_EFFECT_NOT_IDENTIFIED`.**
Ce qui est établi : le renforcement augmente l'exposition et les coûts dans les
situations adverses et allonge les paniers ; ce qui ne l'est pas : qu'il cause les
pertes plutôt qu'il ne marque les paniers déjà en difficulté. Chez le trader réel,
la 3e survient sur recul −4,7 à −6,6 bp (n=3) ; sa règle d'arrêt reste inconnue.
