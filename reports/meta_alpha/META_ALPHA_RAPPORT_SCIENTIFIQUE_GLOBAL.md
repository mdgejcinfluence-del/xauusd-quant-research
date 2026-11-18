# META ALPHA XAUUSD — RAPPORT SCIENTIFIQUE GLOBAL CONSOLIDÉ
### Analyse intégrale des 282 partitions IS certifiées (2010-01-04 → 2020-01-20, 288 086 306 ticks)

*Ordre propriétaire du 2026-11-13. Périmètre IS uniquement — OOS et HOLDOUT jamais ouverts. Budget 0 FCFA. Données = cotations Bid/Ask d'un flux (pas des transactions : aucun volume, carnet ou agresseur n'est mesuré ni supposé). Exécutable : achat Ask / vente Bid. Coûts inconnus (commissions, slippage, latence) jamais remplacés par zéro : toute lecture économique est CONDITIONNELLE.*

**Traçabilité.** Chaîne d'audit `TRIAL_LEDGER_CHAIN.json` (préenregistrement INTEGRAL_SCAN seq 46–47, hash du préenregistrement verrouillé avant calcul). Moteur `ci_tools/integral_scan.py`, exécutions Kaggle : échec `44253130278` conservé (bug de nom de requête, corrigé), succès `44253274284` (282/282, première passe), succès `44254224163` (282/282, passe corrigée `sh_pos`/grille — la première passe reste conservée dans l'historique Git). Artefacts : `integral_scan/INTEGRAL_PARTITION.csv` (282 × 39 métriques), `INTEGRAL_SYNTHESIS.json`, synthèse `ci_tools/synthesize_integral.py`. Deux corrections de mesure documentées : (1) `sh_pos` v1 invalide (moyenne d'un CASE sans ELSE → 1,0 constant), corrigée et recalculée sur 282/282 ; (2) grille du mid seuillée à 1e-9 pour éliminer le bruit binaire flottant. Contrôle d'intégrité : somme des ticks recalculée = 288 086 588 = 288 086 306 + 282 (premier tick de chaque partition), écart nul.

---

## A. Cartographie générale

Dimensions désormais mesurées à couverture 282/282 : mécanique de production des cotations (types de mises à jour), mouvements Bid/Ask/Mid, spread (niveau, distribution, épisodes, dynamique), activité et inter-arrivées, dépendances temporelles et croisées, volatilité (deux échelles, quatre familles de modèles), distributions et extrêmes, cycles UTC/jour/année, granularités, interactions, anomalies contextuelles. Référence temporelle : série mensuelle de 120 mois (`monthly_reference/`) ; aucun agrégat poolé 2010–2020 n'est interprété sans contexte, car le corpus mélange au moins deux processus de cotation.

## B. Fonctionnement des cotations

- **Le mécanisme de production a changé structurellement.** Part des mises à jour bilatérales (Bid et Ask bougent ensemble), médiane annuelle : 98,6 % (2010) → 93,5 % (2011) → 78,1 % (2012) → ~54 % (2013–2014) → 27,8 % (2015) → 28–42 % (2016–2019). Les mises à jour unilatérales (un seul côté) sont **symétriques** : Bid seul ≈ Ask seul dans toutes les ères (0,6 %/0,6 % puis ~30 %/30 %).
- **Aucune cotation croisée ni verrouillée** : part de Bid ≥ Ask = 0,000 sur les 282 partitions et 288 M de ticks. Le flux est propre de ce point de vue.
- **Grille de prix** : plus petit incrément observé = 0,001 $ sur Bid/Ask (0,0005 $ sur le Mid construit, demi-grille mécanique). Les tailles de mouvements des deux côtés sont identiques (ratio médian |ΔBid|/|ΔAsk| = 0,9997 ; bande p10–p90 : 0,990–1,008) et ρ(|ΔBid|,|ΔAsk|) = 1,00 au niveau partition : Bid et Ask sont deux vues d'un même processus, pas deux processus.
- **Symétrie directionnelle** : part des mouvements haussiers parmi les mouvements non nuls = 0,500 dans les trois ères (0,501 / 0,500 / 0,500). Aucun biais directionnel de microstructure.
- **Deux mécanismes de « rendement nul » distincts, à ne jamais confondre** : GD-07 (fin 2012) = republications exactes de la cotation (part mesurée ici, pic ~1,3 % en 2012–2013, partitions GD-07 jusqu'à ~20 %) ; GD-08 (2015–2018) = ajustements compensatoires Bid/Ask à Mid constant (part 1,9–3,5 % en 2016–2018 dans cette passe). Toute statistique tick doit flaguer GD-07.
- **Dépendances croisées sans leader** : corrélation contemporaine ΔBid/ΔAsk 0,35 (ère ancienne) → 0,56–0,60 (ères récentes) ; corrélations décalées d'un événement **strictement symétriques** (0,538 dans les deux sens en ère ancienne — motif « ±1 événement » ; 0,13–0,17 récemment). Aucun côté ne mène l'autre, à aucune époque (confirme et quantifie GLOBAL DISCOVERY).
- **Séries de
...[truncated 8184 chars]