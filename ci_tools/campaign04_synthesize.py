"""CAMPAGNE 4 - synthese descriptive. Bootstrap par blocs mobiles de 20
journees (2000 replicats, graine 20261113): etats, episodes, transitions et
fenetres RECALCULES dans chaque replicat (dictionnaire v2 / comparaisons
gelees). Aucune hypothese ajoutee."""
import pathlib, json, sys
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')
from campaign04_engine import tercile_causal, episodes_et_transitions

ROOT = pathlib.Path('reports/meta_alpha/campaign04')
RNG = np.random.default_rng(20261113)
B = 2000
LBL = {'BAS': 0, 'MOYEN': 1, 'HAUT': 2}

def fenetres(J, trans_conf, trans_all_candidates):
    """Ajoute aux transitions confirmees les stats de fenetre +1-5 / +6-20
    apres D, tronquees a la veille de la prochaine candidate."""
    cand = sorted(trans_all_candidates)
    out = []
    n = len(J)
    for t in trans_conf:
        D = t['confirmation_idx']
        suiv = [c for c in cand if c > t['candidate_idx']]
        borne = (min(suiv) - 1) if suiv else n - 1
        for nom, a, b in [('+1_5', 1, 5), ('+6_20', 6, 20)]:
            i0, i1 = D + a, min(D + b, borne)
            if i1 >= i0 and i0 < n:
                w = J.iloc[i0:i1 + 1]
                t[f'rv_med{nom}'] = float(w.rv_bp.median()); t[f'freq_ext{nom}'] = float(w.freq_extremes.mean())
                t[f'skew_med{nom}'] = float(w['skew'].median()); t[f'imp_par_jour{nom}'] = float(w.imp_m5_count.mean())
                t[f'n_fenetre{nom}'] = int(len(w)); t[f'tronquee{nom}'] = bool(i1 < D + b)
            else:
                t[f'rv_med{nom}'] = np.nan; t[f'freq_ext{nom}'] = np.nan; t[f'skew_med{nom}'] = np.nan
                t[f'imp_par_jour{nom}'] = np.nan; t[f'n_fenetre{nom}'] = 0; t[f'tronquee{nom}'] = True
        out.append(t)
    return out

def construire_transitions(J):
    """Depuis la serie d'etats de J: episodes, transitions d'episodes,
    transitions confirmees entre episodes confirmes (len>=3), catalogue."""
    eps, trans_ep = episodes_et_transitions(J.etat_courant.values)
    for e in eps:
        e['date_debut'] = str(J.date.iloc[e['debut']]); e['date_fin'] = str(J.date.iloc[e['fin']])
        e['duree'] = int(e['fin'] - e['debut'] + 1); e['ere'] = str(J.ere.iloc[e['debut']])
        e['censure_bord'] = bool(e['debut'] == 0 or e['fin'] == len(J) - 1)
    conf_eps = [e for e in eps if e['duree'] >= 3]
    trans_conf = []
    for a, b in zip(conf_eps, conf_eps[1:]):
        C = a['fin'] + 1
        trav = int(b['debut'] - a['fin'])
        trans_conf.append({'candidate_idx': C, 'date_candidate': str(J.date.iloc[C]) if C < len(J) else None,
                           'depuis': a['etat'], 'vers': b['etat'], 'confirmee': True,
                           'confirmation_idx': b['debut'] + 2, 'date_confirmation': str(J.date.iloc[b['debut'] + 2]),
                           'traversee': trav, 'vitesse': 'RAPIDE' if trav <= 2 else ('INTERMEDIAIRE' if trav <= 4 else 'PROGRESSIVE'),
                           'ere': str(J.ere.iloc[C])})
    catalogue = []
    for t in trans_ep:
        b = eps[[e['debut'] for e in eps].index(t['candidate_idx'])] if t['candidate_idx'] in [e['debut'] for e in eps] else None
        catalogue.append({**t, 'date_candidate': str(J.date.iloc[t['candidate_idx']]),
                          'date_confirmation': (str(J.date.iloc[t['confirmation_idx']]) if t['confirmation_idx'] is not None else None),
                          'ere': str(J.ere.iloc[t['candidate_idx']])})
    return eps, trans_conf, catalogue

def retours_habituel(J, eps):
    rows = []
    for e in eps:
        if e['etat'] != 'HAUT': continue
        rstar = J.mediane_rv_60.iloc[e['debut']]
        if pd.isna(rstar): continue
        tps, cens = None, True
        for k in range(e['fin'] + 1, min(e['fin'] + 61, len(J))):
            if J.rv_bp.iloc[k] < rstar: tps = k - e['fin']; cens = False; break
        rows.append({'date_debut': e['date_debut'], 'ere': e['ere'], 'reference_figee_bp': float(rstar),
                     'temps_retour_jours': tps, 'censure': cens})
    return rows

