# PHASE 23-A — RECOMMANDATION FINALE

Statut : `EXPLORATORY_RESEARCH_DESIGN`. Verdicts au registre seq385.

## Réponse à la question de clôture

Les informations externes réellement obtenables, horodatées et alignables causalement à budget
0 FCFA sont limitées et précises :

1. **Contexte quotidien connu la veille (FRED/ALFRED, libre)** : variation du dollar large
   (DTWEXBGS), du taux 10Y nominal (DGS10) et du taux réel 10Y (DFII10), chacune strictement en
   J-1. Mécanismes théoriques distincts, aucun signe présumé. Verdict famille A/B :
   `NEW_CAUSAL_EXTERNAL_INFORMATION_AVAILABLE` à fréquence quotidienne décalée,
   `HISTORICAL_TIMESTAMP_LIMITATION` pour tout usage intrajournalier.
2. **Fenêtres d'événements macro à heure fixe (calendriers officiels, libres)** : CPI/PCE/NFP
   08:30 ET, FOMC 14:00 ET — connues à l'avance, donc causales comme variables de régime
   d'annonce. En revanche, **aucune surprise économique n'est calculable** : le consensus
   contemporain n'existe pas en libre avec provenance vérifiable (`SOURCE_OR_LICENSE_BLOCKED`).
   Les valeurs de première vintage ALFRED sont utilisables uniquement après l'heure exacte de
   publication.
3. **Marché futures GC** : prix, volume et open interest historiques sont licenciés CME et
   payants → `SOURCE_OR_LICENSE_BLOCKED` à budget 0. Seul le calendrier des échéances est causal
   et libre. Ne jamais assimiler le volume GC au spot.
4. **Calendrier** (fériés US, DST, échéances) : `CAUSAL_HISTORY_VERIFIABLE`, mais risque de
   redescription de régimes déjà cartographiés (20-A/21-C) ; à n'utiliser qu'en contrôle.

## Ce qui est explicitement écarté

- Tout usage le jour même des valeurs quotidiennes FRED (fuite temporelle : publication J+1).
- Toute surprise macro reconstruite a posteriori, tout consensus inventé.
- Tout DXY/GC intrajournalier « gratuit » sans licence ni provenance vérifiable.
- Toute prétention de validation indépendante : les événements XAU/USD 2010-2020 restent les
  mêmes que ceux des phases 20-22 ; la holdout 2020-2026 demeure fermée.

## Suite autorisable (non lancée)

Une extraction ultérieure exigerait un contrat distinct avec liste fermée, par exemple :
{variation DTWEXBGS J-1, variation DGS10 J-1, variation DFII10 J-1, fenêtre CPI/NFP, fenêtre FOMC,
échéance GC}, alignement causal horodaté, et question préenregistrée sur l'amplitude/asymétrie
conditionnelle — sans modèle ni P&L à ce stade. Aucune extraction n'est lancée par cette phase.
