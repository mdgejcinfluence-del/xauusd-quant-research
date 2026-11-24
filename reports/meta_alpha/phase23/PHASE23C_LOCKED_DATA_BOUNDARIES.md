# PHASE 23-C — FRONTIÈRES DES DONNÉES VERROUILLÉES

- `FOMC_DEVELOPMENT_EVENTS` : les 73 décisions FOMC 2010-2019 et leurs 73 témoins (Phase 23-B),
  consommés pour la conception et les audits. Interdits dans toute validation future.
- `FOMC_LOCKED_VALIDATION_EVENTS` : registre vide au gel (seq389) ; il ne recevra que des
  décisions FOMC postérieures au gel du protocole, horodatées avant toute lecture des résultats
  économiques associés. Aucune lecture exploratoire avant la taille minimale (81 événements,
  horizon 60 min) n'est autorisée ; seuls les contrôles de qualité des cotations le sont.
- Holdout 2020-2026 : définitivement fermé, aucune réutilisation.
- Aucun nouvel événement historique ne peut être ajouté à la population de développement.
- Les deux registres sont committés avec cette phase ; toute modification ultérieure doit passer
  par une nouvelle entrée au registre des essais.
