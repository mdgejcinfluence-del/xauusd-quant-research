# PHASE 10 — RAPPORT FINAL DE CORRECTION F10-01 / F10-03 (amendement seq289)

**Statut : résultats historiquement évalués sur corpus IS 2010–2020
(jamais des confirmations). Protocole gelé PHASE 10-A (seq283),
amendement ciblé seq289, préflight et ordre seq284–285. Holdout
2020–2026 jamais ouvert. Aucune promotion, aucune stratégie, aucun
autre test relancé, aucune optimisation.**

## Comparaison avant / après correction

| | Avant (run 44919631588, seq288) | Après (run 45011013927, seq289) |
|---|---|---|
| F10-01 détectés / éligibles | 0 / 0 | **3 134 / 3 107** (2 617 grappes) |
| F10-03 détectés / éligibles | 0 / 0 | **762 / 660** (597 grappes) |
| Verdicts avant | NON ÉVALUABLE | **NÉGATIF ÉCONOMIQUE** (porte 2) des deux côtés |

**Pourquoi les anciens zéros étaient invalides.** L'implémentation
d'origine calculait le quantile roulant Q95 sur la fenêtre des 250
derniers rendements en y incluant les rendements indéfinis (NaN après
une barre manquante, typiquement la reprise hebdomadaire ; 3,78 % des
valeurs de fenêtre en H1, 3,81 % en H4). Un seul NaN rend le quantile
NaN : pratiquement chaque fenêtre était empoisonnée, le seuil
n'existait jamais, et aucun événement ne pouvait être détecté. Le
zéro événement était donc un **résultat invalide de
l'implémentation**, non une preuve d'absence d'événements extrêmes —
la correction détecte 3 134 (H1) et 762 (H4) événements, des ordres de
grandeur compatibles avec un seuil Q95 (~5 % des barres éligibles).

**Correction appliquée (seq289, définitions gelées inchangées)** :
fenêtre causale fixe des 250 barres précédentes, barre courante
exclue, NaN/non-finis exclus sans imputation ni remplacement, minimum
200 rendements valides sinon `INELIGIBLE_CAUSAL_WINDOW` (202 fenêtres
H1 et 208 fenêtres H4 inéligibles, essentiellement l'amorçage),
aucune extension de fenêtre vers le passé, quantile type 7 sur les
seules valeurs valides. Validation synthétique préalable : 14/14
tests (fenêtre NaN, 200 valides, 199 valides, fuite de la barre
courante, extension silencieuse).

## Résultats

- **F10-01 (H1)** : seuil Q95 médian 32,27 bp ; brut moyen −1,73 bp,
  net central −3,43 bp (C_ref 4,00 bp) ; MAE événement médiane
  17,19 bp, P90 45,11, ES90 70,60 (grappe : 18,58 / 47,07 / 72,51).
  Porte 1 franchie, **arrêt à la porte 2** (espérance nette ≤ 0).
- **F10-03 (H4)** : seuil Q95 médian 69,57 bp ; brut moyen −1,34 bp,
  net central −3,04 bp (C_ref 4,01 bp) ; MAE événement médiane
  24,17 bp, P90 73,74, ES90 126,09 (grappe : 24,56 / 73,45 / 125,83).
  Porte 1 franchie, **arrêt à la porte 2**.

Aucune p-value produite (arrêt aux portes avant inférence) ; BY
conservé à **m = 6 fixe**, jamais réduit à 2. Les ventilations par ère
(nets de −1,80 à −4,11 bp) sont des diagnostics non confirmatoires.
Les amplitudes post-extrêmes existent mais le mouvement signé de la
barre suivante est en moyenne opposé ou insuffisant face au spread
observé (~2,30 bp) et aux 1,7 bp hypothétiques.

## Provenance et vérifications

Artefacts du run moteur 44919631588 vérifiés avant recomputation
(`CORRECTION_ARTIFACT_VERIFICATION.json`) : comptages par famille
concordants avec seq288 (F10-02 5 652 ; F10-04 1 257 ; F10-05 246 ;
F10-06 657 ; F10-01/F10-03 à 0), couverture 282/282 partitions IS.
Ces artefacts ne contenant pas les séries de barres, la recomputation
ciblée a été exécutée sur le même corpus IS : 8 jobs par lot Kaggle
(chaque partition téléchargée une seule fois ; 3 540 993 barres M1 —
identique au comptage campagne 8), étape 2 d'agrégation H1/H4,
synthèse corrective. Run `45011013927` entièrement vert. Incidents
d'accès (secret Kaggle restauré par le propriétaire, quota Drive)
chaînés seq292–293 ; aucun impact sur les définitions ni les calculs.

## État final de la Phase 10 (soumis à validation du responsable)

| Famille | Verdict final |
|---|---|
| F10-01 H1 extrêmes Q95 | **NÉGATIF ÉCONOMIQUE** (porte 2, après correction seq289) |
| F10-02 H1 cassures 20 barres | NÉGATIF ÉCONOMIQUE (conservé, seq288) |
| F10-03 H4 extrêmes Q95 | **NÉGATIF ÉCONOMIQUE** (porte 2, après correction seq289) |
| F10-04 H4 cassures 30 barres | NÉGATIF ÉCONOMIQUE (conservé, seq288) |
| F10-05 D1 extrêmes Q90 | NÉGATIF ÉCONOMIQUE (conservé, seq288) |
| F10-06 D1 compression → expansion | NÉGATIF ÉCONOMIQUE (conservé, seq288 ; BY m=6 p = 1,0) |

Aucune des six familles préenregistrées n'est économiquement positive
sur le corpus IS aux prix exécutables Bid/Ask. La Phase 10 est
**soumise à la validation du responsable pour clôture** ; toute
confirmation exigerait un ordre distinct (holdout, prospectif).

Limites inchangées : entrée approchée par l'ouverture Bid/Ask de la
barre suivante (délai 120 s contrôlé au créneau attendu ou après
fermeture régulière, étiqueté) ; MFE/MAE = extrema de trajectoire ;
coûts centraux en partie hypothétiques (1,7 bp déduits une fois).
