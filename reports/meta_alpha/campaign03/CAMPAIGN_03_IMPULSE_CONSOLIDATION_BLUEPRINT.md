# CAMPAGNE 3 — IMPULSIONS ET CONSOLIDATIONS : CARTOGRAPHIE CAUSALE (BLUEPRINT)

**PRÉPARATION — DÉFINITIONS À VALIDER AVANT TOUT CALCUL.** Campagne autorisée en
préparation (seq 184). Descriptif seul : aucun backtest, aucun `challenge_sim`,
aucune optimisation, aucune promotion automatique, aucun budget expérimental de
trading, holdout scellé, FRED suspendue, stratégies S12 gelées intactes. Données :
corpus IS déjà consulté (2010–2020) ; le flux prospectif réservé à la
confirmation T0 n'est **jamais** utilisé ici.

## 1. Pourquoi cette campagne

Les campagnes 1–2 ont mesuré impulsions (EV5) et consolidations (EV6) avec des
variables dont une partie résume le futur du chemin (profondeur maximale de
retracement sur 12 barres, range des 60 minutes suivantes) — le même défaut
d'anticipation que la campagne 2.2 a corrigé pour les dépassements et les
cassures. La campagne 3 applique la même reconstruction causale à ces deux
familles : **décrire ce qui est connaissable à chaque instant du développement
d'une impulsion ou d'une consolidation, et seulement ensuite ce qui suit**.

Deux présupposés sont explicitement interdits par l'ordre de mission : qu'une
impulsion « doive » continuer, et qu'une consolidation « doive » déboucher sur
une expansion. Les issues (retracement, extension, sortie) sont des mesures
descriptives, jamais des anticipations.

## 2. Périmètre

- **Impulsions M5** (famille principale IMP) et **M15** (famille secondaire,
  statistiquement séparée) : déclenchement à la clôture d'une barre dont le
  rendement dépasse un seuil causal (quantile roulant sur le passé uniquement,
  dictionnaire §2).
- **Consolidations M1** (famille CONS) : formation par suite de barres calmes
  sous seuil causal, développement et sortie décrits en phases.
- Instantanés de développement : T0 (clôture de la barre de déclenchement /
  de formation), puis +1, +3, +6, +12 barres de la famille. Issues strictement
  postérieures à chaque instantané, horizons 15/30/60 minutes.
- Conditionnements descriptifs préenregistrés : session, ère, régime F3
  (document de méthode) — en nombre fermé, sans découpage exploratoire libre.

## 3. Chaîne de valeur et gates

1. **Gate propriétaire (présente livraison)** : validation du blueprint et du
   dictionnaire des événements (`CAMPAIGN_03_EVENT_DICTIONARY.md`, hash chaîné
   avant calcul).
2. Extraction par la machinerie éprouvée (téléchargement direct Kaggle par
   lots, garde d'intégrité partitions chargées/attendues, commit unique) —
   barres M1/M5/M15 reconstruites depuis le même corpus tick IS.
3. Cartographie descriptive : baselines par famille et contexte, anatomies par
   instantané, comparaisons préenregistrées (méthode et multiplicité gelées).
4. Registre : candidates J1 et résultats négatifs conservés ; aucune fiche
   ANO-C1/C2 modifiée ; les nouvelles observations ne doivent leur existence à
   aucune ressemblance avec les anciennes.

## 4. Livrables attendus à l'exécution (après validation)

`CAMPAIGN_03_CAUSAL_CARTOGRAPHY.md`, `CAMPAIGN_03_EVENT_METRICS.csv`,
`CAMPAIGN_03_SNAPSHOT_STATS.csv`, `CAMPAIGN_03_ANOMALY_REGISTER.csv` (nouvelles
fiches J1 éventuelles + négatifs), `CAMPAIGN_03_DATA_QUALITY.md`. La présente
livraison ne contient que les documents de préparation listés par la décision :
blueprint, dictionnaire, méthode/multiplicité, couverture.
