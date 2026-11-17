import csv, json, numpy as np, pathlib
rows=list(csv.DictReader(open('reports/meta_alpha/vol_hourly/PARTITION_HOUR_TS.csv')))
seen={}
for r in rows: seen[(r['partition'],r['hour_ts'])]=r
agg={}
for r in seen.values():
    a=agg.setdefault(r['hour_ts'], {'ss':0.0,'rp':1.0,'sp':0.0,'n':0})
    a['ss']+=float(r['sumsq_rbp']); a['rp']*=(1+float(r['ret_hour'])); a['n']+=int(float(r['n'])); a['sp']+=float(r['spread_bp'])*float(r['n'])
ts=sorted(agg)
ret=np.array([agg[t]['rp']-1 for t in ts]); rv=np.array([agg[t]['ss'] for t in ts])/1e8
spread=np.array([agg[t]['sp']/agg[t]['n'] for t in ts]); hours=np.array([int(t[11:13]) for t in ts])
print('heures calendaires:', len(ts), ts[0], '->', ts[-1], 'RV horaire mediane (bp2):', float(np.median(rv))*1e4)
np.savez('/tmp/hourly.npz', ts=np.array(ts), ret=ret, rv=rv, spread=spread, hours=hours)

def qlike(f,y):
    f=np.maximum(f,1e-16); return np.log(f)+y/f
def arfima_fc(y, d, mu, steps):
    maxlag=300; pi=np.zeros(maxlag+1); pi[0]=1.0
    for j in range(1,maxlag+1): pi[j]=pi[j-1]*(j-1-d)/j
    hist=list(y); out=[]
    for _ in range(steps):
        k=min(maxlag,len(hist)); vals=np.array(hist[-1:-k-1:-1])
        out.append(mu-np.sum(pi[1:k+1]*(vals-mu))); hist.append(out[-1])
    return np.array(out)
def gph_d(y):
    m=int(len(y)**0.5); fr=np.arange(1,m+1)*2*np.pi/len(y)
    per=np.abs(np.fft.rfft(y-y.mean()))[1:m+1]**2/len(y)
    return float(np.clip(-0.5*np.polyfit(np.log(4*np.sin(fr/2)**2), np.log(per+1e-300),1)[0],0,0.95))

