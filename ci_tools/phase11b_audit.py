"""PHASE 11-B - audit structurel en lecture seule des manifestes Phase 10.
Aucune trajectoire, aucun seuil, aucune grappe recalculee; aucun acces holdout."""
import json, pathlib
import pandas as pd

D = pathlib.Path('reports/meta_alpha/phase10')
ATTENDU = {'F10-01': {'detectes': 3134, 'admissibles': 3107, 'grappes': 2617, 'non_admissibles': 27},
           'F10-03': {'detectes': 762, 'admissibles': 660, 'grappes': 597, 'non_admissibles': 102}}

def audit_famille(ev, fam):
    d = ev[ev.famille == fam].copy()
    elig = d[(d.entree_eligible == 1) & (d.fenetre_complete == 1)]
    inelig = d.drop(elig.index)
    ts = pd.to_datetime(d.t_signal, errors='coerce')
    R = {'famille': fam, 'lignes': int(len(d)),
         'timeframes_observes': sorted(d.timeframe.dropna().unique().tolist()),
         'sens_observes': sorted(int(s) for s in d.sens.dropna().unique()),
         'eres_observees': sorted(d.ere.dropna().unique().tolist()),
         't_signal_non_parsables': int(ts.isna().sum()),
         't_signal_min': str(ts.min()), 't_signal_max': str(ts.max()),
         't_signal_strictement_croissant_dans_le_fichier': bool(ts.is_monotonic_increasing),
         'doublons_ligne_complete': int(d.duplicated().sum()),
         'doublons_cle_composite_famille_tsignal_sens': int(d.duplicated(subset=['famille', 't_signal', 'sens']).sum()),
         'doublons_cle_composite_famille_tsignal': int(d.duplicated(subset=['famille', 't_signal']).sum()),
         'admissibles_entree_et_fenetre': int(len(elig)),
         'non_admissibles': int(len(inelig)),
         'non_admissibles_entree_ineligible': int((inelig.entree_eligible == 0).sum()),
         'non_admissibles_fenetre_incomplete': int((inelig.fenetre_complete == 0).sum()),
         'eligibles_t_entree_manquante': int(pd.to_datetime(elig.t_entree, errors='coerce').isna().sum()),
         'eligibles_t_sortie_manquante': int(pd.to_datetime(elig.t_sortie, errors='coerce').isna().sum()),
         'eligibles_seuil_bp_manquant': int(elig.seuil_bp.isna().sum()) if 'seuil_bp' in elig else None,
         'attendu': ATTENDU[fam]}
    R['comptes_conformes'] = (R['lignes'] == ATTENDU[fam]['detectes'] and R['admissibles_entree_et_fenetre'] == ATTENDU[fam]['admissibles']
                              and R['non_admissibles'] == ATTENDU[fam]['non_admissibles'])
    return R

def main():
    ev = pd.read_csv(D / 'PHASE10_EVENTS_CIBLE.csv.gz')
    vieux = pd.read_csv(D / 'PHASE10_EVENTS.csv.gz')
    corr = json.loads((D / 'PHASE10_CORRECTION_RESULTS.json').read_text())
    res10 = json.loads((D / 'PHASE10_RESULTS.json').read_text())
    cov = json.loads((D / 'P10_CIBLE_COVERAGE.json').read_text())
    ver = json.loads((D / 'CORRECTION_ARTIFACT_VERIFICATION.json').read_text())
    out = {'colonnes_manifeste_cible': list(ev.columns),
           'presence_colonne_event_id': any('event' in c.lower() and 'id' in c.lower() for c in ev.columns),
           'presence_colonne_grappe_id': any('grappe' in c.lower() or 'cluster' in c.lower() for c in ev.columns),
           'presence_colonne_P0': any(c.lower() in ('p0', 'p_0', 'prix_p0', 'mid_cloture') for c in ev.columns),
           'familles_manifeste_cible': {k: int(v) for k, v in ev.famille.value_counts().items()},
           'familles_ancien_manifeste_defectueux': {k: int(v) for k, v in vieux.famille.value_counts().items()},
           'par_famille': {fam: audit_famille(ev, fam) for fam in ATTENDU},
           'grappes_enregistrees_resultats_correction': {f: corr[f].get('grappes') for f in ATTENDU},
           'grappes_enregistrees_conformes': all(corr[f].get('grappes') == ATTENDU[f]['grappes'] for f in ATTENDU),
           'diagnostics_couverture': cov.get('diagnostics'),
           'lots_barres': cov.get('lots_barres'), 'barres_m1': cov.get('barres_m1'),
           'verification_artefacts_44919631588': {'partitions': (ver.get('partitions_chargees'), ver.get('partitions_attendues')),
                                                  'concordance': ver.get('concordance_avec_resultats_seq288'),
                                                  'barres_tf': ver.get('barres_tf')},
           'ancien_resultats_F10_01_03': {f: {'detectes': res10[f]['detectes'], 'verdict': res10[f]['verdict']} for f in ATTENDU}}
    pathlib.Path('/tmp/phase11b_audit_raw.json').write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str))

if __name__ == '__main__': main()
