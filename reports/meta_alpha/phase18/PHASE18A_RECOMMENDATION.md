# PHASE 18-A — RECOMMANDATION

## Verdict : `PARTIALLY_AVAILABLE`

## Ce qui est disponible
Une information causale réellement nouvelle existe dans les sources IS : la **microstructure des cotations pré-décision** (activité, interruptions, tendance du spread), totalement absente des sept variables gelées, et la **texture minute du chemin pré-décision** (volatilité réalisée 30 min, efficience directionnelle, retournements), calculable depuis les barres M1 committées. Six candidats valides sont définis (formules, fenêtres, conventions de bord et de manquants dans `PHASE18A_CANDIDATE_VARIABLES.csv`), un candidat limite (vitesse de retracement, interaction de variables existantes) et un écarté (cosmétique).

## Ce qui ne l'est pas
Aucune information de volume, de profondeur, de transactions ou de remplissage n'existe dans les sources et n'en existera pas par extraction : la caractérisation d'exécution restera limitée à des proxys de cotation. Les séries tick pré-décision ne figurent dans **aucun artefact committé** : trois candidats sur six exigent une extraction future des partitions IS, non autorisée ici.

## Frontière recommandée
Toute suite exigerait une décision distincte : (1) un contrat de calcul gelé des candidats retenus (bornes `<= t_decision`, barres closes uniquement, conventions de bord et de `NON_VALIDABLE`) ; (2) une extraction limitée aux partitions IS 2010–2020 ; (3) un audit de fuite et de redondance empirique avant tout modèle ; (4) le statut permanent des résultats : exploratoires et post-hoc sur population déjà étudiée, jamais confirmation indépendante. Le présent audit n'autorise ni extraction, ni calcul, ni entraînement, ni test économique.
