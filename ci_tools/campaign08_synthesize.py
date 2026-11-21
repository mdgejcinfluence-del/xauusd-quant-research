"""CAMPAGNE 8 - synthese descriptive F-J. Protocole gele V2 (seq266).
Bootstrap par grappes-composantes connexes 2000 replicats graine 20261113;
BY famille de cinq a m=5 FIXE; controles de composition et de grappe
dominante sans aucune p-value ajoutee."""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign08')
RNG = np.random.default_rng(20261113)
B = 2000

class UF:
    def __init__(self, n): self.p = list(range(n))
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb: self.p[ra] = rb

def construire_grappes(units):
    """units: dicts {jour, ancrage, chocs(liste minutes), bras, valeur}.
    Retourne (cluster_id par unite, diagnostics)."""
    n = len(units); uf = UF(n)
    par_jour = {}
    for i, u in enumerate(units): par_jour.setdefault(u['jour'], []).append(i)
    for idxs in par_jour.values():
        for j in idxs[1:]: uf.union(idxs[0], j)
    # sillages chevauchants: balayage sur [ancrage, ancrage+60]
    ordre = sorted(range(n), key=lambda i: units[i]['ancrage'])
    actif = []
    for i in ordre:
        actif = [j for j in actif if units[j]['ancrage'] + 60 >= units[i]['ancrage']]
        if actif: uf.union(i, actif[-1])  # chainage: la connexite suit par transitivite
        actif.append(i)
    # sillage contenant un choc (ou l'ancrage) d'une autre unite
    evenements = []
    for i, u in enumerate(units):
        for t in u['chocs']: evenements.append((t, i))
    evenements.sort()
    ets = np.array([t for t, _ in evenements]) if evenements else np.array([], dtype=int)
    for i, u in enumerate(units):
        if len(ets) == 0: break
        a = np.searchsorted(ets, u['ancrage']); b = np.searchsorted(ets, u['ancrage'] + 60, side='right')
        for k in range(a, b):
            if evenements[k][1] != i: uf.union(i, evenements[k][1])
    # aretes d'appariement (FJ-05)
    for i, u in enumerate(units):
        if u.get('pair') is not None: uf.union(i, u['pair'])
    racines = [uf.find(i) for i in range(n)]
    diag = {}
    tailles = pd.Series(racines).value_counts()
    diag['n_grappes'] = int(len(tailles)); diag['taille_max_grappe'] = int(tailles.max()) if len(tailles) else 0
    jours_par_grappe = {}
    for i, u in enumerate(units): jours_par_grappe.setdefault(racines[i], set()).add(u['jour'])
    diag['grappes_multi_jours'] = int(sum(1 for v in jours_par_grappe.values() if len(v) > 1))
    chev = 0
    for i in ordre:
        if any(j != i and units[j]['ancrage'] <= units[i]['ancrage'] + 60 and units[i]['ancrage'] <= units[j]['ancrage'] + 60 for j in ordre):
            pass
    diag['part_sillages_chevauchants'] = float(np.mean([any(j != i and abs(units[j]['ancrage'] - units[i]['ancrage']) <= 60 for j in range(n)) for i in range(n)])) if n else 0.0
    diag['traversees_minuit'] = int(sum(1 for u in units if (u['ancrage'] % 1440) + 60 >= 1440))
    parts = {}
    for bras in (0, 1):
        idxs = [i for i, u in enumerate(units) if u['bras'] == bras]
        if idxs:
            cnt = pd.Series([racines[i] for i in idxs]).value_counts()
            parts[bras] = float(cnt.max() / len(idxs))
        else: parts[bras] = 0.0
    diag['part_plus_grande_grappe_par_bras'] = {str(k): v for k, v in parts.items()}
    diag['grappes_par_bras'] = {str(bras): int(len(set(racines[i] for i, u in enumerate(units) if u['bras'] == bras))) for bras in (0, 1)}
    return racines, diag

