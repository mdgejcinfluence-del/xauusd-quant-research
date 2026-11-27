# MODULE E — AUTONOMOUS EXPERIMENT DESIGN ENGINE (conception)

## Responsabilité

Décider quelle expérience réaliser ensuite — ou conclure qu'aucune
expérience disponible ne peut plus réduire l'incertitude.

## Algorithme de décision (conceptuel)

1. Lister les hypothèses survivantes et leurs prédictions divergentes.
2. Pour chaque expérience candidate : données requises (segment et
   coût), observations qui soutiendraient/réfuteraient chaque
   hypothèse, gain d'information attendu, risque de contamination
   (réutiliser un segment déjà consommé).
3. Choisir l'expérience au meilleur rapport information/coût, la
   **préenregistrer** (protocole gelé, hash, registre chaîné) avant
   tout calcul — pratique déjà en vigueur depuis seq149.
4. Exécuter, qualifier, éliminer ou borner ; répéter ou conclure
   NON DÉMONTRABLE avec l'observation minimale qui débloquerait.

## Méthodes mobilisées

Tests d'identifiabilité (ensembles compatibles plutôt que points),
expériences contrefactuelles avec traitement explicite de la censure,
sensibilité aux définitions (grilles préenregistrées, jamais de seuil
choisi sur le résultat), stabilité temporelle et par régime, plans
adaptatifs à règle d'arrêt pré-déclarée (précédent : seq486 — évaluation
unique à ≥60 jours prospectifs et ≥150 épisodes, examens intermédiaires
interdits).

## Garde-fous intégrés

- Contrôle D du Drift Guard : ne jamais relancer une expérience dont
  la réponse existe déjà au registre.
- Budget de recherche : une expérience doit pouvoir changer une
  classification, une décision de construction ou un verdict ; sinon
  elle n'est pas lancée.
- Le moteur doit savoir s'arrêter : CTRS-007 (verdict B) et EMI-006
  (frontière démontrée) sont des sorties légitimes, pas des échecs.

## Sorties

`ExperimentPlan` (protocole, segment de données autorisé, critères de
succès/échec pré-déclarés) ou `NonIdentifiabilityVerdict` motivé.
