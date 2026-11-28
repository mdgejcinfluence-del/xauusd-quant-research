# MOTEUR AUTONOME META ALPHA — Rapport de consolidation et de qualification

Dossier externe lu intégralement (`DOSSIER_META_ALPHA_RESEARCH_001.html`,
SHA-256 `a791be92…`) : étude honnête qui déclare ses tests synthétiques
et recommande, comme nous, un monolithe modulaire à journal durable
(option A) contre les microservices (option B). Ses recommandations
retenues : noyau durable + workers jetables, trois mémoires, vieillissement
des connaissances, prévision probabiliste explicite. Écartées : toute
variante « ARENA-native » (capacités non vérifiées — il le dit lui-même),
PostgreSQL/Temporal (concurrence non démontrée), les bibliothèques de
prévision lourdes (aucun bénéfice mesuré chez nous).

## Ce qui a été construit (réel, testé)

| Composant | État avant | Travail réalisé | Tests | État final |
|---|---|---|---|---|
| Noyau autonome | absent (scripts + registre) | `ere/kernel.py` : tâches idempotentes par hash, journal d'événements chaîné, budgets, reprise | reprise + journal + budget | **opérationnel (mono-worker, SQLite)** |
| Agenda / prochaine recherche | choix humain | priorisation par hypothèses départagées/coût, zéro sans segment autorisé | cycle | **opérationnel** |
| Mémoire | documents + manifeste | 3 mémoires via le noyau : épisodique (événements), sémantique (connaissances versionnées, STALE sans effacement), procédurale (méthodes des moteurs) | STALE + historique | **opérationnelle** |
| Recherche scientifique | pratique manuelle | `ere/cycle.py` : OBSERVE→…→SELECT_NEXT exécutable, ≥2 hypothèses + nulle, critères gelés avant exécution | monde sans signal → NOT_IDENTIFIED ; monde à régimes → H-REGIME retenue | **opérationnel sur séries fournies** |
| Incertitude | néant | `ere/uncertainty.py` (INTELLIGENCE-001) | bornes, fiabilité, priorisation | opérationnelle |
| A–I | pratique + fonctions | inchangés, renforcés par intake/kernel | 16 tests moteurs/contrats | conservés, frontières intactes |
| N0–N7 | documentée | autorités codées, inchangées | promotion interdite testée | **préservés** |
| Corpus | inventaire certifié | campagnes CI (INTEL2 : persistance de volatilité invariante) | reproductibles par manifeste | exploité par échantillonnage stratifié |
| Prévision | absente | `ere/forecast.py` : quantiles passés, couverture hors échantillon | synthétique + réel | **baseline calibrée : couverture 79,6 % pour 80 % nominal** (927 prévisions, ticks nov. 2026) |
| Stratégies | V1/V2 gelés rejetés | aucune nouvelle (aucun mécanisme N5) | porte H testée fermée | inchangé, honnête |
| Validation I | jamais exercée | refuse tout positif sans segment indépendant | testé | indépendante, en attente d'un objet légitime |
| ARENA | supervision en session | aucune API présumée ; le noyau vit dans le dépôt + SQLite local/CI | — | superviseur, pas source de vérité |
| Reprise | par protocole | tâches INTERRUPTED→PENDING sans duplication | testé | **démontrée en test** |

## Réponses condensées aux 20 questions du rapport final

L'architecture d'avant était un ensemble de scripts gouvernés ; les
parties externes retenues sont le noyau durable, les trois mémoires et
la prévision explicite ; le reste (services, workflow engines, modèles
lourds) est écarté faute de besoin démontré. La prochaine recherche est
choisie par score d'information/coût sous contrainte de segment
autorisé. Quand une donnée manque, le moteur borne, conditionne et
poursuit sur l'identifiable (TRADER-CANDIDATE-002 en est la preuve
vécue). Le corpus est exploité par partitions via la CI sans jamais
charger 685 M de ticks en mémoire. Recherches réelles exécutées :
ME-001 à ME-003 (registre), découverte INTEL2, baseline de volatilité.
Hypothèses réfutées conservées : fade symétrique, continuation à
horizons fixes, asymétrie de volatilité (×2), contraction→expansion.
**Aucune stratégie n'a passé de validation indépendante** ; les
capacités non qualifiées sont : exécution multi-workers, prévision
directionnelle, tout mécanisme N5+, et l'autonomie sans session
(le noyau persiste dans Git/SQLite, mais aucun ordonnanceur permanent
n'existe dans notre environnement — limite documentée, pas contournée).
Coûts observés : secondes à minutes de CI par partition, zéro dépense.

## Verdict de qualification

Le moteur sait chercher, réfuter, se souvenir, reprendre et choisir sa
prochaine question dans les limites de ses gates. Il ne sait pas encore
produire un mécanisme exploitable — parce que les données, à ce jour,
ne lui en ont pas donné un qui survive. C'est un laboratoire autonome
fonctionnel, pas une machine à alpha : exactement ce qui était demandé.
