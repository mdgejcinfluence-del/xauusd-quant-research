# CAMPAGNE 3 — COUVERTURE DES DONNÉES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Source | Périmètre | Usage campagne 3 | État |
|---|---|---|---|
| Corpus tick IS (282 partitions, Kaggle `shalom5123`, accès HTTPS direct rétabli seq 178) | 2010-01-04 → 2019-12-16, 2 515 journées, 3,54 M barres M1 | Reconstruction des barres M1/M5/M15 et des événements IMP/CONS | Accessible ; intégrité vérifiée par recoupement (36 011 épisodes, seq 179) |
| Brut événementiel campagnes 1–2.3 | Même corpus | Références historiques (EV5/EV6 rétrospectifs) pour comparaison ancien/nouveau régime de variables | Commité, consulté |
| Flux prospectif de confirmation T0 | Postérieur au gel 2.4 | **Interdit à cette campagne** (réservé, chantier A) | Non collecté, non utilisé |
| Holdout / périmètres post-2020 | Scellés | Aucun | Non accédé |
| FRED / exogène | Suspendu | Aucun | Non utilisé |

## Exigences d'exécution (rappel)

- Garde d'intégrité : partitions chargées = partitions attendues (282), journées
  recoupées avant synthèse ; en cas d'écart, suspension documentée, pas de
  publication partielle non étiquetée.
- Historiques de seuils causaux : les quantiles roulants (IMP : 60 jours ;
  CONS : 5 jours) consomment un début de corpus sans déclenchement possible —
  cette zone d'amorçage sera comptée et publiée (journées sans événement
  éligible par construction).
- Les chevauchements d'épisodes et la censure de fin de journée sont mesurés,
  pas corrigés par suppression silencieuse.
- Reproductibilité : moteur versionné, workflow à commit unique (patron
  campagnes 0/1 et reprise 2.3), journaux CI commités y compris en cas d'échec.
