# PHASE 10-A — ADDENDUM DE VALIDATION DES CONSTANTES

**Statut : CONCEPTION EN COURS DE VALIDATION — GEL CHAÎNÉ NON
AUTORISÉ, EXÉCUTION NON AUTORISÉE.** Le présent addendum répond aux
quatre précisions obligatoires du responsable de recherche. Il
conserve les définitions approuvées des cinq documents compagnons et
n'y apporte que les précisions et réconciliations énumérées au §6.
**Aucun calcul, aucune extraction, aucune consultation de nouvelles
données n'a été effectué.**

## 1. Quantiles et fenêtre de 250 barres

| Timeframe | Variable quantilée | Niveau | Fenêtre causale | Durée calendaire approximative de 250 barres |
|---|---|---|---|---|
| H1 | \|r_H1\| (rendement log de clôture, bp) | **Q95** | 250 barres H1 entièrement clôturées précédentes | ≈ 11 journées de cotation (~23 h/jour) |
| H4 | \|r_H4\| (bp) | **Q95** | 250 barres H4 entièrement clôturées précédentes | ≈ 42 journées de cotation (6 barres/jour) |
| D1 | \|r_D1\| (bp) | **Q90** | 250 journées entièrement clôturées précédentes | ≈ 1 année de cotation |
| D1 | range journalier (bp) | **Q25** | 250 journées entièrement clôturées précédentes | ≈ 1 année de cotation |

Règles confirmées : calcul **séparé par timeframe**, aucun quantile
poolé entre timeframes ni entre variables ; la fenêtre contient
**exclusivement des barres entièrement clôturées avant la barre
évaluée**, et la barre courante est **strictement exclue** du calcul
de son propre seuil ; interpolation linéaire (type 7). **Amorçage** :
tant que 250 barres closes du timeframe ne sont pas disponibles,
aucun événement n'est détecté sur ce timeframe (période inéligible
publiée en effectifs dès l'exécution ; son ampleur exacte — de
l'ordre de 250 barres par timeframe, soit ~11 jours en H1, ~42 en H4,
~1 an en D1 en tête de corpus — sera comptée et publiée, jamais
comblée rétroactivement). Les franchissements F10-02/F10-04
n'utilisent pas de quantile : extrêmes (max/min) des 20 (H1) / 30 (H4)
barres closes précédentes.

## 2. Les six tests — table fermée et multiplicité

