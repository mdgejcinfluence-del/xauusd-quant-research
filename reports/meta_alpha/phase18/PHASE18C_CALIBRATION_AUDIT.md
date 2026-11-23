# PHASE 18-C — AUDIT DE CALIBRATION (valeur prédite)

Pentes de calibration (R réalisé ~ R prédit) par segment, population commune :

| Contrat / modèle | Apprentissage | Calibration 2016–2017 | Évaluation 2018–2020 |
|---|---|---|---|
| B08 BASE_7 | 1,00 (en échantillon) | −0,104 | −0,062 |
| B08 EXT_13 | 1,00 (en échantillon) | **−0,222** | +0,476 |
| B09 BASE_7 | 1,00 (en échantillon) | +0,042 | −0,386 |
| B09 EXT_13 | 1,00 (en échantillon) | **−0,019** | +0,143 |

Lecture : le signe de la pente n'est stable sur **aucun** contrat ni aucune architecture entre calibration et évaluation. EXT_13 obtient une pente positive en évaluation mais négative ou nulle en calibration 2016–2017, avec des MAE de calibration dégradés par rapport à BASE_7 et M0_R (B08 : 1,1051 contre 1,0997/1,0963 ; B09 : 0,8311 contre 0,8318/0,8304). Une pente négative ne peut pas être interprétée comme une amélioration ; la configuration observée (positive seulement sur le segment déjà le plus étudié, négative sur le segment intermédiaire) est celle d'un ajustement instable, pas d'un transport. Les distributions de prédictions restent comprimées (évaluation EXT_13 : −0,35 à +0,83 R pour B08) face à des R réalisés d'écart-type ≈ 1,17/0,89.
