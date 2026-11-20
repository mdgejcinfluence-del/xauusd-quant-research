# CAMPAGNE 1 — QUALITÉ ET DISPONIBILITÉ DES DONNÉES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Contrôle | Résultat |
|---|---|
| Corpus | Tick IS 282 partitions (borne 2020-01-20), barres M1 Mid + spread médian de barre ; brut événementiel commité : 224 748 lignes |
| Événements détectés | EV1 10 288 · EV2 dépassements 36 011 (réintégrations 30 590) · EV3 cassures 3 957 (retests 3 128) · EV5 impulsions 69 721 · EV6 consolidations 71 053 |
| Grappes jour×niveau (indépendance) | EV2 5 057 · EV3 2 763/2 170 · EV5 2 562 · EV6 2 565 — les comptages bruts ne sont jamais présentés comme indépendants |
| Journées | 2 515–2 565 journées porteuses selon famille (jours ≥ 300 barres M1) |
| Familles non produites | **EV4 compression/expansion et EV7 extrêmes hebdomadaires : non implémentées dans le moteur de ce run** — déclarées NON PRODUITES au rapport, pas approximées |
| F7 | **NON MESURÉ** : série horaire des probabilités du modèle gelé non versionnée (seq 146) ; aucun substitut utilisé |
| Chevauchements | Débuts de dépassement seuls comptés ; regroupement < 60 min même jour×niveau en grappes pour les statuts |
| Suffisance | Règle gelée : ≥ 200 événements et ≥ 100 grappes = RENSEIGNEE ; toutes les familles globales la satisfont ; cellules conditionnelles fines marquées NON CONCLUANTES le cas échéant dans les CSV |
| Holdout / NR | Non accédés ; baselines = ancien corpus uniquement |
| Incidents | Synthèse du moteur CI tombée sur une erreur d'unpacking après calcul complet des événements ; le brut événementiel étant commité par le workflow, la synthèse a été refaite localement sur ce brut (`CAMPAIGN_01_EVENTS_RAW.csv`), sans relancer l'extraction et sans toucher aux définitions gelées. Moteur CI conservé tel quel au dépôt pour traçabilité |
| Prix | Mid déclaré ; spreads = contexte mesuré à l'événement, jamais un coût de trade appliqué |
