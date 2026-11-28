# RÉCONCILIATION — CONCEPTION DE L'EXÉCUTION KAGGLE

## Réel [DÉPÔT] — ce que nous faisons déjà avec Kaggle

Kaggle sert de **stockage bulk** : migration des partitions Drive →
datasets Kaggle par la CI (`ci_tools/kaggle_migrate.py`, état
`reports/meta_alpha/kaggle_migration/STATE.json`, vérification
distante par `kaggle_verify.py` : fichiers attendus/dists, tailles).
Authentification par secrets CI (présence vérifiée, `KAGGLE_CHECK.json`).
**Aucun kernel/notebook Kaggle n'a été exécuté dans ce programme** ;
le calcul vit dans GitHub Actions. Toute affirmation sur les quotas,
le matériel ou la reprise des kernels est donc **[NV] chez nous** —
le dossier externe les documente ([V] documentaire, 12 h de session,
4 cœurs/30 Go annoncés, 20 Go de sorties) sans les avoir testés non
plus sur notre compte.

## Décision

Kaggle-kernels n'est **pas** le plan de calcul cible tant qu'une
mission de qualification dédiée (autorisée par le fondateur, sur
données synthétiques) n'a pas vérifié : authentification, soumission
privée, binding de version, récupération des sorties, quotas réels du
compte. En attendant, le cycle ci-dessous est la conception de
référence, calquée sur notre cycle CI éprouvé.

## Cycle complet d'une tâche (conception, 10 étapes)

1. **Préparation** : plan gelé (hash), entrées référencées par
   manifeste (partitions + SHA-256), budget déclaré.
2. **Validation des entrées** : schéma, hashes, segment autorisé,
   allowlist — un URI hors domaine autorisé est refusé avant tout IO.
3. **Soumission** : identifiant de tâche dérivé du hash du plan
   (idempotence) ; une soumission ambiguë (timeout après envoi) se
   résout par réconciliation, jamais par resoumission aveugle.
4. **Identification de la version exécutée** : version exacte du
   code/wheel et des datasets enregistrée dans le manifeste de run.
5. **Suivi du statut** : appels courts et répétés (jamais d'attente
   longue dans un job), journal des tentatives.
6. **Récupération des sorties** : version précise, intégralité
   téléchargée avant toute interprétation.
7. **Vérification des empreintes** : SHA-256 des sorties contre le
   manifeste ; un écart invalide la preuve entière.
8. **Publication durable** : petits artefacts + manifestes committés
   sur la branche ; bulk référencé, pas copié dans Git.
9. **Reprise après interruption** : au dernier shard *publié et
   vérifié* ; **un checkpoint local (Kaggle ou runner) n'est jamais
   durable avant publication externe vérifiée** — règle externe
   adoptée, déjà notre pratique via les commits CI d'état.
10. **Déduplication** : même hash de plan + mêmes entrées = même
    tâche ; les tentatives sont des `attempt_id` d'une seule tâche,
    toutes journalisées, une seule publication fait foi.

## Frontières

Aucun PAT GitHub dans Kaggle ; aucun `git push` depuis un kernel ;
aucun secret de validation dans l'environnement de découverte ;
ME-001 et ses zones prospectives ne sont jamais montés dans une
tâche de ce périmètre.
