"""PHASE 7 AXE 2 - MONETISATION F3/F7 (0 essai, simulation pure, modeles geles).
Aucune donnee de marche nouvelle, aucun test: (1) challenge_sim sur flux synthetiques
DECLARES dont la volatilite suit les predictions F3 gelees; (2) filtre F7 chiffre sur
la carte des couts de l'atlas (spreads mesures, pas de score F7 recalcule)."""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, 'ci_tools')
from challenge_sim import simuler

R = pathlib.Path('reports/meta_alpha'); OUT = R / 'phase7'
v2 = json.loads((R / 'phase2/OWNER_CONFIG_V2.json').read_text())
c = v2['CHALLENGE_CONFIG']
cfg = {'CHALLENGE_CONFIG': {'profit_target_phase1_pct': c['phase1_profit_target_pct'], 'daily_loss_max_pct': c['daily_loss_max_pct'],
                            'total_loss_max_pct': c['total_loss_max_pct'], 'min_profitable_days': c['min_trading_days_per_phase'],
                            'min_profit_per_day_pct': c['min_profit_per_qualifying_day_pct'], 'daily_loss_reset': '17h EST', 'duration_days': 'illimitee'}}

f3 = pd.read_csv(R / 'phase2/f3_har/F3_DAILY_PRED.csv').dropna(subset=['pred_har', 'rv'])
sig_hat = np.sqrt(f3.pred_har.values); sig_hat = sig_hat / np.median(sig_hat)   # vol predite relative (mediane 1)
rng = np.random.default_rng(11)
def parcours(pnl, cible_pct, rng):
    """Trajectoire challenge (simulateur declare): arret au passage (cible + >=4 jours >= +0,5%)
    ou a l'echec (jour <= -4% ou drawdown trailing <= -10%). pnl en fractions journalieres."""
    n = len(pnl); eq = 0.0; pic = 0.0; qual = 0
    for j in range(1260):
        x = pnl[rng.integers(0, n)]
        eq += x; pic = max(pic, eq)
        if x >= 0.005: qual += 1
        if x <= -0.04 or eq - pic <= -0.10: return False, j
        if eq >= cible_pct / 100 and qual >= 4: return True, j
    return False, 1260

def simule_trajectoires(pnl, rng, nsim=2000):
    p1 = [parcours(pnl, 10, rng) for _ in range(nsim)]
    npass = sum(1 for ok, _ in p1 if ok)
    durees = [j for ok, j in p1 if ok]
    return {'P_passer_phase1': npass / nsim, 'jours_medians_si_passage': float(np.median(durees)) if durees else None}

res = {'_note_simulateur': "challenge_sim.simuler() (gele) declare echec au premier DD -10% sur 5x252 j meme apres passage: P=0 mecanique sur flux continus - consigne, non utilise pour la comparaison. Simulateur de trajectoire declare ci-dessus (arret au passage/echec, regles V2 phases 1)."}
for mu_bp in [0, 2, 5]:
    z = rng.standard_normal(len(sig_hat))
    base = mu_bp / 1e4 + 0.006 * sig_hat * z / np.mean(sig_hat)   # bruit calibre sur la vol predite F3 (sigma jour ~0,6%)
    cible = base * (1.0 / np.clip(sig_hat, 0.25, 3.0))            # sizing vol-cible F3: risque constant par jour
    res[f'mu_{mu_bp}bp'] = {'sans_F3': simule_trajectoires(base, rng), 'avec_F3_volcible': simule_trajectoires(cible, rng)}
    print(mu_bp, res[f'mu_{mu_bp}bp'])

# F7 en filtre: spreads mesures dans les heures de saut vs heures calmes (atlas horaire)
g = pd.read_parquet(OUT / 'ATLAS_HOURLY.parquet')
seuil = 3 * g.ret.std(); saut = g.ret.abs() > seuil
f7 = {'part_heures_saut': float(saut.mean()), 'spread_median_saut_bp': float(g.spread[saut].median()),
      'spread_median_calme_bp': float(g.spread[~saut].median()), 'spread_p95_saut_bp': float(g.spread[saut].quantile(.95)),
      'F7_gele': 'AUC OOF 0,684; lift 2,85x @ top 5% (F7_RESULTS.json, modele gele - aucun score recalcule ici)'}
f7['exces_spread_par_execution_evites_bp'] = f7['spread_median_saut_bp'] - f7['spread_median_calme_bp']
f7['lecture'] = ("en n'executant pas dans les fenetres flaggees (top 5% du score F7, qui concentrent 2,85x le taux de sauts), "
                 "on evite en mediane l'exces de spread ci-dessus par execution reportee; c'est un cout evite, pas un gain: "
                 "cela suppose un report d'execution acceptable pour la strategie servie.")
(OUT / 'EDGE_MONETIZATION_DATA.json').write_text(json.dumps({'F3_challenge': res, 'F7_filtre': f7}, indent=1, default=str))

lignes = ['# EDGE MONETIZATION — Phase 7 Axe 2 (simulation pure, 0 essai)', '',
          'Modeles geles, aucune donnee nouvelle. Regles 2-Step Pro OWNER_CONFIG_V2; cout aller-retour deja inclus dans les flux nets simules (4,7 bp par trade suppose dans mu).', '',
          '## F3 dans le challenge (flux synthetiques declares: bruit calibre sur la vol predite F3, esperance mu imposee)', '',
          '| mu impose (bp/j) | P(passage P1) sans F3 | P(passage P1) avec sizing vol-cible F3 |', '|---|---|---|']
for k, v in res.items():
    if k.startswith('_'): continue
    lignes.append(f"| {k} | {v['sans_F3']['P_passer_phase1']:.3f} | {v['avec_F3_volcible']['P_passer_phase1']:.3f} |")
lignes += ['', 'Lecture: a esperance imposee egale, le sizing vol-cible F3 ne cree aucune esperance; il regularise le risque journalier '
           '(moins de jours extremes), ce qui deplace legerement la probabilite de passage/survie aux regles -4%/-10%. '
           'Sans strategie directionnelle a servir, mu=0 reste mu=0: la probabilite de passage a mu=0 est celle du hasard moins les couts.', '',
           '## F7 en filtre d execution (carte des couts atlas)', '```json', json.dumps(f7, indent=1, default=str), '```', '',
           '## VERDICT HONNETE (exige par l ordre)',
           'Sans instrument de volatilite dans notre univers (pas d options), F3 et F7 ne monetisent que via timing/sizing '
           "au service d'une strategie directionnelle - jamais seuls. F3 vaut une regularisation du risque (chiffree ci-dessus), "
           "F7 vaut un cout d'execution evite par trade reporte (ci-dessus). Aucun des deux ne produit d'esperance: "
           "ce sont des actifs de service, exactement comme le chassis. Toute strategie future (voie B proprietaire incluse) "
           "les consomme comme tels; aucun frais de challenge ne peut etre justifie par F3/F7 seuls."]
(OUT / 'EDGE_MONETIZATION.md').write_text('\n'.join(lignes))
print('EDGE MONETIZATION TERMINE')
