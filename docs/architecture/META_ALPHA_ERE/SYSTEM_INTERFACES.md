# META ALPHA ERE — INTERFACES SYSTÈME

## Flux principal (par dossier trader)

`TraderDossier` →(A→B) `BehaviorProfile` →(B→C) `HypothesisSet`
→(C→E) `ExperimentPlan` →(E→F) `SignatureReport` →(F→G)
`ModelDossier` →(G→H, si porte franchie) `EngineSpec` →(H→I)
`ValidationVerdict`. Le module D alimente C, E, F, G en références.
Le socle (registres, garde-fou, journal) écrit à chaque transition.

## Boucles autorisées

- G → C : un verdict peut rouvrir une hypothèse nouvelle (jamais
  modifier une hypothèse gelée en cours d'expérience).
- I → E : un échec de validation peut motiver une expérience de
  diagnostic (précédent : BACKTEST-2026-001 → LMD-008), pas un réajustage.
- F → E : une signature ambiguë peut motiver l'expérience
  discriminante suivante.

## Boucles interdites

- I → H avec modification de paramètres sur le même segment (optimisation déguisée).
- F (segment prospectif) → C/E pour ME-001 tant que la règle d'arrêt seq486 n'est pas atteinte.
- Tout module → `main` (branche de travail uniquement).

## Automatisation et supervision

Automatisé : collecte et hash des données, exécution des protocoles
gelés, calculs, tests, manifestes, commits CI. Supervisé par l'agent :
formulation d'hypothèses, choix d'expériences, verdicts. Validation du
fondateur requise : changement de doctrine, activation du module H
pour un modèle, tout passage en conditions réelles (hors périmètre
actuel), toute dépense.

## Gestion des erreurs

Un run échoué produit un journal et un statut, jamais de résultats
partiels promus en conclusions ; les partitions indisponibles sont
classées (UNAVAILABLE/GAP) et le protocole continue sur le segment
restant en le déclarant (précédents : octobre 2026, heures 503).
