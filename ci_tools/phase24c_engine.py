#!/usr/bin/env python3
"""PHASE 24-C - Entrainement et evaluation predictive des 3 Chauffeurs M15.
EXPLORATORY_POST_HOC (seq394). Logistique IRLS reproduite de phase12b_engine
(non penalisee, ridge numerique 1e-8, tol 1e-10, 200 iter, z clip [-35,35]).
4 variables + intercept = 5 parametres. Seuil = prevalence majoritaire du train
propre (regle 24-A). Bootstrap par grappe 10000 repliques, graine 2123.
Aucun P&L, aucun tuning, holdout jamais accede."""
import hashlib, json, pathlib, sys
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
R24 = ROOT / 'reports/meta_alpha/phase24'
GRAINE = 2123; NBOOT = 10000
VARS = ['ratio_repli', 'duree_extreme_vers_treint_min', 'MFE_A_TREINT_BP', 'nb_touches_P0']
MODELES = {'M15_TIME_ONLY': 'perm_TIME_ONLY', 'M15_H4_TIME': 'perm_H4_TIME', 'M15_D1_TIME': 'perm_D1_TIME'}


def logistique_irls(X, y, max_iter=200, tol=1e-10):
    Xd = np.column_stack([np.ones(len(X)), X]); beta = np.zeros(Xd.shape[1])
    for _ in range(max_iter):
        z = np.clip(Xd @ beta, -35, 35); p = 1 / (1 + np.exp(-z))
        W = np.clip(p * (1 - p), 1e-10, None)
        A = Xd.T @ (Xd * W[:, None]) + 1e-8 * np.eye(Xd.shape[1])
        pas = np.linalg.solve(A, Xd.T @ (y - p))
        beta_n = beta + pas
        if np.max(np.abs(beta_n - beta)) < tol: beta = beta_n; break
        beta = beta_n
    cov = np.linalg.inv(Xd.T @ (Xd * np.clip((1 / (1 + np.exp(-np.clip(Xd @ beta, -35, 35)))) *
                        (1 - 1 / (1 + np.exp(-np.clip(Xd @ beta, -35, 35)))), 1e-10, None)[:, None]) + 1e-8 * np.eye(Xd.shape[1]))
    return beta, np.sqrt(np.diag(cov))


def predire(beta, X):
    z = np.clip(np.column_stack([np.ones(len(X)), X]) @ beta, -35, 35)
    return 1 / (1 + np.exp(-z))


def metriques(y, p, seuil):
    y = np.asarray(y, float); p = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15)
    rangs = pd.Series(p).rank(method='average').values
    n1, n0 = y.sum(), len(y) - y.sum()
    auc = float((rangs[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)) if n1 and n0 else np.nan
    pred = (p >= seuil).astype(float)
    tp = float(((pred == 1) & (y == 1)).sum()); fp = float(((pred == 1) & (y == 0)).sum())
    fn = float(((pred == 0) & (y == 1)).sum()); tn = float(((pred == 0) & (y == 0)).sum())
    # pente/intercept de calibration: logit(y) ~ a + b*logit(p) via IRLS simple
    lp = np.log(p / (1 - p))
    try:
        b2, _ = logistique_irls(lp.reshape(-1, 1), y); pente, inter = float(b2[1]), float(b2[0])
    except Exception:
        pente, inter = np.nan, np.nan
    return dict(brier=float(np.mean((p - y) ** 2)),
                log_loss=float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))), auc=auc,
                precision=tp / (tp + fp) if tp + fp else np.nan, rappel=tp / (tp + fn) if tp + fn else np.nan,
                part_decisions_positives=float(pred.mean()), TP=tp, FP=fp, FN=fn, TN=tn,
                pente_calibration=pente, intercept_calibration=inter, prevalence=float(y.mean()),
                p_moyen=float(p.mean()), p_p10=float(np.quantile(p, .1)), p_p90=float(np.quantile(p, .9)))


