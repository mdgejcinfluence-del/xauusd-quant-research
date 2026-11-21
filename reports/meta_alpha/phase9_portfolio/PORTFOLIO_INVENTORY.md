# PHASE 9 — INVENTAIRE INTÉGRAL DU PORTEFEUILLE META ALPHA (étape A)

**Campagne 8 acceptée et clôturée au niveau descriptif (aucune candidate
ANO-C8). Nouvelles campagnes suspendues par ordre du fondateur.**
Sources : registres et catalogues officiels des campagnes 0–8 et
`ANOMALY_REGISTRY.json` (phases antérieures). **Aucune fiche historique
n'est modifiée.** Statuts Phase 9 : J1 descriptive ; M1 mécanisme
documenté ; J2 prédictibilité confirmée indépendamment ; E1/E2 avantage
après coûts estimés / robuste ; S1/S2 stratégie ; P1 prop firm.
**Aucune découverte du portefeuille ne dépasse J1 à ce jour.**

## 1. Registre central des découvertes positives (J1)

| ID | Origine | Phénomène (définition courte) | Effet [IC 95 %] | p / q | Matérialité | Info temporelle réelle | Dépendances / avertissements |
|---|---|---|---|---|---|---|---|
| ANOM-001 | phases tick | autocorrélation lag-1 des rendements **mid** tick | +0,487 | — | n/a | tick, mais prix mid construits | mécanisme demi-pas **réfuté** par preuve directe ; non exécutable (mid) |
| ANOM-002 | phases tick | regroupement de volatilité (autocorr. \|r\| décroissante) | lag1 0,457 → lag20 0,132 | — | n/a | causale en principe | phénomène de littérature ; contexte, pas un signal |
| ANO-C1-001 | C1 | réintégration <60 min des dépassements de niveaux (Asie/veille) | ~85 % réintégrés, délai médian 3 min | descriptif | forte en fréquence | dépassement connu à sa barre ; profondeur finale **non** connue à T0 | base des fiches C2-001/002/004 et de REL-T0 |
| ANO-C1-002 | C1 | cassures confirmées +5 bp souvent retestées, prix encore au-delà à +60 min | retest 79 % ; au-delà 55 % | descriptif | moyenne | cassure et retest observables en séquence | pas de magnitude associée à la fréquence de 55 % |
| ANO-C1-003 | C1 | retour contraire ≥100 % des impulsions M5 | 46,6 % ; retracement max médian 90,5 % | descriptif | forte en fréquence | impulsion connue à T0 (clôture du déclenchement) | taux de base du « fade » d'impulsion ; voir ANO-C3-001 |
| ANO-C1-004 | C1 | heure de formation des extrêmes journaliers | médiane ~11–12 h UTC (correction seq160 : 12 h) | descriptif | n/a | connue seulement en fin de journée | timing descriptif ; non opérationnel en l'état |
| ANO-C1-005 | C1 | range des 60 min après consolidation M1 calme | médiane 14,3 bp | descriptif | échelle | consolidation connue à sa fin | direction indéterminée (volatilité, pas de sens) |
| ANO-C2-001 | C2 (T01) | réintégration quasi totale si profondeur **finale** faible | +32,4 pts [31,6 ; 33,3], 98,2 % vs 65,8 % | p_BY <0,001 | forte | **requalifiée rétrospective** (profondeur finale = futur) ; version T0 = REL-T0 | ne pas utiliser la profondeur finale en règle |
| ANO-C2-002 | C2 (T03) | délai de réintégration 2 vs 3 min selon profondeur finale | ratio 0,67 | p_BY <0,001 | faible (granularité minute) | rétrospective (même requalification) | mesure conditionnelle à la réintégration |
| ANO-C2-003 | C2 (T07) | retests de cassure moins fréquents en régime F3 BAS | −12,8 pts [−16,8 ; −8,6] | p_BY publié | moyenne | **étiquette F3 poolée rétrospective, non causale** (audit F3) | usage causal interdit en l'état ; chantier étiquettes causales non ouvert |
| ANO-C2-004 | C2 (T10) | après retest, encore au-delà à +60 min : 26,9 % (prof. faible) vs 80,7 % (forte) | −53,8 pts [−57,6 ; −49,8] | p_BY <0,001 | forte | requalifiée rétrospective (profondeur finale) ; lien ANO-C1-002 | la profondeur à T0 seule ne reproduit pas ce contraste |
| ANO-C2-005 | C2 | retour complet des impulsions en baisse d'ère 49,3 % → 40,2 % | +9,1 pts [8,0 ; 10,3] | publié | moyenne | ère connue, effet historique | dérive d'ère, pas une règle |
| ANO-C2-006 | C2 (T12) | retracement d'impulsions plus faible en régime BAS | ratio 0,81 [0,77 ; 0,84] | publié | moyenne | **étiquette F3 poolée non causale** | même blocage que C2-003 |
| ANO-C2-007 | C2 | retour complet après impulsion asiatique 42,1 % vs américaine 48,4 % | −6,3 pts [−7,4 ; −5,2] | publié | moyenne | session connue à T0 | forme antérieure, moins nette, d'ANO-C3-001 |
| ANO-C2-008 | C2 (T14) | range post-consolidation plus faible en régime BAS | ratio 0,86 [0,84 ; 0,88] | publié | faible | **étiquette F3 poolée non causale** | direction indéterminée |
| ANO-C2-009 | C2 | range post-compression en baisse d'ère 17,9 → 12,6 bp | ratio 1,42 [1,37 ; 1,47] | publié | échelle | ère | dérive d'échelle historique |
| ANO-C2-010 | C2 | expansion ≥1,5× après compression courte 46,8 % vs longue 41,5 % | +5,3 pts [3,6 ; 7,1] | publié | faible | durée de compression connue à sa fin | direction indéterminée |
| ANO-C2-011 | C2 | range première heure NY en baisse d'ère 43,5 → 28,9 bp | ratio 1,51 [1,42 ; 1,62] | publié | échelle | session + ère | contexte d'exécution, pas un signal |
| ANO-C2-012 | C2 (T20) | mouvements extrêmes des 5 premières minutes NY : 5,6 % (BAS) vs 18,8 % (HAUT) | −13,2 pts [−16,5 ; −9,9] | publié | moyenne | **étiquette F3 poolée non causale** | même blocage |
| ANO-C2-013 | C2 | spread médian après ouverture de Londres en baisse d'ère | 2,40 → 1,87 bp, ratio 1,28 [1,25 ; 1,33] | publié | coût | observable tick IS | **donnée de coût observée** (voir audit coûts) |
| ANO-C2-014 | C2 | extrême haut formé dans le dernier tiers : Asie 41,6 % vs New York 14,4 % | +27,2 pts [24,7 ; 29,5] | publié | moyenne | connue en fin de session seulement | timing rétrospectif |
| REL-T0 | C2.2–2.3 | **profondeur du dépassement mesurée à la barre T0** et réintégration ultérieure | tercile bas T0 : 90,6 % [89,7 ; 91,6] ; réplication décennale +13,3 pts [12,2 ; 14,2] | descriptif répliqué | forte en fréquence | **causale à la clôture de la barre T0** | profondeur médiane du tercile bas : 0,78 bp — amplitude minuscule, voir coûts ; protocole de confirmation 2.4 préparé, non exécuté, T0 tenu séparé |
| ANO-C3-001 | C3 (C3-02) | retracement complet <1 h des impulsions M5 : Londres 57,9 % vs Asie 50,7 % | +7,2 pts [6,0 ; 8,3] | p 0,0005 ; q BY 0,0031 | au-dessus du seuil gelé (5 pts) | session connue à T0 | cohérent dans les 3 ères ; chevauchements d'épisodes comptés |
| ANO-C3-002 | C3 (C3-03) | retracement maximal après impulsions d'amplitude initiale causale basse | −2,40 bp [−2,81 ; −2,04] | q BY 0,0031 | sous les seuils usuels en bp | groupe d'amplitude causal (60 j passés) | échelle non normalisée ; lecture descriptive |
| ANO-C3-003 | C3 | sortie de consolidation par barre >2× le range de formation, plus fréquente si formation étroite | +13,3 pts [12,2 ; 14,2] (réplication décennale T0) | q publié | forte en fréquence | formation connue à sa fin | expansion de volatilité **sans direction** établie |
| ANO-C4-001 | C4 (C4-08) | fréquence journalière des impulsions selon l'état de volatilité **du même jour** | ratio 2,68 | q BY 0,0037 | forte | état connu **à la clôture du jour seulement** | association contemporaine ; inutilisable en intraday en l'état |
| ANO-C4-002 | C4 (C4-09) | déphasage sessions/journée selon l'état journalier | −76,5 pts | q BY 0,0037 | n/a | clôture du jour | **mécanique par construction** (avertissement majeur) ; valeur = quantifier l'hétérogénéité intrajournalière |
| ANO-C5-001 | C5 (C5-01) | amplitude des 30 min après l'ouverture de Londres vs d'Asie | ratio 1,189 [1,148 ; 1,236] (15,34 vs 12,90 bp) | q 0,0042 | sous le seuil (bornes) | heure d'ouverture connue | session/volatilité ; pas de direction |
| ANO-C5-002 | C5 (C5-06) | premières atteintes du haut de la veille disponibles avant 08:00 plus souvent que du bas | +8,08 pts [+3,80 ; +12,59] | q 0,0029 | sous le seuil (bornes) | atteinte observable à sa barre | asymétrie horaire ; composition des journées non contrôlée |
| ANO-C5-003 | C5 (C5-08) | retracement +60 min après première atteinte plus faible avant 13:00 | ratio 0,615 [0,538 ; 0,732] (7,92 vs 12,88 bp) | q 0,0029 | marqué | atteinte et heure connues à la barre | **composition** : heure confondue avec session et activité |

