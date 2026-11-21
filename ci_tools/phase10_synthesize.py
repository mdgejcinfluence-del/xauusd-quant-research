"""PHASE 10 - portes economiques AVANT inference, BY m=6, bootstrap grappes
(protocole gele seq283). Lit PHASE10_EVENTS.csv.gz."""
import json, pathlib, sys
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path('reports/meta_alpha/phase10'); ROOT.mkdir(parents=True, exist_ok=True)
CENTRAL_ADD = 1.7  # commission hyp. 0,7 + slippage hyp. 1,0 bp (deduit une seule fois)
FAMILLES = [('F10-01', 'directionnel'), ('F10-02', 'directionnel'), ('F10-03', 'directionnel'),
            ('F10-04', 'directionnel'), ('F10-05', 'directionnel'), ('F10-06', 'amplitude')]

def by_bh(pv):
    n = len(pv)
    if n == 0: return []
    o = np.argsort(pv); p = np.asarray(pv)[o]; c_star = 1 / np.sum(1 / np.arange(1, n + 1))
    q = p * n * c_star / (np.arange(n) + 1); q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(n); out[o] = np.minimum(q, 1.0); return list(out)

def composantes(idx_time, fenetre_fin):
    """Grappes = composantes connexes de recouvrement [t_signal, fin de mesure]."""
    ident = np.zeros(len(idx_time), dtype=int)
    g = -1; fin_max = None
    for k in np.argsort(idx_time):
        t = idx_time[k]
        if fin_max is None or t > fin_max: g += 1; fin_max = fenetre_fin[k]
        else: fin_max = max(fin_max, fenetre_fin[k])
        ident[k] = g
    return ident

def boot_cluster(x, grappe, stat_fn, nb=10000, seed=20261113, unilat_superieur=False):
    """Bootstrap par grappes (re-echantillonnage des grappes avec remise).
    p bilateral par defaut; unilat_superieur=True -> H1: statistique > 0."""
    rng = np.random.default_rng(seed); x = np.asarray(x, float); grappe = np.asarray(grappe)
    uc = np.unique(grappe)
    par = [x[grappe == c] for c in uc]
    obs = float(stat_fn(x))
    idx = rng.integers(0, len(uc), size=(nb, len(uc)))
    dist = np.empty(nb)
    for b in range(nb):
        dist[b] = stat_fn(np.concatenate([par[k] for k in idx[b]]))
    if unilat_superieur:
        p = (np.sum(dist <= 0) + 1) / (nb + 1)
    else:
        p = 2 * min((np.sum(dist <= 0) + 1) / (nb + 1), (np.sum(dist >= 0) + 1) / (nb + 1))
    return obs, float(min(p, 1.0))

def tail(x, crefs):
    x = np.asarray(x, float)
    if not len(x): return {}
    p90 = float(np.quantile(x, 0.9, method='linear'))
    es = float(x[x >= p90].mean()) if (x >= p90).any() else p90
    ref = crefs
    return {'mediane_MAE': float(np.median(x)), 'P90_MAE': p90, 'ES90_MAE': es,
            'porte_P90': None if not ref else bool(p90 <= 10 * ref), 'porte_ES90': None if not ref else bool(es <= 15 * ref)}

