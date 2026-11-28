# RÉCONCILIATION — DÉCISION SUR LA STACK TECHNOLOGIQUE

**Aucune bibliothèque n'est installée pendant cette mission.**

## Réel [DÉPÔT]

Python (runner CI + venv de session), pandas/NumPy/PyArrow, matplotlib,
scripts déterministes ; téléchargement des partitions par gdown ;
Kaggle utilisé comme stockage (API + `six`, déjà pratiqué :
`kaggle_migrate.py`). Ni DuckDB/Polars ni Pydantic ne sont des
composants du pipeline actuel ; les calculs par partition en pandas
ont suffi à toutes les campagnes (épisodes sur 348 partitions en CI).

## Évaluation des propositions [EXT] (56 bibliothèques étudiées)

| Proposition externe | Décision réconciliée | Justification |
|---|---|---|
| DuckDB 1.3.2 + Polars 1.35.2 (noyau) | **Candidat à benchmark, pas adoption** | nos scans par partition fonctionnent ; adopter deux moteurs de requêtes concurrents avant un goulot mesuré viole notre règle « valeur démontrée d'abord ». Un seul des deux sera retenu si le benchmark (tâche réelle : épisodes transversaux) le justifie |
| Pydantic 2.12.5 + jsonschema | **Candidat prioritaire** (mission contrats) | comble notre manque réel (schémas exécutables) ; licence permissive, pas de dépendance lourde |
| Numba | Différé | utile pour un replay à état futur ; aucun moteur H n'existe |
| arch / ruptures / statsmodels / scikit-learn | Au cas par cas, par protocole | statsmodels/scikit-learn déjà familiers du projet ; `arch` (SPA/bootstrap) pertinent pour I-A, plus tard |
| PyMC *ou* Stan (jamais les deux) | Différé, choix unique le jour venu | convergent avec l'externe ; aucun modèle bayésien n'est requis par nos questions actuelles |
| Optuna / BoTorch / SBI / PyTorch | **Non retenus au MVP** | l'optimisation de paramètres est précisément ce que notre gouvernance interdit sans modèle identifié ; SBI suppose un simulateur validé que nous n'avons pas |
| vectorbt (Apache + Commons Clause), Backtrader (GPL) | **Exclus** | licences incompatibles avec un usage commercial par défaut — alerte externe confirmée et adoptée |
| Dask/Ray/distribué | Exclus | aucun goulot mesuré ; complexité sans bénéfice |
| Kaggle CLI + six | **Déjà notre réel** (stockage) | l'externe confirme le piège `six` que notre pratique CI connaît |

## Règles d'adoption (proposées)

Une bibliothèque entre si : (1) une tâche réelle et mesurée en a
besoin ; (2) licence du tag verrouillé auditée ; (3) lock avec hashes
et test de non-régression sur un résultat certifié ; (4) une seule à
la fois. Les versions « dernières recensées » du dossier externe sont
des métadonnées, pas des recommandations — nous ne faisons jamais de
mise à jour globale silencieuse (règle externe adoptée).
