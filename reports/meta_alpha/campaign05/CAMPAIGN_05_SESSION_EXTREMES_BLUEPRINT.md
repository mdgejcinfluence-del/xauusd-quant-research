# CAMPAGNE 5 — TEMPORALITÉ DES SESSIONS ET EXTRÊMES DATÉS (BLUEPRINT)

**PRÉPARATION — AUCUN CALCUL — EXÉCUTION INTERDITE AVANT VALIDATION DU
PROTOCOLE.** Campagne approuvée dans son principe (seq 208), familles
**F-E** (temporalité fine des sessions) et **F-F** (extrêmes journaliers et
hebdomadaires datés) du plan de reprise (seq 183). Les deux familles sont
préparées, analysées et publiées **séparément** : aucune fusion
d'observations ne servira à gonfler des effectifs. Descriptif seul : aucun
backtest, aucun `challenge_sim`, aucune optimisation, aucune promotion
automatique, holdout scellé, flux prospectif T0 interdit, FRED suspendue,
36 cellules S12 intactes, XAU/USD seul. Doctrine : découvrir, classer et
comprendre avant toute étude de prédictibilité ; aucune hypothèse n'est
privilégiée pour sa rentabilité éventuelle ; les candidates des campagnes
3 et 4 ne sont ni à confirmer ni à reproduire.

## 1. Famille F-E — Temporalité fine des sessions

### 1.1 Ce qui sera distingué
- **Ouvertures de sessions** : la première barre complète d'une session et
  les fenêtres qui la suivent (5/15/30/60 minutes), décrites en amplitude,
  volatilité réalisée, excursion et spread de contexte.
- **Transitions entre sessions** : les frontières 08:00, 13:00, 21:00 et
  00:00 UTC comme événements datés, avec fenêtres symétriques avant/après.
- **Ouverture d'Asie** : traitée avec un **ancrage inter-jours réel**
  (§1.2) — jamais reconstruite à partir de frontières de partitions ou de
  découpages de fichiers.
- **Continuité entre journées** : le trou réel entre la dernière barre
  d'une journée et la première de la suivante (durée mesurée, écart de
  prix mesuré), y compris le trou de fin de semaine, publié comme objet
  descriptif propre.
