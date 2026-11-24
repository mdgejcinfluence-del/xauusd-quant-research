# PHASE 23-B — RECONCILIATION DES SOURCES

- DTWEXBGS via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DTWEXBGS via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DTWEXBGS: AUCUNE SOURCE — serie exclue (SOURCE_RECONCILIATION_FAILED partiel)
- DGS10 via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DGS10 via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DGS10 via DBnomics miroir FRED: ECHEC ReadTimeout HTTPSConnectionPool(host='api.db.nomics.world', port=443): Read timed out. (read timeout=120)
- DGS10: AUCUNE SOURCE — serie exclue (SOURCE_RECONCILIATION_FAILED partiel)
- DFII10 via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DFII10 via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=120)
- DFII10 via DBnomics miroir FRED: ECHEC ReadTimeout HTTPSConnectionPool(host='api.db.nomics.world', port=443): Read timed out. (read timeout=120)
- DFII10: AUCUNE SOURCE — serie exclue (SOURCE_RECONCILIATION_FAILED partiel)
- FOMC parse (communiques officiels): 0 decisions 2010-2019
- CPI/PCE/NFP: dates officielles non enumerables de facon verifiable sans cle API (archives BLS/BEA non indexees par date de publication); familles classees INSUFFICIENT_HISTORICAL_COVERAGE plutot que reconstruites.
- Catalogue VIDE: etude B non evaluable (SOURCE_RECONCILIATION_FAILED)