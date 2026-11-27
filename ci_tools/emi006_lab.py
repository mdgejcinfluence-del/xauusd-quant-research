#!/usr/bin/env python3
"""EMI-006 lab: causal discrimination persistence vs cadence vs extra condition.

Reads frozen DIRR-003 trajectories (ts, mid, pwa, pnl_latent_bp). All state
computations are tick-by-tick, past-only. No look-ahead: the real close is
only used *after* replay to score errors.
"""
import json, pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
SRC = R / 'docs/checkpoints/DEEP_INVENTORY_RECOVERY_003'
OUT = R / 'docs/checkpoints/EXIT_MECHANISM_IDENTIFICATION_006'
OUT.mkdir(parents=True, exist_ok=True)
BASKETS = 'ABCDE'
THETAS = [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0]


def segments(df, theta):
    """Contiguous favourable segments (pnl>=theta). Returns list of dicts."""
    fav = (df.pnl_latent_bp.values >= theta)
    ts = df.ts.values
    segs, i, n = [], 0, len(df)
    while i < n:
        if fav[i]:
            j = i
            while j + 1 < n and fav[j + 1]:
                j += 1
            segs.append({'start_idx': i, 'end_idx': j,
                         'start': pd.Timestamp(ts[i]), 'end': pd.Timestamp(ts[j]),
                         'dur_s': (pd.Timestamp(ts[j]) - pd.Timestamp(ts[i])).total_seconds(),
                         'ticks': j - i + 1})
            i = j + 1
        else:
            i += 1
    return segs


def merged_segments(df, theta, tol_s):
    """Segments merging interruptions <= tol_s (time gap between segments)."""
    segs = segments(df, theta)
    if not segs:
        return segs
    out = [dict(segs[0])]
    for s in segs[1:]:
        gap = (s['start'] - out[-1]['end']).total_seconds()
        if gap <= tol_s:
            out[-1]['end'] = s['end']; out[-1]['end_idx'] = s['end_idx']
            out[-1]['dur_s'] = (s['end'] - out[-1]['start']).total_seconds()
            out[-1]['ticks'] += s['ticks']; out[-1].setdefault('interruptions', 0)
            out[-1]['interruptions'] += 1
        else:
            out.append(dict(s))
    return out


def persistence_interval(segs, close_ts):
    """Continuous persistence: compatible T in (max earlier dur, final dur]."""
    if not segs:
        return None, None, None
    final = segs[-1]
    earlier = [s['dur_s'] for s in segs[:-1]]
    return (max(earlier) if earlier else 0.0), final['dur_s'], final


def cadence_compatible(df, final_start, close_ts, max_n=300, tol_s=1.0):
    """Cadences N anchored at basket open: a grid point in [final_start, close]
    and close within tol_s after the last such grid point; and no grid point
    after an earlier favourable segment start that persisted... (kept simple &
    declared): grid point >= final_start, close-gridpoint <= tol_s."""
    t0 = df.ts.iloc[0]
    good = []
    for N in range(1, max_n + 1):
        k = np.floor((close_ts - t0).total_seconds() / N)
        gp = t0 + pd.Timedelta(seconds=float(k * N))
        if gp >= final_start and (close_ts - gp).total_seconds() <= tol_s:
            good.append(N)
    return good


