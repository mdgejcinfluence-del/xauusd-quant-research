# META ALPHA ERE — CONTRATS DE DONNÉES

Chaque objet échangé porte : identifiant, version de schéma,
provenance (source, hash), segment de données autorisé, niveau de
preuve, et journal des transformations. Un champ absent est explicite
(`ABSENT`), jamais rempli par défaut.

## Objets principaux

- `TraderDossier` (A) : transactions normalisées (timestamp, sens,
  prix, volume, plateforme, fuseau déclaré/incertain), bio et stats
  publiques marquées UNVERIFIED, inventaire présent/absent/incertain/
  contradictoire. Normalisation : prix en unités source + conversion
  documentée, fuseaux convertis en UTC avec drapeau de confiance.
- `BehaviorProfile` (B) : faits observés (avec pointeurs vers les
  transactions) séparés des interprétations (avec niveau de confiance).
- `HypothesisSet` (C) : fiches hypothèses (voir HYPOTHESIS_ENGINE_DESIGN).
- `KnowledgeRef` (D) : source, type, date, qualité, limites, modules concernés.
- `ExperimentPlan` (E) : protocole gelé (définitions, grilles fixées,
  segment autorisé, critères pré-déclarés), hash et seq du registre.
- `SignatureReport` (F) : mesures par segment, définitions exactes,
  censures, intervalles, fichiers de sortie et leurs SHA-256.
- `ModelDossier` (G) : voir ECONOMIC_IDENTIFICATION_ENGINE.
- `EngineSpec` (H) : règles propres, paramètres gelés et leur hash.
- `ValidationVerdict` (I) : critères pré-déclarés vs résultats, par segment.

## Invariants transversaux

1. Aucun objet ne change de niveau de preuve en transit (une hypothèse
   reste `COMPATIBLE` jusqu'au verdict du module G).
2. Toute donnée de marché référence son segment (découverte /
   construction / validation / prospectif) et sa source (Dukascopy
   certifié, HFM, tiers non certifié interdit pour valider).
3. Les coûts sont des champs séparés (brut, spread, commission,
   slippage, net) — jamais un seul nombre opaque, jamais comptés deux fois.
4. Le réel, l'affiché, le simulé et le contrefactuel sont des types
   distincts, non mélangeables dans un même agrégat.
