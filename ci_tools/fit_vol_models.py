import csv, json, numpy as np, pathlib, datetime as dt
rows=list(csv.DictReader(open('reports/meta_alpha/vol_models/DAILY_VOL.csv')))
agg={}
for r in rows:
    a=agg.setdefault(r['date'], {'rv':0.0,'retprod':1.0,'n':0})
    a['rv']+=float(r['rv']); a['retprod']*=(1+float(r['ret_day'])); a['n']+=int(float(r['n']))
dates=sorted(agg)
ret=np.array([agg[d]['retprod']-1 for d in dates]); rv=np.array([agg[d]['rv'] for d in dates])
print('jours calendaires:', len(dates), dates[0], dates[-1], 'RV mediane:', float(np.median(rv)))
np.savez('/tmp/daily.npz', dates=np.array(dates), ret=ret, rv=rv)

def qlike(f, y): 
    f=np.maximum(f,1e-14); return np.log(f)+y/f

def arfima_forecast(y, d, mu, horizon_idx):
    # y: logRV observe jusqu'a t inclus; coefficients pi de (1-L)^d
    maxlag=300
    pi=np.zeros(maxlag+1); pi[0]=1.0
    for j in range(1,maxlag+1): pi[j]=pi[j-1]*(j-1-d)/j
    out=[]
    hist=list(y)
    for _ in horizon_idx:
        vals=np.array(hist[-1:-maxlag-1:-1]) if len(hist)>=1 else np.array([])
        k=len(vals)
        pred=mu - np.sum(pi[1:k+1]*(vals-mu))
        out.append(pred); hist.append(pred)
    return np.array(out)

def run_perimeter(name, mask_dates):
    idx=[i for i,d in enumerate(dates) if mask_dates(d)]
    r_=ret[idx]; v_=rv[idx]; logv=np.log(np.maximum(v_,1e-14))
    n=len(r_); blocks=np.array_split(np.arange(n),5)
    # evaluation a partir du bloc 2 (entrainement = tout avant le bloc), blocs 1..5 avec train>=200 sinon bloc ignore si train<200
    from arch import arch_model
    losses={m:[] for m in ['GARCH_N','GARCH_T','FIGARCH','ARFIMA_LOGVOL','SV_AR1_LOGVOL','NAIF']}
    block_wins={m:0 for m in losses}; nb=0
    details=[]
    for bi,b in enumerate(blocks):
        if b[0]<200: continue
        nb+=1; tr=np.arange(0,b[0])
        # --- GARCH/FIGARCH: params figes a l'origine, previsions 1-pas roulantes
        fc={}
        for label, vol, dist in [('GARCH_N','Garch','normal'),('GARCH_T','Garch','t'),('FIGARCH','FIGARCH','normal')]:
            try:
                am=arch_model(r_[tr]*100, vol=vol, p=1, q=1, dist=dist, rescale=False)
                res=am.fit(disp='off')
                params=res.params.values
                fvars=[]
                fixed=arch_model(r_*100, vol=vol, p=1, q=1, dist=dist, rescale=False)
                for t in b:
                    fx=fixed.fix(params, first_obs=0, last_obs=int(t))
                    fvars.append(float(fx.forecast(horizon=1, reindex=False).variance.values[-1,-1])/10000.0)
                fc[label]=np.array(fvars)
            except Exception as e:
                fc[label]=np.full(len(b), np.nan); print(name,label,'ECHEC',str(e)[:100])
        # ARFIMA d estime sur train (grille, vraisemblance gaussienne via covariance de Toeplitz tronquee: approximation spectrale simple par regression log-periodogramme GPH)
        ytr=logv[tr]
        # estimateur GPH
        m_gph=int(len(ytr)**0.5); freq=np.arange(1,m_gph+1)*2*np.pi/len(ytr)
        per=np.abs(np.fft.rfft(ytr-ytr.mean()))[1:m_gph+1]**2/len(ytr)
        X=np.log(4*np.sin(freq/2)**2); 
        d_est=float(np.clip(-0.5*np.polyfit(X, np.log(per+1e-300),1)[0],0,0.95))
        preds=arfima_forecast(list(ytr), d_est, float(ytr.mean()), range(len(b)))
        fc['ARFIMA_LOGVOL']=np.exp(preds)  # biais log non corrige (documente, identique pour tous les blocs)
        # SV AR1
        x=ytr[:-1]; yy=ytr[1:]; A=np.vstack([np.ones_like(x),x]).T
        coef, *_ = np.linalg.lstsq(A, yy, rcond=None)
        resid=yy-A@coef; s2=float(np.var(resid))
        hist=list(ytr); fsv=[]
        for t in b:
            fsv.append(float(np.exp(coef[0]+coef[1]*hist[-1]+s2/2))); hist.append(float(np.log(max(fsv[-1],1e-14))))
        fc['SV_AR1_LOGVOL']=np.array(fsv)
        fc['NAIF']=np.full(len(b), float(np.mean(v_[tr])))
        bloc_losses={}
        for m in losses:
            L=qlike(fc[m], v_[b]); losses[m].extend(L.tolist()); bloc_losses[m]=float(np.nanmean(L))
        win=min(bloc_losses, key=bloc_losses.get); block_wins[win]+=1
        details.append({'bloc':bi+1,'jours':len(b),'d_ARFIMA':round(d_est,3),'pertes':{k:round(v,4) for k,v in bloc_losses.items()},'gagnant':win})
        print(name, 'bloc', bi+1, {k:round(v,3) for k,v in bloc_losses.items()}, '->', win, flush=True)
    mean={m:float(np.nanmean(losses[m])) for m in losses}
    best=min(mean, key=mean.get)
    verdict = best if block_wins[best]>=4 else 'NON DEPARTAGE'
    return {'perimetre':name,'jours':n,'blocs_evalues':nb,'perte_QLIKE_moyenne':{k:round(v,4) for k,v in mean.items()},'blocs_gagnes':block_wins,'verdict_protocole':verdict,'details':details,
            'losses_journalieres':{m:losses[m] for m in losses}}

