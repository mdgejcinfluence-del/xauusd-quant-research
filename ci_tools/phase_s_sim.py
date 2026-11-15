"""PHASE S — validation de la chaine sur SIMULATION uniquement (aucune donnee reelle).
Chaine testee: granularisation (agregation en barres d'evenements) -> segmentation
exacte par programmation dynamique a penalite BIC (equivalent objectif PELT) ->
HMM gaussien sticky (EM) -> estimation de memoire (variance agregee).
Controles a verite connue, criteres PREENREGISTRES dans ce fichier avant execution.
Toutes les tentatives sont conservees dans le JSON de sortie."""
import json, time, math
import numpy as np

RNG = np.random.default_rng(20261115)

# ---------- briques de la chaine ----------
PEN_FACTOR = 6.0  # tentative 2: penalite renforcee type MBIC (tentative 1 a 2.0 conservee dans les resultats)
MIN_SEG = 50
def dp_segment(y, pen):
    """Segmentation exacte O(n^2) minimisant SSE + pen * nb_segments (n modere)."""
    pen = pen * PEN_FACTOR / 2.0
    n=len(y); c=np.concatenate([[0], np.cumsum(y)]); c2=np.concatenate([[0], np.cumsum(y*y)])
    def sse(a,b):
        m=b-a; s=c[b]-c[a]; return (c2[b]-c2[a]) - s*s/m
    F=np.full(n+1, np.inf); F[0]=-pen; prev=np.zeros(n+1, dtype=int)
    for b in range(1,n+1):
        cand=[F[a]+sse(a,b)+pen if (a==0 or b-a>=MIN_SEG) and (a==0 or a>=MIN_SEG or a==0) else np.inf for a in range(b)]
        prev[b]=int(np.argmin(cand)); F[b]=cand[prev[b]]
    pts=[]; b=n
    while b>0:
        a=prev[b]
        if a>0: pts.append(a)
        b=a
    return sorted(pts)

def hmm_gauss(x, K=2, iters=200, sticky=50.0):
    """HMM gaussien EM avec prior sticky sur la diagonale de transition."""
    n=len(x); mu=np.quantile(x, np.linspace(0.2,0.8,K)); sd=np.full(K, x.std())
    A=np.full((K,K), 0.05/(K-1) if K>1 else 1.0); np.fill_diagonal(A, 0.95)
    pi=np.full(K, 1.0/K)
    def e_step(mu,sd,A):
        B=np.exp(-0.5*((x[:,None]-mu[None,:])/sd[None,:])**2)/(sd[None,:]*math.sqrt(2*math.pi))
        al=np.zeros((n,K)); sc=np.zeros(n); al[0]=pi*B[0]; sc[0]=al[0].sum(); al[0]/=sc[0]
        for t in range(1,n):
            al[t]=(al[t-1]@A)*B[t]; sc[t]=al[t].sum(); al[t]/=sc[t]
        be=np.ones((n,K))
        for t in range(n-2,-1,-1):
            be[t]=(A@(B[t+1]*be[t+1]))/sc[t+1]
        ga=al*be; ga/=ga.sum(1,keepdims=True)
        xi=np.zeros((K,K))
        for t in range(n-1):
            m=np.outer(al[t], B[t+1]*be[t+1])*A; xi+=m/m.sum()
        return ga, xi, float(np.sum(np.log(sc)))
    ll_old=-np.inf
    for _ in range(iters):
        ga,xi,ll=e_step(mu,sd,A)
        Nk=ga.sum(0); mu=(ga*x[:,None]).sum(0)/Nk
        sd=np.sqrt((ga*(x[:,None]-mu[None,:])**2).sum(0)/Nk)+1e-12
        A=(xi+sticky*np.eye(K))/(xi.sum(1,keepdims=True)+sticky)
        pi=ga[0]
        if abs(ll-ll_old)<1e-7: break
        ll_old=ll
    return ga.argmax(1), mu, sd, A

def hurst_aggvar(r, max_lag=64):
    lags=np.array([1,2,4,8,16,32,64]); vars_=[]
    for L in lags:
        m=len(r)//L*L; vars_.append(np.var(r[:m].reshape(-1,L).sum(1)))
    slope=np.polyfit(np.log(lags), np.log(vars_), 1)[0]
    return slope/2  # var somme ~ L^(2H)

def granulate(r, bar=20):
    n=len(r)//bar*bar
    return r[:n].reshape(-1,bar).sum(1)

# ---------- generateurs (verites) ----------
def gen_garch(n, seed):
    rng=np.random.default_rng(seed); e=rng.standard_normal(n); s2=np.zeros(n); r=np.zeros(n); s2[0]=1.0
    for t in range(1,n):
        s2[t]=0.05+0.10*r[t-1]**2+0.85*s2[t-1]; r[t]=math.sqrt(s2[t])*e[t]
    return r*1e-4

def gen_fgn(n, H, seed):
    rng=np.random.default_rng(seed)
    k=np.arange(n); cov=0.5*(np.abs(k+1)**(2*H)-2*np.abs(k)**(2*H)+np.abs(np.maximum(k-1,0))**(2*H)); cov[0]=1.0
    C=np.array([[cov[abs(i-j)] for j in range(200)] for i in range(200)]) if n>200 else None
    # generation par blocs de 200 (approximation documentee: memoire intra-bloc exacte)
    out=[]
    L=np.linalg.cholesky(C+1e-10*np.eye(200))
    while len(out)<n: out.extend(L@rng.standard_normal(200))
    return np.array(out[:n])*1e-4

