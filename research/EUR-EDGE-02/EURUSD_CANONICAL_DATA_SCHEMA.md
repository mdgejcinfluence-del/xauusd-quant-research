# EUR-EDGE-02 — SCHÉMA CANONIQUE EUR/USD (indépendant du fournisseur)

Chaque enregistrement, quelle que soit la source, porte :
`instrument, provider, ts_source, ts_utc, ts_publication, ts_telechargement, bid, ask,
mid_derived, spread, unite_prix, convention_origine, version_donnee, statut_qualite`.

Extensions par famille (jamais écrasées par le schéma commun) :
- **Futures** : `echeance_contrat, code_contrat, multiplicateur, devise_cotation` — série
  continue interdite sans règle de rollover documentée.
- **Macro** : `periode_reference, date_publication_utc, valeur_premiere, valeur_revisee,
  date_revision, vintage_telechargement` — la première valeur n'est jamais remplacée.
- **COT** : `semaine_position (mardi), date_publication, available_from`.
- **Taux** : `date_observation, date_publication, serie_id, source_url`.

Unités EUR/USD : prix décimal 5 chiffres ; pip = 0,0001 (pipette = 0,00001) ; spreads
exprimés en pips ET en bp relatifs (champ explicite) ; rendements en bp logarithmiques.
`mid_derived` est toujours calculé, jamais confondu avec un prix coté.
