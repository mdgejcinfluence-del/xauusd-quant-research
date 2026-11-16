"""DEEP AXES A/B - IS seul, lecture seule. Pre-enregistrement DEEP_AXES_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/deep_axes'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'DEEP_AXES_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/deep_axes']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Deep Axes: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

MAIN="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
med AS (SELECT approx_quantile(spread_rel,0.5) AS smed FROM s),
e AS (SELECT *, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0, lag(mid) OVER w AS mid0 FROM s WINDOW w AS (ORDER BY oid)),
v AS (SELECT *, (mid-mid0)/NULLIF(mid0,0) AS r, CASE WHEN bid<>bid0 AND ask<>ask0 THEN 'both' WHEN bid<>bid0 THEN 'bonly' WHEN ask<>ask0 THEN 'aonly' ELSE 'none' END AS etype,
        sign(mid-mid0) AS dir FROM e),
x AS (SELECT *, lead(r) OVER (ORDER BY oid) AS rnext, lag(r) OVER (ORDER BY oid) AS rprev FROM v)
SELECT
 avg(CASE WHEN etype='none' THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN etype='bonly' THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN etype='aonly' THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN etype='both' THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END),
 avg(CASE WHEN etype='bonly' THEN dir*rnext*10000 END), avg(CASE WHEN etype='bonly' THEN abs(rnext)*10000 END),
 avg(CASE WHEN etype='bonly' AND rnext<>0 THEN CASE WHEN sign(rnext)=dir THEN 1.0 ELSE 0 END END),
 avg(CASE WHEN etype='aonly' THEN dir*rnext*10000 END), avg(CASE WHEN etype='aonly' THEN abs(rnext)*10000 END),
 avg(CASE WHEN etype='aonly' AND rnext<>0 THEN CASE WHEN sign(rnext)=dir THEN 1.0 ELSE 0 END END),
 avg(CASE WHEN etype='both' THEN dir*rnext*10000 END), avg(CASE WHEN etype='both' THEN abs(rnext)*10000 END),
 avg(CASE WHEN etype='both' AND rnext<>0 THEN CASE WHEN sign(rnext)=dir THEN 1.0 ELSE 0 END END),
 corr(CASE WHEN spread_rel>=(SELECT smed FROM med) THEN r END, CASE WHEN spread_rel>=(SELECT smed FROM med) THEN rprev END),
 corr(CASE WHEN spread_rel<(SELECT smed FROM med) THEN r END, CASE WHEN spread_rel<(SELECT smed FROM med) THEN rprev END)
FROM x"""
BARS="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r, epoch(t-lag(t) OVER w) AS dt_s FROM s WINDOW w AS (ORDER BY oid)),
g0 AS (SELECT *, sum(CASE WHEN dt_s>60 THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS seg FROM e),
g AS (SELECT *, row_number() OVER (PARTITION BY seg ORDER BY oid) AS rn FROM g0),
b AS (SELECT seg, (rn-1)//{n} AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1 FROM g GROUP BY seg,bk),
bb AS (SELECT *, m1/m0-1 AS bret FROM b),
x AS (SELECT *, lag(bret) OVER (ORDER BY t0) AS bp, lead(bret) OVER (ORDER BY t0) AS bn FROM bb)
SELECT count(*), corr(bret,bp), avg(abs(bret))*10000, avg(-sign(bret)*bn)*10000 FROM x"""
BARST="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, (mid-lag(mid) OVER (ORDER BY observation_id))/NULLIF(lag(mid) OVER (ORDER BY observation_id),0) AS r FROM read_parquet('{f}')),
b AS (SELECT floor(epoch(t)/{n}) AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1 FROM s GROUP BY bk),
bb AS (SELECT *, m1/m0-1 AS bret FROM b),
x AS (SELECT *, lag(bret) OVER (ORDER BY t0) AS bp, lead(bret) OVER (ORDER BY t0) AS bn FROM bb)
SELECT count(*), corr(bret,bp), avg(abs(bret))*10000, avg(-sign(bret)*bn)*10000 FROM x"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,share_none,share_bonly,share_aonly,share_both,cont_bonly_bp,absnext_bonly_bp,psame_bonly,cont_aonly_bp,absnext_aonly_bp,psame_aonly,cont_both_bp,absnext_both_bp,psame_both,ac1_highspread,ac1_lowspread,EVT10_bars,EVT10_ac1,EVT10_absret_bp,EVT10_rev_bp,EVT50_bars,EVT50_ac1,EVT50_absret_bp,EVT50_rev_bp,TIME30_bars,TIME30_ac1,TIME30_absret_bp,TIME30_rev_bp,TIME60_bars,TIME60_ac1,TIME60_absret_bp,TIME60_rev_bp\n")
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        vals=list(con.execute(MAIN.format(f=local)).fetchone())
        for n in (10,50): vals+=list(con.execute(BARS.format(f=local,n=n)).fetchone())
        for n in (30,60): vals+=list(con.execute(BARST.format(f=local,n=n)).fetchone())
        with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in vals)+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%20==0: checkpoint(state)
        print('AXES',p['name'],flush=True)
    checkpoint(state); print('axes termine:',len(state['done']))
if __name__=='__main__': main()
