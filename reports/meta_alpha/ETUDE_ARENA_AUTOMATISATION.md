# Étude vérifiée — le raisonnement scientifique peut-il tourner sans session Arena ?

## Mécanismes examinés (état réel, pas théorique)
1. **GitHub Actions**: exécute du code déterministe sur événement. Aucun accès LLM:
   aucun secret de type clé API LLM n'existe dans le dépôt, budget 0 Fcfa.
   Un workflow ne peut donc ni "raisonner" ni appeler Arena. Vérifié: les seuls
   secrets présents servent à Kaggle (KGAT) — rien d'autre.
2. **Déclencheurs**: push sur la branche (prouvé), `workflow_call` entre workflows
   de la branche (prouvé, run 43600799707). `workflow_dispatch`, `workflow_run`,
   `schedule` (cron): exigent les fichiers sur la branche par défaut `main`
   (limite GitHub documentée, fusion non effectuée: session contrainte à sa branche).
3. **Kaggle**: authentification prouvée; kernels éphémères pilotables par API
   (`metaalpha/dispatch.py` existe). Un kernel ne peut pas appeler Arena non plus;
   il peut exécuter du code et rendre des fichiers — même classe que Actions.
4. **Arena**: l'agent n'existe que pendant une session active ouverte par
   l'utilisateur. Il n'existe aucun webhook, cron ou réveil d'Arena dans
   l'infrastructure accessible. Prétendre le contraire serait simuler une
   intelligence absente — interdit par le mandat.

## Conclusion factuelle
Le raisonnement LLM **ne peut pas** fonctionner sans session Arena active et sans
budget supplémentaire (clé LLM externe = dépense non autorisée). Ce n'est pas un
choix, c'est l'état des ressources autorisées.

## Meilleure solution compatible (implémentée)
- **Couche déterministe autonome (serveurs, 24/7 par événements)**: calculs,
  checkpoints, reprise, gate statistique codé (`gate_engine.py`, verdicts
  historiques reproduits), classification quantitative des échecs, registre
  verrouillé par chaîne de hash ancrée dans Git (`TRIAL_LEDGER_CHAIN.json`,
  falsification détectée au test), compteurs cumulatifs.
- **File de décision** `DECISION_REQUISE.json`: les serveurs déposent diagnostics
  et contexte; dès qu'une session Arena s'ouvre — votre retour suffit, aucun ordre
  détaillé n'est requis — je consomme la file, je raisonne à partir de la base K,
  je préenregistre et je déclenche la vague suivante.
- **Effet pratique**: votre PC et votre présence ne sont nécessaires ni pour les
  calculs ni pour les gates; seule la *conception d'une nouvelle vague* attend une
  session — et elle est alors immédiate, car tout le contexte chiffré l'attend.
