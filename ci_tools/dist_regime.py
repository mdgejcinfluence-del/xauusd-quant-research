"""DIST REGIME - IS seul, lecture seule. Pre-enregistrement DIST_REGIME_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/dist_regime'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'DIST_REGIME_PARTITION.csv'
def _hook(a,b,c):
    (ROOT/'ERROR.txt').write_text(''.join(traceback.format_exception(a,b,c))); raise b
sys.excepthook=_hook
_s=dt.datetime.fromisoformat("2010-01-04 00:01:10.457"); _e=dt.datetime.fromisoformat("2026-09-30 23:59:58.864")
IS_END=_s+0.6*(_e-_s)
def dl(fid, local, name):
    for _t in range(3):
        if subprocess.run(['gdown','-q','--output',local,fid]).returncode==0: return
        time.sleep(30*(_t+1))
    import requests as rq
    exp={x['name']:x['file_bytes'] for x in json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']}
    url=f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'
    for _t in range(3):
        try:
            with rq.get(url, stream=True, timeout=120, headers={'User-Agent':'Mozilla/5.0'}) as r:
                r.raise_for_status()
                with open(local,'wb') as f:
                    for ch in r.iter_content(1<<20): f.write(ch)
            if open(local,'rb').read(4)==b'PAR1' and pathlib.Path(local).stat().st_size==exp[name]: return
        except Exception: pass
        time.sleep(60*(_t+1))
    raise RuntimeError(f'telechargement impossible: {name}')
def checkpoint(state):
    STATE_P.write_text(json.dumps(state))
    if pathlib.Path('.git').exists():
        subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git','add','reports/meta_alpha/dist_regime']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Dist Regime: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
def qs(expr, ps):
    return ', '.join(f"approx_quantile({expr},{p})" for p in ps)
PS=[0.001,0.01,0.05,0.25,0.5,0.75,0.95,0.99,0.999]
Q = f"""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{{f}}')),
e AS (SELECT *, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0, lag(mid) OVER w AS mid0, lag(t) OVER w AS t0 FROM s WINDOW w AS (ORDER BY oid)),
v AS (SELECT *, (mid-mid0)/NULLIF(mid0,0)*10000 AS rbp, epoch(t-t0) AS dt_s, (bid=bid0 AND ask=ask0) AS nochange FROM e),
f AS (SELECT * FROM v WHERE NOT coalesce(nochange,false) AND rbp IS NOT NULL),
x AS (SELECT *, lag(rbp) OVER (ORDER BY oid) AS rp FROM f),
b AS (SELECT approx_quantile(rbp,0.001) AS bq0, approx_quantile(rbp,0.01) AS bq1, approx_quantile(rbp,0.05) AS bq2, approx_quantile(rbp,0.25) AS bq3, approx_quantile(rbp,0.5) AS bq4, approx_quantile(rbp,0.75) AS bq5, approx_quantile(rbp,0.95) AS bq6, approx_quantile(rbp,0.99) AS bq7, approx_quantile(rbp,0.999) AS bq8 FROM v WHERE rbp IS NOT NULL)
SELECT (SELECT count(*) FROM v) AS n_brut, (SELECT count(*) FROM f) AS n_filtre,
 (SELECT bq0 FROM b), (SELECT bq1 FROM b), (SELECT bq2 FROM b), (SELECT bq3 FROM b), (SELECT bq4 FROM b), (SELECT bq5 FROM b), (SELECT bq6 FROM b), (SELECT bq7 FROM b), (SELECT bq8 FROM b), {qs('rbp',PS)},
 {', '.join(f"approx_quantile(abs(rbp),{q})" for q in [0.5,0.95,0.99])},
 {', '.join(f"approx_quantile(dt_s,{q})" for q in [0.05,0.25,0.5,0.75,0.95,0.99])},
 {', '.join(f"approx_quantile(spread_rel*10000,{q})" for q in [0.05,0.5,0.95,0.99])},
 corr(rbp, rp)
FROM x"""
COLS="partition,n_brut,n_filtre,"+",".join(f"brut_p{int(p*1000)}" for p in PS)+","+",".join(f"filt_p{int(p*1000)}" for p in PS)+",filt_abs_p50,filt_abs_p95,filt_abs_p99,dt_p5,dt_p25,dt_p50,dt_p75,dt_p95,dt_p99,spread_p5,spread_p50,spread_p95,spread_p99,ac1_filtre\n"
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text(COLS)
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        r=con.execute(Q.format(f=local)).fetchone()
        with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%40==0: checkpoint(state)
        print('DIST',p['name'],flush=True)
    checkpoint(state); print('dist termine:',len(state['done']))
if __name__=='__main__': main()