## 2. Découvertes négatives, sous-seuil et non évaluables (conservées, non candidates)

- **C2** : T02, T04, T08, T09, T15, T16, T23 négatifs/non concluants ;
  T05 et T15 significatifs sous le seuil matériel ; T06 complément
  mécanique de T01 ; T24 contexte biaisé par construction.
- **C3** : NEG-C3-001…009 (dont trois significatifs sous le seuil
  matériel : −1,3 pt, +4,0 pts, ratio 0,91).
- **C4** : C4-02…C4-07 négatifs ; C4-01 et C4-06 **non éligibles**
  (9 et 5 fenêtres) ; **C4-10 significative sous le seuil matériel**
  (état de queue de la veille et fréquence d'extrêmes du jour :
  +0,75 [0,52 ; 0,99] en proportion publiée, q 0,0037) — pas de fiche.
- **C5** : C5-02, 04, 05, 07 négatives ; C5-03 et C5-09 non éligibles ;
  **C5-10 structurellement non évaluable** (aucune journée 1 440/1 440).
- **C6** : aucune fiche ; C6-01 non éligible ; **C6-02 significative
  sous le seuil matériel** (+0,0208 d'ER, q 0,0057) ; C6-03/04/05
  négatives. Fait descriptif : journées minute massivement oscillantes.
- **C7** : aucune fiche ; I-01 et I-04 négatives ; I-02 et I-05 **non
  évaluables (composition)** ; **I-03 significative et matérielle mais
  déclassée par le contrôle de composition** (ratio 1,449, q 0,0057) —
  conservée comme association sensible à la composition, pas candidate.
- **C8** : aucune fiche ; FJ-01, FJ-03, FJ-04 négatives ; **FJ-02
  significative sous le seuil matériel** (−3,74 bp, q 0,0057) ; FJ-05
  **non évaluable** (graphe de dépendance : 12 grappes, composition).
- Modèles gelés en service, hors catalogue ANO : F3 HAR-RV et F7
  (prévision/classification de volatilité, jamais directionnels) ;
  directionnel réfuté (phases antérieures). CARRY BTC/ETH : hors
  périmètre (XAU/USD exclusivement en Phase 9).

## 3. Tableau central de progression (extrait ; détail dans le registre CSV)

Toutes les fiches positives sont **J1**. Aucune n'est M1 au sens fort
(mécanisme behavioral documenté) sauf ANO-C4-002 dont le « mécanisme »
est mécanique et disqualifiant pour l'usage. Preuve nécessaire pour
avancer, par fiche sélectionnée : voir `SELECTION_CANDIDATES.md`.
Prochains blocages dominants : (i) amplitudes en bp souvent de l'ordre
ou en dessous des coûts de transaction ; (ii) plusieurs fiches fondées
sur des étiquettes rétrospectives ou des profondeurs finales — seules
leurs versions causales (T0) sont éligibles ; (iii) aucune confirmation
indépendante n'existe pour aucune fiche (IS déjà exploré ; holdout
scellé).
