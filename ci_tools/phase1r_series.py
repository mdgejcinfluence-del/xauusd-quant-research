"""PHASE 1R tache 1 — series descriptives granulees causales, IS seul, lecture seule.
Pre-enregistrement: phase1r/PHASE_1R_PREREG.json (verrouille par chaine).
Granularites: G_EVT100 (100 evenements), G_ACT500 (500 maj), G_VOL10bp (budget
cumulatif |r| de 10 bp par barre, decoupage par somme cumulee). Aucune barre ne
franchit un gap > 60 s (segmentation par gap). Aucune interpolation, aucun OHLC."""
import json, pathlib, subprocess, os, time, datetime as dt, traceback, sys
import duckdb
ROOT=pathlib.Path('reports/meta_alpha/phase1r'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'; PG=ROOT/'PARTITION_GRANULARITY.csv'; MO=ROOT/'MONTHLY_SERIES.csv'
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
        subprocess.run(['git','add','reports/meta_alpha/phase1r']); subprocess.run(['git','commit','-q','-m',f"Checkpoint Phase 1R series: {len(state['done'])}/282"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

BARS = """
WITH s AS (SELECT observation_id AS oid, timestamp_utc AS t, bid, ask, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, (mid-lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS r, epoch(t-lag(t) OVER w) AS dt_s,
        bid-lag(bid) OVER w AS db, ask-lag(ask) OVER w AS da FROM s WINDOW w AS (ORDER BY oid)),
g0 AS (SELECT *, sum(CASE WHEN dt_s>60 THEN 1 ELSE 0 END) OVER (ORDER BY oid) AS seg FROM e),
g AS (SELECT *, row_number() OVER (PARTITION BY seg ORDER BY oid) AS rn,
        sum(abs(r)) OVER (PARTITION BY seg ORDER BY oid ROWS UNBOUNDED PRECEDING) AS cumabs FROM g0),
b AS (SELECT seg, {barkey} AS bk, min(t) AS t0, max(t) AS t1, count(*) AS n,
        arg_min(mid, oid) AS m0, arg_max(mid, oid) AS m1, sqrt(sum(coalesce(r*r,0))) AS vol,
        avg(spread_rel) AS spread, avg(CASE WHEN db<>0 AND da=0 THEN 1.0 WHEN db IS NULL THEN NULL ELSE 0 END) AS sh_bonly,
        avg(CASE WHEN da<>0 AND db=0 THEN 1.0 WHEN da IS NULL THEN NULL ELSE 0 END) AS sh_aonly
      FROM g GROUP BY seg, bk)
SELECT t0, t1, n, epoch(t1-t0) AS dur, m1/m0-1 AS bret, vol, spread, sh_bonly, sh_aonly FROM b ORDER BY t0"""

def barkey(kind):
    return {'G_EVT100':'(rn-1)//100','G_ACT500':'(rn-1)//500','G_VOL10bp':'floor(coalesce(cumabs,0)/0.001)'}[kind]

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[]}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    if not PG.exists(): PG.write_text("partition,granularity,bars,ret_p1,ret_p25,ret_p50,ret_p75,ret_p99,vol_p50,vol_p95,spread_mean,intensity_mean,share_bonly,share_aonly,ac1_barret\n")
    if not MO.exists(): MO.write_text("month,granularity,bars,ret_mean,vol_mean,spread_mean,intensity_mean\n")
    for p in parts:
        if p['name'] in state['done']: continue
        local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
        for kind in ('G_EVT100','G_ACT500','G_VOL10bp'):
            q=BARS.format(f=local, barkey=barkey(kind))
            qq=f"""WITH bars AS ({q}), x AS (SELECT *, lag(bret) OVER (ORDER BY t0) AS bret1 FROM bars)
            SELECT count(*), approx_quantile(bret,0.01), approx_quantile(bret,0.25), approx_quantile(bret,0.5), approx_quantile(bret,0.75), approx_quantile(bret,0.99),
              approx_quantile(vol,0.5), approx_quantile(vol,0.95), avg(spread), avg(CASE WHEN dur>0 THEN n/dur END), avg(sh_bonly), avg(sh_aonly), corr(bret,bret1) FROM x"""
            r=con.execute(qq).fetchone()
            with open(PG,'a') as f: f.write(p['name']+','+kind+','+','.join('' if v is None else str(float(v)) for v in r)+'\n')
            qm=f"""WITH bars AS ({q}) SELECT strftime(t0,'%Y-%m'), count(*), avg(bret), avg(vol), avg(spread), avg(CASE WHEN dur>0 THEN n/dur END) FROM bars GROUP BY 1 ORDER BY 1"""
            with open(MO,'a') as f:
                for row in con.execute(qm).fetchall(): f.write(f"{row[0]},{kind},"+','.join('' if v is None else str(float(v)) for v in row[1:])+'\n')
        os.remove(local); state['done'].append(p['name'])
        if len(state['done'])%20==0: checkpoint(state)
        print('1R', p['name'], flush=True)
    checkpoint(state); print('series terminees:', len(state['done']))

if __name__=='__main__': main()
