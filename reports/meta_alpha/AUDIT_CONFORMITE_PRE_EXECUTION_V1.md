# AUDIT DE CONFORMITÉ SCIENTIFIQUE PRÉ-EXÉCUTION — META ALPHA V1

**Date :** 13 novembre 2026 · **Périmètre :** avant toute montée L0→L4 (non autorisée à ce stade)
**Méthode :** lecture du code, exécution des tests, plan d'extraction réel sur les registres
du propriétaire, tests numériques indépendants sur jeux contrôlés. **Aucun calcul massif lancé.**

---

## 1. Registres et formules — enregistré ≠ implémenté

### 1.1 Les 11 variables instanciées (registres `META_ALPHA_WORK/.../10_REGISTRIES/`)
Colonnes sources du corpus réel : `timestamp_utc` (µs, UTC), `bid`, `ask` (unités : prix XAUUSD).

| Variable | Formule (registre v1) | Sources | Unité | Paramètres (propriétaire) | NULL |
|---|---|---|---|---|---|
| RET_H | mid[t+H] / mid[t] − 1 | bid, ask, timestamp | sans dimension | H = 1s…1h (7) | NULL si pas de cotation à l'horizon* |
| ROLL_STD_MID | écart-type roulant des variations de mid, N événements | bid, ask | prix | N = 50/100/500/1000 | NULL pendant warm-up |
| ROLL_RANGE_MID | max(mid) − min(mid) sur N événements | bid, ask | prix | N = 50/100/500/1000 | NULL pendant warm-up |
| ZSCORE_ROBUST | (retour − médiane roulante) / MAD roulante | bid, ask | sans dimension | fenêtres N ; seuil 4 (sens. 3, 5) | NULL pendant warm-up |
| UPDATE_INTENSITY | nombre de cotations sur T secondes | timestamp | événements/T | T = 1s/5s/30s | 0 si aucun événement (pas NULL) |
| INTERARRIVAL_MEAN | moyenne des écarts entre événements sur N événements | timestamp | secondes | N = 50/100/500/1000 | NULL pendant warm-up |
| SPREAD_REGIME | classe de spread, quantiles sur le PASSÉ uniquement | bid, ask, timestamp | classe 1..3 | 3 classes ; fenêtre 20 j (fallback 1 sem.) | NULL avant calibration |
| SUBPERIODE | découpage en sous-périodes calendaires | timestamp | catégorie | UTC + sessions documentées | **BLOQUÉE (sessions)** |
| REGIME_CLASS | classe de régime, quantiles de volatilité, passé uniquement | bid, ask, timestamp | classe 1..3 | quantiles / 3 ; fenêtre d'apprentissage **non spécifiée** | NULL avant calibration |
| MFE_H | excursion favorable maximale sur H | bid, ask futurs (label) | sans dimension | H = 5min/15min/1h | NULL si horizon incomplet |
| MAE_H | excursion adverse maximale sur H | bid, ask futurs (label) | sans dimension | H = 5min/15min/1h | NULL si horizon incomplet |

*Voir §3.3 : la règle d'alignement temporel exact de RET_H n'est pas encore certifiée.

