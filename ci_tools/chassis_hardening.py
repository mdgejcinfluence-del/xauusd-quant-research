"""DURCISSEMENTS CHASSIS (F14 sec.4 de l'ordre - ingenierie, 0 essai).
Portage des principes annexe_code_v2.py sans modifier meta_chassis.py (teste, gele):
- CUSUM sur residus d'un modele d'equilibre: k=0,5 sigma, h=4 sigma; alerte => arret
  des nouvelles positions + revue, consignee au registre de regime.
- Kelly a mixture de crise: scenarios correles, pi annuel de crise 5%, horizon du trade.
- Decision sur borne basse: helper generique (aucune decision sur estimation ponctuelle).
- Mediane ponderee par credibilite + winsorisation pour donnees d'entree douteuses.
Auto-test: python3 ci_tools/chassis_hardening.py
"""
import json, pathlib
import numpy as np

REGISTRE = pathlib.Path('reports/meta_alpha/phase6/REGISTRE_REGIME.json')

def cusum_alerte(residus, sigma_ref):
    """CUSUM bilateral k=0,5s, h=4s. Retourne (alerte, indice, cote)."""
    r = np.asarray(residus, float) / sigma_ref
    sp = sm = 0.0
    for i, x in enumerate(r):
        sp = max(0.0, sp + x - 0.5); sm = min(0.0, sm + x + 0.5)
        if sp > 4.0: return True, i, '+'
        if sm < -4.0: return True, i, '-'
    return False, -1, ''

def consigner_alerte(date_iso, source, action):
    reg = json.loads(REGISTRE.read_text()) if REGISTRE.exists() else []
    reg.append({'date': date_iso, 'source': source, 'action': action})
    REGISTRE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRE.write_text(json.dumps(reg, indent=1))
    return len(reg)

def kelly_mixture(p, w, l, horizon_jours, pi_annuel_crise=0.05, perte_crise_mult=2.0, grille=2001):
    """Kelly maximise E[log(1+f*X)] sous mixture: regime normal (p, w, l) et crise
    (probabilite pi sur l'horizon, perte amplifiee, gain annule). f dans [0, 1/l]."""
    pi = 1 - (1 - pi_annuel_crise) ** (horizon_jours / 252.0)
    f = np.linspace(0, 0.999 / l, grille)
    def elog(ff):
        normal = p * np.log(1 + ff * w) + (1 - p) * np.log(1 - ff * l)
        crise = np.log(np.maximum(1 - ff * l * perte_crise_mult, 1e-12))
        return (1 - pi) * normal + pi * crise
    vals = elog(f)
    return float(f[int(np.argmax(vals))])

def borne_basse(estimation, sigma, z=1.28):
    """Aucune decision sur estimation ponctuelle: on decide sur estimation - z*sigma."""
    return estimation - z * sigma

def mediane_credibilite(valeurs, credibilites, winsor_q=0.05):
    """Mediane ponderee par credibilite (lissée par les poids), entrees winsorisees."""
    v = np.asarray(valeurs, float); c = np.asarray(credibilites, float)
    lo, hi = np.quantile(v, winsor_q), np.quantile(v, 1 - winsor_q)
    v = np.clip(v, lo, hi)
    o = np.argsort(v); v, c = v[o], c[o]
    cw = np.cumsum(c) - 0.5 * c
    return float(v[np.searchsorted(cw, 0.5 * c.sum())])

if __name__ == '__main__':
    rng = np.random.default_rng(7)
    ok, idx, cote = cusum_alerte(np.tile([0.3, -0.3], 30), 1.0); assert not ok  # residus bornes sous k: aucune derive
    ok, idx, cote = cusum_alerte(np.concatenate([rng.normal(0, 1, 20), rng.normal(1.2, 1, 30)]), 1.0)
    assert ok and cote == '+', (ok, idx, cote)
    f_mix = kelly_mixture(0.55, 1.5, 1.0, 10); f_simple = kelly_mixture(0.55, 1.5, 1.0, 10, pi_annuel_crise=0.0)
    assert 0 < f_mix < f_simple, (f_mix, f_simple)
    assert borne_basse(0.10, 0.02) < 0.10
    assert abs(mediane_credibilite([1, 2, 100], [1, 1, 0.01]) - 2.0) < 0.6
    print(f'chassis_hardening OK: Kelly simple={f_simple:.3f} vs mixture crise={f_mix:.3f}; CUSUM, borne basse, mediane credibilite testes')
