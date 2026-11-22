# PHASE 13-A — PROTOCOLE D'ÉVALUATION DE L'EXPLOITABILITÉ ÉCONOMIQUE DU SIGNAL H1

**Nature : conception, inventaire et préenregistrement documentaires.
Aucun backtest, aucune simulation, aucun calcul de rentabilité ne
sont autorisés ni effectués par la présente mission.**
**Base gelée : modèle H1 confirmé historiquement hors IS
(Phase 12-C.2, `CONFIRMED_HISTORICAL_HOLDOUT` : Brier 0,1798 →
0,1482, log-loss 0,5453 → 0,4850, AUC 0,742, pente de calibration
0,942, n = 1 843). Le holdout 2020–2026 est CONSOMMÉ et
définitivement exclu de toute optimisation ou sélection.**

## 1. Question économique

Le modèle H1 prédit, à `t_reintegration`, une probabilité de
reprise directionnelle. Cette prévisibilité confirmée produit-elle
une **valeur économique positive après spread, commissions,
slippage et contraintes d'exécution réelles** ? Une prédiction
correcte n'est pas un trade gagnant : la présente étude devra
mesurer séparément (i) l'amplitude favorable post-entrée, (ii)
l'amplitude défavorable post-entrée, (iii) le délai de reprise,
(iv) le rendement directionnel réellement réalisable aux prix
exécutables, (v) les coûts, (vi) le risque extrême.

## 2. Modèle et probabilités (gelés)

Modèle H1 exact des Phases 12-B/12-C.1
(`PHASE12C1_MODEL_PARAMETERS.json`, `1bcb3b70…`) : aucun
réentraînement, recalibrage, nouvelle variable ou ajustement.
**Règle d'exposition primaire préenregistrée** : exposition si et
seulement si `p_M1 > M0`, où M0 est la fréquence gelée
**0,7591463414634146**. Ce seuil n'est pas optimisé : c'est la
probabilité de référence du modèle nul, fixée depuis le segment
d'apprentissage 2010–2015 avant toute observation économique ; il
signifie « le modèle juge la reprise plus probable que le taux de
base ». Toute autre règle (exposition systématique sans seuil,
autres seuils, tailles proportionnelles à p) est une **alternative
non préenregistrée**, interdite de sélection après observation
des performances.

## 3. Entrée économique (convention primaire unique)

Instant de décision : `t_reintegration` (clôture de la minute M1
confirmant la première réintégration, définition gelée).

- Événement directionnel +1 : **achat au premier Ask exécutable**
  à partir de `t_reintegration` ;
- Événement directionnel −1 : **vente au premier Bid exécutable**
  à partir de `t_reintegration`.

Opérationnalisation sur les données M1 : prix d'ouverture Ask/Bid
de la première minute M1 commençant à `t_reintegration` (premier
tick de la minute, convention d'agrégation historique). **Délai
maximal : cette première minute.** Si elle est absente (lacune),
si le prix est non fini ou ≤ 0, ou si le spread de la minute est
non fini : **NON_EXÉCUTION**, comptée et publiée, jamais remplacée
par un prix inventé. Aucune tolérance supplémentaire n'est
introduite : la granularité M1 est la justification, et toute
autre tolérance serait une décision à préenregistrer séparément.
Fermetures régulières (nuit, week-end) : l'entrée n'a lieu qu'à la
première minute cotée ; si elle diffère de la minute de
`t_reintegration`, l'événement est NON_EXÉCUTÉ (pas de report
silencieux).

## 4. Sortie économique (convention primaire unique)

La cible prédictive (continuation) n'est **pas** une sortie.
Convention primaire : **sortie à la clôture de la fenêtre
d'observation gelée** — prix Bid de clôture (position longue) ou
Ask de clôture (position courte) de la dernière minute M1 de la
8ᵉ bougie H1 suivant la bougie déclencheuse (fin de fenêtre
répliquée comme en Phase 11-C). Justification : c'est la fenêtre
sur laquelle le phénomène prédit est défini ; elle n'a pas été
choisie sur des résultats économiques. Les positions dont la
fenêtre est censurée sont exclues de la mesure primaire (motif
consigné), jamais prolongées. Alternatives **non
préenregistrées** (à ne jamais sélectionner après coup) : sortie
à la clôture de continuation, sortie sur invalidation (nouvelle
clôture au-delà de P0), horizon plus court — elles exigeraient un
nouveau préenregistrement avant toute donnée nouvelle.

## 5. Rendement et coûts (comptés une seule fois)

