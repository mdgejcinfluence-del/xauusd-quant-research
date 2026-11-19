"""PHASE 9 CARRY - synthese et gates de certification des pattes (prereg seq127).
Net = funding annualise moyen - 0,40% (couts declares). BY sur les 8 pattes testees (famille carry;
la BY(12) globale de phase est plus severe: appliquee au verdict final du rapport)."""
import json, pathlib
import numpy as np, pandas as pd

R = pathlib.Path('reports/meta_alpha/phase9/carry')
raw = json.loads((R / 'CARRY_RAW.json').read_text())
cands = raw['candidats_par_profondeur']
rng = np.random.default_rng(42)
COUT = 0.40  # % annuel declare
def boot_ci(x, n=8000):
    x = np.asarray(x); m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))
def by(pv):
    pv = np.asarray(pv); m = len(pv); o = np.argsort(pv); c = sum(1 / i for i in range(1, m + 1))
    adj = np.empty(m); run = 1.0
    for i in range(m - 1, -1, -1): run = min(run, pv[o[i]] * m * c / (i + 1)); adj[o[i]] = run
    return adj

res = {}; series = {}
for s in cands:
    f = pd.read_csv(R / f'FUNDING_{s}.csv')
    f['ts'] = pd.to_datetime(f.calc_time, unit='ms', utc=True)
    f['ann'] = f.last_funding_rate * (24 / f.funding_interval_hours) * 365 * 100
    f['jour'] = f.ts.dt.date
    dj = f.groupby('jour').last_funding_rate.sum() * 365 * 100 / 1 * 1  # somme journaliere annualisee approx via taux moyen jour
    dj = f.groupby('jour').apply(lambda x: float((x.last_funding_rate * (24 / x.funding_interval_hours)).sum()) / 1, include_groups=False) * 365 * 100 / 365 * 365 / 365
    # somme journaliere des taux (non annualisee) puis annualisation par la moyenne:
    dj = f.groupby('jour').last_funding_rate.sum()
    series[s] = dj
    ann_mean = float(f.ann.mean()); ann_med = float(f.ann.median())
    lo, hi = boot_ci(dj.values * 365 * 100 / (24 / f.funding_interval_hours.median()) * (f.funding_interval_hours.median() / 24))
    # IC sur le rendement journalier annualise directement:
    jr = dj.values * (365 * 100) / 3  # 3 financements/jour typiques: borne declaree, voir note
    lo, hi = boot_ci(f.groupby('jour').ann.mean().values) if 'ann' in f else (lo, hi)
    jours_pos = float((dj > 0).mean())
    # plus longue serie negative (jours consecutifs somme < 0)
    streak = mx = 0
    for v in dj.values:
        streak = streak + 1 if v < 0 else 0; mx = max(mx, streak)
    eras = {}
    for lab, a, b in [('2021-22', '2021-01-01', '2022-12-31'), ('2023-24', '2023-01-01', '2024-12-31'), ('2025-26', '2025-01-01', '2026-12-31')]:
        seg = f[(f.ts >= a) & (f.ts <= b)]
        if len(seg): eras[lab] = float(seg.ann.mean())
    tiers = np.array_split(f.ann.values, 3)
    from math import erf, sqrt
    jj = f.groupby('jour').ann.mean()
    t = jj.mean() / (jj.std(ddof=1) / np.sqrt(len(jj))); p = 1 - erf(abs(t) / sqrt(2))
    res[s] = {'debut': str(f.ts.min()), 'evenements': int(len(f)), 'funding_ann_moyen_pct': ann_mean,
              'funding_ann_median_pct': ann_med, 'IC95_moyen_journalier': [lo, hi], 'net_apres_couts_pct': ann_mean - COUT,
              'jours_positifs_pct': jours_pos * 100, 'plus_longue_serie_negative_j': int(mx),
              'vol_funding_ann_pct': float(f.ann.std()), 'eres': eras,
              'tiers_stables_positifs': int(sum(1 for x in tiers if x.mean() > 0)), 'p': float(p)}
    print(s, res[s])
padj = by([res[s]['p'] for s in cands])
for s, pa in zip(cands, padj):
    r = res[s]
    r['p_BY_8'] = float(pa)
    eres_pos = sum(1 for v in r['eres'].values() if v > 0)
    r['eres_positives'] = eres_pos
    r['CERTIFIEE'] = bool(r['IC95_moyen_journalier'][0] - COUT > 0 and pa < 0.05 and r['tiers_stables_positifs'] == 3
                          and len(r['eres']) >= 3 and eres_pos == len(r['eres'])
                          and r['plus_longue_serie_negative_j'] <= 90 and r['net_apres_couts_pct'] > 0)
    if len(r['eres']) < 3: r['statut'] = 'NON CERTIFIABLE: historique < 3 eres (en observation, pas enterre comme faux)'
    elif not r['CERTIFIEE']: r['statut'] = 'ENTERREE (gate non passe)'
    else: r['statut'] = 'CERTIFIEE'
corr = pd.DataFrame(series).corr()
res['_corr_journaliere'] = {a: {b: float(corr.loc[a, b]) for b in corr.columns} for a in corr.index}
res['_couts_declares_pct_an'] = COUT
(R / 'CARRY_RESULTS.json').write_text(json.dumps(res, indent=1, default=str))
lignes = ['# CARRY MAP — paiements structurels des perpetuels (Phase 9, seq127)', '',
          'Delta-neutre (short perp + long spot). Net = funding annualise moyen - 0,40% (couts declares prudents). Recherche uniquement: aucun compte, aucun capital.', '',
          '| Patte | Debut | Funding moy %/an | Median %/an | Net %/an | Jours+ % | Serie neg max (j) | Eres 21-22 / 23-24 / 25-26 | Certifiee |', '|---|---|---|---|---|---|---|---|---|']
for s in cands:
    r = res[s]; e = r['eres']
    lignes.append(f"| {s} | {r['debut'][:10]} | {r['funding_ann_moyen_pct']:.2f} | {r['funding_ann_median_pct']:.2f} | {r['net_apres_couts_pct']:.2f} | {r['jours_positifs_pct']:.0f} | {r['plus_longue_serie_negative_j']} | {e.get('2021-22', float('nan')):.1f} / {e.get('2023-24', float('nan')):.1f} / {e.get('2025-26', float('nan')):.1f} | {'**OUI**' if r['CERTIFIEE'] else 'non'} |")
lignes += ['', 'Gates: IC95 (journalier) net > 0, BY sur les pattes, stabilite 3/3 tiers, serie negative <= 90 j, profondeur (selection).',
           'Maths de liquidation (declare): a levier L sur la jambe perp, un spike adverse de 100/L % liquide la jambe avant rehedging; marge de survie recommandee: levier <= 3x et collatéral >= 50% du notionnel pour absorber un spike de +/-30% sans liquidation (a verifier par actif avant toute exploitation - hors Phase 9).',
           'Frontiere actions (Hyperliquid qualifie HTTP 200; Binance Vision liste aussi SOXL/SNDK/SKHYNIX parmi les plus profonds): les perpetuels d actions paient comme les crypto, histoire plus courte.']
(R.parent / 'CARRY_MAP.md').write_text('\n'.join(lignes))
print('certifiees:', [s for s in cands if res[s]['CERTIFIEE']])
print('CARRY SYNTHESE TERMINEE')
