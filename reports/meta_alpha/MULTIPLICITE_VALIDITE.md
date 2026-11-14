# Validité mathématique du dispositif de multiplicité (documentée, testée, sans garantie inventée)

## Dispositif retenu (gate_engine_v2.py)
Benjamini-Yekutieli (BY) sur les p-values de la vague + compteur cumulatif
m = total des hypothèses de toutes les vagues (127 après P3-002).

## Ce qui est démontré (littérature)
- BY contrôle le FDR à l'espérance sous **dépendance arbitraire** entre les tests,
  pour une famille de tests **fixée avant observation des données** de cette vague.
- BH ne le garantit que sous indépendance/PRDS — insuffisant ici (labels
  chevauchants, features corrélées, mêmes données).

## Ce qui N'EST PAS garanti — et ne sera jamais affirmé
- La **sélection adaptative entre vagues** (la vague n+1 dépend des résultats de la
  vague n) sort du cadre BY comme de tout FDR standard: aucune garantie formelle de
  contrôle du taux de fausses découvertes global n'existe sans cadre supplémentaire
  (alpha-investing généralisé / e-values offrent des garanties différentes, FDR online).
- Le compteur cumulatif appliqué à BY est une **pénalité conservative** (elle ne peut
  que durcir les seuils); ce n'est pas un théorème. Le dire serait une fabrication.
- Les p-values elles-mêmes reposent sur des t naïfs avec labels chevauchants:
  erreurs-types sous-estimées, donc p optimistes. BY ne répare pas des p invalides.

## Conséquences imposées au système
1. Le gate est un **filtre anti-bruit**, jamais une preuve d'edge.
2. Tout survivant exige une confirmation sur données indépendantes (OOS chronologique
   purgé; Holdout seulement en évaluation finale scellée).
3. Le compteur cumulatif ne se remet jamais à zéro; chaque vague durcit la suivante.
4. Voie d'amélioration identifiée (à justifier avant adoption): e-values / tests
   séquentiels toujours valides, adaptés à la recherche adaptative; non implémenté.

## Tests exécutés
- gate_engine_v2 sur les résultats d'origine P3-001 (m_prior=126): **0 survivant**
  (conforme au verdict historique, par une voie encore plus stricte).
- gate_engine_v2 sur P4-001: **REJETE** (conforme).
- anomaly_registry.py: refus d'une anomalie incomplète (14 champs manquants listés),
  acceptation d'une anomalie complète, statut DESCRIPTIVE par défaut (jamais
  prédictive automatiquement), identifiants immuables.