| ID | TF | Déclencheur (clôture) | Variable primaire unique | Horizon | Unité | H0 / H1 (bilatérale) | Données manquantes |
|---|---|---|---|---|---|---|---|
| F10-01 | H1 | \|r_H1\| > Q95 causal | rendement signé (sens de l'événement) de la barre H1 suivante, Bid/Ask | 1 barre | événement | médiane signée = 0 / ≠ 0 | barre suivante absente ou incomplète ⇒ événement censuré publié, exclu |
| F10-02 | H1 | clôture au-delà des extrêmes des 20 barres précédentes | rendement signé (sens du franchissement) cumulé | 4 barres | événement | médiane signée = 0 / ≠ 0 | toute barre manquante dans les 4 ⇒ censuré publié, exclu |
| F10-03 | H4 | \|r_H4\| > Q95 causal | rendement signé de la barre H4 suivante, Bid/Ask | 1 barre | événement | médiane = 0 / ≠ 0 | barre suivante incomplète ⇒ censuré publié, exclu |
| F10-04 | H4 | clôture au-delà des extrêmes des 30 barres précédentes | rendement signé cumulé | 24 h (6 barres H4) | événement | médiane = 0 / ≠ 0 | fenêtre incomplète ⇒ censuré publié, exclu |
| F10-05 | D1 | \|r_D1\| > Q90 causal | rendement signé du jour suivant, Bid/Ask | 1 journée | événement | médiane = 0 / ≠ 0 | jour suivant incomplet ⇒ censuré publié, exclu |
| F10-06 | D1 | range du jour < Q25 causal | **ratio du range du jour suivant à la médiane causale des ranges (250 j)** | 1 journée | événement | médiane du ratio = 1 / ≠ 1 | jour suivant incomplet ⇒ censuré publié, exclu |

**Multiplicité confirmée : m = 6 correspond exactement à ces six
hypothèses primaires**, chacune dotée d'une métrique primaire unique
produisant une p-value au sein de la correction BY à m = 6 fixe.
Aucune répétition (autre timeframe, autre horizon, autre sens, autre
variante de seuil) n'existe dans la famille : les trois timeframes
portent des tests distincts et déjà comptés. Les ventilations par
ère, par session et par signe, et les mesures MFE/MAE, sont des
**diagnostics non confirmatoires explicitement déclarés** : ils ne
produisent ni p-value ni lecture, et ne peuvent pas relancer une
famille arrêtée.

## 3. Portes économiques — valeurs exactes

Coût de référence d'une famille : **C_ref = spread médian observé des
événements de la famille + 1,7 bp**, où 1,7 bp = commission centrale
hypothétique (0,7) + slippage central hypothétique (1,0),
aller-retour. Scénarios de sensibilité gelés : favorable
(spread ×1,0 + 0,5 bp), central (spread ×1,0 + 1,7 bp), défavorable
(spread ×1,5 + 4,4 bp). Si les prix sont Bid/Ask, le spread est déjà
dans les prix d'entrée/sortie et n'est **jamais** soustrait une
seconde fois dans l'espérance ; C_ref ne sert alors qu'à l'échelle
des portes 1 et 3. En repli Mid (étiqueté non exécutable), le spread
complet est déduit une fois.

Ordre et seuils des portes, appliqués avant toute inférence :

1. **Magnitude** : médiane du range exécutable de la fenêtre
   d'évaluation ≥ **3 × C_ref**. Sinon arrêt de la famille.
2. **Espérance brute / nette** : espérance de la métrique primaire
   **nette du scénario central > 0** strictement (en prix Bid/Ask :
   espérance exécutable > 1,7 bp ; en Mid : espérance > spread
   médian + 1,7 bp). Sinon arrêt.
3. **Queue adverse** : MAE médian (valeur absolue) ≤ **3 × espérance
   nette centrale**. Sinon famille classée fragile et arrêtée.
4. **Effectifs** : ≥ **200 événements** et ≥ **100 grappes**
   temporelles par bras (bras = groupe de signe ou, pour F10-06,
   ensemble des événements) ; ≥ **50 événements par ère et par bras**
   pour que la ventilation d'ère soit conclue — en dessous, elle est
   publiée comme non concluante sans arrêter le test global.

**Règles d'arrêt** : échec à une porte ⇒ famille arrêtée, grandeurs
publiées, aucune p-value produite, facteur BY de famille conservé ;
les portes ne sont ni abaissées ni contournées par un sous-groupe ;
si les six familles échouent, la campagne se conclut négativement
sans élargissement.

## 4. Disponibilité et prix exécutables — chronologie par test

Pour les six tests, sans exception :

**clôture de la barre de signal (signal confirmé) → première
cotation du premier tick de la barre suivante = prix d'entrée
(Ask si long, Bid si court) → fenêtre de mesure ouverte à partir de
cette entrée.**

Il est **interdit** d'utiliser le dernier prix de la barre qui
produit le signal comme prix d'entrée : ce prix appartient au passé
au moment où le signal est confirmable. Le rendement primaire se
mesure donc de l'ouverture exécutable de la barre suivante à
l'ouverture exécutable de la barre qui clôt la fenêtre (F10-01 :
entrée à l'ouverture de la barre H1 suivante, sortie à son ouverture
+1 barre ; F10-02 : +4 barres ; F10-03 : +1 barre H4 ; F10-04 :
+6 barres H4 ; F10-05/F10-06 : entrée au premier tick de la journée
suivante, sortie au premier tick de la journée d'après pour le
rendement, range du jour suivant pour F10-06). Les **MFE/MAE restent
des extrema de trajectoire** : ils bornent ce qui était atteignable
et le risque encouru, et ne sont jamais présentés comme des
rendements réalisables, une sortie au MFE étant inconnaissable au
moment de décider.

## 5. Réconciliation avec les documents compagnons

Définitions approuvées conservées sans changement : question
centrale, famille F10-01…F10-06, cadre Bid/Ask d'abord, dictionnaire
des variables, refus de ressusciter P9-A…P9-E, grappe dominante à
5 %, amorçage inéligible publié, étiquette « historiquement évalué ».

## 6. Modifications apportées par le présent addendum (énumération exhaustive)

1. **F10-06 devient un test à métrique primaire testable** (ratio du
   range du lendemain à la médiane causale, H0 = 1) au lieu d'une
   simple porte sans p-value : c'est ce qui rend « m = 6 »
   exactement égal aux six hypothèses testées. Aucun autre test
   n'est ajouté.
2. **Comptabilité des portes précisée par mode de prix** : en
   Bid/Ask, la porte d'espérance compare l'espérance exécutable aux
   seuls coûts additionnels centraux (1,7 bp), le spread étant déjà
   dans les prix ; C_ref (avec spread) ne sert qu'aux portes
   d'échelle 1 et 3. En Mid, le spread complet est déduit une fois.
3. **Entrée explicitement déplacée** à la première cotation de la
   barre suivant le signal pour les six tests (le dossier initial
   énonçait le principe sans fixer le prix d'entrée test par test).
4. **Effectif minimal par ère (50 par bras)** ajouté comme condition
   de conclusion des ventilations d'ère, sans effet d'arrêt global.

## 7. Intégrité

SHA-256 des documents finaux : protocole `11174d76…a53`,
dictionnaire `33a5174a…b0`, modèle de coûts `164ee4e7…e`,
plan de validation `db879b89…a`, risques/autorisations
`35615e11…c` (valeurs complètes chaînées en seq279 avec le présent
addendum). Confirmé : **aucun calcul, aucune extraction, aucune
consultation de nouvelles données** ; corpus et holdout non touchés ;
la Phase 10 n'est pas déclarée ouverte à l'exécution.