def stats_comparaisons(J, sess_max_etat):
    """Calcule les 10 statistiques (differences A-B ou ratios) sur une serie
    journaliere donnee (observee ou replicat). Retourne dict id -> (stat, na, nb, ja, jb)."""
    J = J.reset_index(drop=True)
    eps, trans_conf, catalogue = construire_transitions(J)
    cand_idx = [t['candidate_idx'] for t in catalogue]
    tc = fenetres(J.copy(), [dict(t) for t in trans_conf], cand_idx)
    res = {}
    def med(col, bras):
        a = [t[col] for t in tc if bras(t, 'A') and not pd.isna(t[col])]
        b = [t[col] for t in tc if bras(t, 'B') and not pd.isna(t[col])]
        return a, b
    # C4-01 RV fenetre ->HAUT vs ->BAS
    a, b = med('rv_med+1_5', lambda t, s: (t['vers'] == 'HAUT') if s == 'A' else (t['vers'] == 'BAS'))
    res['C4-01'] = (np.median(a) / np.median(b) if a and b and np.median(b) != 0 else np.nan, len(a), len(b))
    # C4-02 freq extremes confirmee vs non confirmee (apres D / apres C)
    def freq_fenetre(ref):
        i0, i1 = ref + 1, min(ref + 5, len(J) - 1)
        return float(J.freq_extremes.iloc[i0:i1 + 1].mean()) if i1 >= i0 else np.nan
    ca = [freq_fenetre(t['confirmation_idx']) for t in trans_conf]
    nc = [freq_fenetre(t['candidate_idx']) for t in catalogue if not t['confirmee']]
    ca = [x for x in ca if not np.isnan(x)]; nc = [x for x in nc if not np.isnan(x)]
    res['C4-02'] = ((np.mean(ca) - np.mean(nc)) * 100 if ca and nc else np.nan, len(ca), len(nc))
    # C4-03 durees HAUT vs BAS (bords exclus)
    da = [e['duree'] for e in eps if e['etat'] == 'HAUT' and not e['censure_bord']]
    db = [e['duree'] for e in eps if e['etat'] == 'BAS' and not e['censure_bord']]
    res['C4-03'] = (np.median(da) / np.median(db) if da and db else np.nan, len(da), len(db))
    # C4-04 retours par ere
    R = retours_habituel(J, eps)
    ra = [r['temps_retour_jours'] for r in R if r['ere'] == '2010_2013' and r['temps_retour_jours'] is not None]
    rb = [r['temps_retour_jours'] for r in R if r['ere'] == '2017_2020' and r['temps_retour_jours'] is not None]
    res['C4-04'] = (np.median(ra) / np.median(rb) if ra and rb and np.median(rb) != 0 else np.nan, len(ra), len(rb))
    # C4-05 part rapide ->HAUT vs ->BAS
    pa = [t['vitesse'] == 'RAPIDE' for t in trans_conf if t['vers'] == 'HAUT']
    pb = [t['vitesse'] == 'RAPIDE' for t in trans_conf if t['vers'] == 'BAS']
    res['C4-05'] = ((np.mean(pa) - np.mean(pb)) if pa and pb else np.nan, len(pa), len(pb))
    # C4-06 skew fenetre
    a, b = med('skew_med+1_5', lambda t, s: (t['vers'] == 'HAUT') if s == 'A' else (t['vers'] == 'BAS'))
    res['C4-06'] = ((np.median(a) - np.median(b)) if a and b else np.nan, len(a), len(b))
    # journees: discordance, etat, queue veille
    cls = (J.etat_courant != 'NON_CLASSE') & (J.f3_tercile_causal != 'NON_CLASSE')
    disc = (J.etat_courant != J.f3_tercile_causal)
    ja = cls & (J.ere == '2010_2013'); jb = cls & (J.ere == '2017_2020')
    res['C4-07'] = ((disc[ja].mean() - disc[jb].mean()) if ja.sum() and jb.sum() else np.nan, int(ja.sum()), int(jb.sum()))
    ha = J.etat_courant == 'HAUT'; ba = J.etat_courant == 'BAS'
    res['C4-08'] = ((J.imp_m5_count[ha].mean() / J.imp_m5_count[ba].mean()) if ha.sum() and ba.sum() and J.imp_m5_count[ba].mean() > 0 else np.nan, int(ha.sum()), int(ba.sum()))
    if sess_max_etat is not None:
        dep = pd.Series([ (sess_max_etat.get(str(d), None) is not None and J.etat_courant.iloc[i] in LBL and sess_max_etat.get(str(d)) != J.etat_courant.iloc[i]) for i, d in enumerate(J.date)], index=J.index)
        res['C4-09'] = ((dep[ha].mean() - dep[ba].mean()) if ha.sum() and ba.sum() else np.nan, int(ha.sum()), int(ba.sum()))
    else:
        res['C4-09'] = (np.nan, 0, 0)
    qv = J.etat_queue.shift(1)
    qa = qv == 'HAUT'; qb = qv == 'BAS'
    res['C4-10'] = (((J.freq_extremes[qa].mean() - J.freq_extremes[qb].mean()) * 100) if qa.sum() and qb.sum() else np.nan, int(qa.sum()), int(qb.sum()))
    return res, eps, tc, catalogue, R

