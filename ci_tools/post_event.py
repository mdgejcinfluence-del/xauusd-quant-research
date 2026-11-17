"""POST-EVENT - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement POST_EVENT_PREREG.json."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/post_event'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'POST_EVENT_PARTITION.csv'
def _hook(a,b,c):
    (ROOT/'ERROR.txt').write_text(''.join(traceback.format_exception(a,b,c))); raise b
sys.excepthook=_hook
IS_END=dt.datetime(2020,1,20,9,36,27)

def dl_drive(fid, local, name, exp_size):
    for _t in range(2):
        if subprocess.run(['gdown','-q','--output',local,fid]).returncode==0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size==exp_size: return True
        time.sleep(20*(_t+1))
    import requests as rq
    url=f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'
    for _t in range(2):
        try:
            with rq.get(url, stream=True, timeout=180, headers={'User-Agent':'Mozilla/5.0'}) as r:
                r.raise_for_status()
                with open(local,'wb') as f:
                    for ch in r.iter_content(1<<20): f.write(ch)
            if open(local,'rb').read(4)==b'PAR1' and pathlib.Path(local).stat().st_size==exp_size: return True
        except Exception: pass
        time.sleep(30*(_t+1))
    return False

def checkpoint(state):
    STATE_P.write_text(json.dumps(state))
    if pathlib.Path('.git').exists():
        subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git','add','reports/meta_alpha/post_event']); subprocess.run(['git','commit','-q','-m',f"Checkpoint PostEvent: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

TICKQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0)*10000 AS rbp FROM s WINDOW w AS (ORDER BY oid)),
x AS (SELECT *, sign(rbp) AS dir,
  (lead(mid,10) OVER (ORDER BY oid)-mid)/NULLIF(mid,0)*10000 AS f10,
  (lead(mid,50) OVER (ORDER BY oid)-mid)/NULLIF(mid,0)*10000 AS f50,
  (lead(mid,100) OVER (ORDER BY oid)-mid)/NULLIF(mid,0)*10000 AS f100 FROM e)
SELECT
 sum(CASE WHEN abs(rbp)>10 THEN 1 ELSE 0 END), avg(CASE WHEN abs(rbp)>10 THEN dir*f10 END), avg(CASE WHEN abs(rbp)>10 THEN dir*f50 END), avg(CASE WHEN abs(rbp)>10 THEN dir*f100 END), avg(CASE WHEN abs(rbp)>10 THEN spread_rel*10000 END),
 sum(CASE WHEN abs(rbp)>20 THEN 1 ELSE 0 END), avg(CASE WHEN abs(rbp)>20 AND (SELECT count(*) FROM x x2 WHERE abs(x2.rbp)>20)>=30 THEN dir*f10 END), avg(CASE WHEN abs(rbp)>20 AND (SELECT count(*) FROM x x2 WHERE abs(x2.rbp)>20)>=30 THEN dir*f50 END), avg(CASE WHEN abs(rbp)>20 AND (SELECT count(*) FROM x x2 WHERE abs(x2.rbp)>20)>=30 THEN dir*f100 END)
FROM x"""
BARQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r, epoch(t-lag(t) OVER w) AS dt_s FROM s WINDOW w AS (ORDER BY oid)),
g0 AS (SELECT *, sum(CASE WHEN dt_s>60 THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS seg FROM e),
g AS (SELECT *, row_number() OVER (PARTITION BY seg ORDER BY oid) AS rn FROM g0),
b AS (SELECT seg, (rn-1)//100 AS bk, min(t) AS t0, arg_min(mid,oid) AS m0, arg_max(mid,oid) AS m1, avg(spread_rel)*10000 AS sp FROM g GROUP BY seg,bk),
bb AS (SELECT *, (m1/m0-1)*10000 AS bret FROM b),
x AS (SELECT *, sign(bret) AS dir, lead(bret,1) OVER (ORDER BY t0) AS n1, lead(bret,3) OVER (ORDER BY t0) AS n3 FROM bb)
SELECT sum(CASE WHEN abs(bret)>10 THEN 1 ELSE 0 END), avg(CASE WHEN abs(bret)>10 THEN dir*n1 END), avg(CASE WHEN abs(bret)>10 THEN dir*n3 END), avg(CASE WHEN abs(bret)>10 THEN sp END) FROM x"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts=[p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    kstate=json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof={name: info['batch'] for name, info in kstate['uploaded'].items()}
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,n10,f10,f50,f100,spread_evt,n20,f10_20,f50_20,f100_20,bar_n,bar_n1,bar_n3,bar_spread\n")
    # grouper les partitions restantes par lot Kaggle pour un seul telechargement par lot
    remaining=[p for p in parts if p['name'] not in state['done']]
    from collections import OrderedDict
    groups=OrderedDict()
    for p in remaining: groups.setdefault(batchof.get(p['name'],'DRIVE'), []).append(p)
    api=None; username=None
    for batch, ps in groups.items():
        localdir=None
        if batch!='DRIVE' and (os.environ.get('KAGGLE_API_TOKEN') or os.environ.get('KAGGLE_KEY')):
            try:
                if api is None:
                    from kaggle.api.kaggle_api_extended import KaggleApi
                    api=KaggleApi(); api.authenticate(); username=api.config_values.get('username')
                localdir=f'/tmp/kbatch'
                shutil.rmtree(localdir, ignore_errors=True)
                api.dataset_download_files(f'{username}/{batch}', path=localdir, unzip=True, quiet=True)
                print('lot Kaggle pret:', batch, flush=True)
            except Exception as e:
                print('lot Kaggle indisponible, repli Drive:', batch, str(e)[:120], flush=True); localdir=None
        for p in ps:
            cand=f"{localdir}/{p['name']}" if localdir else None
            if cand and pathlib.Path(cand).exists() and open(cand,'rb').read(4)==b'PAR1':
                local=cand
            else:
                local=f"/tmp/{p['name']}"
                if not dl_drive(p['drive_id'], local, p['name'], p['file_bytes']):
                    state.setdefault('skipped',[]).append(p['name']); checkpoint(state); print('SKIP', p['name'], flush=True); continue
            r=list(con.execute(TICKQ.format(f=local)).fetchone())+list(con.execute(BARQ.format(f=local)).fetchone())
            with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('post-event termine:', len(state['done']))
if __name__=='__main__': main()
