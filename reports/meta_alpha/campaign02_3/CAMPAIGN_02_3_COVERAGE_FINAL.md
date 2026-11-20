# CAMPAGNE 2.3 — MATRICE DE COUVERTURE FINALE (accès rétabli, reprise seq 178)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Aucune promotion
J2, zéro budget expérimental, holdout intact, 36 cellules gelées, FRED suspendue.
Formulation qui fait foi pour le résultat T0 : **« Association conditionnelle
fondée sur des variables disponibles à T0, sans anticipation temporelle. »**

## 1. Accès rétabli — ce qui a réellement débloqué la reprise

Après la régénération propriétaire des identifiants du compte **shalom5123**
(secrets CI mis à jour par le propriétaire, valeurs jamais affichées), la sonde
unique a répondu : librairie Kaggle toujours 403, mais **endpoint HTTPS direct
en Bearer : HTTP 200** avec listage des fichiers. La reprise a donc emprunté la
voie HTTPS directe du moteur (la librairie 1.6.17 reste défaillante, fait déjà
consigné seq 141). Trois incidents de reprise sont consignés sans fard dans les
journaux commités : (i) des lots précoces tués par une garde de couverture mal
calibrée (≥ 200 journées par lot, alors qu'un lot précoce couvre légitimement
~65 journées — tranches chronologiques de ~1,6 jour par partition) ; (ii) des
commits de lots perdus dans des courses de push de la matrice parallèle ;
(iii) un repli de téléchargement direct perdu lors d'un rebase, réappliqué.
Solution retenue : retour au patron éprouvé des campagnes 0/1 — **un seul job
séquentiel** (mode `ALL`), un commit final.

## 2. Matrice de couverture finale

| Période | État | Preuve |
|---|---|---|
| 2010–2013 | **Couverte** : 15 540 épisodes, 1 014 journées | Recoupement exact avec le brut Campagne 1 (15 540) |
| 2014–2016 | **Couverte** : 10 110 épisodes, 754 journées | Recoupement exact (10 110) |
| 2017–2020 | **Couverte** : 10 361 épisodes, 747 journées | Recoupement exact (10 361) — la lacune prioritaire est résolue |
| **Total IS** | **36 011 épisodes, 2 515 journées, 5 057 grappes** | Identique au corpus Campagne 1 (36 011 / 2 515) |
| 2020–2026 | Hors périmètre IS autorisé (clos 2020-01-20) | Non sollicitée — autres périmètres scellés |

Intégrité : 282/282 partitions chargées (8 téléchargements directs HTTP 200,
journal `CI_LOG.txt` commité) ; cassures 3 957 et retests 3 128 retrouvés à
l'unité près contre la Campagne 1. Un défaut de double append dans le fichier
cassures (lignes dupliquées à l'identique lors d'un patch) a été détecté au
contrôle, dédupliqué (31 656 → 18 956 lignes) et est consigné au journal de
qualité ; le fichier dépassements n'était pas affecté (36 011 exacts d'emblée).

## 3. Validation temporelle — l'association T0 tient sur les trois ères

Réplication à méthode gelée (définitions, instants, fenêtres, bootstrap par
grappes 2 000, graine 20261113 ; terciles du périmètre complet, seuils au fichier
`CAMPAIGN_02_3_TERCILE_THRESHOLDS.md` mis à jour). Contraste de réintégration
ultérieure entre terciles extrêmes de profondeur atteinte à T0 :

| Ère | BAS | HAUT | Contraste [IC 95 %] |
|---|---|---|---|
| 2010–2013 (4 343 / 6 106 épisodes) | 90,6 % | 78,2 % | **+12,4 pts [11,0 ; 13,9]** |
| 2014–2016 (3 338 / 3 438) | 90,6 % | 76,9 % | **+13,7 pts [11,9 ; 15,4]** |
| 2017–2020 (4 315 / 2 452) | 89,4 % | 73,8 % | **+15,6 pts [13,5 ; 17,7]** |
| Tout le périmètre (11 996 / 11 996) | 90,2 % | 76,9 % | **+13,3 pts [12,2 ; 14,2]** |

L'association conditionnelle à T0, mesurée à +13,6 points sur le fragment
2010–2014, se reproduit donc sur la décennie avec une valeur centrale stable —
légèrement croissante en ère récente, intervalles qui se recouvrent. C'est une
**stabilité descriptive**, pas un avantage prédictif : aucune confirmation
disjointe, aucune direction, aucun usage opérationnel n'en est tiré, et les
seuils de terciles restent rétrospectifs (exigence de seuils strictement
antérieurs pour tout usage futur, inchangée). Les résultats partiels historiques
(2010 → mars 2014) restent conservés séparément (`CAMPAIGN_02_2_T0_STATS.csv`,
`CAMPAIGN_02_3_TEMPORAL_REPLICATION.csv`) ; la réplication complète vit dans
`CAMPAIGN_02_3_TEMPORAL_REPLICATION_FULL.csv`. Côté cassures (décennal) : au
retest, profondeur atteinte médiane 12,26 bp, délai médian 1 minute, 54,4 %
encore au-delà à retest+60, 75,4 % d'invalidations au moins temporaires avant
T0+60.

## 4. Reproductibilité

Procédure identique au gel seq 170 du premier paramètre au dernier ; seuls les
incidents d'ingénierie ci-dessus ont été corrigés (garde d'intégrité par
partitions chargées/attendues, patron séquentiel), sans toucher aux définitions,
seuils de méthode ou fenêtres. Relancer le workflow `campaign022_all.yml`
reproduit l'extraction à l'identique tant que les secrets Kaggle restent valides.

**STATUT : ACCÈS KAGGLE RÉTABLI — REPRISE DE LA COUVERTURE HISTORIQUE
(décennale, validée par recoupement) — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**

*Annexes : `CAMPAIGN_02_3_TEMPORAL_REPLICATION_FULL.csv`,
`CAMPAIGN_02_3_PARTITION_INVENTORY.csv`, `CAMPAIGN_02_3_TERCILE_THRESHOLDS.md`
(mis à jour), `CAMPAIGN_02_3_DATA_QUALITY.md` (addendum), bruts
`campaign02_2/CAMPAIGN_02_2_*_TIMELINE.csv` + `CI_LOG.txt` + `C22_COVERAGE.json`.
Budgets inchangés ; FRED suspendue (procédure indépendante).*
