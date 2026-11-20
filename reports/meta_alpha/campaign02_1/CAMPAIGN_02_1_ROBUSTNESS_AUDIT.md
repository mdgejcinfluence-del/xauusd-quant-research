# CAMPAGNE 2.1 — AUDIT DE ROBUSTESSE DES DEUX ANOMALIES MAJEURES

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Campagne autorisée
seq 166 ; famille nouvelle R01–R12 gelée seq 167 (correction BY interne à la
famille, distincte des 24 tests de Campagne 2, **non modifiés**). Aucune promotion
J2. Zéro budget expérimental, holdout intact, Phase 12 gelée, FRED suspendue.

## 1. Le résultat principal de cet audit tient en une phrase

Les deux « anomalies majeures » de la Campagne 2 sont des écarts descriptifs réels
**sur une variable qui n'existe pas encore au moment où l'événement commence** :
la « profondeur » du dictionnaire gelé est l'excursion maximale du prix au-delà du
niveau pendant les **60 minutes qui suivent le début** du dépassement (code moteur
commité, `campaign01_engine.py` : fenêtre `i:i+61`, maximum des hauts/bas sur
toute la fenêtre, y compris après une éventuelle réintégration). Classer les
épisodes par cette profondeur, c'est classer les chemins par ce qu'ils ont fait
ensuite. Une partie de l'écart mesuré est donc **mécaniquement construite** : un
chemin qui s'éloigne beaucoup pendant l'heure est, par construction, un chemin qui
souvent n'est pas revenu. L'audit ci-dessous sépare ce qui survit à cette critique
de ce qui n'y survit pas.

## 2. Anomalie A — profondeur et réintégration

**Définitions exactes (code).** Déclenchement : première barre M1 (à partir de
08:00 UTC) dont la clôture franchit le niveau (extrême de la session d'Asie du jour
ou de la veille). Profondeur : excursion maximale au-delà du niveau sur les 61
barres suivantes, en bp. Réintégration : première clôture revenue du bon côté,
sous 60 min ; sinon **censure à droite** (5 421 épisodes, 15,1 %, traités comme
censurés partout ici). Profondeur *initiale* (distance de la clôture de
déclenchement) : **non stockée** ; profondeur *avant réintégration* : **non
séparable** dans le brut (le maximum inclut l'après-réintégration éventuelle). Ces
deux manques sont écrits, pas contournés.

**Ce qui survit.** L'association descriptive entre profondeur maximale et issue est
massive et stable : réintégration 98,2 % (tercile bas) contre 65,8 % (haut) ;
sensibilité aux bornes confirmée — quartiles extrêmes : écart **+37,2 points**
(R02), partage à la médiane : **+23,8 points** (R03) ; effet présent dans chaque
contexte séparé : Londres +37,5 (R04), New York +30,3 (R05), régime F3 bas +35,6
(R06), haut +30,5 (R07) ; profondeur médiane des censurés **30,8 bp** contre 8,8 bp
pour les réintégrations en ≤ 3 min (R08, ratio 3,50). Distributions : profondeur
médiane plus forte en ère ancienne (14,8 → 9,7 bp) et en régime haut (15,0 contre
9,2 bp en bas), taux de réintégration pourtant quasi constant partout (~85 %) —
voir `CAMPAIGN_02_1_OVERSHOOT_ANALYSIS.csv`. La durée au-delà trie la profondeur
de façon monotone : 8,8 bp (≤ 3 min), 10,7 (4–15), 15,2 (16–60), 30,8 (censurés).

**Ce qui ne survit pas.** Le test causal R01 classe les dépassements par la seule
information disponible au déclenchement : la clôture de la barre de franchissement
dépasse-t-elle déjà le niveau de plus de 5 bp (cassure initiale) ou non ? Écart de
réintégration : **−0,8 point** [−2,9 ; +1,1], p_BY = 0,13 — **rien**. Autrement
dit, au moment où un dépassement commence, son ampleur initiale ne dit presque
rien de sa réintégration ; c'est le chemin ultérieur, résumé par la profondeur
maximale, qui « explique » l'issue — en partie tautologiquement.

**Verdict A.** Mécanisme **observé** : les chemins qui s'éloignent loin et
longtemps reviennent moins dans l'heure (c'est presque une identité de chemin).
Mécanisme **plausible** : deux populations de franchissements (frôlements de
liquidité contre traversées informées) — *non démontré*, car le test qui le
soutiendrait (classification causale) est négatif. En l'état, ANO-C2-001/002 restent
des fiches J1 descriptives **requalifiées** : elles décrivent l'anatomie des
chemins après coup, elles ne décrivent pas un comportement prévisible à
l'événement. Aucune fiche n'est modifiée rétroactivement ; la présente
requalification est consignée ici et en chaîne.

