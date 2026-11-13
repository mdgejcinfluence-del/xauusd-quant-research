# META ALPHA — XAUUSD DGP

Recherche quantitative autonome sur les cotations natives XAUUSD Bid/Ask.

> **Ce dépôt ne contient ni edge, ni stratégie gagnante, ni promesse de
> performance.** Il contient l'infrastructure qui permet de chercher, de
> falsifier et de rejeter — y compris la possibilité de conclure `NO_EDGE`.

---

## Ce que fait ce système

Il transforme une séquence de ticks Bid/Ask certifiée en une chaîne scientifique
auditable :

```
TICKS BID/ASK → DGP ANALYTIQUE → VARIABLES → HYPOTHÈSES → ANOMALIES
  → CANDIDATS → EDGES QUALIFIÉS → PORTEFEUILLE → HOLDOUT → ADAPTATEUR → ROBOT
```

Rien ne saute d'étape. Le robot n'est jamais atteignable directement depuis un
backtest. Le Holdout s'ouvre une seule fois, sur autorisation explicite du
propriétaire.

## Ce qui est déjà certifié (et jamais reconstruit)

| Phase | Statut | Contenu |
|---|---|---|
| Phase 1 | **CERTIFIED** | Source primaire XAUUSD, 11 136 fichiers Dukascopy BI5 |
| Phase 2 DGP Base | **CERTIFIED** | 685 118 625 ticks, 348 partitions, ordre chronologique vrai |

Ces deux phases vivent sur Google Drive. Le dépôt les **lit** et **vérifie
leurs SHA-256** ; il ne les modifie jamais. Le module
`metaalpha/drive_preflight.py` refuse de démarrer si la baseline a bougé.

## Ce que l'ingénierie doit produire

Neuf phases, de `PHASE_2_ANALYTICAL` à `PHASE_9_MQL5`. La structure complète,
avec les gates d'entrée et de sortie, est décrite dans
[`metaalpha/mission.py`](metaalpha/mission.py) et rendue visuellement dans
[`docs/ARCHITECTURE_COMPLETE_V2.html`](docs/ARCHITECTURE_COMPLETE_V2.html).

Le schéma HTML est **généré** depuis `mission.py` : il ne peut pas mentir sur
l'existence d'une phase.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# garde-fou secrets (obligatoire avant tout commit)
python scripts/install_hooks.py

# tests
python -m pytest tests/ -q
```

Aucune clé n'est nécessaire pour lancer les tests. La CI est verte sur un fork
public, sans secret — c'est volontaire.

## Accès aux données

L'accès au corpus passe par un **compte de service Google**, jamais par un mot
de passe personnel. Voir [`docs/SETUP_ACCES_DONNEES.md`](docs/SETUP_ACCES_DONNEES.md).

```bash
export GDRIVE_SA_JSON="$(cat sa.json)"
export GDRIVE_ROOT_FOLDER_ID="..."
python -m metaalpha.drive_preflight
```

Attendu : `"status": "PASS"` avec 348 partitions et deux certificats CERTIFIED.

## Sécurité

Dépôt **public par décision du propriétaire**. Trois barrières empêchent
l'introduction d'un secret : `.gitignore`, hook pre-commit, CI. Voir
[`SECURITY.md`](SECURITY.md).

## Contraintes de calcul

- **CPU uniquement.** Aucun GPU : les traitements sont des statistiques de
  séries temporelles, du bootstrap et du replay événementiel — pas du calcul
  matriciel dense.
- DuckDB out-of-core, 2 threads, 4 GB de mémoire par job.
- Une partition à la fois. Jamais 685 M de lignes en mémoire.
- Checkpoints durables : une coupure ne coûte que l'unité en cours.

## Coût

Infrastructure : **0 FCFA par mois**. GitHub Actions, Kaggle et Google Drive
suffisent. Budget alloué : 6 000 FCFA ≈ 9,95 USD, conservé comme marge non
dépensée.

## Ce que ce dépôt ne fera jamais

- Inventer une formule pour remplir une famille scientifique.
- Modifier silencieusement un paramètre.
- Supprimer un résultat négatif.
- Ouvrir le Holdout sans autorisation.
- Modifier un certificat hérité.
- Inventer un paramètre serveur Blue Guardian.
- Déployer en réel sur la seule base d'une compilation.
- Appeler `NET` un résultat sans coût complet confirmé.

Ces interdictions sont dans le code, pas seulement dans cette phrase.

## Licence et usage

Recherche personnelle. Aucune garantie, aucun conseil en investissement. Voir
`SECURITY.md` et `docs/` pour les limites méthodologiques.
