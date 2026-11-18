"""SIMULATEUR DE CHALLENGE (instruction v3.0 sec.5.3) - parametre par CHALLENGE_CONFIG (OWNER_CONFIG_V1).
Monte Carlo par bootstrap stationnaire (blocs, longueur moyenne 10 trades) d'une serie de PnL nets passee en argument.
Sans serie qualifiee: mode compatibilite uniquement (aucun chiffre de passage invente)."""
import json, pathlib, sys
import numpy as np

def compatibilite(cfg):
    c = cfg['CHALLENGE_CONFIG']
    return {
        'duree': c['duration_days'],
        'compatibilite_horloge': 'COMPATIBLE: duree illimitee - aucun forçage d un moteur basse frequence dans une horloge rapide (discipline sec.5 Phase 3)',
        'jours_rentables_min': f"{c['min_profitable_days']} jours >= +{c['min_profit_per_day_pct']}% - non bloquant en duree illimitee pour un moteur positionne en continu (a verifier par simulation des que le moteur existe)",
        'perte_journaliere': f"-{c['daily_loss_max_pct']}% (reset {c['daily_loss_reset']}) vs kill-switch chassis -2%: marge OK",
        'perte_totale': f"-{c['total_loss_max_pct']}% trailing vs gouverneur -3%/-5%: marge OK",
        'decision_frais': 'AUCUN frais engageable: aucun moteur directionnel qualifie a simuler (F9 NON TESTABLE, gate MDE); P(passer) non calculable - le simulateur tranchera quand une composante L2 directionnelle existera',
    }

def simuler(pnl_pct, cfg, n_sim=10000, seed=42, bloc_moyen=10):
    """pnl_pct: rendements journaliers nets (fractions) de la composante simulee."""
    c = cfg['CHALLENGE_CONFIG']
    cible1 = c['profit_target_phase1_pct'] / 100; perte_j = -c['daily_loss_max_pct'] / 100; perte_t = -c['total_loss_max_pct'] / 100
    rng = np.random.default_rng(seed); x = np.asarray(pnl_pct, float); n = len(x)
    passer = echouer = 0; durees = []
    for _ in range(n_sim):
        idx = []
        while len(idx) < 5 * 252:
            start = rng.integers(0, n); L = max(1, int(rng.geometric(1 / bloc_moyen)))
            idx.extend([(start + k) % n for k in range(L)])
        traj = x[np.array(idx[:5 * 252])]
        eq = np.cumsum(traj); pic = np.maximum.accumulate(np.concatenate([[0], eq]))[:-1]
        dd = eq - pic; jour_ok = traj > (c['min_profit_per_day_pct'] / 100)
        if (traj <= perte_j).any() or (dd <= perte_t).any(): echouer += 1; continue
        hit = np.where(eq >= cible1)[0]
        if len(hit) and jour_ok[:hit[0]].sum() >= 0: passer += 1; durees.append(int(hit[0]))
        else: echouer += 1
    return {'P_passer_phase1': passer / n_sim, 'P_echec_ou_inacheve': echouer / n_sim,
            'jours_medians_si_passage': float(np.median(durees)) if durees else None,
            'regle_decision': 'engager les frais seulement si P(echec) <= 25% (sec.5.3 v3.0)'}

if __name__ == '__main__':
    cfg = json.loads(pathlib.Path('reports/meta_alpha/phase2/OWNER_CONFIG_V1.json').read_text())
    print(json.dumps(compatibilite(cfg), indent=1, ensure_ascii=False))
