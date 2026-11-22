"""PHASE 11-B.1 - materialisation deterministe event_id / grappe_id.
Reproduit EXACTEMENT l'algorithme historique Phase 10 (fonction composantes
de ci_tools/phase10_synthesize.py, commit d'origine 84a3c5a, inchangee):
composantes connexes de recouvrement [t_signal, t_sortie] sur les seuls
evenements admissibles (entree_eligible==1 et fenetre_complete==1), par
famille separee. Le manifeste source n'est jamais modifie.
event_id: SHA-256 de la serialisation canonique
"famille|timeframe|t_signal|sens" (sens au format +1/-1), prefixe "EV-".
grappe_id: "GR-<famille>-<rang chronologique 00001...>" - nouvelles
etiquettes deterministes des composantes historiques reproduites (les
identifiants d'origine n'ont jamais existe)."""
import hashlib, json, pathlib, sys
import pandas as pd
sys.path.insert(0, 'ci_tools')
from phase10_synthesize import composantes

SRC = pathlib.Path('reports/meta_alpha/phase10/PHASE10_EVENTS_CIBLE.csv.gz')
OUT = pathlib.Path('reports/meta_alpha/phase11/PHASE11B_EVENT_CLUSTER_MAP.csv')
CODE_REF = 'ci_tools/phase10_synthesize.py:composantes (origine 84a3c5a)'

def sha256_fichier(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def event_id(famille, timeframe, t_signal, sens):
    canon = f"{famille}|{timeframe}|{t_signal}|{int(sens):+d}"
    return 'EV-' + hashlib.sha256(canon.encode('utf-8')).hexdigest(), canon

def main():
    avant = sha256_fichier(SRC)
    ev = pd.read_csv(SRC)
    lignes = []
    controle = {}
    for fam in ('F10-01', 'F10-03'):
        d = ev[ev.famille == fam].reset_index(drop=True)
        elig_mask = (d.entree_eligible == 1) & (d.fenetre_complete == 1)
        d_elig = d[elig_mask].reset_index(drop=True)
        ts0 = pd.to_datetime(d_elig.t_signal).values.astype('datetime64[ns]').astype('int64')
        ts1 = pd.to_datetime(d_elig.t_sortie).values.astype('datetime64[ns]').astype('int64')
        g = composantes(ts0, ts1)
        grappe_par_index = {int(i): f"GR-{fam}-{int(gg) + 1:05d}" for i, gg in zip(d_elig.index, g)}
        # correspondance index d_elig -> index d: positions des admissibles
        pos_elig = [int(i) for i in d.index[elig_mask]]
        grappe_par_pos = {pos: grappe_par_index[k] for k, pos in enumerate(pos_elig)}
        tailles = pd.Series(g).value_counts().sort_index()
        controle[fam] = {'detectes': int(len(d)), 'admissibles': int(len(d_elig)),
                         'non_admissibles': int(len(d) - len(d_elig)),
                         'grappes_reproduites': int(pd.Series(g).nunique()),
                         'taille_grappe_max': int(tailles.max()), 'grappes_singletons': int((tailles == 1).sum())}
        for pos, row in d.iterrows():
            eid, canon = event_id(row.famille, row.timeframe, row.t_signal, row.sens)
            adm = bool(elig_mask.loc[pos])
            if not adm:
                motif = 'ENTREE_INELIGIBLE' if int(row.entree_eligible) == 0 else 'FENETRE_INCOMPLETE'
            else:
                motif = 'AUCUN'
            lignes.append({'timeframe': row.timeframe, 'famille': fam, 'cle_composite_source': canon,
                           't_signal_utc': row.t_signal, 'sens': int(row.sens), 'event_id': eid,
                           'grappe_id': grappe_par_pos.get(int(pos), ''),
                           'statut_admissibilite': 'ADMISSIBLE' if adm else 'NON_ADMISSIBLE',
                           'motif_exclusion': motif,
                           'provenance': 'run 45011013927; reports/meta_alpha/phase10/PHASE10_EVENTS_CIBLE.csv.gz',
                           'code_historique': CODE_REF})
    M = pd.DataFrame(lignes)
    aperes = sha256_fichier(SRC)
    controle['_source'] = {'sha256_avant': avant, 'sha256_apres': aperes, 'source_inchangee': avant == aperes,
                           'lignes_carte': int(len(M)), 'event_id_uniques': int(M.event_id.nunique()),
                           'doublons_event_id': int(M.duplicated('event_id').sum()),
                           'familles_dans_une_meme_grappe': int(M[M.grappe_id != ''].groupby('grappe_id').famille.nunique().max())}
    M.to_csv(OUT, index=False)
    controle['_carte_sha256'] = sha256_fichier(OUT)
    pathlib.Path('/tmp/phase11b1_controle.json').write_text(json.dumps(controle, indent=1))
    print(json.dumps(controle, indent=1))

if __name__ == '__main__': main()
