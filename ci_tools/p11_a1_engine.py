"""P11-A1 - RECONSTITUTION DESCRIPTIVE TICK NEWS T-5..T+30 (autorisation proprietaire seq141).
DESCRIPTIF SEUL: aucun signal, aucun PnL strategique, aucune optimisation.
Pour chaque evenement F15 (available_at_utc PIT) et chaque minute m in [-5, +30]:
n ticks, spread cote bp (mediane/P90/P95/P99/max), mid debut/fin, ecarts inter-ticks
(mediane/max secondes), trou max. Sortie: une ligne par (evenement, minute).
Corpus: lac Kaggle du programme uniquement; rien de brut n'est committe."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
import numpy as np

def dl_drive(fid, local, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown', '-q', '--output', local, fid]).returncode == 0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size == exp_size: return True
        time.sleep(20 * (_t + 1))
    return False

ROOT = pathlib.Path('reports/meta_alpha/p11_a1'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT / 'STATE.json'; OUT = ROOT / 'P11_A1_EVENT_MINUTES.csv'
def _hook(a, b, c):
    (ROOT / 'ERROR.txt').write_text(''.join(traceback.format_exception(a, b, c))); raise b
sys.excepthook = _hook
IS_END = dt.datetime(2020, 1, 20, 9, 36, 27)

EVENTS = []
for line in open('reports/meta_alpha/phase6/F15_EVENTS.csv').read().splitlines()[1:]:
    if not line.strip(): continue
    typ, t = line.rsplit(',', 1)
    EVENTS.append((typ, dt.datetime.fromisoformat(t.replace('Z', '+00:00')).replace(tzinfo=None)))

def extraire(con, fichiers, T):
    fl = "[" + ",".join(f"'{f}'" for f in fichiers) + "]"
    lo, hi = T - dt.timedelta(minutes=6), T + dt.timedelta(minutes=31)
    rows = con.execute(f"""SELECT timestamp_utc, bid, ask, mid FROM read_parquet({fl})
                           WHERE timestamp_utc >= ? AND timestamp_utc < ? ORDER BY timestamp_utc, observation_id""",
                       [lo, hi]).fetchall()
    if not rows: return None
    out = []
    arr = {}
    for ts, b, a, m in rows:
        minute = int((ts.replace(tzinfo=None) - T).total_seconds() // 60)
        if -5 <= minute <= 30: arr.setdefault(minute, []).append((ts, float(b), float(a), float(m)))
    for minute in range(-5, 31):
        v = arr.get(minute, [])
        if not v:
            out.append({'minute': minute, 'n_ticks': 0, 'couverture': 0}); continue
        sp = np.array([(a - b) / m * 10000 for _, b, a, m in v])
        ts = [x[0] for x in v]
        gaps = np.diff([x.timestamp() for x in ts]) if len(ts) > 1 else np.array([0.0])
        out.append({'minute': minute, 'n_ticks': len(v), 'couverture': 1,
                    'spread_med_bp': float(np.median(sp)), 'spread_p90_bp': float(np.quantile(sp, .9)),
                    'spread_p95_bp': float(np.quantile(sp, .95)), 'spread_p99_bp': float(np.quantile(sp, .99)),
                    'spread_max_bp': float(sp.max()), 'bid_premier': v[0][1], 'ask_premier': v[0][2],
                    'mid_debut': v[0][3], 'mid_fin': v[-1][3],
                    'intertick_med_s': float(np.median(gaps)), 'intertick_max_s': float(gaps.max()),
                    'trou_max_s': float(gaps.max())})
    return out

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
    state['skipped'] = []
    con = duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    hdr = "type,t_avail,minute,n_ticks,couverture,spread_med_bp,spread_p90_bp,spread_p95_bp,spread_p99_bp,spread_max_bp,bid_premier,ask_premier,mid_debut,mid_fin,intertick_med_s,intertick_max_s,trou_max_s"
    if not OUT.exists(): OUT.write_text(hdr + "\n")
    todo = {}
    for typ, T in EVENTS:
        if T > IS_END or T < dt.datetime(2010, 1, 1): continue
        for i, (lo, hi, p) in enumerate(spans):
            if lo - dt.timedelta(hours=5) <= T <= hi:
                todo.setdefault(p['name'], []).append((typ, T)); break
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
                print('lot Kaggle indisponible:', batch, str(e)[:120], flush=True); localdir = None
                (ROOT/'DEBUG.txt').write_text(f'batch={batch} erreur={type(e).__name__}: {e}\nbatches={list(groups)[:5]} token_present={bool(os.environ.get("KAGGLE_API_TOKEN"))}')
        for p in ps:
            cand = f"{localdir}/{p['name']}" if localdir else None
            local = cand if (cand and pathlib.Path(cand).exists()) else f"/tmp/{p['name']}"
            if not pathlib.Path(local).exists():
                if not dl_drive(p.get('drive_id', ''), local, p.get('file_bytes', -1)):
                    state.setdefault('skipped', []).append(p['name']); continue
            idx = [i for i, (lo, hi, pp) in enumerate(spans) if pp['name'] == p['name']][0]
            fichiers = [local]
            if idx + 1 < len(spans):
                c2 = f"{localdir}/{spans[idx + 1][2]['name']}" if localdir else f"/tmp/{spans[idx + 1][2]['name']}"
                if pathlib.Path(c2).exists(): fichiers.append(c2)
            for typ, T in todo[p['name']]:
                r = extraire(con, fichiers, T)
                if r is None: continue
                with open(OUT, 'a') as fh:
                    for d in r:
                        fh.write(f"{typ},{T.isoformat()},{d['minute']},{d['n_ticks']},{d['couverture']}," +
                                 ",".join('' if k not in d else f"{d[k]:.4f}" for k in
                                          ['spread_med_bp','spread_p90_bp','spread_p95_bp','spread_p99_bp','spread_max_bp',
                                           'bid_premier','ask_premier','mid_debut','mid_fin','intertick_med_s','intertick_max_s','trou_max_s']) + "\n")
            state['done'].append(p['name'])
            if len(state['done']) % 20 == 0:
                STATE_P.write_text(json.dumps(state))
                subprocess.run(['git', 'add', 'reports/meta_alpha/p11_a1']); subprocess.run(['git', 'commit', '-q', '-m', f"P11-A1 checkpoint {len(state['done'])}"])
                subprocess.run(['git', 'pull', '--rebase', '-q', 'origin', 'arena/afe12737-xauusd-quant-research']); subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:arena/afe12737-xauusd-quant-research'])
            print('P11-A1 part traitee:', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    STATE_P.write_text(json.dumps(state)); print('P11-A1 EXTRACTION TERMINEE', len(state['done']))

if __name__ == '__main__': main()
