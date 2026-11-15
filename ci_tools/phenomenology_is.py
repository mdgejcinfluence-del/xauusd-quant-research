"""EXTRACTION PHENOMENOLOGIQUE IS (directive: registre != decouverte).
Mesures DESCRIPTIVES uniquement sur les 282 partitions IS: distributions du spread,
rendements tick, sauts, rythme, autocorrelations, dynamique autour des trous,
relations conditionnelles spread/volatilite/activite. Aucune hypothese, aucun label
futur exploite comme signal: les ecarts apres trou sont decrits, pas testes.
Checkpoint Git periodique, reprise par etat."""
import json, pathlib, subprocess, os, time, datetime as dt
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phenomenology'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; CSV=ROOT/'PARTITION_PHENOMENA.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phenomenology']); subprocess.run(['git','commit','-q','-m',f"Checkpoint phenomenologie IS: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    new=not CSV.exists()
    with open(CSV,'a') as cf:
        if new: cf.write("partition,n,spread_p1,spread_p25,spread_p50,spread_p75,spread_p99,ret_std,ret_skew,ret_kurt,autocorr_lag1,autocorr_abs_lag1,jump_5bp_per_10k,gaps60,absret_after_gap,absret_normal,spread_after_jump,spread_normal,interarr_p50,interarr_p95\n")
        for p in parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            q=f"""
            WITH s AS (SELECT timestamp_utc AS t, mid, spread_rel FROM read_parquet('{local}') ORDER BY observation_id),
            e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r,
                        epoch(t-lag(t) OVER w) AS dt_s FROM s WINDOW w AS (ORDER BY t)),
            j AS (SELECT *, lag(r) OVER (ORDER BY t) AS r_prev, abs(r) AS ar FROM e)
            SELECT count(*),
              approx_quantile(spread_rel,0.01), approx_quantile(spread_rel,0.25), approx_quantile(spread_rel,0.5), approx_quantile(spread_rel,0.75), approx_quantile(spread_rel,0.99),
              stddev_samp(r), skewness(r), kurtosis(r),
              corr(r, r_prev), corr(ar, lag(ar) OVER (ORDER BY t)),
              10000.0*avg(CASE WHEN ar>0.0005 THEN 1 ELSE 0 END),
              sum(CASE WHEN dt_s>60 THEN 1 ELSE 0 END),
              avg(CASE WHEN dt_s>60 THEN ar END), avg(CASE WHEN dt_s<=60 THEN ar END),
              avg(CASE WHEN r_prev IS NOT NULL AND abs(r_prev)>0.0005 THEN spread_rel END),
              avg(CASE WHEN r_prev IS NOT NULL AND abs(r_prev)<=0.0005 THEN spread_rel END),
              approx_quantile(dt_s,0.5), approx_quantile(dt_s,0.95)
            FROM j"""
            r=con.execute(q).fetchone(); os.remove(local)
            cf.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n'); cf.flush()
            state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('phenomenes', p['name'], flush=True)
    checkpoint(state); print('extraction terminee:', len(state['done']))

if __name__=='__main__': main()
