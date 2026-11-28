# ARCHITECTURE RECONCILIATION 001 — Matrice d'intégration de l'étude externe

Étude lue intégralement : `META_ALPHA_Etude_Architecture_Autonomie.md`
(SHA-256 `eb0d6e13…`). Elle est de bonne qualité et honnête : elle
déclare n'avoir audité ni le dépôt ni le corpus. La présente matrice
fait l'audit qu'elle n'a pas pu faire, composant par composant, contre
le code réel (branche `arena/afe12737…`, HEAD `0435207`, descendant
vérifié de `9c4f9a6` ; `main` à `98bfd359` ; 31/31 tests rejoués).

Légende : **VÉRIFIÉ** / **INCOMPLET** / **À RENFORCER** / **À CONSTRUIRE**
/ **NON DISPONIBLE** / **BLOQUÉ (autorisation externe)**.

## 1. Matrice de réconciliation

| Composant de l'étude | État réel (fichier, symbole, preuve) | Statut | Delta exact à produire |
|---|---|---|---|
| Plan de contrôle durable (noyau) | `ere/kernel.py: Kernel` — tâches, journal chaîné, budgets, reprise ; tests `test_kernel_cycle.py` | INCOMPLET | leases/epochs, outbox, états de tâche enrichis (voir §2) |
| Journal d'événements chaîné | `Kernel._log`, `verify_journal` (chaîne des prev_hash) | VÉRIFIÉ (mono-processus) | ancrage externe périodique de la tête (non fait) ; le `ts` n'est pas couvert par le hash — limite connue |
| Idempotence | `create_task` par hash de spec ; `TaskRunner` shards (`ere/runner.py`) | VÉRIFIÉ | étendre la clé aux appels externes (outbox) |
| Reprise après interruption | `resume_interrupted()` RUNNING→INTERRUPTED→PENDING | VÉRIFIÉ en test | reprise *hors session* : aucun processus ne relance le noyau — NON DISPONIBLE aujourd'hui |
| Budgets | `BudgetExceeded` sur nombre de tâches | INCOMPLET | ledger par mission (réservé/consommé/incertain), budgets CPU/données/appels |
| Leases et fencing tokens | absents (recherche `lease`/`fencing` : vide) | À CONSTRUIRE | claim atomique + epoch monotone + rejet des anciens workers |
| Ordonnanceur / réveil automatique | aucun service ; la CI `schedule` existe mais GitHub n'exécute les crons que depuis la branche par défaut — notre workflow y est présent via `main` historique, la collecte prospective fonctionne ainsi | NON DISPONIBLE pour un réveil du noyau | service mono-hôte autorisé (systemd ou équivalent) + watchdog — **BLOQUÉ : autorisation + hôte à décider par le fondateur** |
| Workers éphémères | GitHub Actions joue ce rôle pour les campagnes (jobs CI bornés, résultats committés) | INCOMPLET | enveloppe de tâche formelle (limites, hash d'entrée) déjà partielle via `TaskRunner` |
| Broker API ARENA | aucun client API ; l'agent opère en session Agent Mode | À CONSTRUIRE, **BLOQUÉ** | campagne de tests B.3 de l'étude seulement après : clé connue du fondateur, plafond écrit, politique de données approuvée. **Aucune clé n'a été demandée, reçue ni manipulée dans cette mission** |
| Multi-agents (8 rôles) | aucun ; un seul agent en session | À CONSTRUIRE (plus tard) | les rôles sont des *fonctions* du cycle avant d'être des agents ; ne pas créer d'armée d'agents (l'étude le dit aussi) |
| Boucle de recherche ouverte | `ere/cycle.py: run_cycle` — OBSERVE→SELECT_NEXT, hypothèses + nulle, critères gelés | INCOMPLET | déduplication canonique des hypothèses, score versionné, méta-recherche quand le portefeuille est vide |
| Méta-recherche / mission ouverte | le cycle sélectionne une prochaine recherche mais aucune « mission » persistante n'existe comme objet | À CONSTRUIRE | objet Mission (OPEN/PAUSED/CONCLUDED_WITH_EVIDENCE) dans le noyau ; une réfutation ne ferme jamais la mission |
| Mémoires ×3 | épisodique = journal ; sémantique = `put_knowledge/mark_stale` ; procédurale = cartes méthodes de D | INCOMPLET | relations typées (supports/contradicts/depends_on), domaines de validité structurés |
| Protocoles gelés | `ExperimentPlan.plan_hash` anti-modification, préenregistrements seq au registre | VÉRIFIÉ | classification exploratoire/confirmatoire explicite sur chaque plan |
| Gates N0–N7 | `ere/taxonomy.py` autorités de promotion, tests négatifs | VÉRIFIÉ | inchangés — l'étude les respecte, nous aussi |
| Validation I indépendante | `engine_ia_validate` refuse tout positif sans segment indépendant ; identité distincte non réalisée (même processus) | INCOMPLET | identité/stockage distincts au moment d'un premier objet légitime — pas avant |
| Holdout protégé | segmentation gelée + règle d'arrêt ME-001.4 (jamais accédée dans ces missions) | VÉRIFIÉ par discipline | ACL technique le jour où un service persistant existera |
| Rétro-ingénierie trader | TRADER-CANDIDATE-002 : N2, NOT_IDENTIFIED, fuseau UNKNOWN | VÉRIFIÉ | voie F aveugle déjà séparée ; rien à changer |
| Méthodes avancées (PyMC, ruptures, PySR, DoWhy, River) | aucune installée ; DuckDB retenu sur benchmark | À CONSTRUIRE au cas par cas | adoption seulement sur besoin mesuré + audit licences (déjà notre règle) |
| Prévision probabiliste | `ere/forecast.py` + audit : couverture 79,6 % vs 80 %, gain marginal sur le naïf | VÉRIFIÉ (partiellement qualifiée) | conformal adapté à la dépendance : candidat documenté, non installé |
| Sauvegardes / restauration | Git + manifestes SHA par checkpoint ; pas de sauvegarde SQLite testée | INCOMPLET | sauvegarde cohérente (API SQLite) + test de restauration avant tout service persistant |
| Observabilité / alertes | journaux CI + registre ; aucune métrique de santé du noyau | À CONSTRUIRE | compteurs minimaux (âge des tâches, leases, intégrité) avec le service |
| Sandbox du code généré | les scripts sont écrits par l'agent puis relus/testés ; pas de conteneur dédié | INCOMPLET | limites CI existantes (timeout des jobs) ; sandbox renforcée seulement si du code tiers est exécuté |

