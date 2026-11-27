#!/usr/bin/env python3
"""BACKTEST-COLORFUL-2026-001 — backtest du moteur GELE V1 sur les ticks reellement
accessibles (Dukascopy journaliers nov. 2026; jamais presentes comme HFM).
Aucun parametre modifie: on importe rejouer() de colorful_replay.py tel quel.
Sensibilite couts S1-S3 appliquee post-hoc sur le PnL (signaux inchanges):
surcout = delta_bp/10000 * prix_moyen * volume_total du panier."""
import hashlib, json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay import rejouer, COUT_BP

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/BACKTEST_COLORFUL_2026'; OUT.mkdir(parents=True, exist_ok=True)
JOURS = ['20', '22', '23', '24', '25', '26', '27']
HFM = [('Janvier', 151.61), ('Fevrier', 75.64), ('Mars', 91.01), ('Avril', 54.87), ('Mai', 46.01),
       ('Juin', 44.57), ('Juillet', 52.60), ('Aout', -1.05), ('Septembre', 33.49), ('Octobre', 16.24), ('Novembre (1-27)', 9.33)]

def main():
    moteur = R / 'ci_tools/colorful_replay.py'
    modele = {'moteur': 'ci_tools/colorful_replay.py (V1 GELE)',
              'sha256_colorful_replay.py': hashlib.sha256(moteur.read_bytes()).hexdigest(),
              'spec': 'H3: frontiere M15 si ret15m>=+5bp OU voie rapide ret5m>=+10bp et reprise>=+7bp; amorcage +30s; renforcement -5.5bp lot 0.02; cloture Mid>=prix moyen apres 60s; cout CENTRAL 1.2bp au-dela du spread Bid/Ask (compte une fois)',
              'cout_bp_moteur': COUT_BP, 'commit_base': '7020253', 'registre_prereg': 'seq454',
              'donnees': 'ticks Dukascopy Bid/Ask (comparatifs, JAMAIS HFM), fichiers research/MA-EDGE-02/data/duka_2026-11-*.parquet',
              'empreintes_donnees': {j: hashlib.sha256((R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').read_bytes()).hexdigest() for j in JOURS}}
    (OUT / 'MODEL_FINGERPRINT.json').write_text(json.dumps(modele, indent=1))
    pd.DataFrame([{'mois': m, 'valeur_affichee': v, 'unite_affichee': '% (affiche)',
                    'statut': 'HFM_DISPLAYED_MONTHLY_METRIC_UNVERIFIED',
                    'note': 'convention inconnue (time-weighted affiche par HFM; depots/retraits JPY; non transformee)'} for m, v in HFM]
                 ).to_csv(OUT / 'HFM_MONTHLY_REFERENCE_2026.csv', index=False)
    paniers, couv = [], []
    for j in JOURS:
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
        p = rejouer(df, df.ts.min(), df.ts.max())
        for x in p:
            vol = sum(v for _, v, _ in x['entrees'])
            paniers.append({'jour': f'2026-11-{j}', 't0': str(x['t0']), 'cloture': str(x['cloture']),
                            'regle': x['regle'], 'nb_positions': x['nb'], 'volume_total': round(vol, 2),
                            'prix_moyen': round(x['prix_moyen'], 2), 'duree_s': round(x['duree_s'], 1),
                            'pnl_net_usd_S0': x['pnl_usd_unite'],
                            'renforcements': x['nb'] - 1})
        couv.append({'jour': f'2026-11-{j}', 'ticks': len(df), 'debut': str(df.ts.min()), 'fin': str(df.ts.max()),
                     'heures_couvertes': round((df.ts.max() - df.ts.min()).total_seconds() / 3600, 2),
                     'spread_median_bp': round(((df.ask - df.bid) / ((df.ask + df.bid) / 2) * 10000).median(), 2),
                     'paniers': len(p)})
    B = pd.DataFrame(paniers); B.to_csv(OUT / 'MONTHLY_BASKETS_2026.csv', index=False)
    C = pd.DataFrame(couv)
    # scenarios de couts (post-hoc, signaux inchanges)
    def pnl_scen(delta_bp):
        return (B.pnl_net_usd_S0 - delta_bp / 10000 * B.prix_moyen * B.volume_total).round(4)
    B['pnl_S1_+25pct'] = pnl_scen(COUT_BP * 0.25); B['pnl_S2_+50pct'] = pnl_scen(COUT_BP * 0.50)
    B['pnl_S3_+2bp_slippage'] = pnl_scen(2.0)
    B.to_csv(OUT / 'MONTHLY_BASKETS_2026.csv', index=False)
    scen = pd.DataFrame([{'scenario': s, 'definition': d, 'pnl_net_total_usd_modele': round(B[c].sum(), 4),
                          'paniers_gagnants': int((B[c] > 0).sum()), 'paniers_perdants': int((B[c] <= 0).sum())}
                         for s, d, c in [('S0', 'couts moteur (spread Bid/Ask + 1.2bp CENTRAL)', 'pnl_net_usd_S0'),
                                         ('S1', 'cout variable +25% (1.5bp)', 'pnl_S1_+25pct'),
                                         ('S2', 'cout variable +50% (1.8bp)', 'pnl_S2_+50pct'),
                                         ('S3', 'S0 + slippage hypothetique 2bp (ETIQUETE HYPOTHETIQUE)', 'pnl_S3_+2bp_slippage')]])
    scen.to_csv(OUT / 'COST_SENSITIVITY_2026.csv', index=False)
    # metriques mensuelles (novembre partiel, jours disponibles)
    eq = B.pnl_net_usd_S0.cumsum(); dd = (eq - eq.cummax()).min()
    g, l = B[B.pnl_net_usd_S0 > 0].pnl_net_usd_S0, B[B.pnl_net_usd_S0 <= 0].pnl_net_usd_S0
    met = {'mois': 'Novembre (1-27)', 'jours_testes': JOURS, 'ticks_exploites': int(C.ticks.sum()),
           'paniers': len(B), 'positions_totales': int(B.nb_positions.sum()), 'renforcements': int(B.renforcements.sum()),
           'pnl_net_usd_modele_S0': round(B.pnl_net_usd_S0.sum(), 4),
           'pnl_brut_approx_usd (net+cout variable moteur)': round((B.pnl_net_usd_S0 + COUT_BP / 10000 * B.prix_moyen * B.volume_total).sum(), 4),
           'taux_paniers_gagnants_pct': round(100 * len(g) / len(B), 1),
           'gain_moyen_usd': round(g.mean(), 4) if len(g) else None, 'perte_moyenne_usd': round(l.mean(), 4) if len(l) else None,
           'profit_factor': round(g.sum() / abs(l.sum()), 3) if len(l) and l.sum() != 0 else None,
           'esperance_par_panier_usd': round(B.pnl_net_usd_S0.mean(), 4),
           'duree_moyenne_s': round(B.duree_s.mean(), 1), 'duree_mediane_s': round(B.duree_s.median(), 1),
           'duree_max_s': round(B.duree_s.max(), 1), 'drawdown_max_usd_modele (equity paniers)': round(float(dd), 4),
           'pire_panier_usd': round(B.pnl_net_usd_S0.min(), 4), 'meilleur_panier_usd': round(B.pnl_net_usd_S0.max(), 4),
           'volume_max_simultane (modele, 1 panier a la fois)': float(B.volume_total.max()),
           'statut': 'PARTIEL: 7 jours de ticks disponibles sur 27; mois NON integralement backteste'}
    pd.DataFrame([met]).to_csv(OUT / 'META_ALPHA_MONTHLY_RESULTS_2026.csv', index=False)
    pd.DataFrame([{'metrique': k, 'valeur': v} for k, v in met.items()]).to_csv(OUT / 'MONTHLY_RISK_METRICS_2026.csv', index=False)
    cap = pd.DataFrame([{'capital_usd': c, 'rendement_net_novembre_partiel_pct': round(100 * B.pnl_net_usd_S0.sum() / c, 4),
                         'drawdown_max_pct_capital': round(100 * abs(float(dd)) / c, 4),
                         'note': 'scenario normalise META ALPHA uniquement; ne reproduit PAS le compte du fournisseur (capital historique inconnu)'}
                        for c in (1000, 10000, 100000)])
    cap.to_csv(OUT / 'CAPITAL_SCENARIOS_2026.csv', index=False)
    mois = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Septembre', 'Octobre', 'Novembre (1-27)']
    comp = pd.DataFrame({'mois': mois, 'HFM_affiche': [v for _, v in HFM],
                         'META_ALPHA_net': ['NON CALCULE (donnees non accessibles)'] * 10 + [round(B.pnl_net_usd_S0.sum(), 4)],
                         'ecart': 'NOT_DIRECTLY_COMPARABLE', 'couverture_ticks_locale': ['certifie Drive 2026-01-12+ non telechargeable ici' if i < 9 else ('certifie jusqu au 2026-09-30' if i == 9 else '7 jours locaux') for i in range(11)],
                         'statut': ['NON_TESTABLE'] * 10 + ['PARTIEL']})
    comp.to_csv(OUT / 'HFM_VS_META_ALPHA_COMPARISON_2026.csv', index=False)
    couv_mois = pd.DataFrame({'mois': mois,
        'couverture': ['corpus certifie a partir du 2026-01-12 (Drive, 2.44 Go, non accessible byte-level ici)'] + ['corpus certifie Drive (non accessible byte-level ici)'] * 8 + ['backfill annonce, absent localement'] + ['7 jours Dukascopy locaux (20,22,23,24,25,26,27)'],
        'ticks_exploites_localement': [0] * 10 + [int(C.ticks.sum())], 'statut': ['NON_TESTABLE'] * 10 + ['PARTIEL']})
    couv_mois.to_csv(OUT / 'MONTHLY_DATA_COVERAGE_2026.csv', index=False)
    C.to_csv(OUT / 'DAILY_COVERAGE_NOV2026.csv', index=False)
    # graphiques
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].bar([m[:3] for m, _ in HFM], [v for _, v in HFM], color='grey'); ax[0].set_title('HFM affiche 2026 (UNVERIFIED, %)')
    ax[1].plot(eq.values, color='navy'); ax[1].set_title('Equity simulee META ALPHA - nov. partiel (USD modele)'); ax[1].axhline(0, color='k', lw=.5)
    fig.tight_layout(); fig.savefig(OUT / 'chart_hfm_vs_equity.png', dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 3.5)); ax.bar(C.jour, C.paniers); ax.set_title('Paniers simules par jour (nov. 2026, jours disponibles)'); fig.tight_layout(); fig.savefig(OUT / 'chart_baskets_per_day.png', dpi=110)
    print(json.dumps(met, indent=1, ensure_ascii=False)); print(scen.to_string())

if __name__ == '__main__':
    main()
