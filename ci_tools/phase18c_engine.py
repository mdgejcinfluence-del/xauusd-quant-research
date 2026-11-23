# -*- coding: utf-8 -*-
"""Phase 18-C: valeur incrementale des six nouvelles variables.
BASE_7 (OLS 17-E reproduit) vs EXT_13 (7+6), population commune complete-case,
M0_R gele 17-E. Aucune imputation, aucun tick, aucun nouveau seuil."""
import json, pathlib
import numpy as np, pandas as pd
R17 = pathlib.Path('reports/meta_alpha/phase17'); R18 = pathlib.Path('reports/meta_alpha/phase18')
ANC = ['RATIO_REPLI_EXTENSION_A_TREINT','DUREE_EXTREME_VERS_TREINT_MIN','MFE_A_TREINT_BP','NB_TOUCHES_P0_AVANT_TREINT','ATR14_H1','SPREAD_DECISION_BP']
NOUV = ['QUOTE_UPDATE_RATE_5M','MAX_QUOTE_GAP_15M','SPREAD_TREND_5M','RV_MID_30M','PATH_EFFICIENCY_60M','REVERSAL_COUNT_60M']
SESSIONS = ['LONDON','LONDON_NY_OVERLAP','NY_AFTERNOON','NIGHT_OTHER']

def design(df, vars_num):
    X = pd.DataFrame({'INTERCEPT':1.0}, index=df.index)
    for v in vars_num: X[v]=df[v].astype(float)
    for s in SESSIONS: X[f'SESSION_REINTEGRATION={s}']=(df.SESSION_REINTEGRATION==s).astype(float)
    return X

def ols(X,y):
    b,*_ = np.linalg.lstsq(X.values,y.values,rcond=None); return b

def vif(X):
    cols=[c for c in X.columns if c!='INTERCEPT']; out={}
    for c in cols:
        autres=[a for a in cols if a!=c]
        A=np.column_stack([np.ones(len(X))]+[X[a].values for a in autres])
        b,*_=np.linalg.lstsq(A,X[c].values,rcond=None); pred=A@b
        ss=1-((X[c].values-pred)**2).sum()/((X[c].values-X[c].values.mean())**2).sum()
        out[c]=float(1/(1-ss)) if ss<1 else float('inf')
    return out

def met(y,p):
    e=p-y; A=np.column_stack([np.ones_like(p),p]); c,*_=np.linalg.lstsq(A,y,rcond=None)
    return dict(n=int(len(y)),MAE=float(np.abs(e).mean()),RMSE=float(np.sqrt((e**2).mean())),
                erreur_moyenne=float(e.mean()),calibration_intercept=float(c[0]),calibration_pente=float(c[1]),
                pred_min=float(p.min()),pred_q25=float(np.quantile(p,.25)),pred_mediane=float(np.median(p)),
                pred_q75=float(np.quantile(p,.75)),pred_max=float(p.max()),
                realise_moyenne=float(y.mean()),realise_mediane=float(np.median(y)))

