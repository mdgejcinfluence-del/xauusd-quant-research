# EUR-EDGE-02 — DÉCISION JURIDIQUE : SOURCE DE PRIX EUR/USD HISTORIQUE

Question : quelle source de ticks Bid/Ask EUR/USD 2010-2026 peut légalement être (a) acquise,
(b) stockée durablement, (c) hébergée sur Kaggle privé ?

| Voie | Acquisition | Stockage privé | Kaggle privé | Verdict |
|---|---|---|---|---|
| Dukascopy flux public, tel quel | Techniquement libre | **Interdit** (conditions : pas de base de données) | **Interdit** | SUSPENDU à accord écrit |
| Dukascopy avec accord écrit | Selon réponse | Selon réponse | Selon réponse | **Voie 1 — courrier préparé (DUKASCOPY_PERMISSION_REQUEST.md), signature fondateur uniquement** |
| Compte démo fondateur (JForex/OANDA/courtier MT5) | Conditions de compte | Généralement toléré pour usage personnel du titulaire | À vérifier selon courtier, jamais présumé | **Voie 2 — connecteurs prêts, identité fondateur requise** |
| API fournisseurs « gratuites » | Souvent compte requis | Rarement explicite | Rarement explicite | Aucune identifiée autorisant explicitement (a)+(b)+(c) |
| Archives publiques/universitaires | Cas par cas | Cas par cas | Cas par cas | Aucune archive EUR/USD tick 2010-2026 aux droits vérifiés n'a été identifiée |
| Datasets Kaggle/GitHub de tiers reprenant Dukascopy | Facile | Droits de l'uploader incertains, conditions Dukascopy inchangées | Non | REJETÉ (la republication par un tiers ne purge pas les droits) |
| Achat de données licenciées | CME/DataMine, vendeurs | Oui selon licence | Selon licence | INTERDIT (budget 0, aucune dépense autorisée) |

Décision : la recherche EUR/USD avance sur les blocs licites (COT, taux, macro) et sur
l'échantillon technique interne déjà mesuré ; **l'archive spot complète attend l'un des deux
actes fondateur** (envoi du courrier, ou ouverture d'un compte démo). Ce n'est pas un arrêt :
le moteur de recherche est construit et testé sur données synthétiques et sur l'échantillon,
de sorte que l'activation soit immédiate dès qu'une voie s'ouvre. Toute interprétation
extensive des conditions (« privé donc permis ») est refusée : une réponse Dukascopy limitée à
l'usage personnel local ne vaudra pas autorisation Kaggle.
