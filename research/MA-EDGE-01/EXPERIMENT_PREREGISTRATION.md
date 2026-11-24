# MA-EDGE-01 — Préenregistrement des expériences (figé avant calcul, seq404)

Cible primaire de la mission : payoff net réalisable (contrat 19-B/24-D), jamais un label seul.

- EXP-01 (Niveau 2, géométrie d'horizon) : pour les événements M15 d'évaluation et de calibration,
  rendement Mid signé dans le sens de l'impulsion depuis la clôture de décision aux horizons
  4/8/16/32 barres M15, stratifié par terciles du score gelé (frontières fixées sur la calibration).
  Question : le score classe-t-il le payoff à un horizon plus court que 8 h ?
- EXP-02 (Niveau 1, saisonnalité horaire) : rendement Mid moyen par heure UTC sur barres M15
  2010-2019, stabilité en deux moitiés (2010-2015 / 2016-2019). Aucune heure ne sera
  sélectionnée comme règle ; simple cartographie avec exigence de signe constant.
- EXP-03 (Niveau 1/2, compression asiatique) : range de la session 00:00-08:00 UTC en terciles
  roulants (250 jours précédents) ; rendement signé 08:00-16:00 dans le sens du mouvement
  asiatique et en sens inverse. Question : continuation ou retour à la moyenne après compression ?
- EXP-04 (Niveau 1, géométrie premier passage) : sur les événements sélectionnés 24-D,
  barrières symétriques ±20/±30/±50 bp depuis le prix de décision (barres M15 High/Low) :
  probabilité que la barrière favorable soit touchée en premier (ambiguïté même barre comptée
  à part). Aucune sortie ne sera construite à partir du vainqueur observé.
- EXP-05 (données) : faisabilité GVZ J-1 / COT — test de canal d'acquisition seulement, aucun
  résultat économique sans données vérifiées.

Règles : splits historiques inchangés ; aucun seuil optimisé ; multiplicité documentée ;
tout résultat = EXPLORATORY_POST_HOC.
- EXP-06 (Niveau 1, ajouté avant calcul) : P&L S2 24-D par direction LONG/SHORT et par taille de
  grappe (événement isolé vs groupé). Aucune règle ne sera tirée d'un sous-groupe isolé.
