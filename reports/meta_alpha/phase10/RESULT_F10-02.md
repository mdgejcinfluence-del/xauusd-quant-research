# PHASE 10 — F10-02 : H1 franchissement extremes 20 barres — signe cumule 4 barres

**Statut : resultat historiquement evalue sur corpus IS (jamais une confirmation). Protocole gele PHASE 10-A seq283 ; preflight seq285 ; ordre seq284.**

- Evenements detectes : 5652 ; eligibles : 5477 ; ineligibles/exclusions : 175/164
- Grappes (composantes connexes) : 2972 ; part grappe dominante : 0.0020 (alerte 5 % : False)
- Spread median observe a l'evenement : 2.308 bp ; C_ref = spread + 1,7 bp hypothetiques (commission 0,7 + slippage 1,0, deduits une seule fois) = 4.008 bp
- Brut moyen -2.81 bp, median -4.92 bp ; net central moyen -4.51 bp, median -6.62 bp (Bid/Ask, spread deja dans les prix)
- MAE mediane 23.83 bp ; P90 70.63 ; ES90 107.27 (par grappe : mediane 35.26, P90 83.57, ES90 125.82)
- Net moyen par ere : 2010_2013: -5.55 bp (n=2297) ; 2014_2016: -3.70 bp (n=1483) ; 2017_2020: -3.81 bp (n=1697) (diagnostics non confirmatoires, sans p-value)

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
