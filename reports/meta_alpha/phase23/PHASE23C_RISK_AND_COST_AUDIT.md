# PHASE 23-C — AUDIT RISQUE ET COÛTS

Comptabilité Phase 19-B reprise à l'identique : spread intégré exactement une fois via Bid/Ask
réels, slippage S0 = 0 / S1 = 0,5 / S2 = 1 bp par côté (S2 principal), commissions exclues,
aucun tarif broker inventé, aucune conversion monétaire par lot. Nom des résultats :
`HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`.

Résultats hypothétiques de développement (73 FOMC, entrée à t+15 dans le sens de la réaction) :
à 60 min, S2 moyen −7,8 bp (médiane −1,7 ; 42 % positifs ; S0 moyen −5,8) ; à 240 min, S2 moyen
+0,2 bp (médiane −2,0 ; 48 % positifs). Les témoins donnent aussi des moyennes négatives à 60 min
(−6,2 bp) : le coût d'exécution et l'absence de direction post-15 dominent. MAE post-15 médian
22,3 bp à 60 min et 32,2 bp à 240 min **sans aucun stop** : l'exposition adverse médiane dépasse
largement tout gain moyen observé.

Informations manquantes pour toute utilisation en compte de démonstration (inventaire, rien
n'est fourni ni promis) : broker et spécification exacte du contrat XAUUSD, taille minimale
d'ordre, commission réelle, spread réel autour des FOMC (fortement élargi en pratique), glissement
réel, règles de rejet, exigences de marge. Aucun ordre envoyé ; aucune promesse de rentabilité
ou de conformité à une prop firm.