Variables dérivables sans décision (F1) : MID, SPREAD_ABS, SPREAD_REL, RET_TICK —
traductions SQL présentes dans le code mais **non inscrites comme variables au registre**
par `instantiate_from_answers` (elles n'ont pas de paramètre libre) : écart de forme à
corriger lors de la certification, sans impact scientifique à ce stade.

### 1.2 État réel d'implémentation (plan d'extraction exécuté sur les registres)
`plan_extraction` sur les réponses réelles du propriétaire : **0 extractible / 11 refusées**.
- 9 × `FORMULE_NON_CERTIFIEE` : aucune traduction SQL certifiée (RET_H, ZSCORE_ROBUST,
  UPDATE_INTENSITY, INTERARRIVAL_MEAN, SPREAD_REGIME, SUBPERIODE, REGIME_CLASS, MFE_H, MAE_H).
- 2 × `PARAMETRE_MANQUANT` : ROLL_STD_MID / ROLL_RANGE_MID — le traducteur attend **une**
  fenêtre entière unique ; le propriétaire a légitimement répondu une **liste** [50,100,500,1000].
**Conclusion d'audit :** les 11 variables sont ENREGISTRÉES et SPÉCIFIÉES ; seules 6 formules
(MID, SPREAD_ABS, SPREAD_REL, RET_TICK, ROLL_STD_MID, ROLL_RANGE_MID) possèdent une traduction
SQL certifiée *pour une fenêtre unique*. Remédiation proposée (à valider, non appliquée) :
instancier chaque couple (variable, fenêtre) comme entrée distincte du registre
(ex. `ROLL_STD_MID@N=100`), puis traduire et tester une à une. Aucune extraction n'est
possible avant cela — le système refuse, et il a raison.

## 2. Validation numérique indépendante (nouveaux tests)
Fichier : `META_ALPHA_CODE_V1/META_ALPHA/tests/test_numeric_audit.py` — **9 tests, tous verts**,
implémentation de référence en Python pur, résultats attendus calculés à la main,
aucun code de production importé.
- F1 : mid/spread_abs/spread_rel sur cotation contrôlée (2300.0/2300.6).
- F2 : RET_TICK, RET_H ; rendements **Bid/Ask** (long = achat ask → revente bid) — démontré :
  le mid peut monter pendant que le long perd (coût du spread réel).
- F3 : rolling std/range en fenêtres **événements**, warm-up = NULL vérifié ligne à ligne.
- F4 : z robuste (médiane 11, MAD 1 sur jeu contrôlé, outlier à 50).
- F5 : inter-arrivées (2s, 3s, 4s → moyennes exactes) ; intensité en fenêtre **temps causale** (t−T, t].
- F8 : MFE/MAE d'un long (entrée ask, excursions sur bid futur) — signes et valeurs exacts.
- Propriété anti-lookahead : perturber le futur ne change aucune feature passée (test dédié).
- Split calendaire 60/20/20 sur 100 jours → 60/20/20 jours exacts ; purge 1h vérifiée.

## 3. Anti-lookahead
### 3.1 Features (utilisables à t)
Formules certifiées : `lag()` uniquement, fenêtres `ROWS BETWEEN n PRECEDING AND CURRENT ROW`.
Aucun `FOLLOWING`, aucun `lead` dans le code d'extraction (vérifié par recherche textuelle
et par le test de perturbation du futur). Règle registre : « disponible à t, calculé avec ≤ t ».
### 3.2 Labels (futur par définition — jamais des features)
RET_H, MFE_H, MAE_H regardent le futur **par construction** : ce sont des cibles.
Ils ne doivent jamais entrer dans une feature ni dans une décision à t. Leur chevauchement
crée une dépendance entre échantillons voisins : deux origines distantes de moins d'1h
partagent une partie de leur fenêtre de label.
### 3.3 Frontières 60/20/20 et purge
Split par durée calendaire (config certifiée), jamais aléatoire. **Purge minimale de 1h :
justifiée** car le plus long label vaut 1h — toute origine située à moins d'1h avant une
frontière a un label qui enjambe la frontière et doit être exclue du segment amont
(embargo symétrique recommandé à l'aval pour les features roulantes dont la fenêtre
chevauche la frontière en arrière : leur warm-up repart à NULL, aucune valeur héritée).
**À compléter plus tard (P4)** : si une durée de détention > 1h est un jour spécifiée,
la purge devient max(1h, détention, horizon d'exécution) — règle déjà inscrite dans la config.
Point d'attention certifié par l'audit : la règle d'**alignement** de RET_H (cotation exacte
à t+H vs première cotation ≥ t+H) n'est pas figée dans le registre ; elle devra être
préenregistrée avant toute traduction, car elle change la valeur du label.

## 4. Régimes — proposition de règle de calibration (NON activée)
Constat : méthode fixée (quantiles de volatilité / 3), fenêtre d'apprentissage absente.
**Proposition soumise à validation (pas appliquée, pas devinée) :**
- Fenêtre candidate W = **20 jours de marché glissants** (cohérence avec la décision 6,
  mais choix *distinct* à valider explicitement pour les régimes) ;
- seuils = terciles (33⅓ %, 66⅔ %) de la volatilité réalisée calculée sur W, **recalculés
  une fois par jour de marché et appliqués au jour suivant uniquement** ;
