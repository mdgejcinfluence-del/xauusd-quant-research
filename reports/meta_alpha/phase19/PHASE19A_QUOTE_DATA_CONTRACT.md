# PHASE 19-A — CONTRAT DE DONNÉES DE COTATIONS (nouvelle capture)

**Objet** : garantir que toute cotation future est née indépendante de la recherche passée et le reste. **Aucune capture n'est démarrée par la présente phase.**

1. **Provenance** : fournisseur et produit documentés (identifiant de source dans chaque enregistrement) ; un changement de fournisseur crée une nouvelle source, jamais fusionnée sans traçabilité.
2. **Contenu minimal** : `timestamp_utc`, Bid, Ask ; horodatage de réception et séquence de mise à jour lorsqu'ils existent ; interruptions/reprises consignées comme événements. Aucune promesse de volume ni de profondeur si la source n'en fournit pas — les limites du schéma `timestamp, bid, ask` des phases précédentes restent la référence honnête par défaut.
3. **Intégrité** : flux brut immuable (écriture unique, SHA-256 par lot journalisé), horloges UTC, doublons et trous conservés et comptés, jamais complétés silencieusement.
4. **Séparation dès la naissance** : chaque lot est affecté à sa naissance à `NEW_DEVELOPMENT_DATA` ou `NEW_LOCKED_VALIDATION_DATA` selon le plan de séparation, avant tout examen de contenu économique ; l'affectation est chaînée au registre.
5. **Interdits** : aucun mélange avec les partitions 2010–2026 sans traçabilité par enregistrement ; aucune lecture de la population verrouillée avant le gel d'un candidat ; aucune utilisation des résultats du holdout consommé pour paramétrer la capture.
