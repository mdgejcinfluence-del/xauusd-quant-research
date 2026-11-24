# -*- coding: utf-8 -*-
"""Phase 20-C: morphologie des grandes amplitudes H4. Artefacts 20-A uniquement."""
import json, pathlib
import numpy as np, pandas as pd
R20 = pathlib.Path('reports/meta_alpha/phase20')
GRAINE = 2011

def main():
    b = pd.read_parquet(R20 / 'PHASE20A_H4_BARSET.parquet').sort_values('bar_start').reset_index(drop=True)
    fw = pd.read_parquet(R20 / 'PHASE20A_H4_FORWARD_MFE_MAE.parquet')
    b['BODY_EFFICIENCY'] = b.ABS_BODY_BP / b.RANGE_BP
    b['CLOSE_LOCATION'] = (b.close - b.low) / (b.high - b.low)
    b['UPPER_WICK_BP'] = 10000 * np.log(b.high / b[['open', 'close']].max(axis=1))
    b['LOWER_WICK_BP'] = 10000 * np.log(b[['open', 'close']].min(axis=1) / b.low)
    b['UPPER_WICK_SHARE'] = b.UPPER_WICK_BP / b.RANGE_BP
    b['LOWER_WICK_SHARE'] = b.LOWER_WICK_BP / b.RANGE_BP
    b['WICK_IMBALANCE'] = (b.LOWER_WICK_BP - b.UPPER_WICK_BP) / b.RANGE_BP
    comp = b[b.complete].reset_index(drop=True)
    # seuils causaux sur 250 barres completes precedentes
    for col, nom in [('RANGE_BP', 'Q90_RANGE'), ('CLOSE_LOCATION', 'CL'), ('WICK_IMBALANCE', 'WI')]:
        vals = comp[col].values
        if nom == 'Q90_RANGE':
            comp[nom] = [np.quantile(vals[i - 250:i], .90) if i >= 250 else np.nan for i in range(len(comp))]
        else:
            comp[nom + '_D10'] = [np.quantile(vals[i - 250:i], .10) if i >= 250 else np.nan for i in range(len(comp))]
            comp[nom + '_D90'] = [np.quantile(vals[i - 250:i], .90) if i >= 250 else np.nan for i in range(len(comp))]
    comp['EXPANSION'] = comp.RANGE_BP >= comp.Q90_RANGE
    # episodes d'expansion consecutifs
    ep = np.full(len(comp), -1); courant = -1
    for i in range(len(comp)):
        if comp.EXPANSION.iloc[i]:
            if i == 0 or not comp.EXPANSION.iloc[i - 1] or comp.bar_start.iloc[i] - comp.bar_start.iloc[i - 1] != pd.Timedelta(hours=4):
                courant += 1
            ep[i] = courant
    comp['EXPANSION_EPISODE_ID'] = np.where(ep >= 0, 'EP-' + pd.Series(ep).astype(str), '')
    comp.loc[ep < 0, 'EXPANSION_EPISODE_ID'] = ''
    comp['EST_PREMIER_EPISODE'] = False
    premiers = comp[comp.EXPANSION].groupby('EXPANSION_EPISODE_ID').head(1).index
    comp.loc[premiers, 'EST_PREMIER_EPISODE'] = True
    comp['CFG_A'] = comp.EXPANSION & (comp.CLOSE_LOCATION >= comp.CL_D90)
    comp['CFG_B'] = comp.EXPANSION & (comp.CLOSE_LOCATION <= comp.CL_D10)
    comp['CFG_C'] = comp.EXPANSION & (comp.CLOSE_LOCATION > comp.CL_D10) & (comp.CLOSE_LOCATION < comp.CL_D90)
    comp['CFG_D'] = comp.EXPANSION & (comp.WICK_IMBALANCE >= comp.WI_D90)
    comp['CFG_E'] = comp.EXPANSION & (comp.WICK_IMBALANCE <= comp.WI_D10)
    exp = comp[comp.EXPANSION].copy()
    exp[['bar_start', 'EXPANSION_EPISODE_ID', 'EST_PREMIER_EPISODE', 'RANGE_BP', 'Q90_RANGE',
         'CFG_A', 'CFG_B', 'CFG_C', 'CFG_D', 'CFG_E']].to_parquet(R20 / 'PHASE20C_EXPANSION_EVENT_CATALOG.parquet', index=False)
    comp[['bar_start', 'BODY_BP', 'ABS_BODY_BP', 'RANGE_BP', 'BODY_EFFICIENCY', 'CLOSE_LOCATION',
          'UPPER_WICK_BP', 'LOWER_WICK_BP', 'UPPER_WICK_SHARE', 'LOWER_WICK_SHARE', 'WICK_IMBALANCE',
          'ATR14_H4_PREV']].to_parquet(R20 / 'PHASE20C_EVENT_SHAPE_METRICS.parquet', index=False)
    # futur oriente
    j = exp.merge(fw, on='bar_start', how='left')
    DIRECTION = {'CFG_A': 1, 'CFG_B': -1, 'CFG_D': -1, 'CFG_E': 1}
    lignes_f = []
    closes = comp.set_index('bar_start').close
    starts = comp.bar_start.values; idx_of = {t: i for i, t in enumerate(comp.bar_start)}
    for r in j.itertuples():
        i0 = idx_of[r.bar_start]
        for H in (1, 2, 3, 4):
            if i0 + H >= len(comp): continue
            if starts[i0 + H] - starts[i0] != np.timedelta64(4 * H, 'h'): continue
            term_raw = 10000 * np.log(comp.close.iloc[i0 + H] / comp.close.iloc[i0])
            # temps (en barres) jusqu'aux extremes de l'horizon
            seg_hi = comp.high.iloc[i0 + 1:i0 + H + 1]; seg_lo = comp.low.iloc[i0 + 1:i0 + H + 1]
            t_up = int(np.argmax(seg_hi.values)) + 1 if len(seg_hi) else np.nan
            t_dn = int(np.argmin(seg_lo.values)) + 1 if len(seg_lo) else np.nan
            for cfg, d in DIRECTION.items():
                if not getattr(r, cfg): continue
                mfe = r.__getattribute__(f'UP_{H}') if d == 1 else r.__getattribute__(f'DOWN_{H}')
                mae = r.__getattribute__(f'DOWN_{H}') if d == 1 else r.__getattribute__(f'UP_{H}')
                lignes_f.append(dict(bar_start=r.bar_start, episode=r.EXPANSION_EPISODE_ID, premier=r.EST_PREMIER_EPISODE,
                                     configuration=cfg, horizon=H, direction=d, terminal_oriente=d * term_raw,
                                     MFE=mfe, MAE=mae, restitution=(mfe - d * term_raw) / mfe if mfe and mfe > 0 else np.nan,
                                     t_MFE_barres=t_up if d == 1 else t_dn, t_MAE_barres=t_dn if d == 1 else t_up,
                                     semaine= r.bar_start.strftime('%G-W%V')))
            if r.CFG_C:
                lignes_f.append(dict(bar_start=r.bar_start, episode=r.EXPANSION_EPISODE_ID, premier=r.EST_PREMIER_EPISODE,
                                     configuration='CFG_C', horizon=H, direction=0, terminal_oriente=np.nan,
                                     terminal_brut=term_raw, MFE=np.nan, MAE=np.nan,
                                     UP=r.__getattribute__(f'UP_{H}'), DOWN=r.__getattribute__(f'DOWN_{H}'),
                                     semaine=r.bar_start.strftime('%G-W%V')))
    F = pd.DataFrame(lignes_f)
    F.to_parquet(R20 / 'PHASE20C_FORWARD_EXCURSIONS.parquet', index=False)
    # couverture des configurations
    cov = []
    for cfg in ['CFG_A', 'CFG_B', 'CFG_C', 'CFG_D', 'CFG_E']:
        g = exp[exp[cfg]]
        cov.append(dict(configuration=cfg, n_toutes=int(len(g)), n_episodes=int(g.EXPANSION_EPISODE_ID.nunique()),
                        n_primaires=int(g.EST_PREMIER_EPISODE.sum()),
                        n_semaines=int(g.bar_start.dt.strftime('%G-W%V').nunique()),
                        chevauchements=';'.join(f'{c2}:{int((g[cfg]&g[c2]).sum())}' for c2 in ['CFG_A','CFG_B','CFG_C','CFG_D','CFG_E'] if c2 != cfg),
                        atr_valides=int(g.merge(comp[['bar_start','ATR14_H4_PREV']], on='bar_start').ATR14_H4_PREV.notna().sum()) if False else int(comp[comp.bar_start.isin(g.bar_start)].ATR14_H4_PREV.notna().sum())))
    pd.DataFrame(cov).to_csv(R20 / 'PHASE20C_CONFIGURATION_COVERAGE.csv', index=False)
    # asymetrie MFE/MAE (primaire)
    P = F[F.premier]
    asym = []
    for (cfg, H), g in P.groupby(['configuration', 'horizon']):
        a = dict(configuration=cfg, horizon=H, n=int(len(g)), MFE_mediane=float(g.MFE.median()), MFE_moyen=float(g.MFE.mean()),
                 MAE_mediane=float(g.MAE.median()), MAE_moyen=float(g.MAE.mean()),
                 terminal_mediane=float(g.terminal_oriente.median()) if cfg != 'CFG_C' else float(g.terminal_brut.median()),
                 terminal_moyen=float(g.terminal_oriente.mean()) if cfg != 'CFG_C' else float(g.terminal_brut.mean()))
        for p in (10, 25, 50, 75, 90, 95): a[f'terminal_P{p}'] = float((g.terminal_oriente if cfg != 'CFG_C' else g.terminal_brut).quantile(p / 100))
        for seuil in (30, 60, 100): a[f'part_MFE_sup{seuil}'] = float((g.MFE > seuil).mean())
        asym.append(a)
    pd.DataFrame(asym).to_csv(R20 / 'PHASE20C_MFE_MAE_ASYMMETRY.csv', index=False)
    # couverture couts (diagnostic)
    cov2 = []
    for (cfg, H), g in P.groupby(['configuration', 'horizon']):
        if cfg == 'CFG_C': continue
        for ref in (4.0, 4.5):
            ligne = dict(configuration=cfg, horizon=H, reference_bp=ref)
            for mult in (1, 2, 3, 5):
                ligne[f'part_MFE_sup_{mult}x'] = float((g.MFE > mult * ref).mean())
                ligne[f'part_terminal_sup_{mult}x'] = float((g.terminal_oriente > mult * ref).mean())
            cov2.append(ligne)
    pd.DataFrame(cov2).to_csv(R20 / 'PHASE20C_AMPLITUDE_COST_COVERAGE.csv', index=False)
    # tests primaires: cfg vs C sur terminal oriente (C: terminal dans le sens de A/B/D/E? comparaison par paires directionnelles)
    rng = np.random.default_rng(GRAINE); tests = []
    C = P[P.configuration == 'CFG_C']
    for cfg, d in DIRECTION.items():
        A = P[P.configuration == cfg]
        for H in (1, 2, 3, 4):
            a = A[A.horizon == H]; c = C[C.horizon == H]
            # pour C, orienter son terminal brut dans la direction de la configuration comparee
            c_or = d * c.terminal_brut
            obs = float(a.terminal_oriente.mean() - c_or.mean())
            ea = a.groupby('episode').terminal_oriente.mean().values
            ec = (d * c.terminal_brut).groupby(c.episode).mean().values
            boots = np.array([rng.choice(ea, len(ea), replace=True).mean() - rng.choice(ec, len(ec), replace=True).mean() for _ in range(2000)]) if len(ea) and len(ec) else np.array([np.nan])
            p = float(min(1.0, 2 * min((boots <= 0).mean(), (boots >= 0).mean()))) if np.isfinite(boots).any() else np.nan
            tests.append(dict(configuration=cfg, horizon=H, comparaison=f'{cfg} vs CFG_C (terminal oriente)',
                              n_config=int(len(a)), n_C=int(len(c)), n_episodes=int(a.episode.nunique()),
                              n_semaines=int(a.semaine.nunique()), effet_moyen_bp=obs,
                              difference_medianes=float(a.terminal_oriente.median() - c_or.median()),
                              p_value=p, ic95=[float(np.nanquantile(boots, .025)), float(np.nanquantile(boots, .975))],
                              statut='EVALUE' if (len(a) >= 50 and a.semaine.nunique() >= 20) else 'NON_EVALUABLE_INFERENTIAL'))
    T = pd.DataFrame(tests)
    if len(T):
        p = T.p_value.values; ordre = np.argsort(p); q = np.empty(len(p)); prev = 1.0
        for i, ix in enumerate(ordre[::-1]): prev = min(prev, p[ix] * len(p) / (len(p) - i)); q[ix] = prev
        T['q_value_BH'] = q
    T.to_csv(R20 / 'PHASE20C_MULTIPLE_TEST_CORRECTION.csv', index=False)
    # stabilite temporelle
    stab = []
    for (cfg, H), g in P.groupby(['configuration', 'horizon']):
        for per, m in [('2010-2015', g.bar_start.dt.year <= 2015), ('2016-2020', g.bar_start.dt.year >= 2016)]:
            gg = g[m]
            stab.append(dict(configuration=cfg, horizon=H, periode=per, n=int(len(gg)),
                             terminal_moyen=float((gg.terminal_oriente if cfg != 'CFG_C' else gg.terminal_brut).mean()) if len(gg) else None,
                             MFE_mediane=float(gg.MFE.median()) if len(gg) else None, MAE_mediane=float(gg.MAE.median()) if len(gg) else None))
        for an, gg in g.groupby(g.bar_start.dt.year):
            stab.append(dict(configuration=cfg, horizon=H, periode=str(an), n=int(len(gg)),
                             terminal_moyen=float((gg.terminal_oriente if cfg != 'CFG_C' else gg.terminal_brut).mean()) if len(gg) else None,
                             MFE_mediane=float(gg.MFE.median()) if len(gg) else None, MAE_mediane=float(gg.MAE.median()) if len(gg) else None))
    pd.DataFrame(stab).to_csv(R20 / 'PHASE20C_TEMPORAL_STABILITY.csv', index=False)
    # registre candidats
    reg = []
    for cfg in ['CFG_A', 'CFG_B', 'CFG_C', 'CFG_D', 'CFG_E']:
        t4 = T[(T.configuration == cfg)]; s4 = P[(P.configuration == cfg)]
        qs = t4.q_value_BH.values if len(t4) else []
        st = pd.read_csv(R20 / 'PHASE20C_TEMPORAL_STABILITY.csv')
        s_per = st[(st.configuration == cfg) & (st.horizon == 4) & (st.periode.isin(['2010-2015', '2016-2020']))]
        signes = np.sign(s_per.terminal_moyen.dropna().values) if len(s_per) else []
        if cfg == 'CFG_C': qual = 'AMPLITUDE_ONLY'
        elif not len(qs) or (t4.statut != 'EVALUE').all(): qual = 'INSUFFICIENT_EVIDENCE'
        elif len(signes) == 2 and signes[0] != signes[1]: qual = 'UNSTABLE_STRUCTURAL_CANDIDATE'
        elif (qs < 0.05).any(): qual = 'AMPLITUDE_BACKED_STRUCTURAL_CANDIDATE'
        elif (t4.effet_moyen_bp.abs() > 4.5).any(): qual = 'DIRECTIONAL_ASYMMETRY_CANDIDATE'
        else: qual = 'AMPLITUDE_ONLY'
        reg.append(dict(configuration=cfg, n_primaires=int(s4.bar_start.nunique()), qualification=qual,
                        q_min=float(np.min(qs)) if len(qs) else None,
                        note='classification descriptive, jamais une strategie ni un edge rentable'))
    pd.DataFrame(reg).to_csv(R20 / 'PHASE20C_STRUCTURAL_CANDIDATE_REGISTRY.csv', index=False)
    stats = dict(n_barres_completes=int(len(comp)), n_expansions=int(comp.EXPANSION.sum()),
                 n_episodes=int(comp[comp.EXPANSION].EXPANSION_EPISODE_ID.nunique()),
                 couverture={c: int(exp[c].sum()) for c in ['CFG_A', 'CFG_B', 'CFG_C', 'CFG_D', 'CFG_E']})
    (R20 / '_phase20c_stats.json').write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))

if __name__ == '__main__': main()
