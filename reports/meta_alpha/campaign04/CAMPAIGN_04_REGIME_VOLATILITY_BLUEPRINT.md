# CAMPAGNE 4 — RÉGIMES ET VOLATILITÉ : CARTOGRAPHIE DESCRIPTIVE (BLUEPRINT)

**PRÉPARATION — DÉFINITIONS À VALIDER AVANT TOUT CALCUL.** Campagne autorisée
en préparation (seq 192), dans la priorité « Régimes et volatilité » du plan
de reprise (familles F-A/F-B, seq 183). Descriptif seul : aucun backtest,
aucun `challenge_sim`, aucune optimisation, aucune promotion automatique,
aucun budget expérimental de trading, holdout scellé, flux prospectif T0
interdit à cette campagne, FRED suspendue, 36 cellules S12 intactes, XAU/USD
seul. Le dictionnaire (`CAMPAIGN_04_EVENT_DICTIONARY.md`) sera soumis au
propriétaire ; **son hash sera chaîné avant toute extraction, et aucun
calcul n'aura lieu avant sa validation.**

## 1. Question scientifique centrale

Les propriétés statistiques de XAU/USD changent-elles **progressivement**,
**brusquement**, **par alternance**, ou selon des **transitions
conditionnelles** aux sessions et aux événements structurels internes ?
La campagne quantifie les changements de distribution, de volatilité,
d'asymétrie, de queues et de durée — elle ne présuppose ni que les régimes
sont discrets, ni que F3 les épuise, ni qu'un état quelconque porte une
direction.

## 2. Ce que la campagne distingue rigoureusement (règle d'or)

Quatre objets différents, jamais confondus dans les tableaux :

1. **État fondé sur le passé seul** (connu à l'ouverture du jour) : ce que
   l'on pouvait dire avant que le jour ne se déroule — référence F3 incluse.
2. **État du jour courant** (connu à sa clôture) : construit avec le jour
   écoulé mais des **seuils strictement passés** — jamais de seuil poolé
   rétrospectif présenté comme une détection en temps réel.
3. **Transition confirmée après observation** : une transition n'est dite
   confirmée qu'après la persistance requise ; sa date de confirmation est
   **postérieure** à la date candidate et n'est jamais antidatée.
4. **Conséquence postérieure** : mesurée strictement après la confirmation,
   dans des fenêtres préenregistrées.

## 3. Périmètre

- **Échelle journalière (principale)** : volatilité réalisée quotidienne,
  états causaux BAS/MOYEN/HAUT relatifs aux quantiles des 60 journées
  passées, comparaison systématique à F3 (prédiction HAR gelée seq 75 et ses
  terciles) — y compris les **discordances** F3/état courant, qui sont
  précisément l'endroit où des comportements non capturés par F3 peuvent
  apparaître.
- **Échelle intrajournalière (secondaire, séparée)** : volatilité par
  session (Asie 00–08, Londres 08–13, New York 13–21, nuit 21–24 UTC),
  états par session à seuils causaux propres à chaque session.
- **Dimensions non-F3** (descriptives, sans prétendre à des « régimes »
  discrets) : asymétrie des rendements (skew roulant causal), fréquence
  d'événements extrêmes (queues), volatilité de la volatilité, dispersion
  intrajournalière entre sessions. Ces dimensions décrivent ce que F3, qui
  n'ordonne qu'une échelle d'amplitude journalière, ne contient pas.
- **Développements** : formation (comment un état s'installe : saut ou
  rampe), durée (distributions de runs, censures aux bords publiées),
  alternance (matrice de transition descriptive entre états confirmés),
  retours à l'habituel (temps de retour sous la médiane causale après un
  épisode HAUT), vitesses de transition (rapides vs progressives, définies
  au dictionnaire).
- **Conséquences et interactions** : distributions des rendements (quantiles,
  asymétrie, queues) dans les fenêtres post-confirmation ; fréquence des
  événements structurels internes déjà catalogués (impulsions IMP-M5 de la
  campagne 3, dépassements des campagnes 1–2) selon l'état — conditionnements
  descriptifs, en nombre fermé.
- **Stabilité historique** : toutes les descriptions par ère
  (2010–13 / 2014–16 / 2017–20), publiées même quand elles divergent.

## 4. Chaîne de valeur et gates

1. **Gate propriétaire (présente livraison)** : validation du blueprint et
   du dictionnaire.
2. Gel chaîné du dictionnaire validé + gel des comparaisons fermées
   (≤ 10, proposées dans le document de méthode).
3. Extraction par la machinerie éprouvée (corpus IS seul, garde
   d'intégrité 282 partitions, commit unique, bruts gzip), validation
   temporelle sur données synthétiques avant calcul (patron campagne 3).
4. Cartographie descriptive : baselines par échelle et dimension, anatomies
   de transitions, durées, matrices d'alternance ; registre J1/négatifs au
   catalogue commun, sans promotion et sans transformer un état en signal
   directionnel.

## 5. Livrables attendus à l'exécution (après validation)

`CAMPAIGN_04_REGIME_CARTOGRAPHY.md`, `CAMPAIGN_04_STATE_TIMELINE.csv.gz`
(états quotidiens et par session, seuils causaux et dates de confirmation),
`CAMPAIGN_04_TRANSITION_STATS.csv`, `CAMPAIGN_04_SNAPSHOT_STATS.csv`,
`CAMPAIGN_04_ANOMALY_REGISTER.csv`, `CAMPAIGN_04_DATA_QUALITY.md`. La
présente livraison ne contient que les quatre documents de préparation
exigés, plus la réconciliation du chantier T0 (chantier séparé).
