# PHASE 23-B — ÉTUDE A : CONTEXTE MACRO J-1 (DGS10, DFII10)

Séries FRED obtenues via miroirs GitHub réconciliés (DFII10 : deux miroirs, écart max 0,0 ;
DGS10 : miroir Apress complet 2 689 obs ; vintage courante, limite documentée — ALFRED inaccessible
sans clé depuis l'environnement CI). DTWEXBGS : aucune source complète vérifiable → exclue
(`SOURCE_RECONCILIATION_FAILED` partiel, documenté). Disponibilité causale appliquée : observation
publiée J+1 ouvré 21:15 UTC ; état du jour J = deux dernières observations connues avant 00:00 UTC.

Résultat : **aucune association robuste**. 12 tests préenregistrés (2 séries × 3 horizons ×
rendement signé / amplitude, tercile haut vs bas de la variation J-1, bootstrap semaines ISO
10 000 réplications, BH) : aucun significatif après correction (q minimale 0,094 ; l'effet brut le
plus fort, DFII10 horizon 1 jour sur le rendement signé, vaut −16,3 bp, IC95 [−28,5 ; −4,0] avant
correction — non retenu). Corrélations de rang descriptives ≈ −0,03 à −0,06 : négligeables.
Ni information directionnelle, ni information d'amplitude démontrable dans le contexte taux J-1.

Verdict Étude A : `J1_NO_ROBUST_ASSOCIATION` (DTWEXBGS : `INSUFFICIENT_HISTORICAL_COVERAGE`).
