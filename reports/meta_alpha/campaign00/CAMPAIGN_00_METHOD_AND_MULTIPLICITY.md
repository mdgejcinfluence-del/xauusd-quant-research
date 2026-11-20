# CAMPAGNE 0 — MÉTHODE ET MULTIPLICITÉ

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## 1. Ce qui a été figé avant calcul

Dictionnaire des variables V1–V12, horizons M1/M5/M15/H1, sessions (blocs UTC),
régimes (terciles F3 causaux), ères (2010–13/2014–16/2017–20), règle de suffisance
(n ≥ 1 000 barres et ≥ 100 journées, sinon « NON CONCLUANTE »), et l'interdiction de
produire des combinaisons non listées : gelés dans
`CAMPAIGN_00_VARIABLE_DICTIONARY.md`, sha256 chaîné seq 153, corrigé seq 154
(`974881a7b3d9827c76ef21cb9136f0e2b001eda2b6f48ac262758a28622c4156`), **avant** le
premier run du moteur. Le moteur (`ci_tools/campaign00_engine.py`) implémente ce
dictionnaire et rien d'autre ; sa seule modification en cours de campagne a été
l'ajout des synthèses V6–V10 depuis les séquences déjà accumulées (aucune définition
changée, aucune variable ajoutée après lecture de résultats — les V6–V10 étaient au
dictionnaire gelé et absentes de la première synthèse par incomplétude du code,
consignée au rapport).

## 2. Multiplicité — comment cette campagne évite le data mining

- **Aucun test n'a été effectué** : pas de p-value, pas de seuil de significativité,
  pas de sélection de « meilleure » cellule. La multiplicité des 288 cellules
  publiées est donc une multiplicité de *description*, intégralement publiée (pas de
  tiroir à résultats négatifs) : le fichier CSV contient toutes les cellules
  listées au dictionnaire, y compris les NON CONCLUANTES.
- **Aucune anomalie n'a été sélectionnée pour une quelconque rentabilité** : le
  registre du rapport (§3) consigne six observations descriptives candidates, y
  compris une baseline négative (OBS-C0-04, persistance nulle) qui *borne* les
  prétentions futures au lieu d'en ouvrir.
- **Découverte/confirmation séparées** : si une future campagne de détection (étape
  C du blueprint) formalise des fiches J1, elle devra préenregistrer ses seuils et
  sa correction (BY sur ses comparaisons) et confirmer sur échantillon disjoint ;
  rien dans la Campagne 0 ne vaut confirmation.
- **Dépendances** : les rendements de barres adjacentes et les cellules qui se
  recouvrent (mêmes barres sous plusieurs décompositions) sont dépendants par
  construction ; aucune inférence n'en est tirée ici. Pour les étapes futures,
  l'unité d'indépendance reste la grappe jour×contexte (doctrine seq 148/151).

## 3. Journal de la campagne (positif / négatif / non concluant)

- **Positif (livré)** : distributions globales et décomposées session/régime/ère pour
  V1–V5, V8–V12 sur 4 horizons ; profils chiffrés du rapport §1–2.
- **Négatif (aussi un résultat)** : persistance de signe ≈ 0 à tous les horizons
  (V6) ; retournements ≈ hasard (V7) ; symétrie des excursions (V3≈V4) — trois
  baselines qui ferment descriptivement des familles de prétentions naïves.
- **Non concluant (publié tel quel)** : aucune cellule de distribution n'est tombée
  sous la règle de suffisance (effectifs massifs) ; en revanche V6/V7 portent le
  statut mécanique « NON CONCLUANTE » du fait de leur forme scalaire (n = 1) — limite
  de présentation déclarée, valeurs poolées sur des millions de paires. Familles
  d'épisodes (niveaux, cassures, opens) : non produites, hors périmètre de calcul
  de cette campagne — à préenregistrer pour une Campagne 1.

## 4. Reproductibilité

Moteur versionné `ci_tools/campaign00_engine.py`, workflow
`.github/workflows/campaign00.yml`, runs CI 44710336549 et 44713904881 (succès),
dictionnaire gelé en chaîne. Les budgets expérimentaux n'ont pas bougé (0 essai) ;
les seuls « budgets » consommés sont du temps de calcul CI sur le corpus existant.