- **Mouvements commencés avant une ouverture et poursuivis après** : le
  mouvement des 60 minutes précédant une frontière est mesuré à la
  frontière (passé seul) ; ce qui suit (poursuite, retournement,
  stagnation — vocabulaire d'issues mesurées, patron campagne 3) est
  strictement postérieur.
- **Comportements propres aux périodes de session** : cœurs de session
  hors fenêtres de frontière, pour ne pas attribuer aux sessions ce qui
  appartient à leurs bords.

### 1.2 Ouverture d'Asie : ancrage inter-jours réel
Dans le corpus (horodatages UTC), la session d'Asie conventionnée commence
à 00:00 UTC, qui est aussi la frontière de journée. La campagne ne créera
**aucune ouverture artificielle** : l'événement « ouverture d'Asie » est
la première barre M1 complète présente dans les données à partir de
00:00 UTC, et son contexte pré-ouverture est constitué des barres
réellement présentes avant elle (fin de la session de nuit de la journée
précédente et trou inter-jours mesuré entre la dernière barre de la
veille et cette première barre). Trois cas sont distingués et publiés
séparément, sans jamais les fusionner : **continuité** (trou ≤ 5 minutes,
cotation quasi continue), **trou intra-semaine** (trou > 5 minutes,
typiquement la pause quotidienne de cotation), **réouverture de semaine**
(première journée après un week-end, trou long). Si les données montrent
des journées sans aucune barre avant 08:00, elles sont comptées comme
telles (ouverture d'Asie non observée), jamais complétées par
reconstruction.

### 1.3 Séparer l'effet de session de l'effet de frontière journalière
À 00:00 UTC, ouverture d'Asie et frontière de journée coïncident : les
deux effets sont **confondus par construction** et seront publiés comme
tels. La séparation repose sur les contrastes que le protocole autorise :
les frontières 08:00/13:00/21:00 (transitions de session **sans**
frontière de journée) servent de références internes ; et, à 00:00, la
durée du trou inter-jours sert de dimension descriptive de tri (continuité
vs trou vs réouverture) — si l'« effet d'ouverture d'Asie » persiste en
cotation continue, il relève davantage de l'heure que de la coupure des
données. Aucune décomposition causale au-delà de ces contrastes
descriptifs n'est revendiquée.

## 2. Famille F-F — Extrêmes journaliers et hebdomadaires datés

### 2.1 Ce qui sera distingué (jamais confondu)
- **Extrême courant** : plus haut / plus bas de la journée en cours jusqu'à
  l'instant t — observable à t, et c'est le seul « extrême » autorisé dans
  les variables d'instantané.
- **Première atteinte** : premier franchissement daté d'un niveau connu à
  l'avance (plus haut / plus bas de la journée précédente pour le
  journalier ; de la semaine précédente pour l'hebdomadaire).
- **Mises à jour** : extensions ultérieures de l'extrême courant par pas
  figés (dictionnaire), chacune datée.
- **Extrême final journalier / hebdomadaire** : connu uniquement à la
  clôture ; utilisé exclusivement pour des descriptions de clôture
  étiquetées comme telles, **jamais** pour classer un événement en cours
  de journée ni sélectionner les premières atteintes.

### 2.2 Questions
À quelle heure les premières atteintes surviennent-elles ; que se passe-t-il
ensuite (extension, retracement, stagnation, mesurés après l'instantané,
selon l'heure de formation) ; en quoi les atteintes hebdomadaires
diffèrent-elles des journalières ; quelle part des journées ne franchit
ni le haut ni le bas de la veille. Aucune trajectoire n'est présumée
(ni continuation ni retournement par défaut).

## 3. Différences avec les travaux déjà réalisés (livrable n° 10)

| Antécédent | Ce qui a été fait | Ce que la campagne 5 fait différemment |
|---|---|---|
| Campagne 1 / 1.1 (EV1, EV7, ouvertures) | Extrêmes et ouvertures décrits avec des variables en partie rétrospectives ; ouverture d'Asie **non mesurée** ; seuils d'extrême dont la leçon (C1.1) est qu'ils doivent être causaux et datés | Premières atteintes datées contre des niveaux connus à l'avance ; extrêmes finaux relégués aux descriptions de clôture ; ouverture d'Asie mesurée pour la première fois, avec ancrage inter-jours réel et trou mesuré |
| Campagne 2.2 (dépassements) | Franchissements des niveaux d'Asie/de la veille reconstruits causalement, à l'échelle du dépassement | F-F étudie la **formation des extrêmes eux-mêmes** (premier franchissement des niveaux de la veille et de la semaine, mises à jour, heure de formation), pas la réintégration après dépassement |
| Campagne 3 (impulsions/consolidations) | Seuils causaux roulants, instantanés en barres, issues mesurées | F-E réutilise la discipline (seuils causaux, instantanés, issues) sur des **frontières temporelles** plutôt que sur des événements de prix ; F-F sur des niveaux datés |
| Campagne 4 (régimes/volatilité) | États journaliers et de sessions à seuils causaux | F-E descend à la résolution des **fenêtres de frontière** (minutes), que les états quotidiens ne voient pas ; F-F est une famille d'événements, pas d'états |

## 4. Chaîne de valeur et gates

1. **Gate propriétaire (présente livraison)** : validation du blueprint,
   du dictionnaire, des comparaisons et de leurs hashes.
2. Gel chaîné des définitions validées ; validation temporelle sur données
   synthétiques avant extraction (patron campagnes 3–4).
3. Extraction sur le corpus IS seul (machinerie éprouvée, garde
   d'intégrité 282 partitions, bruts gzip), synthèse par famille séparée.
4. Registre au catalogue commun : candidates J1 éventuelles et résultats
   négatifs/non éligibles, sans promotion ; aucune fiche antérieure
   modifiée ; aucune famille ne sert à « confirmer » une candidate d'une
   autre campagne.
