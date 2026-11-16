"""MONTHLY REFERENCE - IS seul, lecture seule. Pre-enregistrement MONTHLY_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/monthly_reference'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'PARTITION_MONTH.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/monthly_reference']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Monthly Reference: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
Q="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0, lag(mid) OVER w AS mid0, lag(t) OVER w AS t0 FROM s WINDOW w AS (ORDER BY oid)),
v AS (SELECT *, (mid-mid0)/NULLIF(mid0,0) AS r, epoch(t-t0) AS dt_s,
  CASE WHEN bid<>bid0 AND ask<>ask0 THEN 'both' WHEN bid<>bid0 THEN 'bonly' WHEN ask<>ask0 THEN 'aonly' ELSE 'none' END AS etype FROM e)
SELECT strftime(t,'%Y-%m'), count(*), sum(CASE WHEN etype='both' THEN 1 ELSE 0 END), sum(CASE WHEN etype='bonly' THEN 1 ELSE 0 END),
 sum(CASE WHEN etype='aonly' THEN 1 ELSE 0 END), sum(CASE WHEN etype='none' THEN 1 ELSE 0 END),
 avg(spread_rel), approx_quantile(spread_rel,0.5), sum(coalesce(r*r,0)), avg(dt_s), sum(CASE WHEN r=0 THEN 1 ELSE 0 END)
FROM v GROUP BY 1 ORDER BY 1"""
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,month,n,n_both,n_bonly,n_aonly,n_none,spread_mean,spread_p50,sumsq_r,dt_mean,n_r0\n")
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        with open(OUT,'a') as fh:
            for row in con.execute(Q.format(f=local)).fetchall():
                fh.write(p['name']+','+str(row[0])+','+','.join('' if v is None else str(float(v)) for v in row[1:])+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%40==0: checkpoint(state)
        print('MONTHLY',p['name'],flush=True)
    checkpoint(state); print('monthly termine:',len(state['done']))
if __name__=='__main__': main()