def run(name, sel):
    idx=np.where(sel)[0]
    r_=ret[idx]; v_=rv[idx]; h_=hours[idx]; sp_=spread[idx]
    logv=np.log(np.maximum(v_,1e-16))
    n=len(r_); blocks=np.array_split(np.arange(n),5)
    from arch import arch_model
    losses={m:[] for m in ['GARCH_N','GARCH_T','FIGARCH','ARFIMA_LOGVOL','SV_AR1_LOGVOL','NAIF']}
    wins={m:0 for m in losses}; dets=[]
    for bi,b in enumerate(blocks):
        if b[0]<500: continue
        tr=np.arange(0,b[0])
        fac=np.ones(24)
        med_all=np.median(v_[tr])
        for hh in range(24):
            msk=h_[tr]==hh
            fac[hh]=(np.median(v_[tr][msk])/med_all) if msk.sum()>10 else 1.0
        vds=v_/fac[h_]; logds=np.log(np.maximum(vds,1e-16))
        fc={}
        for label, vol, dist in [('GARCH_N','Garch','normal'),('GARCH_T','Garch','t'),('FIGARCH','FIGARCH','normal')]:
            try:
                am=arch_model(r_[tr]*100, vol=vol, p=1, q=1, dist=dist, rescale=False)
                res=am.fit(disp='off'); params=res.params.values
                model=arch_model(r_*100, vol=vol, p=1, q=1, dist=dist, rescale=False)
                fv=np.full(len(b), np.nan)
                # previsions par paquets de 24h depuis chaque origine journaliere
                starts=list(range(0,len(b),24))
                for s in starts:
                    t0=int(b[s]); horizon=min(24, int(b[-1])-t0+1)
                    fx=model.fix(params, first_obs=0, last_obs=t0)
                    path=fx.forecast(horizon=horizon, reindex=False).variance.values[-1]/10000.0
                    pos=np.where((b>=t0)&(b<t0+horizon))[0]
                    fv[pos]=path[:len(pos)]
                fc[label]=fv*fac[h_[b]]
            except Exception as e:
                fc[label]=np.full(len(b), np.nan); print(name,label,'ECHEC',str(e)[:100], flush=True)
        d_est=gph_d(logds[tr])
        fc['ARFIMA_LOGVOL']=np.exp(arfima_fc(list(logds[tr]), d_est, float(np.mean(logds[tr])), len(b)))*fac[h_[b]]
        ytr=logds[tr]; A=np.vstack([np.ones(len(ytr)-1), ytr[:-1]]).T
        coef,*_=np.linalg.lstsq(A, ytr[1:], rcond=None); s2=float(np.var(ytr[1:]-A@coef))
        hist=list(ytr); fsv=[]
        for t in b:
            fsv.append(float(np.exp(coef[0]+coef[1]*hist[-1]+s2/2))); hist.append(float(np.log(max(fsv[-1],1e-16))))
        fc['SV_AR1_LOGVOL']=np.array(fsv)*fac[h_[b]]
        fc['NAIF']=np.full(len(b), float(np.mean(v_[tr])))
        bl={}
        for m in losses:
            L=qlike(fc[m], v_[b]); losses[m].extend(L.tolist()); bl[m]=float(np.nanmean(L))
        w=min(bl,key=bl.get); wins[w]+=1; dets.append({'bloc':bi+1,'d':round(d_est,3),'pertes':{k:round(v,4) for k,v in bl.items()},'gagnant':w})
        print(name,'bloc',bi+1,{k:round(v,3) for k,v in bl.items()},'->',w, flush=True)
    mean={m:float(np.nanmean(losses[m])) for m in losses}; best=min(mean,key=mean.get)
    return {'perimetre':name,'heures':int(n),'perte_QLIKE':{k:round(v,4) for k,v in mean.items()},'blocs_gagnes':wins,'verdict':'NON DEPARTAGE' if wins[best]<4 else best,'details':dets}
out={}
out['IS_COMPLET']=run('IS_COMPLET_HORAIRE', np.ones(len(ts),bool))
out['REGIME_RECENT']=run('REGIME_RECENT_HORAIRE', np.array([t>='2012-10-01' for t in ts]))
# couplage spread (descriptif, serie complete)
def cc(a,b,k):
    if k<0: return float(np.corrcoef(a[-k:], b[:k])[0,1])
    if k>0: return float(np.corrcoef(a[:-k], b[k:])[0,1])
    return float(np.corrcoef(a,b)[0,1])
logrv=np.log(np.maximum(rv,1e-16))
out['couplage_spread']={
 'corr_contemporaine_logRV_spread': round(cc(logrv, spread,0),4),
 'cross_corr_logRV_vers_spread_lags_-5..+5': {str(k): round(cc(logrv, spread,k),4) for k in range(-5,6)},
 'ancien_avant_2012_10': round(cc(logrv[np.array([t<'2012-10-01' for t in ts])], spread[np.array([t<'2012-10-01' for t in ts])],0),4),
 'recent_apres_2012_10': round(cc(logrv[np.array([t>='2012-10-01' for t in ts])], spread[np.array([t>='2012-10-01' for t in ts])],0),4)}
pathlib.Path('reports/meta_alpha/vol_hourly/VOL_HOURLY_RESULTS.json').write_text(json.dumps(out,indent=1))
for k,v in out.items():
    if isinstance(v,dict) and 'perte_QLIKE' in v: print(k, v['perte_QLIKE'], v['verdict'])
print('couplage:', out['couplage_spread'])
