"""CONTROLE NEGATIF HMM (Phase S complementaire) — simulation uniquement.
Question: la chaine HMM envisagee pour 1R invente-t-elle des etats discrets
dans un processus GARCH continu SANS regime?
Chaine exacte: granularisation |r| en barres de 10 (puis sensibilite 50),
HMM gaussien sticky (ci_tools/phase_s_sim.py, inchange), K=2 (sensibilite K=3).
Mesures par repetition: BIC(K=2)-BIC(K=1), occupation des etats, taux de bascule,
durees moyennes, stabilite. Graines 2000+ : jamais utilisees en calibration.
Critere PREENREGISTRE: si BIC prefere K=2 dans > 50% des repetitions, la chaine
HMM 'invente des regimes' sur GARCH -> NON VALIDE comme detecteur autonome."""
import json, math, time, sys
import numpy as np
sys.path.insert(0,'ci_tools')
src=open('ci_tools/phase_s_sim.py').read().split('# ---------- generateurs')[0]
g={}; exec(src,g)
exec('# gen\n'+open('ci_tools/phase_s_sim.py').read().split('# ---------- generateurs (verites) ----------')[1].split('results=')[0], g)
granulate, hmm_gauss, gen_garch = g['granulate'], g['hmm_gauss'], g['gen_garch']

def hmm_ll(x, K, sticky=50.0, iters=200):
    """Log-vraisemblance a convergence (recopie de la boucle EM de hmm_gauss)."""
    import math as m
    n=len(x); mu=np.quantile(x, np.linspace(0.2,0.8,K)); sd=np.full(K, x.std()); A=np.full((K,K),0.05/(K-1) if K>1 else 1.0)
    if K>1: np.fill_diagonal(A,0.95)
    pi=np.full(K,1.0/K); ll_old=-np.inf; states=None
    for _ in range(iters):
        B=np.exp(-0.5*((x[:,None]-mu[None,:])/sd[None,:])**2)/(sd[None,:]*m.sqrt(2*m.pi))
        al=np.zeros((n,K)); sc=np.zeros(n); al[0]=pi*B[0]; sc[0]=al[0].sum(); al[0]/=sc[0]
        for t in range(1,n):
            al[t]=(al[t-1]@A)*B[t]; sc[t]=al[t].sum(); al[t]/=sc[t]
        be=np.ones((n,K))
        for t in range(n-2,-1,-1): be[t]=(A@(B[t+1]*be[t+1]))/sc[t+1]
        ga=al*be; ga/=ga.sum(1,keepdims=True); states=ga.argmax(1)
        xi=np.zeros((K,K))
        for t in range(n-1):
            mm=np.outer(al[t], B[t+1]*be[t+1])*A; xi+=mm/mm.sum()
        Nk=ga.sum(0); mu=(ga*x[:,None]).sum(0)/Nk; sd=np.sqrt((ga*(x[:,None]-mu[None,:])**2).sum(0)/Nk)+1e-12
        A=(xi+sticky*np.eye(K))/(xi.sum(1,keepdims=True)+sticky); pi=ga[0]
        ll=float(np.sum(np.log(sc)))
        if abs(ll-ll_old)<1e-7: break
        ll_old=ll
    npar = K*2 + K*(K-1) + (K-1)
    return ll, npar, states

def bic(ll, npar, n): return -2*ll + npar*math.log(n)

res={'config':{'generateur':'GARCH(1,1) omega=0.05 alpha=0.10 beta=0.85, n=4000, echelle 1e-4',
 'graines':'2000-2011 (neuves)','barres':[10,50],'sticky':[10.0,50.0,200.0],'K':[2,3],
 'critere':'HMM invente des regimes si BIC(K=2) < BIC(K=1) dans > 50% des repetitions (config de reference barres=10, sticky=50)'},
 'repetitions':[]}
t0=time.time()
for seed in range(2000,2012):
    r=gen_garch(4000, seed)
    for bar in (10,50):
        x=np.abs(granulate(r,bar))
        ll1,p1,_=hmm_ll(x,1); ll2,p2,st2=hmm_ll(x,2,50.0)
        switches=int(np.sum(st2[1:]!=st2[:-1]))
        occ=np.bincount(st2, minlength=2)/len(st2)
        res['repetitions'].append({'seed':seed,'barre':bar,'sticky':50.0,'K':2,
          'bic1':round(bic(ll1,p1,len(x)),1),'bic2':round(bic(ll2,p2,len(x)),1),
          'k2_prefere': bool(bic(ll2,p2,len(x))<bic(ll1,p1,len(x))),
          'occupation_min':round(float(occ.min()),3),'bascules':switches,
          'duree_moyenne_etat':round(len(st2)/max(switches,1),1)})
for seed in range(2000,2004):
    r=gen_garch(4000, seed); x=np.abs(granulate(r,10))
    for sticky in (10.0,200.0):
        ll1,p1,_=hmm_ll(x,1); ll2,p2,st2=hmm_ll(x,2,sticky)
        res['repetitions'].append({'seed':seed,'barre':10,'sticky':sticky,'K':2,
          'k2_prefere': bool(bic(ll2,p2,len(x))<bic(ll1,p1,len(x))),
          'bascules':int(np.sum(st2[1:]!=st2[:-1]))})
    ll3,p3,st3=hmm_ll(x,3,50.0); ll1,p1,_=hmm_ll(x,1)
    res['repetitions'].append({'seed':seed,'barre':10,'sticky':50.0,'K':3,
      'k3_prefere': bool(bic(ll3,p3,len(x))<bic(ll1,p1,len(x))),
      'bascules':int(np.sum(st3[1:]!=st3[:-1]))})
ref=[x for x in res['repetitions'] if x['barre']==10 and x['sticky']==50.0 and x['K']==2]
frac=float(np.mean([x['k2_prefere'] for x in ref]))
res['synthese']={'config_reference':'barre=10, sticky=50, K=2','repetitions':len(ref),
 'fraction_K2_prefere_par_BIC':frac,'verdict_selon_critere':'INVENTE_DES_REGIMES' if frac>0.5 else 'NE_PAS_INVENTE',
 'duree_totale_s':round(time.time()-t0,1)}
json.dump(res, open('reports/meta_alpha/phaseS/HMM_NEGATIVE_CONTROL.json','w'), indent=1)
print(json.dumps(res['synthese'], indent=1))
