# META ALPHA ERE — QUESTIONS OUVERTES ET DÉCISIONS DU FONDATEUR

## Décisions demandées au fondateur

1. **Validation de la conception** : les neuf modules et leurs
   frontières (notamment la porte du module H) correspondent-ils à la
   vision ? Sans ce oui, aucune implémentation ne commence.
2. **Deuxième dossier trader** : quel prochain trader/robot alimenter
   en module A (source publique de transactions + bio + statistiques),
   ou faut-il d'abord industrialiser l'existant (étapes 1–3) ?
3. **Cotations HFM réelles (ME-004)** : autoriser une collecte sur
   compte démo (aucun ordre) pour ouvrir le modèle liquidité, ou
   différer ?
4. **Moteur de calcul du corpus** : investir dans l'évaluation
   DuckDB/Polars (étape 3) maintenant, ou rester sur le pipeline CI
   actuel qui suffit aux protocoles par partition ?
5. **Critères de la porte H** : le niveau FORTEMENT ÉTAYÉ + signature
   + queue caractérisée suffit-il, ou exiger directement un verdict
   prospectif favorable (position actuelle, plus stricte) ?

## Questions scientifiques ouvertes (consignées, non bloquantes)

- Représentation formelle des ensembles d'hypothèses équivalentes
  (graphes de prédictions divergentes) : à concevoir avec l'étape 4.
- Mesure du gain d'information attendu sans probabilités arbitraires :
  pistes par ensembles compatibles et pouvoir discriminant des tests.
- Traitement unifié de la censure dans les contrefactuels (renforcements, horizons).
- Définition d'un « régime » partageable entre modèles du portefeuille.

## Risques et dépendances

Fournisseur de données unique (Dukascopy/Drive) ; disparition possible
des phénomènes mesurés (ME-001 attend son épreuve prospective) ;
dépendance à l'agent pour l'orchestration (les verdicts restent
humains/fondateur en dernier ressort) ; coût CI des gros replays.
Aucune dépense engagée par cette conception.
