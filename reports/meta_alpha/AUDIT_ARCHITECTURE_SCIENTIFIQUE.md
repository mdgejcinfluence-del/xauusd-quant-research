# AUDIT — ce qui manque réellement pour un moteur de découverte scientifique autonome
### (P3-002 en cours d'exécution n'a été ni modifié ni interrompu: run 43600799780)

## 1. Audit du code existant (vérifié fichier par fichier)
| Capacité requise | État réel | Preuve |
|---|---|---|
| Exécution distante, checkpoints, reprise | ✅ codé et prouvé | moteurs p3/p4, STATE*.json, runs réels |
| Conservation des résultats (succès/échecs) | ✅ | commits `if: always()`, trades P4 conservés |
| Préenregistrement avant test | ⚠️ procédural | registre committé avant le run (Git horodate), aucun verrou technique |
| Gate statistique (FDR, filtre économique) | ❌ non codé | critères en texte libre dans le registre; calculs faits par Arena en session |
| Diagnostic des causes d'échec | ❌ non codé | `orchestrate.py` journalise une phrase, figé sur P3-001 |
| Génération d'hypothèses | ⚠️ générateur mécanique | `gen_p3_002.py`: produit cartésien features×quintiles×horizons — exactement le "générateur de combinaisons" à dépasser |
| Chaînage inter-workflows | ⚠️ partiel | `workflow_call` prouvé (run 43600799707); `workflow_run`/`workflow_dispatch`/`schedule` exigent la branche par défaut |
| État permanent consultable | ✅ créé, mise à jour manuelle | `ETAT_PERMANENT.md` (à automatiser, voir §3) |
| Protection anti-retest | ⚠️ convention | texte dans le registre; aucun contrôle technique |
| Appel à un LLM depuis GitHub | ❌ impossible en l'état | aucun secret/clé LLM, budget 0: aucun workflow ne peut "raisonner" |

## 2. Ce qu'Arena peut réellement faire — sans invention
Arena (moi) n'existe que pendant une session active: je ne tourne pas en arrière-plan
entre les conversations, aucun réveil automatique d'Arena n'existe dans l'infrastructure.
Dans une session, je peux: lire les résultats committés (`git pull`), calculer les
gates, raisonner, écrire un nouveau registre justifié, committer et pousser le fichier
déclencheur — le serveur exécute alors sans vous. GitHub Actions, lui, exécute du code
déterministe 24/7 par événements, mais ne peut pas raisonner (pas de LLM disponible).
Kaggle est authentifié (token KGAT) et son moteur de dispatch existe dans le code V1,
mais il n'a encore exécuté aucun calcul scientifique — c'est une capacité disponible,
pas un fait accompli.

## 3. Architecture d'implémentation (sur l'infrastructure existante, 0 Fcfa)
Principe: **séparer le déterministe (serveurs) du raisonnement (Arena), et coder tout
ce qui est codable pour que l'intervalle entre deux raisonnements soit productif.**

1. **Base de connaissances certifiée** (créée aujourd'hui): `BASE_CONNAISSANCES_PHASE2.md`
   (K1-K10). Règle d'admission: toute hypothèse cite un K et un résultat antérieur;
   sans citation, le générateur la refuse. Fin des combinaisons arbitraires.
2. **Moteur de gate déterministe** `ci_tools/gate_engine.py` (à coder, prochaine étape):
   lit `P3_00X_RESULTS.json`, calcule p-values, BH-FDR global cumulatif (toutes vagues
   confondues, compteur lu dans le registre cumulatif), filtre économique (amplitude
   vs spread médian K2), stabilité par sous-périodes IS (3 blocs) et classification
   des causes d'échec par règles quantitatives explicites:
   AMPLITUDE_INSUFFISANTE (effet < spread), ABSORBE_PAR_SPREAD (mid+ mais net-),
   INSTABLE (signes opposés entre blocs), DEPENDANCE_PROBABLE (significativité qui
   s'effondre en erreurs par blocs), AUCUN_SIGNAL. Sortie: `GATE_P3_00X.json` structuré.
3. **Registre protégé techniquement**: à chaque préenregistrement, le générateur écrit
   le registre + son SHA-256 dans un fichier verrou séparé committé; le workflow de
   test **vérifie le hash avant de calculer** et refuse de tourner si le registre a été
   modifié après verrouillage. Le Trial Ledger devient cumulatif machine
   (`TRIAL_LEDGER.json`: compteur global d'hypothèses, indispensable au FDR cumulatif).
4. **File de décisions pour Arena**: le gate dépose `DECISION_REQUISE.json`
   (diagnostics chiffrés, familles épuisées, dimensions non explorées de la base K).
   Dès qu'une session Arena s'ouvre (votre retour, ou tout message), je consomme cette
   file en premier, je formule la vague suivante justifiée (chaque hypothèse -> K +
   diagnostic parent), je la préenregistre, je déclenche. Entre sessions, les serveurs
   terminent les calculs en cours et les gates déterministes; ils n'inventent pas de science.
5. **Chaînage sans humain**: un workflow "cycle" unique par vague utilise
   `workflow_call` (prouvé) pour enchaîner calcul -> gate -> mise à jour de
   `ETAT_PERMANENT.md` automatique (compteurs lus dans les JSON, plus d'édition manuelle).
   La vague suivante démarre soit par mon déclenchement en session, soit — pour les
   vagues dont la génération est devenue déterministe (familles déjà justifiées par K) —
   par le même workflow cycle. Aucune boucle infinie: le cycle s'arrête toujours sur
   `DECISION_REQUISE` quand une famille nouvelle exige un raisonnement.
6. **État permanent automatique**: régénéré par le workflow de gate depuis les fichiers
   d'état (runs, compteurs, incidents, prochaine action) — consultable par simple
   actualisation, sans dépendre de ma présence.

## 4. Ce qui restera humain/propriétaire (inchangé)
Feu vert scientifique+économique d'un candidat, ouverture du Holdout (sceau unique),
dépense, réel. Tout le reste — y compris la conception des vagues ordinaires par Arena
à partir de la base K et des diagnostics codés — ne nécessite plus votre intervention.

## 5. Prochaines étapes d'implémentation (ordre)
(a) attendre la fin de P3-002 sans y toucher; (b) coder `gate_engine.py` + verrouillage
par hash + ledger JSON cumulatif, testés sur les résultats P3-001/P4-001 déjà connus
(ils doivent reproduire: H-P3-A générée puis REJETÉE); (c) appliquer le gate codé à
P3-002 dès ses résultats; (d) consommer la file de décision et préenregistrer P3-003
uniquement à partir de K et des diagnostics — pas de reparamétrage des rejetées.
