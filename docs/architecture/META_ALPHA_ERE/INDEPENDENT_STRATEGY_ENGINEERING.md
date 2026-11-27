# MODULE H — INDEPENDENT STRATEGY ENGINEERING (conception)

## Responsabilité

Transformer un mécanisme suffisamment établi (module G) en système
d'exploitation **propre** : nos entrées, nos sorties, notre
dimensionnement, notre budget de risque — qui peuvent différer de ceux
du trader observé, car seul le phénomène compte.

## Conditions d'entrée dans ce module (porte de gouvernance)

`ModelDossier` au niveau FORTEMENT ÉTAYÉ minimum pour la géométrie
économique, signature mesurée dans notre corpus, queue caractérisée.
Aujourd'hui : **aucun modèle ne franchit encore cette porte** (ME-001
attend sa validation prospective) — ce module est donc conçu, pas
activé. Précédent négatif : V1/V2-F2 ont été construits par copie
comportementale avant identification économique ; leur échec (−30,40 /
−33,24, LMD-008) est la justification de cette porte.

## Contenu d'une `EngineSpec`

Règles d'entrée propres (détection de la signature) ; règles de sortie
liées au phénomène (pas au comportement copié) ; dimensionnement par
budget de risque pré-alloué (enseignement ME-001.3 : le filtrage à
l'entrée protège, le stop intra-trajectoire détruit) ; conditions
d'activation/désactivation par régime ; limites d'exposition et de
durée ; gestion explicite de l'échec du phénomène (la question ouverte
de ME-001) ; journalisation intégrale des décisions.

## Règles

Gel par hash dès la première évaluation ; toute modification crée une
nouvelle version avec un nouveau dossier (jamais d'« amélioration »
silencieuse) ; interdiction d'optimiser sur le segment d'évaluation ;
plusieurs moteurs spécialisés possibles, un par source économique,
jamais un moteur par trader copié.
