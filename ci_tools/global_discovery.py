"""GLOBAL DISCOVERY etapes 1-2 - IS seul, lecture seule. Pre-enregistrement GLOBAL_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/global_discovery'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; TICK=ROOT/'GLOBAL_TICK_PARTITION.csv'; SCALE=ROOT/'GLOBAL_SCALE_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/global_discovery']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Global Discovery: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

TICKQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r,
        (bid-lag(bid) OVER w)/NULLIF(lag(bid) OVER w,0) AS rb,
        (ask-lag(ask) OVER w)/NULLIF(lag(ask) OVER w,0) AS ra,
        epoch(t-lag(t) OVER w) AS dt_s, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0
      FROM s WINDOW w AS (ORDER BY oid)),
x AS (SELECT *, lag(r) OVER (ORDER BY oid) AS r1, lag(rb) OVER (ORDER BY oid) AS rb1, lag(ra) OVER (ORDER BY oid) AS ra1,
        lag(abs(r),1) OVER (ORDER BY oid) AS a1, lag(abs(r),5) OVER (ORDER BY oid) AS a5, lag(abs(r),20) OVER (ORDER BY oid) AS a20,
        lag(spread_rel) OVER (ORDER BY oid) AS sp1,
        lag(ra,5) OVER (ORDER BY oid) AS ra_m5, lag(ra,4) OVER (ORDER BY oid) AS ra_m4, lag(ra,3) OVER (ORDER BY oid) AS ra_m3, lag(ra,2) OVER (ORDER BY oid) AS ra_m2, lag(ra,1) OVER (ORDER BY oid) AS ra_m1,
        lead(ra,1) OVER (ORDER BY oid) AS ra_p1, lead(ra,2) OVER (ORDER BY oid) AS ra_p2, lead(ra,3) OVER (ORDER BY oid) AS ra_p3, lead(ra,4) OVER (ORDER BY oid) AS ra_p4, lead(ra,5) OVER (ORDER BY oid) AS ra_p5,
        lag(rb,5) OVER (ORDER BY oid) AS rb_m5, lag(rb,4) OVER (ORDER BY oid) AS rb_m4, lag(rb,3) OVER (ORDER BY oid) AS rb_m3, lag(rb,2) OVER (ORDER BY oid) AS rb_m2, lag(rb,1) OVER (ORDER BY oid) AS rb_m1,
        lead(rb,1) OVER (ORDER BY oid) AS rb_p1, lead(rb,2) OVER (ORDER BY oid) AS rb_p2, lead(rb,3) OVER (ORDER BY oid) AS rb_p3, lead(rb,4) OVER (ORDER BY oid) AS rb_p4, lead(rb,5) OVER (ORDER BY oid) AS rb_p5
      FROM e)
SELECT count(*), epoch(max(t)-min(t)), avg(dt_s), approx_quantile(dt_s,0.5), approx_quantile(dt_s,0.95),
 approx_quantile(r,0.01), approx_quantile(r,0.5), approx_quantile(r,0.99), avg(CASE WHEN r=0 THEN 1.0 WHEN r IS NULL THEN NULL ELSE 0 END),
 corr(r,r1), corr(rb,rb1), corr(ra,ra1), corr(abs(r),a1), corr(abs(r),a5), corr(abs(r),a20),
 approx_quantile(spread_rel,0.5), approx_quantile(spread_rel,0.95), approx_quantile(spread_rel,0.99), corr(spread_rel,sp1),
 avg(CASE WHEN bid<>bid0 AND ask=ask0 THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN ask<>ask0 AND bid=bid0 THEN 1.0 WHEN ask0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN bid<>bid0 AND ask<>ask0 THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 corr(rb,ra_m5), corr(rb,ra_m4), corr(rb,ra_m3), corr(rb,ra_m2), corr(rb,ra_m1), corr(rb,ra),
 corr(rb,ra_p1), corr(rb,ra_p2), corr(rb,ra_p3), corr(rb,ra_p4), corr(rb,ra_p5),
 corr(ra,rb_m5), corr(ra,rb_m4), corr(ra,rb_m3), corr(ra,rb_m2), corr(ra,rb_m1),
 corr(ra,rb_p1), corr(ra,rb_p2), corr(ra,rb_p3), corr(ra,rb_p4), corr(ra,rb_p5)
FROM x"""

BASE_EVT="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r, epoch(t-lag(t) OVER w) AS dt_s FROM s WINDOW w AS (ORDER BY oid)),
g0 AS (SELECT *, sum(CASE WHEN dt_s>60 THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS seg FROM e),
g AS (SELECT *, row_number() OVER (PARTITION BY seg ORDER BY oid) AS rn FROM g0),
b AS (SELECT seg, (rn-1)//{n} AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1, sqrt(sum(coalesce(r*r,0))) AS vol FROM g GROUP BY seg,bk),
x AS (SELECT *, lag(m1/m0-1) OVER (ORDER BY t0) AS b1 FROM (SELECT *, m1/m0-1 AS bret FROM b))
SELECT count(*), corr(bret,b1), approx_quantile(vol,0.5) FROM x"""
BASE_TIME="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, (mid-lag(mid) OVER (ORDER BY observation_id))/NULLIF(lag(mid) OVER (ORDER BY observation_id),0) AS r FROM read_parquet('{f}')),
b AS (SELECT floor(epoch(t)/{n}) AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1, sqrt(sum(coalesce(r*r,0))) AS vol FROM s GROUP BY bk),
x AS (SELECT *, lag(m1/m0-1) OVER (ORDER BY t0) AS b1 FROM (SELECT *, m1/m0-1 AS bret FROM b))
SELECT count(*), corr(bret,b1), approx_quantile(vol,0.5) FROM x"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not TICK.exists(): TICK.write_text("partition,n,duration_s,dt_mean,dt_p50,dt_p95,ret_p1,ret_p50,ret_p99,share_r0,ac1_mid,ac1_bid,ac1_ask,acabs1,acabs5,acabs20,spread_p50,spread_p95,spread_p99,ac1_spread,share_bonly,share_aonly,share_both,"+",".join(f"cc_ba_m{k}" for k in (5,4,3,2,1))+","+"cc_ba_0,"+",".join(f"cc_ba_p{k}" for k in (1,2,3,4,5))+","+",".join(f"cc_ab_m{k}" for k in (5,4,3,2,1))+","+",".join(f"cc_ab_p{k}" for k in (1,2,3,4,5))+"\n")
    if not SCALE.exists(): SCALE.write_text("partition,family,scale,bars,ac1_barret,vol_p50\n")
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        r=con.execute(TICKQ.format(f=local)).fetchone()
        with open(TICK,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
        with open(SCALE,'a') as fh:
            for n in (10,50,100,500,1000):
                rr=con.execute(BASE_EVT.format(f=local,n=n)).fetchone()
                fh.write(f"{p['name']},EVT,{n},"+','.join('' if v is None else str(float(v)) for v in rr)+'\n')
            for n in (30,60,300):
                rr=con.execute(BASE_TIME.format(f=local,n=n)).fetchone()
                fh.write(f"{p['name']},TIME,{n},"+','.join('' if v is None else str(float(v)) for v in rr)+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%20==0: checkpoint(state)
        print('GLOBAL',p['name'],flush=True)
    checkpoint(state); print('global termine:',len(state['done']))
if __name__=='__main__': main()
