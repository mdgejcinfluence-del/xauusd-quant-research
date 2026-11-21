# PHASE 10 — F10-05 : D1 |r| > Q90 causal — jour suivant

**Statut : resultat historiquement evalue sur corpus IS (jamais une confirmation). Protocole gele PHASE 10-A seq283 ; preflight seq285 ; ordre seq284.**

- Evenements detectes : 246 ; eligibles : 184 ; ineligibles/exclusions : 62/62
- Grappes (composantes connexes) : 162 ; part grappe dominante : 0.0163 (alerte 5 % : False)
- Spread median observe a l'evenement : 2.358 bp ; C_ref = spread + 1,7 bp hypothetiques (commission 0,7 + slippage 1,0, deduits une seule fois) = 4.058 bp
- Brut moyen -14.49 bp, median -11.87 bp ; net central moyen -16.19 bp, median -13.57 bp (Bid/Ask, spread deja dans les prix)
- MAE mediane 67.16 bp ; P90 192.50 ; ES90 323.48 (par grappe : mediane 65.73, P90 193.30, ES90 333.35)
- Net moyen par ere : 2010_2013: -8.09 bp (n=69) ; 2014_2016: -23.27 bp (n=57) ; 2017_2020: -18.87 bp (n=58) (diagnostics non confirmatoires, sans p-value)

## Portes economiques (avant toute inference, arret a la premiere echouee)
- P1_magnitude : True
- P2_esperance : False
- P3_colonne : False
- P3_queue_evenement : False
- P3_queue_grappe : False
- P4_effectifs : False
- Arret : PORTE 2 esperance nette centrale <= 0

## Verdict : NEGATIF ECONOMIQUE

Resultats IS = « historiquement evalues », jamais des confirmations. Aucune promotion, aucune strategie. Voir PHASE10_GLOBAL_REPORT.md pour les limitations.