def main():
    new = pd.read_parquet(R18/'PHASE18B_CAUSAL_FEATURES.parquet')
    preds=[]; metrics=[]; coefs=[]; sel=[]; registry={}; cohort=[]; repro={}
    for contrat in ['B08','B09']:
        fea = pd.read_csv(R17/f'PHASE17B_FEATURES_{contrat}.csv')
        tgt = pd.read_csv(R17/f'PHASE17E_TARGETS_{contrat}.csv')
        par17 = json.loads((R17/f'PHASE17E_M2R_{contrat}_PARAMETERS.json').read_text())
        M0 = par17['M0_R']['valeur']
        j = tgt.merge(fea[['event_id','SESSION_REINTEGRATION']+[a for a in ANC if a!='ATR14_H1']], on='event_id').merge(new, on=['event_id','grappe_id','ensemble'], suffixes=('','_n'))
        et = j[j.statut_label=='ETIQUETE'].copy()
        # reproduction 17-E: BASE sur cohorte 17-E complete (etiquetes, features anciennes completes)
        et17 = et.dropna(subset=ANC)
        X17 = design(et17, ANC); tr17 = et17.ensemble=='APPRENTISSAGE'
        b17 = ols(X17[tr17], et17[tr17].R_REALIZED_S2)
        ref = np.array([par17['intercept']]+[par17['coefficients'][c] for c in X17.columns[1:]])
        repro[contrat] = float(np.abs(b17-ref).max())
        # population commune complete-case
        cc = et.dropna(subset=ANC+NOUV).copy()
        for ens in ['APPRENTISSAGE','CALIBRATION','EVALUATION']:
            cohort.append(dict(contrat=contrat,ensemble=ens,
                n_etiquetes=int((et.ensemble==ens).sum()), n_commune=int((cc.ensemble==ens).sum()),
                exclus=int((et.ensemble==ens).sum()-(cc.ensemble==ens).sum()),
                cause_exclusion='au moins une des 13 variables manquante (fenetre NON_VALIDABLE 18-B, aucune imputation)'))
        tr = cc.ensemble=='APPRENTISSAGE'
        modeles={}
        for nom, vnum in [('BASE_7',ANC),('EXT_13',ANC+NOUV)]:
            X = design(cc, vnum); b = ols(X[tr], cc[tr].R_REALIZED_S2)
            modeles[nom]=(X,b)
            registry[f'M2R_{nom}_{contrat}']=dict(methode='OLS numpy.linalg.lstsq rcond=None, sans regularisation ni selection',
                variables=list(X.columns), n_apprentissage=int(tr.sum()), M0_R_gele_17E=M0)
            for c,val in zip(X.columns,b): coefs.append(dict(contrat=contrat,modele=nom,variable=c,coefficient=float(val)))
            if nom=='EXT_13': registry[f'M2R_{nom}_{contrat}']['VIF']=vif(X[tr])
            cc[f'pred_{nom}']=X.values@b
        cc['pred_M0R']=M0
        for ens,g in cc.groupby('ensemble'):
            for nom in ['M0R','BASE_7','EXT_13']:
                p = g[f'pred_{nom}'].values if nom!='M0R' else np.full(len(g),M0)
                metrics.append(dict(contrat=contrat,ensemble=ens,modele=nom,**met(g.R_REALIZED_S2.values,p)))
            for nom in ['BASE_7','EXT_13']:
                ret=g[g[f'pred_{nom}']>0]; rg=ret.groupby('grappe_id').R_REALIZED_S2.mean()
                sel.append(dict(contrat=contrat,ensemble=ens,modele=nom,n_evalue=int(len(g)),n_retenus=int(len(ret)),
                    couverture=float(len(ret)/len(g)),R_moyen_retenus=float(ret.R_REALIZED_S2.mean()) if len(ret) else None,
                    R_mediane_retenus=float(ret.R_REALIZED_S2.median()) if len(ret) else None,
                    part_positifs_retenus=float((ret.R_REALIZED_S2>0).mean()) if len(ret) else None,
                    R_moyen_grappes_retenus=float(rg.mean()) if len(rg) else None,
                    part_top3_evenements_abs=float(ret.R_REALIZED_S2.abs().sort_values(ascending=False).head(3).sum()/ret.R_REALIZED_S2.abs().sum()) if len(ret) else None,
                    PL_S2_moyen_retenus_bp=float(ret.PL_S2_bp.mean()) if len(ret) else None))
        preds.append(cc[['event_id','grappe_id','ensemble','R_REALIZED_S2','PL_S2_bp','pred_M0R','pred_BASE_7','pred_EXT_13']].assign(contrat=contrat))
    pd.DataFrame(cohort).to_csv(R18/'PHASE18C_COHORT_RECONCILIATION.csv',index=False)
    pd.DataFrame(coefs).to_csv(R18/'PHASE18C_COEFFICIENTS.csv',index=False)
    pd.concat(preds).to_parquet(R18/'PHASE18C_EVENT_PREDICTIONS.parquet',index=False)
    pd.DataFrame(metrics).to_csv(R18/'PHASE18C_METRICS_COMPARISON.csv',index=False)
    pd.DataFrame(sel).to_csv(R18/'PHASE18C_ECONOMIC_SELECTION.csv',index=False)
    registry['reproduction_17E_ecart_max_coefficients']=repro
    registry['M0_R']=dict(B08=json.loads((R17/'PHASE17E_M2R_B08_PARAMETERS.json').read_text())['M0_R'],
                          B09=json.loads((R17/'PHASE17E_M2R_B09_PARAMETERS.json').read_text())['M0_R'],
                          note='valeur gelee 17-E conservee; predictions evaluees sur la population commune')
    (R18/'PHASE18C_MODEL_REGISTRY.json').write_text(json.dumps(registry,indent=1,ensure_ascii=False))
    print('repro ecart max:', repro)

if __name__=='__main__': main()
