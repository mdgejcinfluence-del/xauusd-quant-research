"""INTEGRAL_SCAN - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement INTEGRAL_PREREG.json (seq 46-47)."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase2/e3_measures'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'E3_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase2/e3_measures']); subprocess.run(['git','commit','-q','-m',f"Checkpoint E3: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

COLS="nbars,rv_med,j_mean,j_share,bpv_share,ori10_med,ori50_med,ori200_med,ori50_q90"
BARS="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(mid) OVER (ORDER BY oid) AS pm, lag(bid) OVER (ORDER BY oid) AS pb, lag(ask) OVER (ORDER BY oid) AS pa FROM s),
d AS (SELECT *, (mid-pm)/pm*10000 AS rbp, floor(epoch(t)/60) AS bkt FROM v),
w AS (SELECT *, lag(rbp) OVER (ORDER BY oid) AS lr, lag(bkt) OVER (ORDER BY oid) AS lbkt FROM d)
SELECT bkt, sum(coalesce(rbp,0)*coalesce(rbp,0)), 1.5707963*sum(CASE WHEN bkt=lbkt THEN abs(rbp)*abs(lr) ELSE 0 END), count(*) FROM w GROUP BY bkt ORDER BY bkt"""
ORI="""
WITH s AS (SELECT observation_id AS oid, bid, ask FROM read_parquet('{f}')),
v AS (SELECT *, lag(bid) OVER (ORDER BY oid) AS pb, lag(ask) OVER (ORDER BY oid) AS pa FROM s),
d AS (SELECT *, (CASE WHEN bid>pb THEN 1 WHEN bid<pb THEN -1 ELSE 0 END)+(CASE WHEN ask>pa THEN 1 WHEN ask<pa THEN -1 ELSE 0 END) AS u FROM v WHERE pb IS NOT NULL),
w AS (SELECT *, sum(u) OVER (ORDER BY oid ROWS BETWEEN 9 PRECEDING AND CURRENT ROW)/20.0 AS o10, sum(u) OVER (ORDER BY oid ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)/100.0 AS o50, sum(u) OVER (ORDER BY oid ROWS BETWEEN 199 PRECEDING AND CURRENT ROW)/400.0 AS o200 FROM d)
SELECT approx_quantile(abs(o10),0.5), approx_quantile(abs(o50),0.5), approx_quantile(abs(o200),0.5), approx_quantile(abs(o50),0.9) FROM w"""

def process(rows, ori):
    import pandas as pd, numpy as np
    df=pd.DataFrame(rows, columns=['bkt','rv','bpv','n'])
    rv=df['rv'].replace(0, np.nan); j=((rv-df['bpv'])/rv).clip(lower=0)
    return (len(df), float(rv.median()), float(j.mean()), float((j>0.2).mean()), float((df['bpv']/rv).median()),
            float(ori[0]), float(ori[1]), float(ori[2]), float(ori[3]))
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts=[p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    kstate=json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof={name: info['batch'] for name, info in kstate['uploaded'].items()}
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,"+COLS+"\n")
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
            r=tuple(process(con.execute(BARS.format(f=local)).fetchall(), con.execute(ORI.format(f=local)).fetchone()))
            with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('E3 termine:', len(state['done']))
if __name__=='__main__': main()
