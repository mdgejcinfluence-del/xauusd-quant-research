"""PHASE 12.3 - INVENTAIRE DE CONFIGURATIONS SANS PERFORMANCE (seq149).
COMPTAGE SEUL: aucun rendement, aucun PnL, aucune sortie de trade n'est calculee.
Definitions figees (blueprint seq144/146/148): barres 1 min (mid de cotation, declare),
niveaux Asie [00,08) UTC du jour et veille UTC; fenetres d'entree Londres [08,13) et
New York [13,21) UTC; exclusion news [T-5,T+5] (calendrier PIT). S12-01: bougie cloture
au-dela du niveau puis bougie suivante cloture reintegree. S12-02: cloture au-dela de
L+buffer, retest (retour a L +/- 0,05%) avec cloture du bon cote sous 60 min.
Sortie: une ligne par configuration detectee (scenario, direction, niveau, buffer BK)."""
import json, pathlib, subprocess, os, time, datetime as dt, sys, shutil, traceback
import duckdb
import numpy as np
import pandas as pd

ROOT = pathlib.Path('reports/meta_alpha/phase12_3'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT / 'STATE.json'; OUT = ROOT / 'P12_3_CONFIGURATIONS.csv'
def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)

NEWS = []
for line in open('reports/meta_alpha/phase6/F15_EVENTS.csv').read().splitlines()[1:]:
    if not line.strip(): continue
    typ, t = line.rsplit(',', 1)
    NEWS.append(dt.datetime.fromisoformat(t.replace('Z', '+00:00')).replace(tzinfo=None))
def bloque(ts):
    return any((n - dt.timedelta(minutes=5)) <= ts <= (n + dt.timedelta(minutes=5)) for n in NEWS)

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

def detecter(bars):
    """bars: DataFrame ts,o,h,l,c (1 min, mid). Retourne liste de configurations."""
    ev = []
    bars = bars.copy(); bars['date'] = bars.ts.dt.date; bars['heure'] = bars.ts.dt.hour
    jours = {d: g for d, g in bars.groupby('date')}
    dates = sorted(jours)
    for di, d in enumerate(dates):
        g = jours[d].reset_index(drop=True)
        asia = g[(g.ts.dt.hour >= 0) & (g.ts.dt.hour < 8)]
        if len(asia) < 60: continue
        niveaux = {'ASIE': (float(asia.h.max()), float(asia.l.min()))}
        if di > 0:
            pv = jours[dates[di - 1]]
            niveaux['VEILLE'] = (float(pv.h.max()), float(pv.l.min()))
        w = g[((g.ts.dt.hour >= 8) & (g.ts.dt.hour < 21))].reset_index(drop=True)
        if len(w) < 60: continue
        for src, (hi, lo) in niveaux.items():
            for direction, L, sens, Lbk in [('LONG', lo, -1, hi), ('COURT', hi, +1, lo)]:
                # S12-01 sweep & reintegration
                for i in range(len(w) - 1):
                    traverse = (w.c[i] < L) if sens == -1 else (w.c[i] > L)
                    reintegre = (w.c[i + 1] > L) if sens == -1 else (w.c[i + 1] < L)
                    if traverse and reintegre and not bloque(w.ts[i + 1]):
                        ev.append(('S12-01', direction, src, 0, str(d), w.ts[i + 1].isoformat()))
                # S12-02 breakout + retest
                for bk in [2, 5]:
                    L = Lbk  # cassure: LONG franchit le HAUT, COURT franchit le BAS
                    buf = L * bk / 10000.0
                    i = 0
                    while i < len(w):
                        casse = (w.c[i] > L + buf) if sens == +1 else (w.c[i] < L - buf)
                        # direction cassee: LONG casse le HAUT, COURT casse le BAS -> gerer via niveau oppose
                        if casse:
                            for j in range(i + 1, min(i + 61, len(w))):
                                touche = (w.l[j] <= L * 1.0005 and w.c[j] > L) if sens == +1 else (w.h[j] >= L * 0.9995 and w.c[j] < L)
                                if touche:
                                    if not bloque(w.ts[j]): ev.append(('S12-02', direction, src, bk, str(d), w.ts[j].isoformat()))
                                    i = j; break
                        i += 1
    return ev

def main():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    state = json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done': []}
    con = duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("scenario,direction,niveau,buffer_bk_bp,date,ts_confirmation\n")
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts:
        if p['name'] not in state['done']: groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    api = None; username = None
    for batch, ps in groups.items():
        localdir = None
        if batch != 'DRIVE' and os.environ.get('KAGGLE_API_TOKEN'):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi(); api.authenticate(); username = api.config_values.get('username')
                localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True)
                api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True)
            except Exception as e:
                print('Kaggle KO, repli Drive:', str(e)[:80], flush=True); localdir = None
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if not pathlib.Path(local).exists():
                if not dl_drive(p.get('drive_id', ''), local, p.get('file_bytes', -1)):
                    state.setdefault('skipped', []).append(p['name']); continue
            try:
                q = f"""SELECT time_bucket(INTERVAL 1 MINUTE, timestamp_utc) AS ts,
                        arg_min(mid, timestamp_utc) AS o, max(mid) AS h, min(mid) AS l, arg_max(mid, timestamp_utc) AS c
                        FROM read_parquet('{local}') GROUP BY 1 ORDER BY 1"""
                bars = con.execute(q).df(); bars['ts'] = pd.to_datetime(bars.ts).dt.tz_localize(None)
                bars = bars.rename(columns={'o': 'o', 'h': 'h', 'l': 'l', 'c': 'c'})
                ev = detecter(bars[['ts', 'h', 'l', 'c']])
                with open(OUT, 'a') as fh:
                    for e in ev: fh.write(",".join(map(str, e)) + "\n")
            except Exception as e:
                (ROOT / 'ERROR.txt').write_text(f"{p['name']}: {type(e).__name__} {e}")
            state['done'].append(p['name'])
            if len(state['done']) % 40 == 0:
                STATE_P.write_text(json.dumps(state))
                subprocess.run(['git', 'add', 'reports/meta_alpha/phase12_3']); subprocess.run(['git', 'commit', '-q', '-m', f"P12.3 checkpoint {len(state['done'])}"])
                subprocess.run(['git', 'pull', '--rebase', '-q', 'origin', 'arena/afe12737-xauusd-quant-research']); subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:arena/afe12737-xauusd-quant-research'])
            print('P12.3 part:', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    STATE_P.write_text(json.dumps(state)); print('P12.3 COMPTAGE TERMINE', len(state['done']))

if __name__ == '__main__': main()
