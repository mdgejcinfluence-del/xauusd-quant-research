# META ALPHA — PHASE 1R : PROTOCOLE RÉVISÉ (proposition, NON autorisée, NON commencée)

Fondement: décision propriétaire après le contrôle négatif HMM (commit bacc922,
conservé sans modification). Philosophie restaurée:
**DONNÉES NATIVES -> COMPORTEMENTS OBSERVÉS -> ANOMALIES -> CARACTÉRISATION ->
HYPOTHÈSES -> TESTS -> QUALIFICATION.** Les phénomènes se découvrent; les modèles
ne les imposent pas. Les modèles continus sont des explications concurrentes
sérieuses et permanentes.

## 0. Interdictions méthodologiques héritées (non négociables)
- HMM interdit comme détecteur autonome de régimes; ses états ne sont jamais des
  "régimes économiques établis" (au mieux: résumé descriptif étiqueté comme tel).
- Segmentation BIC interdite comme preuve de régimes de volatilité (Phase S).
- MSM non validé pour l'identification séparée des échelles (S3): ne pas l'invoquer.
- Interdit d'optimiser une méthode pour obtenir des états "plus nets".
- Aucun nombre prédéfini d'hypothèses, de régimes ou d'anomalies.
- Corpus certifié intact; Holdout jamais ouvert; OOS jamais utilisé pour calibrer
  ou sélectionner un modèle.

## 1. Comportements et dimensions réellement observables (données natives Bid/Ask)
Uniquement ce que le corpus certifié contient: bid, ask, mid construit, spread
absolu/relatif, horodatages microseconde, ordre d'événements, inter-arrivées,
types de mises à jour (bid-seul/ask-seul/les deux), gaps, et les variables
certifiées (K10). Exclus comme inobservables: volume réel, transactions, carnet,
delta, exécutions.

## 2. Méthodes descriptives par dimension (exploration, pas de modèle d'états imposé)
| Dimension | Méthodes descriptives | Question scientifique |
|---|---|---|
| Distributions tick et granulées | quantiles robustes, queues (EVT descriptif), moments par tiers d'IS | Que vaut la forme, et change-t-elle dans le temps? |
| Volatilité | |r| autocorrélations multi-retards, variance par granularité, courbes d'agrégation | Persistance: continue (type GARCH/ARFIMA) ou par paliers? |
| Spread | distribution conditionnelle au temps/activité, réversion mesurée | Le spread est-il une variable d'état informative ou un bruit de cotation? |
| Rythme | processus d'inter-arrivées, intensité conditionnelle | L'arrivée des cotations porte-t-elle une structure propre? |
| Microstructure bid/ask | décomposition des événements, corrélations croisées décalées -5..+5 (piste ANOM-001) | Une jambe mène-t-elle l'autre? |
| Gaps/événements | classes de durée, distributions post-événement vs témoins appariés | Que change un événement, combien de temps? |
| Dépendances | autocorrélations signées/absolues multi-échelles, corrélations conditionnelles petit nombre justifié | Qu'est-ce qui est lié, à quelle échelle? |

## 3. Modèles continus de référence (concurrents obligatoires)
Toute structure apparemment discrète devra battre ou se distinguer de:
GARCH(1,1) et variantes à mémoire (FIGARCH/ARFIMA sur |r|), processus à volatilité
stochastique continue, marche aléatoire à variance lentement variable.
Règle: si un modèle continu explique la structure aussi bien (critère prédictif
préenregistré, protocole type T4), la qualification "régime discret" est REFUSÉE
et la structure reste descriptive continue. Les états discrets sont l'hypothèse
extraordinaire; la continuité est l'hypothèse par défaut.

