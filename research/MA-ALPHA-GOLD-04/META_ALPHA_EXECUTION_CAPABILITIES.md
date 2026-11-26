# CAPACITÉS D'EXÉCUTION RÉELLES DE META ALPHA

Aujourd'hui : ordres au marché simulés sur flux Bid/Ask Dukascopy (niveau B), horodatage UTC,
entrée/sortie au premier tick ≤ 60 s, NON_EXECUTION comptée — chaîne implémentée et auto-testée
pour le protocole prospectif. Absents : compte chez un courtier, ordres limites réels et leurs
fills, file d'attente, markouts d'exécution, marges, financement réel du compte cible. Le courtier
du fondateur n'étant pas désigné, l'architecture reste fournisseur-indépendante : toute
intégration future exigera ses spécifications écrites (spread par session, commission, swap,
slippage observé, politique de gaps et de stops) avant la moindre conclusion économique le
concernant. Un CFD market-maker internalise le flux : « fournir de la liquidité » y signifie
être la contrepartie du courtier, pas du marché.
