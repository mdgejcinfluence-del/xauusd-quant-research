# FULL REPLAY 2026 — RAPPORT PRINCIPAL (META ALPHA V1 GELÉ)

Moteur importé sans modification (`META_ALPHA_V1_FINGERPRINT.json`), mêmes coûts
(S0 = spread Bid/Ask payé une fois + 1,2 bp CENTRAL), aucune optimisation.
Période réellement rejouée : **2026-01-12 → 2026-09-30** (66 938 889 ticks
Dukascopy certifiés, jamais présentés comme HFM). Réconciliation du segment de
novembre : **exacte** (379 paniers, 898 positions, −0,432 USD = référence seq455).

## C. Backtest — résultats
3 728 paniers clôturés, 8 689 positions. **PnL net S0 : −29,97 USD modèle** ;
profit factor mensuel de 0,23 à 1,20 ; seul juin est positif (+0,825) et il
bascule dès le scénario S1. Mensuel (clôture) : jan −7,90 ; fév −7,93 ; mars
−0,80 ; avr −0,51 ; mai −3,56 ; juin +0,82 ; juil −2,54 ; août −7,56. Paniers
gagnants : 22,6 %. Drawdowns mensuels jusqu'à −9,32 (janvier). Comparaison HFM :
valeurs affichées archivées, statut inchangé
`HFM_DISPLAYED_MONTHLY_METRIC_UNVERIFIED` / `NOT_DIRECTLY_COMPARABLE` — aucun
écart chiffré présenté comme valide.

## D. Diagnostic (détail dans META_ALPHA_FAILURE_ATTRIBUTION_2026.md)
Le modèle échoue d'abord par sa **gestion** : paniers à 3 positions = −30,68 USD
contre +0,71 pour les paniers à 2 positions ; queue de durée jusqu'à ~13,6 jours
sans stop. Ensuite par sa **suractivité** (~17 paniers/jour) qui rend les coûts
décisifs dès S0 (−29,97 → −123,25 en S3). L'avantage économique durable du moteur
gelé est **réfuté sur 8,5 mois** : ce n'était pas un accident de 7 jours.

## E. Fidélité à Colorful drops
Fréquence, durées et structure des paniers restent très éloignées des observations
réelles ; score de fidélité sur ces mois : non mesurable (aucune transaction
réelle observée). Éléments reproduits et manquants : inchangés depuis
COLORFUL-FILTER-002.

## F. GitHub
Branche de session `arena/afe12737-xauusd-quant-research`, rejeu exécuté par le
run CI 46024838552 (résultats committés par le job), tests du présent checkpoint
dans `FULL_REPLAY_TEST_REPORT.md`, manifeste SHA-256 joint.
