#!/usr/bin/env python3
"""MA-EDGE-02 — Pipeline SHADOW: ticks Bid/Ask -> barres M15 Mid -> evenements 24-B
(detection reproduite de ci_tools/phase24b_engine.py) -> score M15_TIME_ONLY gele
(coefficients PHASE24C_COEFFICIENTS.csv, seuil 0,5609549968307628) -> regle deadline
120 min preenregistree (seq407) vs reference 8 h. AUCUN ORDRE. Modes: selftest | run.
Clarifications seq409: depart prospectif = horodatage du preenregistrement; l'invalidation
ne declenche aucune sortie; confirmation = cloture M15 strictement au-dela du meilleur
niveau de cloture favorable pre-reintegration, a ou avant l'echeance."""
import json, pathlib, sys
import numpy as np
import pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
SEUIL = 0.5609549968307628
COEF = {'INTERCEPT': 1.5123425506624915, 'ratio_repli': -0.09591136403766899,
        'duree_extreme_vers_treint_min': -0.005727442729535342, 'MFE_A_TREINT_BP': -0.030115575520743666,
        'nb_touches_P0': -0.026332554232442396}
DEPART_PROSPECTIF = pd.Timestamp('2026-11-24T17:12:57Z')


def barres_m15(ticks: pd.DataFrame) -> pd.DataFrame:
    t = ticks.sort_values('ts').copy()
    t['mid'] = (t.bid + t.ask) / 2
    t['bar_start'] = t.ts.dt.floor('15min')
    g = t.groupby('bar_start').mid
    B = pd.DataFrame({'open': g.first(), 'high': g.max(), 'low': g.min(), 'close': g.last(),
                      'n_ticks': g.size()}).reset_index()
    B['complete'] = B.bar_start + pd.Timedelta(minutes=15) <= t.ts.max()
    return B


def detecter(B: pd.DataFrame) -> pd.DataFrame:
    fermees = B[B.complete].reset_index(drop=True)
    cl, hi, lo, op = fermees.close.values, fermees.high.values, fermees.low.values, fermees.open.values
    starts = fermees.bar_start.values
    absb = np.abs(10000 * np.log(cl / op))
    q90 = np.full(len(fermees), np.nan)
    for i in range(250, len(fermees)):
        fen = absb[i - 250:i]
        if np.isfinite(fen).all():
            q90[i] = np.quantile(fen, .90)
    ev = []
    for i in range(250, len(fermees)):
        if not np.isfinite(q90[i]) or absb[i] < q90[i] or absb[i] == 0:
            continue
        d = 1 if cl[i] > op[i] else -1
        t0 = starts[i] + np.timedelta64(15, 'm'); P0 = cl[i]
        if i + 32 >= len(fermees):
            ev.append(dict(t0=str(t0), direction=d, P0=float(P0), statut='CENSURE_FENETRE')); continue
        closes = cl[i + 1:i + 33]
        cote = (closes - P0) * d
        conf = np.where(cote > 0)[0]; reint = -1
        if len(conf):
            apres = np.where(cote[conf[0]:] < 0)[0]
            if len(apres):
                reint = conf[0] + apres[0]
        if reint < 0:
            ev.append(dict(t0=str(t0), direction=d, P0=float(P0), statut='NON_REINTEGRE')); continue
        t_reint = starts[i + 1 + reint] + np.timedelta64(15, 'm')
        seg_hi, seg_lo = hi[i + 1:i + 2 + reint], lo[i + 1:i + 2 + reint]
        extreme = seg_hi.max() if d > 0 else seg_lo.min()
        mfe = float(10000 * np.log(extreme / P0)) * d
        meilleur = float((closes[:reint] * d).max() * d) if reint > 0 else float(P0)
        creux = seg_lo.min() if d > 0 else seg_hi.max()
        profondeur = float(10000 * np.log(extreme / creux)) * d
        i_ext = int(np.argmax(seg_hi) if d > 0 else np.argmin(seg_lo))
        ev.append(dict(t0=str(t0), direction=d, P0=float(P0), statut='REINTEGRE', t_decision=str(t_reint),
                       reference_favorable=meilleur, MFE_A_TREINT_BP=mfe,
                       ratio_repli=(profondeur / mfe if mfe > 0 else np.nan),
                       duree_extreme_vers_treint_min=float(15 * (reint - i_ext)),
                       nb_touches_P0=int(((seg_lo <= P0) if d > 0 else (seg_hi >= P0)).sum()),
                       idx_barre_decision=i + 1 + reint))
    return pd.DataFrame(ev)


