"""Phase 2 autonome - L2 integrite / L3 derivation / L4 mesure, par lot de partitions.
Telecharge chaque partition (gdown), calcule en DuckDB borne, ecrit des agregats.
Ne stocke jamais les Parquet. Reprise par etat (partitions deja faites ignorees)."""
import json, sys, pathlib, subprocess, os
import duckdb

START, END = int(sys.argv[1]), int(sys.argv[2])
import traceback
_err = pathlib.Path('reports/meta_alpha/phase2'); _err.mkdir(parents=True, exist_ok=True)
def _hook(exc_type, exc, tb):
    pathlib.Path('reports/meta_alpha/phase2/ERROR.txt').write_text(''.join(traceback.format_exception(exc_type, exc, tb)))
    raise exc
sys.excepthook = _hook
inv = json.load(open('reports/meta_alpha/INVENTORY_348.json'))
by_name = {p['name']: p for p in inv['partitions']}
# la 000184 a ete re-sondee a part: son identifiant est connu
by_name['part_000184.parquet'] = {'name':'part_000184.parquet','drive_id':'11TKJcp1Aj7n0kQY_bUBJb2yfPVq5ROdp','rows':48227}
outdir = pathlib.Path('reports/meta_alpha/phase2'); outdir.mkdir(parents=True, exist_ok=True)
state_path = outdir/'STATE.json'
state = json.loads(state_path.read_text()) if state_path.exists() else {'done':{}}
csv_path = outdir/'PARTITION_MEASURES.csv'
new_csv = not csv_path.exists()
con = duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
with open(csv_path,'a') as csv:
    if new_csv:
        csv.write("partition,rows,min_ts,max_ts,ts_regressions,dup_timestamps,invalid_quotes,max_mid_diff,max_spread_diff,gaps_gt_60s,max_gap_s,mean_spread_rel,p50_spread_rel,p95_spread_rel,mean_ret_tick,std_ret_tick\n")
    for i in range(START, END+1):
        name = f'part_{i:06d}.parquet'
        if name in state['done']: print('skip', name); continue
        fid = by_name[name]['drive_id']
        local = f'/tmp/{name}'
        for _try in range(4):
            r=subprocess.run(['gdown','-q','--output',local,fid])
            if r.returncode==0: break
            import time as _t; _t.sleep(15*(_try+1))
        else: raise RuntimeError(f'telechargement impossible apres 4 essais: {name}')
        q = f"""
        WITH s AS (SELECT * FROM read_parquet('{local}') ORDER BY observation_id),
        d AS (SELECT *, lag(timestamp_utc) OVER (ORDER BY observation_id) AS pts,
                     lag(mid) OVER (ORDER BY observation_id) AS pmid FROM s)
        SELECT count(*), min(timestamp_utc), max(timestamp_utc),
          sum(CASE WHEN pts IS NOT NULL AND timestamp_utc < pts THEN 1 ELSE 0 END),
          sum(CASE WHEN pts IS NOT NULL AND timestamp_utc = pts THEN 1 ELSE 0 END),
          sum(CASE WHEN bid <= 0 OR ask < bid THEN 1 ELSE 0 END),
          max(abs(mid - (bid+ask)/2.0)), max(abs(spread_abs - (ask-bid))),
          sum(CASE WHEN pts IS NOT NULL AND epoch(timestamp_utc-pts) > 60 THEN 1 ELSE 0 END),
          max(epoch(timestamp_utc-pts)),
          avg(spread_rel), approx_quantile(spread_rel,0.5), approx_quantile(spread_rel,0.95),
          avg(CASE WHEN pmid IS NOT NULL AND pmid<>0 THEN mid/pmid-1 END),
          stddev_samp(CASE WHEN pmid IS NOT NULL AND pmid<>0 THEN mid/pmid-1 END)
        FROM d"""
        r = con.execute(q).fetchone(); os.remove(local)
        vals=[name]+[('' if v is None else str(v)) for v in r]
        csv.write(','.join(vals)+'\n'); csv.flush()
        state['done'][name]={'rows': int(r[0])}
        # Checkpoint GitHub periodique: le travail survit a toute coupure.
        if len(state['done']) % 20 == 0 and pathlib.Path('.git').exists():
            subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
            subprocess.run(['git','add','reports/meta_alpha/phase2'])
            subprocess.run(['git','commit','-q','-m',f"Checkpoint automatique Phase 2: {len(state['done'])}/348 partitions mesurees"])
            subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
        state_path.write_text(json.dumps(state, indent=1))
        print(name, 'rows', r[0], 'regressions', r[3], 'invalid', r[5], flush=True)
print('batch termine')
