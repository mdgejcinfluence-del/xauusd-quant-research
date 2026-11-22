# PHASE 14.1 — RAPPORT DE RÉCONCILIATION ET D'AUDIT DES DÉNOMINATEURS

**Périmètre : artefacts et journaux déjà produits uniquement
(Phases 13-B et 14). Aucune lecture de ticks bruts, aucun recalcul
de barrières, aucune nouvelle exploration. Qualification inchangée :
`EXPLORATOIRE_IS — HYPOTHÈSES POSTÉRIEURES AUX RÉSULTATS DE
PHASE 13-B`. Aucune configuration n'est sélectionnée ; aucune
nouvelle conclusion de rentabilité n'est produite.**

**Verdict : `PHASE14_FROZEN_EXPLORATORY`** (gel émis sous
`PHASE14_FREEZE_RECORD.md`, avec la correction de dénominateur du
§2 explicitement annexée — les livrables Phase 14 originaux ne
sont pas modifiés).

## 1. Méthode

Réconciliation effectuée par le script `ci_tools/phase14_1_audit.py`
à partir de `PHASE14_EVENT_PATH_SEQUENCE.csv`,
`PHASE14_TRIPLE_BARRIER_EVENTS.csv`, `PHASE14_BARRIER_MATRIX.csv`,
`PHASE14_RESULTS.json`, `PHASE14_COVERAGE_AND_AMBIGUITIES.csv`,
des artefacts de chemin `P14_PATH_*.csv` produits en Phase 14 et
de `PHASE13B_EVENT_EXECUTIONS.csv`. Seules des agrégations de
contrôle sur ces fichiers événementiels ont été calculées.

## 2. Dénominateurs de séquence MFE/MAE — DIVERGENCE DOCUMENTÉE, RÉCONCILIÉE

Le rapport Phase 14 annonçait 223 `MAE_BEFORE_MFE` et 220
`MFE_BEFORE_MAE`, totalisant 443, soit un taux « MAE d'abord » de
50,3 % **sur 443**. La réconciliation événement par événement
(`PHASE14_1_SEQUENCE_DENOMINATORS.csv`, 443 lignes) établit :

- 421 trajectoires **complètes** : 212 MAE d'abord, 209 MFE
  d'abord, 0 même timestamp, 0 indéterminé ;
- 22 trajectoires **incomplètes** (13-B) : classées en Phase 14
  (11/11) à partir des extrêmes observés avant interruption.

