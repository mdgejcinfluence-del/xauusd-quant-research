# PHASE 19-B — TESTS UNITAIRES SYNTHÉTIQUES (données fictives)

Script committé : `ci_tools/phase19b_synthetic_tests.py`, exécuté sur la fonction gelée `remplir()` de `phase17b_engine.py`. **Données entièrement synthétiques — aucune observation de marché.** Résultat : **10/10 PASS**.

Cas couverts (prix fictifs autour de 100, spread fictif de 4 bp) : LONG et SHORT sans mouvement du Mid en S0 → **−4,0000 bp exactement** (perte = spread, ni plus ni moins) ; mêmes cas en S1 → −5,0000 bp et S2 → −6,0000 bp (spread + 2 côtés × slippage) ; mouvements favorables/défavorables du Mid de ±10 bp → ±6,00/−14,01 bp (spread déduit une fois) ; spread de sortie élargi → perte majorée du seul spread réellement traversé ; conversion bp → R selon la définition 17-D → −0,1200 R pour −6 bp et un risque de 49,99 bp.

Ces tests démontrent le comportement comptable de la fonction (spread compté une fois, slippage défavorable une fois par côté, conversions cohérentes) ; ils ne disent rien des conditions réelles de marché.
