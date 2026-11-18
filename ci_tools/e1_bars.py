"""INTEGRAL_SCAN - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement INTEGRAL_PREREG.json (seq 46-47)."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase2/e1_bars'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'E1_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase2/e1_bars']); subprocess.run(['git','commit','-q','-m',f"Checkpoint E1: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

COLS="n,tb50_n,tb50_dur,tb200_n,tb200_dur,tb1000_n,tb1000_dur,s1_n,s1_tpb,s1_amp,s5_n,s5_tpb,s5_amp,s60_n,s60_tpb,s60_amp,s60_spm,r2_n,r2_tpb,r2_dur,r5_n,r5_tpb,r5_dur"
EQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(mid) OVER (ORDER BY oid) AS pm FROM s),
d AS (SELECT *, (mid-pm)/pm*10000 AS rbp, row_number() OVER (ORDER BY oid) AS rn FROM v),
tb50 AS (SELECT count(*) AS nb, avg(dur) AS du FROM (SELECT floor((rn-1)/50) AS b, epoch(max(t)-min(t)) AS dur FROM d GROUP BY b)),
tb200 AS (SELECT count(*) AS nb, avg(dur) AS du FROM (SELECT floor((rn-1)/200) AS b, epoch(max(t)-min(t)) AS dur FROM d GROUP BY b)),
tb1000 AS (SELECT count(*) AS nb, avg(dur) AS du FROM (SELECT floor((rn-1)/1000) AS b, epoch(max(t)-min(t)) AS dur FROM d GROUP BY b)),
s1 AS (SELECT count(*) AS nb, avg(c) AS tpb, avg(amp) AS am, avg(sp) AS spm FROM (SELECT floor(epoch(t)/1) AS b, count(*) AS c, (max(mid)-min(mid))/avg(mid)*10000 AS amp, avg(spbp) AS sp FROM s GROUP BY b)),
s5 AS (SELECT count(*) AS nb, avg(c) AS tpb, avg(amp) AS am, avg(sp) AS spm FROM (SELECT floor(epoch(t)/5) AS b, count(*) AS c, (max(mid)-min(mid))/avg(mid)*10000 AS amp, avg(spbp) AS sp FROM s GROUP BY b)),
s60 AS (SELECT count(*) AS nb, avg(c) AS tpb, avg(amp) AS am, avg(sp) AS spm FROM (SELECT floor(epoch(t)/60) AS b, count(*) AS c, (max(mid)-min(mid))/avg(mid)*10000 AS amp, avg(spbp) AS sp FROM s GROUP BY b)),
rc AS (SELECT *, sum(abs(rbp)) OVER (ORDER BY oid) AS cum FROM d WHERE rbp IS NOT NULL),
r2 AS (SELECT count(*) AS nb, avg(c) AS tpb, avg(dur) AS du FROM (SELECT floor(cum/2) AS b, count(*) AS c, epoch(max(t)-min(t)) AS dur FROM rc GROUP BY b)),
r5 AS (SELECT count(*) AS nb, avg(c) AS tpb, avg(dur) AS du FROM (SELECT floor(cum/5) AS b, count(*) AS c, epoch(max(t)-min(t)) AS dur FROM rc GROUP BY b))
SELECT (SELECT count(*) FROM s), tb50.nb, tb50.du, tb200.nb, tb200.du, tb1000.nb, tb1000.du, s1.nb, s1.tpb, s1.am, s5.nb, s5.tpb, s5.am, s60.nb, s60.tpb, s60.am, s60.spm, r2.nb, r2.tpb, r2.du, r5.nb, r5.tpb, r5.du FROM tb50, tb200, tb1000, s1, s5, s60, r2, r5"""
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
            r=tuple(con.execute(EQ.format(f=local)).fetchone())
            with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('E1 termine:', len(state['done']))
if __name__=='__main__': main()
