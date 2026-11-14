# ÉTAT PERMANENT — META ALPHA XAUUSD DGP (consultable à tout moment, mis à jour par les workflows)

## Mission en cours
- **P3-002** : 126 hypothèses préenregistrées (registre `p3/P3_002_REGISTRY.json`), exécution distante GitHub Actions.
- Dernier gate : **P4-001 REJETÉ** (immuable) — `GATE_P4_001.md`.

## Compteurs d'hypothèses (réels)
| Générées | Préenregistrées | Testées | Rejetées | Non concluantes | Qualifiées (feu vert) |
|---:|---:|---:|---:|---:|---:|
| 127 (1 H-P3-A + 126 lot P3-002) | 127 | 1 (P4-001) + lot en cours | 1 | à déterminer au gate P3-002 | **0** |

## Familles explorées / restantes
Explorées: volatilité/spread conditionnels (P3-001, P4-001 rejeté), lot P3-002
(liquidité, volatilité, rythme, activité, momentum passé). Restantes: asymétries
directionnelles, extrêmes/jumps, régimes causaux, interactions — cycles suivants.

## Exécutions récentes (IDs réels dans les rapports de gate)
- P3-001: run 43495787484, succès 4 h 41. P4-001: run final 43594784236, succès 39 min (7 runs avec incidents corrigés, ~5 h 20 au total, 0 Fcfa).

## Incidents (tous journalisés dans les commits)
Rejets de push de checkpoint (corrigé: rebase-avant-push), throttling Drive
(corrigé: 3 voies de téléchargement + pauses), bug de shadowing (corrigé),
YAML d'indentation (corrigé). Reprise exacte prouvée à chaque fois.

## Ressources
GitHub Actions CPU uniquement, quotas gratuits, 0 Fcfa dépensé. Corpus intact, Holdout scellé.

## Prochaine action automatique
Gate P3-002 à la fin du run -> hypothèses survivantes (FDR + filtre économique)
préenregistrées en P4-002; sinon nouveau lot P3-003 orienté par les échecs.

## Blocage connu (décision propriétaire requise)
Chaînage `workflow_run`/`workflow_dispatch` inter-workflows: exige les workflows sur
`main` (voir DIAGNOSTIC_ORCHESTRATION_MAIN.md). Contournement actif: workflows
réutilisables `workflow_call` enchaînés dans un même déclenchement (démonstration
chain-demo) + checkpoints/reprise entre sessions. Fusion vers main: **non effectuée**
— la session de travail est contrainte à sa branche dédiée; la fusion des 4 fichiers
devra être validée/exécutée côté GitHub par le propriétaire ou une session autorisée
sur main. Aucune protection de branche n'a été contournée.
