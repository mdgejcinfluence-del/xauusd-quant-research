# EUR-EDGE-02 — RAPPORT DE PROGRESSION (mission ouverte, non clôturée)

## Acquis nouveaux de ce cycle

- **Taux BCE complets** : taux de dépôt quotidien 2010-01-01 → 2026-11-25 via l'API SDMX
  officielle (6 173 observations), déposé avec le Trésor US brut dans le dataset Kaggle privé
  vérifié `shalom5123/eurusd-central-banks`. `US_EU_RATE_DATA_COMPLETE.csv` livre les séries
  BCE nettoyées avec disponibilité. (La clé MRO essayée s'arrête en 2008 — série à re-sourcer ;
  le DFR est le taux directeur opérant depuis 2019, le MRO reste à compléter proprement.)
- **HICP zone euro** : 192 mois Eurostat (2010-01 → 2025-12) acquis via l'API officielle,
  livrés dans `MACRO_RELEASE_VINTAGES.csv` avec la mention explicite que la valeur est celle du
  téléchargement (les premières valeurs d'archive exigent les communiqués Eurostat datés).
- **COT réconcilié** : 853 rapports, 8 semaines de mardi absentes (fériés/démarrage), aucun
  doublon, dataset Kaggle vérifié (`COT_FINAL_RECONCILIATION.md`).
- **Décision prix tranchée et documentée** : aucune voie gratuite ne permet légalement
  (acquérir + stocker + héberger Kaggle) les ticks EUR/USD ; courrier Dukascopy prêt à signer
  par le fondateur ; connecteurs démo spécifiés. L'échantillon interne reste un outil de mesure.
- **Architecture** : schéma canonique indépendant du fournisseur, adaptateurs par source,
  design du moteur payoff-first (TP/SL en pips, coûts complets, découpage chronologique
  développement 2010-2015 / calibration 2016-2018 / validation 2019-2022 / test final réservé
  2023-2026, à confirmer après audit de couverture du spot lorsqu'il sera licite).

## Échecs et blocages précis (aucun maquillage)

- API BLS : répond 200 **sans données** (enregistrement/clé désormais requis) → CPI, NFP,
  chômage US **non acquis**. Voies : clé API BLS gratuite (à créer par le fondateur) ou
  archives publiques BLS à auditer. BEA : clé gratuite également.
- FRED injoignable depuis le runner ; Bundesbank 400 (clé à corriger) ; Fed H.15 renvoie vide ;
  DEXUSEU/rendements US différés aux miroirs vérifiés — **différentiels de taux non encore
  calculés**, faute de jambes complètes des deux côtés.
- CME 6E détaillé et IV/RR25/BF25 : licences payantes, inventaire public documenté, rien constitué.
- Consensus macro historique : inexistant dans nos accès → aucune surprise calculée.

## État du socle

Licite et exploitable dès maintenant : COT hebdomadaire 2010-2026, taux BCE quotidiens,
HICP mensuel. Manquant pour une recherche spot sérieuse : l'archive Bid/Ask (acte fondateur),
les rendements US/DE quotidiens complets, les publications US datées. Le moteur est dessiné,
testable sur l'échantillon interne, et n'attend que des données licites pour ses premières
expériences préenregistrées.

## Suite autonome engagée

Corriger la clé Bund/Bundesbank et l'endpoint Trésor XML ; auditer les archives publiques BLS
(sans clé) ; préparer les demandes de clés gratuites BLS/BEA (formulaires prêts, inscription
fondateur) ; tenir le registre Kaggle à jour ; dès l'ouverture d'une voie prix, lancer l'audit
de couverture spot complet puis le découpage chronologique définitif. EUR-EDGE-02 reste ouvert.
