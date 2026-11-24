# MA-EDGE-01 — RAPPORT FINAL AU FONDATEUR

## Conclusion directe

**Je n'ai pas trouvé de stratégie rentable, et je peux maintenant dire précisément pourquoi
toutes celles du programme échouent — et ce qu'il faudrait tester différemment.**

1. *As-tu trouvé une stratégie candidate ?* Non. Aucune politique testée en 25 phases, ni aucune
   des six expériences nouvelles de cette mission, ne produit une espérance nette positive.
2. *Pourquoi le programme prédit-il sans gagner ?* Parce qu'il a appris à prédire des
   **événements de trajectoire** (le prix clôturera-t-il au-delà d'un ancien niveau ?), pas des
   **gains**. La Phase 24-E l'a démontré proprement : quand le label se réalise, il se réalise
   tôt (60 minutes en médiane) et il est capturable (+11,36 bp) ; mais 36 % des événements
   sélectionnés ne le réalisent jamais et dérivent à −31,29 bp pièce. L'espérance est détruite
   par les échecs lents, pas par les réussites manquées.
3. *Le phénomène exploitable existe-t-il quelque part ?* Trois mécanismes restent crédibles et
   jamais testés : le contexte de volatilité implicite de la veille (GVZ, gratuit), le
   positionnement spéculatif (COT, gratuit), et une **sortie par deadline de non-réalisation**
   qui tronquerait la dérive des faux positifs. Les deux premiers attendent l'extraction
   autorisée en 25-A ; le troisième exige un préenregistrement et des événements frais.
4. *Qu'est-ce qui est définitivement mort ?* La direction par l'amplitude (toujours
   bidirectionnelle), les seuils de score économiques (non monotones), les sorties au premier
   passage (pas meilleures que la sortie fixe), la saisonnalité horaire, la continuation après
   compression asiatique, la géométrie de premier passage — réfutés dans cette mission ou avant.
5. *Quelle est la limite dure ?* Notre corpus contient des prix et des spreads, jamais des
   transactions. Si l'avantage vit dans le flux d'ordres (COMEX), il est derrière une licence
   d'environ 35 000 USD/an que le budget de 0 FCFA interdit. Je ne peux pas prouver qu'il
   n'existe aucun edge dans les prix seuls ; je peux prouver que 25 phases et 6 expériences
   nouvelles n'en ont trouvé aucun, et que la cible historique du programme était mal posée.

**Verdict : `MA_EDGE_01_PREDICTIVE_INFORMATION_WITHOUT_ECONOMIC_EDGE`** — avec une réorientation
concrète proposée (cible = payoff net, deadline de non-réalisation préenregistrée, contextes
GVZ/COT), détaillée dans `NEXT_RESEARCH_DECISIONS.md`. Aucun résultat de cette mission n'est une
validation indépendante ; tout est `EXPLORATORY_POST_HOC` sur des données consommées.

## Détail des expériences de la mission

Préenregistrées avant calcul (`EXPERIMENT_PREREGISTRATION.md`), consignées dans
`EXPERIMENT_REGISTER.csv` :

- **EXP-01** — le score M15 ne classe le payoff à **aucun** horizon (1 h à 8 h) : en calibration,
  c'est le tercile de score le plus bas qui gagne le plus à 32 barres. La géométrie d'horizon
  n'explique pas l'échec de 24-D.
- **EXP-02** — dérives horaires UTC inférieures à 0,3 bp par barre et de signes instables entre
  décennies : pas de saisonnalité.
- **EXP-03** — continuation après compression asiatique : +5,28 bp (2010-2015) puis −1,83 bp
  (2016-2019) : inversion, rejetée.
- **EXP-04** — premier passage favorable contre adverse sur les événements sélectionnés :
  39,8 % contre 42,6 % à ±20 bp : la trajectoire est symétrique, il n'y a pas d'asymétrie
  géométrique à exploiter par des barrières.
- **EXP-05** — GVZ/COT : faisabilité documentaire confirmée (25-A), extraction non réalisée.
- **EXP-06** — LONG (−2,33) et SHORT (−4,39) perdent tous les deux ; les événements isolés hors
  grappe affichent +1,54 bp en moyenne mais −2,00 en médiane sur 89 événements : fragile,
  explicitement non promu en hypothèse de règle.

## Ce que je recommande

Ne financez plus d'indicateurs de prix supplémentaires. Les trois décisions qui peuvent encore
changer la conclusion sont énumérées dans `NEXT_RESEARCH_DECISIONS.md` : tester les contextes
externes gratuits (GVZ la veille, COT publié), préenregistrer la deadline de non-réalisation
comme première architecture de sortie fondée sur le payoff, et préparer la capture prospective
qui seule pourra un jour valider indépendamment quoi que ce soit. Si ces trois voies échouent à
leur tour, la conclusion scientifique honnête sera que l'information nécessaire n'est pas dans
les cotations — et ce rapport aura au moins établi exactement où se situe la frontière.
