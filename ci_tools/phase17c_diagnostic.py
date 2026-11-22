# -*- coding: utf-8 -*-
"""Phase 17-C : diagnostic sur artefacts committes 17-A/17-B uniquement.
Aucun tick, aucun nouveau label, aucun entrainement. q_M2 restitue par
application deterministe des parametres GELES aux features committies,
valide contre PHASE17B_ECONOMIC_DECISIONS.csv (evaluation)."""
import json, pathlib
import numpy as np, pandas as pd
R = pathlib.Path('reports/meta_alpha/phase17')
OUT = R
def q_stats(s):
    s = pd.Series(s).dropna()
    if len(s)==0: return dict(n=0)
    return dict(n=int(len(s)), moyenne=float(s.mean()), mediane=float(s.median()),
        ecart_type=float(s.std(ddof=1)) if len(s)>1 else 0.0,
        q10=float(s.quantile(.10)), q25=float(s.quantile(.25)),
        q75=float(s.quantile(.75)), q90=float(s.quantile(.90)),
        minimum=float(s.min()), maximum=float(s.max()), somme=float(s.sum()))

def charger(contrat):
    lab = pd.read_csv(R/f'PHASE17B_LABELS_{contrat}.csv')
    fea = pd.read_csv(R/f'PHASE17B_FEATURES_{contrat}.csv')
    par = json.loads((R/f'PHASE17B_M2_{contrat}_PARAMETERS.json').read_text())
    return lab, fea, par

def appliquer_modele(fea, par):
    """Application deterministe du modele gele (aucun ajustement)."""
    X = pd.DataFrame({'INTERCEPT':1.0}, index=fea.index)
    for v in ['RATIO_REPLI_EXTENSION_A_TREINT','DUREE_EXTREME_VERS_TREINT_MIN',
              'MFE_A_TREINT_BP','NB_TOUCHES_P0_AVANT_TREINT','ATR14_H1','SPREAD_DECISION_BP']:
        # normalisation identique a phase17b : colonnes deja au format du fichier features?
        X[v]=fea[v].astype(float)
    for niv in ['LONDON','LONDON_NY_OVERLAP','NY_AFTERNOON','NIGHT_OTHER']:
        X[f'SESSION_REINTEGRATION={niv}']=(fea['SESSION_REINTEGRATION']==niv).astype(float)
    mu, sd = par.get('normalisation',{}).get('moyennes',{}), par.get('normalisation',{}).get('ecarts_types',{})
    eta = np.full(len(fea), par['intercept'], dtype=float)
    for v,c in par['coefficients'].items():
        col = X[v].astype(float)
        if v in mu: col=(col-mu[v])/sd[v]
        eta = eta + c*col.values
    return 1/(1+np.exp(-eta))

