"""P3-001 PREENREGISTRE (TRIAL_LEDGER.md) - exploration conditionnelle, IS SEUL.
Origines echantillonnees (observation_id % 500 = 0). Features certifiees au temps t
(causales), labels RET_H via ASOF premier tick >= t+H (RET_H_ALIGN_V1).
Deux passes: A seuils de quintiles globaux IS; B agregats par quintile.
Aucun acces OOS/Holdout: seules les partitions entierement dans l'IS sont lues.
Resultats bruts conserves quels qu'ils soient. Checkpoint Git periodique."""
import json, sys, pathlib, subprocess, os, time
import duckdb

ROOT = pathlib.Path('reports/meta_alpha/p3'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT/'STATE.json'
CERT_START, CERT_END = "2010-01-04 00:01:10.457", "2026-09-30 23:59:58.864"
import datetime as _dt
_s=_dt.datetime.fromisoformat(CERT_START); _e=_dt.datetime.fromisoformat(CERT_END)
IS_END = _s + 0.6*(_e-_s)   # split calendaire 60/20/20 gele par le certificat
print('IS_END gele =', IS_END.isoformat(), flush=True)

def dl(fid, local, name):
    for _try in range(3):
        if subprocess.run(['gdown','-q','--output',local,fid]).returncode==0: return
        time.sleep(30*(_try+1))
    import requests as rq
    exp={x['name']:x['file_bytes'] for x in json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']}
    url=f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'
    for _try in range(3):
        try:
            with rq.get(url, stream=True, timeout=120, headers={'User-Agent':'Mozilla/5.0'}) as r:
                r.raise_for_status()
                with open(local,'wb') as f:
                    for ch in r.iter_content(1<<20): f.write(ch)
            if open(local,'rb').read(4)==b'PAR1' and pathlib.Path(local).stat().st_size==exp[name]: return
        except Exception: pass
        time.sleep(60*(_try+1))
    raise RuntimeError(f'telechargement impossible: {name}')

def checkpoint(state):
    STATE_P.write_text(json.dumps(state, indent=1))
    if pathlib.Path('.git').exists():
        subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git','add','reports/meta_alpha/p3']); subprocess.run(['git','commit','-q','-m',f"Checkpoint P3-001: passe {state['pass']} {len(state['done'])}/348"])
        subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

FEATS = """
WITH s AS (SELECT observation_id, timestamp_utc AS t, mid, spread_rel FROM read_parquet('{f}')),
e AS (SELECT *, (mid - lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS ret_mid,
        epoch(t - lag(t,100) OVER w)/100.0 AS interarrival_100
      FROM s WINDOW w AS (ORDER BY observation_id)),
f AS (SELECT *,
        stddev_samp(ret_mid) OVER (ORDER BY observation_id ROWS BETWEEN 100 PRECEDING AND 1 PRECEDING) AS roll_std_100,
        (max(mid) OVER (ORDER BY observation_id ROWS BETWEEN 99 PRECEDING AND CURRENT ROW)
        -min(mid) OVER (ORDER BY observation_id ROWS BETWEEN 99 PRECEDING AND CURRENT ROW))/NULLIF(mid,0) AS roll_range_100,
        count(*) OVER (ORDER BY t RANGE BETWEEN INTERVAL 30 SECOND PRECEDING AND CURRENT ROW) AS intensity_30s
      FROM e)
SELECT observation_id, t, mid, spread_rel, roll_std_100, roll_range_100, interarrival_100, intensity_30s FROM f"""

def main():
    inv = json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    is_parts = [p for p in inv['partitions'] if p['timestamp_max_footer'] and _dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None) <= IS_END]
    print(f'partitions IS (entieres): {len(is_parts)}', flush=True)
    state = json.loads(STATE_P.read_text()) if STATE_P.exists() else {'pass':'A','done':[],'thresholds':{},'buckets':{}}
    con = duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    # PASSE A: seuils quintiles sur origines tres echantillonnees (%5000)
    if state['pass']=='A':
        vals = {'spread_rel':[],'roll_std_100':[],'roll_range_100':[],'interarrival_100':[],'intensity_30s':[]}
        for p in is_parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            q = FEATS.format(f=local) + " WHERE observation_id % 5000 = 0 AND roll_std_100 IS NOT NULL"
            for row in con.execute(q).fetchall():
                for k,v in zip(vals, row[3:8]):
                    if v is not None: vals[k].append(float(v))
            os.remove(local); state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('A', p['name'], flush=True)
        import statistics
        th={}
        for k,v in vals.items():
            v=sorted(v); n=len(v)
            th[k]={'n':n,'q20':v[n//5],'q40':v[2*n//5],'q60':v[3*n//5],'q80':v[4*n//5]}
        state['thresholds']=th; state['pass']='B'; state['done']=[]; checkpoint(state)
        print('seuils:', json.dumps(th), flush=True)
    # PASSE B: agregats par quintile x horizon
    if state['pass']=='B':
        th=state['thresholds']
        def bucket(k, v):
            t=th[k]; return 0 if v<t['q20'] else 1 if v<t['q40'] else 2 if v<t['q60'] else 3 if v<t['q80'] else 4
        agg = state['buckets']
        for p in is_parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            base = FEATS.format(f=local)
            q = f"""WITH f AS ({base}), o AS (SELECT * FROM f WHERE observation_id % 500 = 0 AND roll_std_100 IS NOT NULL)
            SELECT o.observation_id, o.spread_rel, o.roll_std_100, o.roll_range_100, o.interarrival_100, o.intensity_30s,
              a.mid/o.mid-1 AS ret_5m, b.mid/o.mid-1 AS ret_15m, c.mid/o.mid-1 AS ret_1h
            FROM o
            ASOF LEFT JOIN (SELECT timestamp_utc AS t, mid FROM read_parquet('{local}')) a ON o.t + INTERVAL 5 MINUTE <= a.t
            ASOF LEFT JOIN (SELECT timestamp_utc AS t, mid FROM read_parquet('{local}')) b ON o.t + INTERVAL 15 MINUTE <= b.t
            ASOF LEFT JOIN (SELECT timestamp_utc AS t, mid FROM read_parquet('{local}')) c ON o.t + INTERVAL 1 HOUR <= c.t"""
            for row in con.execute(q).fetchall():
                feats={'spread_rel':row[1],'roll_std_100':row[2],'roll_range_100':row[3],'interarrival_100':row[4],'intensity_30s':row[5]}
                labels={'ret_5m':row[6],'ret_15m':row[7],'ret_1h':row[8]}
                for fk,fv in feats.items():
                    if fv is None: continue
                    bk=bucket(fk,float(fv))
                    for hk,hv in labels.items():
                        if hv is None: continue
                        key=f"{fk}|Q{bk+1}|{hk}"; a=agg.setdefault(key,[0,0.0,0.0]); a[0]+=1; a[1]+=float(hv); a[2]+=float(hv)**2
            os.remove(local); state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('B', p['name'], flush=True)
        state['pass']='DONE'; checkpoint(state)
    # Rapport brut
    agg=state['buckets']; out={'trial':'P3-001','is_end':IS_END.isoformat(),'partitions_is':len(is_parts),
      'thresholds':state['thresholds'],'buckets':{}}
    for k,(n,s,s2) in sorted(agg.items()):
        m=s/n; var=(s2/n-m*m) if n>1 else 0.0
        out['buckets'][k]={'n':n,'mean_ret':m,'sd_ret':var**0.5}
    (ROOT/'P3_001_RESULTS.json').write_text(json.dumps(out,indent=1))
    print('P3-001 termine:', len(out['buckets']), 'cellules')

if __name__=='__main__': main()
