"""CAMPAGNE 4 - validation temporelle AVANT calcul (donnees synthetiques).
Verifie: terciles causaux (jour courant exclu des seuils), confirmation
D = C+2 jamais antidatee, non-confirmees conservees avec persistance,
traversee et vitesses, episodes interrompus par NON_CLASSE."""
import sys
import numpy as np
sys.path.insert(0, 'ci_tools')
from campaign04_engine import tercile_causal, episodes_et_transitions

ok = []
# 1) tercile causal: une valeur extreme aujourd'hui ne change pas ses propres seuils
vals = np.concatenate([np.full(50, 10.0), [10000.0]])
lab, q1, q2 = tercile_causal(vals, 60, 40)
assert lab[-1] == 'HAUT' and q1[-1] == 10.0 and q2[-1] == 10.0
lab2, _, _ = tercile_causal(np.concatenate([np.full(50, 10.0), [10.0]]), 60, 40)
assert lab2[-1] in ('BAS', 'MOYEN')
ok.append("terciles causaux: seuils des 60 jours precedents, jour courant exclu")
# 2) minimum d'historique
lab3, _, _ = tercile_causal(np.arange(30.0), 60, 40)
assert (lab3 == 'NON_CLASSE').all()
ok.append("minimum 40 jours d'historique: aucun etat sinon (amorcage publie)")
# 3) confirmation D = C+2, jamais antidatee
etats = ['BAS'] * 5 + ['HAUT'] * 4 + ['BAS'] * 6
eps, trans = episodes_et_transitions(etats)
t = trans[0]
assert t['candidate_idx'] == 5 and t['confirmee'] and t['confirmation_idx'] == 7, t
assert t['confirmation_idx'] > t['candidate_idx']
ok.append("transition confirmee: candidate jour 5, confirmation jour 7 (D = C+2), jamais antidatee")
# 4) non-confirmee conservee avec persistance
etats2 = ['BAS'] * 5 + ['HAUT'] * 2 + ['MOYEN'] * 4
_, trans2 = episodes_et_transitions(etats2)
t2 = [x for x in trans2 if x['vers'] == 'HAUT'][0]
assert (not t2['confirmee']) and t2['persistance'] == 2 and t2['confirmation_idx'] is None
ok.append("transition non confirmee conservee (persistance 2 jours, motif lisible)")
# 5) traversee et vitesses (episodes adjacents: traversee = 1)
etats3 = ['BAS'] * 3 + ['MOYEN'] * 4 + ['HAUT'] * 3
_, trans3 = episodes_et_transitions(etats3)
assert trans3[0]['traversee'] == 1 and trans3[0]['vitesse'] == 'RAPIDE'
ok.append("traversee comptee entre episodes (dernier jour ancien exclu, premier nouveau inclus)")
# 6) NON_CLASSE intercale: pas de transition fabriquee
etats4 = ['BAS'] * 3 + ['NON_CLASSE'] * 2 + ['HAUT'] * 3
eps4, trans4 = episodes_et_transitions(etats4)
assert len(eps4) == 2 and len(trans4) == 0
ok.append("NON_CLASSE intercale: episodes separes, aucune transition inventee")
print('VALIDATION TEMPORELLE CAMPAGNE 4 : OK')
for o in ok: print(' -', o)
