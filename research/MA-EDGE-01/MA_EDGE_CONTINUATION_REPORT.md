# MA-EDGE-01 — RAPPORT DE CONTINUATION

Corrections d'audit apportées au rapport initial :

- **EXP-05 existe** et est désormais présentée avec les cinq autres expériences
  (`EXP05_RECONCILIATION.md`) ; elle se clôt par l'exécution de la Phase 25-B ci-dessous.
- **Reformulation du diagnostic central** (vérifiée contre les rapports originaux) : la formule
  « 25 phases ont optimisé les labels et jamais le payoff » était trop catégorique — les Phases
  13, 17-22 et 24-D/24-E ont bien étudié des résultats économiques et des coûts. Formulation
  corrigée et adoptée : *« Une part importante de l'architecture prédictive a été construite
  autour des labels de trajectoire, tandis que la sélection économique directe et la gestion des
  événements non réalisés n'ont pas produit de mécanisme robuste. »*
- **Portée des résultats négatifs** : chaque expérience de cette mission réfute uniquement
  l'hypothèse, les variables et le contrat testés (voir le registre mis à jour,
  `HYPOTHESIS_REGISTER_UPDATED.csv`, qui distingue réfutée / non démontrée / bloquée /
  insuffisamment couverte). Aucune conclusion universelle sur « les prix » n'est tirée.

Réponses aux questions de la continuation :

1. **GVZ apporte-t-il une information économiquement utile ?** Non, pas en calibration : les
   trois terciles perdent (−2,9 à −4,5 bp). Il échelonne gains et pertes ensemble.
2. **Le COT ?** Non plus : −2,5 à −5,4 bp par tercile en calibration ; hypothèse d'encombrement
   non soutenue.
3. **La deadline de non-réalisation a-t-elle un mécanisme défendable ?** Oui, un mécanisme de
   troncature de queue (les non-réalisés dérivent à −31,29 bp pendant que les réalisés
   confirment en 60 minutes médianes), documenté dans `NON_REALIZATION_DEADLINE_MECHANISM.md`.
4. **Peut-elle être testée sans fuite ?** Oui : l'absence de clôture confirmante à l'échéance
   est observable en temps réel ; la règle unique (120 min) est préenregistrée (seq407) avant
   toute observation nouvelle.
5. **Le SHADOW est-il prêt ?** Prêt et instrumenté (`SHADOW_OBSERVATION_DESIGN.md`, contrat
   JSON, scripts), **non activé** : aucun flux Bid/Ask gratuit et licite n'est connecté ; la
   borne prospective vérifiée est 2026-09-30T23:59:58.864Z ; taille requise calculée
   (≈ 196 événements indépendants, ≈ 350 sélectionnés / 140 grappes, ≈ 8 mois de collecte).
6. **Prochaine expérience la mieux justifiée ?** La collecte SHADOW de la deadline — c'est la
   seule hypothèse restante dont le mécanisme vise directement la cause mesurée des pertes et
   dont le test peut être indépendant.
7. **Existe-t-il une stratégie candidate sérieuse ?** Non. Nous restons au stade des hypothèses :
   une règle préenregistrée non testée, et deux sources externes réelles mais économiquement
   non séparantes. Rien de tout cela n'est une rentabilité validée.
