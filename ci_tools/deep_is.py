"""VALIDATION PROFONDE IS (descriptif, aucune hypothese, aucun Holdout).
ANOM-001: decomposition Bid/Ask evenement par evenement (preuce directe du mecanisme mid).
ANOM-002: persistance volatilite (retards, regimes, granularite 10 ticks).
Gaps: classes de duree, distributions, retour a la normale.
Exploration: dynamique du spread, asymetrie des mises a jour, non-linearites |r|."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/deep'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; CSV=ROOT/'PARTITION_DEEP.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/deep']); subprocess.run(['git','commit','-q','-m',f"Checkpoint validation profonde IS: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

Q="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *,
  bid-lag(bid) OVER w AS db, ask-lag(ask) OVER w AS da,
  (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r,
  (bid-lag(bid) OVER w)/NULLIF(lag(bid) OVER w,0) AS rb,
  (ask-lag(ask) OVER w)/NULLIF(lag(ask) OVER w,0) AS ra,
  epoch(t-lag(t) OVER w) AS dt_s
  FROM s WINDOW w AS (ORDER BY oid)),
x AS (SELECT *, abs(r) AS ar,
  CASE WHEN db<>0 AND da=0 THEN 1 WHEN db=0 AND da<>0 THEN 2 WHEN db<>0 AND da<>0 THEN 3 ELSE 0 END AS ev,
  lag(r) OVER (ORDER BY oid) AS r1, lag(rb) OVER (ORDER BY oid) AS rb1, lag(ra) OVER (ORDER BY oid) AS ra1,
  lag(CASE WHEN db<>0 AND da=0 THEN 1 WHEN db=0 AND da<>0 THEN 2 WHEN db<>0 AND da<>0 THEN 3 ELSE 0 END) OVER (ORDER BY oid) AS ev1,
  lead(ar,1) OVER (ORDER BY oid) AS ar_n1, lead(ar,5) OVER (ORDER BY oid) AS ar_n5,
  lag(ar,1) OVER (ORDER BY oid) AS ar_p1, lag(ar,5) OVER (ORDER BY oid) AS ar_p5,
  lag(ar) OVER (ORDER BY oid) AS a1, lag(ar,5) OVER (ORDER BY oid) AS a5, lag(ar,20) OVER (ORDER BY oid) AS a20, lag(ar,50) OVER (ORDER BY oid) AS a50,
  lead(r) OVER (ORDER BY oid) AS r_next, spread_rel-lag(spread_rel) OVER (ORDER BY oid) AS dsp,
  lag(spread_rel) OVER (ORDER BY oid) AS sp_prev
  FROM e),
y AS (SELECT *, sign(r) AS sr, lag(sign(r)) OVER (ORDER BY oid) AS sr1 FROM x)
SELECT count(*),
 avg(CASE WHEN ev=1 THEN 1.0 ELSE 0 END), avg(CASE WHEN ev=2 THEN 1.0 ELSE 0 END),
 avg(CASE WHEN ev=3 THEN 1.0 ELSE 0 END), avg(CASE WHEN ev=0 THEN 1.0 ELSE 0 END),
 corr(r,r1), corr(rb,rb1), corr(ra,ra1),
 avg(CASE WHEN ev1 IN (1,2) AND sr=sr1 AND sr<>0 THEN 1.0 WHEN ev1 IN (1,2) AND sr<>0 THEN 0 END),
 avg(CASE WHEN ev1=3 AND sr=sr1 AND sr<>0 THEN 1.0 WHEN ev1=3 AND sr<>0 THEN 0 END),
 corr(ar,a1), corr(ar,a5), corr(ar,a20), corr(ar,a50),
 avg(CASE WHEN ar>0.0002 THEN ar_n1 END), avg(CASE WHEN ar<=0.00001 THEN ar_n1 END),
 sum(CASE WHEN dt_s>60 AND dt_s<=300 THEN 1 ELSE 0 END), avg(CASE WHEN dt_s>60 AND dt_s<=300 THEN r END), avg(CASE WHEN dt_s>60 AND dt_s<=300 THEN ar_n5 END),
 sum(CASE WHEN dt_s>300 AND dt_s<=3600 THEN 1 ELSE 0 END), avg(CASE WHEN dt_s>300 AND dt_s<=3600 THEN r END), avg(CASE WHEN dt_s>300 AND dt_s<=3600 THEN ar_n5 END),
 sum(CASE WHEN dt_s>3600 THEN 1 ELSE 0 END), avg(CASE WHEN dt_s>3600 THEN r END), stddev_samp(CASE WHEN dt_s>3600 THEN r END), avg(CASE WHEN dt_s>3600 THEN (CASE WHEN r>0 THEN 1.0 ELSE 0 END) END), avg(CASE WHEN dt_s>3600 THEN ar_n5 END),
 corr(sp_prev, dsp), avg(CASE WHEN ar<=0.00001 THEN ar_n1 END), avg(CASE WHEN ar>0.00001 AND ar<=0.00005 THEN ar_n1 END), avg(CASE WHEN ar>0.00005 THEN ar_n1 END)
FROM y"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    new=not CSV.exists()
    hdr="partition,n,ev_bonly,ev_aonly,ev_both,ev_none,ac_mid,ac_bid,ac_ask,same_sign_after_single,same_sign_after_both,acabs1,acabs5,acabs20,acabs50,absnext_after_big,absnext_after_small,g60_300_n,g60_300_r,g60_300_post5,g300_3600_n,g300_3600_r,g300_3600_post5,g3600_n,g3600_r,g3600_sd,g3600_pos,g3600_post5,spread_reversion,absnext_b1,absnext_b2,absnext_b3\n"
    with open(CSV,'a') as cf:
        if new: cf.write(hdr)
        for p in parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            try:
                r=con.execute(Q.format(f=local)).fetchone()
            except Exception as ex:
                (ROOT/'ERROR.txt').write_text(f"{p['name']}: {ex}"); raise
            os.remove(local)
            cf.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n'); cf.flush()
            state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('deep', p['name'], flush=True)
    checkpoint(state); print('validation profonde terminee:', len(state['done']))

if __name__=='__main__': main()
