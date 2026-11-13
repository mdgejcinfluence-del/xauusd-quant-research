# Rapport de configuration scientifique initiale — META ALPHA (avant tout calcul)

**Réponses enregistrées :** 9/9, attribution `HUMAN` (propriétaire), le 13 novembre 2026,
via `metaalpha.decisions.record_answers`. **Variables instanciées : 11/11**
(`DGP_VARIABLE_REGISTRY_V1.json`, `FORMULA_REGISTRY_V1.json` sous `META_ALPHA_WORK/`).
**Statut : configuration initiale de recherche — pas des paramètres optimaux établis.**

## 1. Les neuf paramètres confirmés
| # | Décision | Valeur du propriétaire |
|---|---|---|
| 1 | D_HORIZONS | 1s, 5s, 30s, 1min, 5min, 15min, 1h |
| 2 | D_FENETRES_VOL | 50, 100, 500, 1000 événements |
| 3 | D_WARMUP_NULL | NULL — lignes conservées, valeurs indisponibles à NULL, aucune suppression pour warm-up |
| 4 | D_SEUIL_SAUT | principal 4 ; sensibilité 3 et 5, résultats comparatifs conservés |
| 5 | D_INTENSITE_T | 1s, 5s, 30s |
| 6 | D_REGIME_SPREAD | 3 classes (faible/normal/élevé), calibration glissante 20 jours de marché, passé uniquement ; fallback 3 classes / 1 semaine documenté |
| 7 | D_TIMEZONE_SESSIONS | UTC + sessions documentées (horaires à documenter, ne pas inventer) |
| 8 | D_METHODE_REGIME | quantiles de volatilité / 3 régimes ; HMM = comparatif ultérieur distinct |
| 9 | D_HORIZON_LABEL | MFE/MAE sur 5min, 15min, 1h ; purge minimale 1h ; chevauchements contrôlés |

## 2. Formules associées (registre, version 1)
- SPREAD_ABS = ask − bid · SPREAD_REL = (ask − bid)/mid · MID = (bid + ask)/2 · RET_TICK (dérivables, F1)
- RET_H = mid[t+H]/mid[t] − 1, H ∈ décision 1 — **fenêtre TEMPS**
- ROLL_STD_MID / ROLL_RANGE_MID : sur N **événements** (décision 2) — fenêtre événements, warm-up NULL
- ZSCORE_ROBUST = (retour − médiane roulante)/MAD roulante, seuil 4 (sensibilité 3, 5 = essais séparés préenregistrés)
- UPDATE_INTENSITY : nombre de cotations sur T secondes · INTERARRIVAL_MEAN : moyenne des écarts sur N événements
- SPREAD_REGIME : quantiles du spread sur le passé uniquement · REGIME_CLASS : quantiles de volatilité, 3 classes
- MFE_H / MAE_H : excursions favorable/adverse maximales sur H ∈ {5min, 15min, 1h}, en tenant compte du Bid/Ask
- Fenêtres temps ≠ fenêtres événements : distinguées ci-dessus et dans le registre, jamais confondues.

## 3. Contrôles anti-lookahead (obligatoires, hérités du code certifié)
- Chaque variable : « disponible à t, calculé avec les données ≤ t » (registre).
- Fenêtres roulantes strictement passées ; aucun `FOLLOWING` ; quantiles de classes
  (spread, régime) appris sur le passé autorisé uniquement, jamais sur le futur.
- Split 60/20/20 par **durée calendaire** (pas par nombre de lignes, jamais aléatoire),
  purge = max(horizon de label 1h, détention, exécution) — la purge minimale 1h du
  propriétaire coïncide avec le plus long label. Chevauchements de labels contrôlés
  (MFE/MAE 1h => embargo d'1h entre segments voisins du label).
- Holdout scellé ; aucune optimisation sur le Holdout ; tous les résultats
  (positifs, négatifs, nuls, non concluants) sont conservés au Trial Ledger.

## 4. Incompatibilités et limites techniques — signalées, pas contournées
1. **Sessions (décision 7)** : les horaires de session ne sont pas encore documentés
   dans le corpus. `SUBPERIODE` est enregistrée mais **aucune analyse de session ne
   démarrera** tant qu'une source documentaire n'a pas fixé horaires et changements
   d'heure — ne pas inventer (consigne du propriétaire elle-même).
2. **REGIME_CLASS — fenêtre d'apprentissage non spécifiée** : la méthode (quantiles/3)
   est fixée, mais la fenêtre passée d'estimation des quantiles ne l'est pas.
   Le paramètre registre correspondant est donc **non opposable en l'état** : la
   variable reste bloquée pour le calcul tant que cette fenêtre n'est pas définie
   (la fenêtre « 20 jours » du propriétaire vise le spread, décision 6 — elle n'est
   pas transposée d'office aux régimes).
3. **Traductions SQL certifiées** : seules MID, SPREAD_ABS, SPREAD_REL, RET_TICK,
   ROLL_STD_MID, ROLL_RANGE_MID disposent d'une traduction certifiée à ce jour ;
   les autres formules devront être traduites et testées une à une, ou resteront
   `FORMULE_NON_CERTIFIEE` (refus d'extraire plutôt qu'extraire faux).
4. **Schéma réel hétérogène** (voir QUOTE_DGP_SPEC_V1) : volumes double (001–294)
   vs uint32 (295–348), ordre des colonnes différent — normalisation explicite par
   nom de colonne et cast documenté, jamais d'hypothèse de schéma unique.
5. **Multiplicité** : 7 horizons × 4 fenêtres × seuils 3/4/5 créent de nombreux
   essais ; chacun sera inscrit au Trial Ledger **avant** exécution, avec baseline
   et contrôle négatif. Les sensibilités ne sont pas du tuning.
6. `bid_volume`/`ask_volume` : sémantique non prouvée — inutilisés comme « volume
   réel » ; les variables F5 enregistrées n'en dépendent pas.

## 5. Verdict
Configuration **cohérente et enregistrée**, prête pour la montée L0→L4 puis les
traductions certifiées de L6, avec deux blocages documentés ci-dessus (sessions,
fenêtre d'apprentissage des régimes) qui n'empêchent pas le reste du programme.
Aucun calcul scientifique n'a été lancé avant ce rapport, conformément à la demande.
