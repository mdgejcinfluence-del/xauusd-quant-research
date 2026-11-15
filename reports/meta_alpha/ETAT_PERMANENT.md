# ÉTAT PERMANENT — META ALPHA XAUUSD DGP (consultable à tout moment, mis à jour par les workflows)

## Mission en cours
- **P3-002 TERMINÉ** : run 43600799780 succès en 4 h 51, 282/282. **Gate v2: 0 survivant sur 21 contrastes** (11 aucun signal, 10 amplitude absorbée par le spread; meilleur écart 0,51 bp << filtre 2,17 bp). Verdict enregistré dans TRIAL_LEDGER_CHAIN.json (tête fba97ccf). **Aucun P4-002: rien n'a survécu.** Extraction phénoménologique terminée (282/282) et AUDIT terminé (run 43688191819): ANOM-001 autocorrélation mid lag-1 = OBSERVATION À VÉRIFIER (mécanisme de construction du mid), ANOM-002 regroupement de volatilité = DESCRIPTIF DOCUMENTÉ. Voir RAPPORT_AUDIT_PHENOMENES.md. Validation profonde terminée: mécanisme ANOM-001 RÉFUTÉ par preuve directe (98,5% d'événements bilatéraux; pistes lead-lag bid/ask ouverte), ANOM-002 confirmé descriptif, gaps sans effet directionnel. Voir RAPPORT_CONSOLIDE_VALIDATION_PROFONDE.md. **PHASE 1R tâche 1 TERMINÉE** (run 43752027483): séries granulées construites (846 lignes, 3 granularités); autocorrélation tick (0,487) éteinte dès 100 événements; aucune anomalie candidate déclarée. Voir META_ALPHA_PHASE_1R_DESCRIPTIVE_SERIES_REPORT.md. Arrêt: décision propriétaire requise pour toute extension.
- **Chaînage automatique : PROUVÉ** — run 43600799707: workflow A (13:38:51Z) puis workflow B consommant son checkpoint (13:39:03Z), sans humain (`chain/CHAIN_PROOF.txt`). Le calcul P3-002 continue sur GitHub même PC éteint.
- Dernier gate : **P4-001 REJETÉ** (immuable) — `GATE_P4_001.md`.

## Compteurs d'hypothèses (réels)
| Générées | Préenregistrées | Testées | Rejetées | Non concluantes | Qualifiées (feu vert) |
|---:|---:|---:|---:|---:|---:|
| 127 (1 H-P3-A + 126 lot P3-002) | 127 | 148 (1 P4-001 + 21 contrastes P3-002 + cellules descriptives) | 22 | 0 survivant P3-002 | **0** |

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
Extraction phénoménologique IS (en cours) -> items K mesurés -> seulement alors, vagues d'hypothèses justifiées (condition de passage de la gouvernance).

## Blocage connu (décision propriétaire requise)
Chaînage `workflow_run`/`workflow_dispatch` inter-workflows: exige les workflows sur
`main` (voir DIAGNOSTIC_ORCHESTRATION_MAIN.md). Contournement actif: workflows
réutilisables `workflow_call` enchaînés dans un même déclenchement (démonstration
chain-demo) + checkpoints/reprise entre sessions. Fusion vers main: **non effectuée**
— la session de travail est contrainte à sa branche dédiée; la fusion des 4 fichiers
devra être validée/exécutée côté GitHub par le propriétaire ou une session autorisée
sur main. Aucune protection de branche n'a été contournée.
