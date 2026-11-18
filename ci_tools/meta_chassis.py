"""CHASSIS PERMANENT META ALPHA (instruction v3.0 sec.5.1-5.2) - agnostique au moteur directionnel.
Formules gelees: taille_i = w_i * (sigma_cible/sigma_hat_i) * g_spread * g_vol * g_tod;
g_spread=1 si spread_prevu<=tau_strate sinon 0; g_vol: 1 (q<=0.8), 0.5 (<=0.9), 0 sinon;
Kelly plafonne w_i <= 0.25*f_i; gouverneur DD: -3% -> x0.5, -5% -> flat; kill-switch journalier -2%.
Aucune valeur broker/challenge codee en dur: tout vient de OWNER_CONFIG_V1.json."""
import json, pathlib

def load_config(path='reports/meta_alpha/phase2/OWNER_CONFIG_V1.json'):
    return json.loads(pathlib.Path(path).read_text())

def g_spread(spread_prevu, tau_strate): return 1.0 if spread_prevu <= tau_strate else 0.0
def g_vol(vol_q): return 1.0 if vol_q <= 0.8 else (0.5 if vol_q <= 0.9 else 0.0)
def kelly_capped(mu, sigma2, w_max=1.0): return min(0.25 * mu / sigma2, w_max) if sigma2 > 0 else 0.0

def taille(w_i, sigma_cible, sigma_hat, spread_prevu, tau, vol_q, g_tod=1.0):
    if sigma_hat <= 0: return 0.0
    return w_i * (sigma_cible / sigma_hat) * g_spread(spread_prevu, tau) * g_vol(vol_q) * g_tod

class Gouverneur:
    """Etat journalier/cumule du portefeuille (regles sec.5.2, parametrables)."""
    def __init__(self, seuil_reduction=-0.03, seuil_flat=-0.05, kill_switch_jour=-0.02):
        self.sr, self.sf, self.ks = seuil_reduction, seuil_flat, kill_switch_jour
        self.dd_cumule = 0.0; self.perte_jour = 0.0; self.flat = False; self.bloque_jour = False
    def nouvel_jour(self): self.perte_jour = 0.0; self.bloque_jour = False
    def enregistrer(self, pnl_pct, fin_de_journee=False):
        self.perte_jour += pnl_pct; self.dd_cumule = min(0.0, self.dd_cumule + pnl_pct) if pnl_pct < 0 else self.dd_cumule
        if self.perte_jour <= self.ks: self.bloque_jour = True
        if self.dd_cumule <= self.sf: self.flat = True
    def multiplicateur(self):
        if self.flat or self.bloque_jour: return 0.0
        return 0.5 if self.dd_cumule <= self.sr else 1.0

if __name__ == '__main__':
    # test de sanite deterministe (aucune donnee de marche)
    assert taille(1.0, 0.10, 0.20, 1.5, 2.0, 0.5) == 0.5
    assert taille(1.0, 0.10, 0.20, 2.5, 2.0, 0.5) == 0.0
    assert taille(1.0, 0.10, 0.20, 1.5, 2.0, 0.95) == 0.0
    g = Gouverneur(); g.enregistrer(-0.021); assert g.multiplicateur() == 0.0  # kill-switch
    g2 = Gouverneur(); g2.enregistrer(-0.016); g2.nouvel_jour(); g2.enregistrer(-0.016); assert g2.multiplicateur() == 0.5  # DD cumule -3.2% sans kill-switch journalier
    cfg = load_config()
    print('chassis OK | challenge:', cfg['CHALLENGE_CONFIG']['profit_target_phase1_pct'], '% / duree:', cfg['CHALLENGE_CONFIG']['duration_days'])
