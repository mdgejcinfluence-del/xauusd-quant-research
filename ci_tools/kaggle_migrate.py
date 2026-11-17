"""Migration Drive -> Kaggle par lot (CI). Etat: kaggle_migration/STATE.json."""
import json, pathlib, subprocess, os, time, datetime as dt, hashlib, sys, traceback
ROOT=pathlib.Path('reports/meta_alpha/kaggle_migration'); ROOT.mkdir(parents=True, exist_ok=True)
STATE_P=ROOT/'STATE.json'
def _hook(a,b,c):
    (ROOT/'ERROR.txt').write_text(''.join(traceback.format_exception(a,b,c))); raise b
sys.excepthook=_hook
IS_END=dt.datetime(2020,1,20,9,36,27)
MISSING=[f'part_{i:06d}.parquet' for i in [269,270,271]+list(range(273,283))]
def dl(fid, local, name, exp_size):
    import requests as rq
    for _t in range(2):
        if subprocess.run(['gdown','-q','--output',local,fid]).returncode==0 and pathlib.Path(local).exists() and pathlib.Path(local).stat().st_size==exp_size and open(local,'rb').read(4)==b'PAR1': return True
        time.sleep(20*(_t+1))
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
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda: f.read(1<<22), b''): h.update(ch)
    return h.hexdigest()
def checkpoint(state):
    STATE_P.write_text(json.dumps(state,indent=1))
    if pathlib.Path('.git').exists():
        subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
        subprocess.run(['git','add','reports/meta_alpha/kaggle_migration']); subprocess.run(['git','commit','-q','-m',f"Kaggle migration: {state.get('last_batch','?')}"])
        subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
def main():
    state=json.loads(STATE_P.read_text()) if STATE_P.exists() else {'uploaded':{},'batches':{}}
    print('KAGGLE_USERNAME present:', bool(os.environ.get('KAGGLE_USERNAME')), '| KAGGLE_KEY present:', bool(os.environ.get('KAGGLE_KEY')), flush=True)
    from kaggle.api.kaggle_api_extended import KaggleApi
    api=KaggleApi(); api.authenticate(); print('Kaggle auth OK:', api.config_values.get('username'), flush=True)
    inv=json.load(open('reports/meta_alpha/INVENTORY_348_EXHAUSTIVE.json'))['partitions']
    is_parts=[p for p in inv if p['timestamp_max_footer'] and dt.datetime.fromisoformat(p['timestamp_max_footer'].replace('Z','+00:00')).replace(tzinfo=None)<=IS_END]
    byname={p['name']:p for p in is_parts}
    done=set(state['uploaded'])
    if not set(MISSING)<=done:
        batch_name='xauusd-is-missing13'; targets=[m for m in MISSING if m not in done]
    else:
        rest=[p['name'] for p in is_parts if p['name'] not in done]
        if not rest: print('MIGRATION COMPLETE: 282/282 deja uploadees'); return
        idx=len([b for b in state['batches'] if b.startswith('xauusd-is-b')])+1
        batch_name=f'xauusd-is-b{idx:02d}'; targets=rest[:40]
    print('lot:', batch_name, 'fichiers vises:', len(targets), flush=True)
    folder=pathlib.Path('/tmp/kaggle_upload'); folder.mkdir(exist_ok=True)
    ok=[]; failed=[]
    for name in targets:
        p=byname[name]; local=str(folder/name)
        if dl(p['drive_id'], local, name, p['file_bytes']):
            ok.append({'name':name,'bytes':p['file_bytes'],'sha256':sha(local)}); print('DL OK', name, flush=True)
        else:
            failed.append(name); print('DL ECHEC', name, flush=True)
            if pathlib.Path(local).exists(): os.remove(local)
    state.setdefault('attempts',[]).append({'batch':batch_name,'ok':[o['name'] for o in ok],'failed':failed,'when':dt.datetime.utcnow().isoformat()})
    if failed:
        state['last_batch']=batch_name+' (INCOMPLET, upload differe)'; checkpoint(state); print('lot incomplet: upload differe pour ne pas creer de dataset partiel'); return
    username=api.config_values.get('username')
    meta={'title':batch_name,'id':f'{username}/{batch_name}','licenses':[{'name':'other'}]}
    (folder/'dataset-metadata.json').write_text(json.dumps(meta))
    try:
        res=api.dataset_create_new(str(folder), public=False, quiet=True)
        (ROOT/'KAGGLE_CREATE_LOG.txt').write_text('API dataset_create_new OK: '+str(res))
        print('kaggle create via API OK:', res, flush=True)
    except Exception as e:
        (ROOT/'KAGGLE_CREATE_LOG.txt').write_text('API dataset_create_new ECHEC: '+repr(e))
        state['last_batch']=batch_name+' (UPLOAD ECHEC)'; checkpoint(state); raise
    time.sleep(20)
    files=api.dataset_list_files(f'{username}/{batch_name}')
    remote=[f.name for f in files.files]
    print('fichiers distants verifies:', len(remote), flush=True)
    for o in ok: state['uploaded'][o['name']]={'batch':batch_name,'sha256':o['sha256'],'bytes':o['bytes'],'remote_verified': o['name'] in remote}
    state['batches'][batch_name]={'files':len(ok),'remote_files':len(remote)}
    state['last_batch']=batch_name; checkpoint(state)
    print('LOT TERMINE:', batch_name, len(ok), 'fichiers; total uploade:', len(state['uploaded']), '/282')
if __name__=='__main__': main()
