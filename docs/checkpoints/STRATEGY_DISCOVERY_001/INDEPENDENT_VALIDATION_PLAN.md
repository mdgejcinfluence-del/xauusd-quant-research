# PLAN DE VALIDATION INDÉPENDANTE

1. Geler V2 (présente spécification + empreinte du moteur) — fait à ce checkpoint.
2. Source : nouveaux paniers réels de Colorful drops via captures publiques
   (poste ordinaire, cadence ≤ 15 min en session ; CI = 403, aucun contournement).
3. Protocole par panier : classer d'abord (cas discriminants seq443/447/449),
   comparer ensuite aux moteurs gelés V1/V2 sans retoucher aucun seuil.
4. Critères : fidélité d'entrée (±120 s), de gestion (positions, délais,
   renforcements), de clôture (écart de durée et de prix), faux paniers dans les
   fenêtres couvertes uniquement.
5. Aucune réinjection d'un résultat prospectif dans le modèle avant classement.
6. Échantillon minimal avant tout verdict : à fixer par la variabilité observée ;
   en dessous, rapporter les cas un par un sans score global trompeur.
