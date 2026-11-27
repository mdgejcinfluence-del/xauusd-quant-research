# BACKTEST-COLORFUL-2026-001 — RAPPORT PRINCIPAL

Modèle testé : **V1 gelé** (`colorful_replay.py`, empreinte dans
`MODEL_FINGERPRINT.json`, préenregistrement seq454). Aucun seuil, aucune règle,
aucun coût moteur modifiés. Branche de session imposée (`main` intacte) — écart
documenté par rapport à la branche dédiée demandée. Période demandée : janvier–
novembre 2026. **Statut scientifique : évaluation diagnostique du modèle gelé,
pas une validation indépendante** (période historique connue ; holdout non rouvert,
aucune optimisation faite ni permise à partir de ces résultats).

## A. Couverture — le résultat d'audit qui borne tout le reste
- Corpus certifié (348 partitions) : les 7 partitions 2026 couvrent
  **2026-01-12 → 2026-09-30** (2,44 Go sur Google Drive, fichiers de 330–470 Mo,
  au-delà de la limite de téléchargement du connecteur) — **non accessibles au
  calcul dans cet environnement**. Janvier 1–11 n'y figure même pas.
- Backfill octobre–novembre annoncé : absent localement.
- Ticks réellement exploitables : Dukascopy journaliers **2026-11-20, 22, 23, 24,
  25, 26, 27** (2 868 871 ticks Bid/Ask). Jours partiels : le 20 s'arrête à 19:00,
  le 23 couvre 02:00–21:00, le 27 s'arrête à 10:00 UTC.
- **Mois testables : 0 intégralement ; novembre : PARTIEL (7 jours) ; janvier–
  octobre : NON TESTABLES.** Aucun mois rempli par interpolation.

## B. Performance META ALPHA (novembre partiel, moteur gelé, coûts S0)
379 paniers, 898 positions, 519 renforcements. **PnL net modèle : −0,432 USD**
(tailles moteur, contrat unitaire) ; PnL avant coût variable moteur ≈ +4,06 USD :
**les coûts détruisent l'avantage brut apparent** — espérance par panier −0,0011 USD,
profit factor 0,906, paniers gagnants 26,1 % seulement (le moteur, trop actif,
contrairement au trader réel sélectif). Durée médiane 61 s (plancher moteur),
moyenne 495 s, **maximum 63 820 s (~17,7 h)** : un panier sans stop porté une nuit
entière — la queue de risque est réelle dans le moteur. Drawdown maximal sur
l'equity des paniers : −1,215 USD modèle ; pire panier −0,092 ; meilleur +0,644
(un seul panier exceptionnel, concentration à noter).

Sensibilité (signaux inchangés, surcoût post-hoc étiqueté) : S0 −0,432 ;
S1 (+25 %) −1,555 ; S2 (+50 %) −2,678 ; S3 (+2 bp de slippage hypothétique) −7,915.
**Le modèle est déficitaire dès S0 et s'aggrave linéairement avec les coûts.**

Régimes (7 jours) : pertes concentrées les jours de hausse (23 : −0,194 ;
25 : −0,511), meilleur jour en baisse (24 : +0,381) — échantillon trop petit pour
conclure, aucun ajustement entrepris (`REGIME_ANALYSIS_2026.md`).

## C. Comparaison HFM
Valeurs HFM archivées telles quelles (`HFM_MONTHLY_REFERENCE_2026.csv`) sous le
statut **HFM_DISPLAYED_MONTHLY_METRIC_UNVERIFIED** : la définition exacte
(time-weighted affichée ; compte JPY avec dépôts ¥305 000 / retraits ¥443 160 ;
base solde ou equity inconnue) n'est pas établie par les pièces disponibles.
Comparaison : **NOT_DIRECTLY_COMPARABLE** pour les 11 mois (conventions et
capitaux différents ; notre novembre est de surcroît partiel). Aucun écart
numérique n'est présenté comme un écart de performance valide. Le « YEAR
6 968,86 » et le « 12 420,75 » globaux restent des affichages non transformés.

## D–E. Risque et comportement
Risque : Buy contre-tendance, renforcements jusqu'à 3 positions (plafond moteur),
aucun stop, durée extrême observée ~17,7 h, exposition maximale simultanée du
modèle 0,04 lot (un panier à la fois par construction). Scénarios de capital
normalisés META ALPHA seulement (`CAPITAL_SCENARIOS_2026.csv`) : à 1 000 USD,
rendement novembre-partiel −0,043 %, drawdown −0,12 % — chiffres d'échelle, en
aucun cas une reproduction du compte du fournisseur, dont le capital historique
est inconnu.
Comportement : le score de **fidélité comportementale** reste celui des missions
RE-ENTRY (entrées V2 5/5 en-échantillon, gestion faible, clôtures non reproduites) ;
il est **non mesurable** pour janvier–novembre faute de transactions réelles
observées sur ces mois. Score économique du backtest : négatif après coûts.

## F. Conclusions aux questions imposées
1. META ALPHA (V1 gelé) est-il profitable sur la période testable ? **Non** :
   −0,432 USD modèle sur novembre partiel, dès le scénario de coûts de base.
2. La performance résiste-t-elle aux coûts ? **Non** — le brut (≈ +4,06) est
   entièrement absorbé par spread + coût central ; chaque scénario aggrave.
3. Le risque est-il acceptable ? **Non démontré** : panier porté ~17,7 h sans
   stop, queue non caractérisée sur mois complets.
4. Mois expliquant le résultat : non déterminable (un seul mois partiel).
5. Le moteur se rapproche-t-il du comportement observé ? Sur les décisions
   réelles : partiellement (RE-ENTRY) ; le backtest économique ne prouve rien
   de comportemental — 379 paniers en 7 jours contre la sélectivité réelle
   observée confirme au contraire l'écart de sélectivité.
6. Règles encore inconnues : déclencheurs exacts d'entrée et de clôture, lots,
   plafond d'exposition, queue.
7. Preuves nécessaires : accès calculable aux ticks 2026 complets, définition
   de la métrique HFM, et nouveaux paniers réels prospectifs.

## G. Reproductibilité
`ci_tools/colorful_backtest_2026.py` relance l'intégralité (moteur importé sans
modification) ; empreintes des données et du modèle dans `MODEL_FINGERPRINT.json` ;
tests dans `BACKTEST_REPRODUCIBILITY_REPORT.md`.
