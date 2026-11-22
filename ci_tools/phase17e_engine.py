# -*- coding: utf-8 -*-
"""Phase 17-E : entrainement M2R_B08/M2R_B09 selon preenregistrement 17-D gele.
Sources: artefacts committes 17-B uniquement. OLS sans regularisation, variables
brutes + intercept + sessions one-hot (ASIA reference), convention 17-B."""
import json, pathlib
import numpy as np, pandas as pd
R = pathlib.Path('reports/meta_alpha/phase17')
VARS = ['RATIO_REPLI_EXTENSION_A_TREINT','DUREE_EXTREME_VERS_TREINT_MIN','MFE_A_TREINT_BP',
        'NB_TOUCHES_P0_AVANT_TREINT','ATR14_H1','SPREAD_DECISION_BP']
SESSIONS = ['LONDON','LONDON_NY_OVERLAP','NY_AFTERNOON','NIGHT_OTHER']  # ASIA = reference
COLS = ['INTERCEPT']+VARS+[f'SESSION_REINTEGRATION={s}' for s in SESSIONS]
K = {'B08':1.0,'B09':1.5}

def design(fea):
    X = pd.DataFrame({'INTERCEPT':1.0}, index=fea.index)
    for v in VARS: X[v]=fea[v].astype(float)
    for s in SESSIONS: X[f'SESSION_REINTEGRATION={s}']=(fea.SESSION_REINTEGRATION==s).astype(float)
    return X[COLS]

def metriques(y, pred):
    e = pred-y
    return dict(n=int(len(y)), MAE=float(np.abs(e).mean()), RMSE=float(np.sqrt((e**2).mean())),
                erreur_moyenne=float(e.mean()), biais=float(e.mean()),
                residu_q25=float(np.quantile(e,.25)), residu_mediane=float(np.median(e)), residu_q75=float(np.quantile(e,.75)))

def calibration(y, pred):
    if np.std(pred)==0: return dict(intercept=None,pente=None)
    A=np.column_stack([np.ones_like(pred),pred]); c,*_=np.linalg.lstsq(A,y,rcond=None)
    return dict(intercept=float(c[0]),pente=float(c[1]))

def stats_R(s):
    s=pd.Series(s)
    return dict(n=int(len(s)), moyenne=float(s.mean()), mediane=float(s.median()),
        P1=float(s.quantile(.01)),P5=float(s.quantile(.05)),P25=float(s.quantile(.25)),
        P75=float(s.quantile(.75)),P95=float(s.quantile(.95)),P99=float(s.quantile(.99)),
        perte_extreme=float(s.min()), part_positifs=float((s>0).mean()))