def main():
    timelines, transitions, compat, replay_rows, false_rows = [], [], [], [], []
    summary = {}
    for b in BASKETS:
        df = pd.read_csv(SRC / f'TRAJECTORY_{b}.csv', parse_dates=['ts'])
        close_ts = df.ts.iloc[-1]
        open_ts = df.ts.iloc[0]
        pwa_chg = df[df.pwa.round(4).diff().fillna(0) != 0].ts
        last_pos_chg = pwa_chg.iloc[-1] if len(pwa_chg) else open_ts
        pnl = df.pnl_latent_bp.values
        # local highs / retracements on running max of pnl (past-only)
        runmax = np.maximum.accumulate(pnl)
        summary[b] = {'open': str(open_ts), 'close': str(close_ts),
                      'duration_s': (close_ts - open_ts).total_seconds(),
                      'ticks': len(df), 'pnl_close_bp': float(pnl[-1])}
        for theta in THETAS:
            segs = segments(df, theta)
            lo, hi, final = persistence_interval(segs, close_ts)
            if final is None:
                compat.append({'panier': b, 'theta_bp': theta, 'modele': 'P_continu',
                               'borne_inf_s': None, 'borne_sup_s': None, 'n_segments': 0,
                               'statut': 'JAMAIS_FAVORABLE'})
                continue
            close_in = bool(final['end'] == close_ts)
            compat.append({'panier': b, 'theta_bp': theta, 'modele': 'P_continu',
                           'borne_inf_s': lo, 'borne_sup_s': hi, 'n_segments': len(segs),
                           'statut': 'INTERVALLE' if close_in else 'CLOTURE_HORS_ETAT (segment final termine avant cloture)'})
            for tol in (0.5, 1.0, 2.0):
                ms = merged_segments(df, theta, tol)
                lo2, hi2, _ = persistence_interval(ms, close_ts)
                compat.append({'panier': b, 'theta_bp': theta, 'modele': f'P_tolerance_{tol}s',
                               'borne_inf_s': lo2, 'borne_sup_s': hi2, 'n_segments': len(ms),
                               'statut': 'INTERVALLE'})
            # cumulative persistence interval: cumulative favourable time at
            # each segment end; T must exceed cum. at end of every earlier
            # segment (else trigger inside it) and be <= cum. at close.
            cum, ok = 0.0, []
            for s in segs:
                cum += s['dur_s']; ok.append(cum)
            compat.append({'panier': b, 'theta_bp': theta, 'modele': 'P_cumulatif',
                           'borne_inf_s': (ok[-2] if len(ok) > 1 else 0.0),
                           'borne_sup_s': ok[-1] if ok else None,
                           'n_segments': len(segs), 'statut': 'INTERVALLE'})
        # reference theta=0 timeline & transitions
        segs0 = segments(df, 0.0)
        fin0 = segs0[-1] if segs0 else None
        first_fav = segs0[0]['start'] if segs0 else None
        timelines.append({
            'panier': b, 'ouverture_panier': open_ts, 'dernier_changement_position': last_pos_chg,
            'premier_retour_pwa(>=0bp)': first_fav,
            'debut_segment_final_favorable': fin0['start'] if fin0 else None,
            'duree_segment_final_s': fin0['dur_s'] if fin0 else None,
            'n_segments_favorables': len(segs0),
            'n_interruptions': max(len(segs0) - 1, 0),
            'duree_max_segment_interrompu_s': max([s['dur_s'] for s in segs0[:-1]], default=0.0),
            'cloture_reelle': close_ts, 'pnl_cloture_bp': float(pnl[-1]),
            'delai_segment_final_vers_cloture_s': fin0['dur_s'] if fin0 else None,
            'delai_premier_favorable_vers_cloture_s': (close_ts - first_fav).total_seconds() if first_fav is not None else None,
            'delai_dernier_changement_vers_cloture_s': (close_ts - last_pos_chg).total_seconds()})
        for k, s in enumerate(segs0):
            transitions.append({'panier': b, 'segment': k + 1, 'debut': s['start'], 'fin': s['end'],
                                'duree_s': s['dur_s'], 'ticks': s['ticks'],
                                'type': 'SEGMENT_FINAL_CLOTURE' if k == len(segs0) - 1 else 'SEGMENT_INTERROMPU',
                                'delai_fin_vers_cloture_s': (close_ts - s['end']).total_seconds()})
        # cadence diagnostics at theta=0
        if fin0 is not None:
            good = cadence_compatible(df, fin0['start'], close_ts)
            summary[b]['cadences_compatibles_theta0'] = good
            summary[b]['n_cadences_compatibles'] = len(good)
        # extra-condition candidates at close (past-only windows)
        t30 = df[df.ts >= close_ts - pd.Timedelta(seconds=30)]
        summary[b]['candidats_a_la_cloture'] = {
            'duree_detention_s': (close_ts - open_ts).total_seconds(),
            'ticks_depuis_dernier_changement': int((df.ts > last_pos_chg).sum()),
            'variation_pnl_30s_bp': float(pnl[-1] - t30.pnl_latent_bp.iloc[0]) if len(t30) else None,
            'volatilite_30s_ecarttype_bp': float(t30.pnl_latent_bp.std()) if len(t30) > 1 else None,
            'distance_pwa_bp': float(pnl[-1]),
            'ticks_segment_final': int(fin0['ticks']) if fin0 else None}
    pd.DataFrame(timelines).to_csv(OUT / 'EXIT_TIMELINE_A_E.csv', index=False)
    pd.DataFrame(transitions).to_csv(OUT / 'EXIT_STATE_TRANSITIONS.csv', index=False)
    cdf = pd.DataFrame(compat)
    cdf.to_csv(OUT / 'EXIT_PARAMETER_COMPATIBILITY.csv', index=False)
    (OUT / 'EMI006_NUMERIC_SUMMARY.json').write_text(json.dumps(summary, indent=1, default=str))
    # common (intersection) persistence intervals per theta/mode
    inter = []
    for (theta, mode), g in cdf[cdf.statut == 'INTERVALLE'].groupby(['theta_bp', 'modele']):
        lo = g.borne_inf_s.max(); hi = g.borne_sup_s.min()
        inter.append({'theta_bp': theta, 'modele': mode, 'borne_inf_commune_s': lo,
                      'borne_sup_commune_s': hi, 'intersection_non_vide': bool(lo < hi),
                      'largeur_s': (hi - lo) if lo < hi else 0.0})
    idf = pd.DataFrame(inter)
    idf.to_csv(OUT / 'EXIT_COMMON_INTERVALS.csv', index=False)
    print(idf.to_string())
    print(json.dumps({b: summary[b].get('n_cadences_compatibles') for b in BASKETS}))
    print(pd.DataFrame(timelines)[['panier', 'duree_segment_final_s', 'duree_max_segment_interrompu_s',
                                   'n_interruptions', 'delai_dernier_changement_vers_cloture_s']].to_string())


