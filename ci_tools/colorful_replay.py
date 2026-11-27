#!/usr/bin/env python3
"""Moteur de reproduction COLORFUL DROPS (modele reconstruit, pas la strategie du trader).
Specification implementee (chaque regle tracee a son statut):
- Entree H3 [HYPOTHESE A TESTER]: a une frontiere M15 si ret15m >= +5 bp, OU a tout tick si
  ret5m >= +10 bp et reprise depuis le creux 5m >= +7 bp (voie rapide). Sens: Buy uniquement
  (12/12 transactions observees sont des Buy; aucun Sell observe -> modele muet sur les Sell).
- Amorcage [FORTEMENT ETAYE]: 2e position 0,01 a +30 s (observe 16-40 s).
- Renforcement [FORTEMENT ETAYE]: 3e position quand le Mid recule <= -5,5 bp depuis la 1re
  entree (zone observee -4,7 a -6,6); volume modele 0,02 [formule NON DETERMINEE: C=0,03].
- Cloture [compatible observe]: Mid >= prix moyen pondere du panier -> tout fermer (Buy: Bid).
- Reinitialisation [FORTEMENT ETAYEE sur 1 cas]: reevaluation immediate apres cloture.
- Protection: AUCUNE observee (pas de stop); plafond de positions du modele = 3 (observe max).
Couts: spread paye via Bid/Ask; commission+slippage du scenario CENTRAL (seq431).
Entrees: ticks Dukascopy (reference comparative, jamais HFM). Fuseau serveur suppose UTC+2."""
import json, pathlib, sys
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
COUT_BP = 1.2  # CENTRAL: commission 0,7 + slippage 0,5 (au-dela du spread deja paye)

def rejouer(df, debut_utc, fin_utc):
    df = df[(df.ts >= debut_utc) & (df.ts <= fin_utc)].reset_index(drop=True)
    df['mid'] = (df.bid + df.ask) / 2
    paniers, panier, prochain_possible = [], None, debut_utc
    ts = df.ts.values; mid = df.mid.values; bid = df.bid.values; ask = df.ask.values
    def ret_bp(i, secondes):
        j = np.searchsorted(ts, ts[i] - np.timedelta64(secondes, 's'))
        return (mid[i] / mid[j] - 1) * 10000 if j < i else 0.0
    def reprise_bp(i):
        j = np.searchsorted(ts, ts[i] - np.timedelta64(300, 's'))
        return (mid[i] / mid[j:i + 1].min() - 1) * 10000 if i > j else 0.0
    i = 0
    while i < len(df):
        t = pd.Timestamp(ts[i])
        if panier is None and t >= prochain_possible:
            frontiere = (t.minute % 15 == 0 and t.second < 5)
            voie_rapide = ret_bp(i, 300) >= 10 and reprise_bp(i) >= 7
            horloge = frontiere and ret_bp(i, 900) >= 5
            if voie_rapide or horloge:
                panier = {'entrees': [(t, .01, float(ask[i]))], 't0': t, 'prix1': float(mid[i]),
                          'regle': 'voie_rapide' if voie_rapide else 'horloge_M15'}
        elif panier is not None:
            entrees = panier['entrees']
            if len(entrees) == 1 and (t - entrees[0][0]).total_seconds() >= 30:
                entrees.append((t, .01, float(ask[i])))
            elif len(entrees) == 2 and (mid[i] / panier['prix1'] - 1) * 10000 <= -5.5:
                entrees.append((t, .02, float(ask[i])))
            vol = sum(v for _, v, _ in entrees); moy = sum(v * p for _, v, p in entrees) / vol
            if mid[i] >= moy and (t - entrees[0][0]).total_seconds() > 60:
                pnl = sum(v * (float(bid[i]) - p) for _, v, p in entrees) - COUT_BP / 10000 * moy * vol
                paniers.append({**panier, 'cloture': t, 'prix_moyen': moy, 'pnl_usd_unite': round(pnl, 4),
                                  'nb': len(entrees), 'duree_s': (t - panier['t0']).total_seconds()})
                panier = None; prochain_possible = t  # reevaluation immediate (cas B)
        i += 1
    return paniers

if __name__ == '__main__':
    res = {}
    for jour, d0, d1 in (('26', '2026-11-26 11:00', '2026-11-26 13:00'), ('27', '2026-11-27 07:30', '2026-11-27 09:30')):
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_2026-11-{jour}.parquet').sort_values('ts')
        p = rejouer(df, pd.Timestamp(d0), pd.Timestamp(d1))
        res[jour] = [{**x, 't0': str(x['t0']), 'cloture': str(x['cloture']),
                      'entrees': [(str(a), b, round(c, 2)) for a, b, c in x['entrees']]} for x in p]
        print(jour, len(p), 'paniers simules')
    (R / 'research/COLORFUL-DROPS-RECONSTRUCTION' / 'REPLAY_RESULTS.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1)[:3000])
