"""PHASE 11-C - anatomie descriptive des grands mouvements H1/H4.
Protocole PHASE 11-A gele (sha256 fdfb04ed...), autorisation seq305.
Populations fermees F10-01 (3107 admissibles) et F10-03 (660), identifiants
PHASE 11-B.1 (aucun nouveau clustering). Trajectoires Mid depuis les barres
M1 IS; aucune rentabilite, aucune p-value. Bootstrap grappes descriptif
2000 repetitions, graine 20261122."""
import glob, json, os, pathlib, sys
import numpy as np
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase10_engine import construire_barres

ROOT = pathlib.Path('reports/meta_alpha/phase11'); ROOT.mkdir(parents=True, exist_ok=True)
SESSIONS = [(0, 'ASIA'), (8, 'LONDON'), (13, 'LONDON_NY_OVERLAP'), (17, 'NY_AFTERNOON'), (21, 'NIGHT_OTHER')]

def session_de(h):
    for borne, nom in reversed(SESSIONS):
        if h >= borne: return nom
    return 'ASIA'

def fermeture_reguliere(fin_precedente):
    return fin_precedente.hour >= 20 or fin_precedente.weekday() >= 4

def charger_barres():
    dossier = os.environ.get('BARS_DIR', 'bars_artifacts')
    fs = sorted(glob.glob(f'{dossier}/**/P10_BARS_*.csv.gz', recursive=True))
    if len(fs) < 8: raise RuntimeError(f'integrite lots: {len(fs)}/8 fichiers de barres')
    bars = pd.concat([pd.read_csv(f) for f in fs])
    bars['ts'] = pd.to_datetime(bars.ts)
    return bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True), len(fs)

