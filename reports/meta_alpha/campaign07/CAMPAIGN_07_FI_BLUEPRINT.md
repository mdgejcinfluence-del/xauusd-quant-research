# CAMPAGNE 7 — BLUEPRINT SCIENTIFIQUE F-I « NOMBRES RONDS DU XAU/USD »

**Statut : PRÉPARATION AUTORISÉE — AUCUN CALCUL, AUCUNE EXTRACTION,
AUCUNE CONSULTATION DE RÉSULTATS F-I.** Principe approuvé par le
fondateur (chaîné seq245). La clôture de la Campagne 6 est
définitivement acceptée (seq244) ; aucune nouvelle candidate J1 n'en
est issue et le catalogue ANO-C6 reste vide.

## 1. Question centrale

Les niveaux de prix psychologiquement ronds présentent-ils des
comportements particuliers dans le parcours du XAU/USD — approche,
première touche, franchissement strict, rejet, retour de l'autre côté,
maintien au-delà, distance parcourue après franchissement — et ces
comportements dépendent-ils de l'échelle du nombre rond ? La question
est posée **sans présupposer l'influence des nombres ronds** : le
protocole est construit pour pouvoir conclure à l'absence d'effet.

## 2. Idée directrice : niveaux exogènes et références placebo

Les niveaux étudiés ne sont **pas formés par le marché** : ce sont des
points d'une grille arithmétique fixée avant tout calcul (multiples de
50 et de 10 USD, § dictionnaire). Le dispositif central de la famille
est la comparaison systématique à des **pseudo-niveaux décalés**
(même grille translatée d'un demi-pas), extraits du même corpus, des
mêmes journées et avec des définitions d'événements strictement
identiques. Tout comportement qui apparaîtrait aussi fort aux
pseudo-niveaux n'est pas un effet de nombre rond : c'est un effet
général de parcours, de volatilité ou de session, et il sera publié
comme tel. Ce dispositif placebo est la réponse de conception au
risque majeur de la famille : fabriquer une anomalie à partir de
niveaux choisis après coup. Les grilles sont donc définies **avant
toute consultation des résultats**, justifiées par la convention de
marché (figures rondes en dizaines et demi-centaines de dollars),
jamais par les effets observés.

## 3. Audit de nouveauté (obligatoire) — campagnes 0 à 6

| Campagne | Objet | Différence avec F-I |
|---|---|---|
| 0–2 : dépassements d'extrêmes et réintégrations | franchissements des plus hauts/bas **formés par le prix** (veille, ancres) et retours | F-I étudie des niveaux arithmétiques exogènes, jamais touchés « parce qu'ils comptaient » dans l'historique ; et ajoute la référence placebo décalée, absente des campagnes 0–2 |
| 2.4 / T0 | réplication prospective d'un contraste de réintégration | aucun lien ; T0 reste séparé et inactif |
| 3 | candidates d'épisodes d'extension après franchissement d'extrêmes | F-I ne définit ni déclencheur ni épisode d'extension ; ses événements sont des contacts avec une grille |
| 4 | états de volatilité réalisée et transitions | aucun état, aucun niveau de volatilité comme objet (seulement des ventilations de contrôle) |
| 5 F-F | premières atteintes des extrêmes de la veille, franchissements stricts vs touches | les niveaux de F-I ne sont ni des extrêmes ni datés par la veille ; la distinction touche/franchissement y est reprise comme **convention d'événement**, pas comme objet |
| 5 F-E | ouvertures de session | aucune session comme objet ; les sessions ne sont que des ventilations publiées |
| 6 F-G | géométrie des trajectoires journalières (ER, S, τ) | aucune grandeur de forme ; F-I est une famille d'événements de contact, pas de géométrie globale |

Conclusion de l'audit : F-I ne reproduit ni les analyses de niveaux
des campagnes 0–2 (niveaux endogènes, sans placebo) ni les atteintes
de C5 (extrêmes de la veille). Son objet — le comportement au contact
d'une grille arithmétique exogène, contre placebo décalé — est nouveau
dans le programme.

## 4. Coûts estimés et règles de suspension (livrable 9)

- Extraction : même corpus décennal M1 (282 partitions, ~3,54 M
  barres) ; détection d'épisodes d'approche sur deux grilles (ronds et
  pseudo-niveaux) en un passage. Coût attendu : **un run CI unique**
  de l'ordre de C5/C6, synthèse locale. Coût financier : 0 FCFA.
  Aucun budget expérimental consommé (compteurs inchangés).
- Suspension : tout échec, toute incohérence de chaîne ou de couverture
  suspend le calcul concerné ; blocage documenté ; comparaisons non
  exécutées conservées comme telles ; aucune dégradation
  méthodologique (ni grille réduite, ni fenêtre raccourcie, ni placebo
  abandonné) pour faire terminer un calcul.

## 5. Restrictions

XAU/USD exclusivement ; holdout 2020–2026 scellé ; aucun backtest ni
`challenge_sim` ; aucun J2/J3 automatique ; aucun budget consommé ;
FRED suspendue ; 36 cellules S12 gelées ; T0 séparé et inactif ;
fiches historiques non modifiées ; candidates C5 sans priorité ni
confirmation automatique ; F-H en réserve, non abandonnée.
