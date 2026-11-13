# META ALPHA — Présentation technique du système RÉELLEMENT construit
### Document destiné à un agent tiers (ChatGPT) — état vérifié le 13 novembre 2026, aucun secret inclus

## 0. Comment lire ce document
Tout ce qui suit a été **vérifié aujourd'hui** (appels API réels, exécutions, lectures).
Les points défaillants sont listés comme tels (§10). Rien n'est théorique.

## 1. Vue d'ensemble
META ALPHA est une recherche quantitative sur les cotations natives XAUUSD Bid/Ask
tick par tick (Dukascopy BI5), 2010-2026, 685 118 625 ticks certifiés. Le système est
conçu pour découvrir d'éventuels avantages statistiques, les valider hors échantillon,
puis — seulement s'ils existent — construire un portefeuille et tester sa compatibilité
Blue Guardian. `NO_EDGE` est un résultat valide. CPU uniquement, budget infrastructure 0.

```
Propriétaire (décisions, gates, autorisations)
        │  autorisations / secrets (GitHub Secrets)
        ▼
ARENA (agent scientifique autonome, cette session)
   lit/écrit le code, diagnostique, rédige les rapports, déclenche les exécutions
        │  git push sur la branche de session
        ▼
GITHUB (dépôt + Actions = orchestrateur et bras d'exécution)
   workflows déclenchés par fichiers "trigger", résultats recommittés sur la branche
        ├──► GOOGLE DRIVE (liens publics, lecture seule) : corpus certifié 348 partitions
        └──► KAGGLE (calcul jetable) : API authentifiée par token, kernels éphémères
```

## 2. Rôle exact d'Arena
Arena est l'agent qui pilote : il détient la session, le contexte scientifique (passation),
le droit d'écrire sur **une seule branche** du dépôt (`arena/afe12737-xauusd-quant-research`),
et déclenche GitHub Actions en poussant des fichiers déclencheurs (`import_trigger/*.txt`).
Limites structurelles d'Arena : sa sandbox n'a **pas d'accès réseau sortant vers
drive.google.com** (proxy limité à github/pypi) et ne peut pas lire les journaux bruts
des workflows (le endpoint de logs renvoie EOF via son proxy) — d'où l'architecture
« Actions télécharge et recommitte les preuves », et la capture d'erreurs **dans le dépôt**
(`reports/meta_alpha/phase2/ERROR.txt`) plutôt que dans les logs.

