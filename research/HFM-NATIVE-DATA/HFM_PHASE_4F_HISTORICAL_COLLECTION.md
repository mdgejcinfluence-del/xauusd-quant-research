# PHASE 4F — COLLECTE HISTORIQUE : DÉCISION D'ARCHITECTURE FINALE

- **HFM natif sans compte : inexistant** (démontré 4A/4B). Dataset `hfm-xauusd-native` : rien à
  publier, et rien ne sera publié sous ce nom sans données HFM prouvées.
- **Externe tick** : Dukascopy demeure la référence tick Bid/Ask du projet (corpus certifié,
  collecte prospective active) — catégorie `xauusd_external_reference`, jamais étiquetée HFM.
- **HistData** : adaptateur `extpilot` prêt ; collecte mensuelle 2009→ à lancer depuis un
  environnement non filtré (poste du fondateur, 30 lignes de commande documentées dans le
  collecteur), puis stockage privé séparé avec provenance `EXTERNAL_REFERENCE/HistData`,
  Bid seul si l'en-tête pilote le confirme — jamais de republication publique sans revue de licence.
- **Prospective HFM** : si le fondateur ouvre un jour un compte HFM, le Tick Chart Trader ou
  l'adaptateur MT5 existant alimenteront `HFM LIVE/SHADOW` en ticks Bid/Ask TSV depuis le
  démarrage — sans jamais prétendre reconstruire le passé.
Verdict de mission : voies HFM sans compte épuisées et prouvées vides ; architecture multi-sources
livrée ; corpus externe réel déjà en place (Dukascopy) ; aucun arrêt du travail quantitatif,
aucune confusion de provenance.
