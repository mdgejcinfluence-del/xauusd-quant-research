# PHASE 14 — PROCÈS-VERBAL DE GEL DES RÉSULTATS (PHASE 14.1)

**Verdict : `PHASE14_FROZEN_EXPLORATORY`**
**Qualification permanente : `EXPLORATOIRE_IS — HYPOTHÈSES
POSTÉRIEURES AUX RÉSULTATS DE PHASE 13-B`. Ce gel ne constitue ni
une confirmation indépendante, ni une preuve de rentabilité, ni
une stratégie ; le verdict `ECONOMICALLY_CONFIRMED_INDEPENDENTLY`
demeure interdit sur cette base.**

## Base gelée

- Préenregistrement 14-A gelé avant calcul (seq334) : protocole
  `da9e52a5…`, grille `791424f4…`, préenregistrement `e1cc412d…`,
  dictionnaire `3f6c5674…`.
- Exécution 14-B : run CI `45054081666` (vert, exit 0) ; verdicts
  `MFE_MAE_SEQUENCE_ANALYZED` + `BARRIER_MATRIX_COMPLETED_EXPLORATORY_IS`
  (seq335, commit `a020bf7`).
- Audit 14.1 (seq336) : réconciliation complète depuis les seuls
  artefacts — 54 cellules sans écart, pondérations grappe et
  quartiles conformes, étiquettes de coûts conformes, franchissements
  après trou conformes à la convention gelée.

## Correction annexée au gel (sans modifier les livrables originaux)

Le taux « MAE avant MFE » de la Phase 14 (50,3 %) portait sur 443
événements incluant les 22 trajectoires incomplètes, dont l'ordre
global des extrêmes n'est pas connaissable sur une fenêtre
censurée. **Dénominateur gelé et correct : 421 trajectoires
complètes — 212 MAE d'abord (50,36 %), 209 MFE d'abord** ; les 22
incomplètes sont `CENSORED` pour l'ordre global dans
`PHASE14_1_SEQUENCE_DENOMINATORS.csv`. Le sens de la conclusion
(aucune avance systématique) est inchangé. Limite consignée :
l'ordre des mouvements pendant les trous de cotation et la
dernière cotation avant trou ne sont pas vérifiables depuis les
artefacts conservés ; la classification des 28 franchissements
après trou repose sur la convention gelée ex ante (premier prix
observable après le trou).

## Portée

Résultats exploratoires IS sur cohorte déjà étudiée, commissions
exclues : aucune configuration (notamment ATR B08/B09) n'est
sélectionnée, validée ou recommandée. Toute utilisation ultérieure
d'une configuration exigerait une décision distincte, un nouveau
préenregistrement et des données n'ayant servi ni à la conception
ni à la sélection ; le holdout 2020–2026 reste définitivement
exclu. Aucune étape suivante n'est autorisée par le présent gel.
