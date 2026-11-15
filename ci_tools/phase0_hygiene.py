"""PHASE 0 - hygiene du corpus, LECTURE SEULE, perimetre IS (282 partitions).
Aucune donnee Holdout lue par ce script. Descriptif uniquement:
quotes croisees/verrouillees/invalides, spreads aberrants, doublons d'horodatage,
resolution des prix et du temps, liste exhaustive des gaps > 60 s (classification
faite ensuite: intraday vs fermetures calendaires). Resultats initiaux conserves."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase0'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; AGG=ROOT/'PARTITION_HYGIENE.csv'; GAPS=ROOT/'GAPS_IS.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase0']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Phase 0 hygiene: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not AGG.exists(): AGG.write_text("partition,n,crossed,locked,nonpositive,spread_rel_max,spread_rel_p999,min_pos_dmid,dup_ts_events\n")
    if not GAPS.exists(): GAPS.write_text("partition,gap_start,gap_end,dur_s\n")
    if True:
        af=open(AGG,'a'); gf=open(GAPS,'a'); af.close(); gf.close()
        for p in parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            q=f"""
            WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{local}')),
            e AS (SELECT *, mid-lag(mid) OVER (ORDER BY oid) AS dm, epoch(t-lag(t) OVER (ORDER BY oid)) AS dt_s, lag(t) OVER (ORDER BY oid) AS t_prev FROM s)
            SELECT count(*), sum(CASE WHEN ask<bid THEN 1 ELSE 0 END), sum(CASE WHEN ask=bid THEN 1 ELSE 0 END),
              sum(CASE WHEN bid<=0 OR ask<=0 THEN 1 ELSE 0 END), max(spread_rel), approx_quantile(spread_rel,0.999),
              min(CASE WHEN dm>0 THEN dm END),
              (SELECT coalesce(sum(c-1),0) FROM (SELECT t, count(*) c FROM s GROUP BY t HAVING c>1))
            FROM e"""
            r=con.execute(q).fetchone()
            with open(AGG,'a') as af: af.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            qg=f"""
            WITH s AS (SELECT timestamp_utc AS t, epoch(timestamp_utc - lag(timestamp_utc) OVER (ORDER BY observation_id)) AS d, lag(timestamp_utc) OVER (ORDER BY observation_id) AS tp FROM read_parquet('{local}'))
            SELECT tp, t, d FROM s WHERE d>60 ORDER BY t"""
            with open(GAPS,'a') as gf:
                for a,b,d in con.execute(qg).fetchall():
                    gf.write(f"{p['name']},{a},{b},{float(d)}\n")
            os.remove(local); state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('phase0', p['name'], flush=True)
    checkpoint(state); print('phase 0 terminee:', len(state['done']))

if __name__=='__main__': main()
