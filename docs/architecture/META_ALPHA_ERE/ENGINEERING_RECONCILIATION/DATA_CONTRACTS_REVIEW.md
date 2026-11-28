# RÉCONCILIATION — REVUE DES CONTRATS DE DONNÉES

**Aucun contrat existant n'est modifié par cette revue.**

## État réel [DÉPÔT]

Nos contrats sont des **spécifications en prose** (`DATA_CONTRACTS.md` :
objets, invariants, champs `ABSENT` explicites) — aucun schéma
exécutable, aucune validation automatique aujourd'hui. Le dossier
externe [EXT] fournit huit contrats typés de référence (Pydantic,
`extra='forbid'`, Decimal, enveloppe commune avec `evidence_level`,
`artifacts` hashés, `parents`), plus des objets auxiliaires à
formaliser (CorpusManifest, SplitManifest, RunManifest, Approval…).

## Revue des huit contrats externes, un par un

| Contrat [EXT] | Notre équivalent | Compatible | Contradictoire / à amender | Absent chez nous |
|---|---|---|---|---|
| TraderDossier | `TraderDossier` (A) | structure, claims non vérifiés, manques explicites | — | `selection_process`, consentement — à reprendre |
| BehaviorProfile | `BehaviorProfile` (B) | faits/ledger d'observations | chez nous B plafonne à N2 ; l'externe n'impose pas de plafond par producteur | lien obligatoire aux `MarketWindow` (notre ajout ERE-REVIEW-002) |
| HypothesisSet | `HypothesisSet` (C) | ≥2 hypothèses, classes d'équivalence, inconnu inclus | **posterior seulement si likelihood + modèle de sélection** : règle externe saine, à adopter telle quelle (interdit nos probabilités arbitraires) | sommes de probabilités à contrôler dans le service, pas le schéma seul [EXT le reconnaît] |
| ExperimentPlan | `ExperimentPlan` (E) | gel par hash, split, arrêt, budget, seed | l'externe exige une approbation pour la validation scellée : convergent avec notre préenregistrement | notre `AvisDeTestabilite` (E) et sa contre-signature (G) à ajouter |
| SignatureReport | `SignatureReport` (F) | NOT_EXECUTED sans chiffres — règle que nos fichiers vides ME-001.4 appliquent déjà en pratique | — | notre bloc coût d'ordre de grandeur (Correction 7) à ajouter |
| ModelDossier | `ModelDossier` (G) | compatibles/rejetés/non identifiés, abstention possible | l'externe distingue attribution au trader et support du marché — convergent, à garder | liste fermée des entrées recevables (ERE-REVIEW-002 §4.2) à porter dans le schéma |
| EngineSpec | `EngineSpec` (H) | RESEARCH_ONLY/PAPER_ONLY, aucun connecteur | gate externe vérifiant l'approbation — convergent avec notre porte | approbation du fondateur comme objet `GovernanceApproval` (hash, périmètre, expiration) |
| ValidationVerdict | `ValidationVerdict` (I-A) | positif exige preuves numériques mesurées | **E5 externe plus faible que notre N7** : exiger indépendance du segment + critères pré-déclarés | mesures de queue et de dépendance inter-moteurs (I-B) |

## Règles communes : convergences et écarts

- Enveloppe commune (schema_version, ids, commit, producteur, niveau,
  artefacts, parents, warnings) : **compatible** avec nos invariants ;
  notre registre chaîné fournit déjà commit + hash + parenté au niveau
  des *missions*, pas encore des *objets*.
- Hash = égalité de contenu, pas vérité ni autorisation [EXT] :
  convergent avec notre pratique (signatures et ACL séparées).
- Prix en Decimal au contrat, entiers de ticks au replay [EXT] :
  compatible avec notre corpus (prix Bid/Ask, digits documentés) ;
  à formaliser par fournisseur (Dukascopy ≠ HFM).
- Contrôles inter-objets (références existantes, splits disjoints,
  approbateur autorisé, hash ↔ artefact) : **absents chez nous** —
  c'est le principal manque que la future formalisation devra combler,
  avec des tests négatifs (un verdict positif sans calcul doit être
  refusé par construction).

## Décision recommandée

Base future = les huit contrats externes amendés par nos trois ajouts
(`MarketWindow`, `AvisDeTestabilite`/contre-seing, liste fermée G,
bloc coût F, niveau N0–N7 au lieu de E0–E5). Formalisation (schémas +
validations croisées) = mission d'implémentation ultérieure, après
validation du fondateur. Rien n'est modifié ici.
