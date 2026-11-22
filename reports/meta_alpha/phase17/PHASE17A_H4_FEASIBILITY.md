# PHASE 17-A — BILAN DOCUMENTAIRE DE FAISABILITÉ H4 (BRANCHE DISTINCTE)

**Aucun modèle H4 n'est entraîné, conçu en détail ou mélangé à H1
dans cette phase. Le présent document est un bilan, pas un protocole.**

## Population historique disponible (artefacts existants)

Famille F10-03, timeframe H4 (features Phase 12-B, étiquetés
directionnels) : **apprentissage 379, calibration 120, évaluation
130** événements — contre 1 640 / 507 / 543 pour H1. En Phase 12-B,
H4 a été déclaré `NON_EVALUABLE` au sens prédictif (évaluation :
130 étiquetés, classe minoritaire 18, sous les critères gelés
100/50), et **aucun modèle H4 n'existe** : il n'y a ni coefficients
H4 gelés, ni confirmation de type 12-C, ni baseline directionnelle
H4 validée.

## État des labels économiques potentiellement constructibles

En principe, la machinerie de barrières (ATR H4 à redéfinir,
ticks IS) pourrait construire des étiquettes de type `Y_ECON`
pour H4. Mais il manquerait l'étage primaire : sans modèle M1-H4
gelé et confirmé, il n'existe ni filtre primaire légitime
(l'équivalent du seuil `p_M1 > M0` n'existe pas pour H4), ni
probabilités hors échantillon, ni base de comparaison. Transférer
les coefficients ou le seuil H1 vers H4 serait un mélange de
timeframes interdit.

## Conséquences méthodologiques

- Effectifs : même avant filtrage, l'évaluation H4 (130) et sa
  classe minoritaire historique (18 reprises absentes) sont sous
  les critères de non-évaluabilité déjà utilisés dans le
  programme ; après un hypothétique filtre primaire, les effectifs
  utiles seraient très inférieurs à ceux de H1 (443 en évaluation).
- Séquence obligatoire pour toute piste H4 future : d'abord un
  protocole prédictif propre (détection, modèle primaire,
  confirmation indépendante), ensuite seulement un meta-modèle
  économique — chaque étape sous décision et préenregistrement
  distincts.
- **Conclusion du bilan : branche H4 NON FAISABLE en l'état pour
  un équivalent de la Phase 17** ; aucun entraînement, aucun
  pooling H1/H4, aucune échéance proposée. Ce bilan ne crée ni
  droit ni obligation de l'ouvrir un jour.
