# PHASE 25-A — RAPPORT FINAL : CARTOGRAPHIE DES NOUVELLES SOURCES

Statut : cartographie documentaire. Aucun entraînement, aucune dépense, aucun téléchargement
massif, holdout fermé, M15_TIME_ONLY et son seuil inchangés.

## Ce qui n'existe pas à budget nul

- Le **volume réel et le carnet du spot XAUUSD** n'existent pas comme série centrale vérifiable
  (marché OTC ; notre corpus ne contient que des cotations Bid/Ask — déjà exploitées en Phase 18) :
  `SOURCE_NOT_VERIFIABLE`.
- Tout ce qui est réellement nouveau en **intraday** — volume/open interest et profondeur COMEX,
  flux agressifs, surfaces d'options (skew, risk reversal), futures inter-marchés — est sous
  licence CME/ICE (dizaines de milliers d'USD annuels par échange) : `LICENSE_OR_COST_BLOCKED`.
  Une API existante n'a jamais suffi à déclarer une source exploitable dans ce programme.
- Les variations quotidiennes de taux/dollar et les fenêtres FOMC sont des **doublons** déjà
  testés et rejetés en Phase 23 ; la surprise macro reste bloquée par le consensus payant.

## Ce qui est nouveau, libre, causal et couvrable

1. **GVZCLS (volatilité implicite des options sur GLD, CBOE via FRED)** — quotidienne depuis
   2008, utilisable en J-1 strict selon la convention causale déjà validée en 23-A/23-B,
   couverture ≈ 100 % des événements M15 en contexte de journée. Information jamais testée :
   une anticipation pricée par le marché, distincte des volatilités réalisées de la Phase 18.
2. **Positionnement COT or (CFTC)** — gratuit, historique long, disponibilité causale documentée
   (positions du mardi publiées le vendredi à 15:30 ET ; seul le dernier rapport *publié* avant
   la décision est admissible, âge 3-10 jours). Information jamais testée : un stock de
   positionnement, pas un flux de prix.

**Verdict global : `PHASE25A_CANDIDATE_INFORMATION_SOURCE_IDENTIFIED`.**

## Proposition de Phase 25-B (soumise à l'arbitrage du fondateur, non autorisée)

- Source retenue (primaire) : GVZCLS ; variable exacte : niveau et variation de la dernière
  clôture GVZ publiée avant la journée de décision (J-1 strict, horodatage de publication
  documenté par événement).
- Mécanisme attendu : en régime d'IV élevée, les réalisations du label coûtent plus cher en
  excursion adverse et les faux positifs perdent davantage ; en IV basse, impulsions plus souvent
  sans suivi (Phase 24-F : gains qui rétrécissent, pertes entières).
- Synchronisation : par date de décision, valeur figée la veille ; aucune valeur du jour même.
- Couverture vérifiable : 2008+ contre événements M15 2010-2019 (≈ 100 %).
- Tests causaux prévus : cartographie par terciles de GVZ J-1 fixés sur 2016-2017 (fréquence de
  réalisation, G, L, MAE, espérance S2 par tercile), relecture post-hoc 2018-2019 sans sélection ;
  aucun modèle entraîné à ce stade.
- Source secondaire documentée : COT (même protocole, contexte hebdomadaire publié).
- Coût réel : **0 FCFA**. Limites : information quotidienne/hebdomadaire, jamais intraday ; elle
  peut expliquer la qualité moyenne des événements, pas leur timing ; tout résultat restera
  exploratoire post-hoc sur des événements déjà consommés.
