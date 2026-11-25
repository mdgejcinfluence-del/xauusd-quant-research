# EUR-EDGE-02 — ADAPTATEURS FOURNISSEURS

Principe : un adaptateur par source, une sortie canonique unique (voir schéma). Remplacer un
fournisseur = écrire un adaptateur, jamais réécrire le moteur.

| Adaptateur | Entrée | Sortie | Statut |
|---|---|---|---|
| `dukascopy_bi5` | fichiers horaires .bi5 | ticks canoniques | implémenté (échantillon interne ; usage borné par la licence) |
| `cftc_tff` | zips annuels officiels | COT canonique | implémenté, 853 rapports |
| `ecb_sdmx` | API SDMX BCE | taux canoniques | implémenté (DFR vérifié) |
| `us_treasury` | TextView officiel | taux canoniques | implémenté (fichier brut vérifié, parse à finaliser) |
| `fred_mirror` | miroirs GitHub des séries Fed | taux canoniques | à fiabiliser (FRED direct injoignable du runner) |
| `bls_api` / `eurostat_api` | APIs officielles | macro canonique | en vérification CI |
| `mt5_demo` / `oanda_api` | flux du compte fondateur | ticks canoniques | spécifiés, en attente d'identifiants (jamais inventés) |
| `cme_6e` | produits licenciés | futures canoniques | BLOQUÉ licence — adaptateur non écrit |

Chaque adaptateur journalise : URL, horodatage de téléchargement, empreinte, lignes reçues,
lignes rejetées et motif. Aucun adaptateur ne « corrige » les écarts entre fournisseurs.
