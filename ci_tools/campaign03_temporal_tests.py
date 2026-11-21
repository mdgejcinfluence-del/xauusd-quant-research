"""CAMPAGNE 3 - validation temporelle AVANT calcul (donnees synthetiques).
Verifie: seuil 60j excluant la barre courante; fenetre [t-60j, t); effectif
minimal; mediane passee causale; classification par trajectoires mesurees.
Aucune donnee reelle, aucun resultat de campagne."""
import sys
import numpy as np
sys.path.insert(0, 'ci_tools')
from campaign03_engine import causal_quantile_series, causal_past_median, classify_trajectory

J = 24 * 3600 * 10**9
ok = []
# 1) exclusion de la barre courante : une valeur extreme a t ne change pas son propre seuil
ts = np.arange(10) * J
vals = np.array([1., 1, 1, 1, 1, 1, 1, 1, 1, 1000.])
thr, cnt = causal_quantile_series(ts, vals, 60 * J, 0.9, 3)
assert np.isnan(thr[0]) and cnt[0] == 0, 'fenetre vide au depart'
assert thr[9] == 1.0, f"la barre courante extreme doit etre exclue, seuil={thr[9]}"
ok.append('seuil calcule sans la barre courante (extreme courant ignore)')
# 2) borne de fenetre : une valeur vieille de plus de 60 jours sort de la fenetre
ts2 = np.array([0, 61 * J, 62 * J, 63 * J, 64 * J], dtype=np.int64)
vals2 = np.array([500., 1, 1, 1, 1])
thr2, cnt2 = causal_quantile_series(ts2, vals2, 60 * J, 0.9, 3)
assert cnt2[4] == 3 and thr2[4] == 1.0, f"l'ancienne valeur doit etre expiree: cnt={cnt2[4]} thr={thr2[4]}"
ok.append('fenetre glissante [t-60j, t) : expiration des valeurs anciennes')
# 3) minimum d'historique respecte
thr3, _ = causal_quantile_series(ts, vals, 60 * J, 0.9, 2000)
assert np.all(np.isnan(thr3))
ok.append("minimum d'historique (2 000 barres) : aucun seuil sinon")
# 4) mediane passee causale
med, n = causal_past_median(ts, vals, 60 * J, 3)
assert n[9] == 9 and med[9] == 1.0
ok.append('mediane des declenchements passes : passee seule, courante exclue')
# 5) trajectoires : mesures posterieures, classes exclusives du gel
H = np.array([100., 100.8, 101.0, 100.2]); L = np.array([100., 100.5, 100.2, 99.7]); C = H.copy()
cls, t50, t100, t_ext, exc, _ = classify_trajectory(1, 100.0, 100.0, H, L, C, 0, 3)
assert t100 == 3 and cls == 'RETRACEMENT_COMPLET', (cls, t100)
H2 = np.array([100., 101, 102, 103]); L2 = np.array([100., 100.8, 101.5, 102.0])
cls2, *_ = classify_trajectory(1, 100.0, 100.0, H2, L2, C, 0, 3)
assert cls2 == 'CONTINUATION', cls2
ok.append('trajectoires : retracement complet et continuation mesures apres T0, sans classer le declenchement')
# 6) stagnation
H3 = np.array([100., 100.9, 100.8]); L3 = np.array([100., 100.6, 100.65])
cls3, *_ = classify_trajectory(1, 100.0, 100.0, H3, L3, C[:3], 0, 2)
assert cls3 == 'STAGNATION', cls3
ok.append('stagnation : ni 50 % de retracement ni extension a 2A')
print('VALIDATION TEMPORELLE CAMPAGNE 3 : OK')
for o in ok: print(' -', o)
