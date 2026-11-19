"""MOTEUR META-PORTEFEUILLE (Phase 8 sec.5 - ingenierie, 0 essai).
Combine des pattes certifiees/service (F3, F7, edges futurs) sans attendre aucun edge:
- allocation proportionnelle a IR^2 penalisee par la correlation entre pattes;
- borne basse par patte (aucune decision sur estimation ponctuelle);
- Kelly de crise multi-strategies (mixture, pi annuel 5%, pertes correlees en crise);
- CUSUM kill-switch individuel par patte (k=0,5 sigma, h=4 sigma) avec registre;
- interface challenge_sim (flux journalier agrege -> probabilite de passage).
Tests: signaux synthetiques uniquement. python3 ci_tools/meta_portfolio.py
"""
import numpy as np

class Patte:
    def __init__(self, nom, ir_estime, sigma_resid, historique_pnl):
        self.nom = nom; self.ir = float(ir_estime); self.sigma = float(sigma_resid)
        self.pnl = np.asarray(historique_pnl, float)
        self.active = True; self.cusum_p = 0.0; self.cusum_m = 0.0

    def maj_cusum(self, residu):
        """ residu standardise du jour; retourne True si kill-switch declenche."""
        self.cusum_p = max(0.0, self.cusum_p + residu - 0.5)
        self.cusum_m = min(0.0, self.cusum_m + residu + 0.5)
        if self.cusum_p > 4.0 or self.cusum_m < -4.0:
            self.active = False; return True
        return False

def allocations(pattes, corr):
    """Poids ∝ IR^2 / (1 + somme des correlations avec les autres pattes actives), bornes basses:
    une patte dont la borne basse d'IR (IR - 1,28 sigma_IR) est <= 0 recoit un poids nul."""
    n = len(pattes); brut = np.zeros(n)
    for i, p in enumerate(pattes):
        if not p.active: continue
        se_ir = 1.0 / np.sqrt(max(len(p.pnl), 1))
        ir_lb = p.ir - 1.28 * se_ir
        if ir_lb <= 0: continue
        penalite = 1.0 + sum(abs(corr[i, j]) for j in range(n) if j != i and pattes[j].active)
        brut[i] = ir_lb ** 2 / penalite
    tot = brut.sum()
    return brut / tot if tot > 0 else brut

def kelly_crise_portefeuille(poids, esperances, sigmas, horizon_jours=10, pi_annuel=0.05, grille=401):
    """Fraction globale du capital a risque: maximise E[log] sous mixture (normal / crise correlee:
    en crise toutes les pattes perdent simultanement 2x leur sigma). Retourne f dans [0, 1]."""
    actifs = poids > 0
    if not actifs.any(): return 0.0
    mu = float(poids @ esperances); sg = float(np.sqrt((poids ** 2) @ (sigmas ** 2)))
    perte_crise = float(poids @ (2.0 * sigmas))
    pi = 1 - (1 - pi_annuel) ** (horizon_jours / 252.0)
    f = np.linspace(0, 1, grille)
    def elog(ff):
        normal = np.log(np.maximum(1 + ff * mu, 1e-9))
        crise = np.log(np.maximum(1 - ff * perte_crise, 1e-9))
        return (1 - pi) * normal + pi * crise - 0.5 * (ff * sg) ** 2
    return float(f[int(np.argmax(elog(f)))])

def flux_agrege(pattes, poids):
    """Serie journaliere agregee (interface challenge_sim.simuler: entre en %)."""
    L = min(len(p.pnl) for p in pattes)
    M = np.column_stack([p.pnl[:L] for p in pattes])
    return (M @ poids) * 100

if __name__ == '__main__':
    rng = np.random.default_rng(3)
    a = Patte('A', 0.8, 1.0, rng.normal(0.001, 0.01, 300))
    b = Patte('B', 0.4, 1.0, rng.normal(0.0005, 0.01, 300))
    c = Patte('C', 0.05, 1.0, rng.normal(0, 0.01, 300))   # borne basse IR <= 0 -> poids nul attendu
    corr = np.array([[1, 0.2, 0], [0.2, 1, 0], [0, 0, 1.0]])
    w = allocations([a, b, c], corr)
    assert w[2] == 0 and w[0] > w[1] > 0, w
    f = kelly_crise_portefeuille(w, np.array([0.001, 0.0005, 0]), np.array([0.01, 0.01, 0.01]))
    assert 0 <= f <= 1, f
    d = Patte('D', 0.5, 1.0, rng.normal(0, 1, 50))
    declenche = any(d.maj_cusum(x) for x in np.concatenate([np.zeros(10), np.full(30, 1.3)]))
    assert declenche and not d.active
    flux = flux_agrege([a, b], w[:2] / w[:2].sum())
    assert len(flux) == 300
    print(f'meta_portfolio OK: poids={np.round(w,3)} kelly_crise={f:.3f} kill-switch CUSUM declenche, flux agrege {len(flux)} j')