## 2. Ce que l'étude a vu juste — et ce qu'elle ne pouvait pas savoir

Juste : l'option A (service mono-hôte + SQLite + workers) contre le
distribué ; ARENA comme fournisseur de raisonnement interchangeable,
jamais autorité ; les appels API incertains (un timeout peut être
facturé) ; le fait qu'un cron GitHub ne vit que sur la branche par
défaut. Elle ignorait : que notre noyau, nos gates et nos campagnes
existent déjà et sont testés ; que la collecte prospective quotidienne
fonctionne par le workflow présent sur `main` ; que le corpus est
réellement accessible en CI par Drive. Ses « à construire » sont donc
pour moitié des « à renforcer » chez nous — et c'est précisément ce
que cette réconciliation établit.

## 3. Ordre exact d'implémentation proposé (dépendances et acceptation)

| # | Étape | Dépend de | Critère d'acceptation mesurable |
|---|---|---|---|
| 1 | Objet **Mission** + états (OPEN/PAUSED/CONCLUDED) dans le noyau ; une réfutation ne ferme pas la mission | noyau actuel | test : mission survivant à 3 réfutations, toujours OPEN |
| 2 | **Leases + fencing** (claim atomique, epoch, rejet d'ancien worker) | 1 | test : publication d'un worker à lease expirée refusée 100 % |
| 3 | **Outbox** d'appels externes (idempotence, rapprochement des incertains) | 2 | test : timeout simulé → coût « incertain », pas de retry aveugle |
| 4 | Sauvegarde SQLite cohérente + restauration testée + ancrage externe de la tête du journal | 1 | restauration en environnement vierge, journal vérifié |
| 5 | Déduplication canonique des hypothèses + score de sélection versionné + méta-recherche si portefeuille vide | 1 | 0 doublon exact sur scénarios figés ; tâche de méta-recherche créée automatiquement |
| 6 | Enveloppe worker formelle (limites CPU/temps/données) sur la CI existante | 2 | job dépassant son enveloppe tué et journalisé BLOCKED |
| 7 | **Broker ARENA** — seulement après autorisation écrite du fondateur (clé, plafond, politique de données) | 3 | `GET /v1/models` + inférence bornée tracés ; 403 → arrêt sans contournement |
| 8 | Service de réveil mono-hôte — seulement après décision d'hébergement du fondateur | 4, 6 | 72 h sans session, interruptions injectées, aucune double publication (recette H de l'étude) |
| 9 | Identité I distincte + coffre holdout technique | 8 | tentatives d'accès chercheur rejetées et journalisées 100 % |

Étapes 1–6 : réalisables dans l'environnement actuel, sans autorisation
nouvelle. Étapes 7–9 : **bloquées par des décisions externes** (compte
API, hébergement, budget) — elles ne seront pas simulées.

## 4. Ce qui ne sera pas fait

Pas de réécriture globale ; pas de microservices ; pas d'agents
multiples avant que les fonctions du cycle en aient besoin ; pas de
déclaration d'autonomie complète avant la recette sans session de
l'étape 8. Le critère final reste : recherche continue du modèle
économique, hypothèses nouvelles générées par le système, preuves
reproductibles — ou blocages nommés, jamais maquillés.