## 3. Les composants réels (noms et chemins)
Dépôt : `mdgejcinfluence-del/xauusd-quant-research` (privé), branche de travail
`arena/afe12737-xauusd-quant-research`. Le code scientifique importé vit sous
`META_ALPHA_CODE_V1/META_ALPHA/` (paquet Python `metaalpha`, 24 modules, ~8 500 lignes,
**168 tests verts vérifiés aujourd'hui**) : `mission.py` (contrat des 9 phases et gates),
`governance.py` (statuts terminaux, sceau Holdout à ouverture unique), `families.py`
(8 familles, 11 variables, 9 décisions), `decisions.py` (réponses HUMAN uniquement),
`extract.py` (traductions SQL certifiées), `extraction_ladder.py` (échelle L0-L7),
`inventory.py` (découverte de schéma par footers), `drive_preflight.py` (préflight
certificats), `dispatch.py` + `orchestrator.py` + `segment.py` (calcul distribué),
`secrets_guard.py`, `connect_app.py` (bouton OAuth « Se connecter à Drive », non utilisé
car les liens publics ont suffi), `remote.py` (accès Drive par compte de service, non branché, voir §10).
Registres et réponses du propriétaire : `META_ALPHA_WORK/RESEARCH_V1_XAUUSD_TICK_ONLY/`
(`00_GOVERNANCE/OWNER_DECISIONS_V1.json`, `10_REGISTRIES/*_REGISTRY_V1.json`).
Rapports et preuves : `reports/meta_alpha/` (baseline, inventaire, audits, mesures Phase 2).

## 4. Intégration GitHub (vérifiée)
Workflows actifs à la racine (`.github/workflows/`) : `import-meta-alpha-code.yml`
(import d'un ZIP depuis un lien Drive public), `inventory348.yml` (inventaire des
348 footers par requêtes HTTP Range), `schema-probe.yml` et `probe184.yml` (sondes
de schéma), `kaggle-check.yml` (présence + authentification Kaggle, sans valeur affichée),
`phase2-autonomous.yml` (traitement L2-L4 par lots avec état de reprise).
Mécanisme : un push modifiant `import_trigger/<nom>.txt` déclenche le workflow,
qui calcule sur runner Ubuntu (Python 3.11, DuckDB, gdown), puis **recommitte**
résultats et état sur la même branche avec le `GITHUB_TOKEN`. Point d'attention :
les workflows du paquet importé (`META_ALPHA_CODE_V1/META_ALPHA/.github/workflows/` :
ci, dispatch_segments, phase_run, preflight_drive, watchdog) sont **inactifs** ici car
imbriqués — ils deviendront actifs dans le dépôt propre du projet. De même, un
déclenchement planifié (cron) ne s'exécute que depuis la branche par défaut.

## 5. Intégration Kaggle (vérifiée aujourd'hui)
Secrets présents dans le dépôt (valeurs jamais affichées) : nom d'utilisateur + clé
au **format token moderne KGAT**, authentification réussie en mode Bearer
(`KAGGLE_API_TOKEN`) par un appel API réel (`kaggle kernels list --mine`), preuve :
`reports/meta_alpha/KAGGLE_CHECK.json`. Le moteur `metaalpha/dispatch.py` découpe le
travail en unités (partitions), pousse un kernel jetable (`kaggle kernels push`),
surveille son statut et récupère les sorties ; un segment perdu est **replanifié,
jamais dupliqué ni rejoué** (démontré par `scripts/demo_dispatch.py`). Le workflow
de dispatch (dans le paquet) attend encore le compte de service Drive (voir §10) :
aucun kernel scientifique n'a encore été poussé. Ressources Kaggle : CPU, sessions
jetables, aucun GPU (`enable_gpu: false` imposé).

## 6. Accès Google Drive (vérifié aujourd'hui)
Le corpus `META_ALPHA_XAUUSD_DGP` est atteint par **liens de partage publics en
lecture seule** (le connecteur Drive d'Arena était branché sur un autre compte ;
les liens ont résolu le problème sans aucun mot de passe). Racine Drive :
dossier `1dy4-…` contenant `04_CHECKPOINTS`, `01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS`
(348 fichiers `part_000001..000348`), registres et rapports historiques. Le dossier du
code (`META_ALPHA_CODE_V1.zip`) a été récupéré de la même façon. Les certificats
Phase 1 et Phase 2 ont été relus octet par octet : CERTIFIED, 11 136 fichiers sources,
**685 118 625 ticks**, et leurs empreintes canoniques sont figées dans
`reports/meta_alpha/BASELINE_HASH_MANIFEST.json`. L'écriture dans Drive (checkpoints
du futur calcul distribué) nécessitera un compte de service — non encore créé (§10).

## 7. Chemin réel des données
Drive (Parquet, lecture) → téléchargement par lot dans GitHub Actions (`gdown`,
ou requêtes Range pour les seuls footers) → calcul DuckDB borné en mémoire (jamais
le corpus entier en RAM ; `metaalpha/duck.py` refuse une connexion sans limite) →
agrégats et empreintes recommittés dans Git (`reports/meta_alpha/**`) → registres et
rapports relus par Arena. Les Parquet ne sont **jamais** committés. Exemple réel du
13 nov. : partition 001 traitée de bout en bout — 40 112 lignes, 0 régression
temporelle, 0 doublon, 0 quote invalide, écart max de reconstruction mid/spread = 0,0.