if __name__ != '__main__':
    main()

def extra_outputs():
    """Model grid replay (pre-registered grids), cadence intersection, robustness."""
    import itertools
    replay, model_rows, false_rows, robust = [], [], [], []
    cadence_sets = {}
    for b in BASKETS:
        df = pd.read_csv(SRC / f'TRAJECTORY_{b}.csv', parse_dates=['ts'])
        close_ts = df.ts.iloc[-1]; pnl = df.pnl_latent_bp.values; ts = df.ts
        segs0 = segments(df, 0.0)
        if segs0: cadence_sets[b] = set(cadence_compatible(df, segs0[-1]['start'], close_ts))
        # --- grid replays (sensitivity grids declared in seq470, not fitted points)
        def first_trigger(mask):
            idx = np.argmax(mask) if mask.any() else None
            return ts.iloc[idx] if idx is not None else None
        fav = pnl >= 0
        # P_continu: trigger when continuous favourable duration >= T
        for T in (1, 5, 10, 30, 60, 90):
            trig = None; run_start = None
            for i in range(len(df)):
                if fav[i]:
                    if run_start is None: run_start = ts.iloc[i]
                    if (ts.iloc[i] - run_start).total_seconds() >= T: trig = ts.iloc[i]; break
                else: run_start = None
            replay.append({'panier': b, 'modele': 'P_continu', 'parametres': f'theta=0,T={T}s',
                           'cloture_simulee': trig, 'cloture_reelle': close_ts,
                           'ecart_s': (trig - close_ts).total_seconds() if trig is not None else None,
                           'classe': 'MANQUEE' if trig is None else ('PREMATUREE' if (trig-close_ts).total_seconds() < -1 else ('RETARDEE' if (trig-close_ts).total_seconds() > 1 else 'SYNCHRONE'))})
        # tick-count confirmation: trigger after K consecutive favourable ticks
        for K in (50, 100, 200, 400):
            trig = None; run = 0
            for i in range(len(df)):
                run = run + 1 if fav[i] else 0
                if run >= K: trig = ts.iloc[i]; break
            replay.append({'panier': b, 'modele': 'P_ticks', 'parametres': f'theta=0,K={K} ticks',
                           'cloture_simulee': trig, 'cloture_reelle': close_ts,
                           'ecart_s': (trig - close_ts).total_seconds() if trig is not None else None,
                           'classe': 'MANQUEE' if trig is None else ('PREMATUREE' if (trig-close_ts).total_seconds() < -1 else ('RETARDEE' if (trig-close_ts).total_seconds() > 1 else 'SYNCHRONE'))})
        # cadence grid replay: first grid tick >= final favourable segment start
        # is scored inside cadence diagnostics; here false triggers = number of
        # distinct favourable segments that ended WITHOUT close (per basket)
        false_rows.append({'panier': b, 'theta_bp': 0.0,
                           'segments_favorables_sans_cloture': max(len(segs0) - (1 if fav[-1] else 0), 0),
                           'segments_interrompus': sum(1 for s in segs0 if s['end'] < close_ts),
                           'note': 'chaque segment interrompu est un faux candidat pour tout declencheur de premier passage'})
        # robustness: theta perturbation -> final upcross delay change; 1s/5s resample
        for th in (-0.5, 0.0, 0.5):
            m = pnl >= th
            idx = [i for i in range(1, len(df)) if m[i] and not m[i-1]]
            d = (close_ts - ts.iloc[idx[-1]]).total_seconds() if idx else None
            robust.append({'panier': b, 'test': f'delai dernier franchissement theta={th}bp', 'valeur': d, 'unite': 's'})
        df1 = df.set_index('ts').resample('1s').last().dropna().reset_index()
        m = df1.pnl_latent_bp.values >= 0
        idx = [i for i in range(1, len(df1)) if m[i] and not m[i-1]]
        robust.append({'panier': b, 'test': 'delai dernier franchissement (resample 1s)', 'valeur': (close_ts - df1.ts.iloc[idx[-1]]).total_seconds() if idx else None, 'unite': 's'})
        robust.append({'panier': b, 'test': 'cloture dans etat favorable (theta=0)', 'valeur': bool(fav[-1]), 'unite': 'bool'})
        robust.append({'panier': b, 'test': 'duree segment final (theta=0)', 'valeur': segs0[-1]['dur_s'] if segs0 else None, 'unite': 's'})
        robust.append({'panier': b, 'test': 'ecart fin dernier segment -> cloture (theta=0)', 'valeur': (close_ts - segs0[-1]['end']).total_seconds() if segs0 else None, 'unite': 's'})
    rdf = pd.DataFrame(replay)
    rdf.to_csv(OUT / 'EXIT_CAUSAL_REPLAY.csv', index=False)
    agg = rdf.groupby(['modele', 'parametres']).apply(lambda g: pd.Series({
        'prematurees': int((g.classe == 'PREMATUREE').sum()), 'synchrones': int((g.classe == 'SYNCHRONE').sum()),
        'manquees': int((g.classe == 'MANQUEE').sum()), 'retardees': int((g.classe == 'RETARDEE').sum()),
        'ecart_abs_median_s': g.ecart_s.abs().median()}), include_groups=False).reset_index()
    agg['verdict'] = np.where((agg.prematurees == 0) & (agg.manquees == 0) & (agg.synchrones >= 4), 'COMPATIBLE_GRID_POINT',
                              np.where(agg.manquees == 5, 'REFUTED (jamais declenche)', 'REFUTED comme point unique (prematures/manques)'))
    agg.to_csv(OUT / 'EXIT_MODEL_COMPARISON.csv', index=False)
    pd.DataFrame(false_rows).to_csv(OUT / 'EXIT_FALSE_TRIGGER_ANALYSIS.csv', index=False)
    pd.DataFrame(robust).to_csv(OUT / 'EXIT_ROBUSTNESS_TESTS.csv', index=False)
    common = set.intersection(*cadence_sets.values()) if cadence_sets else set()
    (OUT / 'EMI006_CADENCE.json').write_text(json.dumps({'par_panier': {k: sorted(v) for k, v in cadence_sets.items()}, 'cadences_communes_ancrage_ouverture': sorted(common)}, indent=1))
    print('cadences communes (ancrage ouverture):', sorted(common))
    print(agg.to_string())

if __name__ == "__main__":
    main(); extra_outputs()
