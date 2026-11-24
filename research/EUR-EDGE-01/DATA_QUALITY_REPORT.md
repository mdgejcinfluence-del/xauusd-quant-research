# EUR-EDGE-01 — RAPPORT QUALITÉ (système et premiers contrôles)

Contrôles implémentés (`eur01_engine.py::qc_ticks`, exécutés à chaque échantillon) : bornes
début/fin, nombre de ticks, horodatages nuls/désordonnés/doublons, Bid ≥ Ask, prix ≤ 0, spread
négatif/extrême (quantiles), saut maximal, écart inter-tick maximal, trous (> 1 h signalés),
complétude par heure et par journée (24 fichiers exigés). Résultats des échantillons :
`PROBE_QC.json` (0 violation sur tous les contrôles de prix ; trous = heures non publiées 503,
récupérées par retries espacés). Comparaisons inter-fournisseurs : non encore licites à grande
échelle (les écarts entre courtiers seront documentés, jamais corrigés artificiellement).
Brut immuable, dérivés séparés, manifestes SHA-256 à chaque lot.
