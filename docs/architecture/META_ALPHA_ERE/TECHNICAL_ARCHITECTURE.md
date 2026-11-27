# META ALPHA ERE — ARCHITECTURE TECHNIQUE CIBLE

## État actuel (existant, éprouvé)

Monolithe de scripts Python versionnés (`ci_tools/`, ~150 modules),
registre chaîné JSON, checkpoints documentaires par campagne, CI
GitHub Actions pour les calculs lourds et les téléchargements Drive/
Dukascopy (exécution locale sans egress réseau), venv unique
(pandas/NumPy/PyArrow/matplotlib). Ce socle a produit 491 entrées de
registre et tous les résultats actuels : **on ne le remplace pas, on
le structure.**

## Cible (incrémentale, par besoin démontré)

1. **Couche dossiers** : schémas `TraderDossier`/`ModelDossier` en
   JSON validés (pydantic ou jsonschema) — premier incrément utile.
2. **Couche corpus** : accès partitionné Parquet + cache local des
   barres dérivées (5 s) par partition avec hash de la partition
   source ; DuckDB/Polars évalués sur la tâche « épisodes
   transversaux » avant adoption.
3. **Couche expériences** : files de protocoles gelés (YAML/JSON +
   hash), exécuteur CI idempotent, registre d'expériences interrogeable.
4. **Couche connaissance** : catalogue Markdown structuré (actuel) →
   index recherchable seulement si le volume le justifie.
5. **Orchestration** : l'agent (modèle de langage) reste l'orchestrateur
   supervisé ; aucun verdict n'est produit par génération de texte.

## Contraintes techniques connues

Calcul tick en Python pur : minutes par partition de ~10 M de ticks
(CI) — acceptable ; les replays complets 2010-2026 exigeraient une
vectorisation ou un moteur colonnaire (décision différée, voir
OPEN_QUESTIONS). Stockage : partitions externes (Drive), jamais dans
Git. Reproductibilité : déterminisme des scripts, seeds inutiles
(aucun aléa dans les protocoles actuels), manifestes par run.

## Ce qui n'est pas construit (assumé)

Pas de plateforme temps réel, pas de connectivité de passage d'ordres,
pas de base de données serveur : inutiles tant qu'aucun modèle n'est
VALIDATED et que le module H reste fermé.
