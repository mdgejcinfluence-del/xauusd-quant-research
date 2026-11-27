# META ALPHA ERE — FEUILLE DE ROUTE DE RÉALISATION

Ordre justifié par la valeur scientifique par unité d'effort. **Aucune
étape ne commence avant la validation du fondateur sur cette
conception**, puis chaque étape produit son propre checkpoint.

| # | Étape | Livrable | Dépend de |
|---|---|---|---|
| 0 | Validation de la présente conception par le fondateur | décisions consignées (OPEN_QUESTIONS) | — |
| 1 | Schémas de dossiers (A/G) + validation automatique | `TraderDossier`/`ModelDossier` JSON schématisés ; le dossier Colorful migré comme exemple | 0 |
| 2 | Registre d'expériences interrogeable | index des protocoles gelés et de leurs segments (depuis le ledger existant) | 1 |
| 3 | Couche corpus à cache de barres | barres 5 s par partition avec provenance/hash ; benchmark DuckDB vs pandas sur une tâche réelle | 0 |
| 4 | Moteur d'hypothèses assisté (C) | génération de fiches concurrentes à partir d'un BehaviorProfile, avec contrôles de complétude | 1 |
| 5 | Planificateur d'expériences (E) | classement information/coût des expériences candidates, génération du préenregistrement | 2, 4 |
| 6 | Deuxième dossier trader complet (A→G) | preuve de réutilisabilité sur un cas nouveau, sans code spécifique | 1–5 |
| 7 | Porte du module H pour ME-001 | uniquement si et quand la validation prospective seq486 conclut favorablement | collecte D en cours |
| 8 | Validation & portefeuille (I) | activé par le premier moteur indépendant | 7 |

## Ce qu'il ne faut pas construire maintenant

Automatisation complète du module C (le jugement d'hypothèse reste
supervisé), plateforme temps réel, connectivité broker, optimisation
de paramètres, interface graphique élaborée : aucun ne réduit
l'incertitude scientifique actuelle, qui est **l'attente de données
prospectives** et l'arrivée d'un second dossier trader.
