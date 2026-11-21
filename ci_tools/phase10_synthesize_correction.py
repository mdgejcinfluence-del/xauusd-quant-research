"""PHASE 10 - synthese corrective ciblee F10-01/F10-03 (amendement seq289).
Portes economiques AVANT inference; BY a m = 6 fixe (les quatre autres
hypotheses preenregistrees entrent avec p = 1: arretees aux portes ou
verdict conserve; le facteur 6 n'est jamais reduit a 2)."""
import json, pathlib, sys
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase10_synthesize import by_bh, composantes, boot_cluster, tail, CENTRAL_ADD, FAMILLES

ROOT = pathlib.Path('reports/meta_alpha/phase10')

def main():
    ev = pd.read_csv(ROOT / 'PHASE10_EVENTS_CIBLE.csv.gz')
    cov = json.loads((ROOT / 'P10_CIBLE_COVERAGE.json').read_text()) if (ROOT / 'P10_CIBLE_COVERAGE.json').exists() else {}
    resultats = {}
    primaires = {}
    for fam in ('F10-01', 'F10-03'):
        d0 = ev[ev.famille == fam] if len(ev) and 'famille' in ev else ev.iloc[0:0]
        d = d0[(d0.entree_eligible == 1) & (d0.fenetre_complete == 1)].reset_index(drop=True)
        R = {'famille': fam, 'type': 'directionnel', 'detectes': int(len(d0)), 'eligibles': int(len(d)),
             'ineligibles': int(len(d0) - len(d)), 'exclusions': int((d0.fenetre_complete == 0).sum()),
             'diagnostic_fenetres': cov.get('diagnostics', {}).get(fam, {})}
        arretee, verdict = None, None
        if len(d):
            d = d.assign(ts0=pd.to_datetime(d.t_signal), ts1=pd.to_datetime(d.t_sortie))
            d['grappe'] = composantes(d.ts0.values.astype('datetime64[ns]').astype('int64'),
                                      d.ts1.values.astype('datetime64[ns]').astype('int64'))
            R['grappes'] = int(d.grappe.nunique())
            vc = d.grappe.value_counts()
            R['part_grappe_dominante'] = float(vc.iloc[0] / len(d))
            R['alerte_grappe_dominante_5pct'] = bool(R['part_grappe_dominante'] > 0.05)
            d['net'] = d.rendement_signe_bp - CENTRAL_ADD
            R['spread_median_bp'] = float(d.spread_bp.median()); R['C_ref_bp'] = float(d.spread_bp.median() + CENTRAL_ADD)
            R['brut_moyen_bp'] = float(d.rendement_signe_bp.mean()); R['brut_median_bp'] = float(d.rendement_signe_bp.median())
            R['net_moyen_bp'] = float(d.net.mean()); R['net_median_bp'] = float(d.net.median())
            R['couverture_MAE_mediane'] = float(d.mae_bp.median()); R['couverture_MFE_mediane'] = float(d.mfe_bp.median())
            R['seuil_bp_median'] = float(d.seuil_bp.median()) if 'seuil_bp' in d else None
            R['par_ere'] = {e: {'n': int((d.ere == e).sum()), 'net_moyen': float(d[d.ere == e].net.mean()) if (d.ere == e).any() else None}
                            for e in ['2010_2013', '2014_2016', '2017_2020']}
            R['queue_evenement'] = tail(d.mae_bp.values, R['C_ref_bp'])
            R['queue_grappe'] = tail(d.groupby('grappe').mae_bp.max().values, R['C_ref_bp'])
            ev_tail, gr_tail = R['queue_evenement'], R['queue_grappe']
            portes = {'P1_magnitude': bool(R['couverture_MAE_mediane'] >= 3 * R['C_ref_bp']),
                      'P2_esperance': bool(R['net_moyen_bp'] > 0),
                      'P3_colonne': bool(R['net_moyen_bp'] > 0 and ev_tail['mediane_MAE'] <= 3 * R['net_moyen_bp']),
                      'P3_queue_evenement': bool(ev_tail['porte_P90'] and ev_tail['porte_ES90']),
                      'P3_queue_grappe': bool(gr_tail['porte_P90'] and gr_tail['porte_ES90']),
                      'P4_effectifs': bool(len(d) >= 200 and R['grappes'] >= 100)}
            R['portes'] = portes
            for k_, motif in [('P1_magnitude', 'PORTE 1 magnitude mediane < 3 x C_ref'), ('P2_esperance', 'PORTE 2 esperance nette centrale <= 0'),
                              ('P3_colonne', 'PORTE 3 colonne MAE mediane > 3 x esperance nette'), ('P3_queue_evenement', 'PORTE 3 queue evenement'),
                              ('P3_queue_grappe', 'PORTE 3 queue grappe'), ('P4_effectifs', 'PORTE 4 effectif/grappes insuffisants')]:
                if not portes[k_]: arretee = motif; break
            if arretee is None:
                obs, p = boot_cluster(d.rendement_signe_bp.values, d.grappe.values, np.mean)
                R['stat_moyenne_brute_bp'] = float(obs); R['p_boot_grappes'] = float(p)
                primaires[fam] = float(p)
            verdict = None if arretee is None else ('NEGATIF ECONOMIQUE' if arretee.startswith(('PORTE 1', 'PORTE 2')) else 'NON ELIGIBLE')
        else:
            R['portes'] = {}; arretee = 'effectif nul'; verdict = 'NON EVALUABLE'
        R['arretee_a'] = arretee
        if verdict: R['verdict'] = verdict
        resultats[fam] = R
    toutes = [(fam, primaires.get(fam, 1.0)) for fam, _ in FAMILLES]  # m = 6 fixe, jamais reduit a 2
    qs = by_bh([p for _, p in toutes])
    mapq = {fam: q for (fam, _), q in zip(toutes, qs)}
    for fam, p in primaires.items():
        resultats[fam]['p_BY_m6'] = float(mapq[fam])
        resultats[fam]['verdict'] = 'POSITIF ECONOMIQUE' if mapq[fam] <= 0.05 else 'NEGATIF ECONOMIQUE'
    (ROOT / 'PHASE10_CORRECTION_RESULTS.json').write_text(json.dumps(resultats, indent=1, default=str))
    print(json.dumps(resultats, indent=1, default=str)[:5000])

if __name__ == '__main__': main()