def boot_medianes(units, racines):
    """Difference de medianes (bras0 - bras1), bootstrap par grappes."""
    vals = {0: [], 1: []}
    grap = {}
    for i, u in enumerate(units):
        grap.setdefault(racines[i], {0: [], 1: []})[u['bras']].append(u['valeur'])
    cles = list(grap.keys())
    na = sum(len(grap[k][0]) for k in cles); nb = sum(len(grap[k][1]) for k in cles)
    ga = sum(1 for k in cles if grap[k][0]); gb = sum(1 for k in cles if grap[k][1])
    if na == 0 or nb == 0 or not cles: return (np.nan,) * 4 + (na, nb, ga, gb)
    va = np.array([u['valeur'] for u in units if u['bras'] == 0]); vb = np.array([u['valeur'] for u in units if u['bras'] == 1])
    stat = float(np.median(va) - np.median(vb))
    la = [np.array(grap[k][0]) for k in cles]; lb = [np.array(grap[k][1]) for k in cles]
    diffs = []
    for _ in range(B):
        idx = RNG.integers(0, len(cles), len(cles))
        xa = np.concatenate([la[i] for i in idx if len(la[i])]) if any(len(la[i]) for i in idx) else np.array([])
        xb = np.concatenate([lb[i] for i in idx if len(lb[i])]) if any(len(lb[i]) for i in idx) else np.array([])
        if len(xa) and len(xb): diffs.append(np.median(xa) - np.median(xb))
    diffs = np.array(diffs, float)
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    p = 2 * min((diffs <= 0).mean(), (diffs >= 0).mean())
    return stat, float(lo), float(hi), float(min(max(p, 1 / B), 1.0)), na, nb, ga, gb

