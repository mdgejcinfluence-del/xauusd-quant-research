# MODULE C — ECONOMIC HYPOTHESIS ENGINE (conception)

## Responsabilité

Transformer un `BehaviorProfile` en un ensemble d'hypothèses
économiques concurrentes, traçables et départageables — y compris des
hypothèses que le trader lui-même ne formulerait pas.

## Familles de départ (non exhaustives, extensibles)

Récupération d'inventaire (ME-001) ; déséquilibre temporaire (ME-002,
réfuté sous forme de fade symétrique) ; impulsion/continuation (ME-003,
réfuté à horizons fixes) ; fourniture de liquidité (ME-004, données
insuffisantes) ; retour après extension ; capture directionnelle ;
arbitrage statistique entre instruments liés ; stratégies
conditionnelles aux régimes ; exploitation de flux récurrents
(liquidations, couvertures, heures fixes). Le moteur peut proposer une
famille nouvelle si les observations ne rentrent dans aucune — avec
justification écrite (précédent : la géométrie asymétrique de ME-001 a
survécu à l'élimination de ME-002 et ME-003).

## Fiche hypothèse (obligatoire)

Fondement économique ; observations qui soutiennent ; observations qui
contredisent ; conditions de marché requises ; risque accepté ;
mécanismes alternatifs compatibles ; informations manquantes ;
expérience discriminante la moins coûteuse ; signature attendue dans
le corpus ; géométrie de gain (qui paie, pourquoi, combien avant
coûts). Aucune probabilité numérique sans modèle génératif déclaré.

## Règles de génération

1. Au minimum **deux** hypothèses concurrentes par dossier (une seule
   hypothèse = pas de science, juste une narration).
2. Chaque hypothèse doit prédire au moins une observation que ses
   concurrentes ne prédisent pas (sinon elles sont fusionnées).
3. Les hypothèses réfutées restent au registre avec leur preuve
   (ME-002, ME-003) : elles bornent l'espace des survivantes.
4. Une hypothèse née d'un dossier trader est retestée comme phénomène
   de marché autonome (question 3 de la constitution).

## Sortie

`HypothesisSet` versionné, transmis au module E. Exemple réel : pour
Colorful, le moteur aurait produit {récupération d'inventaire,
liquidité, momentum} ; les campagnes seq458–491 ont éliminé les formes
simples des deux dernières dans notre corpus.
