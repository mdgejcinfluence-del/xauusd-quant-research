"""Gate v2 (ISOLE: ne remplace pas v1, aucun effet sur P3-002 en cours).
Corrections par rapport a v1:
- Benjamini-Yekutieli (BY) au lieu de BH: valide sous dependance arbitraire entre
  tests d'une vague FIXEE a l'avance (voir MULTIPLICITE_VALIDITE.md pour les limites
  exactes: l'adaptativite entre vagues sort du cadre de garantie; le compteur
  cumulatif reste une penalite conservative, pas une preuve).
- Memes filtres economiques (K2) et causes codees que v1, pour comparabilite.
Les t restent naifs (labels chevauchants): borne optimiste documentee."""
import json, math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gate_engine import gate_buckets, gate_trades, norm_sf

def by_qvalues(pvals, m_total):
    n=len(pvals); c_m=sum(1.0/i for i in range(1, m_total+1))
    order=sorted(range(n), key=lambda i: pvals[i]); q=[0.0]*n; prev=1.0
    for rank in range(n,0,-1):
        i=order[rank-1]; prev=min(prev, pvals[i]*m_total*c_m/rank); q[i]=min(prev,1.0)
    return q

def gate_buckets_v2(results, m_prior):
    g=gate_buckets(results, m_prior)  # calcule diffs, t, verdicts BH
    qs=by_qvalues([t['p'] for t in g['tests']], m_prior+g['n_tests_vague'])
    survivors=[]
    for t,q in zip(g['tests'], qs):
        t['q_by_cumul']=q
        if q<0.05 and t['filtre_economique']: t['verdict']='SURVIVANT_A_QUALIFIER'; survivors.append(t)
        elif q<0.05: t['verdict']='REJETE'; t['cause']='AMPLITUDE_INSUFFISANTE_OU_ABSORBEE_PAR_SPREAD'
        elif t.get('verdict')=='SURVIVANT_A_QUALIFIER': t['verdict']='NON_CONCLUANT'; t['cause']='SIGNIFICATIVITE_PERDUE_SOUS_BY_CUMULATIF'
    g['survivants']=survivors; g['methode']='BY + compteur cumulatif (heuristique conservative, voir MULTIPLICITE_VALIDITE.md)'
    return g

if __name__=='__main__':
    mode, path, m_prior, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    res=json.load(open(path))
    g = gate_buckets_v2(res, m_prior) if mode=='buckets' else gate_trades(res)
    pathlib.Path(out).write_text(json.dumps(g,indent=1))
    print('survivants v2:', len(g.get('survivants',[])) if mode=='buckets' else g['verdict_global'])
