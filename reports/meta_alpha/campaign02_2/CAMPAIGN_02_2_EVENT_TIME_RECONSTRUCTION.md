# CAMPAGNE 2.2 — RECONSTRUCTION TEMPORELLE ET VALIDITÉ DES VARIABLES

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Campagne autorisée
seq 169, méthode gelée seq 170. Aucune promotion J2, zéro budget expérimental,
holdout intact, 36 cellules gelées, FRED suspendue. Les anciennes associations
(98,2 % contre 65,8 % ; 26,9 % contre 80,7 %) sont **conservées telles quelles**
dans le registre historique, étiquetées « résultats rétrospectifs conditionnés par
des variables futures » ; elles ne sont ni supprimées ni réutilisables comme
signaux d'entrée.

## 1. Ce que la reconstruction établit

Chaque dépassement et chaque cassure sont désormais décrits par une **ligne du
temps** : instantanés à T0 (clôture de la barre de franchissement), T+1, T+3 et
T+5 minutes, où chaque variable n'utilise que les barres connues jusqu'à
l'instantané (profondeur initiale, profondeur maximale *atteinte jusqu'ici*,
position par rapport au niveau, durée déjà passée au-delà, volatilité réalisée,
spread, amplitude déjà parcourue), et où toutes les conséquences (réintégration
ultérieure, temps restant, extension supplémentaire, excursions favorable et
adverse, position à +15/+30/+60 après l'instantané) sont mesurées **strictement
après**. L'audit variable par variable est dans
`CAMPAIGN_02_2_LOOKAHEAD_AUDIT.md` : il confirme que la profondeur historique
était la seule variable de classification contaminée des campagnes 1–2.1, et que
les seuils EV7 (P95 décennal) ne sont pas causaux — déjà consigné seq 160.

## 2. État d'extraction — écrit sans détour

L'extraction complète a été tentée trois fois. Premier run monolithique :
chargement partiel silencieux (777 journées, 2010 → mars 2014), détecté par
contrôle de couverture et **refusé comme base de livraison** ; une garde
(≥ 200 journées par lot) rend désormais ce mode d'échec explicite. Deuxième run :
timeout CI à 350 minutes — le chargement partition par partition via Drive est
devenu trop lent. Troisième dispositif, toujours en place : matrice de 8 lots
Kaggle, moteur `campaign022_engine.py`, slug propriétaire corrigé
(`shalom5123/...`). Diagnostic d'accès consigné dans les journaux commités
(`timeline_parts/*_log.txt`) : **l'API Kaggle renvoie 403** avec les identifiants
actuels (défaillance connue de la librairie 1.6.17, déjà rencontrée seq 141), le
repli direct HTTPS ajouté au moteur échoue de même, et **Drive refuse
temporairement les téléchargements** (« Too many users have viewed or downloaded
this file recently ») après les téléchargements répétés de la journée. Aucune
donnée n'a été fabriquée pour combler ce blocage, conformément à la doctrine du
programme.

En conséquence, les statistiques d'instantanés du §3 sont calculées sur
l'extraction partielle **validée ligne à ligne** du premier run : 12 144 épisodes
de dépassement (777 journées, 2010-01-04 → 2014-03-11, ère 2010–13 et début
2014–16), soit le périmètre où la comparaison ancien/nouveau est la plus utile
(c'est l'ère où les anciennes associations étaient les plus fortes). Elles sont
livrées comme **résultats de reconstruction sur périmètre restreint**, pas comme
baselines décennales ; l'achèvement sur les 8 lots est une affaire d'accès aux
données, pas de méthode — le moteur corrigé et la garde de couverture sont
commités et n'attendent que le rétablissement du quota Drive ou des identifiants
Kaggle.

## 3. Ce que les instantanés montrent (périmètre restreint, descriptif)

À T0, la profondeur déjà atteinte (haut/bas de la seule barre de franchissement,
connue à sa clôture) trie déjà les issues, mais faiblement : réintégration
ultérieure de 90,6 % (tercile bas) contre 77,0 % (tercile haut) — à comparer aux
98,2/65,8 de la classification rétrospective. À mesure que l'instantané avance et
que le classeur absorbe du chemin, le tri se durcit : à T+5, 94,2 % contre
63,9 %. La lecture correcte est donc graduée : **une part réelle mais modeste de
l'ancienne association existe dès T0 ; le reste est le chemin lui-même qui se
résume**. Les grandeurs médianes par instantané (profondeur atteinte 2,3 bp à T0
→ 5,8 bp à T+5 ; extension supplémentaire médiane décroissante 11,6 → 6,4 bp ;
excursions favorable/adverse quasi symétriques ~12–13 bp) sont dans les bruts
`CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv`. Les positions à +60 ne sont définies que
pour T0 (fenêtre bornée à T0+60 par le gel) — les cellules vides des instantanés
ultérieurs sont des bornes de construction, pas des manquants.

Côté cassures (extraction partielle : 1 328 retests confirmés) : la profondeur
atteinte **au moment du retest** vaut en médiane 11,9 bp — c'est la variable
causale qui remplace, pour toute suite éventuelle, le maximum sur 60 minutes ;
le délai de retest médian est de 1 minute ; 53,8 % des retestées sont encore
au-delà du niveau 60 minutes après le retest, tandis que 77,6 % connaissent au
moins une clôture de retour du bon côté avant T0+60 (invalidation temporaire ou
définitive confondues — le brut les distingue par la position finale, pas par un
étiquetage forcé). Les cassures sans retest et les issues censurées restent des
catégories séparées, comme gelé.

## 4. Réconciliation des p-valeurs

`CAMPAIGN_02_2_PVALUE_RECONCILIATION.csv` publie, pour les 24 comparaisons :
ancienne p (exécution fautive), nouvelle p, p BY, intervalle, conclusions avant
et après correction, et la fiche ANO concernée. La conclusion avant correction
était uniformément « non concluant » (artefact) ; après correction, 14 fiches
ANO-C2-001 à 014 existent. Les conclusions ne dépendent d'aucune modification
rétroactive du protocole : plan hashé seq 164 inchangé, seule la formule de p a
été réparée, à données et graine identiques (détail : audit Campagne 2.1).

## 5. Ce que cette livraison ne fait pas

Aucun test formel nouveau (gel seq 170) : les gradients par tercile ci-dessus sont
descriptifs, sur périmètre restreint, sans p-valeur ajoutée. Aucune promotion,
aucune direction, aucun signal. La reconstruction décennale complète reste à
achever quand l'accès aux partitions sera rétabli ; les fiches concernées
(ANO-C2-001/002/004) portent déjà la requalification de la Campagne 2.1, que la
présente reconstruction confirme et précise sans l'aggraver ni l'effacer.

**STATUT : CAMPAGNE 2.2 LIVRÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
*Réserve écrite : statistiques d'instantanés sur périmètre restreint
(2010 → mars 2014) pour cause de blocage d'accès aux données, documenté au §2 ;
achèvement décennal en attente du rétablissement Kaggle/Drive.*

*Annexes : `CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv` et
`CAMPAIGN_02_2_BREAKOUT_TIMELINE.csv` (extractions partielles validées, premier
run), `timeline_parts/` (moteur par lots, journaux et gardes),
`CAMPAIGN_02_2_PVALUE_RECONCILIATION.csv`, `CAMPAIGN_02_2_LOOKAHEAD_AUDIT.md`,
`CAMPAIGN_02_2_DATA_QUALITY.md`. Chaîne : seq 169–170 (mission, gel), extraction,
livraison. FRED suspendue ; anciennes fiches immuables.*
