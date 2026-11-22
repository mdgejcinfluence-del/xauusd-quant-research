# PHASE 17-E — RAPPORT FINAL

## Entraînement et évaluation des modèles de payoff continu M2R-B08 et M2R-B09

**Qualification : EXPLORATOIRE_IS — MODÈLE DE PAYOFF CONTINU.** Exécution strictement
conforme au préenregistrement 17-D gelé (seq351, empreintes revérifiées 7/7) : régression
linéaire OLS sans régularisation ni sélection, sept variables gelées brutes + intercept +
sessions one-hot (ASIA en référence, convention 17-B), cible `R_REALIZED_S2`, référence
`M0_R` sur le seul apprentissage, règle `PREDICTED_EXPECTED_R > 0` jamais optimisée.
Commissions exclues, slippage S2 hypothétique ; évaluation 2018–2020 déjà étudiée,
jamais confirmation indépendante.

## 1. Références
`M0_R_B08 = −0,206 R` (n = 1 137) et `M0_R_B09 = −0,127 R` (n = 1 133) : les deux
moyennes d'apprentissage sont négatives, donc la décision théorique du baseline est
**aucune exposition** sur tous les segments. Toute la question était de savoir si M2R
sait identifier les exceptions positives.

## 2. Qualité de prédiction en évaluation (critère gelé : MAE et RMSE < M0_R)
| Contrat | MAE M0_R | MAE M2R | RMSE M0_R | RMSE M2R | Pente de calibration |
|---|---|---|---|---|---|
| B08 | 1,0924 | 1,0943 | 1,1843 | 1,1836 | −0,096 |
| B09 | 0,8267 | 0,8302 | 0,8961 | 0,9010 | −0,445 |

Aucun contrat ne satisfait le critère : B08 dégrade le MAE et ne gagne que 0,06 % relatif
sur le RMSE ; B09 dégrade les deux. Le segment 2016–2017 confirme l'absence de transport
(pentes 0,007 et 0,030 ; MAE également dégradés). Les prédictions varient trop peu et sans
rapport monotone avec les R réalisés : la pente de calibration négative en évaluation
signifie que, dans la queue retenue, prédire plus haut n'annonce pas réaliser plus haut.

## 3. Décision économique `PREDICTED_EXPECTED_R > 0`
B08 retient 13 événements sur 440 (3,0 %) pour +0,35 R réalisé en moyenne — mais les 4
retenues de calibration réalisaient −0,10 R, et cette poignée positive ne repose sur
aucune qualité prédictive établie (MAE dégradé, pente négative) : non cohérente au sens
du critère gelé. B09 retient 37 événements (8,5 %) pour **−0,111 R** réalisé : la décision
produit le contraire de l'espérance annoncée. La pondération par grappe ne modifie aucune
conclusion (retenues quasi toutes mono-événement).

## 4. Verdicts
- `M2R_B08` : **`NO_CONTINUOUS_PAYOFF_IMPROVEMENT`**
- `M2R_B09` : **`NO_CONTINUOUS_PAYOFF_IMPROVEMENT`**

## 5. Conclusion
Changer de représentation — du signe binaire à l'espérance continue normalisée par le
risque — ne crée pas d'information qui n'existe pas dans les variables : à dictionnaire
causal identique, les sept variables ne portent de façon transportable ni le signe (17-B),
ni l'amplitude conditionnelle (17-E). La normalisation en R stabilise bien l'échelle entre
régimes (17-D), mais l'espérance conditionnelle reste imprévisible à ces variables sur
cette cohorte. Limites maintenues : biais de sélection M1 en échantillon sur
l'apprentissage, `p_M1` exclu, évaluation déjà étudiée, commissions exclues, cotations
sans profondeur. Aucun verdict ne constitue une confirmation économique indépendante.
Toute étape ultérieure nécessite une décision distincte ; le holdout reste exclu.