def main():
    resultats={}
    eval_rows=[]; dec_rows=[]
    for contrat in ['B08','B09']:
        lab=pd.read_csv(R/f'PHASE17B_LABELS_{contrat}.csv')
        fea=pd.read_csv(R/f'PHASE17B_FEATURES_{contrat}.csv')
        j=lab.merge(fea[['event_id']+VARS+['SESSION_REINTEGRATION']],on='event_id',validate='one_to_one')
        j['INITIAL_RISK_BP']=K[contrat]*j.ATR14_H1/j.prix_entree*10000
        j['R_REALIZED_S2']=j.PL_S2_bp/j.INITIAL_RISK_BP
        et=j[j.statut_label=='ETIQUETE'].copy()
        # livrable cibles (toutes observations, exclus documentes)
        j.assign(contrat=contrat)[['event_id','grappe_id','ensemble','direction','mecanisme','statut_label','statut_entree',
            'prix_entree','prix_sortie','ATR14_H1','INITIAL_RISK_BP','PL_S0_bp','PL_S1_bp','PL_S2_bp','R_REALIZED_S2']]\
            .to_csv(R/f'PHASE17E_TARGETS_{contrat}.csv',index=False)
        appr=et[et.ensemble=='APPRENTISSAGE']
        X=design(et); y=et.R_REALIZED_S2.values
        Xa=X[et.ensemble.values=='APPRENTISSAGE'].values; ya=appr.R_REALIZED_S2.values
        beta,*_=np.linalg.lstsq(Xa,ya,rcond=None)
        M0=float(ya.mean())
        et=et.assign(pred_M2R=X.values@beta, pred_M0R=M0)
        # livrable predictions (etiquetes uniquement)
        et[['event_id','grappe_id','ensemble','R_REALIZED_S2','PL_S2_bp','pred_M2R','pred_M0R','mecanisme']]\
            .to_csv(R/f'PHASE17E_PREDICTIONS_{contrat}.csv',index=False)
        params=dict(mnle_modele=f'M2R_{contrat}', methode='regression lineaire OLS (numpy.linalg.lstsq, rcond=None), aucune regularisation, aucune selection',
            ordre_variables=COLS, intercept=float(beta[0]),
            coefficients={c:float(b) for c,b in zip(COLS[1:],beta[1:])},
            M0_R=dict(valeur=M0, n_apprentissage=int(len(appr)), mediane_R=float(appr.R_REALIZED_S2.median()),
                      ecart_type_R=float(appr.R_REALIZED_S2.std()), formule='moyenne de R_REALIZED_S2 sur apprentissage uniquement'),
            cible='R_REALIZED_S2', etiquette='NET_OF_SPREAD_AND_HYPOTHETICAL_S2_SLIPPAGE_BEFORE_COMMISSION',
            k_risque=K[contrat], segment_estimation='APPRENTISSAGE 2010-2015 uniquement')
        (R/f'PHASE17E_M2R_{contrat}_PARAMETERS.json').write_text(json.dumps(params,indent=1,ensure_ascii=False))
        resultats[contrat]=dict(M0_R=M0, n={e:int((et.ensemble==e).sum()) for e in ['APPRENTISSAGE','CALIBRATION','EVALUATION']},
                                segments={})
        for ens,g in et.groupby('ensemble'):
            m2=metriques(g.R_REALIZED_S2.values,g.pred_M2R.values); m0=metriques(g.R_REALIZED_S2.values,g.pred_M0R.values)
            ret=g[g.pred_M2R>0]; ret_gr=ret.groupby('grappe_id').R_REALIZED_S2.mean()
            toutes_gr=g.groupby('grappe_id').R_REALIZED_S2.mean()
            eval_rows.append(dict(contrat=contrat,ensemble=ens,MAE_M0R=m0['MAE'],MAE_M2R=m2['MAE'],RMSE_M0R=m0['RMSE'],RMSE_M2R=m2['RMSE'],
                erreur_moyenne_M2R=m2['erreur_moyenne'],calibration=json.dumps(calibration(g.R_REALIZED_S2.values,g.pred_M2R.values)),
                n_grappes=int(g.grappe_id.nunique()),R_moyen_grappes=float(toutes_gr.mean())))
            d=dict(contrat=contrat,ensemble=ens,regle='PREDICTED_EXPECTED_R > 0',n_evalue=int(len(g)),
                 n_retenues=int(len(ret)),couverture=float(len(ret)/len(g)),
                 decision_M0R='AUCUNE_EXPOSITION' if M0<=0 else 'TOUT_EXPOSER',**{f'retenues_{k}':v for k,v in stats_R(ret.R_REALIZED_S2).items() if k!='n'},
                 retenues_moyenne_grappes=float(ret_gr.mean()) if len(ret_gr) else None,
                 retenues_PL_S2_moyen_bp=float(ret.PL_S2_bp.mean()) if len(ret) else None)
            dec_rows.append(d); resultats[contrat]['segments'][ens]=dict(M2R=m2,M0R=m0,decisions=d,
                calibration=calibration(g.R_REALIZED_S2.values,g.pred_M2R.values))
    pd.DataFrame(eval_rows).to_csv(R/'PHASE17E_MODEL_EVALUATION.csv',index=False)
    pd.DataFrame(dec_rows).to_csv(R/'PHASE17E_ECONOMIC_DECISIONS.csv',index=False)
    (R/'_phase17e_resultats.json').write_text(json.dumps(resultats,indent=1,ensure_ascii=False))
    print(json.dumps(resultats,indent=1))

if __name__=='__main__': main()
