#!/usr/bin/env python3
"""BACKTEST-2026-001: agregation des paniers geles (V1 archive seq457, V2 CI
seq474, novembre rejoue localement a l identique) -> metriques obligatoires,
mensuel, sensibilite couts, drawdown, graphiques. Aucun parametre modifie."""
import json, pathlib, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay import rejouer as r1
from colorful_replay_v2 import rejouer as r2

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/BACKTEST_2026_FULL_PERIOD_001'; OUT.mkdir(parents=True, exist_ok=True)
CAPITAL = 10000.0  # reference declaree (les moteurs expriment le PnL par unite de prix x volume)

def scen_cols(B):
    B = B.copy()
    def s(d): return (B.pnl_net_usd_S0 - d / 10000 * B.prix_moyen * B.volume_total)
    if 'pnl_S1' not in B: B['pnl_S1'] = s(0.3).round(4)
    if 'pnl_S2' not in B: B['pnl_S2'] = s(0.6).round(4)
    if 'pnl_S3' not in B: B['pnl_S3'] = s(2.0).round(4)
    return B

def nov(fn):
    rows = []
    for j in ('20', '22', '23', '24', '25', '26', '27'):
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
        for x in fn(df, df.ts.min(), df.ts.max()):
            vol = sum(v for _, v, _ in x['entrees'])
            rows.append({'t0': str(x['t0']), 'cloture': str(x['cloture']), 'mois_cloture': '2026-11', 'regle': x['regle'],
                         'nb_positions': x['nb'], 'volume_total': round(vol, 2), 'prix_moyen': round(x['prix_moyen'], 2),
                         'duree_s': round(x['duree_s'], 1), 'pnl_net_usd_S0': x['pnl_usd_unite'], 'renforcements': x['nb'] - 1})
    return scen_cols(pd.DataFrame(rows))

def metrics(B, label):
    B = B.sort_values('cloture').reset_index(drop=True)
    pnl = B.pnl_net_usd_S0; eq = pnl.cumsum(); dd = eq - eq.cummax()
    gains, pertes = pnl[pnl > 0], pnl[pnl <= 0]
    streak = cur = 0
    for v in pnl: cur = cur + 1 if v <= 0 else 0; streak = max(streak, cur)
    brut = pnl + 1.2 / 10000 * B.prix_moyen * B.volume_total
    return {'moteur_scenario': label, 'capital_reference_usd': CAPITAL, 'paniers': len(B),
            'positions': int(B.nb_positions.sum()), 'resultat_brut_est_usd': round(brut.sum(), 3),
            'couts_implicites_S0_usd': round((brut - pnl).sum(), 3), 'resultat_net_S0_usd': round(pnl.sum(), 3),
            'rendement_net_pct': round(100 * pnl.sum() / CAPITAL, 3),
            'gagnants_pct': round(100 * len(gains) / len(B), 1) if len(B) else None,
            'profit_factor': round(gains.sum() / abs(pertes.sum()), 3) if len(pertes) and pertes.sum() != 0 else None,
            'esperance_par_panier_usd': round(pnl.mean(), 4) if len(B) else None,
            'gain_moyen_usd': round(gains.mean(), 4) if len(gains) else None,
            'perte_moyenne_usd': round(pertes.mean(), 4) if len(pertes) else None,
            'drawdown_max_usd': round(dd.min(), 3) if len(B) else None,
            'duree_moyenne_s': round(B.duree_s.mean(), 1) if len(B) else None,
            'duree_max_s': round(B.duree_s.max(), 1) if len(B) else None,
            'positions_max_par_panier': int(B.nb_positions.max()) if len(B) else None,
            'volume_max_panier': float(B.volume_total.max()) if len(B) else None,
            'pire_panier_usd': round(pnl.min(), 4) if len(B) else None,
            'serie_max_pertes_consecutives': int(streak)}

