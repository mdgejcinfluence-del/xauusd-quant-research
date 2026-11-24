# PHASE 23-C — RÈGLE CANDIDATE FIGÉE (validation prospective uniquement)

Gelée par seq388/seq389, avant toute consultation de futurs événements. Aucune modification
autorisée sans nouvelle phase préenregistrée.

- t0 : publication officielle FOMC 14:00 ET, convertie en UTC avec le calendrier DST historique US.
- P0 : dernier Mid valide strictement avant t0 (âge ≤ 300 s, sinon événement non validable).
- P15 : premier Mid réel à/après t0+15 min (retard ≤ 300 s, sinon non validable).
- Direction : LONG si P15 > P0 ; SHORT si P15 < P0 ; aucune décision si égalité.
  Aucun filtre de taille, aucun seuil.
- Décision à t0+15 min ; entrée : LONG au premier Ask réel strictement après l'instant de
  décision, SHORT au premier Bid ; délai maximal 60 s, sinon `NON_EXECUTION`.
- Sorties fixes, évaluées séparément : t0+60 min et t0+240 min (premier Bid pour un LONG,
  premier Ask pour un SHORT, à/après la cible, retard ≤ 300 s sinon sortie non validable).
- Aucun stop-loss ni take-profit dans cette règle d'observation.
- Coûts : comptabilité 19-B, spread intégré une fois ; slippage S0 = 0, S1 = 0,5, **S2 = 1 bp/côté
  (principal)** ; commissions exclues. Résultats nommés
  `HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`.

État historique (développement, 73 événements consommés) : continuation après 15 min de 52,1 %
(60 min) ; résultat hypothétique S2 moyen −7,8 bp à 60 min et +0,2 bp à 240 min (médianes
négatives). La règle est donc figée comme **hypothèse à réfuter ou confirmer sur événements
nouveaux**, non comme un edge : l'historique ne la soutient pas à 60 minutes et est neutre à
240 minutes.
