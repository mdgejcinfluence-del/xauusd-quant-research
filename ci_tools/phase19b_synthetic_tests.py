# -*- coding: utf-8 -*-
"""Phase 19-B: tests unitaires SYNTHETIQUES de la fonction de P&L gelee remplir()
(phase17b_engine.py l.130-133). Donnees entierement fictives, aucun marche."""
import sys
sys.path.insert(0, 'ci_tools')
from phase17b_engine import remplir

def cas(nom, direction, pe, ps, s, attendu_approx):
    v = remplir(direction, pe, ps, s)
    ok = abs(v - attendu_approx) < 0.05
    print(f"{'PASS' if ok else 'FAIL'} | {nom}: PL={v:.4f} bp (attendu ~{attendu_approx})")
    return ok

res = []
# Mid inchange a 100, spread 4 bp (bid 99.98 / ask 100.02): ouverture+fermeture = -spread
res.append(cas('LONG sans mouvement Mid, S0', 1, 100.02, 99.98, 0.0, -4.0002))
res.append(cas('SHORT sans mouvement Mid, S0', -1, 99.98, 100.02, 0.0, -4.0002))
# slippage defavorable 1 bp/cote: -spread -2 bp approx
res.append(cas('LONG sans mouvement Mid, S2', 1, 100.02, 99.98, 1.0, -6.0002))
res.append(cas('SHORT sans mouvement Mid, S2', -1, 99.98, 100.02, 1.0, -6.0002))
res.append(cas('LONG sans mouvement Mid, S1', 1, 100.02, 99.98, 0.5, -5.0002))
# mouvement favorable du Mid de +10 bp (long): bid de sortie 100.08, ask entree 100.02
res.append(cas('LONG favorable +10bp Mid, S0', 1, 100.02, 100.08, 0.0, 5.9962))
res.append(cas('LONG defavorable -10bp Mid, S0', 1, 100.02, 99.88, 0.0, -14.0038))
res.append(cas('SHORT favorable -10bp Mid, S0', -1, 99.98, 99.92, 0.0, 5.9962))
# spread variable elargi a la sortie (8 bp): long perd le spread de sortie effectif
res.append(cas('LONG spread sortie elargi, S0', 1, 100.02, 99.96, 0.0, -6.0006))
# conversion bp -> R (definition 17-D): R = PL_bp / (k*ATR/prix*10000)
pl = remplir(1, 100.02, 99.98, 1.0); risque_bp = 1.0 * 0.50 / 100.02 * 10000
print(f"conversion R: PL {pl:.4f} bp / risque {risque_bp:.4f} bp = {pl/risque_bp:.4f} R (attendu ~-0.1200)")
res.append(abs(pl/risque_bp - (-0.12)) < 0.005)
print('TESTS SYNTHETIQUES:', 'TOUS PASS' if all(res) else 'ECHEC', f'({sum(res)}/{len(res)})')
