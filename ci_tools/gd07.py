"""GD07 - IS cible, lecture seule. Pre-enregistrement GD07_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/gd07'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'GD07_PARTITION.csv'
def _hook(a,b,c):
    (ROOT/'ERROR.txt').write_text(''.join(traceback.format_exception(a,b,c))); raise b
sys.excepthook=_hook
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
        subprocess.run(['git','add','reports/meta_alpha/gd07']); subprocess.run(['git','commit','-q','-m',f"Checkpoint GD07: {len(state['done'])}/55"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
Q="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0, lag(mid) OVER w AS mid0, lag(t) OVER w AS t0 FROM s WINDOW w AS (ORDER BY oid)),
v AS (SELECT *, (mid-mid0)/NULLIF(mid0,0) AS r, epoch(t-t0) AS dt_s, (bid=bid0 AND ask=ask0) AS nochange, ((mid-mid0)=0) AS z FROM e),
g AS (SELECT *, sum(CASE WHEN z IS DISTINCT FROM lag(z) OVER (ORDER BY oid) THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS grp FROM v),
runs AS (SELECT grp, count(*) AS len, epoch(max(t)-min(t)) AS dur FROM g WHERE z GROUP BY grp)
SELECT (SELECT avg(CASE WHEN z THEN 1.0 WHEN r IS NULL THEN NULL ELSE 0 END) FROM v),
 (SELECT approx_quantile(len,0.5) FROM runs), (SELECT approx_quantile(len,0.95) FROM runs), (SELECT max(len) FROM runs), (SELECT max(dur) FROM runs),
 (SELECT avg(spread_rel) FROM v WHERE z), (SELECT avg(spread_rel) FROM v WHERE NOT z),
 (SELECT avg(dt_s) FROM v WHERE z), (SELECT avg(dt_s) FROM v WHERE NOT z),
 (SELECT avg(CASE WHEN nochange THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END) FROM v)"""
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if 'part_000211'<=p['name']<='part_000265.parquet']
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,share_r0,run_p50,run_p95,run_max,run_dur_max_s,spread_in_zero,spread_out_zero,dt_in_zero,dt_out_zero,share_nochange\n")
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        r=con.execute(Q.format(f=local)).fetchone()
        with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%20==0: checkpoint(state)
        print('GD07',p['name'],flush=True)
    checkpoint(state); print('gd07 termine:',len(state['done']))
if __name__=='__main__': main()
