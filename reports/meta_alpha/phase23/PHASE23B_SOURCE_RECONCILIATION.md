# PHASE 23-B — RECONCILIATION DES SOURCES

- DTWEXBGS via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DTWEXBGS via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DTWEXBGS: AUCUNE SOURCE — serie exclue (SOURCE_RECONCILIATION_FAILED partiel)
- DGS10 via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DGS10 via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DGS10 miroir https://raw.githubusercontent.com/Apress/Statistical-Quantitative-Methods-in-Fin: 2689 obs, 2009-06-01 00:00:00 -> 2020-02-28 00:00:00
- DGS10 miroir https://raw.githubusercontent.com/upathare1/Advanced-Term-Structures/main/Code/d: 1008 obs, 2016-02-18 00:00:00 -> 2020-02-28 00:00:00
- DFII10 via ALFRED alfredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='alfred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DFII10 via FRED fredgraph.csv: ECHEC ReadTimeout HTTPSConnectionPool(host='fred.stlouisfed.org', port=443): Read timed out. (read timeout=45)
- DFII10 via DBnomics miroir FRED: ECHEC ReadTimeout HTTPSConnectionPool(host='api.db.nomics.world', port=443): Read timed out. (read timeout=45)
- DFII10 miroir https://raw.githubusercontent.com/ethanteng/finsight/main/src/datasets/DFII10.cs: 2689 obs, 2009-06-01 00:00:00 -> 2020-02-28 00:00:00
- DFII10 miroir https://raw.githubusercontent.com/js5810/TreasuryAuction/main/data/FRED_data/DFI: 2689 obs, 2009-06-01 00:00:00 -> 2020-02-28 00:00:00
- DFII10 reconciliation deux miroirs: 2689 dates communes, ecart max 0.0
- Series sauvegardees: ['DFII10', 'DGS10'] (vintage: voir source; alfredgraph = vintage ALFRED si obtenu, sinon vintage courante FRED documentee comme limite)
- FOMC parse (communiques officiels): 73 decisions 2010-2019
- CPI/PCE/NFP: dates officielles non enumerables de facon verifiable sans cle API (archives BLS/BEA non indexees par date de publication); familles classees INSUFFICIENT_HISTORICAL_COVERAGE plutot que reconstruites.
- Catalogue: 73 evenements, 73 temoins; types: {'FOMC': 73}