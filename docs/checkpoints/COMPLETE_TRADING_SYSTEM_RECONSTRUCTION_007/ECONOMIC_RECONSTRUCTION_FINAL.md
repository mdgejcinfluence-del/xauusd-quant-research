# CTRS-007 — RECONSTRUCTION ÉCONOMIQUE FINALE

Séparation stricte des quatre mondes (jamais mélangés) :

1. **Réel observé** : 5 paniers, +11/+13/−6/+1/+3 ¥ affichés (somme
   +22 ¥, fenêtre de 2 jours) — aucune inférence de rentabilité.
2. **Public affiché** : espérance +6,01 ¥/transaction (AESR-002) —
   UNVERIFIED.
3. **Simulé (moteurs gelés)** : V1 nov. −0,432 (PF 0,906), janv.–sept.
   2026 −29,97 S0 ; V2-F2 nov. −0,930 (PF 0,663).
4. **Contrefactuel** : effet causal du renforcement NOT_IDENTIFIED.

Diagnostic d'échec de nos moteurs (sans ré-optimisation) : la perte se
concentre sur les paniers à 3 positions (janv.–sept. : −30,68 vs
+0,71 pour 2 positions — association, causalité non identifiée), et
notre sortie de premier passage liquide 17–246 s trop tôt par rapport
au comportement réel. L'échec est donc principalement un échec
**d'accumulation + de déclencheur de sortie**, la fidélité d'entrée
(5/5 en-échantillon avec F2) ne produisant aucun avantage économique
(FILTER-002 : fidélité ≠ rentabilité). La rentabilité du système
candidat complet n'est **pas chiffrable honnêtement** : son déclencheur
de sortie n'est pas identifié, tout chiffre exigerait un paramètre
arbitraire. `profitable_edge=False`.
