"""Synthese locale INTEGRAL_SCAN (aucun nouvel acces donnees brutes).
Entrees: INTEGRAL_PARTITION.csv (282x39) + INVENTORY_348_EXHAUSTIVE.json (dates).
Sortie: INTEGRAL_SYNTHESIS.json. Descriptif uniquement, aucune p-value."""
import json, pathlib
import pandas as pd, numpy as np
R = pathlib.Path('reports/meta_alpha/integral_scan')
df = pd.read_csv(R / 'INTEGRAL_PARTITION.csv')
inv = {p['name']: p for p in json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']}
df['tmax'] = pd.to_datetime(df.partition.map(lambda n: inv[n]['timestamp_max_footer']), utc=True, format='mixed')
df = df.sort_values('tmax').reset_index(drop=True)
df['year'] = df.tmax.dt.year
df['era'] = df.year.map(lambda y: '2010-2012' if y <= 2012 else ('2013-2015' if y <= 2015 else '2016-2020'))
KEY = ['sh_both','sh_bidonly','sh_askonly','sh_repub','sh_midconst_comp','sh_cross','mabs_db_bp','mabs_da_bp',
       'sh_zero_r','absr_p50','absr_p99','absr_max','sh_pos','grid_dm','dt_p50','dt_p99','sh_dt60','cv_dt',
       'sp_p10','sp_p50','sp_p99','mabs_dsp','ac1_r','ac1_absr','ac1_spread','corr_db_da','corr_db_lead_da',
       'corr_da_lead_db','run_len']
out = {'n_partitions': int(len(df)), 'ticks_total': int(df.n.sum() + len(df)),
       'periode': [str(df.tmax.min()), str(df.tmax.max())],
       'comptes_ere': {k: int(v) for k, v in df.era.value_counts().items()},
       'par_annee': df.groupby('year')[KEY].median().round(4).to_dict('index'),
       'par_ere': df.groupby('era')[KEY].median().round(4).to_dict('index')}
df['asym_tailles'] = df.mabs_db_bp / df.mabs_da_bp
out['asym_tailles_bid_ask'] = {'mediane': float(df.asym_tailles.median()),
                               'p10': float(df.asym_tailles.quantile(.1)), 'p90': float(df.asym_tailles.quantile(.9))}
out['grille_dm_prix'] = {'mediane': float(df.grid_dm.median()), 'min': float(df.grid_dm.min()),
                         'max': float(df.grid_dm.max()),
                         'valeurs_basses': sorted(df.grid_dm.round(4).unique().tolist())[:10]}
cm = df[KEY + ['n', 'rv_bp2']].corr(method='spearman')
ks = list(cm.columns); pairs = []
for i, a in enumerate(ks):
    for b in ks[i + 1:]:
        if abs(cm.loc[a, b]) >= 0.6:
            pairs.append({'a': a, 'b': b, 'rho_spearman': round(float(cm.loc[a, b]), 3)})
out['correlations_fortes_niveau_partition'] = sorted(pairs, key=lambda x: -abs(x['rho_spearman']))[:15]
out['leadlag_par_ere'] = [{'ere': e, 'med_corr_dBid_t_dAsk_t+1': float(g.corr_db_lead_da.median()),
                           'med_corr_dAsk_t_dBid_t+1': float(g.corr_da_lead_db.median()),
                           'med_corr_contemporaine': float(g.corr_db_da.median())}
                          for e, g in df.groupby('era')]
anom = []; win = 6
for c in KEY:
    v = df[c].values.astype(float)
    for i in range(len(df)):
        lo, hi = max(0, i - win), min(len(df), i + win + 1)
        nb = np.delete(v[lo:hi], i - lo); med = np.median(nb); mad = np.median(np.abs(nb - med)) * 1.4826
        if mad > 0 and abs(v[i] - med) / mad > 5:
            anom.append({'partition': df.partition.iloc[i], 'annee': int(df.year.iloc[i]), 'metrique': c,
                         'valeur': round(float(v[i]), 4), 'mediane_voisines': round(float(med), 4),
                         'z_robuste': round(float(abs(v[i] - med) / mad), 1)})
out['anomalies_contextuelles'] = {'seuil': '|ecart| > 5 MAD vs 12 voisines temporelles',
                                  'compte_total': len(anom),
                                  'top': sorted(anom, key=lambda x: -x['z_robuste'])[:40]}
out['faits_saillants'] = {'part_cotation_croisee_max_toutes_partitions': float(df.sh_cross.max()),
                          'run_len_par_ere': {k: float(v) for k, v in df.groupby('era').run_len.median().items()},
                          'ac1_r_par_ere': {k: float(v) for k, v in df.groupby('era').ac1_r.median().items()},
                          'ac1_spread_par_ere': {k: float(v) for k, v in df.groupby('era').ac1_spread.median().items()}}
(R / 'INTEGRAL_SYNTHESIS.json').write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))
print(json.dumps({k: out[k] for k in ['n_partitions', 'ticks_total', 'comptes_ere', 'asym_tailles_bid_ask', 'grille_dm_prix', 'faits_saillants']}, indent=1, ensure_ascii=False, default=str))
print('leadlag:', json.dumps(out['leadlag_par_ere']))
print('anomalies total:', len(anom))
print('top corr:', json.dumps(out['correlations_fortes_niveau_partition'][:8]))
print(df.groupby('era')[['sh_both','sh_bidonly','sh_askonly','sh_repub','sh_midconst_comp','sp_p50','dt_p50','ac1_r','run_len','corr_db_da','sh_pos']].median().round(3).to_string())
