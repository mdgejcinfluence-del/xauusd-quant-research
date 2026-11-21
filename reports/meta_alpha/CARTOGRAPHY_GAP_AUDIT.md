# META ALPHA — AUDIT DES LACUNES DE LA CARTOGRAPHIE (documentaire, aucun calcul)

**Statut : AUDIT AUTORISÉ PAR LE FONDATEUR (seq255) — AUCUNE EXTRACTION,
AUCUN CALCUL EXPLORATOIRE, AUCUN TEST, AUCUNE CONSULTATION DU HOLDOUT.**
Base : campagnes 0 à 7 closes au descriptif, protocole F-I gelé et
exécuté (clôture acceptée seq254, catalogue ANO-C7 vide conservé ;
provenance du run corrigé 44906521704 documentée au dossier de
clôture seq253, sorties du run 44903810557 abandonnées sans
contamination de la synthèse).

## 1. Familles déjà couvertes (campagnes 0 à 7)

| Campagne | Famille | Question traitée | Statut / produit |
|---|---|---|---|
| 0–2 | dépassements & réintégrations | franchissements d'extrêmes formés par le prix, retours | anomalie A absente à T0 ; réintégration décennale descriptive |
| 2.4/T0 | confirmation prospective | contraste de réintégration gelé | chantier inactif, flux non consulté |
| 3 | épisodes d'extension | candidates d'épisodes | 3 candidates J1 (ANO-C3), sans priorité |
| 4 | états de volatilité réalisée | états relatifs journaliers/intra-journaliers, transitions, terciles F3 | 2 candidates J1 avec avertissements mécaniques ; audit F3 : étiquettes poolées rétrospectives, recalcul causal exigé avant tout usage « à T0 » |
| 5 F-E | ouvertures de session | amplitudes, spreads, poursuite/retournement aux ouvertures | ANO-C5-001 candidate J1 |
| 5 F-F | extrêmes datés de la veille | premières atteintes HAUT/BAS, précocité, retracement | ANO-C5-002, ANO-C5-003 (composition) |
| 6 F-G | forme des trajectoires journalières | efficience, sinuosité, point médian, classes de forme | aucune candidate ; classe directionnelle quasi vide à fréquence minute |
| 7 F-I | nombres ronds | contact avec grille arithmétique exogène vs placebo décalé | aucune candidate ; I-03 déclassée pour composition |

## 2. Questions traitées partiellement ou restées ouvertes

- **Persistance de la forme** (C6-01) : non éligible, la classe
  directionnelle étant quasi vide **à fréquence minute** ; la question
  reste ouverte à d'autres granularités — mais ce serait un nouveau
  protocole, pas une reprise.
- **Excursion après franchissement de rond** (I-03) : association
  déclassée pour composition ; la question « que se passe-t-il après
  un franchissement, toutes causes confondues » n'a été traitée que
  par niveau (rond/placebo) ou par extrême de veille (C5), jamais pour
  les **chocs de prix eux-mêmes**.
- **Rejet après touche** (I-02) et **évolution de l'écart de rondité**
  (I-05) : non évaluables pour composition (strates trop fines).
- **Continuité inter-jours d'Asie** (C5-03) et **précocité
  hebdomadaire réelle** (C5-09) : non éligibles structurellement.
- **Journées contenues** (C5-10) : critère 1 440/1 440 inapplicable à
  ce marché (halte quotidienne) — question close comme non évaluable.
- **Conditionnements par régime de volatilité** (campagnes 0–4) :
  jamais réalisés causalement (terciles poolés rétrospectifs, audit
  seq196/199) ; un recalcul causal reste un chantier méthodologique
  connu, distinct d'une nouvelle famille.
