# PHASE 15 — ENGINEERING DU POINT D'ENTRÉE DU SIGNAL H1

**Qualification : exploratoire IS, hypothèses postérieures aux
Phases 13-B/14, cohorte déjà étudiée. Ni stratégie validée, ni
confirmation indépendante. Commissions
`COMMISSION_EXCLUDED_BY_DESIGN` ; étiquettes S0/S1/S2 selon la
convention gelée (spread intégré une fois, slippage hypothétique
aux seuls remplissages).**

**Verdicts : `ENTRY_STRUCTURE_IDENTIFIED` ;
`EXPLORATORY_ENTRY_ADVANTAGE_NOT_FOUND`.**

## 1. Cadre et intégrité

Préenregistrement gelé avant tout calcul (seq338–339 : protocole
`99c58a12…`, politiques `f3f320ef…`) ; exécution CI run
`45058110571` entièrement vert (exit 0, 8 lots tick IS + analyse ;
holdout jamais accédé). Cohorte figée : 443 exposés, entrées E0,
probabilités, grappes et échéance repris sans recalcul.
**Réconciliations de référence conformes à l'identique** : E0/X0
reproduit la Phase 13-B (S0 : moyenne +0,1113, médiane −0,8918 bp,
n = 421) ; E0/X1 et E0/X2 reproduisent la matrice Phase 14 gelée
(B08 +1,6110 ; B09 +1,9407 bp en S0). Aucune divergence n'a
déclenché l'arrêt pour audit.

## 2. Anatomie du chemin post-signal (Question : une structure d'entrée existe-t-elle ?)

À la résolution tick (prix de liquidation, 421 trajectoires
complètes) et selon les critères gelés avant calcul :

- Le **premier extrême** suivant l'entrée immédiate est favorable
  dans **60,3 %** des cas (254/421) ; le premier extrême adverse
  survient dans la première minute pour 87,4 % des trajectoires.
  Ces deux faits sont une microstructure à l'échelle du tick —
  quelques secondes — et non un régime exploitable à eux seuls :
  ils décrivent un marché qui « respire » immédiatement autour de
  l'entrée, dans les deux sens.
- À l'échelle des fenêtres relatives (clôtures M1 de liquidation),
  le déplacement directionnel médian oscille sans régime durable :
  −0,49 bp (1–5 min), +0,35 (5–15), −0,36 (15–30), +0,41 (30–60),
  +0,75 (1–2 h), −0,59 (2–4 h), **−2,77 bp (4–8 h)** ; parts de
  fenêtres positives entre 44 % et 53 %. La fenêtre 0–1 min n'est
  pas mesurable avec la règle des deux clôtures (n = 0, consigné).
- L'ordre global des extrêmes confirme la Phase 14 réconciliée
  (14.1) : 212 MAE d'abord contre 209 MFE d'abord sur 421 — la
  continuation et le retracement restent entrelacés pendant toute
  la fenêtre, avec des délais médians d'extrêmes voisins de 2,8 h.

Verdict d'anatomie selon la grille gelée :
`ENTRY_STRUCTURE_IDENTIFIED` (critère du premier extrême rempli à
60,3 %) — à lire strictement comme une structure **descriptive à
l'échelle tick**, dont le §3 montre qu'elle ne se convertit pas en
avantage d'entrée.

## 3. Les trois politiques d'entrée (comparaison primaire : sortie X0)

| Politique | Déclenchés | Exécutés | Délai médian | Prix vs E0 (médian) | Moyenne cohorte 443, S0 | Moyenne exécutés, S0 |
|---|---|---|---|---|---|---|
| E0 immédiate | 443 | 443 (421 mesurés) | ≈ 0 min | — | **+0,106** | +0,111 |
| E1 récupération P0 | 408 | 408 (388 mesurés) | 3,1 min (moy. 32) | **−2,60 bp** | −0,259 | −0,295 |
| E2 deux clôtures | 443 | 443 (421 mesurés) | 5,0 min | −0,95 bp | −0,029 | −0,030 |

Le résultat central est mécanique et défavorable à l'attente :

- **E1 paie presque toujours plus cher** : attendre que la clôture
  revienne du côté favorable de P0, c'est entrer *après* que le
  prix a déjà refait le trajet — prix meilleur que E0 dans
  0,7 % des cas seulement, prix médian dégradé de 2,60 bp
  (moyenne −3,46 bp). Les 35 événements sans récupération de P0
  (`NO_ENTRY_TRIGGER`, jamais comptés comme pertes) ne compensent
  pas : rapportée à la cohorte de 443, E1 est inférieure à E0 sous
  S0, S1 et S2 (−0,259 / −1,135 / −2,010 contre +0,106 / −0,845 /
  −1,795).
