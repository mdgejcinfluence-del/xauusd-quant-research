# EUR-EDGE-01 — AUDIT TICKS SPOT EUR/USD (échantillon technique)

Source testée : flux public Dukascopy `.bi5` EURUSD (fichiers horaires, Bid/Ask, UTC ms,
volumes de cotation). Échantillons mesurés en CI : 6 heures du 2026-11-11 et une heure témoin
du 2015-06-15 (voir `PROBE_QC.json`).

Résultats : aucune violation Bid ≥ Ask, aucun prix non positif, horodatages strictement
croissants, aucun doublon d'horodatage sur les heures complètes ; spread médian 0,2–0,3 pip,
P95 0,4–0,5 pip ; écart inter-tick maximal ≈ 19 s sur l'heure 2015 (marché liquide, mais les
fichiers récents montrent des heures retardées/503 : publication par lots, retries espacés
nécessaires). Taille : ≈ 17 k ticks pour 6 heures échantillon → ordre de 65–70 k ticks/jour,
≈ 0,7 Go Parquet pour 17 ans — le stockage n'est pas contraignant.

**Statut juridique (contraignant)** : conditions Dukascopy = usage personnel non commercial,
interdiction de constituer une base de données et de redistribuer sans accord écrit.
Conséquences appliquées : échantillon limité conservé dans le dépôt de recherche interne ;
**aucune archive massive, aucun transfert Kaggle**. L'acquisition complète exige soit l'accord
écrit de Dukascopy (demande à préparer par le fondateur), soit un canal aux droits compatibles
(compte démo JForex/OANDA du fondateur — connecteurs à préparer, identité non inventée).
Le volume livré avec les ticks est un **volume de cotation**, jamais un volume échangé mondial.