def main():
    V1_js = scen_cols(pd.read_csv(R / 'docs/checkpoints/FULL_REPLAY_2026/META_ALPHA_BASKETS_2026.csv'))
    V2_js = scen_cols(pd.read_csv(OUT / 'CI_V2_BASKETS_JAN_SEP.csv'))
    V1_nov, V2_nov = nov(r1), nov(r2)
    V1 = pd.concat([V1_js, V1_nov], ignore_index=True); V2 = pd.concat([V2_js, V2_nov], ignore_index=True)
    V1.to_csv(OUT / 'BACKTEST_V1_RESULTS.csv', index=False); V2.to_csv(OUT / 'BACKTEST_V2_F2_RESULTS.csv', index=False)
    pd.concat([V1.assign(moteur='V1'), V2.assign(moteur='V2-F2')]).to_csv(OUT / 'TRADE_AND_BASKET_LEDGER.csv', index=False)
    rows = [metrics(V1_js, 'V1 / A janv-sept certifie'), metrics(V2_js, 'V2-F2 / A janv-sept certifie'),
            metrics(V1, 'V1 / B couverture maximale'), metrics(V2, 'V2-F2 / B couverture maximale'),
            metrics(V1_nov, 'V1 / novembre partiel'), metrics(V2_nov, 'V2-F2 / novembre partiel')]
    M = pd.DataFrame(rows); M.to_csv(OUT / 'ENGINE_METRICS.csv', index=False); print(M.to_string())
    # mensuel
    flags = {'2026-01': 'PARTIAL (donnees a partir du 12-01)', '2026-07': 'PARTIAL (trou 17-07 21h au 19-07 22h)',
             '2026-09': 'COMPLETE (0 cloture: panier long ouvert bloquant)', '2026-10': 'GAP (aucune donnee)', '2026-11': 'PARTIAL (7 jours de ticks)'}
    mrows = []
    for (moteur, B) in (('V1', V1), ('V2-F2', V2)):
        for m in [f'2026-{i:02d}' for i in range(1, 12)]:
            g = B[B.mois_cloture == m]
            if len(g) == 0:
                mrows.append({'moteur': moteur, 'mois': m, 'couverture': flags.get(m, 'COMPLETE'), 'paniers': 0, 'resultat_net_S0': None, 'profit_factor': None, 'gagnants_pct': None, 'drawdown_max': None}); continue
            mm = metrics(g, '')
            mrows.append({'moteur': moteur, 'mois': m, 'couverture': flags.get(m, 'COMPLETE'), 'paniers': mm['paniers'],
                          'positions': mm['positions'], 'resultat_brut_est': mm['resultat_brut_est_usd'], 'couts_S0': mm['couts_implicites_S0_usd'],
                          'resultat_net_S0': mm['resultat_net_S0_usd'], 'profit_factor': mm['profit_factor'],
                          'gagnants_pct': mm['gagnants_pct'], 'drawdown_max': mm['drawdown_max_usd']})
    pd.DataFrame(mrows).to_csv(OUT / 'MONTHLY_PERFORMANCE_COMPARISON.csv', index=False)
    # sensibilite couts (scenario C)
    crows = []
    for moteur, B in (('V1', V1), ('V2-F2', V2)):
        for s in ('pnl_net_usd_S0', 'pnl_S1', 'pnl_S2', 'pnl_S3'):
            crows.append({'moteur': moteur, 'scenario_cout': s, 'resultat_net_usd': round(B[s].sum(), 3), 'paniers': len(B)})
    pd.DataFrame(crows).to_csv(OUT / 'COST_SENSITIVITY.csv', index=False)
    # drawdown series + charts
    dd_rows = []
    fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    for k, (moteur, B) in enumerate((('V1', V1), ('V2-F2', V2))):
        B = B.sort_values('cloture'); eq = B.pnl_net_usd_S0.cumsum(); dd = eq - eq.cummax()
        x = pd.to_datetime(B.cloture, format='mixed')
        ax[0].plot(x, eq, label=moteur, lw=1); ax[1].plot(x, dd, label=moteur, lw=1)
        dd_rows.append({'moteur': moteur, 'drawdown_max_usd': round(dd.min(), 3), 'date_dd_max': str(x.iloc[int(dd.argmin())]) if len(B) else None})
    ax[0].set_title('BACKTEST-2026-001 - Equity cumulee (USD modele, S0)'); ax[0].legend(); ax[1].set_title('Drawdown'); ax[1].legend()
    fig.tight_layout(); fig.savefig(OUT / 'chart_equity_drawdown.png', dpi=110)
    pd.DataFrame(dd_rows).to_csv(OUT / 'DRAWDOWN_ANALYSIS.csv', index=False)
    print('OK paniers V1', len(V1), 'V2', len(V2))

if __name__ == '__main__':
    main()
