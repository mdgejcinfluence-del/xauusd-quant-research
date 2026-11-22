# PHASE 13-A.1 — ADDENDUM DE CAUSALITÉ D'EXÉCUTION

**Nature : correction et gel documentaires. Aucun backtest, aucune
simulation, aucun calcul économique, aucune extraction de données
ne sont effectués par la présente mission.**
**Documents de référence (non modifiés) : `PHASE13A_ECONOMIC_RESEARCH_PROTOCOL.md`
(`a4d85f00…`), `PHASE13A_EXECUTION_CONTRACT.json` (`03e1f7eb…`),
`PHASE13A_PREREGISTRATION.json` (`56d408f3…`), verdict 13-A
`PROTOCOL_READY_FOR_ECONOMIC_EVALUATION` (seq328). Le présent
addendum et le contrat V2 **remplacent, pour toute étude future,
la convention d'entrée de la section 3 du protocole 13-A et du
contrat 13-A**, dont le défaut de causalité est consigné ci-dessous.
Aucun ancien document n'est écrasé.**

## 1. Défaut identifié dans la convention 13-A

Le protocole 13-A définissait `t_reintegration` comme la clôture
de la minute M1 confirmant la réintégration, puis retenait comme
prix d'entrée le prix d'ouverture Ask/Bid de « la première minute
M1 commençant à `t_reintegration` », c'est-à-dire le premier tick
de cette même minute. Or ce premier tick est **antérieur ou au
mieux concomitant** au moment où la clôture confirmant la
réintégration — et donc le signal et la probabilité `p_M1` —
devient disponible. Utiliser ce prix reviendrait à exécuter avant
de connaître le signal : biais d'anticipation (look-ahead). Cette
convention est **abrogée** par le présent addendum.

## 2. Convention causale obligatoire (gelée)

- **`t_decision`** : timestamp UTC de clôture de la minute M1
  confirmant la réintégration (définition gelée des phases
  antérieures, inchangée).
- La probabilité `p_M1` du modèle H1 gelé est calculée **après**
  disponibilité de cette clôture. Aucune information postérieure à
  `t_decision` n'entre dans le calcul de `p_M1` ; aucune
  information antérieure ou concomitante ne peut servir de prix
  d'exécution.
- Décision d'exposition uniquement si
  `p_M1 > 0.7591463414634146` (M0 gelé, inchangé ; aucun autre
  seuil, aucune optimisation).
- **Entrée** : première cotation tick Bid/Ask réelle dont le
  timestamp `quote_timestamp` vérifie strictement

  `t_decision < quote_timestamp < t_decision + 60 secondes`.

  - Position longue (direction +1) : prix d'entrée = **Ask** de
    cette première cotation.
  - Position courte (direction −1) : prix d'entrée = **Bid** de
    cette première cotation.
- Si aucune cotation exécutable n'existe dans cette fenêtre
  ouverte : **`NON_EXECUTION`**, comptée et publiée comme telle.
- Interdictions associées : ne jamais utiliser une cotation
  antérieure ou égale à `t_decision` ; ne jamais remplacer la
  première cotation disponible par une cotation ultérieure plus
  favorable ; ne jamais reconstruire le prix d'entrée à partir de
  prix Mid ; la règle doit être appliquée sur les **ticks Bid/Ask
  réels** (partitions tick IS, Kaggle privé du propriétaire, pour
  toute étude future de niveau 2).
- Traçabilité obligatoire pour toute exécution future :
  `t_decision`, `quote_timestamp` exact de la cotation
  sélectionnée, côté utilisé (Ask/Bid), prix, direction, valeur de
  `p_M1`, et statut (`EXECUTE` / `NON_EXECUTION` avec motif).

## 3. Sortie exécutable (convention primaire unique, inchangée et précisée)

Sortie unique : clôture de la fenêtre gelée de huit bougies H1
suivant la bougie déclencheuse (définition des phases antérieures,
inchangée ; la cible prédictive de continuation n'est pas une
sortie économique).

- Position longue : prix de sortie = **Bid** de clôture de la
  dernière minute M1 de la fenêtre (dernier tick Bid/Ask de cette
  minute).
- Position courte : prix de sortie = **Ask** de clôture de cette
  même minute.
- L'entrée et la sortie sont évaluées sur des cotations réellement
  disponibles ; les horodatages exacts des cotations de sortie
  sont conservés.
- Fenêtre censurée, minute de sortie absente, prix non fini ou
  ≤ 0, spread non fini : événement exclu de la mesure primaire
  avec motif consigné, jamais prolongé, jamais remplacé par un
  prix inventé. Fermetures régulières et lacunes : règles de
  couverture et conditions d'arrêt préenregistrées en 13-A
  (NON_EXECUTION > 10 % ou spreads non finis > 5 % ⇒ NON
  MESURABLE en l'état).
- Le spread est intégré une seule fois, par les prix Bid/Ask
  d'entrée et de sortie. **Aucune seconde soustraction du spread
  n'est autorisée**, sous quelque forme que ce soit (y compris la
  convention historique Mid de la Phase 10, qui ne s'applique pas
  ici).

## 4. Portée

Le présent addendum ne change ni le modèle H1 (coefficients et
encodage gelés, `PHASE12C1_MODEL_PARAMETERS.json`, `1bcb3b70…`),
ni la règle d'exposition, ni la sortie primaire, ni les mesures de
risque préenregistrées en 13-A. Il corrige uniquement la causalité
du prix d'entrée et précise les prix exécutables de sortie. Les
conventions de coûts définitives sont gelées dans
`PHASE13A1_COST_CONVENTION.json` et le contrat complet dans
`PHASE13A1_EXECUTION_CONTRACT_V2.json`. Le holdout 2020–2026,
consommé, reste définitivement exclu. La Phase 13-B (étude
économique exploratoire sur l'IS) reste soumise à une décision
distincte.
