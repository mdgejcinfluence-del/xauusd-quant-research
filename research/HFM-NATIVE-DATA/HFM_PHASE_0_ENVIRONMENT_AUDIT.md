# PHASE 0 — AUDIT DE L'ENVIRONNEMENT (rien modifié hors ce dossier)

Dépôt : branche dédiée, chaîne de preuves valide (426 entrées à l'ouverture, vérifiée avant
travaux). Conventions existantes réutilisées telles quelles : collecte CI via GitHub Actions
(workflow historique `phase10_all.yml`, secrets `KAGGLE_API_TOKEN` en environnement de job —
jamais en dépôt), modules `ci_tools/` à modes dispatchés, manifestes JSON par lot, reprise par
manifeste (patron `edge02_dukascopy.py` : heures figées seulement si vides anciens, jamais de
re-téléchargement d'un lot OK), Parquet partitionné, SHA-256 systématique, compte Kaggle
`shalom5123` (publication privée par défaut, vérifiée par journal avant déclaration de succès).
Bibliothèques disponibles dans le venv : pandas/numpy/pyarrow/duckdb (polars absent — non requis,
le collecteur n'en dépend pas). Environnement local : **Linux, sans terminal MetaTrader 5, sans
identifiants HFM** (`HFM_LOGIN/HFM_PASSWORD/HFM_SERVER` absents — vérifié par l'exécution du
mode `probe`, qui refuse proprement). Corpus Dukascopy certifié (348 partitions) : non touché,
non renommé, hors de ce dossier. Verrous §14 : confirmés actifs (holdout fermé, deadline 120 min
inchangée, aucune stratégie relancée — cette mission est données uniquement).
