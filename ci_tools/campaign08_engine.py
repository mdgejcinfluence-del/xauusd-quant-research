"""CAMPAGNE 8 - F-J chocs minute extremes et leur sillage, descriptif.
Protocole gele V2 (seq266). Detection causale (seuil du jour calcule sur
les 20 journees precedentes), episodes a ecart <=15 min, cloture par
silence de 15 minutes integralement observe, sillage retrospectif +60,
bassin de pseudo-evenements par blocs de 60 minutes. Aucun calcul a
travers un trou; aucune reconstruction de donnee manquante."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/campaign08'); ROOT.mkdir(parents=True, exist_ok=True)
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
    import duckdb
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    CHARGER_STATS['attendues'] = len(parts)
    print('C8 ALL', len(parts), 'partitions attendues', flush=True)
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
                        max(mid) AS h, min(mid) AS l, arg_max(mid, timestamp_utc) AS c
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                b = con.execute(q).df(); b['ts'] = pd.to_datetime(b.ts).dt.tz_localize(None); frames.append(b); CHARGER_STATS['chargees'] += 1
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {e}")
            print('C8 part', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    return pd.concat(frames).drop_duplicates('ts').sort_values('ts').reset_index(drop=True)

# ---------- primitives (testees par campaign08_temporal_tests.py) ----------
SESSIONS = [('S1', 0, 420), ('S2', 420, 780), ('S3', 780, 1260), ('S4', 1260, 1440)]

def session_de(minute):
    for nom, a, b in SESSIONS:
        if a <= minute < b: return nom
    return 'S4'

def debut_session(minute):
    for nom, a, b in SESSIONS:
        if a <= minute < b: return a
    return 1260

def seuil_causal(abs_r_fenetre):
    """T_D = max(10 bp, Q99.5% interpolation lineaire)."""
    return max(10.0, float(np.quantile(np.asarray(abs_r_fenetre, float), 0.995, method='linear')))

def est_choc(r, seuil):
    return bool(np.isfinite(r) and abs(r) > seuil)

def calculer_r(ts, c):
    r = np.full(len(ts), np.nan)
    if len(ts) > 1:
        ok = (ts[1:] - ts[:-1]) == 1
        r[1:][ok] = np.log(c[1:][ok] / c[:-1][ok]) * 10000.0
    return r

def grouper_episodes(ts_chocs):
    """Indices (debut, fin inclus) des groupes a ecarts <=15 minutes."""
    groupes = []
    if len(ts_chocs) == 0: return groupes
    debut = 0
    for i in range(1, len(ts_chocs)):
        if ts_chocs[i] - ts_chocs[i - 1] > 15:
            groupes.append((debut, i - 1)); debut = i
    groupes.append((debut, len(ts_chocs) - 1))
    return groupes

def silence_complet(ts, choc, i_der):
    """Les barres t_der+1..t_der+15 existent toutes, consecutives, sans choc."""
    if i_der + 15 >= len(ts): return False
    if ts[i_der + 15] - ts[i_der] != 15: return False
    if np.any(np.diff(ts[i_der:i_der + 16]) != 1): return False
    return not bool(np.any(choc[i_der + 1:i_der + 16]))

def fenetre_ok(ts, i0, h):
    """Barre t0+h presente et aucun trou >15 min sur (t0, t0+h]."""
    j = int(np.searchsorted(ts, ts[i0] + h))
    if j >= len(ts) or ts[j] != ts[i0] + h: return None
    if np.max(np.diff(ts[i0:j + 1])) > 15: return None
    return j

def r_h(ts, c, i0, h, s):
    j = fenetre_ok(ts, i0, h)
    if j is None: return np.nan
    return float(s * np.log(c[j] / c[i0]) * 10000.0)

def activite_avant(ts, r, i):
    """Somme des |r| des 60 minutes precedant i (segment complet exige)."""
    if i < 61: return np.nan
    if ts[i] - ts[i - 61] != 61: return np.nan
    seg = r[i - 60:i]
    if np.any(~np.isfinite(seg)): return np.nan
    return float(np.sum(np.abs(seg)))

def main():
    bars = charger()
    if CHARGER_STATS['chargees'] < CHARGER_STATS['attendues']:
        (ROOT / 'ERROR_INTEGRITE.txt').write_text(f"partitions {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']}")
        raise RuntimeError(f"integrite: {CHARGER_STATS['chargees']}/{CHARGER_STATS['attendues']} partitions")
    bars['date'] = bars.ts.dt.date
    ts = ((bars.ts - pd.Timestamp('2010-01-01')).dt.total_seconds().values // 60).astype(np.int64)
    c = bars.c.values.astype(float); h = bars.h.values.astype(float); l = bars.l.values.astype(float)
    dates = bars.date.values
    uniq, starts = np.unique(dates, return_index=True)
    bounds = list(starts) + [len(bars)]
    r = calculer_r(ts, c)
    absr = np.abs(r)
    # seuils causaux par journee, fenetre des 20 journees precedentes
    seuil_jour = np.full(len(uniq), np.nan); eligible = np.zeros(len(uniq), bool)
    hist = []  # (abs_r du jour) dans l'ordre
    for d in range(len(uniq)):
        ndays = len(hist)
        if ndays >= 10:
            fen = hist[-20:]
            tot = sum(len(x) for x in fen)
            if tot >= 10000:
                eligible[d] = True
                seuil_jour[d] = seuil_causal(np.concatenate(fen))
        a, b = bounds[d], bounds[d + 1]
        seg = absr[a:b]; seg = seg[np.isfinite(seg)]
        hist.append(seg)
    jour_id = np.repeat(np.arange(len(uniq)), np.diff(bounds))
    T_bar = seuil_jour[jour_id]
    choc = np.zeros(len(bars), bool)
    ok = eligible[jour_id] & np.isfinite(r)
    choc[ok] = np.abs(r[ok]) > T_bar[ok]
    idx_chocs = np.where(choc)[0]
    ts_chocs = ts[idx_chocs]
    date_str = bars.date.astype(str).values
    minute = (ts % 1440).astype(int)

    def sillage(i0, s, A):
        out = {}
        for hh in (15, 30, 60):
            out[f'R{hh}'] = r_h(ts, c, i0, hh, s)
        j60 = fenetre_ok(ts, i0, 60)
        if j60 is not None:
            c0 = c[i0]
            if s > 0:
                out['excursion_favorable_bp'] = float((np.max(h[i0 + 1:j60 + 1]) / c0 - 1) * 10000)
                out['excursion_defavorable_bp'] = float((np.min(l[i0 + 1:j60 + 1]) / c0 - 1) * 10000)
            else:
                out['excursion_favorable_bp'] = float((1 - np.min(l[i0 + 1:j60 + 1]) / c0) * 10000)
                out['excursion_defavorable_bp'] = float((1 - np.max(h[i0 + 1:j60 + 1]) / c0) * 10000)
        else:
            out['excursion_favorable_bp'] = np.nan; out['excursion_defavorable_bp'] = np.nan
        out['part_retracee'] = float(max(0.0, -out['R60']) / A) if np.isfinite(out['R60']) and A > 0 else np.nan
        out['retournement'] = int(out['R60'] < -A) if np.isfinite(out['R60']) else None
        # stabilisation: somme |r| 60 min suivant l'ancrage / A_avant du premier evenement (passe en A via cle dediee)
        post = np.nan
        if i0 + 60 < len(ts) and ts[i0 + 60] - ts[i0] == 60 and np.all(np.diff(ts[i0:i0 + 61]) == 1):
            seg = r[i0 + 1:i0 + 61]
            if np.all(np.isfinite(seg)): post = float(np.sum(np.abs(seg)))
        out['_post60'] = post
        k = int(np.searchsorted(ts_chocs, ts[i0] + 60, side='right')) - int(np.searchsorted(ts_chocs, ts[i0], side='right'))
        out['nouveau_choc'] = int(k > 0) if j60 is not None else None
        return out

    episodes = []
    for gi, (a, b) in enumerate(grouper_episodes(ts_chocs)):
        mem = idx_chocs[a:b + 1]
        i_first, i_der = int(mem[0]), int(mem[-1])
        signes = np.sign(r[mem]).astype(int)
        classe = 'POSITIF' if np.all(signes > 0) else ('NEGATIF' if np.all(signes < 0) else 'MIXTE')
        clos = silence_complet(ts, choc, i_der)
        A_av = activite_avant(ts, r, i_first)
        A_bp = float(np.max(np.abs(r[mem])))
        I_ep = float(np.max(np.abs(r[mem]) / T_bar[mem]))
        row = {'episode_id': gi, 'date': date_str[i_first], 'ere': era(dates[i_first]),
               'session': session_de(int(minute[i_first])), 'pos_premier': int(minute[i_first] - debut_session(int(minute[i_first]))),
               't_premier': int(ts[i_first]), 't_dernier': int(ts[i_der]),
               'dispo_min': int(ts[i_der] + 16) if clos else None,
               'n_chocs': int(len(mem)), 'signes': ''.join('+' if s > 0 else '-' for s in signes),
               'classe': classe, 'statut': 'CLOS' if clos else 'CLOTURE_INDETERMINEE',
               'A_bp': A_bp, 'I_ep': I_ep, 'somme_abs_r_bp': float(np.sum(np.abs(r[mem]))),
               'duree_min': int(ts[i_der] - ts[i_first]), 'A_avant': A_av,
               'seuil_premier': float(T_bar[i_first]), 'chocs_t': ';'.join(str(int(x)) for x in ts[mem])}
        if clos:
            s = 1 if classe == 'POSITIF' else (-1 if classe == 'NEGATIF' else int(signes[0]))
            sl = sillage(i_der, s, A_bp)
            row['stabilisation'] = float(sl['_post60'] / A_av) if np.isfinite(sl['_post60']) and np.isfinite(A_av) and A_av > 0 else np.nan
            for k in ('R15', 'R30', 'R60', 'excursion_favorable_bp', 'excursion_defavorable_bp', 'part_retracee', 'retournement', 'nouveau_choc'):
                row[k] = sl[k]
        episodes.append(row)
    EP = pd.DataFrame(episodes)
    # bassin de pseudo-evenements: premiere minute eligible par (jour, session, bloc 60 min)
    pseudos = []
    choc_ts_set = set(int(x) for x in ts_chocs)
    for d in range(len(uniq)):
        if not eligible[d]: continue
        a, b = bounds[d], bounds[d + 1]
        remplis = set()
        for i in range(a, b):
            m = int(minute[i])
            nom = session_de(m); sa = debut_session(m); bloc = (m - sa) // 60
            cle = (nom, bloc)
            if cle in remplis: continue
            if not np.isfinite(r[i]) or r[i] == 0 or choc[i]: continue
            A_av = activite_avant(ts, r, i)
            if not np.isfinite(A_av): continue
            if any((int(ts[i]) - k) in choc_ts_set for k in range(1, 61)): continue
            s = 1 if r[i] > 0 else -1
            sl = sillage(i, s, abs(float(r[i])))
            pseudos.append({'pseudo_id': len(pseudos), 'date': date_str[i], 'ere': era(dates[i]),
                            'session': nom, 'bloc': bloc, 'pos': int(m - sa), 't': int(ts[i]),
                            'signe': s, 'r_bp': float(r[i]), 'A_avant': A_av,
                            'R15': sl['R15'], 'R30': sl['R30'], 'R60': sl['R60'],
                            'excursion_favorable_bp': sl['excursion_favorable_bp'],
                            'excursion_defavorable_bp': sl['excursion_defavorable_bp'],
                            'part_retracee': sl['part_retracee'], 'retournement': sl['retournement'],
                            'nouveau_choc': sl['nouveau_choc']})
            remplis.add(cle)
    PS = pd.DataFrame(pseudos)
    EP.round(4).to_csv(ROOT / 'CAMPAIGN_08_EPISODES.csv.gz', index=False, compression='gzip')
    PS.round(4).to_csv(ROOT / 'CAMPAIGN_08_PSEUDOS.csv.gz', index=False, compression='gzip')
    resume = {'partitions_chargees': CHARGER_STATS['chargees'], 'partitions_attendues': CHARGER_STATS['attendues'],
              'barres_m1': int(len(bars)), 'journees_presentes': int(len(uniq)),
              'journees_eligibles': int(eligible.sum()), 'journees_ineligibles': int((~eligible).sum()),
              'chocs_total': int(choc.sum()), 'chocs_positifs': int((r[choc] > 0).sum()), 'chocs_negatifs': int((r[choc] < 0).sum()),
              'episodes_total': int(len(EP)),
              'episodes_par_classe': {k: int(v) for k, v in EP.classe.value_counts().items()} if len(EP) else {},
              'episodes_par_statut': {k: int(v) for k, v in EP.statut.value_counts().items()} if len(EP) else {},
              'pseudo_bassin': int(len(PS)),
              'seuils_journees_eligibles': {'min': float(np.nanmin(seuil_jour[eligible])), 'mediane': float(np.nanmedian(seuil_jour[eligible])), 'max': float(np.nanmax(seuil_jour[eligible]))} if eligible.any() else {}}
    (ROOT / 'C8_COVERAGE.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume), flush=True)

if __name__ == '__main__': main()
