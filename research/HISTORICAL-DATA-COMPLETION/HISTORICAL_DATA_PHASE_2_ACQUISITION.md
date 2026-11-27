# PHASE 2 — STRATÉGIE D'ACQUISITION

Dukascopy (primaire, `DUKASCOPY_PRIMARY`) : flux public .bi5 horaire déjà éprouvé par
`ci_tools/edge02_dukascopy.py` (Bid/Ask ms UTC, décodeur 20 octets, retries ; publication par
lots avec délais — les heures récentes peuvent répondre 503 puis paraître). Complétion :
`ci_tools/hist_completion.py`, idempotent par manifeste d'heures, brut préservé, normalisation
après contrôle, **aucun écrasement des 348 partitions** (lots mensuels séparés 2026-10/2026-11).
HistData (`HISTDATA_SECONDARY`) : pilote CI = HTTP 200/0 octet depuis les runners (anti-robot
documenté seq429-430) ; l'adaptateur reste utilisable depuis un poste non filtré ; tant qu'aucun
fichier réel n'est inspecté, HistData ne fournit **rien** au corpus et n'est pas comptée.
Autres fournisseurs : aucun ajout sans valeur démontrée (profondeur, Bid/Ask, licence) ;
budget 0 €, aucun achat. Règle absolue : une observation externe ne remplace jamais une
observation Dukascopy certifiée ; classes de provenance conservées par fichier.
