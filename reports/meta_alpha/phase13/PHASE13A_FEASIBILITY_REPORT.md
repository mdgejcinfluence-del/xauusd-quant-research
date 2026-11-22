# PHASE 13-A — RAPPORT DE FAISABILITÉ ÉCONOMIQUE

**Base : inventaire des seuls artefacts autorisés (IS 2010–2020).
Aucun backtest, aucune simulation, aucun calcul de rentabilité
effectués. Le holdout 2020–2026, consommé, n'a été ni lu ni utilisé.**

## 1. Ce qui est réellement mesurable avec les sources disponibles

- **Prix exécutables Bid/Ask à la minute** : disponibles sur tout
  l'IS (ouvertures et clôtures Bid/Ask par minute M1, issues de
  l'agrégation historique des ticks : premier/dernier tick de la
  minute). L'entrée « premier Ask/Bid à partir de
  `t_reintegration` » et la sortie à la clôture de fenêtre sont
  donc mesurables sans inventer de prix, avec la convention du
  contrat (délai maximal : la première minute ; NON_EXÉCUTION
  sinon).
- **Précision tick** : les partitions tick IS existent sur Kaggle
  privé ; un prix au premier tick exact après `t_reintegration`
  serait mesurable si une étude future le préenregistre — le
  primaire retient la granularité M1, cohérente avec toutes les
  phases antérieures.
- **Spread** : intégré par les prix Bid/Ask eux-mêmes (aucune
  double déduction) ; références observées historiques : médiane
  ≈ 2,30 bp aux événements. Le « 1,7 bp » de la Phase 10 est une
  **hypothèse** de coût additionnel, pas une mesure — utilisable
  seulement comme scénario de sensibilité étiqueté.

## 2. Ce qui n'est pas mesurable en l'état

- **Commissions** : aucun barème vérifiable dans le dépôt. Toute
  étude devra soit documenter un barème réel avant exécution,
  soit publier des résultats explicitement « nets de spread, hors
  commissions ». Inventer un tarif invaliderait la mesure.
- **Slippage réel** : aucun historique d'exécutions. Seuls des
  scénarios hypothétiques (grille proposée 0 / 0,5 / 1,0 bp) sont
  honnêtes, à geler avant de voir des résultats.
- **Exécutabilité en taille / profondeur** : aucune donnée de
  carnet d'ordres ; les cotations ne prouvent pas qu'un volume
  donné serait exécuté au prix affiché. Toute conclusion devra
  rester en rendement par événement, sans affirmation de capacité.
- **Financement/swaps** : inconnus, non modélisés au primaire
  (fenêtre ≤ 8 bougies H1).

## 3. Structure de preuve atteignable

Le protocole distingue trois niveaux et n'en promet que deux :
niveau 2, une étude IS **exploratoire** (le modèle y a été
construit : aucune valeur de confirmation) ; niveau 3, une
confirmation économique uniquement sur des données **postérieures
au gel de 13-A** (collecte prospective à organiser sous décision
distincte). Le holdout consommé ne peut plus servir, pour ce
modèle, à aucun niveau. C'est la contrainte centrale de
faisabilité : la question économique indépendante est
scientifiquement posable, mais sa réponse confirmatoire exigera
du temps de collecte, pas un nouveau calcul sur le passé.

## 4. Risques de conception déjà traités

Seuil d'exposition fixé sans optimisation (p > M0 gelé) ; sortie
primaire unique justifiée par la fenêtre de définition du
phénomène ; variantes reléguées au statut non préenregistré ;
risque extrême (perte maximale, quantiles de perte) préenregistré
au même titre que la moyenne ; règles de NON_EXECUTION et
conditions d'arrêt chiffrées avant exécution ; unités de
dépendance (grappes) conservées.

## 5. Conclusion de faisabilité

Le protocole est définissable intégralement à partir des sources
réelles : **`PROTOCOL_READY_FOR_ECONOMIC_EVALUATION`**, sous deux
conditions préalables consignées au contrat (commissions
documentées ou exclusion assumée ; grille de slippage gelée) et
sous décisions distinctes pour l'étude exploratoire IS (niveau 2)
puis, le cas échéant, la collecte prospective (niveau 3). Aucune
réutilisation du holdout n'est requise ni autorisée. Ce verdict
n'autorise ni backtest, ni simulation, ni stratégie.
