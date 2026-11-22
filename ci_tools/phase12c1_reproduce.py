"""PHASE 12-C.1 - reconstruction deterministe du modele H1 (ANO-12B-01).
Reutilise TEL QUEL le code gele de la Phase 12-B (import, aucune copie
modifiee): features deja commitees, segment APPRENTISSAGE F10-01,
IRLS historique. Ecrit un JSON de sortie dont le chemin est argv[1]."""
import json, sys
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase12b_engine import logistique_irls, metriques, calibration, SESSIONS_ORDRE

VARIABLES = ['RATIO_REPLI_EXTENSION_A_TREINT', 'DUREE_EXTREME_VERS_TREINT_MIN',
             'MFE_A_TREINT_BP', 'NB_TOUCHES_P0_AVANT_TREINT']
NOMS = VARIABLES + [f'SESSION_REINTEGRATION={s}' for s in SESSIONS_ORDRE[1:]] + ['INTERCEPT']

def matrice(dd):
    cats = [(dd.SESSION_REINTEGRATION == s).astype(float).values.reshape(-1, 1) for s in SESSIONS_ORDRE[1:]]
    return np.hstack([dd[VARIABLES].astype(float).values] + cats)

def main():
    F = pd.read_csv('reports/meta_alpha/phase12/PHASE12B_FEATURES.csv')
    d = F[(F.famille == 'F10-01')]
    app = d[(d.ensemble == 'APPRENTISSAGE') & (d.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1']))]
    ev = d[(d.ensemble == 'EVALUATION') & (d.cible_statut.isin(['RESUMPTION_0', 'RESUMPTION_1']))]
    assert len(app) == 1640 and int(app.RESUMPTION.sum()) == 1245, (len(app), app.RESUMPTION.sum())
    assert len(ev) == 543 and int(ev.RESUMPTION.sum()) == 410
    beta, predire = logistique_irls(matrice(app), app.RESUMPTION.values.astype(float))
    p0 = float(app.RESUMPTION.mean())
    p_m1 = predire(matrice(ev)); p_m0 = np.full(len(ev), p0)
    m0, m1 = metriques(ev.RESUMPTION.values, p_m0), metriques(ev.RESUMPTION.values, p_m1)
    cal = calibration(ev.RESUMPTION.values, p_m1)
    out = {'n_apprentissage': int(len(app)), 'classe1_apprentissage': int(app.RESUMPTION.sum()),
           'M0_probabilite': p0, 'intercept': float(beta[0]),
           'coefficients': {n: float(b) for n, b in zip(NOMS, list(beta[1:]) + [beta[0]])},
           'beta_ordre_matrice': [float(b) for b in beta],
           'noms_colonnes_matrice': ['INTERCEPT'] + NOMS[:-1],
           'predictions_evaluation': [float(p) for p in p_m1],
           'event_id_evaluation': list(ev.event_id),
           'metriques': {'M0': m0, 'M1': m1, 'calibration_M1': cal}}
    json.dump(out, open(sys.argv[1], 'w'), indent=1)
    print(json.dumps({'beta': out['beta_ordre_matrice'], 'M1': m1, 'M0': m0}, indent=1))

if __name__ == '__main__':
    main()
