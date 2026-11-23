# PHASE 19-A — INVENTAIRE DES SOURCES ET DE LEUR ÉTAT D'USAGE

*Métadonnées et manifestes uniquement (footers d'inventaire, états de migration, rapports) ; aucune valeur de cotation lue, aucun accès au holdout.*

## 1. Sources historiques existantes (toutes consommées)
- **Partitions IS 2010–2020** : 282 partitions (Kaggle privé `xauusd-is-b01..b07` + `xauusd-is-missing13`), schéma `timestamp_utc, bid, ask` (+ Mid dérivé). Utilisées par les Phases 10 à 18 : conception, sélection, entraînement et évaluation y ont toutes eu lieu. **Aucune sous-période IS ne peut être déclarée intacte.**
- **Partitions holdout 2020–2026** : 66 partitions vérifiées 66/66 (seq325) et **consommées** par la confirmation unique 12-C.2 (seq326). Réutilisation interdite sous toutes formes, y compris comme « nouvelle » validation d'un autre modèle.
- **Inventaire global** (`INVENTORY_348_EXHAUSTIVE.json`, métadonnées de footers) : 348 partitions couvrant **2010-01-04 → 2026-09-30**, deux signatures de schéma. Il n'existe dans les sources **aucune période postérieure à septembre 2026 ni antérieure à 2010**.

## 2. Sources nouvelles envisageables
| Option | État | Indépendance |
|---|---|---|
| Période historique non consultée dans les sources actuelles | **Inexistante** (couverture 2010–2026 entièrement consommée) | — |
| Même historique chez un autre fournisseur | Existerait peut-être | **Non indépendante** : mêmes événements déjà utilisés pour conception et sélection (l'ordre de mission l'exclut explicitement) |
| Cotations XAU/USD postérieures à la fin de couverture (à partir d'octobre 2026) | **N'existent pas encore** dans les actifs du programme | Indépendantes par construction si capturées prospectivement sous contrat gelé |
| Flux d'exécution réel (ordres, fills, commissions) | Inexistant (aucun envoi d'ordre jamais effectué ; schéma tick sans exécution) | Ne peut naître que d'une capture future, sans engagement de capital dans le cadre de la recherche (comptes de démonstration/simulation si le propriétaire en décide ainsi, hors présente autorisation) |

## 3. Contraintes d'accès constatées
Budget 0 FCFA ; aucune source payante ; l'environnement d'exécution du programme n'a pas d'accès à un flux de cotations en direct (accès réseau limité aux hébergeurs de code et de paquets). La capture prospective devra donc être opérée par l'infrastructure du propriétaire (terminal/broker ou fournisseur gratuit documenté), selon le contrat de la présente phase, avec provenance et horodatage de réception conservés.

## 4. Conclusion d'inventaire
Aucune donnée indépendante n'est disponible immédiatement ; la seule voie non contaminée est une **capture prospective** postérieure à la couverture actuelle, séparée dès la conception en développement et validation verrouillée. Verdict : `DATA_CAPTURE_REQUIRED`.
