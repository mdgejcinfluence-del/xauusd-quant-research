# MA-EDGE-01 — DISPOSITIF D'OBSERVATION SHADOW (aucun ordre, aucun capital)

Objet : observer prospectivement les événements M15 admissibles **strictement postérieurs au
2026-09-30T23:59:58.864 UTC** (fin de couverture du holdout consommé, manifeste 12-C.2
vérifié ligne par ligne) et évaluer la règle préenregistrée (deadline 120 min) contre la sortie
fixe 8 h, en mode fantôme : aucun ordre n'est envoyé ; seuls des prix Bid/Ask observés sont
enregistrés.

Champs par événement : contrat `SHADOW_DATA_CONTRACT.json` (horodatages, informations à la
décision, état du modèle gelé, Bid/Ask, entrées/sorties théoriques exécutables, P&L S0/S1/S2,
MFE/MAE, durée d'exposition, motif de sortie, incidents de cotation).

Puissance (calculée, pas arbitraire) : écart-type historique de la différence appariée entre
architectures de sortie ≈ 40 bp (ordre de grandeur des différences 24-E). Pour détecter un effet
de +8 bp par événement (α = 0,05 bilatéral, puissance 80 %, test apparié) :
n = ((1,96 + 0,84) × 40 / 8)² ≈ **196 événements indépendants** ; en grappes (les fenêtres se
chevauchent à ≈ 60 %, facteur d'inflation ≈ 1,8), viser **≈ 350 événements sélectionnés ou
140 grappes**, soit, au rythme historique (≈ 560 événements sélectionnés/an en IS), environ
**8 mois de collecte**. En dessous de 50 grappes, tout résultat restera descriptif.

Blocage d'activation documenté : la collecte exige un flux Bid/Ask XAUUSD horodaté en continu,
gratuit et licite. Le programme ne dispose d'**aucune source de ce type actuellement connectée**
(le corpus historique provient de jeux Kaggle privés déjà fermés ; aucun flux temps réel gratuit
vérifiable n'est disponible dans l'environnement d'exécution). Le dispositif est donc **prêt
mais non activé** : scripts de collecte et de scoring dans `research/MA-EDGE-01/shadow/`,
conçus pour démarrer dès qu'un flux autorisé (capture broker démo du fondateur, export de
plateforme) sera fourni. Aucune donnée prospective n'est prétendue collectée.
