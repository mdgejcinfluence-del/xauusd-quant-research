# CARRY MAP — paiements structurels des perpetuels (Phase 9, seq127)

Delta-neutre (short perp + long spot). Net = funding annualise moyen - 0,40% (couts declares prudents). Recherche uniquement: aucun compte, aucun capital.

| Patte | Debut | Funding moy %/an | Median %/an | Net %/an | Jours+ % | Serie neg max (j) | Eres 21-22 / 23-24 / 25-26 | Certifiee |
|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-01-01 | 11.63 | 9.77 | 11.23 | 88 | 11 | 17.4 / 9.9 / 4.2 | **OUI** |
| ETHUSDT | 2020-01-01 | 13.71 | 10.76 | 13.31 | 88 | 13 | 19.2 / 10.6 / 3.6 | **OUI** |
| SOXLUSDT | 2026-05-14 | 14.73 | 0.00 | 14.33 | 62 | 5 | nan / nan / 14.7 | non |
| XAUUSDT | 2025-12-11 | 12.61 | 0.00 | 12.21 | 61 | 6 | nan / nan / 12.6 | non |
| ZECUSDT | 2020-02-04 | 11.14 | 10.95 | 10.74 | 87 | 19 | 21.2 / 12.7 / -10.5 | non |
| SOLUSDT | 2020-09-13 | -12.53 | 9.11 | -12.93 | 71 | 28 | -42.7 / 7.5 / -0.1 | non |
| SNDKUSDT | 2026-04-07 | 10.28 | 0.00 | 9.88 | 58 | 2 | nan / nan / 10.3 | non |
| SKHYNIXUSDT | 2026-06-02 | 26.82 | 0.00 | 26.42 | 62 | 4 | nan / nan / 26.8 | non |

Gates: IC95 (journalier) net > 0, BY sur les pattes, stabilite 3/3 tiers, serie negative <= 90 j, profondeur (selection).
Maths de liquidation (declare): a levier L sur la jambe perp, un spike adverse de 100/L % liquide la jambe avant rehedging; marge de survie recommandee: levier <= 3x et collatéral >= 50% du notionnel pour absorber un spike de +/-30% sans liquidation (a verifier par actif avant toute exploitation - hors Phase 9).
Frontiere actions (Hyperliquid qualifie HTTP 200; Binance Vision liste aussi SOXL/SNDK/SKHYNIX parmi les plus profonds): les perpetuels d actions paient comme les crypto, histoire plus courte.