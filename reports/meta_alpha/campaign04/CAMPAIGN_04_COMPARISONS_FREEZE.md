# CAMPAGNE 4 — LISTE EXACTE DES DIX COMPARAISONS (PROPOSITION FIGÉE À VALIDER)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Liste
exhaustive soumise avec le dictionnaire version 2 (seq 195) : si le
dictionnaire est validé, cette liste sera chaînée avec lui **avant tout
calcul** ; aucune comparaison ne pourra être ajoutée, retirée ou reformulée
après consultation des résultats. Définitions des états, transitions et
fenêtres : `CAMPAIGN_04_EVENT_DICTIONARY_V2.md`.

## 1. Méthode d'inférence figée (commune)

- **Bootstrap par blocs mobiles de 20 journées de cotation** sur la série
  journalière complète (états courants, RV, rendements, fréquences) :
  2 000 réplicats, graine figée au gel d'exécution ; dans chaque réplicat,
  épisodes, candidats, confirmations et fenêtres sont **recalculés à
  l'identique** (les confirmations exigeant 3 journées peuvent être
  tronquées aux coutures de blocs : elles sont alors traitées comme non
  confirmées dans le réplicat, règle publiée et appliquée uniformément).
- **Fenêtres chevauchantes** : chaque fenêtre de conséquence est tronquée à
  la veille de la prochaine date candidate (dictionnaire §5) ; une journée
  ne contribue donc qu'à une seule fenêtre de conséquence par famille de
  transition, et le bootstrap par blocs préserve la dépendance résiduelle.
  Le nombre de fenêtres tronquées est publié par comparaison.
- **Éligibilité descriptive (et non garantie de puissance)** : un bras
  n'est lu que s'il réunit ≥ 200 journées **et**, pour les comparaisons de
  transitions, ≥ **30 transitions** dans le bras. Ce minimum est un filtre
  de lisibilité descriptive : il ne confère ni puissance nominale ni seuil
  de confirmation ; en deçà, la comparaison est publiée « non éligible »
  avec ses effectifs, jamais tue.
- Correction **BY** sur l'ensemble des dix (une seule famille) ; p
  bilatérales issues du bootstrap (doublement de la plus petite queue) ;
  matérialité : 5 points (proportions), ratio 1,15 (médianes et taux) ;
  cohérence de signe dans ≥ 2 ères sur 3 quand la dimension n'est pas
  l'ère. En deçà : significatif sous le seuil matériel, négatif ou non
  éligible — tous publiés.

## 2. Les dix comparaisons (variables, populations, fenêtres, unités)

| ID | Hypothèse descriptive | Variable | Population (bras A vs B) | Fenêtre | Unité statistique | Matérialité |
|---|---|---|---|---|---|---|
| C4-01 | La RV réalisée après une transition confirmée vers HAUT diffère de celle après une transition confirmée vers BAS | RV médiane de la fenêtre (bp) | Transitions confirmées →HAUT vs →BAS (REG-J) | +1–5 journées après D | Transition | ratio de médianes 1,15 |
| C4-02 | Les transitions confirmées sont suivies d'une fréquence d'extrêmes différente de celle des transitions non confirmées de même sens | Fréquence journalière moyenne des barres M1 \|r\| > q99 causal (dictionnaire §7) | Confirmées vs non confirmées, **sens apparié** (→HAUT avec →HAUT, →BAS avec →BAS, poolées après vérification de l'homogénéité par sens publiée) | +1–5 journées après D (confirmées) / après C (non confirmées) | Transition | 5 points de pourcentage relatifs rapportés en différence de fréquence ×100 (points) |
| C4-03 | Les épisodes HAUT et BAS n'ont pas la même durée | Durée d'épisode (journées, runs REG-J) | Épisodes HAUT vs BAS, censures de bord exclues de la médiane mais comptées | Épisode entier | Épisode | ratio de médianes 1,15 |
| C4-04 | Le temps de retour à l'habituel après un épisode HAUT a changé entre la première et la dernière ère | Temps de retour (journées, référence figée par épisode, dictionnaire §5) | Épisodes HAUT débutés en 2010–13 vs 2017–20 | Jusqu'à retour ou censure (60 j) | Épisode | ratio de médianes 1,15 |
| C4-05 | La part des transitions rapides diffère selon le sens | Part des traversées rapides (1–2 j) parmi les transitions confirmées | Confirmées →HAUT vs →BAS | Traversée entière | Transition | 5 points |
| C4-06 | L'asymétrie des rendements après transition diffère selon le sens | g1 journalier médian de la fenêtre (formule §7) | Transitions confirmées →HAUT vs →BAS | +1–5 journées après D | Transition | ratio non applicable à une grandeur signée : **différence de médianes ≥ 0,10** (seuil matériel spécifique, figé ici) |
| C4-07 | Le taux de discordance entre état courant et état-passé F3 (tercile causal) a changé entre ères | Part des journées en discordance (matrice FIGÉE §4) | Journées 2010–13 vs 2017–20 (jours classés des deux côtés uniquement ; NON_CLASSE publié) | Journée | Journée | 5 points |
| C4-08 | La fréquence des impulsions IMP-M5 (définitions campagne 3 gelées) diffère selon l'état courant du jour | Nombre d'impulsions IMP-M5 par journée | Journées d'état courant HAUT vs BAS (l'état du jour ne conditionne que des événements du même jour à titre descriptif contemporain, aucune antériorité revendiquée) | Journée | Journée | ratio de taux 1,15 |
| C4-09 | Le déphasage intrajournalier (état de session maximal ≠ état journalier) diffère selon l'état journalier | Part des journées à déphasage (REG-S vs REG-J) | Journées d'état courant HAUT vs BAS | Journée | Journée | 5 points |
| C4-10 | La fréquence d'extrêmes diffère selon l'état de queue de la veille (dimension queues) | Fréquence d'extrêmes du jour (§7) | Journées dont l'état de queue de la **veille** est HAUT vs BAS (antériorité explicite : état connu à la clôture de la veille) | Journée | Journée | 5 points (fréquence ×100) |

Toutes les variables, seuils et fenêtres renvoient au dictionnaire v2 ;
aucune autre comparaison n'est autorisée dans la synthèse de la campagne.
Les résultats négatifs, sous le seuil matériel et non éligibles seront
publiés dans le registre, comme aux campagnes 1–3.
