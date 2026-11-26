# META ALPHA — RAPPORT FINAL DU PORTEFEUILLE (livraison 2026-12-01)

## Conclusion d'ouverture

**Avons-nous trouvé un edge ? Non — pas encore un edge démontré.** Après l'audit complet du
programme et 47 nouvelles règles préenregistrées couvrant le COT, la volatilité implicite, les
taux réels, le momentum, les journées extrêmes, les barrières TP/SL et les sessions, **aucune
stratégie n'a une espérance nette positive et cohérente dans le temps**. Ce que nous livrons est
mieux qu'un faux edge : (1) une cartographie mesurée de ce qui ne fonctionne pas et pourquoi ;
(2) une règle — la deadline de non-réalisation de 120 minutes — préenregistrée avant observation,
dont le mécanisme vise la cause prouvée des pertes, actuellement en test prospectif réel ;
(3) un portefeuille de simulation structuré en budget de risque, avec statuts honnêtes pour
chaque jambe et critères d'arrêt écrits.

Type d'edge recherché et état : directionnel (réfuté sur les signaux testés), informationnel
(COT/GVZ/taux : réels mais instables), comportemental (capteurs insuffisants sans licence),
structurel (COMEX/options : données licenciées), d'exécution/gestion (la piste vivante : gérer
la position ouverte plutôt que mieux prédire l'entrée). Rentabilité nette démontrée : aucune.
Fréquence : les familles testées produiraient 15 à 250 signaux/an — la fréquence n'a jamais été
le problème ; l'espérance l'est. Risque principal : la queue des non-réalisations (−216 bp
historique), que la deadline doit tronquer — c'est précisément ce que l'observation mesurera.

Détail : `GOLD_HYPOTHESIS_ATLAS.csv` (28 hypothèses), `EXPERIMENT_RESULTS.csv` (47 règles ×
3 périodes), `STRATEGY_CANDIDATES.md`, `PORTFOLIO_CONSTRUCTION.md`,
`ROBUSTNESS_AND_OVERFITTING_AUDIT.md`. Tout résultat historique est `EXPLORATORY_POST_HOC` ;
le holdout 2020-2026 reste fermé ; aucun ordre réel n'est autorisé par ce dossier.

## Décision recommandée au fondateur

Présenter à la communauté la machine de recherche, les réfutations documentées et le test
prospectif en cours — avec la promesse exacte que META ALPHA s'est toujours faite : n'annoncer
une rentabilité que le jour où une population indépendante l'aura démontrée. La collecte
prospective (≈ 350 événements attendus) est le seul chemin restant, et il est déjà en marche.