def boot_grappes(df, col_a, col_b, rng):
    """Difference appariee de Brier (a - b) par reechantillonnage des grappes completes."""
    groupes = {g: v for g, v in df.groupby('grappe_id')}
    cles = list(groupes.keys())
    diffs_b, diffs_l = [], []
    y = df.Y_RESUMPTION.values
    for _ in range(NBOOT):
        idx = np.concatenate([groupes[c].index.values for c in rng.choice(cles, len(cles), replace=True)])
        pos = df.index.get_indexer(idx)
        yy = df.Y_RESUMPTION.values[pos]
        pa = np.clip(df[col_a].values[pos], 1e-15, 1 - 1e-15); pb = np.clip(df[col_b].values[pos], 1e-15, 1 - 1e-15)
        diffs_b.append(np.mean((pa - yy) ** 2) - np.mean((pb - yy) ** 2))
        diffs_l.append(-np.mean(yy * np.log(pa) + (1 - yy) * np.log(1 - pa)) + np.mean(yy * np.log(pb) + (1 - yy) * np.log(1 - pb)))
    return (float(np.mean((np.clip(df[col_a], 1e-15, 1 - 1e-15) - y) ** 2) - np.mean((np.clip(df[col_b], 1e-15, 1 - 1e-15) - y) ** 2)),
            tuple(np.percentile(diffs_b, [2.5, 97.5])),
            tuple(np.percentile(diffs_l, [2.5, 97.5])))


