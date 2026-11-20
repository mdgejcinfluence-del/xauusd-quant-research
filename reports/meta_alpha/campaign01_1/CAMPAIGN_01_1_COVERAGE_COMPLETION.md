# CAMPAGNE 1.1 — COMPLÉTUDE DE LA CARTOGRAPHIE STRUCTURELLE

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Campagne autorisée
seq 159, définitions EV4/EV7 reprises **littéralement** du dictionnaire gelé seq 157
(aucune définition inventée). Zéro essai, budgets inchangés (tick 148/150 · panel
28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12), holdout intact, 36 cellules gelées,
FRED suspendue. Les cinq observations ANO-C1-001 à 005 restent **J1 candidates, sans
modification rétroactive** ; aucune n'est promue.

## 1. Ce que cette campagne ajoute

**EV4 — Compression puis expansion** (définition seq 157 : range 60 min < 0,6 ×
médiane des ranges des 5 jours précédents, seuil causal). **14 782 épisodes**
(2 492 journées) : durée médiane de compression **21 minutes** ; le range des 60
minutes suivantes vaut en médiane **15,75 bp**, et n'atteint 1,5× le range comprimé
que dans **44,3 %** des cas — l'« expansion » après compression est donc, en médiane,
modeste, et elle diminue par ère (17,9 bp en 2010–13 → 12,6 bp en 2017–20, suivant le
calme séculaire).

**EV7 — Journées extrêmes** (range journalier > P95 poolé = 277,9 bp). **129
journées** seulement, et leur distribution par ère est elle-même le résultat :
**96 en 2010–13, 27 en 2014–16, 6 en 2017–20**. Un seuil poolé sur la décennie ne
décrit pas un « extrême » stable : il décrit surtout le début de la période. Leçon
méthodologique consignée pour la future détection : les seuils d'extrême doivent être
définis **par ère ou de façon adaptative causale**, faute de quoi la détection
confondra rareté réelle et dérive du régime. Formation des extrêmes hebdomadaires :
les journées extrêmes se concentrent en fin de semaine (jeu. 36, ven. 30 sur 129).

**Ouvertures de sessions.** Heures UTC des ouvertures mesurées : Londres 08:00,
New York 13:00 (blocs conventionnés seq 144/146 ; changements saisonniers documentés
seq 146 — Londres 08:00 UTC = 08:00 GMT l'hiver, 09:00 BST l'été ; New York 13:00 UTC
= 08:00 EST / 09:00 EDT : la baseline est donc attachée au bloc UTC, pas à l'horloge
locale de la place). Résultats (2 571 ouvertures Londres, 2 570 New York) :

| Ouverture | Spread avant (méd.) | Spread après (méd.) | Range 5 min | Range 60 min | Vitesse 50 % du range | Mouvements extrêmes (range 5 min > 20 bp) |
|---|---|---|---|---|---|---|
| Londres 08:00 UTC | 2,26 bp | 2,25 bp | 6,74 bp | 20,83 bp | 11 min | 3,4 % des jours |
| New York 13:00 UTC | 2,26 bp | 2,24 bp | 10,47 bp | 37,31 bp | 16 min | 12,6 % des jours |

Le spread ne bouge ni à l'ouverture de Londres ni à celle de New York en médiane
(2,26 → 2,25 bp) ; ce qui change, c'est l'amplitude : la première heure new-yorkaise
vaut près du double de la londonienne, et ses extrêmes de 5 minutes sont ~4× plus
fréquents. Par ère, les ranges d'ouverture diminuent (New York 60 min : 43,5 →
28,9 bp) et le spread d'ouverture récent tombe à ~1,9 bp (2017–20). **Ouverture
d'Asie (00:00 UTC) : NON MESURÉE dans ce run** — la fenêtre « avant » (23:30–00:00)
chevauche la borne de journée du traitement ; elle exige un traitement inter-jours
dédié, non improvisé ici. La règle conservatrice des 15 minutes post-ouverture
(blueprint) reste donc fondée sur la prudence, toujours non calibrée.

## 2. Vérification des résultats de Campagne 1 (contrôle qualité demandé)

Tous les chiffres ci-dessous sont recalculés depuis le brut commité
(`CAMPAIGN_01_EVENTS_RAW.csv`, 224 748 lignes), sans toucher aux définitions :

- **36 011 dépassements / 5 057 grappes / 2 515 journées** : les 36 011 sont des
  *débuts* de dépassement (première barre de clôture au-delà, par jour×niveau×côté) ;
  les 5 057 grappes regroupent les débuts séparés de moins de 60 min sur le même
  jour×niveau. Le taux brut compte donc des épisodes répétés intra-journée.
- **Dénominateur du « 85 % »** : 30 590 lignes de réintégration ÷ 36 011 débuts =
  **84,95 %**. Au niveau grappes : 4 373 ÷ 5 057 = **86,5 %**. Les deux sont publiés ;
  le chiffre de campagne 1 (85 %) est le taux brut par début.
