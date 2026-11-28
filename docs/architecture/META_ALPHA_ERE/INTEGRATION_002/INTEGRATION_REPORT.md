# META ALPHA — MISSION 002 : Intégration de l'orchestration autonome ARENA → GitHub → Kaggle

Préenregistrement seq518, résultats seq519. Branche dédiée, `main` inchangée.
Légende des statuts : VÉRIFIÉ / IMPLÉMENTÉ NON ENCORE CERTIFIÉ / PARTIEL /
BLOQUÉ PAR AUTORISATION / NON IMPLÉMENTÉ / NON TESTÉ. Aucun résultat
synthétique n'est présenté comme résultat réel ; aucun test simulé n'est
présenté comme une démonstration.

## 1. Phase 1 — Audit de l'orchestration de référence (inspectée, pas supposée)

L'ingénierie expérimentée par le fondateur **est dans ce dépôt** ; chaque
mécanisme ci-dessous a été lu dans le code, pas reconstruit de mémoire.

| # | Question | Mécanisme réel inspecté | Statut |
|---|---|---|---|
| 1 | ARENA déclenche GitHub | L'agent (session) pousse un commit ou écrit un fichier déclencheur dans `import_trigger/*.txt` ; les workflows réagissent au `push` sur ce chemin (`.github/workflows/kaggle-check.yml`, `chain-demo.yml`, `kaggle_migrate.yml`). C'est le canal ARENA→GitHub existant : **Git est le bus de déclenchement**. | VÉRIFIÉ |
| 2 | GitHub pilote Kaggle | `ci_tools/kaggle_migrate.py` + `kaggle_verify.py` : le job CI authentifie l'API Kaggle (secrets `KAGGLE_USERNAME`/`KAGGLE_KEY`, token moderne KGAT en mode Bearer), télécharge depuis Drive, publie des datasets par lots. `reports/meta_alpha/KAGGLE_CHECK.json` : authentification réelle réussie, aucune valeur de secret affichée. | VÉRIFIÉ |
| 3 | Sauvegarde avant limite d'exécution | `kaggle_migrate.py: checkpoint(state)` commite `STATE.json` sur la branche **à chaque lot** ; jobs bornés (`timeout-minutes: 340` < limite de 6 h). Le travail est découpé en lots reprenables plutôt qu'en une exécution monolithique. | VÉRIFIÉ |
| 4 | Nouveau cycle | `chain-demo.yml` : un push déclenche `chain-a.yml` puis `chain-b.yml` (`workflow_call`, `needs`) — enchaînement prouvé par `reports/meta_alpha/chain/CHAIN_PROOF.txt`. `orchestrateur.yml` : `workflow_run` sur achèvement d'un workflow amont + `ci_tools/orchestrate.py` qui lit les checkpoints et journalise la prochaine action **autorisée** (jamais au-delà d'un gate). | VÉRIFIÉ |
| 5 | Transmission d'état entre cycles | **Par Git** : `STATE.json`, checkpoints et rapports commités par `github-actions[bot]` (`git pull --rebase` puis push). Aucune base externe requise. | VÉRIFIÉ |
| 6 | Récupération après interruption | État relu depuis le dernier commit ; lots déjà faits ignorés (`done=set(state['uploaded'])`) ; `Kernel.resume_interrupted()` côté noyau. | VÉRIFIÉ |
| 7 | Prévention des doubles exécutions | Idempotence par contenu (lots déjà uploadés sautés), commits conditionnels (`git diff --cached --quiet && exit 0`), et à partir de cette mission : groupe `concurrency: ere-cycle` (pas d'annulation en cours) + clés d'idempotence du noyau. | VÉRIFIÉ |
| 8 | Erreurs / interruptions | `sys.excepthook` écrivant `ERROR.txt`, commit d'état `if: always()` dans `kaggle_migrate.yml`, retries bornés avec attente dans `dl()`. | VÉRIFIÉ |
| 9 | Permissions requises | Workflows : `permissions: { contents: write }` uniquement. Secrets : `KAGGLE_USERNAME`, `KAGGLE_KEY` (présents, vérifiés par l'API réelle). `GDRIVE_SA_JSON`/`GDRIVE_ROOT_FOLDER_ID` : absents, non nécessaires (lecture Drive par liens publics). Aucun secret n'existe dans le code ni les logs. | VÉRIFIÉ |
| 10 | Surveillance / relance | `schedule:` (cron) présent dans `nr_collect.yml` et `phase10_all.yml` — **mais GitHub n'exécute les crons que depuis la branche par défaut** : ces planifications vivent sur `main` historique et servent la collecte prospective, pas le noyau ERE. Aucun watchdog ne relance le noyau ERE aujourd'hui. | PARTIEL |

**Conclusion de Phase 1** : le modèle cible du fondateur n'exige aucune
architecture de remplacement. Le patron éprouvé est : *ARENA décide et
pousse → GitHub exécute par lots bornés → l'état transite par commits Git →
Kaggle fournit le calcul lourd*. La mission 002 étend ce patron au noyau
ERE au lieu d'inventer un broker. Aucune clé API ARENA n'est nécessaire à
un mécanisme précis identifié : le canal agent→GitHub existe déjà (§12 de
la mission respecté).

## 2. Phase 2 — Contrat d'intégration

- **Lire une mission** : `Kernel.mission(id)` / export `reports/meta_alpha/ere_state/STATE.json` (committé par le cycle CI).
- **Autorisation** : META ALPHA (noyau) possède missions, budgets, gates N0–N7 ; ARENA propose et exécute des opérations autorisées, ne modifie ni règles ni budgets.
- **Déclencher** : push d'un déclencheur ou `workflow_dispatch` (`ere_cycle.yml`) ; les workers CI sont éphémères et bornés.
- **Transmettre les résultats** : commit Git signé par le bot + manifeste ; côté noyau, publication uniquement via `publish()` sous lease valide (fencing).
- **Appels externes incertains** : outbox — jamais de relance aveugle d'une opération UNCERTAIN (potentiellement facturée).

## 3–6. Phases 3–6 — Implémentation dans le noyau (sans réécriture)

Fichier modifié : `ere/kernel.py` (tables et méthodes ajoutées, API
existante inchangée ; 31 anciens tests toujours verts, 37/37 au total).
Nouveau : `tests/test_orchestration.py` (6 tests).

| Composant | Avant | Après | Statut |
|---|---|---|---|
| Objet Mission | absent (cycle sans mission) | `create_mission/mission/mission_transition`, états OPEN/PAUSED/CANCELLED/CONCLUDED_WITH_EVIDENCE, flux A/B séparés, `record_hypothesis_verdict` ne ferme jamais la mission | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Leases / fencing | absents | `acquire_lease` (epoch monotone), `publish` rejette lease expiré, worker/epoch obsolète et doublon logique (`LeaseRejected`) | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Outbox | absente | `outbox_enqueue` idempotent, `DISPATCHED→UNCERTAIN→CONFIRMED/FAILED_NOT_EXECUTED`, `outbox_dispatchable()` exclut UNCERTAIN | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Déduplication canonique | hash de spec seulement | `register_hypothèse` normalisé (ordre/ponctuation/casse) ; réfutée rouvrable seulement avec justification explicite | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Méta-recherche | absente | `ensure_meta_research` : portefeuille vide + mission OPEN → tâche `meta_recherche` automatique (angles morts, méthodes, représentations, familles, données) | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Sauvegarde/restauration | Git + manifestes | `Kernel.backup()` (API SQLite cohérente) + test de restauration en environnement vierge | IMPLÉMENTÉ NON ENCORE CERTIFIÉ |
| Ancrage externe des preuves | chaîne de hash interne | tête du journal exportée dans l'état committé par Git (historique Git = ancrage externe daté) ; limite documentée : une réécriture complète de l'historique Git resterait possible pour qui contrôle le dépôt — protection proportionnée au modèle mono-fondateur, pas une preuve contre un adversaire propriétaire du dépôt | PARTIEL |

## 7. Phase 7 — Orchestration GitHub

Nouveaux : `ci_tools/ere_cycle_ci.py`, `.github/workflows/ere_cycle.yml`.
Le cycle lit l'état committé, reconstruit les missions (idempotent par
hash), crée les tâches de méta-recherche des portefeuilles vides, exporte
l'état et le commite. Démonstration locale : deux exécutions successives
produisent le même état (missions A et B OPEN, tâches de méta-recherche
créées une seule fois). Exécution réelle du workflow sur GitHub :
voir le run journalisé au registre seq519. Statut : IMPLÉMENTÉ, en cours
de certification par le run CI réel.

```
ARENA (décide) ──push/dispatch──▶ GitHub Actions (ere_cycle, borné 15 min)
      ▲                                │ python ci_tools/ere_cycle_ci.py
      │                                ▼
      └── lit STATE.json ◀── commit état (bot) ── Kernel SQLite (éphémère CI)
                                     │
                     calcul lourd ──▶ Kaggle (kaggle_migrate/verify, secrets CI)
      Mission OPEN ─▶ hypothèses ─▶ réfutation ─▶ (mission reste OPEN)
                  └─▶ portefeuille vide ─▶ tâche META-RECHERCHE automatique
```

## 8. Phase 8 — Pilotage Kaggle

Démontré historiquement et revérifié par `KAGGLE_CHECK.json` :
authentification API réelle, migration par lots avec checkpoints.
La présente mission redéclenche le contrôle de statut Kaggle (aucun
calcul coûteux, aucune publication de dataset) ; le lancement d'un
kernel de calcul ERE sur Kaggle reste à démontrer sur un besoin réel.
Statut : PARTIEL (accès VÉRIFIÉ, calcul ERE via kernel Kaggle NON TESTÉ).

## 9. Phase 9 — Validation indépendante et endurance

- Identité de validation distincte (moteur I) : **NON IMPLÉMENTÉ** — à
  réaliser au premier objet légitime N5+, pas avant (pas d'usine à gaz).
- Campagne d'endurance 72 h sans session : **NON TESTÉ**. Le patron
  GitHub (cron sur branche par défaut + cycles par lots) la rend
  possible, mais un cron ERE devrait vivre sur `main`, que cette mission
  n'a pas le droit de modifier. Décision fondateur requise : autoriser
  un workflow planifié minimal sur `main`, ou un déclencheur externe.
  Statut : BLOQUÉ PAR AUTORISATION.

## 10. Tests exécutés (résultats bruts)

`pytest tests/ -q` → **37 passed** (31 préexistants + 6 nouveaux) :
publication à lease expirée/obsolète rejetée 6/6 tentatives invalides,
aucun doublon logique après interruption/reprise, restauration vierge
sans perte ni double publication, mission OPEN après réfutation de
toutes ses hypothèses, méta-recherche automatique à portefeuille vide,
outbox UNCERTAIN jamais redispatchée, déduplication canonique et
réouverture seulement justifiée. Non exécutés : interruption réelle d'un
run GitHub en plein cycle, récupération d'artefacts d'un kernel Kaggle
ERE, endurance — listés comme tels, non simulés.

## 11. Limites et autorisations encore nécessaires

1. Cron/endurance : workflow planifié sur `main` ou déclencheur externe (décision fondateur).
2. Identité de validation I séparée : au premier candidat N5+ légitime.
3. Calcul Kaggle ERE : premier kernel réel à cadrer par un protocole préenregistré.
4. Aucun secret nouveau requis pour tout ce qui précède sauf décision contraire.

Aucun accès ME-001, aucune écriture dans le corpus source, aucun ordre
réel, `main` inchangée (vérifiée au registre seq519).
