# CAMPAGNE 1.1 — QUALITÉ ET DISPONIBILITÉ DES DONNÉES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Contrôle | Résultat |
|---|---|
| Corpus | Même corpus tick IS 282 partitions, barres M1 Mid (déclaré) ; borne 2020-01-20 respectée ; holdout non accédé |
| EV4 | 14 782 épisodes, 2 492 journées ; seuil causal (médiane des ranges 60 min des 5 jours précédents du même traitement séquentiel) — les premiers jours sans historique suffisant (≥ 200 valeurs) ne produisent pas d'épisode |
| EV7 | 129 journées extrêmes (seuil P95 poolé 277,9 bp) ; concentration par ère 96/27/6 — voir leçon seuils au rapport |
| Ouvertures | 5 141 (Londres 2 571, New York 2 570) ; **Asie NON MESURÉE** (fenêtre « avant » à cheval sur la borne de journée du traitement) |
| Vérification Campagne 1 | Recalcul intégral depuis le brut commité (224 748 lignes) ; un résumé de campagne 1 corrigé (heure d'extrêmes journaliers : 12 h, pas 11 h — mélange de contextes dans la cellule GLOBAL) ; aucun chiffre des campagnes précédentes modifié dans leurs fichiers, la correction vit dans le rapport 1.1 |
| Incident CI | Le pas moteur du run 44723818675 est marqué en échec **après** l'écriture complète des sorties (fichiers de couverture et CSV présents et cohérents : EV4 14 782 lignes, EV7 129, ouvertures 5 141) ; les sorties ont été validées par comptage avant usage. Cause exacte non établie depuis le sandbox (logs inaccessibles) — consigné sans hypothèse |
| Censure | Réintégrations censurées à 60 min : 5 421 dépassements (15,1 %) ; biais de profondeur documenté au rapport §2 |
| Prix/contexte | Mid déclaré ; spreads = contexte à l'événement ; F7 non mesuré (document compagne) ; régime F3 causal |
| Reproductibilité | Moteur `ci_tools/campaign011_engine.py`, workflow `campaign011.yml`, synthèse locale des métriques depuis les bruts committés (patron campagne 1) |
