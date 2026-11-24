# EUR-EDGE-01 — AUDIT MACRO ET TAUX

Acquis/vérifiés en CI : taux de dépôt BCE via API SDMX officielle (clé `FM…KR.DFR.LEV`,
1,8 Mo, OK) ; courbe quotidienne du Trésor américain via l'endpoint officiel (OK, 223 Ko).
Échecs documentés depuis le runner : FRED (timeouts d'egress — contournement par miroirs
GitHub ou H.15 de la Fed, à fiabiliser), DBnomics (404, chemin de série à corriger).
Règles adoptées : chaque série porte source, date de téléchargement et millésime ; DEXUSEU est
un taux de référence de midi à New York, **jamais** un prix exécutable ; les différentiels ne
seront calculés qu'entre séries de disponibilité connue (BCE : date d'annonce ; Trésor/Fed :
publication quotidienne). Le Bund allemand reste à sourcer licitement (Bundesbank/FRED miroir).
Publications macro (valeur, parution, révisions, première valeur) : bloc à construire ensuite
sur sources officielles BCE/BLS/BEA/Eurostat ; **aucun consensus historique ne sera fabriqué** —
les surprises resteront incalculables tant qu'un consensus vérifiable n'existe pas.