def scorer(E: pd.DataFrame) -> pd.DataFrame:
    E = E.copy()
    z = (COEF['INTERCEPT'] + COEF['ratio_repli'] * E.ratio_repli + COEF['duree_extreme_vers_treint_min'] * E.duree_extreme_vers_treint_min
         + COEF['MFE_A_TREINT_BP'] * E.MFE_A_TREINT_BP + COEF['nb_touches_P0'] * E.nb_touches_P0)
    E['p'] = 1 / (1 + np.exp(-z))
    E['selectionne'] = E.p > SEUIL
    return E


def premier_tick(ticks, apres, avant, cote):
    f = ticks[(ticks.ts > apres) & (ticks.ts <= avant)]
    if len(f) == 0:
        return None, None
    r = f.iloc[0]
    return r.ts, float(r.ask if cote == 'ask' else r.bid)


def appliquer_regle(ev, ticks, B):
    """Retourne (pnl_regle_bp, pnl_ref_bp, statut). Comptabilite: prix executables reels."""
    t_dec = pd.Timestamp(ev.t_decision)
    if t_dec.tzinfo is None:
        t_dec = t_dec.tz_localize('UTC')
    d = int(ev.direction)
    cote_e, cote_s = ('ask', 'bid') if d > 0 else ('bid', 'ask')
    te, pe = premier_tick(ticks, t_dec, t_dec + pd.Timedelta(seconds=60), cote_e)
    if pe is None:
        return None, None, 'NON_EXECUTION'
    # confirmation: clotures M15 strictement au-dela de la reference, a ou avant echeance
    echeance = t_dec + pd.Timedelta(minutes=120)
    bars = B[(B.bar_start + pd.Timedelta(minutes=15) > t_dec) & (B.bar_start + pd.Timedelta(minutes=15) <= echeance)]
    confirme = bool(len(bars) and (((bars.close - ev.reference_favorable) * d) > 0).any())
    t_ref = t_dec + pd.Timedelta(minutes=480)
    _, p_ref = premier_tick(ticks, t_ref, t_ref + pd.Timedelta(seconds=60), cote_s)
    if confirme:
        if p_ref is None:
            return None, None, 'EXIT_NONEXECUTABLE'
        pnl = d * 10000 * np.log(p_ref / pe)
        return float(pnl), float(pnl), 'CONFIRME_SORTIE_8H'
    ts_, p_dl = premier_tick(ticks, echeance, echeance + pd.Timedelta(seconds=60), cote_s)
    if p_dl is None or p_ref is None:
        return None, None, 'EXIT_NONEXECUTABLE'
    return float(d * 10000 * np.log(p_dl / pe)), float(d * 10000 * np.log(p_ref / pe)), 'DEADLINE_120'


def selftest():
    rng = np.random.default_rng(7)
    # 300 barres calmes puis impulsion + repli + reintegration, ticks chaque 5 s
    prix = [4000.0]
    for k in range(300 * 15 * 12):
        prix.append(prix[-1] + rng.normal(0, 0.02))
    base = prix[-1]
    for k in range(15 * 12):  # impulsion +60 bp en une barre
        prix.append(base * np.exp(0.006 * (k + 1) / (15 * 12)))
    pic = prix[-1]
    for k in range(30 * 12):  # repli sous P0=cloture impulsion puis reintegration
        prix.append(pic * np.exp(-0.004 * (k + 1) / (30 * 12)))
    for k in range(12 * 720):  # derive lente sans confirmation (12 h de ticks)
        prix.append(prix[-1] * np.exp(-0.0000002 * k))
    ts = pd.date_range('2026-12-01T00:00:00Z', periods=len(prix), freq='5s')
    mid = np.array(prix)
    ticks = pd.DataFrame({'ts': ts, 'bid': mid - 0.15, 'ask': mid + 0.15})
    B = barres_m15(ticks)
    E = detecter(B)
    rein = E[E.statut == 'REINTEGRE']
    assert len(rein) >= 1, 'aucun evenement detecte'
    ev = rein.iloc[0]
    assert int(ev.direction) == 1
    E2 = scorer(rein)
    pnl_r, pnl_ref, statut = appliquer_regle(ev, ticks, B)
    assert statut in ('DEADLINE_120', 'CONFIRME_SORTIE_8H'), statut
    # idempotence collecte: dedoublonnage
    double = pd.concat([ticks, ticks]).drop_duplicates('ts')
    assert len(double) == len(ticks)
    print(f'SELFTEST OK: evenement detecte t_decision={ev.t_decision} p={E2.p.iloc[0]:.3f} statut={statut} pnl_regle={pnl_r:.2f} bp pnl_ref={pnl_ref:.2f} bp')
    print('Depart prospectif verrouille:', DEPART_PROSPECTIF)


if __name__ == '__main__':
    if sys.argv[1] == 'selftest':
        selftest()
