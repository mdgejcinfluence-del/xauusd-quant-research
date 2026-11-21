"""Validation synthétique Phase 10 (protocole gelé seq283). Aucune donnée réelle."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
import pandas as pd
from phase10_engine import seuil_roulant, fermeture_programmee, construire_barres

E = []
def chk(nom, cond): E.append((nom, bool(cond))); print(('OK ' if cond else 'ECHEC ') + nom)

# seuil causal: moins de 250 precedentes = amorcage ineligible; courante exclue
chk('amorcage 250', np.isnan(seuil_roulant(np.arange(249.0), 0.95)))
v = np.concatenate([np.arange(250.0), [10**9]])
chk('courante exclue du seuil', seuil_roulant(v[:-1], 0.95) == np.quantile(np.arange(250.0), 0.95, method='linear'))
chk('fenetre glissante 250', seuil_roulant(np.arange(300.0), 0.95) == np.quantile(np.arange(50.0, 300.0), 0.95, method='linear'))

# fermetures programmees: coupure 21h UTC, vendredi soir, week-end
chk('coupure 21h', fermeture_programmee(pd.Timestamp('2020-01-06 21:00')) is True)
chk('vendredi soir', fermeture_programmee(pd.Timestamp('2020-01-03 22:00')) is True)
chk('mardi 14h non', fermeture_programmee(pd.Timestamp('2020-01-07 14:00')) is False)

# construction de barres H1: agregation et validite >=50%
ts = pd.date_range('2020-01-06 00:00', periods=120, freq='min')
bars = pd.DataFrame({'ts': ts, 'bo': 100.0, 'bh': 101.0, 'bl': 99.0, 'bc': 100.5,
                     'ao': 100.1, 'ah': 101.1, 'al': 99.1, 'ac': 100.6,
                     'mo': 100.0, 'mh': 101.0, 'ml': 99.0, 'mc': 100.5, 'sp': 2.0})
tf = construire_barres(bars, 60)
chk('barres H1 construites', len(tf) == 2 and abs(tf.mc.iloc[0] - 100.5) < 1e-9)
bars_courtes = bars.iloc[:20]
chk('barre incomplete rejetee', len(construire_barres(bars_courtes, 60)) == 0)

print(f"{sum(1 for _, ok in E if ok)}/{len(E)} tests OK")
assert all(ok for _, ok in E)
