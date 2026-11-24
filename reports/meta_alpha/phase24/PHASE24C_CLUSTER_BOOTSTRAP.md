# PHASE 24-C — BOOTSTRAP PAR GRAPPE

Méthode : 10 000 réplications (graine 2123) rééchantillonnant les **grappes complètes**
(fenêtres d'observation chevauchantes regroupées), tous les événements d'une grappe conservés
ensemble ; différences appariées de Brier et de Log Loss sur exactement les mêmes événements
d'évaluation. Aucune précision calculée en traitant les événements comme indépendants.

Résultats (différence conditionnel − généraliste TIME_ONLY, même cohorte ; négatif = le
conditionnel est meilleur) :

- Cohorte H4_TIME (139 événements, 45 grappes) : ΔBrier **+0,0105**, IC95 [+0,0008 ; +0,0208] ;
  ΔLogLoss IC95 [+0,0044 ; +0,0466]. L'intervalle exclut zéro dans le mauvais sens : le
  réentraînement conditionnel H4 est **significativement moins bon** que le généraliste appliqué
  aux mêmes événements.
- Cohorte D1_TIME (198 événements, 59 grappes) : ΔBrier **+0,0100**, IC95 [−0,0008 ; +0,0209] ;
  ΔLogLoss IC95 [−0,0021 ; +0,0448]. Aucune amélioration ; l'intervalle est compatible avec un
  effet nul ou négatif.

Les deux conditionnels battent leur M0 propre (Brier 0,210 et 0,227 contre 0,248) : la sélection
d'une population énergétique porte un signal, mais le **réentraînement conditionnel n'ajoute
rien** — il dégrade même la prédiction par rapport au modèle généraliste entraîné sur 4 733
événements. C'est l'effet classique de variance d'estimation sur petites cohortes.
