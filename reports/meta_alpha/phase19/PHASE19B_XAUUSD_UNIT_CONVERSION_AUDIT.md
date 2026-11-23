# PHASE 19-B — AUDIT DES UNITÉS ET CONVERSIONS XAUUSD

## Chaîne de conversion effectivement utilisée (tracée dans le code)
1. Prix en dollars par once (cotations à trois décimales observées dans les artefacts, ex. 1144,298) ; variations de barrières en dollars (`direction*(liq−entrée)` comparé à `k × ATR14_H1`, ATR lui-même en dollars — `phase17b_engine.py` l.174-176).
2. P&L en **basis points de prix** par log-rendement : `direction * log(ps/pe) * 10000` (l.133). Pour les amplitudes concernées (≤ ~200 bp), l'écart log/arithmétique reste ≤ ~2 % relatif de la valeur et est appliqué uniformément à tous les résultats historiques.
3. Distance de risque en bp (17-D/17-E) : `k × ATR14_H1 / prix_entrée × 10000` (bp arithmétique), puis `R = PL_bp / risque_bp`. Mélange documenté : numérateur en bp logarithmiques, dénominateur en bp arithmétiques — approximation cohérente et gelée par la définition 17-D, sans effet de signe ni d'ordre de grandeur aux amplitudes historiques, mais à connaître avant toute interprétation fine de R.
4. ATR14_H1 : reconstruction Wilder depuis les barres M1 Mid committées (moteur 17-B), en dollars, cohérent avec les barrières.

## Ce qui n'existe pas : la spécification du broker
Aucun artefact du programme ne documente de broker, de type de compte, de taille de tick, de « point » ou de « pip », de taille de contrat (onces par lot) ni de valeur monétaire par mouvement. Les recherches par mots-clés sur les protocoles 13-A/13-A.1, le contrat de coûts 17-A et les moteurs ne retournent **aucune spécification de contrat** ; le protocole 13-A déclare au contraire les commissions « INCONNUES, aucun barème vérifiable ». Le programme n'a donc jamais converti de résultat en devise par lot, et aucun « pip » universel n'a été supposé : tous les résultats sont en bp de prix et en multiples R, unités auto-suffisantes qui ne dépendent d'aucune convention de broker.

## Verdict d'unités
Conversions prix → bp → R : cohérentes et traçables de bout en bout dans le code. Spécification du broker et du contrat : **non documentée** → `BROKER_SPECIFICATION_UNVERIFIED` pour tout ce qui exigerait une conversion monétaire par lot (valeur du point, marge, commission par lot), laquelle n'a jamais été utilisée dans les résultats.
