# PHASE 19-A — RECOMMANDATION

## Verdict : `DATA_CAPTURE_REQUIRED`

## Réponses aux trois questions de clôture
1. **Quelles nouvelles données réellement obtenir sans réutiliser l'existant ?** Aucune historique : la couverture complète 2010-01 → 2026-09 des sources est consommée (IS étudié par les Phases 10–18, holdout confirmé en 12-C.2 et interdit). La seule information non contaminée est **future** : des cotations XAU/USD postérieures à septembre 2026, à capturer. Un historique équivalent chez un autre fournisseur est rejeté : mêmes événements, donc même contamination de conception.
2. **Comment garantir la non-contamination ?** Capture prospective sous contrat gelé (provenance, flux brut immuable haché, affectation des lots à la naissance chaînée au registre), aucun paramètre hérité des résultats passés dans la conception de la collecte, journal d'accès.
3. **Comment réserver une validation indépendante ?** Séparation chronologique décidée maintenant (`NEW_DEVELOPMENT_DATA` puis `NEW_LOCKED_VALIDATION_DATA`), tailles minimales proposées avant ouverture (≥ 300 événements filtrés dans la population verrouillée), ouverture unique après gel chaîné d'un candidat, verdict `NON_EVALUABLE` plutôt que consommation si la taille n'est pas atteinte.

## Frontière
La prochaine autorisation éventuelle porterait sur la **mise en place de la capture** par l'infrastructure du propriétaire (l'environnement du programme n'a pas accès à un flux direct et le budget est de 0 FCFA) — pas sur un modèle. Tant qu'aucune donnée nouvelle n'existe, aucun test économique indépendant n'est matériellement possible, et les conclusions des Phases 17–18 demeurent le dernier état de la preuve : exploratoires, post-hoc, sans avantage économique exploitable démontré.
