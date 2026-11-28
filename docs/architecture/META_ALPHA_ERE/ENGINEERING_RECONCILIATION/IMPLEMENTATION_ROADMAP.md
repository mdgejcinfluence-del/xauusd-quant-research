# RÉCONCILIATION — FEUILLE DE ROUTE (proposée, non commencée)

Chaque étape est une mission séparée, préenregistrée, avec son propre
checkpoint. **Rien ne démarre avant validation du fondateur** sur ce
dossier et sur les décisions d'ERE-REVIEW-002 encore ouvertes.

| # | Étape proposée | Livrable | Déclencheur / dépendance |
|---|---|---|---|
| 0 | Validation fondateur : ce dossier + taxonomie N0–N7 + corrections 1–7 | décisions journalisées | immédiat |
| 1 | Schémas exécutables des contrats (base externe amendée) + contrôles inter-objets + tests négatifs | schémas versionnés ; dossier Colorful migré en exemple | 0 |
| 2 | Objets socles : `DossierState`, `MarketWindow`, `AvisDeTestabilite` | reprise formelle d'un dossier | 1 |
| 3 | Benchmark calcul : pandas actuel vs un candidat (DuckDB *ou* Polars) sur une tâche réelle | rapport de mesure ; adoption ou rejet motivé | besoin mesuré |
| 4 | Lock reproductible CI (hashes) + audit licences | environnement figé et vérifiable | 1 |
| 5 | F découpé (catalog/index/signatures/execute) sur le pipeline CI existant | capacité matrix par segment | 2 |
| 6 | Qualification Kaggle-kernels (synthétique uniquement) si le fondateur la souhaite | rapport de qualification ou abandon motivé | décision fondateur dédiée |
| 7 | Deuxième dossier trader complet A→G | preuve de réutilisabilité | 1–5 |
| 8 | Porte H pour ME-001 | uniquement si la validation prospective (règle seq486) conclut | collecte catégorie D en cours |

**Explicitement pas au programme** : option distribuée, GPU, SBI,
optimisation de paramètres, plateforme temps réel, connectivité
broker, automatisation des verdicts.
