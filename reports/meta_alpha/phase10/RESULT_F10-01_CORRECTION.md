# PHASE 10 — F10-01 (CORRECTION seq289) : H1 |r| > Q95 causal — rendement signe barre H1 suivante

**Statut : resultat historiquement evalue sur corpus IS (jamais une confirmation). Protocole gele PHASE 10-A seq283 + amendement cible seq289 (sha256 addendum 71196017…). Run cible 45011013927 vert (8 lots Kaggle, etape 2, synthese corrective).**

## Diagnostics de fenetre causale (amendement seq289)
- Barres examinees : 59184 ; fenetres examinees : 59184 (fenetre fixe de 250 barres precedentes, courante exclue, jamais etendue)
- Rendements valides au total : 14206360 ; NaN/non-finis : 558265 (3.78 % des fenetres cumulees)
- Fenetres INELIGIBLE_CAUSAL_WINDOW (< 200 valides) : 202 ; valides par fenetre : mediane 239, minimum 0
- Quantile Q95 : interpolation lineaire (type 7) sur les seules valeurs valides ; aucune imputation.

## Evenements et economie
- Detectes : 3134 ; eligibles economiquement : 3107 ; ineligibles/exclusions : 27/23
- Grappes : 2617 ; part grappe dominante 0.0023 (alerte 5 % : False)
- Seuil Q95 median aux evenements : 32.27 bp ; spread median 2.302 bp ; C_ref = 4.002 bp (spread observe + 1,7 bp hypothetiques deduits une seule fois)
- Brut moyen -1.73 bp, median -4.29 ; net central moyen -3.43 bp, median -5.99 bp
- MAE par evenement : mediane 17.19, P90 45.11, ES90 70.60 bp ; par grappe : mediane 18.58, P90 47.07, ES90 72.51 bp
- Net moyen par ere (diagnostics non confirmatoires, sans p-value) : 2010_2013: -3.46 bp (n=1280) ; 2014_2016: -3.26 bp (n=904) ; 2017_2020: -3.56 bp (n=923)

## Portes economiques (avant inference, arret a la premiere echouee)
- P1_magnitude : True
- P2_esperance : False
- P3_colonne : False
- P3_queue_evenement : False
- P3_queue_grappe : False
- P4_effectifs : True
- Arret : PORTE 2 esperance nette centrale <= 0
- Inference : non autorisee (arret aux portes) — aucune p-value produite ; BY m = 6 conserve (jamais reduit a 2).

## Verdict : NEGATIF ECONOMIQUE

Resultat IS = « historiquement evalue », jamais une confirmation. Aucune promotion, aucune strategie. Voir PHASE10_CORRECTION_REPORT.md.