## 3. Anomalie B — amplitude des cassures et après-retest

**Définitions exactes.** Cassure : dépassement dont la clôture de déclenchement
franchit le niveau de plus de 5 bp (observable immédiatement, elle). Retest :
première barre suivante (sous 60 min) touchant le niveau à 0,5 bp près en restant
du côté cassé ; délai cassure→retest médian **1 minute** (le retest est le plus
souvent immédiat). « Encore au-delà à +60 » : clôture 60 min après le retest,
comparée au niveau. L'« amplitude » utilisée en T10 est la même profondeur
maximale sur 60 min que pour A — donc mesurée sur une fenêtre qui **chevauche**
celle de l'issue (retest + 60 min) : même contamination par le futur, aggravée.

**Ensemble vs sous-échantillon (à ne jamais confondre).** Toutes cassures :
3 957. Retestées : 3 128 (79 %). Non retestées : 607 grappes distinctes dont la
profondeur médiane est de 50,7 bp (contre 24,3 pour les retestées) et qui ne
réintègrent sous 60 min que dans **8,4 %** des cas — ce sont les traversées
franches qui ne reviennent pas toucher le niveau. R10 le chiffre sur l'ensemble
des cassures : réintégration de 72,8 % (retestées) contre 8,4 % (non retestées).
Présenter le « 55 % encore au-delà » (retestées seules) comme une propriété des
cassures serait une erreur de sélection : sur toutes les cassures, l'issue
dominante des non-retestées est la continuation sans retour au niveau.

**Robustesse de l'écart T10.** Sensibilité quartiles : 24,1 % (Q1) contre 85,2 %
(Q4), écart −61,1 points (R12) ; pas d'effet du délai de retest (R09 : −0,9 point,
NS) ni de la session (R11 : +2,0 points, NS) ; stabilité par ère de l'issue globale
(54,7 / 54,9 / 56,3 %). Mais le classeur reste la profondeur maximale, contaminée :
l'amplitude *à l'instant du retest* (excursion atteinte avant le retour au niveau)
n'est pas stockée séparément, et c'est elle — pas le maximum sur l'heure — qui
serait la variable causale d'une éventuelle fiche J2. **Verdict B** : écart
descriptif robuste aux bornes, **mécanisme inconnu**, classification non causale ;
la fiche ANO-C2-004 est requalifiée de la même façon que A, sans modification de
son texte d'origine.

## 4. Ce qu'il faudrait pour aller plus loin (non exécuté)

Une ré-extraction causale : stocker, pour chaque dépassement, la distance initiale
de clôture, l'excursion maximale *avant* réintégration ou avant retest, et l'issue
mesurée ensuite. Alors seulement la question « la profondeur connue à l'instant t
trie-t-elle l'issue après t ? » devient testable sans tautologie. Cette étape
relève d'une autorisation distincte ; la promotion J2 reste interdite à ce stade
et, sur la base de R01, **rien dans la présente livraison ne la suggère**.

**STATUT : CAMPAGNE 2.1 LIVRÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**

*Annexes : `CAMPAIGN_02_1_OVERSHOOT_ANALYSIS.csv`,
`CAMPAIGN_02_1_BREAKOUT_ANALYSIS.csv`, `CAMPAIGN_02_1_ROBUSTNESS_TESTS.csv`
(famille R), `CAMPAIGN_02_1_SELECTION_BIAS.md`, `CAMPAIGN_02_1_PVALUE_AUDIT.md`.
Registre historique inchangé (aucune ancienne version écrasée).*
