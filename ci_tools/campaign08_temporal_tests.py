"""Validation synthétique F-J (protocole gelé V2 seq266). Aucune donnée réelle."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
from campaign08_engine import (seuil_causal, est_choc, calculer_r, grouper_episodes,
                               silence_complet, r_h, activite_avant, session_de)

E = []
def chk(nom, cond): E.append((nom, bool(cond))); print(('OK ' if cond else 'ECHEC ') + nom)

# seuil causal: plancher 10 bp et quantile 99.5% lineaire
chk('plancher seuil', seuil_causal(np.full(2000, 0.001)) == 10.0)
v = np.arange(1, 1001, dtype=float)
chk('quantile 99.5 lineaire', abs(seuil_causal(v) - np.quantile(v, 0.995, method='linear')) < 1e-12)
chk('predicat strict', est_choc(10.0, 10.0) is False and est_choc(10.0001, 10.0) is True and est_choc(-11.0, 10.0) is True)

# r uniquement entre barres consecutives (aucun choc fabrique apres un trou)
ts = np.array([0, 1, 2, 10, 11]); c = np.array([100., 101., 102., 200., 201.])
r = calculer_r(ts, c)
chk('r consecutif', np.isfinite(r[1]) and np.isfinite(r[2]) and np.isnan(r[3]) and np.isfinite(r[4]))

# regroupement: ecart 15 inclus, 16 separe
chk('regroupement 15/16', grouper_episodes(np.array([0, 15, 31])) == [(0, 1), (2, 2)])

# cloture: silence integralement observe vs minute manquante
ts2 = np.arange(0, 100); choc2 = np.zeros(100, bool); choc2[10] = True
chk('cloture silence complet', silence_complet(ts2, choc2, 10) is True)
ts3 = np.delete(np.arange(0, 100), 20); choc3 = np.zeros(len(ts3), bool); choc3[10] = True
chk('cloture indeterminee si trou', silence_complet(ts3, choc3, 10) is False)
choc4 = np.zeros(100, bool); choc4[10] = True; choc4[25] = True
chk('pas de cloture si choc a +15', silence_complet(ts2, choc4, 10) is False)

# R60 signee: ancrage cloture derniere barre de choc, orientation par le signe
ts5 = np.arange(0, 200); c5 = np.full(200, 100.0); c5[160] = 101.0
chk('R60 positif', abs(r_h(ts5, c5, 100, 60, +1) - np.log(1.01) * 10000) < 1e-9)
chk('R60 negatif oriente', abs(r_h(ts5, c5, 100, 60, -1) + np.log(1.01) * 10000) < 1e-9)
# fenetre avec trou >15 min: censuree
ts6 = np.concatenate([np.arange(0, 50), np.arange(80, 200)])
c6 = np.full(len(ts6), 100.0)
chk('R60 censure trou', np.isnan(r_h(ts6, c6, 10, 60, +1)))

# activite avant: 60 minutes precedentes, segment complet exige
ts7 = np.arange(0, 200); r7 = np.full(200, 1.0); r7[0] = np.nan
chk('A_avant somme 60', abs(activite_avant(ts7, r7, 100) - 60.0) < 1e-12)
chk('A_avant debut insuffisant', np.isnan(activite_avant(ts7, r7, 30)))

chk('sessions V2', session_de(0) == 'S1' and session_de(500) == 'S2' and session_de(1000) == 'S3' and session_de(1300) == 'S4')

print(f"{sum(1 for _, ok in E if ok)}/{len(E)} tests OK")
assert all(ok for _, ok in E)
