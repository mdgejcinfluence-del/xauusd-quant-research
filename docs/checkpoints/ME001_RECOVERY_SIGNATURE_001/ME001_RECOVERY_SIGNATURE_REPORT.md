# ME-001.1 — FENÊTRES DE RÉCUPÉRATION : RAPPORT

Protocole gelé seq480 (référence causale = max Mid 15 min ; épisodes
longs non chevauchants ; seuils 5/10/20 bp fixés a priori ; découverte
2012/2016, validation 2020/2024/2026 ; exécution mesurée ask→bid, coûts
comptés une fois). 2 327 épisodes sur 5 partitions certifiées.

## Réponses aux dix questions

1. **Les fenêtres existent-elles ? DÉMONTRÉ.** Après un écart de
   5/10/20 bp sous le plus haut de 15 minutes, le prix récupère
   complètement dans 68–94 % des cas en 24 h selon segment et seuil.
2. **Fréquence** : ~3 à 8 épisodes par jour de partition et par seuil
   (276 épisodes à 5 bp sur la partition 2026 de 37 jours).
3. **Régimes** : aucun régime de volatilité ne domine de façon stable
   (à 10 bp, l'edge par tercile change de signe selon le segment) —
   pas de signature de régime exploitable démontrée.
4. **Amplitude disponible** : récupération médiane complète de
   l'écart (le niveau de référence est revu) ; profondeur médiane
   réelle −11 à −44 bp selon le seuil — l'excursion continue bien
   au-delà du seuil de détection.
5. **Attente** : retracement 50 % médian en 1–14 minutes ; récupération
   complète médiane en ~1–5 h sur les épisodes qui récupèrent.
6. **Non-récupération** : 6–32 % des épisodes ne récupèrent pas en
   24 h ; leurs pertes à horizon 4 h atteignent −126 à −257 bp par
   épisode — la queue domine l'espérance.
7. **Brut vs coûts** : à 5 bp, l'espérance nette centrale est négative
   dans 4 segments sur 5 (PF 0,75–0,96) — **RÉFUTÉ** comme edge à ce
   seuil. À 10–20 bp, espérance positive dans la plupart des segments
   (+0,2 à +10,1 bp, PF 0,95–1,96) mais négative en découverte 2016 à
   20 bp et en validation 2026 à 10 bp.
8. **Signature préalable** : la détection est causale (écart confirmé
   sur barres 5 s), mais aucune variable pré-épisode testée (régime de
   volatilité) ne sépare les futurs récupérants des non-récupérants.
9. **Edge net reproductible ? COMPATIBLE MAIS NON IDENTIFIÉ.** Le
   phénomène est réel et parfois rémunérateur après coûts, mais
   l'espérance change de signe entre segments et la queue à 4 h
   (−250 bp) n'est pas gérée par la mesure : sans règle de gestion de
   l'échec de récupération, il n'y a pas d'edge validé. ME-001 passe
   à **SIGNATURE_DETECTED**, pas VALIDATED.
10. **Incertitudes restantes** : gestion de la non-récupération (c'est
    exactement la faiblesse qui a tué V1/V2-F2), Bid/Ask HFM réel,
    épisodes longs multi-jours censurés à 24 h, sélection du seuil
    (5/10/20 bp non calibrés — toute « optimisation » ultérieure devra
    utiliser des données neuves).

## Distinctions (doctrine)

Phénomène statistique : DÉMONTRÉ. Mécanisme économique plausible
(résorption d'écart temporaire / retour au niveau local) : FORTEMENT
ÉTAYÉ. Opportunité détectable : DÉMONTRÉ (règle causale). Opportunité
exécutable : partiellement (mesure ask→bid). Edge net validé : NON.
Aucune fourniture de liquidité n'est affirmée.
