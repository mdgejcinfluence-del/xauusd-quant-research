# PHASE 23-C — RAPPORT FINAL : ANATOMIE TEMPORELLE DES RÉACTIONS FOMC

Statut : `EXPLORATORY_POST_HOC`. Les 73 événements et 73 témoins restent du développement
consommé ; aucun edge n'est déclaré.

## 1. Ce que mesurent les 71 %

Une persistance du déplacement initial **par rapport au prix de départ**, pas une continuation
exploitable après les quinze premières minutes : mesurée correctement depuis P15, la continuation
n'est que de **52,1 % à 60 minutes** (58,3 % à 240 minutes), avec un résultat hypothétique S2
moyen de −7,8 bp à 60 minutes. Les MFE et MAE post-15 sont quasi symétriques (22,2 contre
22,3 bp) : après le choc initial, la trajectoire est une marche sans dérive directionnelle
mesurable.

## 2. Ce que mesurent les 88 %

Une oscillation immédiate autour du prix pré-annonce : 65 des 73 premières revisites surviennent
avant t+15 minutes. Ce n'est ni un retournement tardif ni un argument pour la règle directionnelle.

## 3. Amplitude et direction après P15

L'amplitude post-15 est réelle et symétrique (MFE/MAE ≈ 22-35 bp selon l'horizon) ; la direction
moyenne est nulle. Verdict historique : **`FOMC_VOLATILITY_ONLY`** — le FOMC est un régime
d'amplitude bidirectionnelle, y compris après les quinze premières minutes.

## 4. Règle gelée et protocole

La règle unique (direction = signe de P15 vs P0, entrée premier Ask/Bid après t+15, sorties
60/240 min, S2 principal, sans stop/TP ni seuil) est gelée dans
`PHASE23C_FOMC_CANDIDATE_RULE.md` et le protocole prospectif dans
`PHASE23C_PROSPECTIVE_VALIDATION_PROTOCOL.md`, avec registres séparés développement/validation
et puissance documentée (81 événements minimum pour un effet de 15 bp à 60 min — plus d'une
décennie de FOMC ; aucune conclusion rapide possible). Verdict protocole :
**`FOMC_PROSPECTIVE_PROTOCOL_FROZEN`**. La règle est une hypothèse à tester sur des événements
nouveaux, que l'historique ne soutient pas à 60 minutes ; aucun passage en réel ou en démo n'est
autorisé sans architecture de risque distincte et validée.
