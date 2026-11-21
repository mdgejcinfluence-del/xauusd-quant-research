# PHASE 10-A — REGISTRE DES RISQUES MÉTHODOLOGIQUES ET AUTORISATIONS REQUISES

## 1. Risques méthodologiques

| # | Risque | Traitement pré-déclaré |
|---|---|---|
| R1 | Réutilisation d'un corpus déjà exploré (campagnes 0–8, Phase 9) présentée comme preuve neuve | étiquette « historiquement évalué » obligatoire ; confirmation indépendante exigée avant J2/E1 |
| R2 | Tests multiples et recherche d'horizon « qui marche » | famille fermée de six tests, BY m = 6, aucun ajout postérieur |
| R3 | Confondre MFE (meilleure sortie inconnaissable) et espérance | variable primaire = rendement signé à fenêtre fixe ; MFE/MAE descriptifs et porte de queue |
| R4 | Double comptage du spread | prix Bid/Ask intégrés, ou un spread complet en repli Mid — jamais les deux |
| R5 | Coûts hypothétiques présentés comme réels | scénarios étiquetés ; commissions/swaps réels exigés avant tout statut E1 |
| R6 | Fenêtres chevauchantes comptées comme indépendantes | grappes-composantes connexes, règle de grappe dominante à 5 % |
| R7 | Seuils « causaux » contaminés (quantiles poolés) | quantiles roulants sur 250 barres closes, amorçage inéligible publié |
| R8 | Résurrection déguisée des candidates P9-A…P9-E à un autre horizon | interdite par le protocole ; les événements sont définis par horizon, pas par reprise des anciennes règles |
| R9 | Faibles effectifs D1 et instabilité d'ère | porte d'effectif, stabilité par ère publiée, arrêt si signe instable |
| R10 | Prix Bid/Ask d'agrégats pris pour des remplissages | étiquette « capturable en principe » ; aucune preuve d'exécution |
| R11 | Dérive des conditions de marché post-2020 non observable (holdout scellé) | assumée et déclarée ; aucune extrapolation au présent |

## 2. Autorisations nécessaires avant exécution (aucune n'est accordée par ce dossier)

1. **Validation du présent protocole** par le propriétaire, y compris
   les constantes : horizons H1/H4/D1, fenêtres causales de 250
   barres, quantiles Q95/Q90/Q25, portes économiques (3×, espérance >
   coût central, MAE ≤ 3×, 200 événements / 100 grappes), famille
   fermée F10-01…F10-06, BY m = 6.
2. **Gel chaîné** du protocole validé (SHA-256 en chaîne de preuves).
3. **Ordre d'exécution distinct**, précisant le périmètre de calcul et
   le budget de ressources gratuites, avec suspension documentée en
   cas de dépassement.
4. Décisions séparées ultérieures, **non incluses** : construction de
   toute fiche stratégie ; ouverture éventuelle du holdout ; collecte
   prospective ; étude prop firm (P1) — chacune exige son ordre.
5. Restent interdits sans ordre contraire : backtest stratégique et
   `challenge_sim`, accès FRED, activation T0, modification des
   36 cellules S12, reprise des candidates P9 et des campagnes closes.
