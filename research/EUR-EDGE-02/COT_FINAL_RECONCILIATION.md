# EUR-EDGE-02 — RÉCONCILIATION FINALE COT EURO FX 099741 (TFF futures-only)

Rapports nettoyés : **{len(K)}**, du {K.report_date.min().date()} au {K.report_date.max().date()}.
Doublons de date de référence : 0.
Semaines du mardi attendues sur la fenêtre : 853 ; semaines absentes : 8 ['2012-12-25', '2013-01-01', '2017-07-04', '2018-12-25', '2019-01-01', '2020-12-22', '2023-07-04', '2025-11-11']
(absences compatibles avec jours fériés fédéraux américains et démarrage TFF mi-2010 ; aucune semaine fabriquée).
Positions : colonnes Long/Short/Spreading conservées dans le brut (88 colonnes) ; nets calculés = Long - Short par catégorie ; % OI = net / open interest.
Contrôles : open interest > 0 partout : True ; nets Leveraged Money dans [-39.9 ; 32.6] % OI.
Dates : `report_date` (mardi, référence) et `available_from` (+4 j, vendredi + marge) séparées et vérifiées monotones.
Dataset Kaggle privé `shalom5123/eurusd-cftc-cot` : création vérifiée en CI EUR-EDGE-01 (journal KAGGLE_UPLOAD_COT_LOG.txt) ; métadonnées : titre, id, licence 'other' + citation CFTC (domaine public US).
Manifeste : SHA-256 des fichiers COT dans EUR_EDGE_01_SHA256_MANIFEST.txt et le présent manifeste EUR-EDGE-02.

Anomalies : aucune justifiant de recommencer le dataset. Limites : futures-only (le combined reste un dataset séparé futur si requis) ; nombre de traders par catégorie présent dans le brut, non repris dans le nettoyé v1.