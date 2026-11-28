# RÉCONCILIATION — DÉCISION EXÉCUTIVE

**Verdict : `READY_FOR_FOUNDER_REVIEW`.** Aucune implémentation commencée.

## État réel vérifié (dépôt, ce jour)

- Branche `arena/afe12737-xauusd-quant-research`, HEAD `07f6999` à
  l'ouverture (ERE-REVIEW-002), arbre propre, `main` à `98bfd359`
  inchangée. Registre chaîné : 498 entrées après préenregistrement.
- **DRIFT GUARD : VERT.** La mission sert l'identification de modèles
  économiques (contrôle A), ne reconstruit aucun paramètre interne (B),
  réduit l'incertitude « quelle ingénierie construire ? » (C), et ne
  rejoue aucun test déjà fait (D).
- Architecture ERE : 16 documents + 5 diagrammes + 2 revues
  (seq492–497) — **conception documentée, aucun des neuf moteurs
  n'existe comme composant logiciel** ; ils sont exercés comme
  *pratique* par ~206 scripts `ci_tools/` et la CI.
- Le dossier externe (315 Ko, lu intégralement) est une étude
  indépendante honnête : il déclare n'avoir eu accès ni au dépôt, ni
  au corpus, ni à ME-001 ; ses 14 tests sont synthétiques. Ses
  propositions sont donc confrontées ci-dessous à notre réel, jamais
  adoptées sur sa seule autorité.

## Décisions recommandées (détail dans les documents liés)

1. **Architecture cible : monolithe scientifique modulaire** (option A
   du dossier externe), alignée avec l'existant — pas de microservices,
   pas de distribué (option C rejetée : aucun goulot mesuré).
2. **Calcul : GitHub Actions reste le moteur de calcul prouvé**
   (348 partitions téléchargées par gdown, replays de dizaines de
   millions de ticks, commits de résultats). Le plan « Kaggle kernels
   comme plan de calcul » du dossier externe est **non vérifié chez
   nous** : notre usage Kaggle réel est le *stockage* (migration des
   partitions en datasets, `kaggle_migrate.py`, état vérifié), pas
   l'exécution de notebooks. Kaggle-kernels devient une option à
   qualifier, pas la cible.
3. **Taxonomie officielle : N0–N7** (ERE-REVIEW-002, en attente de
   validation fondateur) ; E0–E5 du dossier externe est conservé comme
   table de correspondance, pas fusionné (voir
   `EVIDENCE_TAXONOMY_DECISION.md`).
4. **Contrats : adopter les huit contrats du dossier externe comme
   base de la future formalisation**, amendés par nos objets existants
   (`MarketWindow`, `DossierState`, `AvisDeTestabilite`) — aucune
   modification de contrat dans cette mission.
5. **Aucune bibliothèque installée.** Le noyau actuel
   (Python/pandas/NumPy/PyArrow en CI) suffit ; DuckDB/Polars et
   Pydantic sont des candidats à benchmark, pas des adoptions.
6. **Frontières scientifiques inchangées** : trois objets épistémiques
   séparés, porte H fermée (aucun modèle ne la franchit), zones
   prospectives ME-001 non accédées pendant cette mission.

## Incompatibilités principales découvertes

- Le dossier externe suppose un adaptateur ARENA et des dispatchs
  Kaggle qui **n'existent pas** dans notre environnement (aucune API
  ARENA ; l'agent agit en session, la CI exécute).
- Il propose Python 3.12 et un wheelhouse Kaggle ; notre réel est la
  CI GitHub (Python système du runner, venv pandas) et Drive→CI.
- Son E5 « VALIDATED » est plus faible que notre exigence N7
  (données indépendantes + critères pré-déclarés) ; fusionner les
  échelles diluerait notre protection principale.

Les décisions qui exigent l'approbation du fondateur sont listées
dans `RISKS_AND_OPEN_DECISIONS.md`.
