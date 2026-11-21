"""Validation synthétique F-I (protocole gelé V1 seq250). Aucune donnée réelle."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
from campaign07_engine import episodes_niveau, distance_bp, est_franchissement, session_de, niveaux

E = []
def chk(nom, cond): E.append((nom, bool(cond))); print(('OK ' if cond else 'ECHEC ') + nom)

chk('distance touche', distance_bp(99.0, 101.0, 100.0) == 0.0)
chk('distance bp', abs(distance_bp(98.0, 99.0, 100.0) - 100.0) < 1e-9)
chk('franchissement strict', est_franchissement(100.1, 100.0, True) and not est_franchissement(100.0, 100.0, True))
chk('sessions', session_de(0) == 'ASIE' and session_de(600) == 'LONDRES' and session_de(1000) == 'NEWYORK' and session_de(1300) == 'NUIT')
lv = niveaux('R10', 1000, 1200); chk('R10 disjoint de 50', all(x % 50 != 0 for x in lv))
lv = niveaux('P50', 1000, 1200); chk('P50 jamais multiple de 10', all(x % 10 == 5 for x in lv))
lv = niveaux('P10', 1000, 1200); chk('P10 jamais multiple de 10', all(x % 10 == 5 for x in lv))

def mk(closes, niveau=100.0, start=0):
    c = np.array(closes, float); o = np.concatenate([[c[0]], c[:-1]])
    h = np.maximum(o, c) + 0.02; l = np.minimum(o, c) - 0.02
    ts = np.arange(start, start + len(c)); day = np.zeros(len(c), dtype=int)
    return ts, day, o, h, l, c

# approche par en dessous puis franchissement strict (cloture au-dela)
closes = [99.90] * 70 + [99.99, 100.05] + [100.10] * 70
ts, day, o, h, l, c = mk(closes)
eps = episodes_niveau(ts, day, o, h, l, c, 100.0, 'G50')
chk('approche + franchissement', len(eps) == 1 and eps[0]['franchissement'] == 1 and eps[0]['terminal'] == 'FRANCHISSEMENT')
chk('maintien (pas de retour)', eps[0]['maintien'] == 1 and eps[0]['suivi_complet'] == 1)
# touche puis rejet (>=25 bp en dessous: niveau 100 -> 99.70 = 30 bp)
closes = [99.90] * 70 + [99.99, 99.98, 99.90, 99.70] + [99.70] * 70
ts, day, o, h, l, c = mk(closes)
eps = episodes_niveau(ts, day, o, h, l, c, 100.0, 'G50')
chk('touche puis rejet', len(eps) == 1 and eps[0]['touche'] == 1 and eps[0]['rejet'] == 1 and eps[0]['terminal'] == 'REJET')
# washout: deux entrees dans la bande a 30 min d'intervalle = un seul episode
closes = [99.90] * 10 + [99.99] + [99.90] * 30 + [99.99] + [99.90] * 100
ts, day, o, h, l, c = mk(closes)
eps = episodes_niveau(ts, day, o, h, l, c, 100.0, 'G50')
chk('washout 60 min un episode', len(eps) == 1)
# retour apres franchissement
closes = [99.90] * 70 + [100.05] + [100.10] * 10 + [99.95] + [99.90] * 70
ts, day, o, h, l, c = mk(closes)
eps = episodes_niveau(ts, day, o, h, l, c, 100.0, 'G50')
chk('retour apres franchissement', eps[0]['franchissement'] == 1 and eps[0]['retour'] == 1 and eps[0]['maintien'] == 0)
print(f"{sum(1 for _, ok in E if ok)}/{len(E)} tests OK")
assert all(ok for _, ok in E)