- **Heure des extrêmes du jour courant** : jamais décrite en tant que
  telle (C5 date les atteintes des extrêmes **de la veille** ; F-G
  mesure un point médian de parcours, pas l'heure des extrêmes).

## 3. Trois familles candidates (classement multicritère)

Échelle 1 (faible) à 5 (fort) ; pour « risques » et « coût », 5 =
risque/coût **faible** (favorable). Aucun score n'est issu d'un calcul
nouveau : appréciations documentaires.

### Candidate A — F-J « Chocs minute extrêmes et leur sillage »
Question : que sont et que deviennent les très grandes variations
minute du XAU/USD (définies sur la distribution contemporaine des
|variations| M1, par ère) ? Regroupement temporel des chocs, asymétrie
hausse/baisse, trajectoire descriptive des 60 minutes suivant un choc
(continuation, retour partiel, stabilisation), selon l'heure et l'ère.
Jamais traitée : ni les campagnes de niveaux (0–2, 5, 7), ni les états
de volatilité (4, qui agrège au jour), ni la géométrie (6).

### Candidate B — F-L « Mémoire intraday du marché »
Question : quelle est la structure de dépendance temporelle des
variations et de l'activité à l'intérieur de la journée et d'un jour à
l'autre (autocorrélations descriptives des rendements et des
amplitudes par échelle 5–240 minutes, persistance de l'activité) ?
Dimension fondamentale jamais cartographiée en tant que telle ; à
distinguer de F3/HAR (prévision de la volatilité **journalière**,
modèle gelé en service, non directionnel) : F-L décrirait la mémoire
**intra-journalière**, sans modèle prédictif.

### Candidate C — F-H « Localisation temporelle des extrêmes du jour »
Question : à quelle heure le plus haut et le plus bas **du jour même**
se forment-ils, dans quel ordre, et comment cela a-t-il évolué ?
**Chevauchement explicitement évalué** : adjacente à C5 F-F (atteintes
des extrêmes de la veille : autre objet, mais mêmes barres et même
machinerie de datation) et à F-G (τ, point médian de parcours, n'est
pas l'heure d'un extrême mais partage la journée comme unité). La
nouveauté est réelle mais partielle : c'est la plus « proche parente »
des campagnes closes.

| Critère | A. F-J chocs | B. F-L mémoire | C. F-H extrêmes du jour |
|---|---|---|---|
| 1. Nouveauté scientifique | 5 | 4 | 3 |
| 2. Indépendance vs campagnes 0–7 | 5 | 4 | 2 |
| 3. Faisabilité (données IS disponibles) | 5 | 5 | 5 |
| 4. Risques de biais/fuite (5 = faible) | 3 | 4 | 4 |
| 5. Coût informatique (5 = faible) | 4 | 5 | 5 |
| 6. Valeur pour comprendre le XAU/USD | 5 | 4 | 3 |
| **Total** | **27** | **26** | **22** |

Risques principaux : A — définitions d'« extrême » par quantiles
contemporains (rétrospectifs, à étiqueter ; seuils à fixer par ère
sans regarder les sillages) et chevauchement des fenêtres de sillage
entre chocs groupés (grappes à définir) ; B — tentation prédictive
(l'autocorrélation descriptive ne doit jamais être présentée comme
exploitable ; proximité avec F3 à borner explicitement) ; C —
recouvrement méthodologique avec C5/F-G (à assumer comme cartographie
de complément, pas comme dimension nouvelle).

## 4. Exploitation du corpus IS sans holdout

Les trois candidates n'utilisent que le corpus décennal M1 déjà
constitué (282 partitions, 2010–2020 IS) : aucun accès holdout, aucun
budget expérimental (tick/panel/exo intacts), aucun flux T0, aucune
donnée FRED. Chacune suivrait le cycle complet habituel : blueprint,
dictionnaire, protocole consolidé soumis au gel, validation
temporelle synthétique, extraction CI unique, BY par famille,
publication intégrale des négatifs et non éligibles.

## 5. Recommandation argumentée

**Recommandation : Candidate A — F-J « Chocs minute extrêmes et leur
sillage ».** C'est la famille la plus nouvelle et la plus indépendante :
toutes les campagnes closes décrivent soit des niveaux (endogènes ou
exogènes), soit des états ou des formes de journée entière ; aucune ne
décrit les événements de prix les plus violents eux-mêmes ni ce qui les
suit à l'échelle de l'heure. Elle est entièrement faisable sur le
corpus existant, son coût est borné (un passage sur les barres M1),
et sa valeur de compréhension est directe : la manière dont le marché
absorbe un choc (retour, continuation, regroupement) est une propriété
comportementale de base du XAU/USD, utile à toute la cartographie
future — y compris pour relire, sans les relancer, les questions
laissées ouvertes par C6-01 et I-03. Ses deux risques (quantiles
rétrospectifs, sillages chevauchants) sont traitables dès le
dictionnaire, comme l'ont été les discontinuités de F-G et le placebo
de F-I.

Ordre de préférence : **F-J (27) > F-L (26) > F-H (22)**. F-L est une
excellente seconde (dimension fondamentale, coût minimal), à condition
de borner explicitement sa frontière avec F3/HAR. F-H reste en réserve
légitime mais doit être présentée, si elle est choisie, comme un
complément de cartographie adjacent à C5/F-G plutôt que comme une
dimension nouvelle.

**Décision demandée** : choix de la famille (recommandation F-J) et
autorisation de préparer blueprint + dictionnaire — préparation
documentaire uniquement, calculs toujours interdits à ce stade.
