# CAMPAGNE 5 — NOTE FINALE DE CLÔTURE (après vérifications fondateur, seq223)

Retour fondateur sur seq222 : résultats descriptifs **acceptés**, trois
candidates J1 acceptées au catalogue commun sans priorité ni promotion
automatique. La présente note exécute les deux vérifications
documentaires demandées (aucune nouvelle extraction, aucune relance de
run, aucune donnée source rouverte, aucun effet ni définition modifié),
requalifie C5-10, et clôt définitivement la campagne.

## 1. Vérification de provenance des runs

Faits établis sur l'historique Git (commits du runner GitHub Actions) :

- Run initial **44892050419** → commit `60a6fef` (10:02 UTC) : extraction
  complète mais atteintes journalières vides (bug d'initialisation des
  niveaux de référence de la veille, Hprev/Lprev jamais assignés au
  premier jour utilisable, donc aucun franchissement détectable dans la
  machine d'état journalière séquentielle).
- Run corrigé **44892455679** → commit `abbc2bc` (10:06 UTC) : régénère
  `CAMPAIGN_05_ATTEINTES_JOUR.csv.gz` (58 → 111 036 octets),
  `CAMPAIGN_05_DAY_FF.csv`, `CAMPAIGN_05_TOUCHES.csv`,
  `C5_COVERAGE.json` et `CI_LOG.txt`.
- La synthèse finale (`CAMPAIGN_05_COMPARISONS.csv`, seq222) a été
  exécutée localement **après récupération du commit `abbc2bc`**, sur
  les versions de fichiers de ce commit. Tous les résultats présentés
  proviennent donc des sorties validées.

| Comparaison | Fichier(s) d'entrée | Run de provenance |
|---|---|---|
| C5-01..C5-05 (F-E) | `CAMPAIGN_05_OPENINGS.csv.gz` (version commit `abbc2bc`) | run corrigé 44892455679 |
| C5-06, C5-07, C5-08 | `CAMPAIGN_05_ATTEINTES_JOUR.csv.gz` (régénéré) | run corrigé uniquement |
| C5-09 | `CAMPAIGN_05_ATTEINTES_SEMAINE.csv` (blob identique dans les deux commits) | run corrigé (contenu identique au run 1) |
| C5-10 | `CAMPAIGN_05_DAY_FF.csv` + `CAMPAIGN_05_TOUCHES.csv` (régénérés) | run corrigé uniquement |

Réponses explicites :

- **C5-01 à C5-05 reposent sur le run corrigé 44892455679** (versions de
  fichiers du commit `abbc2bc`, sur lesquelles la synthèse a tourné).
- **Aucune sortie du run initial n'a été utilisée pour une comparaison
  F-E.** De plus, le contenu décompressé de `CAMPAIGN_05_OPENINGS.csv.gz`
  est bit-identique entre les deux runs (sha256 du CSV décompressé :
  `4d00aaf1b3485a7ab0774c44a43e116e5a95a2de8666f5ae1913ad3c778838c5` ;
  seul l'en-tête gzip diffère) : le bug ne touchait pas le chemin
  d'ouverture de session, donc même une hypothétique utilisation du
  run 1 n'aurait rien changé aux résultats F-E.
- **Les sorties du run initial ont été exclues de F-F** parce que la
  machine d'état journalière n'y détectait aucun franchissement :
  `CAMPAIGN_05_ATTEINTES_JOUR.csv.gz` y est vide (58 octets, en-tête
  seul) et les drapeaux d'atteinte de `CAMPAIGN_05_DAY_FF.csv` y sont
  structurellement faux. C5-06/07/08 et le dénominateur de C5-10 en
  dépendent directement.
- Les fichiers hebdomadaires (`CAMPAIGN_05_ATTEINTES_SEMAINE.csv`,
  `CAMPAIGN_05_WEEKS.csv`) et de couverture
  (`CAMPAIGN_05_DAY_COVERAGE.csv`, `CAMPAIGN_05_WINDOW_COVERAGE.csv`,
  `CAMPAIGN_05_ORDRE_INDETERMINE.csv`) ont des blobs Git identiques
  dans les deux commits : chemins indépendants du bug.

## 2. Vérification de la multiplicité BY

Formule Benjamini–Yekutieli appliquée, par famille séparée :
pour m tests et H_m = somme(1/i, i=1..m), q_(k) = min_{j≥k} (m · H_m ·
p_(j) / j), plafonné à 1, p triées croissantes (implémentation
`ci_tools/campaign05_synthesize.py`, fonction `BY`, vérifiée par
recalcul indépendant à partir des seules p-values publiées — écarts
nuls partout).

### Famille F-E (5 hypothèses préenregistrées)
| ID | Hypothèse prévue | Testable | p brute | q publié (m=4) | q sensibilité (m=5) |
|---|---|---|---|---|---|
| C5-01 | Amplitude ouverture Londres vs Asie | oui | 0,0005 | 0,00417 | 0,00571 |
| C5-02 | Poursuite post-transition NY vs Londres | oui | 0,1010 | 0,28056 | 0,38436 |
| C5-03 | Amplitude Asie CONTINUITE vs TROU | **non** (bras B : 0 éligible) | — | NaN publié | — |
| C5-04 | Amplitude Londres lundi vs vendredi | oui | 0,0520 | 0,21667 | 0,29683 |
| C5-05 | Spread d'ouverture NY vs Londres | oui | 0,7260 | 1,00000 | 1,00000 |

Correction publiée avec **m=4, H_4=2,083333** : BY s'applique aux tests
effectivement réalisés disposant d'une p-value ; C5-03, structurellement
non testable (aucune p-value n'existe), est exclue du décompte et son q
est publié NaN, sans imputation. À titre conservateur, la correction a
été recalculée avec **m=5, H_5=2,283333** (taille de famille
préenregistrée, 4 p-values connues) : **aucune q ne franchit le seuil de
0,05 dans un sens ou dans l'autre, aucune lecture ne change** (C5-01
reste candidate J1 à 0,00571). Les deux jeux de q sont conservés
ci-dessus ; le publié (m=4) reste la référence, la sensibilité m=5 la
borne conservative.

### Famille F-F (5 hypothèses préenregistrées)
| ID | Hypothèse prévue | Testable | p brute | q publié (m=5) |
|---|---|---|---|---|
| C5-06 | Précocité d'atteinte avant 08:00, HAUT vs BAS | oui | 0,0005 | 0,00285 |
| C5-07 | Extension +60 min, HAUT vs BAS | oui | 0,2340 | 0,89050 |
| C5-08 | Retracement +60 min, avant/dès 13:00 | oui | 0,0005 | 0,00285 |
| C5-09 | Précocité hebdomadaire avant mercredi | calculable, non éligible (effectifs) | 1,0000 | 1,00000 |
| C5-10 | Journées contenues par ère | calculable, dégénérée (voir §3) | 1,0000 | 1,00000 |

Correction avec **m=5, H_5=2,283333** dès l'origine : conforme à la
famille de cinq annoncée. Le recalcul reproduit chaque q à 10⁻⁵ près.

**Conclusion BY : conforme.** Un seul écart de décompte (F-E m=4),
justifié par l'absence d'une p-value pour C5-03, borné par la
sensibilité m=5, sans effet sur aucune lecture.

## 3. Requalifications et nuances (interprétation seule)

- **C5-10 : comparaison STRUCTURELLEMENT NON ÉVALUABLE.** Aucune journée
  du corpus ne satisfait le critère gelé de 1 440/1 440 minutes observées
  (halte quotidienne du marché) ; numérateurs 0/863 et 0/632. Ce résultat
  ne doit **pas** être présenté comme une preuve d'absence de journées
  contenues sur le marché : il documente l'inapplicabilité du critère à
  ce corpus. La mention « NÉGATIF dégénéré » de seq222 est remplacée par
  la présente qualification. C5-10 n'est plus comptée parmi les
  comparaisons négatives.
- **ANO-C5-001 (nuance)** : le ratio estimé 1,189 dépasse le seuil
  matériel 1,15, mais la borne basse de l'IC95 (1,148) se situe
  légèrement **sous** ce seuil : l'excès de matérialité n'est pas établi
  à 95 % sur tout l'intervalle.
- **ANO-C5-002 (nuance)** : l'effet estimé +8,08 pts dépasse le seuil de
  5 points, mais la borne basse de l'IC95 (+3,80 pts) se situe **sous**
  ce seuil : la matérialité complète n'est pas garantie sur tout
  l'intervalle.
- **ANO-C5-003** : avertissement de composition session/régime
  d'activité maintenu tel quel.

## 4. Conservation

Sont conservés sans modification : les quatre résultats réellement
négatifs (C5-02, C5-04, C5-05, C5-07) ; les deux comparaisons non
éligibles (C5-03, C5-09) ; C5-10 structurellement non évaluable ; les
trois candidates J1 (ANO-C5-001/002/003), sans priorité ni promotion ;
les deux incidents techniques et leurs traces (run 44892050419, commits
`60a6fef`/`a29e3f1`/`abbc2bc`, note d'incidents). Aucune donnée
historique, aucun effet observé, aucune définition du protocole n'a été
modifié par la présente note. Aucun J2/J3. Restrictions inchangées :
XAU/USD exclusivement, holdout scellé, aucun backtest ni `challenge_sim`,
T0 séparé et inactif, FRED suspendue, 36 cellules S12 gelées, aucun
recalcul des fiches C3/C4, aucune optimisation à partir des candidates C5.

## 5. Hashes SHA-256 et checkpoint

- `CAMPAIGN_05_COMPARISONS.csv` : `0db427a9f4421826a4335456ab4499e81d9dc8c446698aceb311396fec4bfd3f`
- `C5_COVERAGE.json` : `54a365e0ce6b9e126c0ea3adf80b41b63cd509d64cea48045f716db6af48579d`
- `CAMPAIGN_05_OPENINGS.csv.gz` : `682c83a45ee26adf24242cf7043989e0dd6ff1cce86577c8f807b2288025ff67`
- `CAMPAIGN_05_ATTEINTES_JOUR.csv.gz` : `33ca0704bf4fac2348a8fda7c73f6de24477f927fbc282abab7d07ea20c1b2e7`
- `CAMPAIGN_05_ATTEINTES_SEMAINE.csv` : `d628dd3ccc9e5713166c0cba9cf4b6f24103cac9feed637836857ff10d15c9e5`
- `CAMPAIGN_05_REPORT_FE.md` : `d1e486315d229966fbd6b7742c583fdda8767dca9b79533d89132aed04da481f`
- `CAMPAIGN_05_REPORT_FF.md` : `af42fd8d8951757fb8ba88001254ef5bb9556c92d0772477a6b4e0a2d8f7f85e`
- `CAMPAIGN_05_CLOSING_DOSSIER.md` : voir registre (hash chaîné en seq223)
- Chaîne : la présente note est chaînée en **seq223** dans
  `reports/meta_alpha/TRIAL_LEDGER_CHAIN.json` ; chaîne revérifiée
  valide après ajout.

**STATUT : CAMPAGNE 5 — RÉSULTATS ACCEPTÉS, CLÔTURE DÉFINITIVE.**