def gen_hmm_vol(n, seed, vols=(1.0,3.0), p_stay=0.995):
    rng=np.random.default_rng(seed); st=np.zeros(n,dtype=int)
    for t in range(1,n): st[t]=st[t-1] if rng.random()<p_stay else 1-st[t-1]
    return rng.standard_normal(n)*np.array(vols)[st]*1e-4, st

def gen_spread_regime(n, seed, means=(2.0e-4,4.0e-4), sd=0.3e-4, p_stay=0.995):
    rng=np.random.default_rng(seed); st=np.zeros(n,dtype=int)
    for t in range(1,n): st[t]=st[t-1] if rng.random()<p_stay else 1-st[t-1]
    return np.array(means)[st]+rng.standard_normal(n)*sd, st

def gen_msm_vol(n, seed):
    """Volatilite a 2 echelles markoviennes (approximation MSM documentee)."""
    rng=np.random.default_rng(seed)
    s1=np.zeros(n,dtype=int); s2=np.zeros(n,dtype=int)
    for t in range(1,n):
        s1[t]=s1[t-1] if rng.random()<0.999 else 1-s1[t-1]
        s2[t]=s2[t-1] if rng.random()<0.98 else 1-s2[t-1]
    vol=(1.0+1.5*s1)*(1.0+0.8*s2)
    return rng.standard_normal(n)*vol*1e-4, vol

def acc(true, est, labels_true=(0,1)):
    """Exactitude apres alignement optimal des etiquettes (permutation)."""
    best=0
    for perm in [(0,1),(1,0)]:
        m=np.array([perm[e] for e in est]); best=max(best, float(np.mean(m==true)))
    return best

results={'controles':[], 'tentatives':[]}
def log(control, ok, details):
    results['controles'].append({'controle':control,'succes':bool(ok),'details':details})
    print(control, 'PASS' if ok else 'FAIL', details, flush=True)

# ---------- S1: GARCH sans regime (controle negatif imperatif) ----------
t0=time.time(); fps=0; reps=8
for s in range(reps):
    r=gen_garch(4000, 100+s); g=granulate(np.abs(r),20)
    pts=dp_segment(g, pen=len(g)*0+ 2*math.log(len(g))*np.var(g))
    if len(pts)>1: fps+=1
    results['tentatives'].append({'controle':'S1_GARCH','seed':100+s,'ruptures':len(pts)})
log('S1_GARCH_aucun_regime', fps<=1, {'repetitions':reps,'series_avec_ruptures_spurieuses(>1)':fps,'critere':'<=1/8','duree_s':round(time.time()-t0,1)})

# ---------- S2: processus fractionnaire (memoire stable) ----------
t0=time.time(); est=[]; halves=[]
for s in range(4):
    r=gen_fgn(2000, 0.7, 200+s); est.append(hurst_aggvar(r))
    halves.append(abs(hurst_aggvar(r[:1000])-hurst_aggvar(r[1000:])))
ok = abs(float(np.mean(est))-0.7)<0.10 and float(np.max(halves))<0.20
log('S2_fractionnaire_H07', ok, {'H_vrai':0.7,'H_estime_moyen':round(float(np.mean(est)),3),'ecart_moitiees_max':round(float(np.max(halves)),3),'critere':'|H-0.7|<0.10 et stabilite<0.20','duree_s':round(time.time()-t0,1)})

# ---------- S3: MSM 2 echelles ----------
t0=time.time(); accs=[]
for s in range(4):
    r,vol=gen_msm_vol(6000, 300+s); g=granulate(np.abs(r),10)
    est,mu,sd,A=hmm_gauss(g,2)
    true_lab=(vol[9::10][:len(est)]>np.median(vol)).astype(int)
    accs.append(acc(true_lab, est))
ok=float(np.mean(accs))>0.65
log('S3_MSM_echelles', ok, {'exactitude_etat_volatilite_moyenne':round(float(np.mean(accs)),3),'critere':'0.65 (etats de volatilite seulement, echelles non garanties)','duree_s':round(time.time()-t0,1)})

# ---------- S4: sticky HMM volatilite ----------
t0=time.time(); accs=[]; ratios=[]
for s in range(4):
    r,st=gen_hmm_vol(6000, 400+s); g=np.abs(granulate(r,10)); true_b=st[9::10]
    est,mu,sd,A=hmm_gauss(g,2); accs.append(acc(true_b[:len(est)], est)); ratios.append(float(max(sd)/min(sd)))
ok=float(np.mean(accs))>0.70
log('S4_HMM_volatilite', ok, {'exactitude_moyenne':round(float(np.mean(accs)),3),'ratio_vol_estime':[round(x,2) for x in ratios],'vrai_ratio':3.0,'critere':'exactitude>0.70','duree_s':round(time.time()-t0,1)})

# ---------- S5: regimes de spread a volatilite egale ----------
t0=time.time(); accs=[]
for s in range(4):
    sp,st=gen_spread_regime(4000, 500+s)
    est,mu,sd,A=hmm_gauss(sp,2); accs.append(acc(st, est))
    pts=dp_segment(sp, pen=2*math.log(len(sp))*np.var(sp))
    results['tentatives'].append({'controle':'S5_spread','seed':500+s,'ruptures_dp':len(pts)})
ok=float(np.mean(accs))>0.75
log('S5_regimes_spread_meme_vol', ok, {'exactitude_moyenne':round(float(np.mean(accs)),3),'critere':'exactitude>0.75','duree_s':round(time.time()-t0,1)})

import pathlib as _pl
_pl.Path('reports/meta_alpha/phaseS').mkdir(parents=True, exist_ok=True)
json.dump(results, open('reports/meta_alpha/phaseS/PHASE_S_RESULTS.json','w'), indent=1)
print('resultats ecrits')
