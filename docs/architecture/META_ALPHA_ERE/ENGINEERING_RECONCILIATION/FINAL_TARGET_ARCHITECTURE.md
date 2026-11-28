# RÉCONCILIATION — ARCHITECTURE CIBLE FINALE (proposée)

## Forme

**Monolithe scientifique modulaire** dans le dépôt existant : les neuf
moteurs deviennent, le moment venu et sur décision du fondateur, des
packages Python aux interfaces typées — pas des services. Les scripts
actuels restent les adaptateurs d'exécution via la CI.

## Répartition des responsabilités (réconciliée avec le réel)

| Acteur | Responsabilité cible | Ne fait jamais |
|---|---|---|
| **Fondateur** | approbations structurantes : porte H, dépenses, doctrine, accès aux zones protégées | — |
| **ARENA (agent en session)** | supervision scientifique : formuler hypothèses et protocoles, préenregistrer, lire les preuves, rédiger les verdicts proposés | n'est pas un service ; aucun état critique ne vit dans la conversation |
| **GitHub (branche dédiée)** | source de vérité : code, contrats, protocoles gelés, registre chaîné, manifestes, décisions | ne stocke ni ticks ni gros artefacts |
| **GitHub Actions** | exécution par lots prouvée : téléchargement des partitions (gdown), calcul, vérification, commit des résultats ; collecte prospective quotidienne | n'attend pas indéfiniment ; pas de secret exposé dans les journaux |
| **Kaggle** | stockage bulk existant (datasets de migration des partitions), lecture vérifiée | aucun PAT GitHub ; pas (encore) de plan de calcul tant que la qualification kernels n'a pas été décidée et testée |
| **Stockage externe (Drive)** | source actuelle des 348 partitions certifiées, inventaire hashé | jamais d'écrasement des partitions certifiées |

## Principes conservés des deux sources

- Protocole gelé avant calcul, registre append-only, reprise par
  shard/protocole, publication seulement après vérification des hashes.
- Trois objets épistémiques séparés ; niveaux de preuve N0–N7 ;
  porte H ; segmentation découverte/construction/validation/prospectif.
- CPU d'abord ; extensions scientifiques (PyMC/Stan, EIG, SBI) uniquement
  sur goulot ou gain d'information démontré — recommandation du dossier
  externe que notre historique confirme (nos réfutations ME-002/ME-003
  n'auraient rien gagné à un GPU).

## Ce qui n'est pas dans la cible

Microservices, queue/PostgreSQL, orchestrateur distribué, base
vectorielle, service permanent quelconque, connectivité de trading,
API ARENA inventée. Chacun pourra être réexaminé sur déclencheur
mesurable consigné (quotas dépassés plusieurs campagnes, tâche non
partitionnable, besoin de concurrence réelle).
