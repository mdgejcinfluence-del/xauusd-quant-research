# BACKTEST-2026-001 — COMPARAISON DES MOTEURS

1. **Meilleur net** : V1 (−30,40 vs −33,24 USD modèle, couverture B).
2. **Meilleur profit factor** : V1 (0,528 vs 0,371).
3. **Drawdown le plus faible** : V1 (−31,09 vs −33,45).
4. **Meilleure espérance/panier** : V1 (−0,0074 vs −0,0101) — toutes deux négatives.
5. **Sensibilité aux coûts** : V2-F2 perd davantage dès S1 en relatif
   (S0→S3 : V1 −30,4→−131,2 ; V2 −33,2→−113,0 en absolu, mais V2 part
   plus bas avec moins de paniers ; par panier, dégradation comparable).
6. **Concentration des pertes** : V2-F2 — série de 62 pertes consécutives
   (V1 : 40), mois d'août −8,90 (pire mois des deux moteurs).
7. **Cohérence mensuelle** : pertes quasi généralisées (V1 : 9 mois
   négatifs, juin +0,83 seul positif ; V2-F2 : 10/10 négatifs sur les
   mois couverts). Le négatif ne dépend pas d'une période unique :
   janvier–février concentrent ~53 % des pertes de V1, mais tous les
   scénarios et presque tous les mois confirment le signe.
8. **Dépendance à une période** : non déterminante — retirer le pire
   mois (août) laisse les deux moteurs nettement négatifs.

## Comparaison avec Colorful drops (mondes séparés)

- **Réel observé** : 5 paniers, +22 ¥ affichés sur 2 jours (novembre).
- **Public dynamique** : +6,01 ¥/transaction d'espérance affichée —
  UNVERIFIED, non transactionnel.
- **Simulé V1 / V2-F2** : négatifs ci-dessus.
Aucune similarité ou divergence de rendement ne prouve ni ne réfute
l'identité du mécanisme ; nos moteurs sont des reconstructions
partielles (CTRS-007, verdict B) dont la sortie de premier passage est
déjà réfutée comme mécanisme réel.
