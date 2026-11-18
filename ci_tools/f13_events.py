"""INTEGRAL_SCAN - IS seul via Kaggle (lots) + repli Drive. Pre-enregistrement INTEGRAL_PREREG.json (seq 46-47)."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys, shutil
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase2/f13_events'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; OUT=ROOT/'F13_GAP.csv'; OUTJ=ROOT/'F13_JUMP.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase2/f13_events']); subprocess.run(['git','commit','-q','-m',f"Checkpoint F13: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

COLS="kind,year,n_tick_or_gap,spread_bp,ret_a,ret_b"
# GAP: evenements vendredi->dimanche par partition; sorties simulees en Python sur fenetres tick
GAPQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(mid) OVER (ORDER BY oid) AS pm, lag(t) OVER (ORDER BY oid) AS pt FROM s)
SELECT oid, t, bid, ask, mid, spbp, pm, pt FROM v WHERE extract('dow' FROM t)=0 AND extract('dow' FROM pt)=5 AND epoch(t-pt)>3600 ORDER BY oid"""
# JUMPS: sauts tick avec ORI pre-saut et retours executables directionnels
JUMPQ="""
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel*10000 AS spbp FROM read_parquet('{f}')),
v AS (SELECT *, lag(mid) OVER (ORDER BY oid) AS pm, lag(bid) OVER (ORDER BY oid) AS pb, lag(ask) OVER (ORDER BY oid) AS pa FROM s),
d AS (SELECT *, (mid-pm)/pm*10000 AS rbp, (CASE WHEN bid>pb THEN 1 WHEN bid<pb THEN -1 ELSE 0 END)+(CASE WHEN ask>pa THEN 1 WHEN ask<pa THEN -1 ELSE 0 END) AS u FROM v WHERE pm IS NOT NULL),
w AS (SELECT *, sum(u) OVER (ORDER BY oid ROWS BETWEEN 50 PRECEDING AND 1 PRECEDING)/100.0 AS ori_pre,
        lead(bid,200) OVER (ORDER BY oid) AS b200, lead(ask,200) OVER (ORDER BY oid) AS a200,
        lead(bid,1000) OVER (ORDER BY oid) AS b1000, lead(ask,1000) OVER (ORDER BY oid) AS a1000 FROM d)
SELECT t, spbp, ori_pre, rbp,
 CASE WHEN rbp>0 THEN (b200-ask)/ask*10000 ELSE (bid-a200)/bid*10000 END,
 CASE WHEN rbp>0 THEN (b1000-ask)/ask*10000 ELSE (bid-a1000)/bid*10000 END,
 CASE WHEN ori_pre>0 THEN (b200-ask)/ask*10000 ELSE (bid-a200)/bid*10000 END
 FROM w WHERE abs(rbp)>10 AND b1000 IS NOT NULL AND ori_pre<>0"""
def process(rows):
    return [tuple(r) for r in rows]
def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    parts=[p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    kstate=json.loads(pathlib.Path('reports/meta_alpha/kaggle_migration/STATE.json').read_text())
    batchof={name: info['batch'] for name, info in kstate['uploaded'].items()}
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not OUT.exists(): OUT.write_text("partition,kind,t_sunday,gap_bp,spread_open_bp,fade_ret_bp,follow_ret_bp,exit_reason,n_fwd\n")
    if not OUTJ.exists(): OUTJ.write_text("partition,kind,t,spbp,ori_pre,rbp,dirjump200,dirjump1000,dirori200\n")
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
            for ev in con.execute(GAPQ.format(f=local)).fetchall():
                oid0, t0 = ev[0], ev[1]
                fri_mid, mid_sun, sp0 = float(ev[6]), float(ev[4]), float(ev[5])
                gap_bp=(mid_sun-fri_mid)/fri_mid*10000
                if abs(gap_bp) < 2*sp0: continue
                import datetime as _dt
                mon14 = (t0 + _dt.timedelta(days=1)).replace(hour=14, minute=0, second=0)
                fwd = con.execute("SELECT timestamp_utc, bid, ask, mid FROM read_parquet('"+local+"') WHERE observation_id>=? AND timestamp_utc<=? ORDER BY observation_id", [int(oid0), mon14]).fetchall()
                if len(fwd)<10: continue
                def sim(side):
                    # side=+1 long, -1 short; entree executable au premier tick
                    entry = float(fwd[0][2]) if side>0 else float(fwd[0][1])
                    for (tt, bb, aa, mm) in fwd[1:]:
                        mm=float(mm)
                        if side>0:
                            if mm>=fri_mid and side*(mid_sun-fri_mid)<0: pass
                            hit_target = (mm>=fri_mid) if (fri_mid>mid_sun) else (mm<=fri_mid)
                            adverse = (mid_sun-mm)/mid_sun*10000 >= abs(gap_bp) if side<0 else (mm-mid_sun)/mid_sun*10000 >= abs(gap_bp)
                        else:
                            hit_target = (mm<=fri_mid) if (fri_mid<mid_sun) else (mm>=fri_mid)
                            adverse = (mm-mid_sun)/mid_sun*10000 >= abs(gap_bp)
                        if side>0:
                            stop = (mid_sun-mm)/mid_sun*10000 >= abs(gap_bp)
                            tgt = mm>=fri_mid if fri_mid>mid_sun else mm<=fri_mid
                        else:
                            stop = (mm-mid_sun)/mid_sun*10000 >= abs(gap_bp)
                            tgt = mm<=fri_mid if fri_mid<mid_sun else mm>=fri_mid
                        if tgt: return ((float(bb)-entry)/entry*10000 if side>0 else (entry-float(aa))/entry*10000), 'fill'
                        if stop: return ((float(bb)-entry)/entry*10000 if side>0 else (entry-float(aa))/entry*10000), 'stop'
                    tt, bb, aa, mm = fwd[-1]
                    return ((float(bb)-entry)/entry*10000 if side>0 else (entry-float(aa))/entry*10000), 'deadline'
                fade_side = -1 if gap_bp>0 else 1
                rf, rs = sim(fade_side); rb, rsb = sim(-fade_side)
                with open(OUT,'a') as fh: fh.write(f"{p['name']},GAP,{t0},{gap_bp:.3f},{sp0:.3f},{rf:.4f},{rb:.4f},{rs},{len(fwd)}\n")
            for r in con.execute(JUMPQ.format(f=local)).fetchall():
                with open(OUTJ,'a') as fh: fh.write(p['name']+',JUMP,'+str(r[0])+','+','.join('' if v is None else str(float(v)) for v in r[1:])+'\n')
            if local.startswith('/tmp/part_'): os.remove(local)
            state['done'].append(p['name'])
            if len(state['done'])%40==0: checkpoint(state)
            print('POST', p['name'], flush=True)
        shutil.rmtree('/tmp/kbatch', ignore_errors=True)
    checkpoint(state); print('F13 termine:', len(state['done']))
if __name__=='__main__': main()
