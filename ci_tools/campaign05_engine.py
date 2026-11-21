"""CAMPAGNE 5 - sessions (F-E) et extremes dates (F-F), descriptif causal.
Protocole V2 + addenda V2.1/V2.2 geles (seq221). Barre M1 disponible a sa
cloture; avant B = disponibilite < B; atteinte reelle identifiable seulement
si continuite minute a minute complete depuis le debut de la periode."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign05'); ROOT.mkdir(parents=True, exist_ok=True)
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)

def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

def era(d): return '2010_2013' if d.year <= 2013 else ('2014_2016' if d.year <= 2016 else '2017_2020')

CHARGER_STATS = {'chargees': 0, 'attendues': 0}
def charger():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    CHARGER_STATS['attendues'] = len(parts)
    print('C5 ALL', len(parts), 'partitions attendues', flush=True)
    con = duckdb.connect(); con.execute("SET memory_limit='5GB'"); con.execute("SET threads=2")
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts: groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    frames, api, username = [], None, None
    for batch, ps in groups.items():
        localdir = None
        tok = os.environ.get('KAGGLE_API_TOKEN', '')
        if tok:
            try:
                import requests, zipfile, io
                url = f'https://www.kaggle.com/api/v1/datasets/download/shalom5123/{batch}'
                r = None
                for hdrs, auth in [({'Authorization': f'Bearer {tok}'}, None), ({}, (os.environ.get('KAGGLE_USERNAME', ''), tok))]:
                    r = requests.get(url, headers=hdrs, auth=auth, timeout=600)
                    print('direct Kaggle', batch, r.status_code, flush=True)
                    if r.status_code == 200: break
                if r is not None and r.status_code == 200:
                    localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True); pathlib.Path(localdir).mkdir(parents=True)
                    zipfile.ZipFile(io.BytesIO(r.content)).extractall(localdir)
                    print('direct Kaggle OK', batch, len(list(pathlib.Path(localdir).glob('*'))), flush=True)
            except Exception as e:
                print('direct Kaggle KO', str(e)[:100], flush=True); localdir = None
        if localdir is None and batch != 'DRIVE' and os.environ.get('KAGGLE_API_TOKEN'):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi(); api.authenticate(); username = 'shalom5123'
                localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True)
                for _try in range(2):
                    try:
                        api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True); break
                    except Exception:
                        if _try == 1: raise
                        time.sleep(30)
            except Exception as e:
                print('Kaggle KO repli Drive', str(e)[:80], flush=True); localdir = None
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if not pathlib.Path(local).exists():
                if not dl_drive(p.get('drive_id', ''), local, p.get('file_bytes', -1)): continue
            try:
                q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts, arg_min(mid, timestamp_utc) AS o,
                        max(mid) AS h, min(mid) AS l, arg_max(mid, timestamp_utc) AS c, median((ask-bid)/mid*10000) AS sp
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b); CHARGER_STATS['chargees'] += 1
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C5 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives (testees par campaign05_temporal_tests.py) ----------
def statut_fenetre(attendu, observe, trou_max):
    if observe >= attendu: return 'COMPLETE'
    if attendu and observe / attendu >= 0.9 and trou_max <= (15 if attendu >= 60 else 5): return 'PARTIELLE'
    return 'CENSUREE'

def classe_retard(retard_min):
    if retard_min is None: return 'ABSENTE'
    if retard_min <= 1: return 'PONCTUELLE'
    if retard_min <= 5: return 'LEGER'
    if retard_min <= 30: return 'DIFFEREE'
    return 'INELIGIBLE'

def avant(dispo, borne):
    """avant B = disponibilite strictement inferieure a B."""
    return dispo < borne

def atteinte_reelle(minutes_manquantes_avant):
    return minutes_manquantes_avant == 0

def categorie_issue(pre_bp, sens, atteint_poursuite, atteint_retournement, meme_barre=False):
    if pre_bp == 0: return 'MOUVEMENT_NUL'
    if atteint_poursuite and atteint_retournement: return 'LES_DEUX'
    if atteint_poursuite: return 'POURSUITE_SEULE'
    if atteint_retournement: return 'RETOURNEMENT_SEUL'
    return 'AUCUN'

def mises_a_jour_niveaux(extreme_courant, E0, sens, pas_bp=5.0):
    """Nombre de seuils S_n franchis par l'extreme courant (ancre E0)."""
    if sens == 1:
        if extreme_courant <= E0: return 0
        return int(np.floor((extreme_courant / E0 - 1) * 10000 / pas_bp + 1e-12))
    else:
        if extreme_courant >= E0: return 0
        return int(np.floor((1 - extreme_courant / E0) * 10000 / pas_bp + 1e-12))

