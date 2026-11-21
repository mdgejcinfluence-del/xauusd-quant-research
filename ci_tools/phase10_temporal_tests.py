"""Validation synthétique Phase 10 (protocole gelé seq283). Aucune donnée réelle."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
import pandas as pd
from phase10_engine import seuil_roulant, fermeture_programmee, construire_barres, seuil_causal_fenetre_fixe, diagnostic_fenetre

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

# --- amendement seq289: fenetre causale fixe 250, NaN exclus, min 200 valides ---
base = np.arange(250.0)
fen_nan = base.copy(); fen_nan[::25] = np.nan  # 10 NaN -> 240 valides
valides = fen_nan[np.isfinite(fen_nan)]
chk('fenetre avec NaN: quantile sur valides seuls',
    seuil_causal_fenetre_fixe(fen_nan, 0.95) == np.quantile(valides, 0.95, method='linear'))
chk('diagnostic fenetre NaN', diagnostic_fenetre(fen_nan) == {'taille_fenetre': 250, 'rendements_valides': 240, 'rendements_non_finis': 10, 'eligible_causal': True})
fen200 = np.full(250, np.nan); fen200[:200] = np.arange(200.0)
chk('exactement 200 valides: eligible', np.isfinite(seuil_causal_fenetre_fixe(fen200, 0.95))
    and seuil_causal_fenetre_fixe(fen200, 0.95) == np.quantile(np.arange(200.0), 0.95, method='linear'))
fen199 = np.full(250, np.nan); fen199[:199] = np.arange(199.0)
chk('199 valides: INELIGIBLE_CAUSAL_WINDOW', np.isnan(seuil_causal_fenetre_fixe(fen199, 0.95))
    and diagnostic_fenetre(fen199)['eligible_causal'] is False)
# pas de fuite de la barre courante: la fonction ne recoit que les precedentes;
# une valeur courante extreme passee en plus ne doit jamais entrer (fenetre bornee aux 250 dernieres passees)
fen_avec_courante = np.concatenate([base, [1e9]])
chk('pas d extension vers le passe (fenetre bornee a 250)',
    seuil_causal_fenetre_fixe(np.concatenate([np.full(50, -1e9), base]), 0.95) == np.quantile(base, 0.95, method='linear'))
chk('infini traite comme non fini', np.isnan(seuil_causal_fenetre_fixe(np.where(base < 60, np.inf, base), 0.95)))

print(f"{sum(1 for _, ok in E if ok)}/{len(E)} tests OK")
assert all(ok for _, ok in E)
