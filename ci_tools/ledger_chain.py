"""Registre scientifique verrouille: chaine de hash ancreE dans Git.
Chaque entree contient prev_hash; entry_hash = sha256(prev_hash + entree canonique).
Modifier le registre ET son empreinte casse la chaine a partir de l'entree touchee
et exige de reecrire toutes les entrees suivantes — visible dans l'historique Git
du fichier lui-meme (l'ancrage externe = l'historique distant de la branche).
Un workflow doit appeler `verify` AVANT tout calcul et refuser de tourner si KO."""
import json, hashlib, pathlib, sys
P = pathlib.Path('reports/meta_alpha/TRIAL_LEDGER_CHAIN.json')

def canon(o): return json.dumps(o, sort_keys=True, separators=(',',':'), ensure_ascii=False)

def load():
    if P.exists(): return json.loads(P.read_text())
    return {'entries': []}

def entry_hash(prev, entry): return hashlib.sha256((prev+canon(entry)).encode()).hexdigest()

def add(entry):
    d=load(); prev=d['entries'][-1]['entry_hash'] if d['entries'] else 'GENESIS'
    e={'seq':len(d['entries'])+1,'prev_hash':prev,'entry':entry}
    e['entry_hash']=entry_hash(prev, entry); d['entries'].append(e)
    P.write_text(json.dumps(d,indent=1,ensure_ascii=False)); return e['entry_hash']

def verify():
    d=load(); prev='GENESIS'
    for e in d['entries']:
        if e['prev_hash']!=prev: return False, f"chaine cassee seq {e['seq']}"
        if entry_hash(prev, e['entry'])!=e['entry_hash']: return False, f"hash invalide seq {e['seq']}"
        prev=e['entry_hash']
    return True, f"{len(d['entries'])} entrees, chaine valide, tete={prev[:16]}"

def registry_lock(registry_path):
    """Empreinte d'un registre d'hypotheses a stocker dans une entree chainee."""
    return hashlib.sha256(pathlib.Path(registry_path).read_bytes()).hexdigest()

if __name__=='__main__':
    if sys.argv[1]=='verify': print(verify())
    elif sys.argv[1]=='lock':
        print(add({'type':'REGISTRY_LOCK','registry':sys.argv[2],'sha256':registry_lock(sys.argv[2])}))
