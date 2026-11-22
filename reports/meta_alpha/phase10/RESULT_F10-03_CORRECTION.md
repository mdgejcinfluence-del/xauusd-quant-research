# PHASE 10 — F10-03 (CORRECTION seq289) : H4 |r| > Q95 causal — H4 suivante

**Statut : resultat historiquement evalue sur corpus IS (jamais une confirmation). Protocole gele PHASE 10-A seq283 + amendement cible seq289 (sha256 addendum 71196017…). Run cible 45011013927 vert (8 lots Kaggle, etape 2, synthese corrective).**

## Diagnostics de fenetre causale (amendement seq289)
- Barres examinees : 15195 ; fenetres examinees : 15195 (fenetre fixe de 250 barres precedentes, courante exclue, jamais etendue)
- Rendements valides au total : 3623693 ; NaN/non-finis : 143682 (3.81 % des fenetres cumulees)
- Fenetres INELIGIBLE_CAUSAL_WINDOW (< 200 valides) : 208 ; valides par fenetre : mediane 241, minimum 0
- Quantile Q95 : interpolation lineaire (type 7) sur les seules valeurs valides ; aucune imputation.

## Evenements et economie
- Detectes : 762 ; eligibles economiquement : 660 ; ineligibles/exclusions : 102/101
- Grappes : 597 ; part grappe dominante 0.0061 (alerte 5 % : False)
- Seuil Q95 median aux evenements : 69.57 bp ; spread median 2.310 bp ; C_ref = 4.010 bp (spread observe + 1,7 bp hypothetiques deduits une seule fois)
- Brut moyen -1.34 bp, median -3.80 ; net central moyen -3.04 bp, median -5.50 bp
- MAE par evenement : mediane 24.17, P90 73.74, ES90 126.09 bp ; par grappe : mediane 24.56, P90 73.45, ES90 125.83 bp
- Net moyen par ere (diagnostics non confirmatoires, sans p-value) : 2010_2013: -1.80 bp (n=263) ; 2014_2016: -4.11 bp (n=202) ; 2017_2020: -3.62 bp (n=195)

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
