# CAMPAGNE 4 — DICTIONNAIRE DES ÉVÉNEMENTS ET DES ÉTATS (À VALIDER)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Ce
dictionnaire est soumis à validation propriétaire ; son hash sera chaîné
avant toute extraction. Aucune définition ne peut être modifiée après
consultation des résultats. Seuils toujours causaux (passé uniquement,
barre/jour courant exclu des seuils) ; aucun seuil poolé rétrospectif ne
sera présenté comme une détection en temps réel ; aucun état ne constitue
un signal directionnel.

## 1. Conventions communes

- Corpus : barres M1 reconstruites depuis le tick IS (282 partitions,
  2010-01-04 → 2019-12-16), même corpus que les campagnes 1–3. Prix Mid.
- Journée de cotation = date UTC présente dans le corpus. Ères
  2010–13 / 2014–16 / 2017–20. Sessions UTC : Asie 00–08, Londres 08–13,
  New York 13–21, nuit 21–24.
- « Jours précédents » = journées de cotation présentes dans le corpus,
  jour courant exclu. Minimums d'historique : en deçà, aucun état n'est
  attribué (zone d'amorçage comptée et publiée).
- Référence existante conservée telle quelle : **F3** (prédiction HAR
  journalière gelée seq 75, `F3_DAILY_PRED.csv`, terciles de prévision
  BAS/MOYEN/HAUT, jours non classés publiés à part). F3 n'est ni modifié ni
  présupposé exhaustif.

## 2. Échelle journalière (famille REG-J, principale)

| Élément | Définition proposée (à valider) |
|---|---|
| Volatilité réalisée du jour j (RV_j) | √(Σ r²) des rendements log M1 du jour ( ×10⁴, en bp ), calculée sur barres complètes du jour ; jour utilisable si ≥ 300 barres M1 |
| Seuils causaux du jour j | Quantiles 1/3 et 2/3 de {RV des **60 journées précédentes**} (minimum 40 journées d'historique, sinon pas d'état) — recalculés chaque jour, passé seul |
| **État-passé** (connu à l'ouverture de j) | Tercile F3 du jour j (BAS/MOYEN/HAUT/NON_CLASSE) : ce qui était assignable avant le déroulement du jour |
| **État courant** (connu à la clôture de j) | BAS si RV_j ≤ q1/3 causal, HAUT si RV_j > q2/3 causal, MOYEN entre les deux — seuils du passé, mesure du jour |
| Discordance F3 | Jour où l'état courant diffère de l'état-passé F3 (matrice 3×3 publiée intégralement, NON_CLASSE à part) |
| Transition candidate | Premier jour où l'état courant diffère de l'état courant de la veille |
| **Transition confirmée** | Transition candidate suivie de **3 journées consécutives** (candidate incluse) dans le nouvel état ; date de confirmation = 3e journée. Si l'état rechute avant 3 jours : transition **non confirmée**, comptée et publiée comme telle (jamais antidatée, jamais effacée) |
| Vitesse de transition | Nombre de journées entre la dernière journée de l'ancien état et la journée candidate : **rapide** si ≤ 2, **progressive** si ≥ 5, intermédiaire entre les deux — mesurée sur le chemin des états courants, publiée en distribution |
| Durée d'un état | Run de journées consécutives de même état courant ; runs tronqués aux bords du corpus = censurés, comptés |
| Retour à l'habituel | Après une journée HAUT, première journée où RV repasse sous la **médiane causale des 60 journées précédentes** ; temps de retour en journées, censuré à 60 journées ou fin de corpus |
| Alternance | Matrice des transitions confirmées (ancien → nouvel état), fréquences et parts, par ère |

## 3. Échelle intrajournalière (famille REG-S, secondaire et séparée)

| Élément | Définition proposée (à valider) |
|---|---|
| RV de session | √(Σ r²) des rendements log M1 de la session du jour (bp) ; session utilisable si ≥ 60 barres M1 |
| Seuils causaux de session | Quantiles 1/3 et 2/3 de la RV de **la même session** sur les 60 journées précédentes (minimum 40) — chaque session a ses propres seuils |
| État de session | BAS/MOYEN/HAUT par comparaison aux seuils propres, connu à la clôture de la session |
| Événements de session | Changement d'état entre sessions consécutives du même jour et entre la dernière session de la veille et la première du jour (comptés séparément) ; part des jours où l'état de session maximal diffère de l'état courant journalier (déphasages intra-journaliers, dimension que REG-J ne voit pas) |

## 4. Dimensions non-F3 (descriptives, famille DIM)

Ces dimensions décrivent des comportements que F3 ne contient pas (F3
n'ordonne qu'une amplitude journalière prévue). Elles sont publiées comme
**dimensions continues et leurs états terciles causaux**, sans prétendre
qu'elles forment des régimes discrets :

| Dimension | Définition proposée (à valider) |
|---|---|
| Asymétrie | Skew des rendements M1 du jour ; état d'asymétrie = tercile causal (60 journées précédentes, min 40) du skew journalier |
| Queues / extrêmes | Fréquence journalière des barres M1 dont \|r\| dépasse le **quantile 99 causal des \|r\| M1 des 60 journées précédentes** (min 20 000 barres) ; état de queue = tercile causal de cette fréquence |
| Volatilité de la volatilité | Écart-type des log RV sur les 20 journées écoulées (jour courant inclus pour la mesure, seuils terciles causaux sur le passé pour l'état) |
| Dispersion intrajournalière | Ratio RV de session maximale / RV de session minimale du jour (sessions utilisables uniquement) ; état par terciles causaux (60 journées précédentes) |

## 5. Conséquences postérieures (strictement après confirmation)

Pour chaque transition confirmée (date de confirmation D) : distributions
sur les fenêtres **+1 à +5 journées** et **+6 à +20 journées** suivant D
(journées de cotation, excluant D) : quantiles des rendements journaliers,
RV médiane, skew médian, fréquence d'extrêmes, fréquence des impulsions
IMP-M5 (définitions campagne 3 gelées) et des dépassements (campagnes 1–2,
définitions historiques) rapportée au nombre de journées. Aucune fenêtre ne
déborde sur la transition confirmée suivante sans être signalée
(chevauchement de fenêtres compté). Les mêmes distributions sont publiées
pour les transitions **non confirmées** (fenêtres après la date candidate),
séparément — c'est le contraste descriptif central : ce qui distingue une
transition qui persiste d'une fausse alerte, sans jamais reclasser la
candidate a posteriori dans les séries d'états.

## 6. Ce que le dictionnaire interdit

Présenter un seuil poolé sur tout l'échantillon comme une détection
historique en temps réel ; antidater une confirmation ; supprimer les
transitions non confirmées ; transformer un état, une transition ou une
discordance en signal directionnel ; modifier F3 ou ses terciles ; comparer
une famille (REG-J, REG-S, DIM) à un contexte qui n'est pas le sien ;
imposer aux dimensions DIM le vocabulaire de « régime » avant de l'avoir
mesuré. Les événements « structurels » traités sont internes (sessions,
frontières de journée, événements déjà catalogués) : aucun calendrier
exogène n'est utilisé (FRED suspendue).
