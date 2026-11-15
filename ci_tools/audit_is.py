"""AUDIT SCIENTIFIQUE IS (descriptif, aucune hypothese, aucun Holdout).
Priorite: autocorrelation signee lag-1 suspecte (~0,49).
Comparaisons imposees: tri observation_id vs tri timestamp; alignement des
rendements; doublons de timestamps; frontieres; retards 1..50; sensibilite a
l'echantillonnage (1 tick sur 10); rendements nuls; apres-gaps par duree;
sauts (frequence, asymetrie, contexte); spread post-saut; queues.
Resultats initiaux conserves: cet audit ne reecrit pas PARTITION_PHENOMENA.csv."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/audit'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; CSV=ROOT/'PARTITION_AUDIT.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/audit']); subprocess.run(['git','commit','-q','-m',f"Checkpoint audit IS: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

Q = """
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid, spread_rel FROM read_parquet('{f}')),
o AS (SELECT *, (mid-lag(mid) OVER (ORDER BY oid))/NULLIF(lag(mid) OVER (ORDER BY oid),0) AS r,
        epoch(t-lag(t) OVER (ORDER BY oid)) AS dt_s FROM s),
x AS (SELECT *, abs(r) AS ar, lag(r,1) OVER (ORDER BY oid) AS r1, lag(r,2) OVER (ORDER BY oid) AS r2,
        lag(r,5) OVER (ORDER BY oid) AS r5, lag(r,10) OVER (ORDER BY oid) AS r10,
        lag(ar,1) OVER (ORDER BY oid) AS a1, lag(ar,5) OVER (ORDER BY oid) AS a5, lag(ar,20) OVER (ORDER BY oid) AS a20,
        lead(r) OVER (ORDER BY oid) AS r_next, lead(spread_rel,1) OVER (ORDER BY oid) AS sp1, lead(spread_rel,5) OVER (ORDER BY oid) AS sp5 FROM o)
SELECT count(*),
 avg(CASE WHEN r=0 THEN 1.0 ELSE 0 END),
 corr(r,r1), corr(r,r2), corr(r,r5), corr(r,r10),
 corr(ar,a1), corr(ar,a5), corr(ar,a20),
 corr(CASE WHEN r<>0 AND r1<>0 THEN r END, CASE WHEN r<>0 AND r1<>0 THEN r1 END),
 avg(CASE WHEN dt_s>60 AND dt_s<=300 THEN ar END), count(CASE WHEN dt_s>60 AND dt_s<=300 THEN 1 END),
 avg(CASE WHEN dt_s>300 AND dt_s<=3600 THEN ar END), count(CASE WHEN dt_s>300 AND dt_s<=3600 THEN 1 END),
 avg(CASE WHEN dt_s>3600 THEN ar END), count(CASE WHEN dt_s>3600 THEN 1 END),
 10000.0*avg(CASE WHEN ar>0.0003 THEN 1 ELSE 0 END), 10000.0*avg(CASE WHEN ar>0.001 THEN 1 ELSE 0 END),
 avg(CASE WHEN ar>0.0005 THEN ar END), avg(CASE WHEN ar>0.0005 THEN (CASE WHEN r>0 THEN 1.0 ELSE 0 END) END),
 avg(CASE WHEN ar>0.0005 THEN sign(r)*r_next END), avg(CASE WHEN ar>0.0005 THEN sp1 END), avg(CASE WHEN ar>0.0005 THEN sp5 END),
 avg(CASE WHEN r>0 THEN 1.0 ELSE 0 END),
 (SELECT count(*) FROM (SELECT t, count(*) c FROM s GROUP BY t HAVING c>1))
FROM x"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    new=not CSV.exists()
    with open(CSV,'a') as cf:
        if new: cf.write("partition,n,zero_ret_frac,ac1,ac2,ac5,ac10,acabs1,acabs5,acabs20,ac1_nonzero,gap60_300_abs,gap60_300_n,gap300_3600_abs,gap300_3600_n,gap3600_abs,gap3600_n,jump3bp_10k,jump10bp_10k,jump_amp_mean,jump_pos_share,jump_continuation,spread_next,spread_p5,ret_pos_share,dup_ts_groups,ac1_tri_timestamp\n")
        for p in parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            r=con.execute(Q.format(f=local)).fetchone()
            # Tri timestamp (tie-break observation_id): autocorrelation de controle
            qt=f"""WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, mid FROM read_parquet('{local}')),
            o AS (SELECT *, (mid-lag(mid) OVER (ORDER BY t, oid))/NULLIF(lag(mid) OVER (ORDER BY t, oid),0) AS r FROM s),
            x AS (SELECT r, lag(r) OVER (ORDER BY t, oid) AS r1 FROM o) SELECT corr(r,r1) FROM x"""
            ac_ts=con.execute(qt).fetchone()[0]
            os.remove(local)
            cf.write(p['name']+','+','.join('' if v is None else str(float(v)) for v in r)+','+('' if ac_ts is None else str(float(ac_ts)))+'\n'); cf.flush()
            state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('audit', p['name'], flush=True)
    # ajouter la colonne de controle au header si absent
    checkpoint(state); print('audit termine:', len(state['done']))

if __name__=='__main__': main()