META = {
 'C4-01': ('med', 'ratio', "RV mediane +1-5j apres transition confirmee ->HAUT vs ->BAS"),
 'C4-02': ('prop', 'diff', "Frequence d'extremes +1-5j, transitions confirmees vs non confirmees (sens apparie)"),
 'C4-03': ('med', 'ratio', "Duree mediane des episodes HAUT vs BAS"),
 'C4-04': ('med', 'ratio', "Temps de retour a l'habituel apres HAUT, ere 2010-13 vs 2017-20"),
 'C4-05': ('prop', 'diff', "Part des traversees rapides parmi les confirmees ->HAUT vs ->BAS"),
 'C4-06': ('med', 'diff', "Asymetrie mediane +1-5j apres transition confirmee ->HAUT vs ->BAS"),
 'C4-07': ('prop', 'diff', "Part des journees en discordance F3 causal, ere 2010-13 vs 2017-20"),
 'C4-08': ('med', 'ratio', "Impulsions IMP-M5 par journee, etat courant HAUT vs BAS"),
 'C4-09': ('prop', 'diff', "Part des journees a dephasage session/journalier, etat HAUT vs BAS"),
 'C4-10': ('prop', 'diff', "Frequence d'extremes du jour selon l'etat de queue de la veille HAUT vs BAS")}

def BY(pvals):
    p = np.asarray(pvals, float); m = len(p); H = sum(1 / i for i in range(1, m + 1))
    o = np.argsort(p); q = p[o] * m * H / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty(m); out[o] = np.minimum(q, 1.0)
    return out

def blocs_indices(n, L=20):
    starts = RNG.integers(0, n, size=int(np.ceil(n / L)))
    idx = np.concatenate([np.arange(s, s + L) % n for s in starts])[:n]
    return idx

