# ERE — PHASE 2 : ENVIRONNEMENT REPRODUCTIBLE ET BENCHMARK

## Audit de l'environnement réel

- Session/CI : Python 3.11.2, Linux x86_64. Le venv de travail
  (`/tmp/metaalpha-venv`) contient pandas 3.1.1, NumPy 2.4.6,
  PyArrow 26.0.1, DuckDB 2.0.0, Polars 2.1.0, pytest 9.2.0
  (déjà présents ; **aucune installation effectuée dans cette phase**).
- Lock reproductible : `ere/requirements.lock.txt` (pip freeze complet,
  111 distributions épinglées). C'est un point de départ de session ;
  le lock CI définitif reste à figer sur le runner (limite connue R3).
- Licences : aucune nouvelle dépendance ; les exclusions du dossier de
  réconciliation sont maintenues (vectorbt Commons Clause, Backtrader
  GPL exclus ; pas de mise à jour globale).

## Benchmark sur tâche réelle représentative

Tâche : construire des barres de 5 secondes (moyenne du Mid) depuis
2 000 000 de ticks Parquet (34,5 Mo, 17 280 barres) — l'opération de
base de nos scans d'épisodes. Un seul passage par moteur, même machine :

| Moteur | Temps | Décision |
|---|---|---|
| DuckDB 2.0.0 | **0,21 s** | **retenu** comme moteur de requêtes pour les scans F (sélections, agrégats, contrôles) |
| pandas 3.1.1 | 0,94 s | conservé pour la logique à état (épisodes, trajectoires) déjà éprouvée |
| Polars 2.1.0 | 4,12 s | **non retenu** : aucun avantage mesuré sur cette tâche ; ajouter un troisième moteur serait une redondance |

Limites honnêtes : un seul type de tâche, données synthétiques locales,
pas de mesure mémoire fine. La décision est révisable si une tâche
future (jointures asof massives, par exemple) montre un autre profil.
Pydantic : non adopté (décision D10) — les contrats stdlib passent
leurs tests sans dépendance nouvelle ; réévaluation si des schémas
JSON doivent être publiés à des tiers.

## Dépendance Drive

Inchangée dans cette phase : les partitions restent téléchargées par
la CI (gdown) et référencées par l'inventaire certifié ; la migration
Kaggle-stockage existante continue de la réduire. Aucune écriture sur
les partitions certifiées.
