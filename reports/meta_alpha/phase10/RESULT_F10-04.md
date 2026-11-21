# PHASE 10 — F10-04 : H4 franchissement extremes 30 barres — signe cumule 6 barres (24 h)

**Statut : resultat historiquement evalue sur corpus IS (jamais une confirmation). Protocole gele PHASE 10-A seq283 ; preflight seq285 ; ordre seq284.**

- Evenements detectes : 1257 ; eligibles : 1003 ; ineligibles/exclusions : 254/251
- Grappes (composantes connexes) : 508 ; part grappe dominante : 0.0100 (alerte 5 % : False)
- Spread median observe a l'evenement : 2.297 bp ; C_ref = spread + 1,7 bp hypothetiques (commission 0,7 + slippage 1,0, deduits une seule fois) = 3.997 bp
- Brut moyen 0.07 bp, median -1.22 bp ; net central moyen -1.63 bp, median -2.92 bp (Bid/Ask, spread deja dans les prix)
- MAE mediane 49.77 bp ; P90 139.06 ; ES90 222.96 (par grappe : mediane 74.77, P90 164.14, ES90 262.93)
- Net moyen par ere : 2010_2013: 2.44 bp (n=405) ; 2014_2016: -4.22 bp (n=280) ; 2017_2020: -4.55 bp (n=318) (diagnostics non confirmatoires, sans p-value)

## Portes economiques (avant toute inference, arret a la premiere echouee)
- P1_magnitude : True
- P2_esperance : False
- P3_colonne : False
- P3_queue_evenement : False
- P3_queue_grappe : False
- P4_effectifs : True
- Arret : PORTE 2 esperance nette centrale <= 0

## Verdict : NEGATIF ECONOMIQUE

Resultats IS = « historiquement evalues », jamais des confirmations. Aucune promotion, aucune strategie. Voir PHASE10_GLOBAL_REPORT.md pour les limitations.