def main():
    ev = pd.read_csv(ROOT / 'PHASE10_EVENTS.csv.gz')
    cov = json.loads((ROOT / 'P10_COVERAGE.json').read_text()) if (ROOT / 'P10_COVERAGE.json').exists() else {}
    resultats = {}
    primaires = []  # (famille, p) pour BY m=6
    for fam, kind in FAMILLES:
        d0 = ev[ev.famille == fam]
        d = d0[(d0.entree_eligible == 1) & (d0.fenetre_complete == 1)].reset_index(drop=True)
        R = {'famille': fam, 'type': kind, 'detectes': int(len(d0)), 'eligibles': int(len(d)),
             'ineligibles': int(len(d0) - len(d)), 'exclusions': int((d0.fenetre_complete == 0).sum())}
        if len(d):
            t0 = pd.to_datetime(d.t_signal); t1 = pd.to_datetime(d.t_sortie)
            d = d.assign(ts0=t0, ts1=t1)
            d['grappe'] = composantes(d.ts0.values.astype('datetime64[ns]').astype('int64'), d.ts1.values.astype('datetime64[ns]').astype('int64'))
            R['grappes'] = int(d.grappe.nunique())
            vc = d.grappe.value_counts()
            R['part_grappe_dominante'] = float(vc.iloc[0] / len(d)) if len(vc) else None
            R['alerte_grappe_dominante_5pct'] = bool(R['part_grappe_dominante'] and R['part_grappe_dominante'] > 0.05)
            if kind == 'directionnel':
                d['net'] = d.rendement_signe_bp - CENTRAL_ADD  # spread deja dans Bid/Ask; 1,7 bp deduits une fois
                R['spread_median_bp'] = float(d.spread_bp.median())
                R['C_ref_bp'] = float(d.spread_bp.median() + CENTRAL_ADD)
                R['brut_moyen_bp'] = float(d.rendement_signe_bp.mean()); R['brut_median_bp'] = float(d.rendement_signe_bp.median())
                R['net_moyen_bp'] = float(d.net.mean()); R['net_median_bp'] = float(d.net.median())
                R['couverture_MAE_mediane'] = float(d.mae_bp.median()); R['couverture_MFE_mediane'] = float(d.mfe_bp.median())
                R['par_ere'] = {e: {'n': int((d.ere == e).sum()), 'net_moyen': float(d[d.ere == e].net.mean()) if (d.ere == e).any() else None} for e in ['2010_2013', '2014_2016', '2017_2020']}
                R['queue_evenement'] = tail(d.mae_bp.values, R['C_ref_bp'])
                mae_g = d.groupby('grappe').mae_bp.max().values
                R['queue_grappe'] = tail(mae_g, R['C_ref_bp'])
                q = d.groupby('grappe').apply(lambda g: float(g.rendement_signe_bp.max()), include_groups=False)
                fen = d.groupby('grappe').range_fenetre_bp.max()
            else:
                R['ratio_median'] = float(d.ratio_range.median()); R['ratio_moyen'] = float(d.ratio_range.mean())
                R['queue_evenement'] = {}; R['queue_grappe'] = {}
                fen = d.groupby('grappe').range_fenetre_bp.max()
        # ---- PORTES (avant inference) ----
        portes = {}; arretee = None
        if not len(d):
            verdict = 'NON EVALUABLE'; arretee = 'effectif nul'
        elif kind == 'directionnel':
            ev_tail = R['queue_evenement']; gr_tail = R['queue_grappe']
            portes['P1_magnitude'] = bool(R['couverture_MAE_mediane'] >= 3 * R['C_ref_bp'])
            portes['P2_esperance'] = bool(R['net_moyen_bp'] > 0)
            portes['P3_colonne'] = bool(ev_tail['mediane_MAE'] <= 3 * R['net_moyen_bp'] if R['net_moyen_bp'] > 0 else False)
            portes['P3_queue_evenement'] = bool(ev_tail['porte_P90'] and ev_tail['porte_ES90'])
            portes['P3_queue_grappe'] = bool(gr_tail['porte_P90'] and gr_tail['porte_ES90'])
            portes['P4_effectifs'] = bool(len(d) >= 200 and R['grappes'] >= 100)
            ordre = [('P1_magnitude', 'PORTE 1 magnitude mediane < 3 x C_ref'), ('P2_esperance', 'PORTE 2 esperance nette centrale <= 0'),
                     ('P3_colonne', 'PORTE 3 colonne MAE mediane > 3 x esperance nette'), ('P3_queue_evenement', 'PORTE 3 queue evenement'),
                     ('P3_queue_grappe', 'PORTE 3 queue grappe'), ('P4_effectifs', 'PORTE 4 effectif/grappes insuffisants')]
            for k_, motif in ordre:
                if not portes[k_]: arretee = motif; break
            verdict = None if arretee is None else ('NEGATIF ECONOMIQUE' if arretee.startswith('PORTE 1') or arretee.startswith('PORTE 2') else 'NON ELIGIBLE')
        else:
            portes['P1_magnitude_na'] = 'amplitude non directionnelle: porte 1 par ratio median > 1 et test unilat.'
            portes['P4_effectifs'] = bool(len(d) >= 200 and R['grappes'] >= 100)
            arretee = None if portes['P4_effectifs'] else 'PORTE 4 effectif/grappes insuffisants'
            verdict = None if arretee is None else 'NON ELIGIBLE'
        R['portes'] = portes; R['arretee_a'] = arretee
        # ---- INFERENCE (seulement si aucune porte n'arrete) ----
        if arretee is None:
            if kind == 'directionnel':
                obs, p = boot_cluster(d.rendement_signe_bp.values, d.grappe.values, np.mean)
                R['stat_moyenne_brute_bp'] = float(obs); R['p_boot_grappes'] = float(p)
                primaires.append((fam, float(p)))
            else:
                obs, p = boot_cluster(d.ratio_range.values - 1.0, d.grappe.values, np.median, unilat_superieur=True)
                R['stat_mediane_ratio_moins_1'] = float(np.median(d.ratio_range.values - 1.0))
                R['p_boot_grappes_median'] = float(p)
                primaires.append((fam, float(p)))
            R['verdict_apres_portes'] = 'INFERENCE EXECUTEE'
        else:
            R['verdict'] = verdict if 'verdict' in dir() else arretee
            R['verdict'] = verdict
        resultats[fam] = R
    qs = by_bh([p for _, p in primaires])
    for (fam, p), q in zip(primaires, qs):
        resultats[fam]['p_BY_m6'] = float(q)
        passe = q <= 0.05
        if passe:
            dominant = resultats[fam].get('grappes', 0)
            resultats[fam]['verdict'] = 'POSITIF ECONOMIQUE' if resultats[fam].get('type') == 'directionnel' else 'POSITIF ECONOMIQUE (amplitude F10-06)'
        else:
            resultats[fam]['verdict'] = 'NEGATIF ECONOMIQUE'
    (ROOT / 'PHASE10_RESULTS.json').write_text(json.dumps(resultats, indent=1, default=str))
    print(json.dumps(resultats, indent=1, default=str)[:6000])

if __name__ == '__main__': main()
