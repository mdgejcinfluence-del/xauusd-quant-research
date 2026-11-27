#!/usr/bin/env python3
"""Moteur de REPLAY chronologique META ALPHA — preparation (aucune strategie, aucune optimisation).
Lit des ticks Bid/Ask UTC tries, applique BUY: entree Ask/sortie Bid, SELL: entree Bid/sortie Ask
(spread compte exactement une fois via les prix d execution), scenarios de couts parametres,
positions multiples/panier, journal de chaque decision. Mode selftest: rejoue un fichier reel
et execute un panier demonstratif horodate (preuve mecanique, pas un test de strategie)."""
import json, pathlib, sys
import pandas as pd

SCENARIOS = {  # bp additionnels AU-DELA du spread Bid/Ask deja paye via les prix d execution
 'OPTIMISTE': {'commission_bp': 0.0, 'slippage_bp': 0.0, 'swap_bp_nuit': 0.0},
 'CENTRAL':   {'commission_bp': 0.7, 'slippage_bp': 0.5, 'swap_bp_nuit': 2.0},
 'PRUDENT':   {'commission_bp': 1.0, 'slippage_bp': 1.5, 'swap_bp_nuit': 4.0},
 'STRESSE':   {'commission_bp': 1.5, 'slippage_bp': 4.0, 'swap_bp_nuit': 8.0}}

class Replay:
    def __init__(self, scenario='CENTRAL'):
        self.c = SCENARIOS[scenario]; self.positions = []; self.journal = []
        self.equity_pics = []
    def prix_exec(self, cote, sens):
        return cote[1] if sens == 'BUY' else cote[0]  # entree: BUY=Ask, SELL=Bid
    def ouvrir(self, ts, sens, lots, bid, ask):
        px = ask if sens == 'BUY' else bid
        p = {'ts_ouverture': str(ts), 'sens': sens, 'lots': lots, 'px_entree': float(px)}
        self.positions.append(p); self.journal.append({'type': 'OUVERTURE', **p})
        return p
    def fermer(self, pos, ts, bid, ask, motif):
        px = bid if pos['sens'] == 'BUY' else ask
        brut = (px - pos['px_entree']) / pos['px_entree'] * 10000 * (1 if pos['sens'] == 'BUY' else -1)
        couts = self.c['commission_bp'] + self.c['slippage_bp']
        net = brut - couts
        e = {'type': 'CLOTURE', 'motif': motif, 'ts_cloture': str(ts), 'px_sortie': float(px),
             'brut_bp': round(float(brut), 3), 'couts_bp': couts, 'net_bp': round(float(net), 3),
             'duree': str(pd.Timestamp(ts) - pd.Timestamp(pos['ts_ouverture']))}
        self.positions.remove(pos); self.journal.append(e); return e
    def fermer_panier(self, ts, bid, ask, motif='PANIER'):
        return [self.fermer(p, ts, bid, ask, motif) for p in list(self.positions)]

def selftest(fichier):
    df = pd.read_parquet(fichier).sort_values('ts')
    r = Replay('CENTRAL'); fermetures = []
    pas = max(1, len(df) // 50)
    for i in range(0, len(df) - pas, pas):
        t = df.iloc[i]
        if i == 0:
            r.ouvrir(t.ts, 'BUY', 0.10, t.bid, t.ask); r.ouvrir(t.ts, 'BUY', 0.05, t.bid, t.ask)
        if i == 25 * pas:
            fermetures += r.fermer_panier(t.ts, t.bid, t.ask)
    print(json.dumps({'fichier': str(fichier), 'ticks': int(len(df)),
                      'journal': r.journal, 'clotures': fermetures}, indent=1, default=str))

if __name__ == '__main__':
    selftest(sys.argv[1])
