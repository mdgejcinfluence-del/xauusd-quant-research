"""MARKET DIMENSIONS - IS seul, lecture seule. Pre-enregistrement DIMENSIONS_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/market_dimensions'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; HOUR=ROOT/'PARTITION_HOUR.csv'; JUMP=ROOT/'PARTITION_JUMPS.csv'; SCALE=ROOT/'PARTITION_SCALE2.csv'
def _hook(a,b,c):
    (ROOT/'ERROR.txt').write_text(''.join(traceback.format_exception(a,b,c))); raise b
sys.excepthook=_hook
_s=dt.datetime.fromisoformat("2010-01-04 00:01:10.457"); _e=dt.datetime.fromisoformat("2026-09-30 23:59:58.864")
IS_END=_s+0.6*(_e-_s)
def dl(fid, local, name):
    for _t in range(3):
        if subprocess.run(['gdown','-q','--output',local,fid]).returncode==0: return True
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
            if open(local,'rb').read(4)==b'PAR1' and pathlib.Path(local).stat().st_size==exp[name]: return True
        except Exception: pass
        time.sleep(60*(_t+1))
    return False

KAGGLE_DIR=pathlib.Path('/tmp/kaggle_dl')
def kaggle_fetch(name):
    """Bascule connecteur: priorite Kaggle (lot xauusd-is-missing13), repli Drive gere par l'appelant."""
    try:
        target=KAGGLE_DIR/name
        if target.exists() and open(target,'rb').read(4)==b'PAR1': return str(target)
        if not os.environ.get('KAGGLE_API_TOKEN') and not os.environ.get('KAGGLE_KEY'): return None
        from kaggle.api.kaggle_api_extended import KaggleApi
        api=KaggleApi(); api.authenticate(); username=api.config_values.get('username')
        KAGGLE_DIR.mkdir(exist_ok=True)
        api.dataset_download_files(f'{username}/xauusd-is-missing13', path=str(KAGGLE_DIR), unzip=True, quiet=True)
        if target.exists() and open(target,'rb').read(4)==b'PAR1': return str(target)
    except Exception as e:
        print('Kaggle fetch indisponible:', str(e)[:150], flush=True)
    return None

def checkpoint(state):
    STATE_P.write_text(json.dumps(state))
    if pathlib.Path('.git').exists():
        subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git','add','reports/meta_alpha/market_dimensions']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Market Dimensions: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
BASE="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, lag(bid) OVER w AS bid0, lag(ask) OVER w AS ask0, lag(mid) OVER w AS mid0, lag(t) OVER w AS t0 FROM s WINDOW w AS (ORDER BY oid)),
v AS (SELECT *, (mid-mid0)/NULLIF(mid0,0)*10000 AS rbp, epoch(t-t0) AS dt_s,
  CASE WHEN bid<>bid0 AND ask<>ask0 THEN 1.0 WHEN bid0 IS NULL THEN NULL ELSE 0 END AS isboth FROM e)"""
QH=BASE+"""
SELECT hour(t), count(*), avg(spread_rel)*10000, sum(coalesce(rbp*rbp,0)), avg(dt_s), avg(isboth) FROM v GROUP BY 1 ORDER BY 1"""
QJ=BASE+""",
x AS (SELECT *, lead(abs(rbp),1) OVER (ORDER BY oid) AS a1, lead(abs(rbp),5) OVER (ORDER BY oid) AS a5, lead(abs(rbp),10) OVER (ORDER BY oid) AS a10,
  lead(rbp,1) OVER (ORDER BY oid) AS r1 FROM v),
o AS (SELECT *, rank() OVER (ORDER BY abs(rbp) DESC) AS rk, count(*) OVER () AS ntot FROM x WHERE rbp IS NOT NULL)
SELECT count(*), sum(CASE WHEN abs(rbp)>5 THEN 1 ELSE 0 END), sum(CASE WHEN abs(rbp)>10 THEN 1 ELSE 0 END),
 sum(CASE WHEN abs(rbp)>20 THEN 1 ELSE 0 END), sum(CASE WHEN abs(rbp)>50 THEN 1 ELSE 0 END), max(abs(rbp)),
 approx_quantile(rbp,0.0001), approx_quantile(rbp,0.9999),
 sum(CASE WHEN rk<=greatest(1,ntot*0.01) THEN rbp*rbp ELSE 0 END)/nullif(sum(rbp*rbp),0),
 corr(rbp,a1), corr(rbp,a5), corr(rbp,a10), corr(sign(rbp), r1*abs(r1)) FROM o"""
QT="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, (mid-lag(mid) OVER (ORDER BY observation_id))/NULLIF(lag(mid) OVER (ORDER BY observation_id),0) AS r FROM read_parquet('{f}')),
b AS (SELECT floor(epoch(t)/{n}) AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1, sqrt(sum(coalesce(r*r,0))) AS vol FROM s GROUP BY bk),
bb AS (SELECT *, (m1/m0-1)*10000 AS bretbp FROM b),
x AS (SELECT *, lag(bretbp) OVER (ORDER BY t0) AS bp FROM bb)
SELECT count(*), corr(bretbp,bp), approx_quantile(abs(bretbp),0.5), approx_quantile(bretbp,0.99), approx_quantile(bretbp,0.01), approx_quantile(vol,0.5) FROM x"""
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not HOUR.exists(): HOUR.write_text("partition,hour,n,spread_bp,sumsq_rbp,dt_mean,share_both\n")
    if not JUMP.exists(): JUMP.write_text("partition,n,n_gt5,n_gt10,n_gt20,n_gt50,absmax_bp,ret_p001,ret_p9999,top1_var_share,lev_a1,lev_a5,lev_a10,corr_sign_rnext2\n")
    if not SCALE.exists(): SCALE.write_text("partition,scale_s,bars,ac1,absret_p50_bp,ret_p99_bp,ret_p1_bp,vol_p50\n")
    for p in parts:
        if p['name'] in state['done']: continue
        kf=kaggle_fetch(p['name']) if p['name'] in {f'part_{i:06d}.parquet' for i in [269,270,271]+list(range(273,283))} else None
        local=kf if kf else f"/tmp/{p['name']}"
        if not kf and not dl(p['drive_id'], local, p['name']):
            state.setdefault('skipped',[]).append(p['name']); (ROOT/'SKIPPED.json').write_text(json.dumps(state['skipped']))
            checkpoint(state); print('SKIP telechargement:', p['name'], flush=True); continue
        with open(HOUR,'a') as fh:
            for row in con.execute(QH.format(f=local)).fetchall():
                fh.write(p['name']+','+str(int(row[0]))+','+','.join('' if v is None else str(float(v)) for v in row[1:])+'\n')
        r=con.execute(QJ.format(f=local)).fetchone()
        with open(JUMP,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
        with open(SCALE,'a') as fh:
            for n in (300,900,3600):
                rr=con.execute(QT.format(f=local,n=n)).fetchone()
                fh.write(f"{p['name']},{n},"+','.join('' if v is None else str(float(v)) for v in rr)+'\n')
        (os.remove(local) if local.startswith('/tmp/part_') else None); state['done'].append(p['name'])
        if len(state['done'])%40==0: checkpoint(state)
        print('DIM',p['name'],flush=True)
    checkpoint(state); print('dimensions termine:',len(state['done']))
if __name__=='__main__': main()
