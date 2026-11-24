# EUR-EDGE-01 — RAPPORT FINAL : SOCLE DE DONNÉES EUR/USD 2010-2026

Mission exécutée de manière autonome (étapes 1→7 ; l'étape 8, recherche scientifique, est
préparée mais non entamée : elle exige ses propres préenregistrements).

## Ce qui existe maintenant, prouvé

- **COT Euro FX complet** : 853 rapports hebdomadaires CFTC TFF futures-only (code 099741),
  2010-07-20 → 2026-11-17, brut + série nettoyée avec dates de référence (mardi) et de
  disponibilité (vendredi + marge) séparées. Domaine public → dataset Kaggle privé
  `shalom5123/eurusd-cftc-cot` (création vérifiée en CI, journal `KAGGLE_UPLOAD_COT_LOG.txt`).
  Diagnostic notable : l'Euro FX est absent du fichier Disaggregated (marchés physiques) —
  la bonne source est le TFF.
- **Taux officiels** : taux de dépôt BCE téléchargé via l'API SDMX officielle (6 172 lignes) ;
  courbe quotidienne du Trésor US via l'endpoint officiel. FRED est injoignable depuis le
  runner (timeouts) : DEXUSEU et rendements Fed passeront par miroirs vérifiés ou H.15 —
  documenté, non maquillé.
- **Échantillon spot mesuré** : ticks Bid/Ask Dukascopy propres sur les heures testées
  (0 violation, spread médian 0,2–0,3 pip, ≈ 0,7 Go/17 ans estimés) et barres M1→H4 dérivées.

## La contrainte qui commande tout le reste

Les conditions Dukascopy (usage personnel non commercial ; interdiction de constituer une base
de données et de redistribuer sans accord écrit) interdisent l'archive massive et tout dépôt
Kaggle des ticks. Même conclusion pour TrueFX (usage interne) et HistData (personnel/éducatif,
horodatage dégradé). **Le socle spot complet est donc suspendu à un acte du fondateur** : soit
demander l'autorisation écrite à Dukascopy, soit ouvrir un compte démo à son nom (JForex/OANDA)
dont j'ai préparé l'intégration sans inventer d'identifiants. Aucune donnée n'a été contournée.

## Bloqués et documentés

CME 6E détaillé et volatilité implicite/RR25/BF25 : licences payantes, `LICENSE_OR_COST_BLOCKED`,
aucune série fabriquée, aucun proxy présenté comme une IV. Macro par publications (valeur,
parution, révisions) : sources officielles identifiées, construction à venir ; consensus
historique déclaré manquant, jamais reconstruit.

## Organisation temporelle adoptée

Segments descriptifs 2010-2014 / 2015-2018 / 2019-2022 / 2023-2026 ; toute recherche future
déclarera ses dates d'usage, séparera développement/validation/test final, et ne nommera jamais
indépendante une période ayant servi à sélectionner. Les séries révisées seront archivées par
millésime de téléchargement.

## Suite autonome (sans arbitrage, dès la prochaine session)

Compléter les taux US (miroirs), construire le bloc publications macro officielles, préparer la
demande d'autorisation Dukascopy et les connecteurs démo, puis ouvrir le programme scientifique
EUR/USD (direction conditionnelle, barrières TP/SL préenregistrées en unités EUR/USD, coûts
spot réels) uniquement sur les données licites disponibles. Le critère de fin de la mission —
savoir exactement ce qui existe, ce qui est récupéré, ce qui est légal et ce qui manque — est
atteint pour ce premier socle ; il sera révisé à chaque acquisition nouvelle.
