# PHASE 11-A — PROCÈS-VERBAL DE GEL DÉFINITIF

**Date : 2026-11-13. Gel décidé par le responsable (ordre officiel de
gel Phase 11-A). Ce gel ne vaut pas autorisation d'exécution.**

## Document gelé

- `reports/meta_alpha/phase11/PHASE11_PROTOCOL.md`
- **SHA-256 définitif :
  `fdfb04ed71cd5317e9b342a408194ac79c42ab06188555cbc1fcb3367aa38f94`**
- Version initiale (seq296, conservée dans l'historique) :
  `0254ea47e6ba70d1bae8fe5cf0cb3795f238eeb1cbd774b6135b12c7618fd8b6`.
- Addendum documentaire intégré avant gel (seq297–298) : champs
  `extreme_minute_start_utc`, `extreme_available_at_utc`,
  `extreme_timestamp_resolution` (= M1) pour chaque extrême reconstruit
  depuis les barres M1 ; aucun instant intraminute exact déductible.

## Rapport de vérification documentaire (avant gel)

- Hash complet revérifié à l'octet près : conforme à la version
  définitive présentée et chaînée (seq298 ; préfixe `fdfb04ed`
  de l'ordre de gel).
- Contenu revérifié : effectifs conservés (F10-01 : 3 134 détectés /
  3 107 éligibles / 2 617 grappes ; F10-03 : 762 / 660 / 597),
  seuils Q95 gelés, grappes originales, huit horizons t+1…t+8, cinq
  catégories UTC, six archétypes descriptifs, graine bootstrap
  20261122, absence de p-value confirmatoire et de calcul de
  rentabilité ; aucune autre définition modifiée par l'addendum.
- Aucun calcul, aucune extraction, aucun accès au corpus IS ni au
  holdout n'ont été effectués pendant la conception et le gel.

## Traçabilité

- seq295 : mission de conception ; seq296 : préenregistrement du
  protocole initial (`0254ea47…`) ; seq297 : validation méthodologique
  du responsable et précision d'horodatage ; seq298 : addendum intégré ;
  seq299 : ordre de gel ; seq300 : **GEL DÉFINITIF**.
- Commits : conception `379057d2…` (Phase 10-A, historique),
  protocole 11-A `cf93af0…`, version définitive `f748052…` (vérifiés
  distants, arbre propre au moment du gel).

## Statuts après gel

- **PHASE 11-A : GELÉE DÉFINITIVEMENT.** Aucune modification
  silencieuse ni réécriture du protocole gelé ; toute évolution
  exigera une nouvelle décision formelle chaînée.
- PHASE 11-B — AUDIT DES MANIFESTES : NON AUTORISÉ.
- PHASE 11 — ANALYSE COMPORTEMENTALE : NON AUTORISÉE.
- L'exécution nécessitera une décision distincte du responsable.
  Interdictions maintenues : calcul et extraction sans ordre, holdout
  2020–2026, lancements des livrables d'exécution, stratégie,
  optimisation, promotion J2/J3, dépenses.