def main():
    dec = pd.read_csv(R/'PHASE17B_ECONOMIC_DECISIONS.csv')
    res17b = json.loads((R/'PHASE17B_RESULTS.json').read_text())
    audit = json.loads((R/'PHASE17B_LABEL_AUDIT.json').read_text())
    validation_q, contrats = {}, {}
    for contrat in ['B08','B09']:
        lab, fea, par = charger(contrat)
        # features B08/B09 identiques ?
        q = appliquer_modele(fea, par)
        fea = fea.assign(q_M2=q)
        m = fea.merge(dec[dec.contrat==contrat][['event_id','q_M2']], on='event_id', suffixes=('_restitue','_livre'))
        m = m[m.ensemble=='EVALUATION']
        validation_q[contrat] = dict(n_communs=int(len(m)),
            ecart_max_q=float((m.q_M2_restitue-m.q_M2_livre).abs().max()) if len(m) else None)
        contrats[contrat] = (lab, fea, par)
    # coherence features entre contrats
    f8, f9 = contrats['B08'][1], contrats['B09'][1]
    cols = [c for c in f8.columns if c not in ('q_M2',)]
    memes_features = bool(f8[cols].reset_index(drop=True).equals(f9[cols].reset_index(drop=True)))

    # ---------- 1. Decomposition des issues ----------
    rows=[]
    for contrat,(lab,fea,par) in contrats.items():
        for ens,g in lab.groupby('ensemble'):
            tot_et = g[g.statut_label=='ETIQUETE']; total_pl = tot_et.PL_S2_bp.sum()
            cats = g.mecanisme.fillna('SANS_MECANISME').where(g.statut_label!='NON_EXECUTION','NON_EXECUTION')
            for cat, gc in g.groupby(cats):
                et = gc[gc.statut_label=='ETIQUETE']
                st = q_stats(et.PL_S2_bp) if len(et) else dict(n=0)
                gc_abs = et.groupby('grappe_id').PL_S2_bp.sum().abs().sort_values(ascending=False) if len(et) else pd.Series(dtype=float)
                rows.append(dict(contrat=contrat, ensemble=ens, categorie=cat,
                    n_candidats=int(len(gc)), n_etiquetes=int(len(et)),
                    n_succes=int((et.Y_ECON==1).sum()), n_echecs=int((et.Y_ECON==0).sum()),
                    n_censures=int((gc.statut_label=='CENSORED').sum()),
                    n_non_execution=int((gc.statut_label=='NON_EXECUTION').sum()),
                    **{k:st.get(k) for k in ['moyenne','mediane','ecart_type','q10','q25','q75','q90','minimum','maximum','somme']},
                    contribution_somme_PL=float(st.get('somme',0)/total_pl) if total_pl else None,
                    part_abs_PL=float(et.PL_S2_bp.abs().sum()/tot_et.PL_S2_bp.abs().sum()) if len(tot_et) else None,
                    part_extremes_abs_sup100bp=float((et.PL_S2_bp.abs()>100).mean()) if len(et) else None,
                    nb_grappes=int(et.grappe_id.nunique()),
                    part_top5_grappes_abs=float(gc_abs.head(5).sum()/gc_abs.sum()) if gc_abs.sum() else None))
    pd.DataFrame(rows).to_csv(OUT/'PHASE17C_OUTCOME_DECOMPOSITION.csv', index=False)

    # ---------- 2. Distribution des payoffs ----------
    rows=[]
    for contrat,(lab,fea,par) in contrats.items():
        for ens,g0 in lab.groupby('ensemble'):
            g = g0[g0.statut_label=='ETIQUETE']
            for signe, gs in [('GAIN', g[g.PL_S2_bp>0]), ('PERTE', g[g.PL_S2_bp<0]), ('TOUS', g)]:
                s = gs.PL_S2_bp.abs() if signe!='TOUS' else gs.PL_S2_bp
                st = q_stats(s)
                rows.append(dict(contrat=contrat, ensemble=ens, groupe=signe, **st))
            gains, pertes = g[g.PL_S2_bp>0].PL_S2_bp, -g[g.PL_S2_bp<0].PL_S2_bp
            rows.append(dict(contrat=contrat, ensemble=ens, groupe='RATIO_GAIN_MOY_PERTE_MOY',
                n=int(len(g)), moyenne=float(gains.mean()/pertes.mean()) if len(pertes) and pertes.mean() else None,
                mediane=float(gains.median()/pertes.median()) if len(pertes) and pertes.median() else None))
    pd.DataFrame(rows).to_csv(OUT/'PHASE17C_PAYOFF_DISTRIBUTION.csv', index=False)

    # ---------- 3. Diagnostic calibration M2 (deciles par probabilites seules) ----------
    rows=[]; qdist={}
    for contrat,(lab,fea,par) in contrats.items():
        j = fea[fea.statut_label=='ETIQUETE'].merge(lab[['event_id','PL_S2_bp','mecanisme']], on='event_id')
        for ens,g in j.groupby('ensemble'):
            qd = q_stats(g.q_M2); qdist[f'{contrat}|{ens}'] = qd
            g = g.assign(decile=pd.qcut(g.q_M2, 10, labels=False, duplicates='drop'))
            for d, gd in g.groupby('decile'):
                st=q_stats(gd.PL_S2_bp)
                rows.append(dict(contrat=contrat, ensemble=ens, groupe=f'D{int(d)+1}',
                    n=int(len(gd)), q_min=float(gd.q_M2.min()), q_max=float(gd.q_M2.max()),
                    q_moyen=float(gd.q_M2.mean()), taux_positif_observe=float(gd.Y_ECON.mean()),
                    ecart_calibration=float(gd.Y_ECON.mean()-gd.q_M2.mean()),
                    PL_moyen=st.get('moyenne'), PL_mediane=st.get('mediane'), PL_q25=st.get('q25'), PL_q75=st.get('q75')))
            # retenues/rejetees au seuil gele P_BE
            for nom, gd in [('RETENUES', g[g.q_M2>par['P_BE']]), ('REJETEES', g[g.q_M2<=par['P_BE']])]:
                st=q_stats(gd.PL_S2_bp)
                rows.append(dict(contrat=contrat, ensemble=ens, groupe=nom+'_AU_SEUIL_GELE', n=int(len(gd)),
                    q_moyen=float(gd.q_M2.mean()) if len(gd) else None,
                    taux_positif_observe=float(gd.Y_ECON.mean()) if len(gd) else None,
                    PL_moyen=st.get('moyenne'), PL_mediane=st.get('mediane')))
    pd.DataFrame(rows).to_csv(OUT/'PHASE17C_M2_CALIBRATION_DIAGNOSTIC.csv', index=False)

    # ---------- 4. Audit distributions par segment ----------
    VARS=['RATIO_REPLI_EXTENSION_A_TREINT','DUREE_EXTREME_VERS_TREINT_MIN','MFE_A_TREINT_BP',
          'NB_TOUCHES_P0_AVANT_TREINT','ATR14_H1','SPREAD_DECISION_BP']
    rows=[]
    fea = contrats['B08'][1]; lab8 = contrats['B08'][0]
    ref = fea[fea.ensemble=='APPRENTISSAGE']
    for v in VARS:
        for ens,g in fea.groupby('ensemble'):
            st=q_stats(g[v]); r=ref[v]
            smd = float((g[v].mean()-r.mean())/r.std(ddof=1)) if r.std(ddof=1) else None
            rows.append(dict(variable=v, type='NUMERIQUE', ensemble=ens, SMD_vs_apprentissage=smd, manquants=int(g[v].isna().sum()), **st))
    for niv,g in fea.groupby('SESSION_REINTEGRATION'):
        for ens,ge in g.groupby('ensemble'):
            rows.append(dict(variable=f'SESSION_REINTEGRATION={niv}', type='CATEGORIELLE', ensemble=ens,
                n=int(len(ge)), moyenne=float(len(ge)/len(fea[fea.ensemble==ens]))))
    pd.DataFrame(rows).to_csv(OUT/'PHASE17C_SPLIT_DISTRIBUTION_AUDIT.csv', index=False)

    # ---------- 6. Ponderation par grappe ----------
    rows=[]
    for contrat,(lab,fea,par) in contrats.items():
        for ens,g0 in lab.groupby('ensemble'):
            g=g0[g0.statut_label=='ETIQUETE']
            par_gr = g.groupby('grappe_id').agg(PL=('PL_S2_bp','mean'), Y=('Y_ECON','mean'), n=('PL_S2_bp','size'))
            gains_e, pertes_e = g[g.PL_S2_bp>0].PL_S2_bp.mean(), -g[g.PL_S2_bp<0].PL_S2_bp.mean()
            gg = par_gr.PL[par_gr.PL>0].mean(); ll = -par_gr.PL[par_gr.PL<0].mean()
            rows.append(dict(contrat=contrat, ensemble=ens, n_evenements=int(len(g)), n_grappes=int(len(par_gr)),
                taille_grappe_moy=float(par_gr.n.mean()),
                taux_positif_evenements=float(g.Y_ECON.mean()), taux_positif_grappes=float(par_gr.Y.mean()),
                PL_moyen_evenements=float(g.PL_S2_bp.mean()), PL_moyen_grappes=float(par_gr.PL.mean()),
                G_evenements=float(gains_e), L_evenements=float(pertes_e),
                P_BE_implicite_evenements=float(pertes_e/(gains_e+pertes_e)),
                G_grappes=float(gg), L_grappes=float(ll), P_BE_implicite_grappes=float(ll/(gg+ll)) if gg==gg and ll==ll else None,
                part_top5_grappes_PL_abs=float(g.groupby('grappe_id').PL_S2_bp.sum().abs().sort_values(ascending=False).head(5).sum()/g.groupby('grappe_id').PL_S2_bp.sum().abs().sum())))
    pd.DataFrame(rows).to_csv(OUT/'PHASE17C_CLUSTER_WEIGHTING.csv', index=False)

    # ---------- 8. Perte d'information du label binaire (statistiques) ----------
    info={}
    for contrat,(lab,fea,par) in contrats.items():
        info[contrat]={}
        for ens,g0 in lab.groupby('ensemble'):
            g=g0[g0.statut_label=='ETIQUETE']; pl=g.PL_S2_bp; y=g.Y_ECON
            entre = sum(len(gg)*(gg.PL_S2_bp.mean()-pl.mean())**2 for _,gg in g.groupby(y))
            eta2 = float(entre/ ((pl-pl.mean())**2).sum())
            p1, p0 = g[y==1].PL_S2_bp, g[y==0].PL_S2_bp
            exemples = dict(
                positif_min=dict(event_id=str(g.loc[p1.idxmin(),'event_id']), PL=float(p1.min())),
                positif_max=dict(event_id=str(g.loc[p1.idxmax(),'event_id']), PL=float(p1.max())),
                negatif_min=dict(event_id=str(g.loc[p0.idxmin(),'event_id']), PL=float(p0.min())),
                negatif_max=dict(event_id=str(g.loc[p0.idxmax(),'event_id']), PL=float(p0.max())))
            info[contrat][ens]=dict(eta2_label=float(eta2),
                part_PL_faible_abs_inf2bp=float((pl.abs()<2).mean()), part_PL_abs_inf5bp=float((pl.abs()<5).mean()),
                dispersion_positifs=q_stats(p1), dispersion_negatifs=q_stats(p0), exemples=exemples)
    (OUT/'_phase17c_info.json').write_text(json.dumps(dict(validation_q=validation_q, memes_features=memes_features,
        qdist=qdist, info=info), indent=1, ensure_ascii=False))
    print(json.dumps(validation_q, indent=1)); print('memes_features', memes_features)

if __name__=='__main__': main()
