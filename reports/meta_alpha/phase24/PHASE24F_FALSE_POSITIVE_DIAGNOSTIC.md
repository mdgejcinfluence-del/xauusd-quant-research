# PHASE 24-F — DIAGNOSTIC DES FAUX POSITIFS

Les faux positifs ne sont ni uniformes ni séparables :

- **Score** : médiane des FP = 0,654 (calibration) et 0,664 (évaluation), contre 0,681 et 0,690
  pour les vrais positifs. Les distributions se chevauchent presque entièrement ; les FP sont
  présents dans toutes les classes sélectionnées, y compris les plus hautes.
- **Variables causales** : les médianes des FP sont proches de celles des VP (ratio de repli
  1,83 contre 1,98 ; durée extrême→réintégration 15 min dans les deux cas ; touches de P0 : 3
  contre 3). Seul le MFE déjà atteint à la décision diffère légèrement (13,7 contre 10,0 bp en
  calibration). Aucune variable existante ne sépare les FP des VP — `M15_FALSE_POSITIVES_NOT_SEPARABLE`
  sur la base des informations causales disponibles, et aucune recherche de filtre n'est autorisée.
- **Stabilité** : le profil est le même en 2016-2017 et en 2018-2019 ; ce n'est pas une instabilité
  temporelle locale, c'est une propriété structurelle de la sélection au seuil gelé.

Conclusion : l'erreur de sélection est diffuse dans le score et dans les variables ; elle ne peut
pas être corrigée par un filtre post-hoc sans créer un nouveau prédicteur — ce qui est interdit.
