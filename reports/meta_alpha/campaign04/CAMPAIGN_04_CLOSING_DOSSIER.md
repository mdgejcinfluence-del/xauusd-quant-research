# CAMPAGNE 4 — DOSSIER FINAL DE CLÔTURE (COMPLÉMENT seq 203)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Ce dossier
clôt la campagne 4 sans **aucun nouveau calcul sur les données sources** :
toutes les valeurs ci-dessous sont recopiées ou tabulées depuis les sorties
déjà produites et livrées (seq 202) — bruts quotidiens et de sessions,
catalogues d'épisodes et de transitions, tableau des dix comparaisons. Il
ne modifie ni les chiffres, ni les fiches, ni les rapports déjà livrés ; il
les réconcilie, corrige une formulation d'interprétation, et qualifie les
candidates. Aucune fiche historique des campagnes 0 à 3 n'est touchée ; la
sensibilité ANO-C2-003/006/008/012 n'a pas été recalculée.

## 1. Réconciliation des effectifs (1 281 / 286 / 994)

Les trois nombres ne portent pas sur le même objet, et leur articulation
est exacte :

- **1 281** = nombre d'**épisodes** d'état courant (`CAMPAIGN_04_EPISODES.csv`,
  1 281 lignes) sur 2 532 journées classées.
- **1 280** = nombre de **transitions entre épisodes consécutifs**
  (`CAMPAIGN_04_TRANSITIONS.csv`, 1 280 lignes). Deux épisodes adjacents
  définissent exactement une transition ; 1 281 épisodes en chaîne en
  définissent donc 1 280. Aucune transition n'est fabriquée à travers les
  journées NON_CLASSE : celles-ci (40) sont intégralement situées dans la
  zone d'amorçage initiale (les états commencent à l'indice 40,
  2010-03-01), avant le premier épisode — il n'y a donc aucun trou
  ultérieur dans la chaîne.
- **286 + 994 = 1 280** : « confirmée » et « non confirmée » qualifient
  les **transitions** (la suivante persiste ou non 3 journées), jamais les
  épisodes. La formulation de la cartographie est ainsi réconciliée sans
  changer aucun chiffre.

**Statut explicite du dernier épisode** (1 281ᵉ ligne du fichier produit) :
épisode **BAS d'une seule journée, le 2019-12-16**, dernière journée du
corpus, marqué `censure_bord = True`. Trois conséquences, toutes déjà
appliquées dans les sorties : (i) sa durée (1 jour) est **tronquée par la
fin du corpus** et exclue des médianes de durées (règle des bords) ;
(ii) il est la cible de la 1 280ᵉ et dernière transition (HAUT → BAS,
candidate le 2019-12-16), classée **non confirmée par censure de bord** :
sa persistance observée est de 1 jour, faute d'observation au-delà du
corpus — ce n'est ni une rechute observée ni une confirmation manquante
de peu, c'est une impossibilité d'observation, et le catalogue la
conserve comme telle ; (iii) il n'a, par construction, **aucune transition
sortante**. Symétriquement, le premier épisode (BAS, 7 jours,
2010-03-01 → 2010-03-09) n'a aucune transition entrante. Aucun épisode
n'est donc « perdu » : la différence 1 281 − 1 280 est la propriété
arithmétique d'une chaîne, et le dernier maillon est intégralement
identifié ci-dessus.

## 2. Interprétation F3 corrigée (la discordance de 60,2 %)

Le chiffre est conservé comme résultat descriptif. En revanche, toute
formulation suggérant qu'il **démontrerait à lui seul** une incapacité de
F3 à prévoir le tercile de volatilité du lendemain est **corrigée et
retirée**, pour la raison précise que les deux classements comparés ne
reposent ni sur le même objet ni sur la même fenêtre de référence :

| | Classement « état-passé » | Classement « état courant » |
|---|---|---|
| Objet classé | **Prévision** F3 de la RV du jour (modèle HAR causal, valeur continue connue à la clôture de la veille) | **RV réalisée** du jour (mesure connue à la clôture du jour) |
| Seuils | Terciles causaux des prévisions des **250 journées précédentes** | Terciles causaux des RV des **60 journées précédentes** |
| Ce que mesure la discordance | L'écart conjoint entre (prévision vs réalisation) **et** entre (deux fenêtres de référence différentes) | — |

La discordance de 60,2 % mélange donc deux effets inséparables dans ce
seul nombre : l'erreur propre de prévision à horizon d'un jour, et le
décalage de construction entre une classification de prévisions à fenêtre
de 250 jours et une classification de réalisations à fenêtre de 60 jours.
La formulation faisant foi est : **« sur les 2 011 journées classées des
deux côtés, l'état réalisé (terciles des 60 journées précédentes) diffère
du tercile causal de la prévision F3 (terciles des 250 journées
précédentes) dans 60,2 % des cas ; ce taux décrit l'écart entre ces deux
classements tels que définis, et ne constitue pas, à lui seul, une mesure
de la capacité prédictive de F3, laquelle relève de ses critères propres
(QLIKE/Mincer-Zarnowitz sur la valeur continue, gelés seq 75 et non
rejugés ici). »** Aucun diagnostic supplémentaire (par exemple une
discordance à fenêtres harmonisées) n'a été calculé : il exigerait une
validation distincte.

