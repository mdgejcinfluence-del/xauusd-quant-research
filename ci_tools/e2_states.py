"""INTEGRAL_SCAN - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement INTEGRAL_PREREG.json (seq 46-47)."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase2/e2_states'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'E2_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase2/e2_states']); subprocess.run(['git','commit','-q','-m',f"Checkpoint E2: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

COLS="nbars,ss_med,ss_le25,vq_med,vq_gt80,aq_med,corr_vq_next,corr_ss_next,run_bar,jump_share"
BARS="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(mid) OVER (ORDER BY oid) AS pm FROM s),
d AS (SELECT *, (mid-pm)/pm*10000 AS rbp FROM v)
SELECT floor(epoch(t)/60) AS bkt, avg(spbp), sum(coalesce(rbp,0)*coalesce(rbp,0)), count(*), arg_max(mid, oid) FROM d GROUP BY bkt ORDER BY bkt"""

def causal_quantile(x, W=20000, MINP=500):
    import bisect
    out=[float('nan')]*len(x); win=[]
    for i, val in enumerate(x):
        if len(win)>=MINP:
            out[i]=bisect.bisect_left(win, val)/len(win)
        bisect.insort(win, val)
        if len(win)>W: win.pop(0)
    return out

def process(rows):
    import pandas as pd, numpy as np
    df=pd.DataFrame(rows, columns=['bkt','sp','rv','n','close']).sort_values('bkt')
    ret=(df['close'].diff()/df['close'].shift(1)*10000)
    ewma=df['rv'].ewm(alpha=0.06, adjust=False).mean()
    ss=causal_quantile(df['sp'].tolist()); vq=causal_quantile(ewma.tolist()); aq=causal_quantile(df['n'].astype(float).tolist())
    df['ss'],df['vq'],df['aq']=ss,vq,aq; df['ret']=ret
    nxt=df['ret'].abs().shift(-1)
    c1=df[['vq']].join(nxt.rename('nx')).dropna()
    c2=df[['ss']].join(df['sp'].shift(-1).rename('ns')).dropna()
    sg=np.sign(ret.fillna(0).values); runs=[]; cur=0; prev=0
    for v in sg:
        if v!=0 and v==prev: cur+=1
        elif v!=0: cur=1; prev=v
        else: cur=0; prev=0
        if v!=0: runs.append(cur)
    # longueur moyenne de serie: moyenne des longueurs completes approximee par 1/(taux de changement de signe)
    nz=sg[sg!=0]; chg=float((nz[1:]!=nz[:-1]).mean()) if len(nz)>2 else 0.0; runlen=float(1.0/chg) if chg>0 else float(len(nz))
    def m(x): 
        v=pd.Series(x).dropna(); return float(v.median()) if len(v) else float('nan')
    return (len(df), m(ss), float((pd.Series(ss)<=0.25).mean()), m(vq), float((pd.Series(vq)>0.8).mean()), m(aq),
            float(c1['vq'].rank().corr(c1['nx'].rank())) if len(c1)>50 else float('nan'),
            float(c2['ss'].rank().corr(c2['ns'].rank())) if len(c2)>50 else float('nan'),
            runlen, float((ret.abs()>10).mean()))
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
            r=tuple(process(con.execute(BARS.format(f=local)).fetchall()))
            with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('E2 termine:', len(state['done']))
if __name__=='__main__': main()
