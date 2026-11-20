# CAMPAGNE 2.3 — QUALITÉ DES DONNÉES ET DE LA REPRISE

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Contrôle | Résultat |
|---|---|
| Sonde d'accès (gelée seq 174) | Kaggle : 403 (librairie), 403 (HTTPS Bearer), 403 (HTTPS basic) ; Drive : 1 fichier, échec rc=1 contrôle de taille non atteint. Journal commité `ACCESS_PROBE.txt`. Aucun téléchargement au-delà de la sonde |
| Inventaire | 348 partitions recensées depuis l'inventaire commité ; 282 IS (8 lots Kaggle, intégrité vérifiée à la migration) ; 66 hors IS-282 en métadonnées seules, jamais ouvertes ; `drive_id` réduit à un booléen de présence dans l'inventaire livré |
| Périmètres | IS clos le 2020-01-20 (borne gelée) ; 2020–2026 = autres périmètres scellés, non sollicités ; holdout jamais accédé ; aucun nouvel actif |
| Réplication | Méthode seq 170 reproduite à l'identique sur le périmètre disponible ; 6 épisodes T0 sans issue mesurable exclus du calcul des taux (taux de manquants ≈ 0,05 %, publié dans `TEMPORAL_REPLICATION.csv`) ; intervalles par bootstrap par grappes jour×niveau, 2 000 répétitions, graine 20261113 |
| Cohérence temporelle | Ère 2010–13 : +13,6 pts [11,9 ; 15,3] ; fragment 2014 (48 journées) : +13,7 pts [5,8 ; 21,5] ; ère 2017–20 : **non mesurée**, ligne conservée au fichier de réplication |
| Identifiants | Aucune valeur d'identifiant affichée, journalisée ou commitée dans cette campagne ; les journaux CI ne contiennent que des statuts (403, rc, tailles attendues/conformes) ; Kaggle ≠ FRED (cette dernière reste suspendue, procédure de rotation distincte et non traitée ici) |
| Données fabriquées | Aucune. Les périodes inaccessibles sont écrites NON MESURÉ / HORS PÉRIMÈTRE, jamais comblées |
| Reproductibilité | Sonde `ci_tools/campaign023_probe.py` + workflow `campaign023_probe.yml` ; moteur de reprise `campaign022_engine.py` (lots, garde de couverture) inchangé depuis seq 168–172 ; calculs de réplication relancés localement sur le brut commité |

## Addendum seq 178 — extraction décennale

| Contrôle | Résultat |
|---|---|
| Accès | Sonde : HTTPS Bearer HTTP 200 (librairie Kaggle toujours 403) ; extraction par téléchargements directs, 8/8 datasets, 282/282 partitions traitées (CI_LOG commité) |
| Recoupement | Épisodes par ère et totaux identiques au brut Campagne 1 (15 540 / 10 110 / 10 361 ; 36 011 ; 2 515 journées ; 3 957 cassures ; 3 128 retests) |
| Défaut corrigé | Double append des lignes cassures (patch moteur) : 12 700 lignes dupliquées à l'identique supprimées (31 656 → 18 956) ; dépassements non affectés. Le moteur commité conserve le défaut pour traçabilité ; la correction est appliquée au brut livré et consignée ici |
| Incidents de reprise | Garde ≥ 200 journées/lot inadaptée aux tranches précoces (~65 j) remplacée par un contrôle partitions chargées/attendues ; commits de matrice perdus en courses de push → patron séquentiel à commit unique ; repli HTTPS perdu en rebase, réappliqué et vérifié dans le code commité |
| Manquants | 6 épisodes T0 sans issue mesurable sur 36 011 (fin de fenêtre) ; taux publiés dans la réplication |
