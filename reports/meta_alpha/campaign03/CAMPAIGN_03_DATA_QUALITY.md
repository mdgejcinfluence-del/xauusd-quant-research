# CAMPAGNE 3 — QUALITÉ DES DONNÉES ET TRAÇABILITÉ D'EXÉCUTION

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Couverture

| Contrôle | Résultat |
|---|---|
| Partitions chargées / attendues | **282 / 282** (garde d'intégrité du moteur satisfaite ; échec = suspension documentée, non déclenchée) |
| Barres reconstruites | 3 540 993 M1 ; 702 397 M5 ; 231 875 M15 (barres complètes uniquement : `n >= minutes` constituantes) |
| Dates UTC présentes | 3 097 (toute date ayant au moins une barre M1 ; les journées de cotation « pleines » du corpus historique sont 2 515 — les deux comptes sont publiés sans être confondus) |
| Épisodes | IMP-M5 70 493 ; IMP-M15 23 075 ; CONS 15 973 |
| Amorçage des seuils causaux | 2 000 premières barres IMP de chaque famille sans seuil possible (minimum gelé) ; 1 journée CONS sans seuil (minimum 1 000 barres poolées non atteint le premier jour) |
| Censure | Trajectoires IMP censurées fin de journée : 0,7 % (M5), 1,4 % (M15) ; CONS censurées +120 min : 0,6 % — comptées, jamais imputées |
| Chevauchements | IMP-M5 57 401 épisodes (81 %) ; IMP-M15 12 724 (55 %) déclenchés dans la fenêtre d'issue d'un prédécesseur — signalés en colonne, jamais supprimés ; aucune analyse de sensibilité par exclusion n'avait été préenregistrée, aucune n'a été faite |

## Définitions appliquées (rappel traçable)

Dictionnaire seq 185–186 (sha256 `76490c40e4c6aca1cad56a98f30d4711d6723ac56e39cf08f978a0349d354a92`,
revérifié inchangé avant exécution) ; clarifications temporelles et 12
comparaisons gelées seq 189 (sha256 `ac151cb8007df82cd239b14e58676fc10d9789a98be50f5840363b91e24541c8`).
Prix d'origine des impulsions = clôture de la barre précédant le
déclenchement ; prix Mid de barres (déclaré au dictionnaire) ; régime F3 du
jour gelé seq 75 ; ères 2010–13 / 2014–16 / 2017–20 ; sessions UTC
conventionnées du dictionnaire.

Items de lecture assumés et publiés : les intervalles bootstrap de C3-11 et
C3-12 sont dégénérés ([0,0 ; 0,0] et médianes identiques 8 min) — conservés
tels quels au tableau des comparaisons et au registre plutôt que maquillés ;
le bras Londres de C3-11 est faible (466 épisodes, 287 journées) mais atteint
la suffisance gelée.

## Journal d'exécution (incidents et résolutions)

1. Runs CI 44879795186, 44880100539, 44880414736 : extraction terminée côté
   runner mais **commit des résultats échoué** (données perdues avec le
   runner). Journaux GitHub Actions inaccessibles depuis le bac à sable
   (EOF du service de logs) : cause racine non observable directement.
2. Sonde dédiée (run 44881744231) : un micro-commit poussé depuis le même
   runner réussit — le push Git du runner est fonctionnel ; l'échec tenait
   donc au contenu (volume des tableaux bruts non compressés). La sonde et
   ses fichiers de diagnostic ont été retirés du dépôt après usage.
3. Correctif : tableaux bruts publiés en **gzip** (plus gros fichier final :
   instantanés IMP 23,0 Mo compressés) ; run 44881797073 vert, commit CI
   `94dddc3` récupéré et vérifié (282/282 partitions au journal).
4. Aucun paramètre de définition n'a été modifié pendant ces incidents :
   seuls le format de sortie (gzip, arrondi 4 décimales) et l'étape de
   commit du workflow ont changé, après le gel et sans contact avec les
   résultats chiffrés (les échecs précédaient toute récupération de
   résultats).

## Périmètres interdits — état

Holdout / post-2020 : non accédé. Flux prospectif T0 : inexistant et non
utilisé. FRED : suspendue, non utilisée. Budgets expérimentaux de trading :
aucune consommation. 36 cellules S12 : intactes. Aucun résultat intermédiaire
de confirmation consulté (il n'en existe pas).
