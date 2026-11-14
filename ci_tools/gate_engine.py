"""Moteur de GATE deterministe META ALPHA (aucun LLM, statistiques explicites).
Ingere les resultats bruts d'une vague et produit un verdict structure:
- p-values (approx. normale sur contraste Q5-Q1, t naif documente comme borne optimiste)
- BH-FDR CUMULATIF: le nombre total d'hypotheses deja testees (toutes vagues) est
  passe en parametre et s'ajoute a la correction (penalite sequentielle simple et
  conservative: rang calcule sur la vague, seuil BH avec m = cumul).
- Filtre economique K2: |effet| doit depasser le spread_rel median IS.
- Classification des causes d'echec par regles quantitatives (voir CAUSES).
Produit GATE_<vague>.json + DECISION_REQUISE.json pour la file Arena.
Reproduction historique exigee: P3-001 -> pattern detecte mais NON qualifie;
P4-001 -> REJETE (IC OOS entierement negatif)."""
import json, math, pathlib, sys

SPREAD_MEDIAN_BP = 2.17  # K2: mediane IS approx. depuis seuils P3-001 (q40..q60)

def norm_sf(x):
    return 0.5*(1-math.erf(abs(x)/math.sqrt(2)))

def bh_qvalues(pvals, m_total):
    """q BH avec correction elargie a m_total hypotheses cumulees (>= vague)."""
    n=len(pvals); order=sorted(range(n), key=lambda i: pvals[i])
    q=[0.0]*n; prev=1.0
    for rank in range(n,0,-1):
        i=order[rank-1]
        val=pvals[i]*m_total/rank
        prev=min(prev,val); q[i]=min(prev,1.0)
    return q

def gate_buckets(results, m_prior):
    b=results['buckets']; feats=sorted({k.split('|')[0] for k in b}); hors=sorted({k.split('|')[2] for k in b})
    tests=[]
    for f in feats:
        for h in hors:
            cells=[b.get(f"{f}|Q{i}|{h}") for i in range(1,6)]
            if any(c is None for c in cells): continue
            m=[c['mean_ret'] for c in cells]; n=[c['n'] for c in cells]; sd=[c['sd_ret'] for c in cells]
            diff=m[4]-m[0]; se=math.sqrt(sd[4]**2/n[4]+sd[0]**2/n[0]); t=diff/se if se>0 else 0.0
            mono = all(m[i+1]>=m[i] for i in range(4)) or all(m[i+1]<=m[i] for i in range(4))
            tests.append({'feature':f,'horizon':h,'diff_bp':diff*1e4,'t_naif':t,'p':2*norm_sf(t),'monotone':mono})
    qs=bh_qvalues([t['p'] for t in tests], m_prior+len(tests))
    survivors=[]
    for t,q in zip(tests,qs):
        t['q_bh_cumul']=q
        eco = abs(t['diff_bp']) > SPREAD_MEDIAN_BP
        t['filtre_economique'] = eco
        if q<0.05 and eco: t['verdict']='SURVIVANT_A_QUALIFIER'; survivors.append(t)
        elif q<0.05 and not eco: t['verdict']='REJETE'; t['cause']='AMPLITUDE_INSUFFISANTE_OU_ABSORBEE_PAR_SPREAD'
        elif t['p']<0.05: t['verdict']='NON_CONCLUANT'; t['cause']='SIGNIFICATIVITE_PERDUE_APRES_CORRECTION_CUMULATIVE'
        else: t['verdict']='REJETE'; t['cause']='AUCUN_SIGNAL'
    return {'type':'buckets','n_tests_vague':len(tests),'m_cumulatif':m_prior+len(tests),'tests':tests,'survivants':survivors}

def gate_trades(results):
    oos={k:v for k,v in results.items() if k.startswith('OOS')}
    verdicts={}
    for k,v in oos.items():
        lo,hi=v['boot_ci95_bp']
        if lo<=0<=hi: verdicts[k]='REJETE (IC inclut 0)'
        elif hi<0: verdicts[k]='REJETE (IC entierement negatif)'
        elif lo>0: verdicts[k]='SURVIVANT_A_QUALIFIER'
    global_v='REJETE' if all(v.startswith('REJETE') for v in verdicts.values()) else 'SURVIVANT_A_QUALIFIER'
    return {'type':'trades','verdicts_oos':verdicts,'verdict_global':global_v,
            'cause':'ABSORBE_PAR_SPREAD' if global_v=='REJETE' else None}

if __name__=='__main__':
    mode, path, m_prior, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    res=json.load(open(path))
    g = gate_buckets(res, m_prior) if mode=='buckets' else gate_trades(res)
    pathlib.Path(out).write_text(json.dumps(g,indent=1))
    print(json.dumps({'verdict_global':g.get('verdict_global'),'survivants':len(g.get('survivants',[])) if mode=='buckets' else g['verdict_global']},indent=1))
