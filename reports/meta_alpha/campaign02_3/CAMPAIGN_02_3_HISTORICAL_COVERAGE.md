# CAMPAGNE 2.3 — COUVERTURE HISTORIQUE ET VALIDATION TEMPORELLE

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Campagne autorisée
seq 173, sonde d'accès gelée seq 174. Aucune promotion J2, zéro budget
expérimental, holdout intact, 36 cellules gelées. La relation T0 est conservée
sous sa formulation qui fait foi : **« Association conditionnelle fondée sur des
variables disponibles à T0, sans anticipation temporelle. »**

## 1. Le critère de fin, appliqué honnêtement

La mission demandait : matrice de couverture précise + méthode reproduite sur
toutes les données IS disponibles. La matrice est livrée (§2, et
`CAMPAIGN_02_3_PARTITION_INVENTORY.csv`, 348 partitions). La reproduction sur
« toutes les données disponibles » a une réponse factuelle : **les données IS ne
sont actuellement disponibles nulle part où ce programme peut les lire**. La
sonde minimale gelée (seq 174, une requête de listage Kaggle, un seul fichier
Drive, rien d'autre) a répondu :

- Kaggle, librairie officielle : **403 Forbidden** ; endpoint HTTPS direct,
  Bearer puis basic auth : **403, 403**. Le slug propriétaire est pourtant
  correct (`shalom5123/xauusd-is-b01`) depuis la correction seq 168.
- Drive, un fichier unique avec contrôle de taille : **échec** (rc=1, fichier
  absent), refus de quota déjà documenté seq 171/172.

Conformément à la sonde gelée, aucune extraction n'a été relancée et aucun
téléchargement supplémentaire n'a été tenté : multiplier les essais aggraverait
le refus Drive et ne changerait pas un 403 d'authentification. L'achèvement de
la couverture historique est donc **en attente d'une action propriétaire** (§4),
et cette limitation est conservée explicitement, comme le critère de fin
l'exige.

## 2. Matrice de couverture par période

| Période | État | Preuve |
|---|---|---|
| 2010–2014 (référence) | **Reproduite** : 11 513 épisodes T0 en ère 2010–13 (extraction partielle validée seq 171) | `CAMPAIGN_02_2_OVERSHOOT_TIMELINE.csv` |
| 2014–2017 | **Partielle seulement** : 631 épisodes, janvier–mars 2014 (48 journées) ; 2014-04 → 2017 non extrait | Idem |
| 2017–2020 | **Lacune non résolue** : 0 épisode reconstruit ; partitions présentes à l'inventaire (56 partitions IS non extraites, tous lots confondus) mais **non accessibles** à la date de la sonde | Inventaire + `ACCESS_PROBE.txt` |
| 2020–2026 | **Hors périmètre IS autorisé** : le corpus IS se clos le 2020-01-20 (borne gelée du programme) ; les données postérieures relèvent d'autres périmètres scellés (NR/holdout), non sollicités et non ouverts. Ce n'est pas une lacune à combler dans cette campagne, mais une frontière d'autorisation | Doctrine du programme, seq 155 |

Inventaire : 348 partitions recensées ; 282 dans le périmètre IS (8 lots Kaggle,
intégrité vérifiée à la migration, seq antérieures) ; 66 hors IS-282 en métadonnées
seules, jamais touchées. Attribution par partition du périmètre extrait : non
établie (les partitions ne sont pas des tranches chronologiques pures) — écrit
dans l'inventaire plutôt qu'inventé.

## 3. Réplication temporelle sur le périmètre disponible

`CAMPAIGN_02_3_TEMPORAL_REPLICATION.csv` reproduit la méthode gelée (mêmes
définitions, instants, fenêtres, bootstrap par grappes 2 000, graine 20261113)
par ère disponible, avec les terciles du périmètre (seuils au §
`CAMPAIGN_02_3_TERCILE_THRESHOLDS.md`) :

- **Ère 2010–13** (référence) : contraste profondeur atteinte T0 BAS−HAUT =
  **+13,6 points [11,9 ; 15,3]** (90,7 % contre 77,1 % ; 3 798/3 863 épisodes,
  635/704 journées, 1 037/1 367 grappes).
- **Début 2014–16** (48 journées seulement) : contraste **+13,7 points
  [5,8 ; 21,5]** — même valeur centrale, intervalle large : cohérent, non probant
  à lui seul, et il n'est pas présenté autrement.
- **Ère 2017–20** : ligne « NON MESURÉ — accès bloqué », conservée au fichier.
- **2020–2026** : ligne « HORS PÉRIMÈTRE IS AUTORISÉ », conservée.

Il n'était pas exigé que les chiffres restent identiques à 2010–2014 ; sur ce qui
est mesurable, ils le sont en valeur centrale, avec l'incertitude qui convient à
48 journées. La stabilité réelle sur 2017–2020 reste **inconnue** — c'est
exactement la question que la restauration de couverture devra trancher, sans
qu'aucun paramètre ne soit ajusté entre-temps.

## 4. Restauration des accès — ce qui dépend du propriétaire

**Kaggle (à ne pas confondre avec FRED, qui reste suspendue pour sa propre
rotation).** Procédure : sur kaggle.com, compte `shalom5123` → Settings → API →
« Create New Token » (ou régénération de la clé héritée) ; injecter les nouvelles
valeurs **uniquement** dans les secrets CI du dépôt (`KAGGLE_USERNAME`,
`KAGGLE_KEY`) ; ne jamais les afficher, journaliser ou committer — les workflows
ne lisent que `${{ secrets.* }}`. Vérification avant extraction : relancer la
sonde (`campaign023_probe.yml`, une requête de listage) ; n'autoriser la matrice
d'extraction que si elle répond OK. Le diagnostic actuel (403 sur trois routes,
slug correct) désigne les identifiants, pas le code : la librairie 1.6.17 avait
déjà produit ce 403 dans l'histoire du programme (seq 141).

