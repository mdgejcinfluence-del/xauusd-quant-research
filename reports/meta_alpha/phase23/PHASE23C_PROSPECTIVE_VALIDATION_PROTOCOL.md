# PHASE 23-C — PROTOCOLE DE VALIDATION PROSPECTIVE (GELÉ)

Contrat gelé et committé avant toute consultation des futurs résultats économiques. Les 73
événements historiques sont exclus de la population de validation (registre
`FOMC_DEVELOPMENT_EVENTS`) ; seuls les FOMC postérieurs au gel alimentent
`FOMC_LOCKED_VALIDATION_EVENTS`, sans aucune lecture exploratoire intermédiaire des résultats
économiques (seuls les contrôles de qualité de cotation sont autorisés).

Règles identiques à `PHASE23C_FOMC_CANDIDATE_RULE.md` : t0 officiel 14:00 ET→UTC (DST
historique), P0/P15 et fraîcheur (300 s), direction par signe de P15 vs P0 sans seuil, entrée
premier Ask/Bid strictement après t0+15 min (≤ 60 s sinon NON_EXECUTION), sorties 60/240 min
séparées, S2 principal (S0/S1 sensibilités), commissions exclues, aucun stop/TP. Cotation
manquante : événement classé non validable, jamais interpolé ; gap de cotation > 300 s autour
d'un point de référence : point non validable, documenté, jamais remplacé.

Métriques de risque obligatoires par événement : MAE post-entrée jusqu'à chaque sortie,
excursion adverse maximale, temps passé sous le prix d'entrée, nombre de passages de P0.
Aucune architecture de risque n'étant définie, **aucun passage en réel ou en démo n'est autorisé**
par ce protocole ; il ne produit qu'une évaluation statistique.

Analyse de puissance (variance historique de développement, écart-type du net S2 : 48,2 bp à
60 min, 62,0 bp à 240 min) : détecter un effet moyen de 10 bp (α = 0,05 bilatéral, puissance
80 %) exige **183 événements** à 60 min et **302** à 240 min ; pour 15 bp : 81 et 134. À raison
de 8 décisions par an, une validation à 10 bp prendrait plus de deux décennies : la taille
minimale réaliste est fixée à **81 événements (horizon 60 min, effet 15 bp)**, tout résultat
antérieur restant descriptif et non décisionnel. Cette contrainte est assumée et documentée :
elle interdit toute conclusion rapide.
