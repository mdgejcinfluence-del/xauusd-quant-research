# PACK EXOGÈNE — RAPPORT DE CERTIFICATION (ingénierie seule, 0 essai, aucune analyse)

Runs : 44291206652 (collecte initiale) · 44292939940 (annulé après 50 min — FRED injoignable, conservé) · 44300136768 (fallback Yahoo) · 44303765794 (upload corrigé, final).

## Publié et vérifié (noms + tailles, VERIFY_KAGGLE.json)
| Dataset Kaggle (privé) | Rôle | all_ok |
|---|---|---|
| shalom5123/xauusd-exogenous-pack-is | EXPOSÉ (12 fichiers) | **true** |
| shalom5123/xauusd-exogenous-pack-oos | SCELLÉ (11 fichiers, métadonnées seules) | **true** |
| shalom5123/xauusd-exogenous-pack-holdout | SCELLÉ (11 fichiers, métadonnées seules) | **true** |

Audit anti-fuite (§3) : max(available_at_utc) exposé = 2020-01-18 ≤ borne 2020-01-20T09:36:27 → **PASSE**. Découpage OOS (→2023-12-31) / HOLDOUT (>2023) : choix d'ingénierie consigné au manifeste, motivé par aucune analyse. Toute jointure future utilisera `available_at_utc`, jamais `reference_date` (inscrit au MANIFEST).

## Couverture par famille (honnêteté)
| Famille | Contenu livré | Source réelle (bascules consignées) | Limite |
|---|---|---|---|
| F1 dollar | dollar broad (DXY proxy), EURUSD, USDJPY — daily | Yahoo (DX-Y.NYB, EURUSD=X, JPY=X) ; FRED injoignable depuis CI | granularité daily : le M1/tick Dukascopy/HistData n'a pas été collecté (volumes incompatibles avec le CI gratuit) — fallback n°3 de l'instruction, documenté |
| F2 taux & vol | taux 10 ans (^TNX), taux court 3 m proxy (^IRX), VIX (^VIX) — daily | Yahoo, fallback FRED consigné | **DFII10 (taux réel) NON collecté** : FRED seul le publie et FRED bloque les IP CI ; GVZ non collecté (même motif) |
| F3 volume réel | COMEX GC + SI : OHLCV daily 2000→2026 | Yahoo (GC=F/SI=F) ; Stooq inexploitable depuis CI, bascule consignée | daily seulement ; pas d'intraday, pas d'open interest CME gratuit |
| F4 calendrier macro PIT | **NON COLLECTÉ — aucune exposition** | — | les vintages ALFRED exigent une clé API FRED personnelle (absente des secrets CI) ; toute approximation de date de publication violerait la règle anti-révision. Champ vide consigné, zéro imputation |
| F5 positionnement | COT or désagrégé hebdo, 880 semaines 2010→2026 | CFTC (cftc.gov, fichiers annuels officiels) | flux GLD/IAU non collectés (historique shares outstanding non certifiable gratuitement) |
| F6 contexte | SPX (^GSPC), WTI (CL=F) daily | Yahoo, fallback FRED consigné | — |

## Conventions de disponibilité (available_at_utc)
FRED/Yahoo daily : référence + 1 jour 00:00 UTC (conservateur) · futures daily : référence 22:00 UTC (clôture alignée sur le calendrier du flux) · COT : mardi → vendredi 20:30 UTC (après publication 15:30 ET). SHA-256 par fichier dans VERIFY_IS/OOS/HOLDOUT.json ; dictionnaire complet dans MANIFEST.json.

## Incidents consignés
FRED inaccessible depuis les runners GitHub (timeouts répétés, run annulé à 50 min) · Stooq inexploitable depuis CI · écrasement de noms DGS10/DGS2 corrigé (taux_10a / taux_court_3m_proxy) · première publication Kaggle incomplète (3 fichiers du run 1) corrigée par create_version + attente longue. Tous les échecs restent dans l'historique Git et au manifeste.

## Arrêt
STOP, comme ordonné : aucune statistique, aucune corrélation, aucun graphique. Le pack dort jusqu'au préenregistrement d'une hypothèse nouvelle (annexe de l'ordre : structure dollar/taux réels, confirmation par le volume, fenêtres macro horodatées, extrêmes COT), chacune avec budget neuf et gate R3 — sur ordre explicite du propriétaire.