## 8. Distribution, certification, reprise
Découpe en unités = partitions (ou segments d'hypothèses plus tard), checkpoints
persistants (`reports/meta_alpha/phase2/STATE.json`, registres append-only, Trial
Ledger à venir en P3), reprise = seules les unités absentes de l'état sont traitées.
Certification : tests automatisés (168), empreintes SHA-256 des artefacts, registre
des formules versionné (v1, v2), garde anti-secrets (`.gitignore` + hook + scan) et
sceau Holdout à **ouverture unique** (`governance.py`) — le Holdout n'a jamais été ouvert.

## 9. Ressources et limites
GitHub Actions : jobs ≤ 6 h (les nôtres : 40 s à 20 min), disque runner limité (lots
dimensionnés en conséquence) ; Kaggle : sessions CPU jetables ; Drive : stockage
durable en lecture ; budget 6 000 FCFA une fois, 0 FCFA/mois d'infrastructure.
Splits scientifiques : 60/20/20 **calendaires**, purge ≥ 1 h (plus long label),
jamais de split aléatoire ; coûts inconnus classés GROSS/CONDITIONAL, jamais NET.

## 10. Connexions et points défaillants (réels, à date)
1. **Compte de service Drive absent** (`GDRIVE_SA_JSON`, `GDRIVE_ROOT_FOLDER_ID` non
   déposés) : la lecture est couverte par les liens publics ; l'écriture des
   checkpoints Drive et le préflight « officiel » par compte de service sont en attente.
2. **Lot Phase 2 (L2-L4)** : premier lancement en échec — cause exacte diagnostiquée
   (dépendance `pytz` absente du workflow), corrigée, et **1 partition traitée en
   preuve**. Les 347 restantes n'ont **pas** été lancées (arrêt ordonné par le propriétaire).
3. **Variables bloquées (6/11)** : ZSCORE_ROBUST et SPREAD_REGIME/REGIME_CLASS
   (traductions étagées à implémenter), SUBPERIODE (horaires de session non documentés),
   MFE_H/MAE_H (convention de direction Bid/Ask à définir). 5 variables certifiées
   (22 entrées SQL) : RET_H (label), ROLL_STD_MID, ROLL_RANGE_MID, UPDATE_INTENSITY,
   INTERARRIVAL_MEAN (+ base MID/SPREAD/RET_TICK).
4. **Journaux GitHub illisibles depuis la sandbox Arena** (EOF du proxy) : contourné
   par la capture d'erreurs committée dans le dépôt.
5. Dépôt projet **public** `meta-alpha-xauusd` toujours pas créé (décision du
   propriétaire à exécuter au moment de la bascule, après scan anti-secrets — déjà propre).

## 11. Mission en attente et procédure de lancement
Prêt : infrastructure, données certifiées et inventoriées (348/348, schéma réel connu :
16 colonnes, deux signatures 001-294/295-348), 9 décisions du propriétaire enregistrées,
22 traductions certifiées, Kaggle authentifié, moteur de lots Phase 2 fonctionnel.
En attente : montée L0→L4 complète (lots de partitions), gate Phase 2, puis phases
P3 (mining préenregistré au Trial Ledger) → P4 validation → P5 stress → P6 qualification
→ P7 portefeuille ; P8 Holdout **uniquement sur autorisation explicite distincte** ;
P9 robot **uniquement sur autorisation distincte**. Lancement type d'une mission :
(1) écrire le lot dans `import_trigger/phase2_batch.txt` et pousser ; (2) le workflow
traite, committe mesures + état ; (3) Arena lit les rapports, évalue le gate objectif
(comptes exacts, écarts expliqués, intégrité) ; (4) rapport de gate automatique.
Déclencheurs : autorisation du propriétaire pour chaque nouvelle phase scientifique
(selon la directive d'autonomie : progression automatique *à l'intérieur* du périmètre
autorisé, arrêt aux gates sensibles — Holdout, réel, dépense).

## 12. Règles à ne jamais enfreindre (pour l'agent lecteur)
Ne jamais : inventer une formule/paramètre/valeur serveur ; ouvrir le Holdout sans
autorisation explicite ; appeler un tick une transaction ; présenter du GROSS comme
du NET ; optimiser sur le Holdout ; supprimer un résultat négatif ; modifier les
certificats hérités ; demander au propriétaire une réponse déjà dans les documents.
En cas d'écart avec la baseline figée : s'arrêter, rapporter l'écart exact, ne pas « corriger ».
