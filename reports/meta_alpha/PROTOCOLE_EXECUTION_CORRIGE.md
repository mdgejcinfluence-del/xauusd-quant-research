# PROTOCOLE D'EXÉCUTION CORRIGÉ — découverte de régimes et granularisation
(Corrige la contradiction signalée : aucune donnée réelle ne doit être exploitée
par une chaîne non validée sur simulation. Aucune phase ci-dessous n'est lancée
par ce document.)

## 1. Correspondance ancien plan (Blueprint §9) -> plan corrigé
| Ancien plan (Blueprint) | Plan corrigé | Dépendances | Porte de validation (gate) |
|---|---|---|---|
| — (absent) | **Phase 0. Hygiène du corpus** (en cours, autorisée) : réconciliation, gaps classifiés, quotes croisées/verrouillées, doublons, résolution | Baseline figée | Rapport Phase 0 accepté par le propriétaire |
| Étape 1. Représentations granulées sur IS réel | **Phase S. Validation simulée de la chaîne** : générer des séries synthétiques à régimes CONNUS (changement de volatilité/spread/lead-lag injectés, paramètres tirés des ordres de grandeur K, jamais des ticks réels copiés), exécuter granularisation + segmentation + caractérisation, mesurer si la chaîne retrouve les régimes injectés (taux de détection, délai, faux positifs sur séries sans régime) | Phase 0 | Critères préenregistrés atteints sur simulation, y compris **zéro régime halluciné** sur contrôles sans rupture au taux annoncé |
| Étape 2. Cartographie PELT réelle | **Phase 1R. Représentations + cartographie sur IS réel** (chaîne déjà validée en S) | Phase S validée | Stabilité des segments entre tiers d'IS (seuil préenregistré) |
| Étape 3. États causaux (BOCPD/HMM) | **Phase 2R. États causaux sur IS**, HMM confronté, nombre d'états par validation prédictive intra-IS (sous-périodes) | Phase 1R | Profils stables; états non stables rejetés et conservés |
| Étapes 4-5. Caractérisation + anomalies conditionnelles | **Phase 3R. Anomalies conditionnelles intra-état** (5 mesures, registre ANOM) | Phase 2R | Qualification phénoménologique complète |
| Étape 6. Mécanismes | **Phase 4R. Preuves de mécanisme** (décompositions directes, témoins) | Phase 3R | Mécanisme démontré ou piste arrêtée |
| Étape 7. Hypothèses | **Phase 5R. Hypothèses préenregistrées** puis gate v2, puis **confirmation OOS** (voir §2 T4) | Phase 4R + autorisation | Gate + OOS selon protocole gelé |

Règle d'or corrigée: **simulation d'abord, réel ensuite**, à chaque fois qu'une
nouvelle brique de chaîne est introduite (pas seulement la première fois).

## 2. Frontières statistiques précisées
### T4 — comparaison hors échantillon ARFIMA contre MSM (modèle à changement de régime markovien)
- Les deux modèles sont estimés **uniquement sur IS** (paramètres, nombre de régimes
  MSM, ordres ARFIMA), avec toutes les formes fonctionnelles **préenregistrées**
  (familles, critères de choix: BIC intra-IS uniquement) AVANT tout calcul.
- Comparaison sur OOS en **prévision récursive causale**: à chaque origine OOS,
  seuls les paramètres estimés sur le passé (IS + OOS déjà écoulé si le protocole
  préenregistré autorise la réestimation glissante; sinon paramètres figés IS)
  sont utilisés. Aucune frontière de régime rétrospective OOS n'alimente les modèles.
- Métrique préenregistrée unique (ex. log-vraisemblance prédictive à 1 pas sur la
  série granulée + erreur quadratique), test de Diebold-Mariano avec erreurs HAC,
  résultat conservé quel qu'il soit. L'OOS ne sert qu'une fois pour ce test;
  toute modification après lecture = nouvel essai compté, confirmation impossible
  sur le même OOS (il faudrait alors le Holdout, interdit sans autorisation finale).

### Données consultables par étape (matrice d'accès)
| Étape | IS | OOS | Holdout |
|---|---|---|---|
| Phase 0 hygiène | lecture descriptive | non (sauf mesures 348 déjà figées en Phase 2) | **jamais** |
| Phase S simulation | synthétique seulement (+ ordres de grandeur K publiés) | non | jamais |
| Phases 1R-4R découverte | oui | **non** | jamais |
| Phase 5R confirmation | oui (estimation) | oui, une fois, protocole gelé | jamais |
| Évaluation finale | — | — | ouverture unique, autorisation distincte, manifeste de verrouillage |

### Critère P1 — "variation non triviale et statistique plate" (définition opérationnelle)
À préenregistrer avant calcul, valeurs gelées:
- **Variation non triviale**: l'écart entre régimes sur la statistique cible
  (ex. volatilité réalisée médiane par état) doit dépasser **2x le spread_rel médian
  IS (K2)** en unités comparables ET 25% en relatif — en dessous, les états sont
  déclarés économiquement indiscernables, piste arrêtée.
- **Statistique plate**: à l'intérieur de chaque régime retenu, la pente de régression
  de la statistique cible sur le temps intra-régime doit être non significative après
  correction (BY) ET son amplitude totale < 25% de l'écart inter-régimes — sinon le
  "régime" est une tendance découpée, pas un état.

### Exploration des 270 cellules sans sélection opportuniste
- Les 270 cellules (granularités x échelles x statistiques, grille à figer AVANT
  calcul dans le préenregistrement) sont **toutes** calculées et publiées; interdiction
  de ne rapporter que la meilleure.
- Correction globale: BY sur l'ensemble des 270 (plus compteur cumulatif des vagues
  antérieures). La "meilleure cellule" n'a aucun statut spécial: un phénomène n'est
  retenu que s'il (a) survit à la correction, (b) est présent dans au moins 2 des 3
  tiers d'IS avec le même signe, (c) dépasse le filtre d'amplitude P1.
- La grille elle-même est un choix scientifique documenté; toute cellule ajoutée
  après coup compte comme nouvelle vague au compteur.

### Conservation des négatifs et des tentatives
- Chaque tentative (y compris simulations échouées et segmentations instables) est
  committée avec code, configuration, hashes et verdict; le compteur cumulatif ne se
  remet jamais à zéro; les registres sont chaînés (TRIAL_LEDGER_CHAIN.json) et
  vérifiés avant exécution.

## 3. Autorisations nécessaires pour la suite (aucune n'est accordée par ce document)
1. Acceptation du rapport Phase 0. 2. Autorisation Phase S (simulation).
3. Autorisation Phases 1R-4R (découverte IS réelle). 4. Autorisation Phase 5R
(confirmation OOS, usage unique). 5. Autorisation distincte Holdout (finale).
6. Autorisation distincte pour tout usage robot/réel (hors périmètre actuel).
