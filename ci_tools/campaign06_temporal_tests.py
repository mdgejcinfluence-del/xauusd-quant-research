"""Validation synthétique F-G (protocole gelé V1.1+V1.2+V1.2.1+V1.2.2).
Aucune donnée réelle. Vérifie segments, L, Δseg, ER<=1, statuts,
B15 option A, τ, classes, déplacement faible."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
from campaign06_engine import compute_day, classe_forme, halte_candidates

E = []
def chk(nom, cond): E.append((nom, bool(cond))); print(('OK ' if cond else 'ECHEC ') + nom)

# journée continue monotone : L = |Δ|, ER = 1
m = np.arange(100); c = 100 + 0.1 * m
r = compute_day(m, c, c + 0.05, c - 0.05, c, 2)
chk('monotone ER=1', abs(r['ER'] - 1) < 1e-9 and r['n_segments'] == 1)
# aller-retour : Δseg=0, ER=0, L>0
c2 = np.concatenate([100 + 0.1 * np.arange(50), 105 - 0.1 * np.arange(1, 51)])
r = compute_day(m, c2, c2 + 0.05, c2 - 0.05, c2, 2)
chk('aller-retour ER=0', abs(r['ER']) < 1e-9 and r['L_bp'] > 0)
# saut exclu de L : deux segments, saut de +5 entre eux
m3 = np.concatenate([np.arange(50), np.arange(70, 120)])
c3 = np.concatenate([100 + 0.1 * np.arange(50), 110 + 0.1 * np.arange(50)])
r = compute_day(m3, c3, c3 + 0.05, c3 - 0.05, c3, 2)
chk('saut exclu de L (L=98 pas intra)', abs(r['L_bp'] - (98 * 0.1 / 100 * 10000)) < 1 and r['n_segments'] == 2)
chk('ER<=1 malgre saut', r['ER'] <= 1 + 1e-12 and r['D_bp'] > 400)
chk('rho = part observee', abs(r['rho'] - r['D_bp'] / (r['L_bp'] + r['D_bp'])) < 1e-9)
# L=0, D>0 -> INDETERMINEE, rho=1 descriptive, jamais ER
m4 = np.concatenate([np.arange(10), np.arange(30, 40)]); c4 = np.concatenate([np.full(10, 100.0), np.full(10, 101.0)])
r = compute_day(m4, c4, c4, c4, c4, 2)
chk('L=0 D>0 indeterminee rho=1', r['statut_forme'] == 'INDETERMINEE_DISCONTINUITES' and r['rho'] == 1 and np.isnan(r['ER']))
# L=0, D=0 -> PLATE, rho NaN
r = compute_day(np.arange(10), np.full(10, 100.0), np.full(10, 100.0), np.full(10, 100.0), np.full(10, 100.0), 2)
chk('plate rho NaN', r['statut_forme'] == 'PLATE_OBSERVEE' and np.isnan(r['rho']) and np.isnan(r['ER']))
# B15 : fenêtre UTC fixe début 21:00 (1260) durée 60, unique, mercredi
chk('B15 candidat 21h', halte_candidates([(1261, 60)], 2) == [0])
chk('B15 rejet hors fenetre', halte_candidates([(601, 60)], 2) == [])
chk('B15 rejet duree', halte_candidates([(1261, 20)], 2) == [])
chk('B15 rejet samedi', halte_candidates([(1261, 60)], 5) == [])
# classes et déplacement faible prioritaire
chk('classes bornes', classe_forme(10, 0.10) == 'OSCILLANTE' and classe_forme(10, 0.30) == 'DIRECTIONNELLE' and classe_forme(10, 0.2) == 'MIXTE')
chk('deplacement faible prioritaire', classe_forme(4.9, 0.9) == 'DEPLACEMENT_FAIBLE' and classe_forme(5.0, 0.9) == 'DIRECTIONNELLE')
# point médian : chemin uniforme, atteint au milieu
m5 = np.arange(101); c5 = 100 + 0.1 * m5
r = compute_day(m5, c5, c5, c5, c5, 2)
chk('tau milieu', r['tau_min'] == 50)
# trou de session > 15 min -> censurée (hors halte B15)
m6 = np.concatenate([np.arange(200), np.arange(240, 400)]); c6 = 100 + 0.01 * np.arange(len(m6))
r = compute_day(m6, c6, c6 + 0.05, c6 - 0.05, c6, 2)
chk('trou session 39 min censuree', r['statut_forme'] == 'CENSUREE_FORME')
print(f"{sum(1 for _, ok in E if ok)}/{len(E)} tests OK")
assert all(ok for _, ok in E)
