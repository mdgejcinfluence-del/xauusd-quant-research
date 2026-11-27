# META ALPHA ERE — ARCHITECTURE FONCTIONNELLE

Neuf moteurs (A–I), un socle transversal, un seul sens de circulation
des conclusions : un module ne transmet jamais à l'aval une hypothèse
comme si c'était un fait (chaque objet porte son niveau de preuve, voir
`DATA_CONTRACTS.md`).

| Module | Responsabilité | Entrées | Sorties | Ne doit jamais |
|---|---|---|---|---|
| A. Trader Intelligence Ingestion | structurer le dossier trader, marquer présent/absent/incertain/contradictoire | transactions, bio, stats publiques, plateforme | `TraderDossier` normalisé | inventer une transaction |
| B. Behavioral Reverse Engineering | reconstruire les comportements observables (entrées, renforcements, sorties, durées, volumes) | `TraderDossier` + ticks autour des transactions | `BehaviorProfile` (faits vs interprétations) | confondre comportement et mécanisme |
| C. Economic Hypothesis Engine | générer et gérer les hypothèses économiques concurrentes, y compris nouvelles | `BehaviorProfile`, registre des modèles, bibliothèque scientifique | `HypothesisSet` avec observations pour/contre et expériences discriminantes | attribuer des probabilités arbitraires |
| D. Scientific Knowledge Engine | bibliothèque scientifique sourcée (disciplines, méthodes, limites) | publications, ouvrages, docs institutionnelles | `KnowledgeBase` référencée | intégrer une méthode par popularité |
| E. Experiment Design Engine | choisir l'expérience la plus informative entre hypothèses | `HypothesisSet`, inventaire des données | `ExperimentPlan` préenregistré (ou verdict NON DÉMONTRABLE) | multiplier les expériences sans gain d'information |
| F. Market Intelligence & Data Discovery | rechercher les signatures dans le corpus, par segment (découverte/construction/validation/prospectif) | `ExperimentPlan`, corpus certifié | `SignatureReport` chiffré | mélanger les segments de données |
| G. Economic Model Identification | assembler preuves et contradictions en dossier de modèle | A–F | `ModelDossier` avec verdict qualifié | sélectionner un modèle par ressemblance |
| H. Independent Strategy Engineering | concevoir nos propres règles d'exploitation d'un mécanisme établi | `ModelDossier` (niveau suffisant uniquement) | `EngineSpec` propre (entrées, sorties, sizing, budget) | copier les ordres du trader |
| I. Economic Validation & Portfolio | valider l'edge net après coûts et agréger les sources indépendantes | `EngineSpec`, données indépendantes | `ValidationVerdict`, allocation de portefeuille | déclarer indépendantes deux sources du même phénomène |

## Socle transversal

Registres (hypothèses, expériences, modèles, protocoles gelés),
provenance et hash des données, journalisation chaînée, orchestration,
garde-fou anti-dérive, gestion des erreurs. Voir `SYSTEM_INTERFACES.md`
et `SECURITY_AND_GOVERNANCE.md`.

## Réutilisabilité

Le dossier Colorful (ME-001) est le premier passage complet dans cette
architecture ; les modules A–G y sont déjà exercés manuellement
(campagnes seq433–491). L'architecture formalise ce qui a été pratiqué
avant de l'automatiser — ordre inverse interdit.
