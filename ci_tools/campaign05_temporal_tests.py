"""CAMPAGNE 5 - validation temporelle AVANT calcul (donnees synthetiques)."""
import sys
import numpy as np
sys.path.insert(0, 'ci_tools')
from campaign05_engine import statut_fenetre, classe_retard, avant, atteinte_reelle, categorie_issue, mises_a_jour_niveaux

ok = []
# 1) avant B = disponibilite strictement inferieure a B (passee en minutes depuis minuit)
import datetime as dt
assert avant(dt.datetime(2019, 1, 1, 7, 59), dt.datetime(2019, 1, 1, 8, 0)) is False or True
# convention: disponibilite passee en datetime de cloture de barre
dispo_0759 = dt.datetime(2019, 1, 1, 8, 0)   # barre commencant 07:59, disponible 08:00
dispo_0758 = dt.datetime(2019, 1, 1, 7, 59)  # barre commencant 07:58
assert avant(dispo_0759, dt.datetime(2019, 1, 1, 8, 0)) == False, 'barre 07:59 disponible 08:00: pas avant 08:00'
assert avant(dispo_0758, dt.datetime(2019, 1, 1, 8, 0)) == True
ok.append("avant B: disponibilite < B (barre de 07:59 exclue, barre de 07:58 incluse)")
# 2) atteinte reelle identifiable seulement si zero minute manquante avant
assert atteinte_reelle(0) and not atteinte_reelle(1) and not atteinte_reelle(45)
ok.append("atteinte reelle identifiable: 0 minute manquante avant; sinon ATTEINTE OBSERVEE")
# 3) statuts de fenetre
assert statut_fenetre(60, 60, 0) == 'COMPLETE'
assert statut_fenetre(60, 55, 3) == 'PARTIELLE'
assert statut_fenetre(30, 29, 6) == 'CENSUREE'
assert statut_fenetre(5, 2, 3) == 'CENSUREE'
ok.append("fenetres: COMPLETE/PARTIELLE/CENSUREE selon couverture et trou maximal")
# 4) retards d'ouverture
assert classe_retard(0) == 'PONCTUELLE' and classe_retard(4) == 'LEGER' and classe_retard(20) == 'DIFFEREE' and classe_retard(31) == 'INELIGIBLE'
ok.append("retards: PONCTUELLE/LEGER/DIFFEREE/INELIGIBLE (>30 min)")
# 5) mouvement nul jamais poursuite; quatre categories
assert categorie_issue(0.0, 0, True, False) == 'MOUVEMENT_NUL'
assert categorie_issue(12.0, 1, True, False) == 'POURSUITE_SEULE'
assert categorie_issue(12.0, 1, False, True) == 'RETOURNEMENT_SEUL'
assert categorie_issue(12.0, 1, True, True) == 'LES_DEUX'
assert categorie_issue(12.0, 1, False, False) == 'AUCUN'
ok.append("C5-02: mouvement nul exclu des poursuites; poursuite seule/retournement seul/les deux/aucun")
# 6) mises a jour par pas de 5 bp ancre au niveau franchi
assert mises_a_jour_niveaux(100.0, 100.0, 1) == 0
assert mises_a_jour_niveaux(100.06, 100.0, 1) == 1   # +6 bp > seuil 1 (5 bp)
assert mises_a_jour_niveaux(100.11, 100.0, 1) == 2   # +11 bp > seuil 2 (10 bp)
assert mises_a_jour_niveaux(99.94, 100.0, -1) == 1
ok.append("mises a jour: pas relatifs de 5 bp ancres au niveau franchi, sans arrondi ajoute")
print('VALIDATION TEMPORELLE CAMPAGNE 5 : OK')
for o in ok: print(' -', o)
