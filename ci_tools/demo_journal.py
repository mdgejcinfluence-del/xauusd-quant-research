"""VOIE B — PHASE DEMO: journal -> statistiques -> gate GO/NO-GO (plan sec.5-6).
Journal CSV attendu: date,setup,fenetre,risque_pct,R_realise,regles_respectees
  date ISO; setup libre (ex: S1_tendance_pullback, S2_range); fenetre libre (ex: 13-16);
  risque_pct = risque engage en % du capital; R_realise = resultat en multiples de R;
  regles_respectees = oui/non (respect integral du playbook + veto du chassis).
Sortie: win rate, R moyen, esperance (%/trade), max DD (%), respect des regles,
puis challenge_sim sur les PnL journaliers agreges -> P(passer)/P(echec) et verdict du gate.
Aucun frais tant que le gate n'est pas GO. Les frais sont du capital."""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from challenge_sim import simuler

def analyser(chemin_journal):
    j = pd.read_csv(chemin_journal, parse_dates=['date'])
    j['pnl_pct'] = j.risque_pct * j.R_realise
    n = len(j)
    stats = {
        'trades': int(n),
        'win_rate': float((j.R_realise > 0).mean()),
        'R_moyen': float(j.R_realise.mean()),
        'esperance_pct_par_trade': float(j.pnl_pct.mean()),
        'respect_regles_pct': float((j.regles_respectees.astype(str).str.lower().isin(['oui', 'yes', '1', 'true'])).mean() * 100),
        'par_setup': j.groupby('setup').agg(n=('R_realise', 'size'), R_moyen=('R_realise', 'mean'),
                                            pnl_pct=('pnl_pct', 'sum')).round(4).to_dict('index'),
    }
    jour = j.groupby(j.date.dt.floor('D')).pnl_pct.sum().sort_index()
    eq = jour.cumsum(); dd = eq - eq.cummax()
    stats['max_drawdown_pct'] = float(dd.min()) if len(dd) else 0.0
    stats['jours_de_trade'] = int(len(jour))
    cfg = json.loads(pathlib.Path('reports/meta_alpha/phase2/OWNER_CONFIG_V1.json').read_text())
    if n >= 30:
        sim = simuler(jour.values / 100.0, cfg)
        stats['simulateur'] = sim
    else:
        stats['simulateur'] = {'note': 'echantillon trop faible pour simuler (< 30 trades)'}
    gate = {
        'esperance_positive_100_trades': bool(n >= 100 and stats['esperance_pct_par_trade'] > 0),
        'respect_au_moins_95pct': bool(stats['respect_regles_pct'] >= 95),
        'P_echec_au_plus_25pct': bool(stats.get('simulateur', {}).get('P_echec_ou_inacheve', 1) <= 0.25) if n >= 100 else False,
    }
    gate['VERDICT'] = 'GO' if all(gate.values()) else 'NO-GO — continuer la demo (aucun frais engage)'
    return stats, gate

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] != '--selftest':
        s, g = analyser(sys.argv[1]); print(json.dumps(s, indent=1, default=str)); print(json.dumps(g, indent=1))
    else:
        # auto-test deterministe: journal synthetique, pas de marche reel
        rng = np.random.default_rng(7)
        dates = pd.bdate_range('2026-01-05', periods=70).repeat(2)[:120]
        tmp = pathlib.Path('/tmp/journal_test.csv')
        pd.DataFrame({'date': dates, 'setup': rng.choice(['S1_tendance_pullback', 'S2_range'], 120),
                      'fenetre': '13-16', 'risque_pct': 0.25,
                      'R_realise': rng.choice([-1.0, 1.6], 120, p=[0.52, 0.48]),
                      'regles_respectees': rng.choice(['oui', 'non'], 120, p=[0.97, 0.03])}).to_csv(tmp, index=False)
        s, g = analyser(tmp)
        print(json.dumps(s, indent=1, default=str)); print(json.dumps(g, indent=1))
        assert s['trades'] == 120 and 'VERDICT' in g
        print('demo_journal OK')
