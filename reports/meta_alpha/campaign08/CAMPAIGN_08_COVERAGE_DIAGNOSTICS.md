# CAMPAGNE 8 — DIAGNOSTICS DE COUVERTURE ET DE DÉPENDANCE

## 1. Couverture

282/282 partitions, 3 540 993 barres M1, 3 097 journées présentes
(2010–2013 : 1 245 ; 2014–2016 : 932 ; 2017–2020 : 920). Journées
éligibles à la détection causale : 3 087 ; inéligibles (amorçage) :
10, toutes en début de corpus. Épisodes par ère : 3 823 / 2 634 /
1 448. Par session du premier choc : S1 810, S2 2 105, S3 4 678,
S4 312. Seuil T_D des journées éligibles : min 10,0, médiane 10,04,
max 27,68 bp — le plancher de 10 bp est donc le seuil effectif de la
majorité des journées, le quantile causal ne le dépassant nettement
que dans les périodes agitées ; c'est une propriété publiée du
dispositif gelé, pas un ajustement.

## 2. Dépendance (composantes connexes, par comparaison)

| Comparaison | Grappes | Plus grande grappe | Grappes multi-jours | Sillages chevauchants | Traversées minuit | GRAPPE_DOMINANTE |
|---|---|---|---|---|---|---|
| FJ-01 | 2 078 | 15 unités | 2 | 33,5 % | 86 | non (≤1,0 %) |
| FJ-02 | 2 191 | 19 | 4 | 41,2 % | 96 | non |
| FJ-03 | 2 078 | 15 | 2 | 33,5 % | 86 | non |
| FJ-04 | 1 404 | 15 | 1 | 34,1 % | 61 | non |
| FJ-05 | **12** | **10 228 (99,8 %)** | 12 | 42,0 % | 56 | **OUI** |

Pour FJ-01…FJ-04, les fusions inter-journalières existent mais restent
rares (1 à 4 grappes) : la frontière UTC ne suffisait pas à les créer,
le graphe gelé les a néanmoins absorbées comme prévu. Pour FJ-05,
l'ajout des arêtes d'appariement connecte les journées entre elles en
chaîne et produit une composante géante : diagnostic publié avant
lecture, lecture NON ÉVALUABLE conformément au gel (voir rapport
pseudo-événements).

## 3. Censures

CLÔTURE_INDÉTERMINÉE : 72 épisodes (silence de 15 minutes interrompu
par une minute manquante) — exclus des comparaisons, descripteurs
publiés étiquetés incomplets. CENSURE_FENÊTRE à +60 : 43 épisodes clos
non mixtes. Aucune fenêtre incomplète n'est présentée comme complète.
