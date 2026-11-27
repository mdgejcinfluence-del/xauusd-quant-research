# ME-001.2 — FORENSIQUE DES NON-RÉCUPÉRATIONS

Même protocole d'épisodes que ME-001.1 (seq480/482) ; 2 136 épisodes
enregistrés avec trajectoires (segmentation : reprise après la barre
de récupération, d'où 2 136 vs 2 327 au catalogue ME-001.1 qui reste
la référence des taux). Issues : 1 958 récupérés, 166 non-récupérés à
24 h, 12 censurés par fin de partition (jamais comptés comme échecs).

## Structure des non-récupérations (DÉMONTRÉ)

Ce ne sont pas des récupérations « un peu lentes » : profondeur médiane
à 24 h de **−186 bp** (quartiles −129 / −267, extrême −546 bp), contre
des seuils de détection de 5–20 bp. La trajectoire médiane diverge
tôt et continûment (rendement médian vs référence à 5 min déjà plus
négatif, écart croissant à chaque horizon —
`ME001_NONRECOVERY_CHRONOLOGY.csv`). La queue des pertes de la mesure
baseline absorbe **80,7 % des gains** des épisodes récupérés
(ES95 ≈ −200 bp, pire −257 bp).

## Signatures précoces : information réelle mais drapeau préenregistré réfuté

Les médianes se séparent avec le temps (fraction de retracement
maximale à 900 s : 0,94 récupérés vs 0,53 non-récupérés ; temps sans
amélioration : 335 s vs 565 s), faiblement à 60–300 s. Mais le drapeau
causal gelé en seq482 (retracement < 25 % **et** profondeur ≤ −2×seuil)
n'atteint qu'une **sensibilité de 3–8 %** pour une spécificité de
97–100 % : il arrive trop tard ou jamais, car les non-récupérations
passent souvent par des retracements partiels avant de s'aggraver.
**RÉFUTÉ** comme détecteur. Il existe bien un moment de divergence
statistique (visible à 900 s dans les médianes), mais aucun seuil
simple préenregistré ne le transforme en décision précoce utile —
chercher ce seuil sur ces mêmes données serait de l'optimisation.

## Familles de sortie contrefactuelles : toutes dégradent (DÉMONTRÉ)

Sur découverte **et** validation, chaque famille gelée fait pire que
la baseline « attendre récupération ou 4 h » (espérance baseline
+0,98/+1,56 bp) : sortie temporelle 1 h ≈ −3,4 bp ; excursions
−30/−50/−80 bp ≈ −2,2 à −4,0 bp ; non-amélioration ≈ −2,1 à −3,4 bp.
Protéger naïvement détruit plus de récupérations qu'il n'évite de
queue : les épisodes qui récupèrent traversent eux aussi de longues
phases sans amélioration et des excursions profondes. C'est la
confirmation indépendante, dans le corpus, du piège qui a tué V1/V2-F2.

## Verdicts aux questions

1. Structure : aggravation continue profonde (−186 bp médian), pas
   une famille « lente » homogène — profondeurs en quartiles
   faible/modérée/sévère/extrême (`ME001_NONRECOVERY_CATALOG.csv`).
2. Familles : distribution continue de profondeurs, pas de classes
   nettes démontrées.
3. Caractéristiques avant aggravation : **COMPATIBLE MAIS NON
   IDENTIFIÉ** — séparation médiane réelle dès 300–900 s, aucun
   détecteur causal simple validé.
4. Moment : la séparation devient nette vers 15 min, trop tard pour
   protéger l'essentiel de la queue déjà engagée.
5. Faux positifs du drapeau : 0,4–3,3 % des récupérés (faibles) —
   mais au prix d'une sensibilité inutilisable.
6. Gains sacrifiés par les familles de sortie : elles transforment
   une espérance de +1,0/+1,6 bp en −2,1 à −4,9 bp, soit ~3–6 bp par
   épisode sacrifiés.
7. Queue évitable par ces familles : négative nette — elles
   « évitent » moins qu'elles ne détruisent.
8. Politique économiquement intéressante sur données indépendantes :
   **aucune parmi celles testées (RÉFUTÉ pour ces familles gelées)**.
9. Non identifiable ici : une règle de protection apprise (exigerait
   des données neuves pour être validée), le Bid/Ask HFM réel, le
   comportement au-delà de 24 h.

ME-001 reste **SIGNATURE_DETECTED**. La conclusion économique se
durcit : le phénomène paie l'attente, et toute protection simple le
détruit — l'exploitation éventuelle devra résoudre ce dilemme avec un
mécanisme qualitativement différent (dimensionnement du risque dès
l'entrée, pas un stop), à formuler comme nouvelle hypothèse et à
valider sur données indépendantes.
