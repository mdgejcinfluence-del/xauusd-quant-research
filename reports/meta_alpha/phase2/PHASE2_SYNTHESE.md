# PHASE 2 — SYNTHÈSE (IS seul, OOS/HOLDOUT jamais ouverts)

Config : OWNER_CONFIG_V1 hachée (seq 51/55). Challenge Blue Guardian 2-Step Pro 5k complet ; courtier partiel — commission 5 USD/lot (convention inconnue), slippage et spécification MT5 UNKNOWN : tout verdict économique reste CONDITIONNEL, sizing définitif bloqué.

## Fondations (282/282 chacune)
- **E1** barres tick/secondes/range construites ; la barre 1 000 ticks dure 2 073 s (2010-12) → 711 s (2016-20).
- **E2** 3 540 993 barres 60 s, états causaux validés (quantiles passé strict ~uniformes ; dérive 0,40 = compression du spread, pas une fuite).
- **E3** RV/BPV/J : part de barres J>0,2 = 13 % → 35 % → 60 % (ère) — à l'échelle minute, J capte largement le bruit de cotation (BPV/RV médian 0,74 en récent), pas seulement de vrais sauts : prudence consignée. ORI médian |ORI50| ≈ 0,06 stable.
- **E4** vérité économique : le forward long inconditionnel vaut ≈ −spread de clôture à tous horizons (−4,19 bp contre 4,17 en ère ancienne ; ≈ −2,1 contre 2,09 en récent).
- **E5** gate de fuite PASSÉ (permutation par blocs : corrélation 0,005 contre 0,704 alignée ; le test v1 par décalage d'un pas, mal conçu sur série persistante, est consigné et remplacé).

## Familles
| Famille | Verdict | Mesure décisive |
|---|---|---|
| F3 HAR-RV | **SUCCÈS GELÉ L1** | QLIKE récent 0,0191 < naïf 0,0266 ; 5/5 blocs ; R² MZ médian 0,200 > 0,15 → vol targeting/filtrage |
| F4 spread AR(2) | Critère non atteint | gain RMSE 1,5 % < 10 % gelé (échelle horaire) |
| F1 réversion cond. | **REJETÉE, fermée** | cellules n≥200 toutes négatives ; cellules serrées n<200 = ÉCHANTILLON INSUFFISANT (R1), signes mixtes |
| F2 ORI | **REJETÉE** | IC médian récent 0,003–0,004 ≪ 0,02 ; déciles ≈ 0,01 bp |
| F6 réversion horaire | **REJETÉE** | net ≈ −2,0 bp ≈ −spread ; brut ≈ 0 aux 3 ères (v1 bug d'alignement consignée et rejetée) |
| F5 saisonnalités | Non qualifiée | meilleure cellule (mer. 12h, −3,07 bp, n=206) : signe retourné au 3ᵉ tiers |
| F7 anticipation sauts | **SUCCÈS GELÉ L1** | AUC OOF purgé 0,684 ≥ 0,60 ; lift 2,85× à 5 % d'alerte → évitement/gating |
| F8 méta-labeling | Sans objet | aucun primaire directionnel candidat (F1/F2/F6 rejetées) |

## Budget d'essais (plafond instruction : 150)
Déclarés : F3 1 · F4 1 · F6 4 · F1 4 · F2 12 · F5 120 · F7 2 = **144/150**. Restant : 6 — insuffisant pour toute nouvelle famille ; la recherche directionnelle Phase 2 est close en l'état.

## Statut final Phase 2 (IS)
- Aucun edge directionnel extractible à coûts retail sur ces cotations : conclusion renforcée, désormais conditionnelle et chiffrée cellule par cellule (critère d'arrêt §7 de l'instruction atteint pour le directionnel).
- Deux composants de **gestion** qualifiés L1 « découverte candidate » : F3 (prévision de volatilité HAR) et F7 (anticipation de sauts) — utilisables pour sizing/filtrage/évitement, pas pour générer des trades.
- L2 (walk-forward strict + DSR/PBO sur prédictions out-of-fold) reste exécutable sous les mêmes préenregistrements sans nouvel essai ; L3 OOS exige votre ordre explicite — non donné.
- Le pivot prévu par l'instruction si le directionnel échouait : F3+F7 appliqués à une entrée extérieure (autre actif/source avec volume), décision propriétaire.
