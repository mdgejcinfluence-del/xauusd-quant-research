"""INTEGRAL_SCAN - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement INTEGRAL_PREREG.json (seq 46-47)."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/integral_scan'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'INTEGRAL_PARTITION.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/integral_scan']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Integral: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

COLS="n,price_med,sh_both,sh_bidonly,sh_askonly,sh_repub,sh_midconst_comp,sh_cross,mabs_db_bp,mabs_da_bp,sh_zero_r,absr_p50,absr_p90,absr_p99,absr_max,sh_pos,grid_dm,grid_db,dt_p50,dt_p95,dt_p99,dt_max,sh_dt10,sh_dt60,cv_dt,sp_p10,sp_p50,sp_p90,sp_p99,mabs_dsp,rv_bp2,sum_absr_bp,ac1_r,ac1_absr,ac1_spread,corr_db_da,corr_db_lead_da,corr_da_lead_db,run_len"
EQ1="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(bid) OVER (ORDER BY oid) AS pb, lag(ask) OVER (ORDER BY oid) AS pa, lag(mid) OVER (ORDER BY oid) AS pm, lag(t) OVER (ORDER BY oid) AS pt, lag(spbp) OVER (ORDER BY oid) AS psp FROM s),
d AS (SELECT *, bid-pb AS db, ask-pa AS da, mid-pm AS dm, (mid-pm)/pm*10000 AS rbp, epoch(t-pt) AS dts, spbp-psp AS dsp FROM v WHERE pm IS NOT NULL)
SELECT count(*), median(pm), avg(CASE WHEN db<>0 AND da<>0 THEN 1.0 ELSE 0 END), avg(CASE WHEN db<>0 AND da=0 THEN 1.0 ELSE 0 END), avg(CASE WHEN db=0 AND da<>0 THEN 1.0 ELSE 0 END), avg(CASE WHEN db=0 AND da=0 THEN 1.0 ELSE 0 END), avg(CASE WHEN dm=0 AND (db<>0 OR da<>0) THEN 1.0 ELSE 0 END), (SELECT avg(CASE WHEN bid>=ask THEN 1.0 ELSE 0 END) FROM s), avg(CASE WHEN db<>0 THEN abs(db)/pm*10000 END), avg(CASE WHEN da<>0 THEN abs(da)/pm*10000 END), avg(CASE WHEN dm=0 THEN 1.0 ELSE 0 END), approx_quantile(abs(rbp),0.5), approx_quantile(abs(rbp),0.9), approx_quantile(abs(rbp),0.99), max(abs(rbp)), avg(CASE WHEN dm>0 THEN 1.0 WHEN dm<0 THEN 0.0 END), (SELECT min(abs(dm)) FROM d WHERE abs(dm)>1e-9), (SELECT min(abs(db)) FROM d WHERE abs(db)>1e-9), approx_quantile(dts,0.5), approx_quantile(dts,0.95), approx_quantile(dts,0.99), max(dts), avg(CASE WHEN dts>10 THEN 1.0 ELSE 0 END), avg(CASE WHEN dts>60 THEN 1.0 ELSE 0 END), stddev(dts)/avg(dts), (SELECT approx_quantile(spbp,0.1) FROM s), (SELECT approx_quantile(spbp,0.5) FROM s), (SELECT approx_quantile(spbp,0.9) FROM s), (SELECT approx_quantile(spbp,0.99) FROM s), avg(abs(dsp)), sum(rbp*rbp), sum(abs(rbp)) FROM d"""
EQ2="""
WITH s AS (SELECT observation_id AS oid, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(bid) OVER (ORDER BY oid) AS pb, lag(ask) OVER (ORDER BY oid) AS pa, lag(mid) OVER (ORDER BY oid) AS pm FROM s),
d AS (SELECT oid, spbp, (bid-pb)/pm*10000 AS dbbp, (ask-pa)/pm*10000 AS dabp, (mid-pm)/pm*10000 AS rbp FROM v WHERE pm IS NOT NULL),
w AS (SELECT *, lag(rbp) OVER (ORDER BY oid) AS lr, lag(abs(rbp)) OVER (ORDER BY oid) AS lar, lag(spbp) OVER (ORDER BY oid) AS lsp, lead(dabp) OVER (ORDER BY oid) AS fda, lead(dbbp) OVER (ORDER BY oid) AS fdb FROM d),
nz AS (SELECT *, sign(rbp) AS sg FROM d WHERE rbp<>0),
nz2 AS (SELECT *, lag(sg) OVER (ORDER BY oid) AS psg FROM nz),
g AS (SELECT *, sum(CASE WHEN sg<>coalesce(psg,0) THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS grp FROM nz2),
runs AS (SELECT avg(c) AS rl FROM (SELECT count(*) AS c FROM g GROUP BY grp))
SELECT corr(rbp,lr), corr(abs(rbp),lar), corr(spbp,lsp), corr(dbbp,dabp), corr(dbbp,fda), corr(dabp,fdb), (SELECT rl FROM runs) FROM w"""
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts=[p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    kstate=json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof={name: info['batch'] for name, info in kstate['uploaded'].items()}
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,w_n,w_len,w_len95,w_dur,w_dur95,w_share,w_spread,t_n,t_len,t_len95,t_dur,t_dur95,t_share,t_spread\n")
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
            r=tuple(con.execute(EQ1.format(f=local)).fetchone())+tuple(con.execute(EQ2.format(f=local)).fetchone())
            with open(OUT,'a') as fh: fh.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('integral termine:', len(state['done']))
if __name__=='__main__': main()
