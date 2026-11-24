# EUR-EDGE-01 — AUDIT COT EURO FX (CFTC 099741)

Source retenue après diagnostic : **Traders in Financial Futures (TFF), futures-only**
(`fut_fin_txt_YYYY.zip`, officiels CFTC). Le fichier Disaggregated ne contient que les marchés
physiques (274 marchés, aucun FX) — l'Euro FX en est absent, fait établi par diagnostic CI, pas
supposé. Le code contrat `CFTC_Contract_Market_Code = 099741` identifie EURO FX (CME).

Acquis : **853 rapports hebdomadaires, 2010-07-20 → 2026-11-17** (le TFF Euro FX commence
mi-2010 dans ces fichiers ; les années pleines donnent 52–53 rapports). Catégories TFF :
Dealer, Asset Manager, Leveraged Money, Other Reportables (long/short/spreading), open interest.
Série nettoyée : `data/CFTC_COT_EUROFX_099741_TFF_clean.parquet` — positions nettes et % de
l'open interest par catégorie (ex. Leveraged Money net : médiane −4,5 % de l'OI, extrêmes
−39,9/+32,6 %).

Causalité : `report_date` = mardi de référence ; `available_from` = mardi + 4 jours (publication
réelle vendredi, marge conservative) ; **toute utilisation avant `available_from` est une fuite**.
Licence : domaine public américain → redistribution autorisée avec citation ; dataset Kaggle
privé créé/vérifié en CI (`shalom5123/eurusd-cftc-cot`, voir `KAGGLE_UPLOAD_COT_LOG.txt`).
Limites : pas de Legacy ni de Futures-and-Options-Combined dans ce lot (le futures-only TFF est
la lecture principale ; les variantes seront des datasets séparés si une hypothèse les réclame).
