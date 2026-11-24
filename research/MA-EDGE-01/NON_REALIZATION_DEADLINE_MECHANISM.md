# MA-EDGE-01 — MÉCANISME DE LA DEADLINE DE NON-RÉALISATION (reconstruction 24-E)

Faits mesurés (Phase 24-E, événements sélectionnés 2018-2019) :

- Délai de réalisation du label chez les 719 réalisés : médiane **60 min**, P25 30 min,
  P75 135 min, P90 240 min, P95 300 min (délais calendaires, week-ends inclus) ; la distribution
  est très étalée — la médiane n'est pas une deadline « optimale », seulement un centre de masse.
- Les réalisés gagnent +12,50 bp à 8 h (et +11,36 au premier passage) ; les 405 non-réalisés
  perdent **−31,29 bp** à 8 h : l'écart entre les deux populations vaut ≈ 44 bp.
- Le moment de différenciation : par construction du label, un événement qui n'a pas produit de
  clôture confirmante après plusieurs heures a déjà consommé l'essentiel de sa fenêtre utile ;
  le MAE médian avant passage des réalisés n'est que de 8,6 bp, donc la perte des non-réalisés
  s'accumule **après** les premières heures, en dérive lente (durée médiane en perte : 295 min).
- Distinguabilité en temps réel : l'absence de clôture M15 confirmante à un instant donné est
  observable sans connaître l'issue (c'est une information de trajectoire courante, pas future).
  En revanche, on ne peut pas savoir à l'avance *quels* non-réalisés actuels réaliseront plus
  tard : 25 % des réalisés le font après 135 minutes.

Mécanisme économique proposé : la deadline ne prédit rien ; elle **tronque la queue gauche**
des événements dont la confirmation n'arrive pas, au prix de sacrifier les réalisations tardives
(environ 25 % des gains si l'échéance est à 120 min). Le gain net attendu dépend donc de trois
quantités mesurables prospectivement : part des pertes évitées après l'échéance, part des gains
tardifs sacrifiés, coût d'exécution supplémentaire nul (une seule sortie, déplacée).
