"""PHASE 9 B2-EXTENSION (0 essai, descriptif): prime GVZ - RV(21j) ere 2020->aujourd'hui.
^GVZ via Yahoo chart (CI); RV depuis GC=F daily. Aucune certification, aucun trade."""
import io, json, pathlib
import numpy as np, pandas as pd, requests

OUT = pathlib.Path('reports/meta_alpha/phase9')
def yahoo(sym):
    for host in ['query1', 'query2']:
        try:
            r = requests.get(f'https://{host}.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d', timeout=60,
                             headers={'User-Agent': 'Mozilla/5.0'})
            j = r.json()['chart']['result'][0]; q = j['indicators']['quote'][0]
            return pd.Series(q['close'], index=pd.to_datetime(j['timestamp'], unit='s', utc=True).date)
        except Exception: continue
    return None
gvz = yahoo('%5EGVZ'); gc = yahoo('GC%3DF')
res = {}
if gvz is None or gc is None:
    res = {'statut': 'B2-EXTENSION CLOSE PROPREMENT: ^GVZ ou GC=F indisponible depuis CI (consigne, rien fabrique)', 'gvz': gvz is not None, 'gc': gc is not None}
else:
    ret = np.log(gc.sort_index()).diff()
    rv21 = ret.rolling(21).std() * np.sqrt(252) * 100
    df = pd.DataFrame({'gvz': gvz, 'rv21': rv21}).dropna()
    df['prime'] = df.gvz - df.rv21
    eras = {}
    for lab, a, b in [('2020-22', '2020-01-01', '2022-12-31'), ('2023-24', '2023-01-01', '2024-12-31'), ('2025-26', '2025-01-01', '2026-12-31')]:
        seg = df[(df.index >= pd.Timestamp(a).date()) & (df.index <= pd.Timestamp(b).date())]
        if len(seg): eras[lab] = {'prime_moyenne': float(seg.prime.mean()), 'part_positive': float((seg.prime > 0).mean()), 'n': int(len(seg))}
    res = {'source': 'Yahoo ^GVZ + GC=F (CI)', 'n': int(len(df)), 'prime_globale': float(df.prime.mean()), 'eres': eras,
           'rappel_IS_ancien': '2010-13 +7,1 / 2014-16 +6,0 / 2017-20 +3,1 pts (seq123)',
           'verdict_erosion': 'a lire dans les eres ci-dessus; descriptif pur, actif dormant sans infrastructure options'}
(OUT / 'B2_EXTENSION_NR.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=1, default=str)[:800])