- **Censure** : 36 011 − 30 590 = **5 421 dépassements (15,1 %) sans réintégration
  observée sous 60 min** — censurés à droite par la fenêtre d'observation (on ne sait
  pas s'ils réintègrent à +61 min ou jamais ; la fenêtre gelée s'arrête à 60). Leur
  profondeur médiane est nettement supérieure à celle des réintégrés (~25,6 bp contre
  ~9,7 bp sur l'appariement par grappe) : **les dépassements profonds réintègrent
  moins** — le taux de 85 % est donc tiré vers le haut par les dépassements peu
  profonds, biais de sélection écrit.
- **Délai médian de 3 minutes** : calculé sur les **seuls réintégrés** (30 590),
  quartiles 1 / 3 / 8 / 22 min (Q1/médiane/Q3/P90). Un délai médian incluant les
  censurés serait plus long et non calculable sans hypothèse de censure ; il n'est
  pas présenté.
- **« 79 % retestées » et « 55 % »** : 3 128 retests ÷ 3 957 cassures = 79,0 % ;
  le 55 % est la fréquence, **parmi les seuls retests**, des prix encore au-delà du
  niveau à +60 min (moyenne de l'indicateur `encore_au_dela_60`) — dénominateur =
  retests, pas cassures ; parmi toutes les cassures, la part « retest puis encore
  au-delà » vaut 0,79 × 0,55 ≈ 43 %.
- **Retracement médian de 90,5 % (EV5)** : définition algorithmique — pour chaque
  barre M5 avec |r| ≥ P90 poolé de |r| M5, cumul des rendements des 12 barres
  suivantes dans le sens contraire, maximum du cumul (plancher 0) divisé par
  l'amplitude de l'impulsion ; médiane de ce ratio = 90,5 %. Peut dépasser 100 %.
- **Range de 14,3 bp après consolidation (EV6)** : range haut−bas, en bp du prix de
  fin d'épisode, des **60 barres M1 suivant la fin** de la consolidation ; médiane
  14,27 bp.
- **Heures de formation des extrêmes** : distribution complète des 2 572 journées —
  **correction à la campagne 1** : le « 11 h UTC » publié provenait de la cellule
  GLOBAL mélangeant les contextes (journée + 3 sessions) ; pour la seule journée,
  l'heure médiane de formation du haut et du bas est **12 h UTC**, avec une
  distribution bimodale (pics à 00 h et 12–15 h) : la médiane seule est un résumé
  pauvre, la distribution est désormais la référence. Les extrêmes de session, eux,
  se forment par construction tard dans leur session (Asie ~02–03 h, Londres 10 h,
  New York 14 h en médiane).

## 3. F7 sur les événements structurels

Voir `CAMPAIGN_01_1_F7_CONTEXT.md`. En résumé : les sorties réellement disponibles du
modèle gelé sont des agrégats (AUC 0,684, lift 2,85×, taux de base 10,1 %) ; la série
horaire des probabilités n'est pas versionnée, donc **aucune mesure F7 par événement
n'est produite** et aucun substitut (p. ex. la volatilité réalisée) n'est présenté
comme équivalent. Le rôle descriptif futur de F7 est spécifié dans ce document
compagne, sans réentraînement.

## 4. Méthodologie de détection conditionnelle proposée (non exécutée)

Préparation demandée, soumise à autorisation distincte — **rien de ce qui suit n'a
été calculé** :

1. **Référence adaptée par construction** : chaque famille d'événements reçoit sa
   baseline du même contexte (session × régime F3 × ère), jamais une référence
   globale ; les seuils d'extrême sont causaux et datés (leçon EV7).
2. **Unité d'indépendance** : grappe jour×niveau ; intervalles d'incertitude par
   bootstrap par grappes (jamais par événement brut) ; tailles minimales : ≥ 200
   événements et ≥ 100 grappes par cellule de détection (règle gelée seq 157).
3. **Multiplicité** : le nombre de comparaisons de détection (familles × dimensions
   × métriques) est compté avant calcul et publié ; correction BY sur cette famille
   de détection ; plafond de fiches développées (10, doctrine atlas) sans limite de
   conservation au registre.
4. **Dépendances inter-événements** : deux familles partageant les mêmes épisodes
   (EV2/EV3 sur le même niveau) sont fichées comme liées ; aucun comptage double en
   indépendance.
5. **Séparation découverte/confirmation** : détection sur l'IS de développement,
   confirmation sur réserve temporelle interne disjointe, holdout jamais ouvert
   pendant la cartographie.
6. Les cinq observations ANO-C1 restent la matière première candidate de cette
   détection, **sans modification rétroactive** de leurs fiches.

## 5. État de la cartographie après 1.1

Couvertes : distributions de référence (Campagne 0) ; anatomies d'épisodes EV1,
EV2, EV3, EV5, EV6 ; EV4 et EV7 (avec la leçon des seuils) ; ouvertures de Londres
et New York. Restent ouvertes : ouverture d'Asie (traitement inter-jours), contexte
F7 par événement (inférence du modèle gelé à reconstituer sans réentraînement, sous
ordre), régime NR en résolution événementielle. La détection générale des anomalies
**n'est pas autorisée par la présente livraison** : elle attend l'examen du
propriétaire.

**STATUT : CAMPAGNE 1.1 LIVRÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**

*Annexes : `CAMPAIGN_01_1_EVENT_METRICS.csv`, `CAMPAIGN_01_1_SESSION_OPENINGS.csv`
(5 141 ouvertures), `CAMPAIGN_01_1_F7_CONTEXT.md`, `CAMPAIGN_01_1_DATA_QUALITY.md`,
bruts `EV4_EVENTS.csv` / `EV7_EVENTS.csv`. Chaîne : seq 159 → calcul → livraison.
FRED suspendue ; ANO-C1-001 à 005 inchangées.*
