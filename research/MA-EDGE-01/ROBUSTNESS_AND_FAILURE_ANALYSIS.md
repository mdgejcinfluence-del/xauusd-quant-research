# MA-EDGE-01 — 09 · ROBUSTESSE ET ANALYSE DES ÉCHECS

Taxonomie des échecs du programme, causes probables et preuves :

- **Cible mal posée** (cause dominante, démontrée en 24-E) : les labels de trajectoire
  (reprise, premier passage) sont réalisés tôt et capturables (+11,36 bp conditionnellement),
  mais la sélection complète perd (−3,31 bp) parce que 36 % de faux positifs dérivent à
  −31,29 bp. Optimiser P(label) n'optimise pas E[payoff].
- **Amplitude sans direction** : chaque phénomène d'amplitude découvert (H4, D1, FOMC, score)
  est bidirectionnel ; les MFE/MAE restent symétriques à tous les horizons testés (EXP-04 :
  39,8 % contre 42,6 %).
- **Instabilité temporelle** : les rares poches positives changent de signe entre sous-périodes
  (classe de score [0,56 ; 0,60) : +3,28 puis −3,27 ; compression asiatique : +5,28 puis −1,83 ;
  permission D1 : −7,88 puis +5,05). Aucune n'a survécu à une seconde lecture.
- **Petites cohortes et dépendance** : les conditionnements intéressants laissent 40-60 grappes ;
  les intervalles par grappes ont tué plusieurs résultats apparemment positifs (24-C).
- **Coûts** : les pertes persistent en S0 — les coûts aggravent mais n'expliquent pas les échecs.
- **Exécution** : délais d'entrée médians < 1 s sur les audits tick ; l'exécution n'est pas le
  facteur limitant identifié.
- **Biais évités et documentés** : multiplicité (familles BH), holdout consommé jamais rouvert,
  seuils jamais choisis sur l'évaluation dans les phases récentes, post-hoc étiqueté.

Risque résiduel principal pour la suite : la deadline de non-réalisation (H05) est née de
l'observation des données consommées ; la tester sur ces mêmes événements sans protocole gelé
reproduirait exactement le biais que ce programme a appris à éviter.
