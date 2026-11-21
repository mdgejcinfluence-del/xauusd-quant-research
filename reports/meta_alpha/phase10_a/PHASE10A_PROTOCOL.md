# PHASE 10-A — PROTOCOLE DE RECHERCHE DE MOUVEMENTS ÉCONOMIQUEMENT CAPTURABLES

**Statut : GELÉ DÉFINITIVEMENT (décision du responsable de recherche ;
procès-verbal `PHASE10A_FREEZE_RECORD.md`) — EXÉCUTION NON
AUTORISÉE, AUCUN CALCUL, AUCUNE CONSULTATION DU HOLDOUT.** La Phase 9
est close : aucune des cinq candidates P9-A…P9-E ne couvre ses coûts ;
elles ne sont **pas** reprises comme candidates actives et leurs
règles ne seront pas optimisées. Le gel ne déclare pas la Phase 10
ouverte à l'exécution : celle-ci exigera une décision distincte.
L'entrée se fait à la première cotation de la barre suivant le signal,
au plus 120 secondes après son ouverture attendue (dictionnaire,
modèle de coûts, addendum final §2 — règle unique) ; les portes de
queue élargies P90/ES90 du MAE y sont définies (addendum final §1).

## 1. Question centrale

Existe-t-il, sur XAU/USD aux horizons **H1, H4 et D1**, des
comportements observables **au moment de la décision** dont les
mouvements potentiels sont suffisamment importants pour absorber les
coûts d'entrée et de sortie ? Trois notions restent distinctes en
permanence : **amplitude observée** (une grandeur descriptive),
**prévisibilité** (une association conditionnelle établie), et
**rentabilité** (une espérance nette de coûts, jamais déduite des
deux premières).

## 2. Périmètre et protections

XAU/USD exclusivement ; corpus IS déjà autorisé uniquement ; holdout
2020–2026 scellé ; FRED interdite ; aucun backtest stratégique ni
`challenge_sim` ; aucune promotion automatique J2/J3 ; aucun budget
consommé ; 36 cellules S12 gelées et non modifiées ; chantier T0 non
activé ; fiches historiques intactes. Tout résultat issu du corpus IS
sera qualifié de **résultat historiquement évalué**, jamais de
confirmation indépendante : le corpus a déjà été largement exploré.

## 3. Cadre de mesure commun (A, B, C)

**Instants de décision.** Clôtures de barres complètes : H1 (chaque
heure), H4 (blocs 00/04/08/12/16/20 UTC), D1 (clôture de la journée
UTC). Une variable n'est utilisable que si elle est calculable à la
clôture de la barre de décision, avec les seules barres closes.

**Prix exécutables d'abord.** Les mouvements seront mesurés, lorsque
les ticks le permettent, sur des barres **Bid et Ask séparées**
agrégées depuis le corpus tick IS : une entrée longue se mesure à
l'Ask, une entrée courte au Bid, la sortie symétriquement — le spread
est alors **dans** les prix et n'est jamais soustrait une seconde
fois. À défaut (barres Mid seules), la mesure est étiquetée
**non exécutable** et soumise à la porte économique la plus stricte
(§6). Le spread observé à la barre de décision est publié pour chaque
événement.

**Mesures post-décision (descriptives, jamais explicatives).** Pour
chaque événement et chaque sens candidat : excursion favorable
maximale (MFE) et défavorable maximale (MAE) sur la fenêtre suivante
(1× l'horizon de décision pour H1/H4 ; 1 jour pour D1), rendement
signé à fenêtre fixe, temps jusqu'à l'excursion extrême. Les fenêtres
qui se chevauchent sont traitées par grappes (§7), jamais comme des
indépendances. Aucune de ces mesures n'entre dans la définition de
l'événement.

## 4. Famille fermée de comportements candidats (H)

Six tests, pas un de plus, chacun avec hypothèse et variable primaire
figées dès maintenant :

| ID | Horizon | Événement (causal, à la clôture) | Variable primaire |
|---|---|---|---|
| F10-01 | H1 | barre H1 extrême : \|r_H1\| > Q95 causal des 250 barres H1 précédentes | rendement signé de la barre H1 suivante, orienté par le signe de l'événement (continuation si > 0) |
| F10-02 | H1 | franchissement en clôture H1 du plus haut/bas des 20 barres H1 précédentes | rendement signé sur les 4 heures suivantes, orienté par le sens du franchissement |
| F10-03 | H4 | barre H4 extrême : \|r_H4\| > Q95 causal des 250 barres H4 précédentes | rendement signé de la barre H4 suivante, orienté par le signe |
| F10-04 | H4 | clôture H4 au-delà du plus haut/bas des 30 barres H4 précédentes | rendement signé sur les 24 heures suivantes, orienté par le sens |
| F10-05 | D1 | jour extrême : \|r_D1\| > Q90 causal des 250 jours précédents | rendement signé du jour suivant, orienté par le signe |
| F10-06 | D1 | jour étroit : range du jour < Q25 causal des 250 jours précédents | **amplitude seulement** : range du jour suivant (aucun sens ; porte de magnitude, pas de test directionnel) |

F10-06 est volontairement non directionnel : il ne peut alimenter
qu'une étude de magnitude (leçon de P9-D), jamais une règle de sens.
Aucun événement n'utilise de quantile poolé sur tout l'échantillon :
tous les seuils sont causaux et roulants, avec période d'amorçage
inéligible publiée (250 barres/jours d'historique requis).

## 5. Ce que le protocole refuse par construction

Reprendre P9-A…P9-E sous un nouvel horizon ; optimiser un paramètre
(fenêtre, quantile, horizon de sortie) après avoir vu un résultat ;
présenter une amplitude (MFE) comme une espérance (le MFE suppose une
sortie au meilleur point, inconnaissable) ; transformer une
régularité descriptive en « stratégie » sans passer les portes du §6
puis une confirmation indépendante hors corpus exploré.
