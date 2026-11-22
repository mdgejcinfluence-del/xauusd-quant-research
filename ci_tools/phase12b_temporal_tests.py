"""Tests synthetiques temporels Phase 12-B (a executer AVANT production).
Verifie la borne t_reintegration des cinq variables: aucune minute
poster ieure a la minute de reintegration ne peut influencer les
variables bornees."""
import sys
sys.path.insert(0, 'ci_tools')
import numpy as np
from phase12b_engine import features_bornees

def serie(d=1):
    # minutes 0..9; P0=100; montee puis reintegration a l'indice 5 (cloture < P0)
    mc = np.array([101., 103., 102., 100.5, 99.5, 99., 150., 1., 200., 1.])
    mh = mc + 0.4; ml = mc - 0.4
    mh[1] = 104.; ml[3] = 99.8; ml[4] = 99.2  # touches de P0 avant reintegration (indices 3,4: ml<100)
    if d < 0:
        mc = 200. - mc + 100.; mh, ml = 200. - ml + 100., 200. - mh + 100.
        mc = np.array([99., 97., 98., 99.5, 100.5, 101., 50., 199., 0.5, 199.])
        mh = mc + 0.4; ml = mc - 0.4; ml[1] = 96.; mh[3] = 100.2; mh[4] = 100.8
    ts = np.arange(10) * 1 + 1000
    return mh, ml, mc, ts

def test_borne_aucun_futur():
    mh, ml, mc, ts = serie()
    f1 = features_bornees(1, mh, ml, mc, ts, 100.0, 5)
    mh2, ml2, mc2 = mh.copy(), ml.copy(), mc.copy()
    mh2[6:] = 99999.; ml2[6:] = 0.001; mc2[6:] = 12345.  # futur absurde apres t_reintegration
    f2 = features_bornees(1, mh2, ml2, mc2, ts, 100.0, 5)
    assert f1 == f2, (f1, f2)
    print('PASS borne: le futur ne change aucune variable')

def test_ratio_non_plafonne():
    mh, ml, mc, ts = serie()
    ml[5] = 90.  # repli profond constate a la minute de reintegration
    f = features_bornees(1, mh, ml, mc, ts, 100.0, 5)
    assert f['MFE_A_TREINT_BP'] > 0 and f['RATIO_REPLI_EXTENSION_A_TREINT'] > 1.0, f
    print('PASS ratio > 100 % conserve:', round(f['RATIO_REPLI_EXTENSION_A_TREINT'], 3))

def test_touches_avant_uniquement():
    mh, ml, mc, ts = serie()
    f = features_bornees(1, mh, ml, mc, ts, 100.0, 5)
    assert f['NB_TOUCHES_P0_AVANT_TREINT'] == 2, f
    print('PASS touches avant reintegration = 2 (futur ignore)')

def test_duree_et_mfe():
    mh, ml, mc, ts = serie()
    f = features_bornees(1, mh, ml, mc, ts, 100.0, 5)
    assert f['DUREE_EXTREME_VERS_TREINT_MIN'] == 4, f  # sommet minute 1 -> reintegration minute 5
    assert abs(f['MFE_A_TREINT_BP'] - 10000 * np.log(104. / 100.)) < 1e-9, f
    print('PASS duree extreme->reintegration et MFE borne')

def test_sens_negatif():
    mh, ml, mc, ts = serie(d=-1)
    f = features_bornees(-1, mh, ml, mc, ts, 100.0, 5)
    assert f['MFE_A_TREINT_BP'] > 0 and f['NB_TOUCHES_P0_AVANT_TREINT'] == 2, f
    print('PASS sens -1 symetrique')

if __name__ == '__main__':
    test_borne_aucun_futur(); test_ratio_non_plafonne(); test_touches_avant_uniquement()
    test_duree_et_mfe(); test_sens_negatif()
    print('PHASE12B TESTS SYNTHETIQUES: 5/5 PASS')
