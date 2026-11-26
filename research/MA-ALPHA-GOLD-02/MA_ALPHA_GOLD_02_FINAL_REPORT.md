# META ALPHA GOLD-02 — RAPPORT FINAL : COMMENT L'ARGENT SE GAGNE SUR L'OR

## La réponse à la question posée

**Un opérateur gagne de façon répétée sur XAUUSD en étant payé par quelqu'un d'identifiable** :
par le participant impatient (fourniture de liquidité — le reflux post-impulsion vaut
exactement le spread, ≈ 2,3 bp, que le preneur d'ordres au marché *paie* au lieu de le
recevoir), par l'acheteur de protection (prime de variance mesurée sur l'or : l'implicite
dépasse la réalisée suivante de +2,0 points en médiane), par le hedger qui transfère son risque
(hedging pressure des futures, documentée par la littérature, instable comme règle hebdomadaire
chez nous), ou par la gestion du risque des autres (la dérive des positions non confirmées,
−31 bp, que notre deadline préenregistrée cherche à tronquer en observation prospective).
**Aucun de ces revenus n'est accessible à un ordre au marché envoyé après un signal** — et c'est
exactement la position que META ALPHA a occupée pendant 25 phases. Voilà le mécanisme derrière
nos échecs répétés, démontré cette fois chiffres à l'appui plutôt que soupçonné.

## Ce que ce cycle a établi

- **Audit forensique des 47 règles** : correction honnête — deux règles étaient positives sur
  trois périodes, dont une (dérive 17-22h, ≈ +1 bp) sous les coûts ; 19 règles positives sur
  deux périodes montrent combien de faux edges un critère plus faible aurait livrés.
- **La « journée extrême » est déclassée** : sa moyenne (+24 bp) est portée par 5 événements
  (140,6 % du profit) avec un expected shortfall de −485 bp. C'est une prime de queue, pas un edge.
- **Les grilles sont réfutées par nos données** : 62 % de journées gagnantes, queue à −1 112 bp.
- **Aucun portefeuille rentable n'est présenté.** Le portefeuille 60/25/15 précédent est
  explicitement requalifié en allocation expérimentale ; il ne reste qu'une jambe de gestion en
  test prospectif (deadline 120 min, préenregistrée, en collecte) et une jambe de connaissance
  chiffrant les primes inaccessibles pour décider un jour, en connaissance de cause, si leurs
  licences vaudraient leur prix.

## Pour la livraison du 1er décembre

La communauté reçoit la carte des mécanismes, les mesures et les réfutations de ce dossier, et
le test prospectif en cours — sans promesse de rentabilité. La prochaine vérité de META ALPHA
viendra de la population prospective de la deadline (≈ 350 événements), ou d'une décision
d'accès aux instruments qui paient (options, futures, carnet) que seul le fondateur peut prendre
en connaissance des coûts documentés ici.