def BY_m5(pvals):
    p = np.asarray(pvals, float); H5 = sum(1 / i for i in range(1, 6))
    ok = ~np.isnan(p); out = np.full(len(p), np.nan)
    if ok.sum() == 0: return out
    pv = p[ok]; o = np.argsort(pv); q = pv[o] * 5 * H5 / (np.arange(len(pv)) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    tmp = np.empty(len(pv)); tmp[o] = np.minimum(q, 1.0); out[ok] = tmp
    return out

def unites_episodes(df):
    return [{'jour': r.date, 'ancrage': int(r.t_dernier), 'chocs': [int(x) for x in str(r.chocs_t).split(';')],
             'bras': int(r._bras), 'valeur': float(r.R60)} for r in df.itertuples()]

def tercile_assign(pool):
    q1, q2 = np.quantile(pool, [1 / 3, 2 / 3], method='linear')
    return (q1, q2), lambda v: 0 if v <= q1 else (1 if v <= q2 else 2)

def main():
    EP = pd.read_csv(ROOT / 'CAMPAIGN_08_EPISODES.csv.gz')
    PS = pd.read_csv(ROOT / 'CAMPAIGN_08_PSEUDOS.csv.gz')
    details = {}
    details['populations'] = {
        'episodes_total': int(len(EP)),
        'par_classe': {k: int(v) for k, v in EP.classe.value_counts().items()},
        'par_statut': {k: int(v) for k, v in EP.statut.value_counts().items()},
        'isoles': int((EP.n_chocs == 1).sum()), 'regroupes': int((EP.n_chocs >= 2).sum()),
        'chocs_total_episodes': int(EP.n_chocs.sum()),
        'pseudo_bassin': int(len(PS))}
    clos = EP[(EP.statut == 'CLOS') & (EP.classe != 'MIXTE')].copy()
    base = clos[np.isfinite(clos.R60)].copy()  # CENSURE_FENETRE exclue des bras, taux publies
    details['censure_fenetre_parmi_clos_non_mixtes'] = int(len(clos) - len(base))
    isol = base[base.n_chocs == 1].copy(); regr = base[base.n_chocs >= 2].copy()

    comparaisons = {}
    def prep(df_a, df_b):
        a = df_a.copy(); b = df_b.copy(); a['_bras'] = 0; b['_bras'] = 1
        units = unites_episodes(pd.concat([a, b]))
        racines, diag = construire_grappes(units)
        return units, racines, diag

    # FJ-01 signe
    comparaisons['FJ-01'] = (isol[isol.classe == 'POSITIF'], isol[isol.classe == 'NEGATIF'], None)
    # FJ-02 regroupement
    comparaisons['FJ-02'] = (regr, isol, None)
    # FJ-03 intensite
    comparaisons['FJ-03'] = (isol[isol.I_ep >= 2], isol[(isol.I_ep > 1) & (isol.I_ep <= 1) if False else (isol.I_ep < 2)], None)
    # FJ-04 eres
    comparaisons['FJ-04'] = (isol[isol.ere == '2010_2013'], isol[isol.ere == '2017_2020'], None)

    # FJ-05 appariement (protocole V2 section 6)
    cand = EP[(EP.statut == 'CLOS') & (EP.classe != 'MIXTE') & (EP.n_chocs == 1)].copy()
    cand = cand[np.isfinite(cand.A_avant)].sort_values('t_premier')
    seuils_terc = {}; terc = {}
    for ses in ['S1', 'S2', 'S3', 'S4']:
        pool = np.concatenate([PS[PS.session == ses].A_avant.values,
                               EP[(EP.n_chocs == 1) & (EP.session == ses)].A_avant.dropna().values])
        (q1, q2), f = tercile_assign(pool); seuils_terc[ses] = (float(q1), float(q2)); terc[ses] = f
    PS = PS.copy(); PS['tercile'] = [terc[r.session](r.A_avant) if np.isfinite(r.A_avant) else -1 for r in PS.itertuples()]
    cand['tercile'] = [terc[r.session](r.A_avant) for r in cand.itertuples()]
    cand['signe'] = np.where(cand.classe == 'POSITIF', 1, -1)
    utilises = set(); paires = []; non_app = []
    ps_par_strate = {}
    for r in PS.itertuples():
        ps_par_strate.setdefault((r.session, int(r.signe), int(r.tercile)), []).append(r)
    for r in cand.itertuples():
        cands = [p for p in ps_par_strate.get((r.session, int(r.signe), int(r.tercile)), []) if p.pseudo_id not in utilises]
        if not cands:
            non_app.append({'episode_id': int(r.episode_id), 'motif': 'STRATE_VIDE'}); continue
        cands.sort(key=lambda p: (abs(int(p.pos) - int(r.pos_premier)), int(p.t)))
        best = cands[0]
        if abs(int(best.pos) - int(r.pos_premier)) > 60:
            non_app.append({'episode_id': int(r.episode_id), 'motif': 'DISTANCE_POSITION>60'}); continue
        utilises.add(int(best.pseudo_id))
        paires.append({'episode_id': int(r.episode_id), 'pseudo_id': int(best.pseudo_id),
                       'distance_position': int(abs(int(best.pos) - int(r.pos_premier)))})
    details['FJ-05_appariement'] = {'episodes_candidats': int(len(cand)), 'paires': int(len(paires)),
                                    'non_apparies': int(len(non_app)),
                                    'motifs_non_apparies': pd.Series([x['motif'] for x in non_app]).value_counts().to_dict() if non_app else {},
                                    'distances_position': paires,
                                    'seuils_terciles_par_session': {k: list(v) for k, v in seuils_terc.items()}}
    ep_ids = [p['episode_id'] for p in paires]; ps_ids = [p['pseudo_id'] for p in paires]
    ep_p = EP[EP.episode_id.isin(ep_ids)].copy(); ps_p = PS[PS.pseudo_id.isin(ps_ids)].copy()
    ep_p = ep_p[np.isfinite(ep_p.R60)]; ps_p = ps_p[np.isfinite(ps_p.R60)]
    paires_valides = [(e, p) for e, p in paires if e in set(ep_p.episode_id) and p in set(ps_p.pseudo_id)]
    details['FJ-05_appariement']['paires_deux_R60'] = int(len(paires_valides))
    # composition ere x session (bras apparies utilises)
    def parts_ere(df):
        v = df.ere.value_counts(normalize=True)
        return {e: float(v.get(e, 0.0)) for e in ['2010_2013', '2014_2016', '2017_2020']}
    pe, pp = parts_ere(ep_p), parts_ere(ps_p)
    compo_sensible = any(min(pe[e], pp[e]) < 0.10 for e in pe) or any(abs(pe[e] - pp[e]) > 0.10 for e in pe)
    details['FJ-05_composition'] = {'parts_ere_episodes': pe, 'parts_ere_pseudos': pp,
                                    'COMPOSITION_SENSIBLE': bool(compo_sensible),
                                    'effectifs_ere_x_session_episodes': ep_p.groupby(['ere', 'session']).size().astype(int).to_dict() if len(ep_p) else {},
                                    'effectifs_ere_x_session_pseudos': ps_p.groupby(['ere', 'session']).size().astype(int).to_dict() if len(ps_p) else {}}
    details['FJ-05_composition'] = json.loads(json.dumps(details['FJ-05_composition'], default=str))

    res = {}; diags = {}; flags = {}
    for cid, (a, b, _) in comparaisons.items():
        units, racines, diag = prep(a, b)
        res[cid] = boot_medianes(units, racines); diags[cid] = diag
        parts = diag['part_plus_grande_grappe_par_bras']
        flags[cid] = {'GRAPPE_DOMINANTE': bool(max(parts.values()) > 0.05) if parts else False}
    # FJ-05 unites jointes (episodes bras 0, pseudos bras 1, aretes d'appariement)
    ep_map = {int(r.episode_id): r for r in ep_p.itertuples()}; ps_map = {int(r.pseudo_id): r for r in ps_p.itertuples()}
    units5 = []
    for e, p in paires_valides:
        r = ep_map[e]
        units5.append({'jour': r.date, 'ancrage': int(r.t_dernier), 'chocs': [int(x) for x in str(r.chocs_t).split(';')], 'bras': 0, 'valeur': float(r.R60)})
    base5 = len(units5)
    for j, (e, p) in enumerate(paires_valides):
        r = ps_map[p]
        units5.append({'jour': r.date, 'ancrage': int(r.t), 'chocs': [int(r.t)], 'bras': 1, 'valeur': float(r.R60), 'pair': j})
        units5[j]['pair'] = base5 + j
    racines5, diag5 = construire_grappes(units5)
    res['FJ-05'] = boot_medianes(units5, racines5); diags['FJ-05'] = diag5
    flags['FJ-05'] = {'GRAPPE_DOMINANTE': bool(max(diag5['part_plus_grande_grappe_par_bras'].values()) > 0.05),
                      'COMPOSITION_SENSIBLE': bool(compo_sensible)}
    details['diagnostics_grappes'] = diags
    # ventilations descriptives par session (sans test)
    vent = {}
    for cid, df in [('episodes_clos_non_mixtes_R60', base), ('pseudos_apparies', ps_p)]:
        vent[cid] = {ses: {'n': int(len(df[df.session == ses])), 'mediane_R60': float(df[df.session == ses].R60.median()) if len(df[df.session == ses]) else None} for ses in ['S1', 'S2', 'S3', 'S4']}
    details['ventilation_session'] = vent
    details['descriptifs'] = {
        'mediane_R60_isoles_positifs': float(isol[isol.classe == 'POSITIF'].R60.median()) if len(isol) else None,
        'mediane_R60_isoles_negatifs': float(isol[isol.classe == 'NEGATIF'].R60.median()) if len(isol) else None,
        'mediane_R60_regroupes': float(regr.R60.median()) if len(regr) else None,
        'taux_nouveau_choc_episodes': float(base.nouveau_choc.dropna().mean()) if base.nouveau_choc.notna().any() else None,
        'taux_nouveau_choc_pseudos_apparies': float(ps_p.nouveau_choc.dropna().mean()) if len(ps_p) and ps_p.nouveau_choc.notna().any() else None,
        'mediane_stabilisation_episodes': float(base.stabilisation.median()) if base.stabilisation.notna().any() else None}

    META = [('FJ-01', 'R_60 isoles POSITIFS vs NEGATIFS'), ('FJ-02', 'R_60 regroupes vs isoles'),
            ('FJ-03', 'R_60 isoles MAJEURS (I_ep>=2) vs MODERES (1<I_ep<2)'),
            ('FJ-04', 'R_60 isoles 2010-2013 vs 2017-2020'), ('FJ-05', 'R_60 isoles apparies vs pseudo-evenements')]
    rows = []
    for cid, label in META:
        stat, lo, hi, p, na, nb, ga, gb = res[cid]
        materiel = bool(abs(stat) >= 10.0) if np.isfinite(stat) else False
        rows.append({'id': cid, 'comparaison': label, 'variable': 'R_60 (bp, diff. de medianes)',
                     'statistique': stat, 'ic95_bas': lo, 'ic95_haut': hi, 'p_brute': p,
                     'n_a': na, 'n_b': nb, 'grappes_a': ga, 'grappes_b': gb,
                     'seuil_materiel_bp': 10.0, 'materiel': materiel,
                     'grappe_dominante': flags[cid]['GRAPPE_DOMINANTE'],
                     'composition_sensible': flags[cid].get('COMPOSITION_SENSIBLE', False)})
    comp = pd.DataFrame(rows)
    comp['q_BY_m5'] = BY_m5(comp.p_brute.values)
    def lecture(r):
        if not np.isfinite(r.p_brute): return 'STRUCTURELLEMENT_NON_EVALUABLE'
        if r.id == 'FJ-05':
            if not (r.n_a >= 200 and r.n_b >= 200 and r.grappes_a >= 100 and r.grappes_b >= 100): return 'NON_EVALUABLE (comparabilite insuffisante)'
        elif not (r.n_a >= 200 and r.n_b >= 200 and r.grappes_a >= 100 and r.grappes_b >= 100): return 'NON_ELIGIBLE (effectifs publies)'
        if r.q_BY_m5 < 0.05 and r.materiel:
            if r.grappe_dominante or r.composition_sensible: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL (plafond: grappe dominante et/ou composition sensible)'
            return 'CANDIDATE_J1'
        if r.q_BY_m5 < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture, axis=1)
    comp.round(6).to_csv(ROOT / 'CAMPAIGN_08_COMPARISONS.csv', index=False)
    (ROOT / 'CAMPAIGN_08_DETAILS.json').write_text(json.dumps(details, indent=1, default=str))
    print(comp.to_string(index=False))

if __name__ == '__main__': main()
