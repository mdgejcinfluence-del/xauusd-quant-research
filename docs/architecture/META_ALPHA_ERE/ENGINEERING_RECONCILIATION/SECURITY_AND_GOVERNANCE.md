# RÉCONCILIATION — SÉCURITÉ ET GOUVERNANCE

## Réel [DÉPÔT]

Secrets dans GitHub Actions uniquement (Kaggle, Drive via gdown) ;
aucun jeton dans le dépôt ni dans les artefacts ; `main` jamais
touchée ; moteurs gelés V1/V2-F2 et checkpoints certifiés immuables,
hashes testés ; registre chaîné append-only ; accès HFM en lecture
publique seulement ; aucun ordre réel. La CI a déjà rencontré des
limites d'accès (403 sur certains endpoints) — documentées, jamais
contournées.

## Menaces et contrôles (réconciliation)

| Menace | Contrôle (statut) |
|---|---|
| Fuite du futur (look-ahead) | définitions causales, `dropna`, pas de `bfill` — pratiqué ; tests métamorphiques « modifier le futur ne change pas le passé » à formaliser [EXT] |
| Contamination des zones protégées | allowlist positive des segments ; le prospectif ME-001 n'est ouvert qu'à sa règle d'arrêt ; aucun accès pendant cette mission |
| Fuite par les métriques | les performances prospectives ne sont ni lues ni citées dans les protocoles de découverte |
| Secret dans Kaggle | **aucun PAT GitHub dans Kaggle** ; Kaggle ne reçoit que ses propres accès via la CI |
| Écriture sur zones protégées | partitions certifiées en lecture seule ; moteurs gelés protégés par tests de hash ; écritures CI limitées aux chemins de résultats |
| Injection par biographie/texte | tout texte de trader est une *donnée* (N0), jamais une instruction ; aucun `eval` issu de texte |
| Supply chain | pas d'installation dans cette mission ; règle future : lock avec hashes, audit de licences (vectorbt/Backtrader exclus) |
| Corruption d'artefacts | SHA-256 des sorties vérifié avant publication ; un octet corrompu invalide la preuve |
| Publication accidentelle | datasets Kaggle privés vérifiés (`kaggle_verify.py`) ; jamais de corpus rendu public pour gagner de l'espace |
| Réécriture d'historique | le registre chaîné détecte toute modification d'une entrée passée (test de chaîne à chaque mission) |

## Gouvernance inchangée

Drift Guard avant chaque mission (VERT pour celle-ci) ; décisions
structurantes au journal ; validations du fondateur pour : porte H,
dépenses, doctrine, accès aux zones protégées, adoption d'un nouveau
plan de calcul. Le présent dossier ne supprime ni ne contourne aucun
de ces contrôles — il les cite comme contraintes de conception.
