# CAMPAGNE 4 — CARTOGRAPHIE DES RÉGIMES ET DE LA VOLATILITÉ

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE. CAMPAGNE
EXÉCUTÉE** sur autorisation fondateur (seq 201), dictionnaire v2 gelé
(sha256 `0a615c54…`), dix comparaisons gelées (`4024eaae…`). Aucune
hypothèse ajoutée en cours de campagne ; aucune fiche historique des
campagnes 0 à 3 modifiée ; la sensibilité des quatre fiches ANO-C2 de
régime n'a **pas** été recalculée (autorisation distincte toujours
requise). Aucun backtest, aucun `challenge_sim`, aucun J2/J3, holdout
scellé, chantier T0 séparé et inactif, FRED suspendue, budgets inchangés.

## 1. Ce que la campagne a mesuré (et avec quelles horloges)

2 572 journées utilisables (≥ 300 barres M1 ; 525 journées présentes sous
le seuil, exclues et comptées), 282/282 partitions. Quatre horloges
distinctes, jamais confondues : prédiction F3 du jour (causale, connue à
la clôture de la veille ; tercile **causal roulant** 250 j), état courant
du jour (RV réalisée contre les terciles des 60 journées précédentes,
connu à la clôture), transition confirmée (D = C+2, jamais antidatée),
conséquences strictement postérieures. Validation temporelle verte avant
calcul (tests synthétiques rejoués en CI). États classés : 2 532 journées
en état courant, 2 011 en tercile causal F3.

## 2. La structure d'ensemble : alternance rapide, pas de régimes longs

Le fait descriptif dominant de la campagne est la **brièveté des états** à
l'échelle du tercile journalier : 1 281 épisodes pour 2 532 journées
classées (durée médiane 1 jour en HAUT et MOYEN, 2 jours en BAS), 1 280
transitions d'épisodes dont **286 seulement confirmées** (persistance
≥ 3 jours) et 994 non confirmées, toutes cataloguées. Les traversées des
transitions confirmées se répartissent en 33,6 % rapides (1–2 j),
23,1 % intermédiaires (3–4 j) et 43,4 % progressives (≥ 5 j, chemin par
les états intermédiaires compté) : le marché passe donc son temps à
changer d'état relatif, et quand un état nouveau persiste, le chemin est
plus souvent graduel que brutal. Les retours à l'habituel après un épisode
HAUT (référence figée au début de l'épisode) sont rapides : médiane
1 jour, censure 1,1 % (360 retours mesurés). À cette échelle et avec ces
définitions, les « régimes » journaliers de volatilité relative sont un
phénomène d'**alternance** bien plus que de plateaux — c'est une réponse
descriptive directe à la question centrale, sans qu'aucune discrétisation
plus lente (hebdomadaire, par exemple) n'ait été autorisée ni testée.

## 3. F3 face au réalisé : ordonner une échelle n'est pas prévoir un tercile

Sur les journées classées des deux côtés, l'état courant diffère du
tercile causal de la prédiction F3 dans **60,2 %** des cas (matrice
complète publiée dans `CAMPAIGN_04_STATE_STATS.csv` et au registre
NEG-C4-007 : même lorsque F3 prévoit BAS, le réalisé se répartit
382 BAS / 263 MOYEN / 249 HAUT). Ce taux est **stable entre ères**
(C4-07, −1,1 point, négatif). Lecture disciplinée : F3 a été qualifié
historiquement pour ordonner une échelle d'amplitude et prévoir le niveau
de RV (QLIKE), pas pour assigner le tercile du lendemain — la campagne
quantifie cet écart sans rien retirer aux usages descriptifs antérieurs,
dont la lecture rétrospective fait l'objet de l'audit chaîné seq 199.
Les états relatifs décrivent par ailleurs des niveaux absolus qui ont
fortement dérivé : la cartographie publie RV absolue (bp) et log-ratio à
la médiane causale à côté de chaque état (bruts quotidiens), et les
différences d'ère en bp ne sont jamais relues comme des changements
d'état.

## 4. Les dix comparaisons gelées — résultats complets

Détail : `CAMPAIGN_04_COMPARISONS.csv` (statistiques, IC95 par bootstrap
à blocs mobiles de 20 journées avec recalcul des états/épisodes/fenêtres
dans chaque réplicat — 2 000 réplicats valides pour les dix, aucun
réplicat exclu —, p brutes, q BY, effectifs, lectures).

- **2 candidates J1 descriptives** : ANO-C4-001 (impulsions IMP-M5 par
  journée 2,68× plus fréquentes en état courant HAUT qu'en BAS —
  conditionnement **contemporain**, état connu à la clôture, cohérent sur
  les 3 ères) et ANO-C4-002 (déphasage sessions/journalier, fichée avec
  **avertissement mécanique majeur** : le maximum de quatre états de
  session dépasse presque par construction le tercile journalier BAS).
- **1 significative sous le seuil matériel** : C4-10 (persistance des
  queues au lendemain de l'état de queue, +0,75 point pour un seuil gelé
  de 5) — conservée, non fichée.
- **2 non éligibles, publiées avec leurs effectifs** : C4-01 et C4-06
  (9 et 5 fenêtres +1–5 j non tronquées par sens : les candidates
  suivantes surviennent trop vite — conséquence directe de l'alternance
  du §2 ; aucune fenêtre n'a été élargie après coup).
- **5 négatives** : C4-02 (confirmées vs non confirmées indiscernables
  sur la fréquence d'extrêmes postérieure), C4-03 (durées HAUT/BAS),
  C4-04 (retours par ère), C4-05 (vitesse selon le sens), C4-07
  (discordance F3 stable entre ères). Toutes conservées au registre.

**Correction d'unité documentée** : la statistique de C4-02 et C4-10 est
exprimée en points (fréquence ×100) ; le seuil matériel gelé de 5 points
leur a été appliqué en points (un premier passage du script appliquait
0,05, seuil des proportions — statistiques et intervalles inchangés,
seules la colonne de matérialité et la lecture de C4-10 en découlent :
sous le seuil matériel). L'incident est consigné ici et dans le document
qualité plutôt que corrigé silencieusement.

## 5. Livrables

`CAMPAIGN_04_DAILY.csv.gz` (états, RV absolue et relative, F3 continu et
ses deux formes de terciles, dimensions DIM, comptages d'événements),
`CAMPAIGN_04_SESSIONS.csv.gz`, `CAMPAIGN_04_EPISODES.csv`,
`CAMPAIGN_04_TRANSITIONS.csv` (catalogue complet confirmées/non
confirmées), `CAMPAIGN_04_TRANSITIONS_CONFIRMEES.csv` (fenêtres et leurs
troncatures), `CAMPAIGN_04_RETOURS.csv`, `CAMPAIGN_04_STATE_STATS.csv`,
`CAMPAIGN_04_COMPARISONS.csv`, `CAMPAIGN_04_ANOMALY_REGISTER.csv`
(2 candidates + 8 négatifs/non éligibles), `CAMPAIGN_04_DATA_QUALITY.md`,
journal CI et couverture.

**STATUT : CAMPAGNE 4 EXÉCUTÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
La campagne apprend sur le marché (alternance rapide des états relatifs,
discordance F3 quantifiée, fragilité des fenêtres post-transition) ; elle
ne confirme ni n'infirme aucune hypothèse préexistante et ne fonde aucune
utilisation prédictive. Les autres familles du plan de reprise restent
ouvertes en parallèle.
