"""P4-001 PREENREGISTRE (TRIAL_LEDGER.md). Candidat H-P3-A teste, pas optimise.
Regle: ROLL_STD_100 dans le quintile superieur CAUSAL (seuils walk-forward expansifs,
recalcules par partition a partir des seules partitions precedentes; warm-up sans
signal tant que l'historique causal < 20000 valeurs echantillonnees).
Entree longue au ASK du tick origine, sortie au BID du premier tick >= t+H
(15 min, 1 h, series separees), origines NON chevauchantes (espacement >= H).
Rendement = bid_sortie/ask_entree - 1 = net du spread Bid/Ask observe, AVANT couts
inconnus (slippage/commission INCONNUS -> classement CONDITIONAL, jamais NET).
Origines: observation_id % 500 = 0. Purge: origines a moins de 1 h des frontieres
IS/OOS et OOS/fin exclues. Holdout JAMAIS lu: seules les partitions entierement
avant la fin OOS sont telechargees. Checkpoint Git periodique, reprise par etat."""
import json, pathlib, subprocess, os, time, datetime as dt
import duckdb

ROOT = pathlib.Path('reports/meta_alpha/p4'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P = ROOT/'STATE.json'; TRADES = ROOT/'trades.csv'
_s=dt.datetime.fromisoformat("2010-01-04 00:01:10.457"); _e=dt.datetime.fromisoformat("2026-09-30 23:59:58.864")
IS_END=_s+0.6*(_e-_s); OOS_END=_s+0.8*(_e-_s)
print('IS_END',IS_END.isoformat(),'OOS_END',OOS_END.isoformat(), flush=True)

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
        subprocess.run(['git','add','reports/meta_alpha/p4']); subprocess.run(['git','commit','-q','-m',f"Checkpoint P4-001: {len(state['done'])}/348 partitions"])
        subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])

FEATS = """
WITH s AS (SELECT observation_id, timestamp_utc AS t, bid, ask, mid FROM read_parquet('{f}')),
e AS (SELECT *, (mid - lag(mid) OVER w)/NULLIF(lag(mid) OVER w,0) AS ret_mid FROM s WINDOW w AS (ORDER BY observation_id)),
f AS (SELECT *, stddev_samp(ret_mid) OVER (ORDER BY observation_id ROWS BETWEEN 100 PRECEDING AND 1 PRECEDING) AS roll_std_100 FROM e)
SELECT observation_id, t, bid, ask, mid, roll_std_100 FROM f"""

def main():
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))
    parts=[p for p in inv['partitions'] if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None) <= OOS_END]
    print(f'partitions traitees (IS+OOS, Holdout exclu): {len(parts)}; derniere={parts[-1]["name"]}', flush=True)
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'done':[],'hist':[],'last15':None,'last1h':None}
    con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=2")
    new_trades = not TRADES.exists()
    with open(TRADES,'a') as tf:
        if new_trades: tf.write("segment,horizon,entry_ts,ret_net_spread,ret_mid\n")
        for p in parts:
            if p['name'] in state['done']: continue
            local=f"/tmp/{p['name']}"; dl(p['drive_id'], local, p['name'])
            hist=sorted(state['hist']); q80=None
            if len(hist)>=20000: q80=hist[int(0.8*len(hist))]
            if q80 is not None:
                q=f"""WITH f AS ({FEATS.format(f=local)}), o AS (SELECT * FROM f WHERE observation_id % 500 = 0 AND roll_std_100 >= {q80})
                SELECT o.t, o.ask, o.mid, a.bid, a.mid, b.bid, b.mid FROM o
                ASOF LEFT JOIN (SELECT timestamp_utc AS t, bid, mid FROM read_parquet('{local}')) a ON o.t + INTERVAL 15 MINUTE <= a.t
                ASOF LEFT JOIN (SELECT timestamp_utc AS t, bid, mid FROM read_parquet('{local}')) b ON o.t + INTERVAL 1 HOUR <= b.t
                ORDER BY o.t"""
                for t,ask,mid,bid15,mid15,bid1,mid1 in con.execute(q).fetchall():
                    seg = 'IS' if t.replace(tzinfo=None) < IS_END - dt.timedelta(hours=1) else ('OOS' if IS_END <= t.replace(tzinfo=None) <= OOS_END - dt.timedelta(hours=1) else None)
                    if seg is None: continue
                    for hz,bidx,midx,lastk in (('15m',bid15,mid15,'last15'),('1h',bid1,mid1,'last1h')):
                        if bidx is None: continue
                        H=dt.timedelta(minutes=15) if hz=='15m' else dt.timedelta(hours=1)
                        last = dt.datetime.fromisoformat(state[lastk]) if state[lastk] else None
                        if last is not None and t.replace(tzinfo=None) < last + H: continue
                        state[lastk]=t.replace(tzinfo=None).isoformat()
                        tf.write(f"{seg},{hz},{t.isoformat()},{float(bidx)/float(ask)-1:.10f},{float(midx)/float(mid)-1:.10f}\n")
                tf.flush()
            # mise a jour causale de l'historique APRES traitement de la partition
            q2=FEATS.format(f=local)+" WHERE observation_id % 5000 = 0 AND roll_std_100 IS NOT NULL"
            state['hist'].extend(float(r[5]) for r in con.execute(q2).fetchall())
            os.remove(local); state['done'].append(p['name'])
            if len(state['done'])%20==0: checkpoint(state)
            print('fait', p['name'], 'hist', len(state['hist']), 'q80 actif' if q80 else 'warm-up', flush=True)
    checkpoint(state)
    (ROOT/'P4_001_STATE_FINAL.json').write_text(json.dumps({'is_end':IS_END.isoformat(),'oos_end':OOS_END.isoformat(),'partitions':len(parts),'hist_n':len(state['hist'])}))
    print('P4-001 collecte terminee')

if __name__=='__main__': main()
