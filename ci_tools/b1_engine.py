"""F15 - MOTEUR EVENEMENTS x TICK (preenregistre seq109, gate R3 TESTABLE seq-fichier F15_F16_GATES).
Entree: premier tick >= T+60s. Premier mouvement: signe(mid a T+5min - mid entree).
Sorties H in {15,60,240} min: premier tick >= T+H. PnL executable (bid/ask) + PnL mid.
Placebos calendaires: T decale de -30 j et +30 j (meme protocole, H=60, mid).
Aucune statistique ici: extraction brute seulement, checkpoint par lot Kaggle."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT = pathlib.Path('reports/meta_alpha/phase9/b1_events'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT / 'STATE.json'; OUT = ROOT / 'B1_EVENT_PNL.csv'
def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)

def dl_drive(fid, local, name, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

def checkpoint(state):
    STATE_P.write_text(json.dumps(state))
    if pathlib.Path('.git').exists():
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]']); subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git', 'add', 'reports/meta_alpha/phase6']); subprocess.run(['git', 'commit', '-q', '-m', f"Checkpoint F15: {len(state['done'])}/282"])
        subprocess.run(['git', 'pull', '--rebase', '-q', 'origin', 'arena/afe12737-xauusd-quant-research']); subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:arena/afe12737-xauusd-quant-research'])

EVENTS = []
for line in open('reports/meta_alpha/phase6/F15_EVENTS.csv').read().splitlines()[1:]:
    if not line.strip(): continue
    typ, t = line.rsplit(',', 1)
    EVENTS.append((typ, dt.datetime.fromisoformat(t.replace('Z', '+00:00')).replace(tzinfo=None)))

def extraire(con, fichiers, T):
    """Retourne dict des pnls ou None si couverture insuffisante."""
    fl = "[" + ",".join(f"'{f}'" for f in fichiers) + "]"
    def tick_at(ts, sens='ge'):
        op = '>=' if sens == 'ge' else '<='
        ordre = 'ASC' if sens == 'ge' else 'DESC'
        r = con.execute(f"SELECT timestamp_utc, bid, ask, mid FROM read_parquet({fl}) WHERE timestamp_utc {op} ? ORDER BY timestamp_utc {ordre}, observation_id {ordre} LIMIT 1", [ts]).fetchone()
        return r
    ref = tick_at(T + dt.timedelta(seconds=60))
    if ref is None: return None
    e0 = tick_at(T + dt.timedelta(minutes=5))   # v2: entree APRES le premier mouvement (connu a T+5min)
    if e0 is None: return None
    mouv = (float(e0[3]) - float(ref[3])) / float(ref[3]) * 10000
    res = {'mouv_bp': mouv, 'spread_entree_bp': (float(e0[2]) - float(e0[1])) / float(e0[3]) * 10000}
    for H in [15, 60, 240]:
        x = tick_at(T + dt.timedelta(minutes=H))
        if x is None: return None
        eb, ea, em = float(e0[1]), float(e0[2]), float(e0[3])
        xb, xa, xm = float(x[1]), float(x[2]), float(x[3])
        res[f'exec_long_{H}'] = (xb - ea) / ea * 10000
        res[f'exec_short_{H}'] = (eb - xa) / eb * 10000
        res[f'mid_{H}'] = (xm - em) / em * 10000
    return res

def main():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts = [p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None) <= IS_END]
    kstate = json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof = {name: info['batch'] for name, info in kstate['uploaded'].items()}
    spans = []
    for p in parts:
        lo = dt.datetime.fromisoformat(p['timestamp_min_footer'].replace('Z', '+00:00')).replace(tzinfo=None) if p.get('timestamp_min_footer') else dt.datetime(2009, 1, 1)
        hi = dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z', '+00:00')).replace(tzinfo=None)
        spans.append((lo, hi, p))
    state = json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done': []}
    con = duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("type,t_avail,dec, mouv_bp,spread_entree_bp,exec_long_15,exec_short_15,mid_15,exec_long_60,exec_short_60,mid_60,exec_long_240,exec_short_240,mid_240\n".replace(' ', ''))
    # indexer les evenements (et placebos) par partition contenant T
    todo = {}
    for typ, T in EVENTS:
        for dec in [0, -7, 7]:
            Td = T + dt.timedelta(days=dec)
            if Td > IS_END or Td < dt.datetime(2010, 1, 1): continue
            for i, (lo, hi, p) in enumerate(spans):
                if lo - dt.timedelta(hours=5) <= Td <= hi:
                    todo.setdefault(p['name'], []).append((typ, T, dec, i)); break
    from collections import OrderedDict
    groups = OrderedDict()
    for p in parts:
        if p['name'] in todo and p['name'] not in state['done']:
            groups.setdefault(batchof.get(p['name'], 'DRIVE'), []).append(p)
    api = None; username = None
    for batch, ps in groups.items():
        localdir = None
        if batch != 'DRIVE' and (os.environ.get('KAGGLE_API_TOKEN') or os.environ.get('KAGGLE_KEY')):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api = KaggleApi(); api.authenticate(); username = api.config_values.get('username')
                localdir = '/tmp/kbatch'; shutil.rmtree(localdir, ignore_errors=True)
                api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True)
                print('lot Kaggle pret:', batch, flush=True)
            except Exception as e:
                print('lot Kaggle indisponible, repli Drive:', batch, str(e)[:120], flush=True); localdir = None
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if local.startswith('/tmp/part_') and not pathlib.Path(local).exists():
                if not dl_drive(p['drive_id'], local, p['name'], p['file_bytes']):
                    state.setdefault('skipped', []).append(p['name']); continue
            idx = [i for i, (lo, hi, pp) in enumerate(spans) if pp['name'] == p['name']][0]
            fichiers = [local]
            for j in [idx - 1, idx + 1]:
                if 0 <= j < len(spans):
                    np_ = spans[j][2]['name']
                    c2 = f"{localdir}/{np_}" if localdir else f"/tmp/{np_}"
                    if pathlib.Path(c2).exists(): fichiers.append(c2)
            for typ, T, dec, i in todo[p['name']]:
                Td = T + dt.timedelta(days=dec)
                r = extraire(con, fichiers, Td)
                if r is None: continue
                with open(OUT, 'a') as fh:
                    fh.write(f"{typ},{T.isoformat()},{dec},{r['mouv_bp']:.3f},{r['spread_entree_bp']:.3f}," + ",".join(f"{r[f'{k}_{H}']:.4f}" for H in [15, 60, 240] for k in ['exec_long', 'exec_short', 'mid']) + "\n")
            if local.startswith('/tmp/part_') and (not localdir or local != f"{localdir}/{p['name']}"): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done']) % 20 == 0: checkpoint(state)
            print('B1 part traitee:', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('B1 extraction terminee:', len(state['done']))
if __name__ == '__main__': main()
