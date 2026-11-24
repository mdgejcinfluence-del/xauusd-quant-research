# MA-EDGE-02 — NOUVELLES HYPOTHÈSES (toutes EXPLORATORY_POST_HOC tant que non préenregistrées)

Point de départ : EXP-07 (données consommées, anatomie des 405 faux positifs sélectionnés).
Les pertes ne sont pas un phénomène unique : la classe dominante est la **dérive après MFE**
(265 événements, −39,0 bp en moyenne) — le prix part d'abord dans le sens favorable, puis saigne
lentement (MAE médiane 46 bp atteinte vers 277 min). L'**échec rapide** (24 événements) est
presque indolore (+2,4 bp). La deadline de 120 min vise exactement cette dérive (le MAE médian
des FP survient à 225 min, après l'échéance).

- **H17 — Trajectoire précoce post-décision** : l'état de la position simulée à +30/+60 min
  (en gain/en perte, MFE/MAE intra-fenêtre) pourrait séparer la dérive de la confirmation.
  *Statut : interdite comme règle tant qu'elle n'est pas préenregistrée ; testable uniquement
  sur le flux prospectif, ou descriptivement (déjà consommé) sans sélection.*
- **H18 — Dérive après MFE comme phénomène propre** : une sortie sur « MFE atteint puis retour
  sous le prix d'entrée » est une *autre* règle que la deadline temporelle ; elle devra son
  propre préenregistrement avant tout examen prospectif ; ne pas la comparer à la deadline sur
  les mêmes événements prospectifs pour choisir la meilleure.
- **H19 — Abstention par coût relatif** : quand le spread courant dépasse un quantile de sa
  propre distribution récente, l'espérance nette se dégrade mécaniquement ; observable en
  prospectif seulement (spread Dukascopy journalisé par événement dans le contrat SHADOW).
- **H20 — Représentation payoff des événements** : remplacer l'unique probabilité de label par
  le triplet (probabilité de confirmation ≤ 120 min, espérance conditionnelle de dérive des
  non-confirmés, MAE précoce) — à construire uniquement si H17/H18 montrent une structure
  prospective ; aucun score composite avant démonstration des composantes.

Priorité (boucle §5) : (1) faire vivre la collecte SHADOW et la règle gelée — seul test
indépendant disponible ; (2) EXP-07 taxonomie approfondie historique si elle peut motiver un
préenregistrement H18 propre ; (3) connecteur MT5 démo préparé, en attente d'identité fondateur.

Prochaine étape déjà engagée : collecte quotidienne automatisée (cron CI), premier bilan
d'événements prospectifs lorsque le compteur d'événements sélectionnés atteindra un seuil de
*description* (25 événements : rapport de fréquence/qualité uniquement, aucune conclusion
économique avant la taille préenregistrée).
