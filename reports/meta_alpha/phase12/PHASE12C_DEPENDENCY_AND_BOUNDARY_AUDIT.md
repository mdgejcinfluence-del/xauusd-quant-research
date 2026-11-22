# PHASE 12-C — AUDIT DES DÉPENDANCES ET DES FRONTIÈRES

**Documentaire uniquement. Aucun accès au holdout (ni montage, ni
listage, ni lecture de données ou de métadonnées) pendant sa
rédaction.**

## 1. Dépendances du modèle à confirmer

| Élément | État | Source vérifiable |
|---|---|---|
| Code d'entraînement/évaluation | GELÉ par hash | `ci_tools/phase12b_engine.py`, SHA-256 `a1c9f52d9ddeb7160e2113ded3ad95da29926518ccc7b50117922117e2ee597b` |
| Code d'extraction bornée | Inclus au moteur (`features_bornees`) | idem ; tests `ci_tools/phase12b_temporal_tests.py` `b21bc998299220adf85730c87a7610e7855a01cdbca1aca48da1fadbc271c1cd` (5/5) |
| Données d'entraînement | GELÉES par hash | `PHASE12B_FEATURES.csv` `6f684ee882b4c840ab27255864266729095b4fa4b52275821923f10a53c16485` (segment APPRENTISSAGE H1, n = 1 640) |
| Variables, ordre, encodage, transformations | Définis au manifeste | `PHASE12C_MODEL_FREEZE_MANIFEST.json` (variables brutes, référence ASIA) |
| Fréquence M0 | GELÉE : 0,7591463414634146 (1245/1640) | `PHASE12B_RESULTS.json`, `PHASE12B_MODEL_EVALUATION.csv` |
| Formules des métriques | Au code gelé | Brier, log-loss, AUC de Mann-Whitney, écrêtages documentés |
| **Coefficients β et intercept M1** | **NON ARCHIVÉS (ANO-12B-01)** | Absents de tous les artefacts 12-B — blocage §2 du protocole |
| **Versions pandas/numpy** | **NON ÉPINGLÉES** | Workflow du run 45028022637 : `pip install -q pandas numpy` sans version ; Python 3.11 consigné |
| Dépendances système/BLAS | Non consignées | Risque de reproduction numérique traité au §2 du protocole (vérification des métriques à la précision publiée, arrêt si écart) |

Conclusion dépendances : la chaîne de reproduction est complète à
deux éléments près (coefficients, versions), levables sans holdout
par l'étape préalable préenregistrée. En l'état : modèle non
figeable, `PHASE12C_BLOCKED`.

## 2. Frontières et indépendance

- **Frontière IS/holdout : 2020-01-01T00:00 UTC** (clôture de la
  bougie déclencheuse). Le corpus IS de référence reste les 282
  partitions documentées (3 540 993 barres M1, couverture 11-C) ;
  le holdout 2020–2026 n'a été ni monté, ni listé, ni lu pendant
  les Phases 11 et 12 — son existence et son périmètre sont ceux
  documentés depuis le gel des protocoles, sans aucune métadonnée
  nouvelle consultée pour ce document.
- **Chevauchements de fenêtres** : fenêtre d'observation de
  8 bougies H1 ; tout événement dont la fenêtre chevauche la
  frontière est exclu des deux côtés.
- **Grappes** : grappes IS gelées par la carte 11-B.1
  (`3281f594…`) ; les grappes du futur corpus holdout seront
  construites indépendamment par la méthode historique ; toute
  grappe à cheval sur la frontière exclut ses événements holdout.
- **Dépendances statistiques résiduelles** : événements voisins
  partageant une fenêtre sont traités par la purge de frontière et
  l'exclusion par grappe ; aucune grappe ne peut réunir un
  événement d'entraînement (2010–2015) et un événement de
  confirmation.
- **Chronologie** : ajustement (2010–2015) < évaluation IS
  (2018–2020) < confirmation (2020–2026) ; aucune information du
  holdout ne peut refluer vers M0, M1, la cible ou les seuils.
- **Censure** : règles 11-A/12-A inchangées (horizon < 8 →
  CENSORED, ordre intraminute indéterminé → AMBIGUOUS), jamais
  converties en étiquettes.

## 3. Risques résiduels documentés

1. Reproduction numérique des coefficients (BLAS/versions) :
   mitigée par la vérification obligatoire des métriques 12-B à
   la précision publiée avant tout gel des coefficients.
2. La détection d'événements sur le holdout réutilisera la
   procédure gelée Phase 10 ; tout écart de couverture ou de
   provenance du corpus holdout devra arrêter l'exécution
   (BLOCKED), sans adaptation des définitions.
3. Le résultat, même favorable, restera une confirmation
   historique hors IS — pas une validation prospective, pas une
   preuve de rentabilité.

## 4. Verdict de l'audit

Frontières, M0, métriques, critères et contrôles d'indépendance
sont entièrement définis ; **l'unique point bloquant est la
non-conservation des coefficients M1 et des versions de
dépendances (ANO-12B-01)**. Verdict : `PHASE12C_BLOCKED`, levable
par la seule étape de reproduction déterministe du protocole §2,
séparément autorisée et sans accès au holdout.