out={}
out['IS_COMPLET']=run_perimeter('IS_COMPLET', lambda d: True)
out['ANCIEN_REGIME']=run_perimeter('ANCIEN_REGIME', lambda d: d < '2012-10-01')
out['REGIME_RECENT']=run_perimeter('REGIME_RECENT', lambda d: d >= '2012-10-01')
# bootstrap blocs mensuels sur differences de perte (IS complet), graine 11
rng=np.random.default_rng(11)
L=out['IS_COMPLET'].pop('losses_journalieres')
for o in out.values(): o.pop('losses_journalieres', None)
import itertools
pairs={}
arr={m:np.array(v) for m,v in L.items()}
months=np.array([d[:7] for d in dates])
# aligner: les pertes IS complet correspondent aux jours evalues dans l'ordre des blocs; reconstruire l'alignement mois via blocs
# simplification documentee: bootstrap par blocs de 21 jours ouvres consecutifs sur la sequence des pertes
def boot_ci(diff):
    n=len(diff); bs=21; reps=1000; stats=[]
    starts=np.arange(0,n-bs)
    for _ in range(reps):
        s=rng.choice(starts, size=int(np.ceil(n/bs)))
        sample=np.concatenate([diff[i:i+bs] for i in s])[:n]
        stats.append(np.mean(sample))
    return [round(float(np.percentile(stats,2.5)),4), round(float(np.percentile(stats,97.5)),4)]
for a,b in itertools.combinations(L.keys(),2):
    d=arr[a]-arr[b]
    pairs[f'{a} vs {b}']={'diff_moyenne':round(float(np.mean(d)),4),'IC95_bootstrap_blocs21j':boot_ci(d)}
out['IS_COMPLET']['comparaisons_paires_bootstrap'] = pairs
pathlib.Path('reports/meta_alpha/vol_models/VOL_MODELS_RESULTS.json').write_text(json.dumps(out,indent=1))
for k,v in out.items(): print(k, v['perte_QLIKE_moyenne'], 'verdict:', v['verdict_protocole'])
