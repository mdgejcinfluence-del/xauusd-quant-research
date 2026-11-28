# RÉCONCILIATION — CONCEPTION TECHNIQUE DES NEUF MOTEURS

État réel commun : **aucun moteur n'existe comme logiciel** ; chacun est
une responsabilité exercée par des scripts et des documents. La table
donne la conception cible réconciliée (dossier externe [EXT] + ERE
seq492–497 + réel du dépôt [DÉPÔT]).

| Moteur | Responsabilité (frontière) | Entrées | Sorties | Dépendances | État réel |
|---|---|---|---|---|---|
| A Ingestion | structurer le dossier trader, absences explicites | transactions, bio, stats publiques | `TraderDossier` (N0/N1) | — | pratique manuelle (dossiers Colorful) |
| B Comportement | décrire faits vs interprétations | `TraderDossier` + `MarketWindow` | `BehaviorProfile` (N1/N2) | A, corpus (fenêtres) | pratique (campagnes seq433+) |
| C Hypothèses | ≥2 mécanismes concurrents + inconnu | `BehaviorProfile`, D, registre | `HypothesisSet` (N3) | B, D | pratique (ME-001..004) |
| D Connaissances | méthodes sourcées avec limites | littérature, docs institutionnelles | `KnowledgeRef`/`KnowledgeBundle` | — | catalogue Markdown partiel |
| E Expériences | testabilité, plan discriminant le moins coûteux, gel | `HypothesisSet`, **F.catalog**, D | `ExperimentPlan` + `AvisDeTestabilite` | C, D, F.catalog | pratique (préenregistrements seq149+) |
| F Marché | voir découpage ci-dessous | plan gelé, corpus autorisé | `SignatureReport` (N4) + coût d'ordre de grandeur | E, corpus | scripts CI par campagne |
| G Identification | verdict économique, contre-seing du non-testable | liste fermée (ERE-REVIEW-002 §4.2) | `ModelDossier` (N5/N6 ou qualifications) | C, D, F.execute | registre des modèles tenu |
| H Stratégies | nos règles propres, derrière porte | `ModelDossier` ≥ N5 + approbation fondateur | `EngineSpec` gelée | G | **fermé** (aucun modèle éligible) |
| I-A Validation | edge net d'un moteur, seul | `EngineSpec`, segment indépendant | `ValidationVerdict` (N7 possible) | H | jamais exercé sur un moteur ERE |
| I-B Portefeuille | indépendance économique des sources validées | verdicts I-A favorables | allocation par budget de risque | I-A | portefeuille vide |

## Frontières tranchées

- **E ↔ G** (conforme aux deux sources) : E juge la *testabilité* et
  gèle le protocole ; G juge le *mécanisme*. Le « non démontrable » de
  E est un avis qui exige le contre-seing de G pour clore un dossier.
- **F en quatre sous-responsabilités** (proposition [EXT] adoptée comme
  découpage interne, pas comme moteurs nouveaux) : **F.catalog**
  (inventaire, capacités, segments — *avant* E, lève la circularité
  E↔F), **F.index** (index d'événements et barres dérivées causales,
  avec provenance), **F.signatures** (définitions de signatures par
  famille), **F.execute** (exécution du plan gelé, shards, mesures).
  F.execute ne choisit ni seuils ni segment.
- **H ↔ I** : H conçoit et gèle ; I-A évalue sans pouvoir modifier ;
  tout retour H après verdict passe par un nouveau protocole (E).
- **I-A / I-B** : séparation d'ERE-REVIEW-002 maintenue (le juge d'un
  moteur n'alloue pas son poids).
- Aucune fusion de responsabilités n'est décidée ; le découpage de F
  est interne et ne crée pas de dixième moteur.

## Dépendances et boucles

Boucles autorisées : F.execute → E (ambiguïté), G → C (hypothèse
nouvelle), I-A → E (diagnostic). Interdites : I → H sur le même
segment, prospectif protégé → C/E avant règle d'arrêt, modification
d'un protocole gelé (toute reprise crée une nouvelle version).
