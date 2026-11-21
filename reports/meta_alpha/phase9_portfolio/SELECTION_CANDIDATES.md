# PHASE 9 — SÉLECTION DES CANDIDATES POUR L'ÉTUDE ÉCONOMIQUE (étapes B–C, préliminaire)

**Principe : la significativité statistique n'est pas une preuve de
rentabilité.** Sont sélectionnées les découvertes dont l'événement est
causalement identifiable au moment de décider, le mécanisme est
compréhensible, la matérialité est crédible devant les coûts, les
avertissements sont examinables et une règle opérationnelle est
formulable. Aucune n'est promue : toutes restent J1 ; les étapes sont
J1 → (M1 mécanisme) → étude économique (E1/E2 seulement après coûts) →
protocole de confirmation indépendante (J2) → stratégie (S1/S2) → P1.

## Candidates retenues pour l'audit économique (dans cet ordre d'étude)

### P9-A — REL-T0 / ANO-C1-001 : retour des dépassements peu profonds
- **Règle esquissée** : à la clôture de la barre de franchissement T0
  d'un niveau Asie/veille, si la profondeur atteinte à T0 est dans le
  tercile bas causal, entrer **contre** le dépassement (retour vers le
  niveau), sortie à la réintégration ou à horizon borné, stop au-delà.
- **Pourquoi elle est prioritaire à évaluer** : seule fiche assortie
  d'une réplication décennale descriptive à variables strictement T0
  (90,6 % de réintégration dans le tercile bas ; protocole de
  confirmation 2.4 déjà rédigé, jamais exécuté, T0 tenu séparé).
- **Blocage attendu (à mesurer, pas à présumer)** : la profondeur
  médiane du tercile bas est de **0,78 bp** et les réintégrations se
  jouent en quelques bp — l'espérance brute par trade risque d'être
  très inférieure au spread observé (~2 bp dès 2010–13, ANO-C2-013).
  L'étude économique devra le chiffrer avant toute fiche stratégie.

### P9-B — ANO-C1-002 : cassure confirmée puis retest
- **Règle esquissée** : après cassure confirmée +5 bp puis retest du
  niveau, entrer **dans le sens** de la cassure (55 % des retests
  encore au-delà à +60 min).
- **Blocage** : les fiches publient des fréquences, pas les magnitudes
  directionnelles conditionnelles au retest ; sans distribution des
  excursions signées, aucune espérance n'est calculable. Étape C devra
  d'abord extraire ces magnitudes (analyse historique de faisabilité
  sur IS, qualifiée comme telle).

### P9-C — ANO-C3-001 (+ taux de base ANO-C1-003) : fade des impulsions M5 de Londres
- **Règle esquissée** : à T0 d'une impulsion IMP-M5 déclenchée en
  session de Londres, entrer **contre** l'impulsion avec objectif de
  retracement complet sous 60 minutes (57,9 % contre 50,7 % en Asie ;
  cohérent dans les trois ères).
- **Blocage** : convertir la fréquence de retracement en espérance
  nette exige la distribution des retracements partiels et des
  excursions adverses (données d'épisodes C3 existantes), et traiter
  les chevauchements d'épisodes (81 % en M5) sans double comptage des
  positions.

### P9-D — ANO-C3-003 : expansion après formation étroite
- **Nature** : effet de **volatilité sans direction** (+13,3 pts de
  sorties par barre >2× le range de formation). Aucune règle
  directionnelle n'en découle ; valeur éventuelle pour le dimensionnement
  ou le timing, pas pour un signal. Conservée au stade mécanisme (M1 à
  documenter), **pas** de fiche stratégie à ce stade.

### P9-E — ANO-C5-003 (secondaire) : retracement après première atteinte de la veille selon l'heure
- Retracement +60 plus faible avant 13:00 (ratio 0,615). Sélectionnée
  **sous réserve expresse** : l'avertissement de composition (heure
  confondue avec session et activité) doit être examiné avant toute
  lecture économique ; si la composition explique l'effet, elle sera
  documentée comme échec et classée.

## Candidates explicitement non retenues (motifs)

- ANO-C2-003/006/008/012 : étiquettes de régime F3 **poolées
  rétrospectives** — toute règle serait non causale ; reconstruction
  causale = chantier séparé non autorisé ici.
- ANO-C2-001/002/004 en l'état : profondeur **finale** (futur) ; seules
  les versions T0 sont éligibles (P9-A ; une version T0 de C2-004
  pourrait être construite à l'étape C si P9-B le justifie).
- ANO-C4-001 : condition connue à la clôture du jour même.
  ANO-C4-002 : tautologie mécanique. ANO-C1-004, C2-014 : timings
  rétrospectifs. ANO-C2-005/009/011, C5-001, C5-002 : dérives d'ère,
  contextes de session ou asymétries sans règle de sens. ANO-C1-005,
  C2-008/010 : volatilité sans direction. ANO-C3-002 : effet de
  2,40 bp non normalisé, sous les seuils. ANOM-001 : artefact mid non
  exécutable, mécanisme réfuté. ANOM-002 : contexte de volatilité.
- Sous-seuil et déclassées (C4-10, C6-02, I-03, FJ-02) : le gel de
  chaque campagne interdit d'en faire des fiches ; elles restent des
  bornes publiées, pas des candidates déguisées.

## Audit des coûts — disponibilité des données (étape B, cadrage)

- **Observés (IS)** : spreads tick Bid/Ask du corpus (ex. ANO-C2-013 :
  médiane post-ouverture de Londres 2,40 bp en 2010–13 → 1,87 bp en
  2017–20). Le corpus IS contient bid/ask tick : les spreads par
  session/ère et autour des événements des candidates sont extractibles
  sans hypothèse. Les prix des barres M1 sont des **mid** : toute
  espérance calculée sur mid devra être re-frappée en
  bid/ask (acheter à l'ask, vendre au bid), **sans double comptage** du
  spread.
- **Non observés (à scénariser, jamais présentés comme réels)** :
  commissions, slippage d'exécution, latence, swaps/financement,
  remplissages partiels, comportement des stops en marché rapide.
  Trois scénarios gelés par candidate : favorable / central /
  défavorable, avec coût maximal supportable et marge après frais.
- **Interdits à ce stade** : backtest `challenge_sim` ou prop firm
  (étape G seulement, après confirmation) ; toute présentation d'un
  résultat mid comme preuve d'exécution.

## Suite du chantier (par étapes, sur ordre)

B (audit coûts chiffré par candidate) → C (mécanismes et magnitudes
manquantes, analyses IS qualifiées de faisabilité) → D (fiches
opérationnelles) → E (espérance nette et stress) → F (protocoles de
confirmation indépendante/prospective ; le holdout reste scellé et
toute confirmation sur IS est exclue par principe) → G (après
confirmation seulement). Si une candidate échoue à une étape, elle est
documentée comme échec et l'on passe à la suivante.
