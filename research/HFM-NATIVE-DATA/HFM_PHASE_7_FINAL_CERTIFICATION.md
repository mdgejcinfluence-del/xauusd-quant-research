# PHASE 7 — CERTIFICATION FINALE (partielle et honnête)

## Réponses aux 15 questions du rapport final
1. HFM permet-il d'obtenir l'historique depuis 2010 ? **Non démontré** — le serveur n'a pas pu
   être interrogé (pas d'identifiants, pas de terminal Windows dans cet environnement).
2. Première date récupérable : **inconnue** ; le mode `probe` la mesurera par TF et pour les ticks.
3. Ticks collectés : **0**. 4. Ticks Bid/Ask : 0 (aucun corpus). 5. Couverture M1-D1 : aucune.
6. Trous : non mesurables sans données. 7. Périodes certifiées : **aucune**. 8. Indisponibles :
   toutes, au statut `UNAVAILABLE` (non obtenues), sans préjuger de ce que le serveur détient.
9. Méthodes qui fonctionnent : l'architecture MT5 + pipeline (validée en selftest synthétique).
10. Échecs : accès direct — identifiants absents et package MetaTrader5 Windows-only (échecs
    documentés et propres, aucune donnée fabriquée). 11. Structure Kaggle : définie, non publiée.
12. SHA-256 : mécanisme en place et testé ; rien à certifier. 13. Continuité automatique :
    possible sous terminal Windows allumé + reprise par manifeste ; non active aujourd'hui.
14. Coûts : 0 € engagés. 15. Dépendances restantes : **identifiants HFM Pro du fondateur en
    secrets d'environnement + un poste/runner Windows avec MT5** ; puis probe → pilote → collecte.

## Statuts
Toutes périodes/granularités : `UNAVAILABLE` (non collectées). Aucune période `CERTIFIED`.
Corpus Dukascopy : intact (vérifié par non-modification). Verrous META ALPHA : respectés.
Ce livrable est une infrastructure prête et un blocage documenté — pas une « collecte terminée ».