Rendement net primaire par événement, en bp log :
`direction × ln(prix_sortie_exécutable / prix_entrée_exécutable) × 10 000`,
avec achat à l'Ask et vente au Bid aux deux extrémités : **le
spread est intégré par les prix eux-mêmes et n'est jamais soustrait
une seconde fois** (à la différence de la convention historique
Phase 10 sur prix Mid, où le coût de référence 4,002 bp = spread
observé médian 2,302 bp + 1,7 bp **hypothétiques** était déduit
une fois ; ces 1,7 bp sont une hypothèse, pas une mesure).

- **Commissions : INCONNUES.** Aucun barème de courtier vérifiable
  n'existe dans les artefacts. Le résultat primaire est donc
  « net de spread, hors commissions », étiqueté comme tel ; aucun
  tarif n'est inventé. Avant toute exécution future, un barème
  documenté devra être consigné ou l'exclusion des commissions
  explicitement assumée comme limite.
- **Slippage : aucun historique d'exécution réel.** Scénarios de
  sensibilité **hypothétiques**, à geler avant exécution (grille
  proposée : 0 / 0,5 / 1,0 bp par transaction, déduits une fois
  par aller-retour selon la convention retenue au gel), jamais
  présentés comme mesurés.
- **Financement** : fenêtre ≤ 8 bougies H1 ; pas de détention
  overnight par construction, sauf traversée de fermeture
  (week-end) déjà traitée par les règles de censure — swaps et
  frais de financement : inconnus, documentés comme tels, non
  modélisés au primaire.

## 6. Mesures de risque (préenregistrées)

Par événement, après entrée : MFE et MAE exécutables (extrema
Bid/Ask orientés), médiane et quantiles (p5, p25, p75, p95) des
rendements nets, perte maximale observée et quantiles de perte
extrême (p1, p5), part de trades positifs, durée d'exposition,
taux de NON_EXÉCUTION, sensibilité aux lacunes ; résultats par
événement **et** pondérés par grappe (les grappes étant l'unité
de dépendance) ; aucun sous-groupe (session, direction, période)
ne peut être sélectionné après observation — seules les
stratifications descriptives listées ici (direction, session de
réintégration, terciles de probabilité prédite aux bornes fixes
0,7591 / 0,85 / 0,92) sont préenregistrées comme descriptives,
jamais comme règles. Une moyenne favorable ne suffit pas : si les
pertes extrêmes (p1, maximum) rendent l'exposition impraticable,
le protocole impose de le conclure.

## 7. Niveaux de preuve et données autorisées

- **Niveau 1 (acquis)** : prévisibilité historique confirmée hors
  IS (12-C.2).
- **Niveau 2 (seul accessible à la prochaine étude)** :
  exploitabilité économique **historique exploratoire** sur l'IS
  2010–2020 — descriptive, jamais une confirmation ; le modèle et
  les règles y sont ceux gelés ici, sans aucun réglage.
- **Niveau 3 (futur)** : confirmation économique indépendante,
  uniquement sur des données **postérieures au gel du présent
  protocole** (collecte prospective à définir, ou autre source
  indépendante autorisée par décision distincte). Le holdout
  2020–2026 ne peut servir à aucun niveau supplémentaire.

## 8. Contrôles de qualité et conditions d'arrêt

Avant toute mesure future : intégrité des prix Bid/Ask (minutes
manquantes, spreads non finis ou aberrants comptés), taux de
NON_EXÉCUTION publié, aucune interpolation de prix, aucune
utilisation du holdout, reproductibilité du pipeline sur les
barres IS déjà commitées. Conditions d'arrêt : taux de
NON_EXÉCUTION > 10 % des événements éligibles, ou part de minutes
à spread non fini > 5 % sur les fenêtres mesurées, ou divergence
de provenance des prix → étude déclarée NON MESURABLE en l'état,
sans adaptation des règles.

## 9. H4

`NON_EVALUABLE_IN_PHASE12B` : aucune recherche économique H4,
aucun pooling, aucun modèle dérivé du H1.

## 10. Verdict de conception

Sources Bid/Ask IS inventoriées, entrée et sortie primaires
uniques définies et justifiées avant tout résultat, règle
d'exposition fixée sans optimisation (p > M0 gelé), coûts
distingués (spread intégré ; commissions inconnues et déclarées ;
slippage en scénarios hypothétiques à geler), risques et
conditions d'arrêt préenregistrés, aucun recours au holdout
requis : **`PROTOCOL_READY_FOR_ECONOMIC_EVALUATION`** — sous les
deux conditions préalables consignées au contrat (barème de
commissions documenté ou exclusion assumée ; grille de slippage
gelée avant exécution). Ce verdict n'autorise ni backtest ni
simulation : l'étude économique (niveau 2, puis éventuellement
niveau 3) exigera des décisions distinctes.
