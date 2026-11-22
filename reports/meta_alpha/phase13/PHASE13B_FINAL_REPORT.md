# PHASE 13-B — ÉVALUATION ÉCONOMIQUE EXPLORATOIRE DU SIGNAL H1 SUR L'IS 2010–2020

**Qualification : NIVEAU 2 — EXPLORATOIRE IS UNIQUEMENT. Cette étude
n'est ni une confirmation économique indépendante, ni une stratégie
validée, ni une autorisation de trading réel. Tous les résultats
portent l'étiquette `NET_OF_SPREAD_BEFORE_COMMISSION_AND_SLIPPAGE`
(commissions exclues par conception, `COMMISSION_EXCLUDED_BY_DESIGN` ;
aucune rentabilité nette complète n'est démontrée ni affirmée).**

**Verdict : `ECONOMICALLY_INCONCLUSIVE_EXPLORATORY_IS`**

## 1. Cadre et préflight

Contrat appliqué sans modification : `PHASE13A1_EXECUTION_CONTRACT_V2.json`
(`86ae5d34…`, gelé seq330, `ECONOMIC_CONTRACT_FROZEN`). Préflight
conforme : chaîne valide jusqu'à seq330, commit `ba8510c`, livrables
13-A/13-A.1 intacts, modèle H1 gelé (`PHASE12C1_MODEL_PARAMETERS.json`,
`1bcb3b70…`), M0 gelé = 0,7591463414634146. Autorisation chaînée
seq331 ; grille de verdict fixée dans le moteur **avant** tout
résultat (cf. §7). Exécution CI : run `45049575517` entièrement
vert (8 lots IS + analyse, exit 0), après deux incidents consignés
au journal (`PHASE13B_LOG.txt` des runs précédents, commits du
dépôt) : fichier ticks vide d'un lot, puis normalisation de fuseau
des horodatages de barres — corrections minimales du moteur,
aucune correction des contrats gelés ni des données. Le holdout
2020–2026 n'a été ni monté, ni listé, ni lu : seules les partitions
IS (filtre historique `IS_END = 2020-01-20`) des datasets Kaggle
privés du propriétaire ont été téléchargées par les lots CI.

## 2. Population (préenregistrée, hors entraînement)

Population primaire : famille **F10-01, timeframe H1**, ensemble
**EVALUATION** de la Phase 12-B (séparation chronologique par
grappe entière : apprentissage 2010–2015, calibration 2016–2017,
évaluation 2018–2020 ; grappes jamais partagées), événements
étiquetés uniquement : **543 candidats**. Ni apprentissage ni
calibration ne sont mélangés aux métriques principales. Directions
issues de `PHASE11C_EVENT_PATHS.csv` (351 longues / 192 courtes
parmi les candidats avant exposition). Probabilités `p_M1` par
application déterministe des coefficients gelés aux features 12-B —
**contrôle de reproduction** : Brier 0,16538954947396367 et
log-loss 0,5468387473824291 recalculés à l'identique des valeurs
publiées en 12-B (`reproduction_conforme: true`). Aucune
réestimation, aucun recalibrage, aucune redétection d'événements,
aucun nouveau clustering, H4 exclu.

## 3. Exécution causale (contrat gelé appliqué tel quel)

- `t_decision` = clôture UTC de la minute M1 de réintégration ;
  exposition si et seulement si `p_M1 > 0,7591463414634146` :
  **443 exposés**, 100 sans exposition (conservés en couverture,
  aucune position artificielle).
- Entrée : premier tick Bid/Ask réel avec
  `t_decision < quote_timestamp < t_decision + 60 s`, extrait des
  partitions tick IS (Ask si long, Bid si court), horodatage exact
  conservé par événement dans `PHASE13B_EVENT_EXECUTIONS.csv` :
  **443 exécutés, 0 NON_EXECUTION** (taux 0/443 = 0,0 % < seuil
  d'arrêt 10 %).
- Sortie primaire unique : clôture de la fenêtre de 8 bougies H1 —
  Bid (long) / Ask (court) de clôture de la dernière minute M1 de
  la fenêtre : **421 clôtures conformes** ; **22 trajectoires
  incomplètes** (minute de sortie absente des barres — fermetures/
  lacunes de cotation), exclues de la mesure primaire avec motif
  consigné, jamais prolongées ni imputées.
- Spreads non finis : 0/842 minutes d'entrée et de sortie des
  événements clôturés (0,0 % < seuil d'arrêt 5 %).
- Spread intégré une seule fois par les prix exécutables ; aucune
  seconde soustraction (ni des 2,30 bp historiques). Slippage :
  seuls les scénarios gelés S0/S1/S2 (0 / 0,5 / 1,0 bp par côté),
  appliqués défavorablement aux deux exécutions.
- Le « rendement brut exécutable » et le « rendement après spread
  intégré » coïncident ici par construction avec S0 : utilisant
  des prix Bid/Ask réels aux deux extrémités, le spread y est déjà
  intégré et n'est pas séparable sans revenir à des prix Mid, ce
  que le contrat interdit.

## 4. Résultats (bp log, nets de spread, avant commissions et slippage sauf scénario)

Par événement (n = 421) :

| Scénario | Moyenne | Médiane | Part positifs | Perte maximale | p5 | p95 |
|---|---|---|---|---|---|---|
| S0 (0 bp) | **+0,11** | −0,89 | 49,4 % | −203,5 | −67,7 | +67,5 |
| S1 (0,5 bp/côté) | **−0,89** | −1,89 | 47,7 % | −204,5 | −68,7 | +66,5 |
| S2 (1,0 bp/côté) | **−1,89** | −2,89 | 47,3 % | −205,5 | −69,7 | +65,5 |

Par grappe (n = 390 grappes, moyenne intra-grappe puis statistique
entre grappes) : moyennes S0 **+0,77**, S1 −0,23, S2 −1,23 bp ;
médianes toutes négatives (−1,01 / −2,01 / −3,01 bp). Détail
complet (quantiles p1–p95, gains extrêmes) : `PHASE13B_RESULTS.json`
et `PHASE13B_RISK_METRICS.csv`.

## 5. Risque

- **Excursions** (prix de liquidation Bid/Ask des barres M1 issues
  des ticks, par événement) : MFE médiane 25,3 bp (p95 94,4 ;
  max 302,2) ; MAE médiane 20,9 bp (p95 84,3 ; max 349,0). Le
  signal déplace bien les prix favorablement après entrée, mais
  l'excursion défavorable est du même ordre — à la sortie fixe de
  fenêtre, l'avantage ne survit pas en médiane.
- **Pertes extrêmes** : perte maximale −203,5 bp (S0), p1 ≈
  −119 bp : la queue gauche est lourde ; une moyenne S0
  marginalement positive (+0,11 bp) ne compense ni la médiane
  négative ni ces pertes extrêmes — conformément au contrat, une
  moyenne positive n'aurait de toute façon pas suffi.
- **Durée d'exposition** : médiane 478 min (≈ la fenêtre de 8 h),
  moyenne 842 min, p95 ≈ 3 415 min : les fenêtres enjambant les
  fermetures régulières (week-ends) prolongent l'exposition
  calendaire, conformément aux définitions gelées ; limite à
  documenter pour toute suite (financement toujours inconnu et
  non modélisé).
- **Concentration** : 421 événements répartis en 390 grappes —
  faible redondance intra-grappe ; la pondération grappe ne change
  pas le diagnostic (moyenne S0 positive mais médianes négatives,
  S1/S2 négatifs).

## 6. Réponse à la question posée

La règle d'exposition préenregistrée (`p_M1 > M0`) **ne conserve
pas de valeur économique positive démontrée** après intégration du
spread : le scénario sans slippage (S0) est en moyenne
par événement quasi nul (+0,11 bp) avec une médiane négative et
moins de la moitié de positions positives ; dès 0,5 bp de slippage
hypothétique par côté (S1), la moyenne devient négative, et S2
l'accentue. Le résultat est donc **fragile aux coûts
supplémentaires** — et il resterait, même sous S0, avant
commissions (inconnues, exclues par conception). La prévisibilité
statistique confirmée en 12-C.2 (niveau 1) ne se convertit pas, sur
l'IS et sous ce contrat d'exécution, en avantage économique
exploitable établi (niveau 2 négatif en tendance, formellement
non conclusif selon la grille préenregistrée).

## 7. Verdict et hiérarchie de la preuve

Conformément à la grille fixée avant résultats (seq331) —
POSITIVE exigeant moyennes événement et grappe **et** médiane
événement positives sous les trois scénarios, NEGATIVE exigeant
moyennes événement et grappe négatives sous les trois scénarios,
conditions d'arrêt respectées (NON_EXECUTION 0 %, spreads non
finis 0 %) :

**`ECONOMICALLY_INCONCLUSIVE_EXPLORATORY_IS`** — S0 ne satisfait
pas le critère positif (médiane −0,89 bp), S1/S2 sont négatifs ;
le critère négatif intégral n'est pas satisfait non plus (S0 moyen
positif). Aucun scénario n'est sélectionné pour conclure ; les
trois sont rapportés.

Ce verdict est de **niveau 2** : exploratoire, sur des données
ayant servi aux recherches antérieures. Il ne constitue ni une
confirmation économique indépendante (niveau 3, non autorisé —
exigerait des données postérieures au gel du contrat, le holdout
étant définitivement exclu), ni une stratégie, ni une autorisation
quelconque d'étape suivante. Toute suite nécessite une décision
distincte du responsable.

## 8. Livrables et traçabilité

- `PHASE13B_EVENT_EXECUTIONS.csv` (`20c5ae22…`) : 543 lignes
  (candidats), horodatages et prix exacts d'entrée/sortie, statuts,
  résultats S0/S1/S2, MFE/MAE, complétude.
- `PHASE13B_RISK_METRICS.csv` (`93334ee1…`) : risque par scénario
  et pondération (événement/grappe).
- `PHASE13B_COVERAGE_AND_EXECUTION.csv` (`eeb908cb…`) : effectifs,
  non-exécutions et motifs à chaque étape.
- `PHASE13B_RESULTS.json` (`e4c26528…`) : résultats numériques,
  dénominateurs explicites des conditions d'arrêt, contrôle de
  reproduction prédictive.
- Journal d'exécution CI conservé : `PHASE13B_LOG.txt`,
  `PHASE13B_ENGINE_EXIT.txt` (0) ; barres P13B et ticks d'entrée
  par lot conservés dans le même répertoire. Moteur
  `ci_tools/phase13b_engine.py`, jobs `lots13b`/`analyse13b` du
  workflow historique `phase10_all.yml`, run `45049575517`.