Or les maxima globaux d'une fenêtre censurée avant son terme ne
sont pas connaissables : un extrême observé avant la lacune ne
prouve pas qu'il resterait l'extrême global de la fenêtre. Pour
l'analyse de l'**ordre global** MFE/MAE, ces 22 événements sont
donc reclassés **`CENSORED`** dans le tableau réconcilié (colonne
`ordre_global_reconcilie`), sans modifier le livrable Phase 14
original. **Dénominateur correct des statistiques de séquence :
421.** Taux réconcilié « MAE avant MFE » : 212/421 = **50,36 %**,
contre 50,34 % sur 443 : la divergence est un défaut de
dénominateur, documenté et corrigé ; **le sens de la conclusion
est inchangé** (aucune avance systématique d'un extrême sur
l'autre). Le taux communiqué de 50,3 % doit désormais être lu
avec le dénominateur 421.

## 3. Trous de cotation et 84 « franchissements » — CONFORME AU GEL, LIMITE CONSIGNÉE

Précision de comptage : les « 84 franchissements » du rapport
Phase 14 sont des lignes événement × configuration × scénario ;
ils correspondent à **28 franchissements uniques
(événement × configuration)** touchant **11 événements**, répétés
sur les 3 scénarios (les franchissements ne dépendent pas du
scénario). Pour chacun (`PHASE14_1_GAP_CROSSING_AUDIT.csv`) :
le trou a été retrouvé dans les artefacts de chemin (début, fin,
durée : de ≈ 60 minutes à ≈ 2 942 minutes — il s'agit pour
l'essentiel de fermetures régulières nuit/week-end), le premier
tick suivant le trou est présent dans la séquence d'extrêmes, et
son prix de liquidation franchit bien le niveau de la barrière
concernée (28/28 vérifiés au-delà du niveau, dans le bon sens).
**Convention effectivement appliquée = convention du
préenregistrement gelé (seq334)** : franchissement déterminé au
premier prix observable après le trou, prix de ce tick utilisé,
horodatage réel du tick (jamais inventé). Aucun amendement
rétroactif n'a été nécessaire ni appliqué.
**Limite qui reste ouverte et consignée** : l'ordre des mouvements
*pendant* le trou n'est pas observable par construction, et la
dernière cotation valide avant le trou n'est pas conservée en
tant que telle dans les artefacts de chemin (seuls les ticks
atteignant un nouvel extrême courant et les bornes de morceaux y
figurent) — ces deux éléments ne sont pas vérifiables sans
nouvelle extraction, laquelle n'est pas autorisée par la présente
mission. La classification repose donc sur la convention gelée
ex ante (exécution au premier prix observable), non sur une
preuve de trajectoire intra-trou ; aucune trajectoire continue
n'a été supposée dans les calculs, les prix et horodatages
utilisés étant ceux du premier tick réel suivant chaque trou.

## 4. Matrice des barrières — 54 CELLULES CONCORDANTES

Réconciliation cellule par cellule
(`PHASE14_1_BARRIER_MATRIX_RECONCILIATION.csv`) : effectifs
TP/SL/VERTICAL/censures, effectif économique, moyenne, médiane,
taux positif, perte maximale, moyennes et médianes par grappe —
**0 écart** au-delà de 10⁻⁹ entre la matrice publiée et les
agrégations recalculées depuis le fichier événementiel. Valeurs
communiquées confirmées : ATR B09 S0 **+1,9407 bp**, S2
**−0,0593 bp** ; ATR B08 S0 **+1,6110 bp**, S2 **−0,3890 bp** ;
pertes maximales ATR en S0 comprises entre **−63,89 et −32,17 bp**
selon la configuration ; les **9 configurations `R_EVENT` sont
toutes négatives en moyenne S0**. Aucune configuration n'est
sélectionnée, B08 et B09 ne sont ni distinguées ni recommandées.

## 5. Pondération par grappe — CONFORME

408 `grappe_id` distincts dans la cohorte (repris tels quels des
Phases 11-B/13-B, **aucun recalcul**) ; pour les 54 cellules
(`PHASE14_1_CLUSTER_WEIGHTING_AUDIT.csv`) : moyenne intra-grappe
puis moyenne des grappes à poids égal, vérifiées ; les événements
censurés sont exclus des deux pondérations avec des dénominateurs
explicites et distincts (distributions événementielles ≠
distributions des moyennes par grappe). Aucun résultat par grappe
absent.

## 6. Quartiles de confiance — CONFORMES

Reconstruction du classement sur le seul `p_M1` (départage
`event_id`) : concordance totale avec les étiquettes Phase 14 ;
seuils identiques à ceux consignés (Q1 [0,7599 ; 0,7961], Q2
[0,7963 ; 0,8228], Q3 [0,8228 ; 0,8660], Q4 [0,8666 ; 0,9996] ;
111/111/111/110) ; aucun classement fondé sur MFE, MAE ou
rendement. Conclusion descriptive Q4 confirmée telle quelle :
MFE médian 30,77 bp, MAE médian 18,02 bp, fréquence MFE d'abord
47,3 % — **aucun avantage temporel d'ordre démontré** ; Q4 n'est
pas transformé en filtre.

## 7. Coûts — CONFORMES

Étiquettes par scénario présentes et exactes dans le fichier
événementiel (S0/S1/S2, cf. `PHASE14_1_RESULTS.json`). Statuts de
franchissement **identiques entre scénarios** pour chaque
événement × configuration (le slippage n'affecte que les
remplissages) ; deltas médians des résultats S1−S0 = −1,00 bp et
S2−S0 = −2,00 bp, conformes à la grille gelée. Spread intégré une
seule fois aux prix Bid/Ask ; aucune commission inventée
(`COMMISSION_EXCLUDED_BY_DESIGN`) ; aucun résultat qualifié de
net après tous les coûts.

## 8. Synthèse des contrôles

| Contrôle | Statut |
|---|---|
| Dénominateurs de séquence | Divergence de dénominateur (443 → 421) documentée et réconciliée ; sens inchangé ; 22 incomplètes reclassées `CENSORED` pour l'ordre global |
| Franchissements après trou (28 uniques / 11 événements) | Conformes à la convention gelée ; trous et prix vérifiés 28/28 ; ordre intra-trou et dernière cotation avant trou : limites ouvertes consignées (non vérifiables sans nouvelle extraction) |
| Matrice 18 × 3 = 54 cellules | Conforme, 0 écart |
| Pondérations grappe | Conformes, dénominateurs explicites |
| Quartiles Q1–Q4 | Conformes, descriptifs |
| Étiquettes et slippage | Conformes (remplissages seuls) |

Les conclusions confirmées par les artefacts sont celles des §2
(taux réconcilié), 4, 5, 6 et 7. La seule divergence numérique —
le dénominateur du taux de séquence — est intégralement
réconciliée depuis les artefacts existants et ne change pas le
sens des résultats. Les résultats Phase 14 sont gelés **tels que
réconciliés par le présent audit** ; les livrables originaux
demeurent inchangés et l'écart reste tracé dans la chaîne.
