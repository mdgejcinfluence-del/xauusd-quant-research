# CAMPAGNE 2 — DÉTECTION CONDITIONNELLE DES ANOMALIES COMPORTEMENTALES

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Campagne autorisée
seq 161 ; plan de détection gelé avant calcul (seq 162–164, 24 comparaisons fermées,
`CAMPAIGN_02_DETECTION_PLAN.md`, sha256 chaîné). Zéro essai stratégique, budgets
inchangés (tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12),
holdout intact, 36 cellules gelées, FRED suspendue, ouvertures d'Asie toujours
**NON MESURÉES**, F7 hors périmètre (série réelle du modèle absente du dépôt).
**Aucune fiche ANO-C1 modifiée** ; J2 et J3 non autorisées, aucune promotion.

## 1. Ce que la détection a trouvé — et ce qu'elle n'a pas trouvé

Sur 24 comparaisons préenregistrées, **14 écarts franchissent la règle gelée**
(p_BY < 0,05 après correction de Benjamini-Yekutieli, écart matériel, effectifs
suffisants, cohérence d'ère) et deviennent des fiches **J1 candidates nouvelles**
ANO-C2-001 à 014. Huit comparaisons ne franchissent pas la règle et sont conservées
dans `CAMPAIGN_02_NEGATIVE_RESULTS.md` ; une est un complément mécanique (T06), une
est classée contexte biaisé par construction (T24). La lecture honnête de ce bilan :
la plupart des écarts détectés sont des **différences de contexte** (le régime F3
ordonne les amplitudes, les ères dérivent, les sessions ont des profils propres) —
c'est exactement ce que « référence conditionnelle » signifie : ces fiches disent où
le comportement normal *change de valeur*, pas où il « casse ». Une vraie anomalie,
au sens de la doctrine, devrait subsister *à l'intérieur* d'un contexte homogène ;
plusieurs fiches ci-dessous devront donc être relues comme des paramètres de
référence datés plutôt que comme des bizarreries.

## 2. Les écarts les plus marqués

**La profondeur d'un dépassement décide de son anatomie (ANO-C2-001/002, T01/T03).**
Dans le tercile de profondeur basse, 98,2 % des dépassements réintègrent sous
60 minutes ; dans le tercile haut, seulement 65,8 % (+32,4 points, IC [31,6 ; 33,3],
cohérent dans les trois ères). Et parmi les réintégrés, le délai médian passe de
2 minutes (peu profond) à 3 minutes (profond). Le « 85 % » de la campagne 1 mélangeait
donc deux populations : des frôlements quasi toujours résorbés et des traversées
franches qui, un tiers du temps, ne reviennent pas dans l'heure. Toute référence
future sur les dépassements doit être **conditionnée à la profondeur**.

**Après un retest, tout dépend de l'ampleur de la cassure (ANO-C2-004, T10).**
C'est l'écart le plus fort de la campagne : prix encore au-delà du niveau à
+60 minutes dans **26,9 %** des retests de cassures peu profondes contre **80,7 %**
pour les cassures profondes (−53,8 points, cohérent sur les trois ères). Le « 55 % »
de la campagne 1 était donc, lui aussi, une moyenne de deux mondes. Lecture
obligatoire, écrite dans la fiche : cette fréquence est conditionnée sur le retest
réalisé et sur l'amplitude déjà parcourue ; elle ne dit rien de prévisible à
l'instant de la cassure, et **aucune direction ne lui est attribuée**.

**Les impulsions « tiennent » différemment selon l'époque, le régime et la session
(ANO-C2-005/006/007, T11/T12/T13).** Retour contraire complet : 49,3 % en 2010–13
contre 40,2 % en 2017–20 ; retracement médian de 75,8 % (régime F3 bas) contre
93,7 % (régime haut) ; retour complet moins fréquent après une impulsion asiatique
(42,1 %) qu'américaine (48,4 %). Aucun de ces écarts n'est un signal : ils
paramètrent la référence « ce qu'une impulsion fait d'habitude, ici et maintenant ».

**Le régime ordonne, l'époque dérive (ANO-C2-008 à 013).** Range post-consolidation
×0,86 en régime bas ; expansions post-compression de 17,9 bp (2010–13) à 12,6 bp
(2017–20) ; première heure new-yorkaise de 43,5 à 28,9 bp entre ères extrêmes ;
extrêmes d'ouverture de New York de 5,6 % (régime bas) à 18,8 % (régime haut) ;
spread post-ouverture de Londres amélioré de 2,40 à 1,87 bp en ère récente. Ce sont
des **paramètres de baseline datés**, précieux pour la détection future (une anomalie
devra être mesurée contre *sa* ère), et sans aucune valeur prédictive revendiquée.

**Les extrêmes de session ne naissent pas au même moment du cycle de session
(ANO-C2-014, T22)** : dernier tiers de session dans 41,6 % des cas en Asie contre
14,4 % à New York — reflet des profils d'activité (l'Asie culmine tôt, New York
charge le début d'après-midi UTC), fiche de contexte autant que d'anomalie.

## 3. Anomalies ou queues de distribution ?

La règle gelée tranche mécaniquement, et le rapport la double d'une lecture :
- **Queues confirmées comme telles** : T05 (réintégration Londres vs New York,
  −2,2 points : significatif au bootstrap mais sous le seuil matériel de 5 points —
  un effet réel et sans importance descriptive), T15 (+11,7 % de range
  post-consolidation entre ères : significatif mais sous le seuil de ratio 1,15),
  T02/T04/T09/T16/T23 (intervalles couvrant zéro ou effets minuscules).
- **Paramètres de référence conditionnels** (la majorité des 14 fiches) : écarts
  forts mais explicables par la structure du contexte — ils *définissent* le normal
  local.
- **Candidates à mécanisme inconnu** (à documenter avant toute J2 éventuelle) :
  ANO-C2-001/002 (anatomie par profondeur) et ANO-C2-004 (issue de retest par
  profondeur de cassure) — les deux écarts les plus amples, cohérents par ère, sans
  explication articulée à ce stade. Aucune n'est promue : la promotion J2 exige une
  autorisation distincte et une confirmation chronologique disjointe.

## 4. Censure et dépendances — traitées, pas contournées

Les 5 421 dépassements sans réintégration sous 60 min (15,1 %) sont traités comme
**censurés à droite**, jamais comme des échecs ni des manquants aléatoires : le test
T06 (leur complément mécanique) le rappelle, et la fiche ANO-C2-001 publie les deux
taux. Les intervalles sont calculés par bootstrap **par grappes jour×niveau**
(les impulsions d'une même journée ne comptent pas comme indépendantes). T24
(amplitude après retest vs après réintégration, ratio 1,60) est conservée comme
fiche de **contexte biaisé** : les deux bras n'ont pas la même distribution
d'amplitude de départ, la comparaison naïve est interdite par le plan lui-même.

## 5. Ce que cette campagne ne dit pas

Aucune des 14 fiches ne comporte de direction, de probabilité exploitable, de PnL ou
de mécanisme. Les baselines conditionnelles chiffrées vivent dans
`CAMPAIGN_02_CONDITIONAL_BASELINES.csv` (24 lignes : effectifs, grappes, journées,
écarts, IC 95 %, p bruts et BY) ; l'audit de la procédure (y compris le bug de
p-valeur détecté et corrigé avant livraison, et l'intervalle dégénéré de T03 causé
par la granularité minute) est dans `CAMPAIGN_02_STATISTICAL_AUDIT.md` ; les limites
dans `CAMPAIGN_02_DATA_LIMITATIONS.md`. **La décision de promouvoir une anomalie en
J2 sera prise séparément** — elle n'appartient pas à cette livraison.

**STATUT : CAMPAGNE 2 LIVRÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**

*Annexes : `CAMPAIGN_02_ANOMALY_REGISTER.csv` (19 fiches : 14 nouvelles J1 +
5 ANO-C1 reproduites sans modification), `CAMPAIGN_02_CONDITIONAL_BASELINES.csv`,
`CAMPAIGN_02_STATISTICAL_AUDIT.md`, `CAMPAIGN_02_NEGATIVE_RESULTS.md`,
`CAMPAIGN_02_DATA_LIMITATIONS.md`, plan gelé `CAMPAIGN_02_DETECTION_PLAN.md`.
Chaîne : seq 161 (mission), 162–164 (plan gelé + hash), calcul local sur bruts
commités des campagnes 1/1.1, livraison. FRED suspendue.*
