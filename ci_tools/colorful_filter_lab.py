#!/usr/bin/env python3
"""Laboratoire experimental COLORFUL-FILTER-001 (moteur gele colorful_replay.py INTOUCHE).
1) Audit du matching seq446 (glouton +-120 s). 2) Features causales au tick d'entree pour
entrees reelles (A-E, serveur UTC+2 suppose -> UTC) et simulees non appariees.
3) Tests exploratoires en-echantillon F1 (fond ret15m sur voie rapide), F2 (unicite M15),
F3 (delai post-cloture), F4 (ret30m/ret60m). Aucun prix futur. Dukascopy = comparatif."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
OUT = R / 'research/COLORFUL-FILTER-001'; OUT.mkdir(parents=True, exist_ok=True)
REELLES = {  # ouverture affichee serveur (UTC+2 suppose) -> UTC
 'A': '2026-11-26 11:31:20', 'B': '2026-11-26 11:50:34',
 'C': '2026-11-27 08:30:00', 'D': '2026-11-27 08:45:00', 'E': '2026-11-27 09:00:00'}
CLOT_REELLES = {'A': '2026-11-26 11:50:32', 'B': '2026-11-26 12:02:29',
 'C': '2026-11-27 08:40:50', 'D': '2026-11-27 08:45:17', 'E': '2026-11-27 09:01:27'}

def features(df, t):
    df = df[df.ts <= t]
    if len(df) < 100: return None
    mid = df.mid.values; ts = df.ts.values; t64 = np.datetime64(t)
    def ret(s):
        j = np.searchsorted(ts, t64 - np.timedelta64(s, 's'))
        return float((mid[-1] / mid[j] - 1) * 10000) if j < len(mid) else None
    def fen(s):
        j = np.searchsorted(ts, t64 - np.timedelta64(s, 's')); w = mid[j:]
        return w
    w15, w60 = fen(900), fen(3600)
    w5 = fen(300)
    rets1m = pd.Series(w15).pct_change(300).dropna()  # approx non utilisee; vol = ecart inter-tick robuste
    return {'ret5m': ret(300), 'ret15m': ret(900), 'ret30m': ret(1800), 'ret60m': ret(3600),
            'reprise5m_bp': float((mid[-1] / w5.min() - 1) * 10000),
            'pos15_pct': float((mid[-1] - w15.min()) / (w15.max() - w15.min()) * 100) if w15.max() > w15.min() else None,
            'pos60_pct': float((mid[-1] - w60.min()) / (w60.max() - w60.min()) * 100) if w60.max() > w60.min() else None,
            'dist_max15_bp': float((mid[-1] / w15.max() - 1) * 10000),
            'range5_bp': float((w5.max() / w5.min() - 1) * 10000),
            'range15_bp': float((w15.max() / w15.min() - 1) * 10000),
            'bougie_M15_min': int(t.minute % 15), 'heure_utc': str(t)}

def main():
    sim = json.loads((R / 'research/COLORFUL-DROPS-RECONSTRUCTION/REPLAY_RESULTS.json').read_text())
    res = {'audit_matching': {}, 'features': {'reelles': {}, 'simulees_non_appariees': []}}
    utilisees = set()
    for jour, cle in (('2026-11-26', '26'), ('2026-11-27', '27')):
        df = pd.read_parquet(R / f'research/MA-EDGE-02/data/duka_{jour}.parquet').sort_values('ts')
        df['mid'] = (df.bid + df.ask) / 2
        paniers = sim[cle]
        for nom, tstr in REELLES.items():
            if not tstr.startswith(jour): continue
            t = pd.Timestamp(tstr)
            ecarts = [(abs((pd.Timestamp(p['t0']) - t).total_seconds()), i, p) for i, p in enumerate(paniers)]
            ecarts.sort()
            d, i, p = ecarts[0]
            apparie = d <= 120
            if apparie: utilisees.add((cle, i))
            res['audit_matching'][nom] = {'reelle_utc': tstr, 'simulee_la_plus_proche': p['t0'],
                'ecart_s': round((pd.Timestamp(p['t0']) - t).total_seconds(), 1),
                'appariee_pm120s': bool(apparie), 'duree_simulee_s': p['duree_s']}
            f = features(df, t);  res['features']['reelles'][nom] = f
        for i, p in enumerate(paniers):
            if (cle, i) in utilisees: continue
            f = features(df, pd.Timestamp(p['t0']))
            if f: res['features']['simulees_non_appariees'].append({'t0': p['t0'], 'regle': p['regle'], **f})
        # occupation a l'instant E (27) / contexte
    # E: panier simule ouvert a 09:00 UTC le 27 ?
    for p in sim['27']:
        t0, cl = pd.Timestamp(p['t0']), pd.Timestamp(p['cloture'])
        if t0 <= pd.Timestamp(REELLES['E']) <= cl:
            res['audit_matching']['E_occupation'] = {'panier_simule_occupant': p['t0'], 'cloture': p['cloture']}
    # F2: distribution des simulees par bougie M15
    from collections import Counter
    c = Counter()
    for cle in ('26', '27'):
        for p in sim[cle]:
            t = pd.Timestamp(p['t0']); c[(str(t.date()), t.hour, t.minute // 15)] += 1
    res['F2_bougies_multiples'] = {'bougies_avec_plusieurs_entrees_simulees': int(sum(1 for v in c.values() if v > 1)),
                                   'entrees_dans_ces_bougies': int(sum(v for v in c.values() if v > 1)),
                                   'total_bougies': len(c)}
    (OUT / 'FILTER_LAB_RESULTS.json').write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res['audit_matching'], indent=1))
    print('reelles:'); print(pd.DataFrame(res['features']['reelles']).T.round(2).to_string())
    s = pd.DataFrame(res['features']['simulees_non_appariees'])
    print('simulees non appariees n=', len(s)); print(s.describe().T.round(2).to_string())

if __name__ == '__main__':
    main()