def analyser_event(ev_row, tf_bars, trig_idx, M, minutes_tf):
    """M: arrays M1 (ts_min, mo, mh, ml, mc). Retourne dict de mesures."""
    d = int(ev_row.sens); t0 = pd.Timestamp(ev_row.t_signal)
    trig = tf_bars.iloc[trig_idx]
    P0 = float(trig.mc)
    ts_min, mo, mh, ml, mc = M
    t0min = int(t0.value // 60_000_000_000)
    # --- barres de trajectoire et censure ---
    chemin, motif_censure = [], 'COMPLETE'
    fin_prec = t0
    for k in range(1, 9):
        j = trig_idx + k
        if j >= len(tf_bars): motif_censure = 'FIN_COUVERTURE'; break
        b = tf_bars.iloc[j]
        ecart = (b.debut - fin_prec) / pd.Timedelta(minutes=1)
        if ecart > minutes_tf and not fermeture_reguliere(fin_prec):
            motif_censure = 'LACUNE_ANORMALE'; break
        chemin.append(b); fin_prec = b.fin
    horizon = len(chemin)
    R = {'t0': str(t0), 'P0': P0, 'direction': d, 'horizon_atteint': horizon,
         'statut_censure': 'COMPLETE' if horizon == 8 else motif_censure,
         'session_declenchement': session_de(t0.hour)}
    if horizon == 0:
        return R
    fin_fenetre = chemin[-1].fin
    i0 = int(np.searchsorted(ts_min, t0min))
    i1 = int(np.searchsorted(ts_min, int(fin_fenetre.value // 60_000_000_000)))
    s_mh, s_ml, s_mc, s_ts = mh[i0:i1], ml[i0:i1], mc[i0:i1], ts_min[i0:i1]
    if len(s_mc) == 0:
        R['statut_censure'] = 'DONNEES_M1_ABSENTES'; R['horizon_atteint'] = 0; return R
    R['temps_marche_minutes'] = int(len(s_mc))
    R['temps_calendaire_minutes'] = int((fin_fenetre - t0) / pd.Timedelta(minutes=1))
    y = d * 10000 * np.log(s_mc / P0)  # clotures M1 orientees (bp)
    if d > 0:
        fav_px = np.maximum.accumulate(s_mh); adv_px = np.minimum.accumulate(s_ml)
        fav_bp = 10000 * np.log(fav_px / P0); adv_bp = 10000 * np.log(P0 / adv_px)
        extreme_decl = float(trig.mh)
    else:
        fav_px = np.minimum.accumulate(s_ml); adv_px = np.maximum.accumulate(s_mh)
        fav_bp = 10000 * np.log(P0 / fav_px); adv_bp = 10000 * np.log(adv_px / P0)
        extreme_decl = float(trig.ml)
    # bornes de fin de chaque bougie de trajectoire (en minutes)
    fins = [int(b.fin.value // 60_000_000_000) for b in chemin]
    for k in range(1, 9):
        if k <= horizon:
            ik = int(np.searchsorted(s_ts, fins[k - 1]))
            R[f'mfe_{k}'] = float(max(0.0, fav_bp[:ik].max())) if ik else 0.0
            R[f'mae_{k}'] = float(max(0.0, adv_bp[:ik].max())) if ik else 0.0
            R[f'disp_{k}'] = float(y[ik - 1]) if ik else np.nan
        else:
            R[f'mfe_{k}'] = np.nan; R[f'mae_{k}'] = np.nan; R[f'disp_{k}'] = np.nan
    def minute_iso(idx):
        return str(pd.Timestamp(s_ts[idx], unit='m')) if 0 <= idx < len(s_ts) else None
    imfe = int(np.argmax(fav_bp)); imae = int(np.argmax(adv_bp))
    R['mfe_max_bp'] = float(fav_bp[imfe]); R['mae_max_bp'] = float(adv_bp[imae])
    R['mfe_extreme_minute_start_utc'] = minute_iso(imfe); R['mae_extreme_minute_start_utc'] = minute_iso(imae)
    R['mfe_extreme_available_at_utc'] = str(pd.Timestamp(s_ts[imfe], unit='m') + pd.Timedelta(minutes=1)) if len(s_ts) else None
    R['mae_extreme_available_at_utc'] = str(pd.Timestamp(s_ts[imae], unit='m') + pd.Timedelta(minutes=1)) if len(s_ts) else None
    R['extreme_timestamp_resolution'] = 'M1'
    R['session_mfe'] = session_de(pd.Timestamp(s_ts[imfe], unit='m').hour) if len(s_ts) else None
    R['session_mae'] = session_de(pd.Timestamp(s_ts[imae], unit='m').hour) if len(s_ts) else None
    # --- extension confirmee, repli (clotures), reprise ---
    best = np.maximum.accumulate(y)
    ext_idx = np.where(y > 0)[0]
    extension = len(ext_idx) > 0
    R['extension_confirmee'] = int(extension)
    repli_start, best_avant_repli = None, None
    if extension:
        for mIdx in range(len(y)):
            if best[mIdx] > 0 and y[mIdx] < best[mIdx]:
                repli_start, best_avant_repli = mIdx, float(best[mIdx]); break
    R['repli_present'] = int(repli_start is not None)
    # repli depuis l'extreme favorable (extrema, minute du sommet exclue pour ne pas inventer d'ordre intraminute)
    profondeur, i_repli_ext, i_sommet = 0.0, None, None
    if d > 0:
        sommet = np.maximum.accumulate(s_mh)
        for mIdx in range(1, len(y)):
            prof = 10000 * np.log(sommet[mIdx - 1] / s_ml[mIdx])
            if prof > profondeur: profondeur, i_repli_ext, i_sommet = float(prof), mIdx, int(np.argmax(s_mh[:mIdx]))
    else:
        creux = np.minimum.accumulate(s_ml)
        for mIdx in range(1, len(y)):
            prof = 10000 * np.log(s_mh[mIdx] / creux[mIdx - 1])
            if prof > profondeur: profondeur, i_repli_ext, i_sommet = float(prof), mIdx, int(np.argmax(-s_ml[:mIdx]))
    R['repli_profondeur_max_bp'] = profondeur
    R['repli_extreme_minute_start_utc'] = minute_iso(i_repli_ext) if i_repli_ext is not None else None
    R['repli_duree_minutes'] = int(s_ts[i_repli_ext] - s_ts[i_sommet]) if (i_repli_ext is not None and i_sommet is not None) else None
    R['session_repli'] = session_de(pd.Timestamp(s_ts[i_repli_ext], unit='m').hour) if i_repli_ext is not None else None
    # ordre intraminute indetermine: sommet favorable et extreme de repli dans la meme minute (calcul inclusif)
    intra = False
    if i_repli_ext is not None and i_sommet is not None and s_ts[i_repli_ext] == s_ts[i_sommet]: intra = True
    R['intra_minute_order_unknown'] = int(intra)
    if repli_start is not None:
        R['repli_debut_minute_start_utc'] = minute_iso(repli_start)
        apres = np.where(y[repli_start + 1:] > best_avant_repli)[0]
        R['reprise_apres_repli'] = int(len(apres) > 0)
        R['reprise_minute_start_utc'] = minute_iso(repli_start + 1 + int(apres[0])) if len(apres) else None
    else:
        R['reprise_apres_repli'] = 0; R['reprise_minute_start_utc'] = None; R['repli_debut_minute_start_utc'] = None
    R['session_reprise'] = session_de(pd.Timestamp(R['reprise_minute_start_utc']).hour) if R['reprise_minute_start_utc'] else None
    # --- touche et reintegration de P0 ---
    touche = np.where(adv_bp > 0)[0]
    R['touche_P0'] = int(len(touche) > 0)
    R['touche_delai_minutes'] = int(s_ts[touche[0]] - t0min) if len(touche) else None
    R['touche_minute_start_utc'] = minute_iso(int(touche[0])) if len(touche) else None
    R['session_touche'] = session_de(pd.Timestamp(s_ts[touche[0]], unit='m').hour) if len(touche) else None
    reint, best_avant_reint = None, None
    if extension:
        premier_ext = int(ext_idx[0])
        cand = np.where(y[p
...[truncated 14062 chars]