**Drive.** Le refus est temporaire (quota de consultation/téléchargement par
fichier, aggravé par les tentatives répétées) ; règle maintenue : **ne pas
multiplier les téléchargements**. Si Kaggle reste indisponible après
rétablissement du quota, reprise en **un seul passage** par la matrice de lots
existante (chaque lot = un dataset ou ses replis Drive, garde ≥ 200 journées,
journal commité), en réutilisant d'abord l'extraction partielle déjà commitée
(2010 → 2014-03) et en ne produisant que les périodes manquantes.

## 5. Ce qui reste vrai et ce qui reste ouvert

Vrai et clos : l'inventaire des partitions, la matrice des périodes, la
réplication de référence 2010–13 et sa cohérence sur le fragment 2014, les seuils
de terciles documentés au bp près. Ouvert et écrit comme tel : la couverture
2014-04 → 2020, subordonnée à la régénération des identifiants Kaggle ou au repos
du quota Drive — deux actions qui ne sont pas du ressort du code. Aucune
promotion prédictive n'est automatique ni demandée par cette livraison.

**STATUT : COUVERTURE HISTORIQUE ÉTENDUE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
*Réserve écrite jointe : l'extension au-delà de mars 2014 est bloquée par l'accès
aux données (sonde seq 174) ; la matrice et la réplication de référence sont,
elles, complètes et livrées.*

*Annexes : `CAMPAIGN_02_3_PARTITION_INVENTORY.csv` (348 partitions),
`CAMPAIGN_02_3_TEMPORAL_REPLICATION.csv`, `CAMPAIGN_02_3_TERCILE_THRESHOLDS.md`,
`CAMPAIGN_02_3_DATA_QUALITY.md`, `ACCESS_PROBE.txt`. Chaîne : seq 173–174
(mission, sonde gelée), sonde, livraison. FRED suspendue (procédure distincte) ;
budgets inchangés ; anciennes fiches ANO immuables.*
