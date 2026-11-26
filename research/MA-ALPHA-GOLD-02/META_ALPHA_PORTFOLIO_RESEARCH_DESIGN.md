# DESIGN DU PORTEFEUILLE DE RECHERCHE (correction du portefeuille de simulation GOLD-01)

Correction explicite : la répartition 60/25/15 de GOLD-01 était une **allocation expérimentale
de budget de risque de simulation**, pas la preuve d'un portefeuille rentable ; elle est révisée.
Le portefeuille de recherche ne contient que des jambes à source de rendement nommée :
- **Jambe de gestion (prospective)** : deadline 120 min (+ bras H17 séparé) — source : troncature
  de la dérive mesurée des non-réalisations ; en collecte, aucun poids « validé ».
- **Jambe de connaissance (0 capital)** : mesure continue des primes inaccessibles (variance,
  hedging pressure) pour décider, chiffres à l'appui, si une licence vaudrait un jour son prix —
  décision fondateur, jamais automatique.
- **Retirées** : la jambe « journée extrême » (queue dominante) et toute pondération présentée
  comme une diversification (même actif, fenêtres chevauchantes).
Un portefeuille candidat n'existera que lorsqu'une jambe aura produit une espérance nette sur
population indépendante ; ses poids seront alors calculés en budget de risque avec corrélations
mesurées sur les périodes communes, plafonds de perte simultanée et règle d'arrêt écrite.