- **E2 dégrade moins mais dégrade aussi** : deux clôtures
  directionnelles surviennent toujours (443/443, délai médian
  5 min), au prix d'une entrée médiane 0,95 bp plus mauvaise
  (meilleur prix dans 38,6 % des cas) ; moyennes de cohorte
  inférieures à E0 sous les trois scénarios.
- Avec les sorties à barrières (X1/X2), le même ordre se conserve
  dans la plupart des cellules (p. ex. X2 S0 : E0 +1,94, E2 +1,64,
  E1 +1,51 bp par événement) : le retard d'entrée **érode** la
  valeur des barrières ATR au lieu de l'améliorer, car l'échéance
  verticale, inchangée, laisse d'autant moins de fenêtre utile et
  l'entrée se fait après le premier mouvement favorable.

Selon les critères gelés (protocole §6, comparaison X0 sur
cohorte) : **`EXPLORATORY_ENTRY_ADVANTAGE_NOT_FOUND`** — E1 et E2
sont inférieures ou égales à E0 en moyenne de cohorte sous S0, S1
et S2. Aucune combinaison des 27 cellules n'est sélectionnée ;
les commissions théoriques d'équilibre (moyennes S0 par cellule,
bornes théoriques et non tarifs) figurent dans la matrice.

## 4. Confiance (descriptif uniquement)

En X0/S0, les moyennes par quartile (exécutés) ne dessinent pas
d'avantage propre aux entrées retardées : Q1 reste le quartile le
plus favorable pour les trois politiques (E0 +4,94 ; E2 +4,25 ;
E1 +3,27) et Q2 le plus défavorable (E0 −6,58 ; E1 −5,94 ;
E2 −5,87) ; E1/E2 « améliorent » relativement Q2/Q3 tout en
dégradant Q1/Q4 — un rééquilibrage, pas un gain, et toujours
inférieur à E0 à cohorte constante là où le signal gagne.
Aucun quartile n'est érigé en filtre (interdit et non fait).

## 5. Réponse à la question centrale

Le moment où le modèle prédit le mouvement et le moment où le
marché offrirait un point d'entrée « propre » ne se séparent pas
dans cette cohorte : la séquence stabilisation → récupération →
reprise n'apparaît pas comme un régime dominant (extrêmes
entrelacés 50/50, fenêtres relatives sans signe stable), et les
deux confirmations structurelles testées font payer l'attente —
la récupération de P0 est un signal de poursuite déjà pricée,
les deux clôtures directionnelles coûtent ~1 bp de prix médian.
**L'entrée immédiate E0 reste, sur l'IS et sous ce contrat, la
moins mauvaise des trois conventions étudiées** — ce qui ne la
valide pas économiquement pour autant (sa propre moyenne S0 de
+0,11 bp, médiane −0,89, devient négative dès S1 : cf. 13-B).

## 6. Limites et traçabilité

Entrées E1/E2 au premier tick réel (fenêtre stricte de 60 s,
horodatages conservés, 0 non-exécution parmi les déclenchés) ;
22 trajectoires incomplètes conservées dans les dénominateurs et
traitées selon les conventions 14/14.1 (barrières classées
seulement avant la première interruption, sinon `CENSORED` ;
ordre intra-gap jamais supposé) ; fenêtre d'anatomie 0–1 min non
mesurable (consigné) ; pas de courbe de capital ni de
portefeuille simultané ; résultats par grappe (moyenne
intra-grappe puis moyenne des grappes) dans
`PHASE15_CLUSTER_WEIGHTING.csv`. Livrables : chemins comparés
événement par événement `acaf7e98…`, exécutions `cac77342…`,
matrice 27 cellules `5ec1d365…`, confiance `dac47c43…`, grappes
`1e50affc…`, couverture et gaps `ca72e279…`, résultats
`90ac6e62…` ; moteur `ci_tools/phase15_engine.py`, jobs
`lots15`/`analyse15`. Toute étape ultérieure — par exemple une
évaluation prospective d'une entrée retardée — exigerait une
décision distincte, un nouveau préenregistrement et des données
n'ayant servi ni à la conception ni à la sélection ; le holdout
reste définitivement exclu et l'entrée immédiate n'est pas
davantage validée par ce résultat relatif.