def main():
    J = pd.read_csv(ROOT / 'CAMPAIGN_04_DAILY.csv.gz')
    J['date'] = J.date.astype(str)
    S = pd.read_csv(ROOT / 'CAMPAIGN_04_SESSIONS.csv.gz')
    sess_max = {}
    for d, g in S.groupby(S.date.astype(str)):
        vals = [LBL[x] for x in g.etat_session if x in LBL]
        if vals: sess_max[d] = ['BAS', 'MOYEN', 'HAUT'][max(vals)]
    obs, eps, tc, catalogue, R = stats_comparaisons(J, sess_max)
    # catalogue complet des transitions et episodes (publications)
    pd.DataFrame(catalogue).to_csv(ROOT / 'CAMPAIGN_04_TRANSITIONS.csv', index=False)
    pd.DataFrame([{**e} for e in eps]).to_csv(ROOT / 'CAMPAIGN_04_EPISODES.csv', index=False)
    pd.DataFrame([{**t} for t in tc]).to_csv(ROOT / 'CAMPAIGN_04_TRANSITIONS_CONFIRMEES.csv', index=False)
    pd.DataFrame(R).to_csv(ROOT / 'CAMPAIGN_04_RETOURS.csv', index=False)
    # bootstrap par blocs mobiles 20 journees, recalcul complet par replicat
    n = len(J)
    boot = {k: [] for k in META}
    excl = {k: 0 for k in META}
    for rep in range(B):
        idx = blocs_indices(n)
        Jr = J.iloc[idx].copy()
        # etats recalcules dans le replicat depuis les series echantillonnees
        Jr['etat_courant'], _, _ = tercile_causal(Jr.rv_bp.values, 60, 40)
        Jr['f3_tercile_causal'], _, _ = tercile_causal(Jr.pred_har.values, 250, 60)
        Jr['etat_queue'], _, _ = tercile_causal(Jr.freq_extremes.values, 60, 40)
        Jr['mediane_rv_60'] = pd.Series(Jr.rv_bp.values).shift(1).rolling(60, min_periods=40).median().values
        try:
            rr, *_ = stats_comparaisons(Jr, sess_max)
        except Exception:
            for k in META: excl[k] += 1
            continue
        for k in META:
            v = rr[k][0]
            if v is None or (isinstance(v, float) and np.isnan(v)): excl[k] += 1
            else: boot[k].append(v)
        if rep % 200 == 0: print('replicat', rep, flush=True)
    rows = []
    for cid, (typ, mode, label) in META.items():
        stat, na, nb = obs[cid]
        arr = np.array(boot[cid], float)
        if mode == 'ratio':
            lo, hi = np.percentile(np.log(arr), [2.5, 97.5]); lo, hi = float(np.exp(lo)), float(np.exp(hi))
            centre = np.log(stat) if stat and stat > 0 else np.nan
            p = 2 * min((np.log(arr) <= 0).mean(), (np.log(arr) >= 0).mean()) if len(arr) else 1.0
            mat = (stat >= 1.15 or stat <= 1 / 1.15) if stat == stat else False
        elif cid == 'C4-06':
            lo, hi = np.percentile(arr, [2.5, 97.5])
            p = 2 * min((arr <= 0).mean(), (arr >= 0).mean()) if len(arr) else 1.0
            mat = abs(stat) >= 0.10 if stat == stat else False
        else:
            lo, hi = np.percentile(arr, [2.5, 97.5])
            p = 2 * min((arr <= 0).mean(), (arr >= 0).mean()) if len(arr) else 1.0
            mat = abs(stat) >= 0.05 if stat == stat else False
        rows.append({'id': cid, 'comparaison': label, 'type': typ, 'statistique': stat, 'ic95_bas': float(lo), 'ic95_haut': float(hi),
                     'p_brute': float(min(max(p, 1 / max(len(arr), 1)), 1.0)), 'n_a': na, 'n_b': nb, 'replicats_valides': len(arr),
                     'replicats_exclus': excl[cid], 'materiel': bool(mat)})
    comp = pd.DataFrame(rows)
    comp['q_BY'] = BY(comp.p_brute.values)
    trans_ids = {'C4-01', 'C4-02', 'C4-05', 'C4-06'}
    def lecture(r):
        elig = (r.n_a >= (30 if r.id in trans_ids or r.id in ('C4-03', 'C4-04') else 200) and r.n_b >= (30 if r.id in trans_ids or r.id in ('C4-03', 'C4-04') else 200))
        # pour transitions: n en transitions; journees: fenetres deja conditionnees; regle publiee au PV
        if not elig: return 'NON_ELIGIBLE (effectifs publies)'
        if r.q_BY < 0.05 and r.materiel: return 'CANDIDATE_J1'
        if r.q_BY < 0.05: return 'SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL'
        return 'NEGATIF'
    comp['lecture'] = comp.apply(lecture, axis=1)
    comp.round(5).to_csv(ROOT / 'CAMPAIGN_04_COMPARISONS.csv', index=False)
    # statistiques descriptives d'etats et de transitions
    st = []
    for col in ['etat_courant', 'f3_tercile_causal', 'etat_asymetrie', 'etat_queue', 'etat_vov', 'etat_dispersion']:
        for k, g in J.groupby(col):
            st.append({'dimension': col, 'modalite': k, 'journees': len(g), 'part_pct': round(100 * len(g) / len(J), 2),
                       'rv_mediane_bp': round(float(g.rv_bp.median()), 2)})
    for k, g in pd.DataFrame(catalogue).groupby(['depuis', 'vers', 'confirmee']) if len(catalogue) else []:
        st.append({'dimension': 'transition_episode', 'modalite': f"{k[0]}->{k[1]} confirmee={k[2]}", 'journees': len(g), 'part_pct': np.nan, 'rv_mediane_bp': np.nan})
    pd.DataFrame(st).to_csv(ROOT / 'CAMPAIGN_04_STATE_STATS.csv', index=False)
    print(comp.to_string(index=False))
    print('episodes', len(eps), 'transitions confirmees (inter-episodes confirmes)', len(tc), 'catalogue', len(catalogue), 'retours', len(R))

if __name__ == '__main__': main()
