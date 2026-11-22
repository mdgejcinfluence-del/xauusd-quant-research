"""PHASE 10 - etape 2 ciblee (seq291): agrege les barres M1 des 8 lots,
construit H1/H4 et recalcule uniquement F10-01/F10-03 (seuils seq289).
Aucun telechargement, aucun acces holdout."""
import glob, json, os, pathlib, sys
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase10_engine import construire_barres, evenements_tf, ROOT

def main():
    dossier = os.environ.get('BARS_DIR', 'bars_artifacts')
    fs = sorted(glob.glob(f'{dossier}/**/P10_BARS_*.csv.gz', recursive=True))
    print('fichiers barres', fs, flush=True)
    if len(fs) < 8: raise RuntimeError(f'integrite lots: {len(fs)}/8 fichiers de barres')
    bars = pd.concat([pd.read_csv(f) for f in fs])
    bars['ts'] = pd.to_datetime(bars.ts)
    bars = bars.drop_duplicates('ts').sort_values('ts').reset_index(drop=True)
    all_ev, resume = [], {'mode': 'CIBLE_F10-01_F10-03_ETAPE2', 'amendement': 'seq289', 'lots_barres': len(fs),
                          'barres_m1': int(len(bars)), 'diagnostics': {}}
    for nom_tf, minutes in [('H1', 60), ('H4', 240)]:
        tf = construire_barres(bars, minutes)
        ev, dg = evenements_tf(tf, nom_tf, minutes, cible=True)
        fam = 'F10-01' if nom_tf == 'H1' else 'F10-03'
        resume['diagnostics'][fam] = dg
        all_ev += ev
        print('P10 ETAPE2', nom_tf, 'barres', len(tf), 'evenements', len(ev), flush=True)
    EV = pd.DataFrame(all_ev)
    EV.round(4).to_csv(ROOT / 'PHASE10_EVENTS_CIBLE.csv.gz', index=False, compression='gzip')
    if len(EV): resume['evenements_par_famille'] = {k: int(v) for k, v in EV.famille.value_counts().items()}
    (ROOT / 'P10_CIBLE_COVERAGE.json').write_text(json.dumps(resume, indent=1))
    print(json.dumps(resume), flush=True)

if __name__ == '__main__': main()