SESSIONS = [('ASIE', 0, 8), ('LONDRES', 8, 13), ('NEWYORK', 13, 21), ('NUIT', 21, 24)]

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date
    bars['minute'] = bars.ts.dt.hour * 60 + bars.ts.dt.minute
    jours = {}
    for d, g in bars.groupby('date'):
        g = g.sort_values('ts')
        jours[d] = {'g': g, 'n': len(g), 'minutes': g.minute.values, 'ts': g.ts.values,
                    'o': g.o.values, 'h': g.h.values, 'l': g.l.values, 'c': g.c.values, 'sp': g.sp.values}
    dates = sorted(jours)
    utilisable = {d: jours[d]['n'] >= 300 for d in dates}
    # ---- couverture journaliere ----
    day_rows = []
    for d in dates:
        J = jours[d]; mins = J['minutes']
        present = set(mins.tolist())
        trous = np.diff(mins) - 1 if len(mins) > 1 else np.array([0])
        taux = len(mins) / 1440 * 100
        complete = (len(mins) >= 1368 and mins[0] <= 10 and mins[-1] >= 1430 and (len(trous) == 0 or trous.max() <= 30))
        day_rows.append({'date': str(d), 'ere': era(d), 'jour_semaine': int(pd.Timestamp(d).dayofweek),
                         'n_barres': len(mins), 'taux_couverture_pct': round(taux, 3),
                         'premiere_minute': int(mins[0]), 'derniere_minute': int(mins[-1]),
                         'trou_max_min': int(trous.max()) if len(trous) else 0,
                         'statut_journee': 'COMPLETE' if complete else ('PARTIELLE' if len(mins) >= 300 else 'EXCLUE'),
                         'minutes_manquantes_total': int(1440 - len(present)),
                         'contenue_etablie_possible': bool(len(present) == 1440)})
    DAY = pd.DataFrame(day_rows).set_index('date')
    # ---------- F-E : ouvertures ----------
    openings = []; winctrl = []
    prev_date = {dates[i]: dates[i - 1] for i in range(1, len(dates))}
    for d in dates:
        if not utilisable[d]: continue
        J = jours[d]; mins = J['minutes']
        for sname, h0, h1 in SESSIONS:
            theo = h0 * 60
            cand = np.where((mins >= theo) & (mins < h1 * 60))[0]
            if len(cand) == 0:
                openings.append({'date': str(d), 'ere': era(d), 'session': sname, 'heure_theorique': f'{h0:02d}:00',
                                 'retard_min': None, 'classe_retard': 'ABSENTE', 'eligible': 0})
                continue
            i0 = int(cand[0]); retard = int(mins[i0] - theo)
            t0 = pd.Timestamp(J['ts'][i0])
            base = {'date': str(d), 'ere': era(d), 'session': sname, 'heure_theorique': f'{h0:02d}:00',
                    'ts_premiere_barre': str(t0), 'retard_min': retard, 'classe_retard': classe_retard(retard),
                    'eligible': int(retard <= 30), 'jour_semaine': int(pd.Timestamp(d).dayofweek)}
            if sname == 'ASIE':
                pd_ = prev_date.get(d)
                if pd_ is not None:
                    trou_min = int(mins[i0] + 1440 - (jours[pd_]['minutes'][-1] + 1)) if pd.Timestamp(d).toordinal() - pd.Timestamp(pd_).toordinal() == 1 else int((pd.Timestamp(d) - pd.Timestamp(pd_)).total_seconds() // 60 - (jours[pd_]['minutes'][-1] + 1) + mins[i0])
                    ecart = float(np.log(J['o'][i0] / jours[pd_]['c'][-1]) * 10000)
                    if pd.Timestamp(pd_).dayofweek == 4: classe = 'REOUVERTURE_SEMAINE'
                    elif trou_min > 720: classe = 'FERMETURE_EXCEPTIONNELLE'
                    elif trou_min > 5: classe = 'TROU_INTRA_SEMAINE'
                    else: classe = 'CONTINUITE'
                    base.update({'classe_ancrage_asie': classe, 'trou_inter_jours_min': trou_min, 'ecart_trou_bp': round(ecart, 3)})
            # mouvement pre-ouverture (60 min avant l'instant, barres presentes, meme jour ou veille pour ASIE)
            pre_mask = (bars.ts >= t0 - pd.Timedelta(minutes=60)) & (bars.ts < t0)
            pre = bars[pre_mask]
            if len(pre) >= 2:
                pre_bp = float(np.log(pre.c.iloc[-1] / pre.o.iloc[0]) * 10000)
            else: pre_bp = np.nan
            base['mouvement_pre60_bp'] = round(pre_bp, 3) if pre_bp == pre_bp else None
            for dur in (5, 15, 30, 60):
                wmask = (J['ts'] >= J['ts'][i0]) & (J['ts'] < J['ts'][i0] + np.timedelta64(dur, 'm'))
                idx = np.where(wmask)[0]
                attendu = dur; observe = len(idx)
                if observe:
                    wmin = J['minutes'][idx]
                    trous_w = np.diff(np.concatenate([[theo + retard - 1], wmin])) - 1 if False else None
                    # trous dans la fenetre: minutes attendues de l'instant a l'instant+dur
                    attendues = set(range(int(mins[i0]), int(mins[i0]) + dur))
                    manq = len(attendues - set(wmin.tolist()))
                    # plus long trou: suites de minutes manquantes
                    trou_max = 0; run = 0
                    pres = set(wmin.tolist())
                    for m in range(int(mins[i0]), int(mins[i0]) + dur):
                        if m in pres: run = 0
                        else:
                            run += 1; trou_max = max(trou_max, run)
                else:
                    manq, trou_max = dur, dur
                st = statut_fenetre(attendu, observe, trou_max)
                winctrl.append({'date': str(d), 'session': sname, 'fenetre_min': dur, 'barres_attendues': attendu,
                                'barres_observees': int(observe), 'taux_couverture_pct': round(100 * observe / attendu, 2),
                                'trou_max_min': int(trou_max), 'statut': st})
                if st != 'CENSUREE' and observe:
                    seg_h, seg_l = J['h'][idx], J['l'][idx]
                    ouv = J['o'][idx[0]]
                    r = np.diff(np.log(J['c'][idx]))
                    base[f'amplitude_{dur}_bp'] = round(float((seg_h.max() - seg_l.min()) / ouv * 10000), 3)
                    base[f'rendement_{dur}_bp'] = round(float(np.log(J['c'][idx[-1]] / ouv) * 10000), 3)
                    base[f'rv_{dur}_bp'] = round(float(np.sqrt(np.sum(r ** 2)) * 10000), 3) if len(r) else 0.0
                    spv = J['sp'][idx]; base[f'spread_{dur}_bp'] = round(float(np.nanmedian(spv)), 4) if np.isfinite(spv).any() else None
                    base[f'fenetre_{dur}_statut'] = st; base[f'fenetre_{dur}_couverture'] = round(100 * observe / attendu, 2)
                else:
                    base[f'fenetre_{dur}_statut'] = st
            # issues a +30/+60: poursuite/retournement vs mouvement pre-ouverture
            if pre_bp == pre_bp:
                A = abs(pre_bp); sens = 0 if A == 0 else (1 if pre_bp > 0 else -1)
                ouv = J['o'][i0]
                for dur in (30, 60):
                    if A == 0:
                        base[f'issue_{dur}'] = 'MOUVEMENT_NUL'; continue
                    idx = np.where((J['ts'] > J['ts'][i0]) & (J['ts'] <= J['ts'][i0] + np.timedelta64(dur, 'm')))[0]
                    trou_f = False
                    if len(idx):
                        pres = set(J['minutes'][idx].tolist())
                        manq = [m for m in range(int(mins[i0]) + 1, int(mins[i0]) + dur + 1) if m not in pres and m < 1440]
                        trou_f = len(manq) > 0 and (dur >= 60 and len(manq) > 15 or dur < 60 and len(manq) > 5)
                    seuil_p = ouv * (1 + sens * 0.5 * A / 10000); seuil_r = ouv * (1 - sens * 0.5 * A / 10000)
                    att_p = att_r = False
                    if len(idx):
                        if sens == 1: att_p = bool((J['h'][idx] > seuil_p).any()); att_r = bool((J['l'][idx] < seuil_r).any())
                        else: att_p = bool((J['l'][idx] < seuil_p).any()); att_r = bool((J['h'][idx] > seuil_r).any())
                    base[f'issue_{dur}'] = 'CENSURE' if trou_f else categorie_issue(pre_bp, sens, att_p, att_r)
            openings.append(base)
    OP = pd.DataFrame(openings)
    # references causales par session (mediane des 60 journees precedentes, min 40) pour amplitude_30
    if len(OP) and 'amplitude_30_bp' in OP.columns:
        OP = OP.sort_values(['session', 'date']).reset_index(drop=True)
        refs = []
        for sname, g in OP.groupby('session', sort=False):
            v = g['amplitude_30_bp'] if 'amplitude_30_bp' in g else pd.Series(dtype=float)
            refs.append(v.shift(1).rolling(60, min_periods=40).median())
        OP['ref_causale_amplitude30_bp'] = pd.concat(refs).sort_index()
        OP['ratio_ref_amplitude30'] = (OP['amplitude_30_bp'] / OP['ref_causale_amplitude30_bp']).round(4)
    # ---------- F-F : extremes journaliers ----------
    att_rows = []; touch_rows = []; indet_rows = []; dayff_rows = []
    prev_util = {}
    lastu = None
    Hprev = Lprev = None
    for d in dates:
        J = jours[d]
        if not utilisable[d]:
            dayff_rows.append({'date': str(d), 'ere': era(d), 'statut_journee': DAY.loc[str(d), 'statut_journee'], 'ff_usage': 'EXCLUE'})
            continue
        mins, H, L, C = J['minutes'], J['h'], J['l'], J['c']
        st_j = DAY.loc[str(d), 'statut_journee']
        rec = {'date': str(d), 'ere': era(d), 'statut_journee': st_j, 'ff_usage': 'OK', 'jour_semaine': int(pd.Timestamp(d).dayofweek)}
        if Hprev is None:
            rec['ff_usage'] = 'SANS_REFERENCE'; dayff_rows.append(rec)
            Hprev, Lprev = float(H.max()), float(L.min()); lastu = (Hprev, Lprev); continue
        # minutes manquantes avant chaque barre (depuis 00:00)
        pos = np.arange(len(mins))
        manq_avant = mins - pos  # minutes d'horloge avant la fin de la barre i moins barres presentes jusqu'a i
        evs = {}
        for cote, niv, sens in [('HAUT', Hprev, 1), ('BAS', Lprev, -1)]:
            franch = np.where(H > niv)[0] if sens == 1 else np.where(L < niv)[0]
            touch = np.where(H == niv)[0] if sens == 1 else np.where(L == niv)[0]
            if len(touch) and (not len(franch) or touch[0] < (franch[0] if len(franch) else 10**9)):
                touch_rows.append({'date': str(d), 'ere': era(d), 'cote': cote, 'ts_barre': str(J['ts'][touch[0]]),
                                   'reelle_identifiable': bool(atteinte_reelle(int(manq_avant[touch[0]]))),
                                   'minutes_manquantes_avant': int(manq_avant[touch[0]])})
            if len(franch):
                i = int(franch[0]); E0 = niv
                reelle = atteinte_reelle(int(manq_avant[i]))
                row = {'date': str(d), 'ere': era(d), 'cote': cote, 'ts_barre': str(J['ts'][i]),
                       'heure_debut_barre': f'{int(mins[i])//60:02d}:{int(mins[i])%60:02d}',
                       'heure_disponibilite': f'{(int(mins[i])+1)//60:02d}:{(int(mins[i])+1)%60:02d}',
                       'disponibilite_min': int(mins[i]) + 1,
                       'statut_atteinte': 'REELLE_IDENTIFIABLE' if reelle else 'OBSERVEE',
                       'minutes_manquantes_avant': int(manq_avant[i]), 'niveau_franchi': float(E0),
                       'statut_journee': st_j, 'posterieure_opposee': 0}
                # issues sur barres suivantes
                for hz in (15, 30, 60):
                    idx = np.where((J['ts'] > J['ts'][i]) & (J['ts'] <= J['ts'][i] + np.timedelta64(hz, 'm')))[0]
                    if len(idx):
                        if sens == 1:
                            row[f'extension_{hz}_bp'] = round(float(max(0.0, (J['h'][idx].max() - E0) / E0 * 10000)), 3)
                            row[f'retracement_{hz}_bp'] = round(float(max(0.0, (E0 - J['l'][idx].min()) / E0 * 10000)), 3)
                        else:
                            row[f'extension_{hz}_bp'] = round(float(max(0.0, (E0 - J['l'][idx].min()) / E0 * 10000)), 3)
                            row[f'retracement_{hz}_bp'] = round(float(max(0.0, (J['h'][idx].max() - E0) / E0 * 10000)), 3)
                        row[f'position_fin_{hz}_bp'] = round(float(((J['c'][idx[-1]] - E0) if sens == 1 else (E0 - J['c'][idx[-1]])) / E0 * 10000), 3)
                        pres = set(mins[idx].tolist()); manq_w = sum(1 for m in range(int(mins[i]) + 1, min(int(mins[i]) + hz, 1439) + 1) if m not in pres)
                        row[f'censure_{hz}'] = int(manq_w > 0 and J['ts'][idx[-1]] < J['ts'][i] + np.timedelta64(hz, 'm') and int(mins[i]) + hz <= 1439)
                    else:
                        row[f'extension_{hz}_bp'] = None; row[f'retracement_{hz}_bp'] = None; row[f'position_fin_{hz}_bp'] = None; row[f'censure_{hz}'] = 1
                ext_cour = np.maximum.accumulate(H)[i:] if sens == 1 else np.minimum.accumulate(L)[i:]
                row['mises_a_jour_journee'] = int(mises_a_jour_niveaux(float(ext_cour[-1]), E0, sens)) if len(ext_cour) else 0
                evs[cote] = (i, row); att_rows.append(row)
        if 'HAUT' in evs and 'BAS' in evs:
            ih, ib = evs['HAUT'][0], evs['BAS'][0]
            if ih == ib:
                indet_rows.append({'date': str(d), 'type': 'ATTEINTES_SIMULTANEES_MEME_BARRE', 'ts_barre': str(J['ts'][ih])})
                for r in att_rows[-2:]: r['ordre_indetermine'] = 1
            else:
                for c, (ii, r) in evs.items():
                    r['posterieure_opposee'] = int((ib if c == 'HAUT' else ih) < ii)
        rec['atteinte_haut'] = int('HAUT' in evs); rec['atteinte_bas'] = int('BAS' in evs)
        rec['contenue_etablie'] = int(len(set(mins.tolist())) == 1440 and not evs and not touch_rows_d(dayff_rows, touch_rows, d))
        dayff_rows.append(rec)
        lastu = (float(H.max()), float(L.min())); Hprev, Lprev = lastu
    ATT = pd.DataFrame(att_rows); 
    if 'ordre_indetermine' not in ATT.columns and len(ATT): ATT['ordre_indetermine'] = 0
    # ---------- F-F hebdomadaire ----------
    wk_rows = []; watt_rows = []
    Jday = {d: jours[d] for d in dates if utilisable[d]}
    mondays = {}
    for d in Jday:
        lundi = d - dt.timedelta(days=pd.Timestamp(d).dayofweek)
        mondays.setdefault(lundi, []).append(d)
    sems = sorted(mondays)
    prev_sem = None
    for k, lundi in enumerate(sems):
        jrs = sorted(mondays[lundi])
        utilisable_sem = len(jrs) >= 4
        rec = {'semaine_lundi': str(lundi), 'ere': era(lundi), 'n_journees_utilisables': len(jrs),
               'reference_valide': int(prev_sem is not None and prev_sem[2]), 'statut_reference': 'CENSUREE' if not (prev_sem and prev_sem[2]) else 'OK'}
        wk_rows.append(rec)
        if prev_sem is not None and prev_sem[2]:
            Hp, Lp, _ = prev_sem
            for cote, niv, sens in [('HAUT', Hp, 1), ('BAS', Lp, -1)]:
                found = None
                manq_cum = 0
                # jours ouvres (lun-ven) entierement absents avant le jour de l'evenement: 1440 minutes manquantes chacun
                for d in jrs:
                    J = Jday[d]; mins = J['minutes']
                    franch = np.where(J['h'] > niv)[0] if sens == 1 else np.where(J['l'] < niv)[0]
                    if len(franch):
                        i = int(franch[0]); pos = np.arange(len(mins)); manq = int(mins[i] - pos[i]) + manq_cum
                        # jours ouvres absents entre lundi et la veille de l'evenement
                        dd = lundi
                        while dd < d:
                            if dd.weekday() < 5 and dd not in Jday and dd in jours and not utilisable.get(dd, False): manq += 1440
                            elif dd.weekday() < 5 and dd not in jours: manq += 1440
                            dd += dt.timedelta(days=1)
                        found = {'semaine_lundi': str(lundi), 'ere': era(lundi), 'cote': cote, 'date': str(d),
                                 'ts_barre': str(J['ts'][i]), 'disponibilite': str(J['ts'][i] + np.timedelta64(1, 'm')),
                                 'avant_mercredi': int((J['ts'][i] + np.timedelta64(1, 'm')) < np.datetime64(f'{lundi + dt.timedelta(days=2)}T00:00')),
                                 'statut_atteinte': 'REELLE_IDENTIFIABLE' if manq == 0 else 'OBSERVEE',
                                 'minutes_manquantes_avant': manq}
                        break
                    manq_cum += int(1440 - len(set(mins.tolist())))
                if found: watt_rows.append(found)
        if utilisable_sem:
            hs = [float(Jday[d]['h'].max()) for d in jrs]; ls = [float(Jday[d]['l'].min()) for d in jrs]
            prev_sem = (max(hs), min(ls), True)
        else:
            prev_sem = (None, None, False)
    OP.round(4).to_csv(ROOT / 'CAMPAIGN_05_OPENINGS.csv.gz', index=False, compression='gzip')
    pd.DataFrame(winctrl).to_csv(ROOT / 'CAMPAIGN_05_WINDOW_COVERAGE.csv', index=False)
    DAY.reset_index().round(4).to_csv(ROOT / 'CAMPAIGN_05_DAY_COVERAGE.csv', index=False)
    ATT.round(4).to_csv(ROOT / 'CAMPAIGN_05_ATTEINTES_JOUR.csv.gz', index=False, compression='gzip') if len(ATT) else pd.DataFrame().to_csv(ROOT / 'CAMPAIGN_05_ATTEINTES_JOUR.csv.gz', index=False, compression='gzip')
    pd.DataFrame(touch_rows).to_csv(ROOT / 'CAMPAIGN_05_TOUCHES.csv', index=False)
    pd.DataFrame(indet_rows).to_csv(ROOT / 'CAMPAIGN_05_ORDRE_INDETERMINE.csv', index=False)
    pd.DataFrame(dayff_rows).to_csv(ROOT / 'CAMPAIGN_05_DAY_FF.csv', index=False)
    pd.DataFrame(wk_rows).to_csv(ROOT / 'CAMPAIGN_05_WEEKS.csv', index=False)
    pd.DataFrame(watt_rows).to_csv(ROOT / 'CAMPAIGN_05_ATTEINTES_SEMAINE.csv', index=False)
    cov = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
           'barres_m1': int(len(bars)), 'journees_presentes': int(len(dates)),
           'journees_utilisables': int(sum(utilisable.values())),
           'ouvertures_lignes': int(len(OP)), 'atteintes_jour': int(len(ATT)), 'touches': int(len(touch_rows)),
           'ordre_indetermine': int(len(indet_rows)), 'semaines': int(len(wk_rows)), 'atteintes_semaine': int(len(watt_rows))}
    (ROOT / 'C5_COVERAGE.json').write_text(json.dumps(cov, indent=1))
    print('C5 TERMINE', cov, flush=True)

def touch_rows_d(dayff_rows, touch_rows, d):
    return any(t['date'] == str(d) for t in touch_rows)

if __name__ == '__main__': main()
