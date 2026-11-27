#!/usr/bin/env python3
"""RE-ENTRY-001 — reconstruction des paniers A/B du 2026-11-26 sur ticks Dukascopy
(reference comparative uniquement, jamais presentee comme cotation HFM).
Balayage de fuseau UTC+0..+5 juge sur la coherence avec les profits affiches (11 et 13),
puis fenetres pre-entree, deplacements aux renforcements, progression des lots, clotures."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
df = pd.read_parquet(R/'research/MA-EDGE-02/data/duka_2026-11-26.parquet').sort_values('ts').reset_index(drop=True)
A = [('13:31:20',.01),('13:32:00',.01),('13:35:00',.02)]; AC = ['13:50:32','13:50:33']
B = [('13:50:34',.01),('13:51:03',.01),('14:01:01',.02)]; BC = ['14:02:29']

def px(t, cote):
    i = int(df.ts.searchsorted(t));  return float(df[cote].iloc[min(i, len(df)-1)]) if i < len(df) else np.nan
def mid(t):
    i = int(df.ts.searchsorted(t));  return float((df.bid.iloc[min(i,len(df)-1)] + df.ask.iloc[min(i,len(df)-1)])/2)

def panier(E, C, sh):
    ents = [(pd.Timestamp(f'2026-11-26 {t}')-sh, v, px(pd.Timestamp(f'2026-11-26 {t}')-sh,'ask')) for t,v in E]
    ex = px(pd.Timestamp(f'2026-11-26 {C[0]}')-sh, 'bid')
    pnl = sum(v*(ex-p) for _,v,p in ents)
    vol = sum(v for _,v,p in ents); moy = sum(v*p for _,v,p in ents)/vol
    return ents, ex, pnl, moy

res = {'source_cotations': 'Dukascopy (reference comparative, pas HFM)', 'fuseaux': {}}
for tz in range(0, 6):
    sh = pd.Timedelta(hours=tz); ligne = {}
    for nom, E, C in (('A', A, AC), ('B', B, BC)):
        ents, ex, pnl, moy = panier(E, C, sh)
        ligne[nom] = {'pnl_usd_par_unite_contrat': round(pnl, 4), 'prix_moyen': round(moy, 2), 'sortie_bid': round(ex, 2)}
    res['fuseaux'][f'UTC+{tz}'] = ligne
    print(f"UTC+{tz}: A={ligne['A']['pnl_usd_par_unite_contrat']} B={ligne['B']['pnl_usd_par_unite_contrat']} (affiches 11 / 13)")

# Fuseau retenu pour la description mecanique: celui ou les deux paniers sont positifs et du meme ordre
print(json.dumps(res, indent=1))
(R/'research/RE-ENTRY-001'/'TZ_SCAN.json').write_text(json.dumps(res, indent=1))
