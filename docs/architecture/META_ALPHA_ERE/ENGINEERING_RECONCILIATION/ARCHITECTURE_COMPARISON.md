# RÉCONCILIATION — COMPARAISON DES ARCHITECTURES

Légende : **[DÉPÔT]** fait vérifié dans le dépôt · **[EXT]** proposition
du dossier externe · **[NV]** non vérifié.

| Sujet | Dossier externe [EXT] | Réel META ALPHA [DÉPÔT] | Décision recommandée |
|---|---|---|---|
| Forme générale | Monolithe modulaire Python, 9 packages (option A) ; B avancée ; C distribuée | Monolithe de fait : ~206 scripts `ci_tools/`, pas encore de packages moteurs | **A confirmé** ; B par extensions justifiées ; C rejeté (aucun goulot mesuré, coût/complexité sans bénéfice) |
| Plan de calcul | Kaggle batch (preflight→shard→export), Actions en appels courts | **GitHub Actions** : téléchargement Drive par gdown, calcul, commit des résultats avec boucle pull-rebase/push (prouvé sur 348 partitions et dizaines de campagnes) | Conserver Actions comme plan de calcul cible ; Kaggle-kernels = option à qualifier séparément |
| Stockage bulk | Datasets Kaggle versionnés ou objet externe, référencés par SHA-256 | Drive (source des 348 partitions) + migration Kaggle en cours (`reports/meta_alpha/kaggle_migration/STATE.json`, VERIFY.json) ; partitions jamais dans Git | Git = vérité logique + manifestes ; bulk = Drive/Kaggle datasets existants ; aucun nouvel objet à acheter sans décision fondateur |
| Reprise | Checkpoints par shard, publication externe avant « durable » | Reprise par protocole : scripts idempotents relancés, états CI committés (ex. STATE.json de migration), checkpoints documentaires par campagne | Adopter la règle externe « local ≠ durable » ; notre équivalent durable = commit vérifié sur la branche |
| État / machine à états | Machine à états persistante, journal append-only à writer unique | Registre chaîné SHA-256 `TRIAL_LEDGER_CHAIN.json` (append-only par discipline + test), journal des décisions Markdown | Le registre chaîné joue déjà ce rôle pour les *décisions* ; une machine à états des *tâches* reste à concevoir si le besoin apparaît (pas au MVP) |
| Orchestration | ARENA supervise via commandes typées ; Actions submit/reconcile/collect | L'agent (session ARENA) écrit le code, dispatche la CI via `gh`, lit les journaux ; **aucune API ARENA n'existe** [DÉPÔT] | Décrire ARENA comme superviseur en session, pas comme service ; ne rien concevoir qui exige une API inexistante (voir `ARENA_ORCHESTRATION_DESIGN.md`) |
| Environnements | Wheelhouse verrouillé, locks avec hashes, SBOM | venv de session + `pip` du runner CI ; pas de lock formel [DÉPÔT] | Manque réel identifié : lock reproductible à traiter dans une mission d'implémentation, pas ici |
| Déploiement | Aucun trading ; H = spécification, I ≤ paper | Aucun ordre réel, aucun connecteur ; porte H fermée | Convergent — confirmé |

**Conclusion :** le dossier externe et notre réel convergent sur la
forme (monolithe modulaire, preuves d'abord) et divergent sur le plan
de calcul (Kaggle-kernels supposé vs CI prouvée). La réconciliation
retient leur discipline (shards, reprise, publication vérifiée) et
notre substrat (Actions + Drive/Kaggle-stockage).