- conséquence sur le début d'échantillon : les 20 premiers jours de marché sont
  **UNCLASSIFIED (NULL)** — perte assumée et documentée, aucune calibration sur le futur ;
- toute recalibration intraday est interdite dans cette proposition (stabilité des classes).
Alternatives à trancher lors de la validation : fenêtre expansive avec plancher de 20 jours,
ou W = 60 jours. REGIME_CLASS reste **bloquée pour le calcul** jusqu'à cette validation.

## 5. Sessions
SUBPERIODE et toute analyse de session : **BLOQUÉES** jusqu'à documentation fiable
(horaires, changements saisonniers, source). Les 10 autres variables n'en dépendent pas
et ne sont pas bloquées par ce point.

## 6. Intégrité des données
- Corpus : partitions natives XAUUSD Bid/Ask du dossier certifié — 348/348 footers lus,
  **685 118 625 lignes, écart 0** vs certificat Phase 2 (`INVENTORY_348.json`, `PROBE_000184.json`).
- Certificats P1/P2 CERTIFIED vérifiés sur octets ; empreintes canoniques figées :
  P1 `9bbeb9a2…2248`, P2 `bb3b63f1…e1f1` (`BASELINE_HASH_MANIFEST.json`).
- Bornes : 2010-01-04 00:01:10.457 UTC → 2026-09-30 23:59:58.864 UTC (certificat P2).
- Aucune donnée synthétique, interpolation, substitution OHLC ou donnée externe dans les
  preuves : les seuls jeux synthétiques utilisés sont des **fixtures de test** (§2),
  jamais présentés comme des preuves. Deux signatures de schéma (001–294 / 295–348)
  documentées dans `QUOTE_DGP_SPEC_V1.md` : normalisation par nom + cast explicite exigés.

## 7. Tests et Git
- Avant audit : 143 tests (code importé). Après réponses structurées : **146**
  (correctif `decisions._match_parameter` + `tests/test_decisions_structured.py`, 3 tests).
  Après audit : **155 verts** (+ `tests/test_numeric_audit.py`, 9 tests). Scan secrets : propre.
- Fichiers modifiés dans cette passe : `metaalpha/decisions.py` (correctif),
  `tests/test_decisions_structured.py`, `tests/test_numeric_audit.py` (nouveaux),
  registres sous `META_ALPHA_WORK/` (réponses HUMAN), rapports sous `reports/meta_alpha/`.
- Commits de référence : import `15f553f`, correctif dépendances `fffd9e4`,
  inventaire `b89085f`/`5ab95ad`, baseline `8b1cec9`, décisions+configuration `c04481d`,
  présent audit (voir journal Git). **Reste à faire :** traductions certifiées variable
  par variable (§1.2), règle d'alignement RET_H, validation de la règle régimes (§4),
  documentation sessions (§5) — aucun de ces points n'est comblé par défaut.

## 8. Plan d'exécution proposé (à autoriser explicitement)
| Niveau | Livrables | PASS | BLOCKED si |
|---|---|---|---|
| L0 Découverte | liste des 348 partitions (IDs Drive) | 348 noms conformes | nommage inattendu |
| L1 Topologie | inventaire footers (déjà produit, à régénérer via `build_inventory`) | total = 685 118 625, signatures documentées | écart de total non expliqué |
| L2 Intégrité | par partition : ordre des timestamps, spread ≥ 0, doublons, quotes invalides | 0 partition illisible, écarts consignés | partition corrompue → arrêt + rapport |
| L3 Dérivation | MID, SPREAD_ABS/REL, RET_TICK recalculés vs colonnes certifiées | écarts numériques = 0 (ou tolérance documentée) | divergence → arrêt |
| L4 Mesure | quantiles, inter-arrivées, gaps, distributions par signature de schéma | mesures produites, aucun label calculé | — |
**Conditions d'arrêt générales :** tout écart avec la baseline figée (hashes, comptes,
bornes) arrête la montée et produit un rapport ; aucun calcul d'anomalie, aucune
exploration de stratégie, aucun franchissement de gate sans autorisation du propriétaire.

**Verdict d'audit : CONFORME SOUS RÉSERVES — prêt pour autorisation L0→L4, avec
4 points ouverts explicitement listés (§1.2, §3.3, §4, §5), aucun comblé par défaut.**
