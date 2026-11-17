"""Verification distante Kaggle: liste complete (pagination) vs STATE.json."""
import json, pathlib, os, subprocess, sys
ROOT=pathlib.Path('reports/meta_alpha/kaggle_migration')
def checkpoint(msg):
    subprocess.run(['git','config','user.name','github-actions[bot]']); subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'])
    subprocess.run(['git','add','reports/meta_alpha/kaggle_migration']); subprocess.run(['git','commit','-q','-m',msg])
    subprocess.run(['git','pull','--rebase','-q','origin','arena/afe12737-xauusd-quant-research']); subprocess.run(['git','push','-q','origin','HEAD:arena/afe12737-xauusd-quant-research'])
def main():
    from kaggle.api.kaggle_api_extended import KaggleApi
    api=KaggleApi(); api.authenticate(); username=api.config_values.get('username')
    state=json.loads((ROOT/'STATE.json').read_text())
    out={'username':username,'batches':{},'total_verified_files':0,'all_ok':True}
    # regrouper par lot
    byl={}
    for name, info in state['uploaded'].items(): byl.setdefault(info['batch'], {})[name]=info
    for batch, files in sorted(byl.items()):
        remote={}; token=None
        for _ in range(10):
            res=api.dataset_list_files(f'{username}/{batch}', page_token=token, page_size=100)
            for f in res.files: remote[f.name]=getattr(f,'total_bytes', getattr(f,'totalBytes', None))
            token=getattr(res,'next_page_token', None)
            if not token: break
        missing=[n for n in files if n not in remote]
        badsize=[n for n,i in files.items() if n in remote and remote[n] not in (None, i['bytes'])]
        out['batches'][batch]={'attendus':len(files),'distants':len(remote),'manquants':missing,'tailles_differentes':badsize}
        out['total_verified_files']+=len(remote)-len(missing)
        if missing or badsize: out['all_ok']=False
        print(batch, len(files), 'attendus,', len(remote), 'distants, manquants:', missing, 'tailles diff:', badsize, flush=True)
    (ROOT/'VERIFY.json').write_text(json.dumps(out,indent=1))
    checkpoint('Kaggle verification distante complete')
    print('ALL_OK:', out['all_ok'], 'fichiers verifies:', out['total_verified_files'])
if __name__=='__main__': main()
