# PHASE 5 — SPÉCIFICATIONS CONTRACTUELLES ET COÛTS (couches séparées des données)

## Observations HFM fournies par le fondateur (captures, date de consultation — jamais rétro-appliquées)
Serveur `HFMarketsSV-Live Server 9`, symbole **XAUUSDc** (compte Cent), contract size 1,
digits 2, spread flottant, calcul CFD, exécution Market, volume 0,01–1000 pas 0,01, marge USD,
swap en points : long −73,56 / short 0, triple swap le mercredi. Ces valeurs décrivent **ce
compte, à cette date** ; le spread d'une capture n'est pas une moyenne historique et le Cent
(contract size 1) ne se confond ni avec le standard (100 oz) ni avec Dukascopy.

## Modèle de coûts paramétrable (implémenté dans `ci_tools/replay_engine.py`)
Exécution : BUY entrée Ask / sortie Bid ; SELL entrée Bid / sortie Ask — le spread est payé
**une seule fois**, par les prix eux-mêmes. Au-delà, scénarios de bp additionnels (commission +
slippage + swap/nuit), le swap réel dépendant du profil : OPTIMISTE 0/0/0 ; CENTRAL 0,7/0,5/2,0 ;
PRUDENT 1,0/1,5/4,0 ; STRESSE 1,5/4,0/8,0. Références META ALPHA conservées sans écrasement :
spread observé historique ≈ 2,3 bp (mesuré sur le flux, M15 médian 2,33 bp), coût preneur
aller-retour complet ≈ 4–4,5 bp dans nos mesures GOLD. Pour un replay « conditions HFM Cent » :
convertir avec contract size 1 et swap en points du jour de simulation — hypothèses explicites
par scénario, jamais mélangées aux ticks Dukascopy.