## 4. Détection d'anomalies (après description, avant hypothèses)
Écarts mesurés par rapport à des références descriptives explicites (pas à des
états imposés): scores robustes roulants causaux, extrêmes conditionnels à la
granularité, ruptures de distribution confirmées sur deux granularités voisines.
Chaque détection candidate suit la qualification en 5 mesures et le registre
ANOM à 15 champs; statut initial maximal: OBSERVATION À VÉRIFIER.

## 5. Caractérisation et stabilité
Un phénomène n'avance que s'il est: présent dans au moins 2 des 3 tiers d'IS avec
le même signe/sens; d'amplitude rapportée avec intervalles (bootstrap par blocs);
stable à un changement de granularité voisin (pas un artefact d'échelle unique);
documenté avec effectifs réels. Sinon: INCONCLUSIF ou REJETÉ, conservé.

## 6. Correction de l'ambiguïté "variation inter-régime" (P1 révisé)
Le critère P1 précédent supposait des régimes déjà établis: **il est remplacé**.
Nouvelle définition, applicable sans aucun régime préalable:
- **Variation non triviale d'une structure candidate**: l'écart de la statistique
  entre les quantiles extrêmes (Q1 vs Q5) de la variable de conditionnement
  causale doit dépasser 2x le spread_rel médian IS (K2) en unités comparables
  ET 25% en relatif, sur au moins 2 tiers d'IS.
- **Stabilité intra-condition ("plate")**: à conditionnement fixé, la statistique
  ne doit présenter ni tendance significative après correction BY, ni amplitude
  interne > 25% de l'écart Q1-Q5.
Le mot "régime" est banni des critères tant qu'aucune structure n'a passé
la comparaison aux modèles continus du §3.

## 7. Génération d'hypothèses (après observation seulement)
Admission selon GOUVERNANCE_GENERATION_VAGUES (5 conditions, citation K/ANOM,
nouveauté démontrée, jamais de reparamétrage d'une rejetée). Le nombre découle
des phénomènes qualifiés. Dépendances et multiplicité: compteur cumulatif
permanent (actuellement 148 tests + 3 vagues descriptives documentées), BY,
bootstrap par blocs pour toute inférence; la confirmation exige l'OOS intact
(protocole gelé, usage unique par test type T4), puis le Holdout en finale
autorisée séparément.

## 8. Séparation des échantillons
IS: découverte et description (seul échantillon lu en 1R). OOS: confirmation
unique des hypothèses verrouillées, jamais de calibration/sélection. Holdout:
scellé (ouverture unique, autorisation distincte, manifeste de verrouillage).

## 9. Critères de validation et d'arrêt
- Validation d'un phénomène: §§5-6 satisfaits + mécanisme recherché (preuve
  directe type ANOM-001) + survie face aux modèles continus (§3).
- Arrêt d'une piste: instabilité inter-tiers; amplitude structurellement sous le
  spread sans mécanisme de coût différent; mécanisme réfuté; explication continue
  équivalente (le discret est alors refusé).
- Arrêt global possible: aucune structure qualifiée après exploration complète
  des dimensions du §2 = conclusion scientifique valide et complète.

## 10. Modifications par rapport à la version précédente
1. Suppression du HMM comme brique de découverte (disqualifié par contrôle négatif).
2. Segmentation reléguée aux changements de niveau, jamais preuve de régime.
3. Les modèles continus deviennent concurrents obligatoires et hypothèse par défaut.
4. P1 réécrit sans présupposer de régimes (§6).
5. L'exploration descriptive multi-granularité précède toute modélisation d'états;
   les états discrets deviennent une conclusion à prouver, pas un outil.

## 11. Point exact de départ possible de la Phase 1R
Après décision explicite du propriétaire sur ce protocole: première tâche =
construction des séries descriptives granulées causales sur IS (granularités
justifiées: événementielle de référence, activité, volatilité cumulée), avec
préenregistrement des statistiques et des seuils des §§5-6, verrouillage par
chaîne, puis exécution distante par checkpoints. Aucune lecture réelle n'a été
faite pour préparer ce document.
