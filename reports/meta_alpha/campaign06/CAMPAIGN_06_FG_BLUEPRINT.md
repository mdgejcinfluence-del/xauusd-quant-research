# CAMPAGNE 6 — BLUEPRINT SCIENTIFIQUE F-G « FORME DES TRAJECTOIRES JOURNALIÈRES »

**Statut : PRÉPARATION AUTORISÉE — CALCULS INTERDITS.** Principe approuvé
par le fondateur (chaîné seq226). Aucune extraction, aucun calcul
exploratoire, aucune consultation de résultats nouveaux. Aucune
définition n'est gelée : ce blueprint, le dictionnaire, la liste des
comparaisons et la méthode seront soumis à validation avant tout gel.

## 1. Objectif scientifique

Déterminer si la géométrie des trajectoires intrajournalières du
XAU/USD constitue une dimension comportementale distincte : les journées
présentent-elles des formes directionnelles (chemin quasi rectiligne),
oscillantes (allers-retours sans déplacement net), mixtes, ou d'autres
formes que les mesures révéleront ? Les catégories ne sont **pas**
imposées artificiellement : les indicateurs continus sont primaires ;
toute classe (directionnelle / oscillante / mixte) devra être définie
par des constantes fixées a priori dans le protocole gelé, jamais par
des seuils ajustés sur les résultats.

Doctrine inchangée : description et cartographie avant toute stratégie.
Il ne s'agit ni de démontrer qu'une forme est « plus rentable », ni de
construire un signal. Toute candidate éventuelle irait au catalogue J1,
sans promotion automatique.

## 2. Nouveauté par rapport aux campagnes 0 à 5 (livrable 12)

| Campagne | Dimension cartographiée | Ce que F-G n'y reprend pas |
|---|---|---|
| 0–2 (dépassements, réintégrations) | franchissements de niveaux et retours | F-G ignore les niveaux : aucune référence à un prix d'ancrage |
| 2.4 / T0 (chantier inactif) | réplication prospective d'un contraste de réintégration | aucun lien, T0 reste séparé et inactif |
| 3 | candidates d'épisodes d'extension | F-G ne définit aucun épisode ni déclencheur |
| 4 | états relatifs de volatilité réalisée (journalier puis intra-journalier) et transitions entre états | F-G ne mesure pas le niveau de volatilité ; ses grandeurs sont des ratios de forme, sans dimension |
| 5 F-E | événements d'ouverture de session (amplitudes, spreads, issues à seuils relatifs) | F-G couvre la journée entière, sans session ni ouverture privilégiée |
| 5 F-F | premières atteintes des extrêmes de la veille | F-G ne date aucun franchissement ; l'heure n'intervient que comme localisation interne du parcours |

La question « quelle forme prend le chemin ? » n'a donc été traitée par
aucune campagne : F-G est une dimension nouvelle, indépendante des
candidates C3/C4/C5, qui ne sont ni réutilisées ni privilégiées.

## 3. Coût informatique estimé et règles de suspension (livrable 11)

- Extraction : même corpus décennal M1 que C4/C5 (282 partitions,
  ~3,54 M barres) ; un seul passage calcule les cinq grandeurs par
  journée. Coût attendu : **un run CI unique** de l'ordre de ceux de
  C4/C5 (quelques minutes de runner), synthèse locale en secondes.
  Coût financier : 0 FCFA. Aucun budget expérimental consommé
  (compteurs inchangés : tick 148/150, panel 28/60, exo 6/60,
  P7 0/24, NR 0/24, P9 10/12).
- Règles de suspension : si l'extraction échoue ou dépasse le cadre CI
  habituel, le calcul est suspendu, le blocage documenté, et les
  comparaisons non exécutées sont conservées comme telles ; aucun
  remplacement méthodologique sans autorisation ; aucun dépassement ne
  peut justifier de réduire la fenêtre, l'échantillon ou les contrôles
  de couverture.

## 4. Restrictions

XAU/USD exclusivement ; holdout 2020–2026 scellé ; aucun backtest ni
`challenge_sim` ; aucun J2/J3 automatique ; FRED suspendue ; 36 cellules
S12 gelées ; T0 séparé et inactif ; fiches historiques non modifiées ;
F-H et F-I conservées en réserve, non abandonnées.
