#!/usr/bin/env python3
"""STRATEGY-DISCOVERY-001: diagnostics trajectoires (nov. 2026 local, ticks Dukascopy
comparatifs). D1: etat avant 3e position + contrefactuel descriptif 'sans 3e'
(regle de cloture V1 appliquee au panier tronque a 2 positions; panier non cloture
a la fin du jour = CENSORED, jamais force). D2: decomposition de la suractivite.
Comparaison V1 vs V2 (F2) a donnees et couts identiques. Aucun seuil modifie."""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from colorful_replay import rejouer as rejouer_v1, COUT_BP
from colorful_replay_v2 import rejouer as rejouer_v2

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'docs/checkpoints/STRATEGY_DISCOVERY_001'; OUT.mkdir(parents=True, exist_ok=True)
JOURS = ['20', '22', '23', '24', '25', '26', '27']

def contrefactuel_sans_3e(df, x):
    """Panier tronque aux 2 premieres positions, cloture V1 (Mid>=moyenne, >60s)."""
    if len(x['entrees']) < 3: return None
    (t1, v1, p1), (t2, v2, p2) = x['entrees'][0], x['entrees'][1]
    moy2 = (v1 * p1 + v2 * p2) / (v1 + v2)
    seg = df[(df.ts > t2) & (df.ts <= x['cloture'])]
    can = seg[(seg.mid >= moy2) & ((seg.ts - t1).dt.total_seconds() > 60)]
    if not len(can): return {'cloture_cf': None, 'pnl_cf': None, 'statut': 'CENSORED_PAS_DE_CLOTURE_AVANT_CLOTURE_REELLE_OU_FIN'}
    t = can.ts.iloc[0]; bid = float(df[df.ts <= t].bid.iloc[-1])
    pnl = v1 * (bid - p1) + v2 * (bid - p2) - COUT_BP / 10000 * moy2 * (v1 + v2)
    return {'cloture_cf': str(t), 'pnl_cf': round(float(pnl), 4), 'statut': 'CLOTURE_SIMULEE_REGLE_V1'}

def main():
    res = {'paniers_nov': [], 'comparaison': {}}
    for j in JOURS:
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
        df['mid'] = (df.bid + df.ask) / 2
        for x in rejouer_v1(df, df.ts.min(), df.ts.max()):
            ligne = {'jour': f'2026-11-{j}', 't0': str(x['t0']), 'nb': x['nb'], 'regle': x['regle'],
                     'duree_s': round(x['duree_s'], 1), 'pnl': x['pnl_usd_unite']}
            if x['nb'] >= 3:
                t3 = x['entrees'][2][0]
                avant = df[(df.ts >= x['t0']) & (df.ts <= t3)]
                ligne.update({'mae_avant_3e_bp': round(float((avant.mid.min() / x['prix1'] - 1) * 10000), 2),
                              'delai_3e_s': round((t3 - x['t0']).total_seconds(), 1),
                              **(contrefactuel_sans_3e(df, x) or {})})
            res['paniers_nov'].append(ligne)
    B = pd.DataFrame(res['paniers_nov']); B.to_csv(OUT / 'NOV_BASKET_TRAJECTORIES.csv', index=False)
    # V1 vs V2 memes jours
    lignes = []
    for nom, moteur in (('V1', rejouer_v1), ('V2_F2', rejouer_v2)):
        tous = []
        for j in JOURS:
            df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{j}.parquet').sort_values('ts')
            tous += moteur(df, df.ts.min(), df.ts.max())
        pnl = pd.Series([x['pnl_usd_unite'] for x in tous]); eq = pnl.cumsum()
        lignes.append({'modele': nom, 'paniers': len(tous), 'positions': sum(x['nb'] for x in tous),
            'pnl_net_S0': round(pnl.sum(), 4), 'gagnants_pct': round(100 * (pnl > 0).mean(), 1),
            'profit_factor': round(pnl[pnl > 0].sum() / abs(pnl[pnl <= 0].sum()), 3),
            'duree_moy_s': round(np.mean([x['duree_s'] for x in tous]), 1),
            'duree_max_s': round(max(x['duree_s'] for x in tous), 1),
            'drawdown_max': round(float((eq - eq.cummax()).min()), 4),
            'paniers_3pos': sum(1 for x in tous if x['nb'] == 3),
            'pnl_3pos': round(sum(x['pnl_usd_unite'] for x in tous if x['nb'] == 3), 4)})
    C = pd.DataFrame(lignes); C.to_csv(OUT / 'MODEL_COMPARISON_V1_V2.csv', index=False)
    p3 = B[B.nb >= 3]; cf = p3[p3.statut == 'CLOTURE_SIMULEE_REGLE_V1'] if 'statut' in p3 else p3.iloc[0:0]
    resume = {'nov_paniers': len(B), 'nov_3pos': int((B.nb >= 3).sum()),
              'pnl_3pos': round(B[B.nb >= 3].pnl.sum(), 4), 'pnl_2pos': round(B[B.nb == 2].pnl.sum(), 4),
              'cf_evalues': len(cf),
              'cf_pnl_sans_3e': round(cf.pnl_cf.sum(), 4) if len(cf) else None,
              'pnl_reel_sousensemble_cf': round(cf.pnl.sum(), 4) if len(cf) else None,
              'mae_avant_3e_median_bp': round(float(p3.mae_avant_3e_bp.median()), 2) if len(p3) else None}
    (OUT / 'DIAGNOSTIC_RESUME.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume, indent=1)); print(C.to_string())

if __name__ == '__main__':
    main()