**Matrice de confusion et marginales** (tabulation des sorties déjà
produites — fichier quotidien livré ; aucune donnée source recalculée) :

| Prévision F3 (tercile causal 250 j) ↓ / État courant (terciles 60 j) → | BAS | MOYEN | HAUT | **Total (marginale)** |
|---|---|---|---|
| BAS | 382 | 263 | 249 | **894** |
| MOYEN | 235 | 166 | 142 | **543** |
| HAUT | 149 | 172 | 253 | **574** |
| **Total (marginale)** | **766** | **601** | **644** | **2 011** |

Accord : 39,8 % ; discordance : 60,2 %. Les marginales recoupent
`CAMPAIGN_04_STATE_STATS.csv` (état courant sur 2 572 journées : BAS 983,
MOYEN 752, HAUT 797, NON_CLASSE 40 ; F3 causal : BAS 894, MOYEN 543,
HAUT 574, NON_CLASSE 561 — les écarts avec la matrice tiennent aux
journées classées d'un seul côté).

## 3. Les dix comparaisons — tableau de clôture complet

Source : `CAMPAIGN_04_COMPARISONS.csv` (bootstrap par blocs mobiles de
20 journées avec recalcul des états, épisodes, transitions et fenêtres
dans chaque réplicat ; 2 000 réplicats valides pour les dix, 0 exclu ;
p bilatérales de bootstrap ; q = p corrigées **BY** sur la famille des
dix). Matérialité : 5 points (proportions et fréquences ×100), ratio 1,15
(médianes et taux), 0,10 (différence de médianes d'asymétrie, C4-06).

| ID | Statistique observée | IC95 (bootstrap) | p brute | q BY | n A / B | Matériel | Lecture de clôture |
|---|---|---|---|---|---|---|---|
| C4-01 | ratio RV +1–5 j →HAUT/→BAS = 1,38 | [1,62 ; 2,45]* | 0,0005 | 0,0037 | 9 / 5 transitions | oui | **NON ÉLIGIBLE** (seuil de 30 transitions non atteint ; statistique publiée à titre de transparence, non interprétable) |
| C4-02 | +0,18 point (fréq. extrêmes ×100) | [−0,04 ; +0,21] | 0,224 | 1,000 | 286 / 993 transitions | non | NÉGATIF |
| C4-03 | ratio durées HAUT/BAS = 0,50 | [0,50 ; 2,00] | 0,957 | 1,000 | 360 / 427 épisodes | oui (formel) | NÉGATIF |
| C4-04 | ratio retours par ère = 1,00 | [1,00 ; 2,00] | 0,479 | 1,000 | 131 / 115 épisodes | non | NÉGATIF |
| C4-05 | +9,4 points (parts rapides) | [−12,6 ; +15,8] | 0,828 | 1,000 | 84 / 137 transitions | oui (formel) | NÉGATIF |
| C4-06 | −0,04 (diff. médianes g1) | [−0,51 ; +0,56] | 0,811 | 1,000 | 9 / 5 transitions | non | **NON ÉLIGIBLE** (idem C4-01) |
| C4-07 | −1,1 point (discordance par ère) | [−3,3 ; +21,1] | 0,140 | 0,820 | 474 / 763 journées | non | NÉGATIF |
| C4-08 | ratio impulsions/jour HAUT/BAS = 2,68 | [1,66 ; 2,05]† | 0,0005 | 0,0037 | 797 / 983 journées | oui | **CANDIDATE J1** (§4) |
| C4-09 | −76,5 points (déphasage) | [−73,8 ; −60,9]† | 0,0005 | 0,0037 | 797 / 983 journées | oui | **CANDIDATE J1 AVEC AVERTISSEMENT MÉCANIQUE MAJEUR** (§4) |
| C4-10 | +0,75 point (fréq. extrêmes ×100) | [+0,52 ; +0,99] | 0,0005 | 0,0037 | 863 / 873 journées | **non** (< 5 points) | SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL |

\* Pour les ratios (C4-01, C4-03, C4-04, C4-08), les bornes publiées au
fichier sont celles de l'échelle du log-ratio exponentiée lorsque la
procédure les a produites ainsi ; elles sont recopiées sans retraitement.
† Bornes recopiées du fichier produit. L'intervalle de C4-01 illustre à
lui seul la non-éligibilité : il est calculé sur 9 et 5 fenêtres.

**La significative sous le seuil matériel** : C4-10 (persistance de la
fréquence d'extrêmes au lendemain d'un état de queue HAUT, +0,75 point
pour un seuil gelé de 5) — conservée, non fichée, seuil appliqué sans
exception. **Les cinq négatives** : C4-02, C4-03, C4-04, C4-05, C4-07.
**Les deux non éligibles** : C4-01 et C4-06 (9 et 5 fenêtres +1–5 j non
tronquées par la règle gelée de troncature à la prochaine candidate ;
effectifs publiés, lectures suspendues, aucune fenêtre élargie).

## 4. Qualification des deux candidates (limites faisant foi)

- **ANO-C4-001 (IMP-M5, C4-08)** — conservée comme **candidate J1
  descriptive contemporaine** : les journées d'état courant HAUT comptent
  2,68 fois plus d'impulsions IMP-M5 que les journées BAS (cohérent sur
  les 3 ères : 3,07 / 2,49 / 2,40). Limites : (i) l'état courant n'est
  connu qu'à la **clôture** du jour qu'il décrit — aucune antériorité,
  aucun usage à l'ouverture ; (ii) **risque de dépendance mécanique
  documenté** : la détection IMP-M5 compare chaque barre M5 à un seuil
  causal (quantile 90 des |r| des 60 jours calendaires précédents) qui
  s'adapte lentement, alors que la RV du jour est une mesure du même
  matériau de rendements — une journée de forte volatilité réalisée tend
  mécaniquement à produire davantage de barres dépassant un seuil hérité
  de journées plus calmes. L'association décrit donc, pour une part non
  quantifiée ici, la co-mesure du même phénomène d'amplitude plutôt que
  deux comportements indépendants ; (iii) aucune direction, aucun
  mécanisme, aucune exploitation. Aucune promotion J2/J3.
- **ANO-C4-002 (déphasage, C4-09)** — conservée **avec avertissement
  mécanique majeur** : elle ne doit pas être présentée comme une anomalie
  indépendante solidement établie. Le maximum de quatre états de session
  dépasse presque par construction le tercile journalier lorsque celui-ci
  est BAS ; la fiche quantifie surtout le fait que l'état journalier
  masque l'hétérogénéité interne des sessions. Aucune promotion J2/J3.

## 5. Diagnostics et traces des deux corrections

| Incident | Trace | Effet sur les résultats |
|---|---|---|
| Bug `skew` (run CI 44884286806) | Traceback commité dans `CI_LOG.txt` : `AttributeError: 'function' object has no attribute 'values'` (`Ju.skew` = méthode pandas) ; correctif `Ju['skew']` au moteur et à la synthèse, tests temporels reverdits, run propre 44884486846 (commit CI `d8d42c8`) | Aucun : l'échec précède toute production et toute consultation de résultat ; définitions inchangées |
| Unité du seuil matériel ×100 (C4-02, C4-10) | Premier passage appliquant 0,05 (unité des proportions) à des statistiques en points (fréquence ×100) ; corrigé à **5 points** conformément au gel ; consigné dans la cartographie §4 et `CAMPAIGN_04_DATA_QUALITY.md` | Statistiques, intervalles et p-values **inchangés** ; seule la lecture de C4-10 devient « significative sous le seuil matériel » (au lieu de candidate) ; C4-02 déjà négative |

## 6. Registre consolidé des limites et incidents de la campagne

Alternance rapide rendant les fenêtres post-confirmation rares (C4-01/06
non éligibles) ; durées d'épisodes discrètes de 1–2 jours (intervalles de
C4-03 discrets et larges) ; états relatifs aux 60 journées précédentes et
non niveaux absolus (RV absolue publiée dans les bruts) ; C4-08
contemporaine et partiellement mécanique (§4) ; C4-09 largement mécanique
(§4) ; discordance F3 mélangeant erreur de prévision et fenêtres de
référence différentes (§2) ; échelle journalière uniquement — rien n'est
affirmé sur des échelles plus lentes, non autorisées ; synthèse bootstrap
de ≈ 19 minutes tenue sans dégradation (2 000/2 000 réplicats valides).

## 7. Checkpoint et hashes complets

Hashes SHA-256 des fichiers de référence de la campagne (calculés à la
clôture, sur les fichiers tels que commités) — voir l'entrée de chaîne
seq 204 accompagnant ce dossier pour les valeurs complètes des livrables
de clôture ; hashes gelés avant exécution, revérifiés à la clôture :
dictionnaire v2 `0a615c54fa4b7b2c2980428c486571f76f1b29abc6ec892538940ed0e0f12824`,
dix comparaisons `4024eaaefc16031d813fe73a2effab2d648e60d6172c0359954fc8deb7d8ff5a`.

**STATUT : CAMPAGNE 4 CLÔTUR
...[truncated 911 chars]