# PHASE 16 — INGÉNIERIE D'ENTRÉE PASSIVE : CAPTURE DU PREMIER RETRACEMENT

**Qualification : exploratoire IS, cohorte déjà étudiée. Statut de
preuve du remplissage : `QUOTE_CROSSING_PROXY_ONLY` — les ticks
sont des cotations Bid/Ask sans transactions, volume ni profondeur
(`PHASE16_FILLABILITY_AUDIT.md`, `2aaa01a1…`) ; aucun remplissage
n'est présenté comme un ordre réellement exécuté, et aucune
rentabilité nette complète n'est affirmée (commissions exclues).**

**Verdicts : `PASSIVE_ENTRY_ANALYSIS_INCONCLUSIVE` (structure) ;
`QUOTE_CROSSING_PROXY_ONLY` (qualité d'exécution) ;
`EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_NOT_FOUND` (économie).**

## 1. Cadre et intégrité

Protocole gelé avant tout calcul (seq341–342 : protocole
`88720927…`, audit de remplissabilité `2aaa01a1…`). Exécution CI
run `45060504262` entièrement vert (exit 0 ; 8 lots de fenêtres
tick 60 s + analyse ; holdout jamais accédé). **Contrôle de la
cotation de référence : 443/443 identiques au tick d'entrée 13-B**
(Bid, Ask et horodatage, 0 divergent, 0 sans cotation) — la
référence E3 est exactement la première cotation post-signal déjà
étudiée, et `P_limit` en est le milieu.

## 2. Ce que fait réellement la limite au milieu du spread

- **Franchissement (proxy) : 221/443 événements (49,9 %)**, délai
  médian **15,1 secondes** ; 222 ordres expirés à 60 s (`NO_FILL`,
  ni perte ni gain, conservés dans tous les dénominateurs) ;
  20 observations d'égalité stricte écartées comme il se doit
  (une égalité n'est pas un franchissement).
- Selon la grille gelée (≥ 50 % pour « identifiée », < 25 % pour
  « non identifiée »), le taux de 49,9 % tombe dans la zone
  intermédiaire : **`PASSIVE_ENTRY_ANALYSIS_INCONCLUSIVE`** — le
  premier retracement traverse le milieu du spread initial dans
  environ un cas sur deux, sans que ce soit un régime dominant.
- **Amélioration de prix médiane : +0,97 bp** (moyenne +1,02) —
  c'est, par construction, la demi-largeur du spread initial :
  un gain *mécanique et théorique*, conditionnel au
  franchissement, et non une preuve d'exécution à ce prix.

## 3. Le prix de la sélection : les remplis sont les événements qui reculaient

Le franchissement n'est pas un tirage neutre : un ordre n'est
« rempli » (proxy) que si le prix revient contre la direction du
signal dans la minute. Conséquence mesurée en sortie verticale
X0 (S0, conditionnel aux 207 remplis complets) : moyenne **−2,77
bp**, médiane −6,54 bp — nettement pire que la cohorte E0
entière (+0,11). Sur le même sous-ensemble des remplis, E3 fait
légèrement mieux que l'entrée E0 comparable (−6,54 contre −7,38
bp en médiane : à peu près l'amélioration mécanique), mais
rapporté à la **cohorte de 443** où les 222 non-remplis comptent
0, E3 tombe à **−1,29 bp** contre **+0,11** pour E0 à convention
de coûts comparable — et reste inférieur sous S1 et S2
(−1,53/−1,76 contre −0,37/−0,85). Avec les barrières, même
hiérarchie : X1 cohorte −0,62 (E0/X1 : +1,60 en Phase 15), X2
−0,16 (E0/X2 : +1,91) ; la cellule E3/X2 conditionnelle est la
moins défavorable (moyenne −0,34, médiane +0,40 en S0) mais ne
survit ni à la lecture cohorte ni au slippage (S2 : −1,34).
Selon la grille gelée : **`EXPLORATORY_PASSIVE_ENTRY_ADVANTAGE_NOT_FOUND`**.

En une phrase : la limite capture bien le premier retracement —
c'est précisément le problème. Les événements qui reviennent
assez vite pour franchir sont ceux dont la continuation est la
plus faible (sélection adverse), et l'autre moitié des signaux,
qui continuent sans revenir, est abandonnée à 0. Le bp mécanique
gagné sur les remplis ne paie pas cette double peine.

## 4. Limites qui bornent strictement la portée

1. **Exécution non prouvée** : sans données de transactions, de
   volume ou de carnet, rien n'établit qu'un ordre réel à
   `P_limit` aurait été servi, ni pour quelle quantité. Toute la
   partie « remplissage » est un proxy de franchissement de
   cotations, étiqueté comme tel dans chaque livrable.
2. **Fenêtre de 60 secondes gelée** : les franchissements plus
   tardifs ne sont pas étudiés (aucun autre délai testé,
   conformément aux interdictions) ; le taux de 49,9 % est
   inséparable de cette fenêtre.
3. Les 22 trajectoires incomplètes restent identifiées (14
   censures en X0 parmi les remplis, barrières classées seulement
   avant la première interruption ; 15 franchissements de
   barrières après trou comptés en lignes événement × cellule,
   ordre intra-gap jamais supposé, limites 14.1 respectées).
4. Aucune courbe de capital, aucune simultanéité de positions,
   commissions inconnues exclues : même un résultat favorable
   n'aurait pas constitué une rentabilité nette.

## 5. Livrables et traçabilité

`PHASE16_ENTRY_EVENTS.csv` (référence, `P_limit`, franchissement,
délai, amélioration, statuts — 443 lignes) ;
`PHASE16_ENTRY_COMPARISON.csv` (E3 contre E0 comparable, cohorte
et sous-ensemble rempli) ; `PHASE16_EXIT_MATRIX.csv` (9 cellules,
pondérations événement/grappe, commission théorique d'équilibre
en borne) ; `PHASE16_FILL_AND_GAP_AUDIT.csv` ;
`PHASE16_CLUSTER_WEIGHTING.csv` ; `PHASE16_RESULTS.json` ;
détail événement × cellule `PHASE16_ENTRY_EXECUTIONS_DETAIL.csv` ;
fenêtres tick par lot `P16_WIN_*.csv` et journaux conservés.
Moteur `ci_tools/phase16_engine.py`, jobs `lots16`/`analyse16`,
run `45060504262`.

## 6. Conclusion autorisée

L'entrée passive au milieu du spread capture le premier
retracement dans un cas sur deux et gagne mécaniquement ~1 bp
sur les franchis, mais la sélection adverse des événements
remplis et l'abandon des continuations immédiates rendent le
bilan de cohorte négatif face à l'entrée immédiate — laquelle
demeure, relativement, la moins mauvaise convention étudiée
(sans être validée : cf. 13-B/15). Aucune réussite économique
n'est fabriquée à partir du franchissement : le résultat est
un **non-avantage exploratoire sous proxy de cotation**. Toute
suite (autre fenêtre, données de transactions réelles) exigerait
une décision distincte et un nouveau préenregistrement, sur des
données n'ayant servi ni à la conception ni à la sélection ; le
holdout reste définitivement exclu.
