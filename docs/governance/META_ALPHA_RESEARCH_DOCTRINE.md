# META ALPHA — DOCTRINE DE RECHERCHE

*Processus opérationnel de découverte d'un modèle économique
(mission fondatrice 009). À lire avant toute nouvelle mission.*

## Pipeline standard d'un dossier

1. **Contrôle garde-fou** (`META_ALPHA_DRIFT_GUARD.md`) : classement
   VERT/JAUNE/ORANGE/ROUGE motivé, consigné au journal des décisions.
2. **Trois questions** : modèle économique supposé ; pourquoi il peut
   payer (phénomène + risque rémunéré) ; comment l'exploiter nous-mêmes.
3. **Extraction économique** des observations existantes (ne pas
   relancer de campagnes déjà faites : vérifier le registre des
   connaissances et les checkpoints d'abord).
4. **Hypothèses concurrentes** énumérées, avec pour chacune la signature
   qui la distinguerait et le test le moins coûteux.
5. **Détection dans le corpus** : signature recherchée dans les ticks
   (fréquence, amplitude, résorption, horizons), avant tout backtest
   général.
6. **Edge brut puis net** : rendement par opportunité, coûts réalistes
   comptés une fois (spread, commission, slippage, financement),
   espérance, PF, drawdown, durées, exposition, régimes défavorables.
7. **Moteur candidat propre** (nos règles, pas celles du trader), gelé
   par hash dès sa première évaluation ; jamais d'optimisation sur la
   période d'évaluation présentée ensuite comme validation.
8. **Validation indépendante** : données non utilisées pour construire
   le modèle ; sinon statut maximal CANDIDATE_ENGINE.
9. **Registre** : fiche modèle mise à jour (état, preuves, limites,
   dépendances) et procès-verbal au ledger chaîné.
10. **Clôture** : verdict qualifié (DÉMONTRÉ / FORTEMENT ÉTAYÉ /
    COMPATIBLE MAIS NON IDENTIFIÉ / NON DÉMONTRABLE / RÉFUTÉ), livrables
    avec manifeste SHA-256, HEAD distant vérifié, arbre propre.

## Règles de coût de recherche

- Une mission sans incertitude réduite ni décision modifiée n'est pas lancée.
- Un problème déjà testé et non identifiable avec les données actuelles
  n'est pas répété : on documente la frontière et l'observation minimale
  qui la franchirait.
- La progression se mesure en connaissance économique nouvelle, pas en
  nombre de rapports, scripts ou backtests.
- Autonomie technique complète (méthodes, outils, métriques) ; aucune
  modification silencieuse de l'objectif stratégique.

## États des modèles (registre)

DISCOVERED, HYPOTHESIS, IDENTIFICATION_IN_PROGRESS, SIGNATURE_DETECTED,
CANDIDATE_ENGINE, VALIDATION_IN_PROGRESS, VALIDATED (edge net sur
données indépendantes uniquement), CONDITIONAL, REJECTED,
INSUFFICIENT_DATA.
