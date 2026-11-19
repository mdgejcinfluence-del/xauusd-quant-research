# PHASE 10 — RAPPORT DE SIMULATION STRUCTURELLE (hors budget, 0 essai)

Processus declare: bruit journalier calibre sur la vol predite F3, esperance mu IMPOSEE (pas mesuree). Regles 2-Step exactes (V2). 4000 trajectoires/politique, horizon 1000 j.

## E1 — P(passage) par politique (P1 x P2 entre parentheses)

| mu impose | politique | filtres | P1 | P1xP2 | ruine P1 |
|---|---|---|---|---|---|
| mu_-2bp (couts seuls) | fixe | sans filtre | 0.317 | 0.185 | 0.683 |
| mu_-2bp (couts seuls) | fixe | filtres M1/M5+F7 | 0.282 | 0.164 | 0.718 |
| mu_-2bp (couts seuls) | kelly_fraction | sans filtre | 0.000 | 0.000 | 0.000 |
| mu_-2bp (couts seuls) | kelly_fraction | filtres M1/M5+F7 | 0.000 | 0.000 | 0.000 |
| mu_-2bp (couts seuls) | f3_asservi | sans filtre | 0.323 | 0.197 | 0.677 |
| mu_-2bp (couts seuls) | f3_asservi | filtres M1/M5+F7 | 0.305 | 0.175 | 0.695 |
| mu_-2bp (couts seuls) | jeu_hardi_borne | sans filtre | 0.203 | 0.023 | 0.723 |
| mu_-2bp (couts seuls) | jeu_hardi_borne | filtres M1/M5+F7 | 0.198 | 0.023 | 0.721 |
| mu_0 | fixe | sans filtre | 0.398 | 0.260 | 0.602 |
| mu_0 | fixe | filtres M1/M5+F7 | 0.375 | 0.241 | 0.625 |
| mu_0 | kelly_fraction | sans filtre | 0.000 | 0.000 | 0.000 |
| mu_0 | kelly_fraction | filtres M1/M5+F7 | 0.000 | 0.000 | 0.000 |
| mu_0 | f3_asservi | sans filtre | 0.391 | 0.254 | 0.610 |
| mu_0 | f3_asservi | filtres M1/M5+F7 | 0.388 | 0.254 | 0.613 |
| mu_0 | jeu_hardi_borne | sans filtre | 0.226 | 0.027 | 0.685 |
| mu_0 | jeu_hardi_borne | filtres M1/M5+F7 | 0.221 | 0.027 | 0.697 |
| mu_+2bp | fixe | sans filtre | 0.448 | 0.307 | 0.552 |
| mu_+2bp | fixe | filtres M1/M5+F7 | 0.486 | 0.350 | 0.513 |
| mu_+2bp | kelly_fraction | sans filtre | 0.450 | 0.312 | 0.550 |
| mu_+2bp | kelly_fraction | filtres M1/M5+F7 | 0.476 | 0.342 | 0.523 |
| mu_+2bp | f3_asservi | sans filtre | 0.457 | 0.324 | 0.543 |
| mu_+2bp | f3_asservi | filtres M1/M5+F7 | 0.476 | 0.332 | 0.524 |
| mu_+2bp | jeu_hardi_borne | sans filtre | 0.240 | 0.033 | 0.667 |
| mu_+2bp | jeu_hardi_borne | filtres M1/M5+F7 | 0.238 | 0.034 | 0.667 |

## E2 — Panier controle vs chassis
```json
{
 "panier_controle_declare (92% +0,10% / 7% -0,8% / 1% -4,5% stop dur)": {
  "P_passer_P1": 0.0,
  "P_ruine": 0.99975
 },
 "esperance_journaliere_panier_bp": -0.8999999999999995
}
```

Le panier affiche un taux de reussite quotidien eleve mais son esperance declaree est negative et sa queue (-4,5%) touche directement la limite journaliere: compare sa P(passage) a la meilleure ligne E1 a mu equivalent.

## E3 — Arithmetique du ticket
```json
{
 "frais_bas_$32 (repere Standard 5K) x gain_finance_$100": {
  "EV_a_mu_-2bp_meilleure_politique": -12.34,
  "P1xP2": 0.1966
 },
 "frais_bas_$32 (repere Standard 5K) x gain_finance_$200": {
  "EV_a_mu_-2bp_meilleure_politique": 7.31,
  "P1xP2": 0.1966
 },
 "frais_bas_$32 (repere Standard 5K) x gain_finance_$400": {
  "EV_a_mu_-2bp_meilleure_politique": 46.62,
  "P1xP2": 0.1966
 },
 "frais_median_$75 x gain_finance_$100": {
  "EV_a_mu_-2bp_meilleure_politique": -55.34,
  "P1xP2": 0.1966
 },
 "frais_median_$75 x gain_finance_$200": {
  "EV_a_mu_-2bp_meilleure_politique": -35.69,
  "P1xP2": 0.1966
 },
 "frais_median_$75 x gain_finance_$400": {
  "EV_a_mu_-2bp_meilleure_politique": 3.62,
  "P1xP2": 0.1966
 },
 "frais_haut_$150 x gain_finance_$100": {
  "EV_a_mu_-2bp_meilleure_politique": -130.34,
  "P1xP2": 0.1966
 },
 "frais_haut_$150 x gain_finance_$200": {
  "EV_a_mu_-2bp_meilleure_politique": -110.69,
  "P1xP2": 0.1966
 },
 "frais_haut_$150 x gain_finance_$400": {
  "EV_a_mu_-2bp_meilleure_politique": -71.38,
  "P1xP2": 0.1966
 },
 "_meilleure_politique_mu_-2bp": "mu_-2bp (couts seuls)|f3_asservi|sans filtre",
 "_regle_coherence": "frais engages seulement si P(echec) <= 25% (P(passage total) >= 75%) - aucune politique a mu<=0 ne l'approche"
}
```

## VERDICT E3 (une ligne)
A esperance de marche nulle ou negative (couts), aucune politique ne porte P(passage total) pres des 75% exiges par la regle de coherence: le ticket est une loterie a prix connu, pas un achat rationnel - sauf a disposer d'une esperance directionnelle reelle, que 131 sequences n'ont pas trouvee.

## Plafond honnete de la politique optimale
La theorie des barrieres le disait (a esperance nulle, P(+a avant -b) = b/(a+b) ne depend pas du calibrage): le dimensionnement change le chemin, la duree et la queue - pas l'esperance. F3 asservi et filtres reduisent la ruine marginale; le jeu hardi borne maximise la probabilite de passage a mu donne en concentrant le risque; Kelly a mu=0 refuse de jouer (taille 0) - c'est aussi un resultat. Aucune politique ne cree le mu qui manque.