def main():
    P = pd.read_parquet(R24 / 'PHASE24B_M15_GATE_PERMISSION_PANEL.parquet')
    P['event_id'] = ['EV-M15-%06d' % i for i in range(len(P))]
    P['IMPULSE_EPISODE_ID'] = P.grappe_id
    P['WEEK_ISO'] = P.semaine_iso
    rng = np.random.default_rng(GRAINE)
    coefs, preds, registry, recon = [], P[['event_id', 'grappe_id', 'IMPULSE_EPISODE_ID', 'WEEK_ISO', 'split', 'Y_RESUMPTION']].copy(), {}, []
    betas = {}
    for nom, col in MODELES.items():
        pop = P[P[col]]
        tr = pop[pop.split == 'APPRENTISSAGE']
        beta, se = logistique_irls(tr[VARS].values, tr.Y_RESUMPTION.values)
        betas[nom] = beta
        seuil = float(tr.Y_RESUMPTION.mean())
        registry[nom] = dict(population=col, n_train=int(len(tr)), prevalence_train=seuil, seuil_classification=seuil,
                             parametres=5, variables=VARS, graine=GRAINE,
                             algorithme='IRLS non penalise (reproduction phase12b), ridge numerique 1e-8, tol 1e-10, max 200 iter')
        for v, b_, s_ in zip(['INTERCEPT'] + VARS, beta, se):
            coefs.append(dict(modele=nom, terme=v, coefficient=float(b_), erreur_standard=float(s_)))
        preds[f'p_{nom}'] = np.nan
        preds.loc[pop.index, f'p_{nom}'] = predire(beta, pop[VARS].values)
        recon.append(dict(modele=nom, train=int(len(tr)), calibration=int((pop.split == 'CALIBRATION').sum()),
                          evaluation=int((pop.split == 'EVALUATION').sum()),
                          reference_24B={'M15_TIME_ONLY': (4733, 1469), 'M15_H4_TIME': (408, 139), 'M15_D1_TIME': (469, 198)}[nom]))
    # M0 par variante (prevalence train) applique a sa population
    for nom, col in MODELES.items():
        preds[f'p_M0_{nom}'] = np.nan
        preds.loc[P[col], f'p_M0_{nom}'] = registry[nom]['prevalence_train']
    preds.to_parquet(R24 / 'PHASE24C_EVENT_PREDICTIONS.parquet', index=False)
    pd.DataFrame(coefs).to_csv(R24 / 'PHASE24C_COEFFICIENTS.csv', index=False)
    # metriques par modele x segment sur sa population; puis comparaisons communes
    lignes, audit = [], []
    for nom, col in MODELES.items():
        pop = P[P[col]]
        for seg in ['APPRENTISSAGE', 'CALIBRATION', 'EVALUATION']:
            g = pop[pop.split == seg]
            m = metriques(g.Y_RESUMPTION.values, preds.loc[g.index, f'p_{nom}'].values, registry[nom]['seuil_classification'])
            m0 = metriques(g.Y_RESUMPTION.values, np.full(len(g), registry[nom]['prevalence_train']), registry[nom]['seuil_classification'])
            lignes.append(dict(modele=nom, segment=seg, n=len(g), **{k: m[k] for k in ('brier', 'log_loss', 'auc', 'precision', 'rappel', 'part_decisions_positives', 'prevalence')}))
            audit.append(dict(modele=nom, segment=seg, n=len(g), brier_modele=m['brier'], brier_M0=m0['brier'],
                              logloss_modele=m['log_loss'], logloss_M0=m0['log_loss'], auc=m['auc'],
                              pente_calibration=m['pente_calibration'], intercept_calibration=m['intercept_calibration'],
                              TP=m['TP'], FP=m['FP'], FN=m['FN'], TN=m['TN'], p_moyen=m['p_moyen'], p_p10=m['p_p10'], p_p90=m['p_p90']))
    pd.DataFrame(audit).to_csv(R24 / 'PHASE24C_BRIER_LOGLOSS_AUDIT.csv', index=False)
    pd.DataFrame(lignes).to_csv(R24 / 'PHASE24C_AUC_AND_CALIBRATION.csv', index=False)
    # comparaisons communes sur EVALUATION des cohortes conditionnelles
    comp = []
    stats = {}
    for cond, col in [('M15_H4_TIME', 'perm_H4_TIME'), ('M15_D1_TIME', 'perm_D1_TIME')]:
        ev = P[P[col] & (P.split == 'EVALUATION')].copy()
        evp = preds.set_index('event_id').loc[ev.event_id].reset_index()
        m_cond = metriques(ev.Y_RESUMPTION.values, evp[f'p_{cond}'].values, registry[cond]['seuil_classification'])
        m_gen = metriques(ev.Y_RESUMPTION.values, evp['p_M15_TIME_ONLY'].values, registry['M15_TIME_ONLY']['seuil_classification'])
        m_m0 = metriques(ev.Y_RESUMPTION.values, np.full(len(ev), registry[cond]['prevalence_train']), registry[cond]['seuil_classification'])
        d = ev[['grappe_id', 'Y_RESUMPTION']].copy()
        d['p_cond'] = evp[f'p_{cond}'].values; d['p_gen'] = evp['p_M15_TIME_ONLY'].values
        db, cib, cil = boot_grappes(d, 'p_cond', 'p_gen', rng)
        comp.append(dict(cohorte=cond, n=len(ev), grappes=int(ev.grappe_id.nunique()),
                         brier_cond=m_cond['brier'], brier_generaliste=m_gen['brier'], brier_M0=m_m0['brier'],
                         logloss_cond=m_cond['log_loss'], logloss_generaliste=m_gen['log_loss'], logloss_M0=m_m0['log_loss'],
                         auc_cond=m_cond['auc'], auc_generaliste=m_gen['auc'],
                         diff_brier_cond_moins_generaliste=db, IC95_diff_brier=cib,
                         IC95_diff_logloss=cil, pente_calibration_cond=m_cond['pente_calibration']))
        stats[cond] = comp[-1]
    pd.DataFrame([{k: (str(v) if isinstance(v, tuple) else v) for k, v in c.items()} for c in comp]).to_csv(
        R24 / 'PHASE24C_COMMON_COHORT_COMPARISON.csv', index=False)
    pd.DataFrame(comp).assign(IC95_diff_brier=lambda d: d.IC95_diff_brier.astype(str), IC95_diff_logloss=lambda d: d.IC95_diff_logloss.astype(str))\
        .to_csv(R24 / 'PHASE24C_BASELINE_COMPARISON.csv', index=False)
    pd.DataFrame(recon).to_csv(R24 / 'PHASE24C_COHORT_RECONCILIATION.csv', index=False)
    registry['_meta'] = dict(phase='24-C', graine=GRAINE, nboot=NBOOT, variables=VARS,
                             note='Q90 M15 vs Q95 H1 historique: evenements differents des evenements H1; aucun coefficient M1 reutilise')
    (R24 / 'PHASE24C_MODEL_REGISTRY.json').write_text(json.dumps(registry, indent=1))
    (R24 / '_phase24c_stats.json').write_text(json.dumps(stats, indent=1, default=str))
    print(pd.DataFrame(audit).round(4).to_string()); print(pd.DataFrame(comp).round(4).to_string(), flush=True)


if __name__ == '__main__':
    main()
