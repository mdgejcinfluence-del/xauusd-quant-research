# MA-EDGE-02 — PRÉENREGISTREMENT DES EXPÉRIENCES EXP-08 À EXP-12

Écrit et enregistré au registre (seq411) **avant tout calcul** de ces expériences.
Toutes portent sur des données consommées 2010-2019 : statut `EXPLORATORY_POST_HOC`,
aucune ne peut valider une stratégie. Les prix de barres sont des Mid ; tout résultat de
famille nouvelle est un **majorant** auquel on applique des scénarios de coût forfaitaires
de 0 / 2 / 4 bp par aller-retour (le coût tick réel documenté en 24-D vaut ≈ spread médian
de l'événement + scénarios S1/S2 ; un majorant positif sous 4 bp ne suffit pas à promouvoir).
Périodes fixes : découverte 2010-2015, contrôle 2016-2017, rejeu 2018-2019. Un mécanisme
n'est « cohérent » que si le signe de l'effet est le même sur les trois périodes.

- **EXP-08 (H17, trajectoire précoce)** — population : les 1 124 événements sélectionnés 24-D
  (PnL_S2 tick réel connu). Variables causales reconstruites depuis le barset : rendement Mid
  directionnel à +4 barres (60 min), MFE/MAE intra-fenêtre (hauts/bas Mid). Question : l'état à
  +60 min sépare-t-il le PnL terminal ? Sortie simulée à +60 min (clôture Mid) présentée à titre
  de majorant descriptif uniquement.
- **EXP-09 (familles nouvelles)** — population : barres d'impulsion Q90/250 du barset, horloge
  08:00-16:00 UTC (primaire). Règles figées avant calcul :
  A continuation (entrée clôture d'impulsion, sens de l'impulsion, sortie +8 et +32 barres) ;
  B fade (sens opposé, mêmes horizons) ; C confirmation locale (entrée à la clôture de la barre
  suivante si elle clôture au-delà de la clôture d'impulsion dans le sens de l'impulsion, sortie
  +8 barres après l'entrée, sinon abstention) ; D entrée différée (entrée à +4 barres si le prix
  a retracé moins de 50 % du corps de l'impulsion, sens de l'impulsion, sortie +8 barres).
  Placebo : 200 tirages d'instants aléatoires appariés en heure UTC, sens aléatoire, mêmes
  horizons ; l'effet doit dépasser le percentile 97,5 du placebo pour être discuté.
- **EXP-10 (géométrie du risque)** — événements réintégrés : risque initial = distance
  t_decision → niveau d'invalidation structurelle (extrême de la barre d'impulsion) ; potentiel =
  distance t_decision → référence favorable ; ratio potentiel/risque en terciles dont les bornes
  sont fixées sur 2010-2015. Lectures : fréquence Y (tous réintégrés) et PnL_S2 (sélectionnés).
- **EXP-11 (asymétrie des excursions)** — impulsions : distributions MFE/MAE directionnels à
  4/8/32 barres, par sens et par tercile d'amplitude du corps (bornes 2010-2015) ; test de
  symétrie MFE vs MAE (médianes et quantiles appariés par événement).
- **EXP-12 (abstention par coût, H19 historique)** — événements sélectionnés : `spread_median_bp`
  de la barre de décision (barset, coût historique réel) en terciles (bornes fixées sur les
  événements 2010-2015 sélectionnés s'ils existent, sinon sur tous les réintégrés horloge) ;
  lecture PnL_S2 et PnL_S0−S2 (coût effectivement payé).

Décisions interdites après coup : changer les horizons, les seuils 50 %, les bornes de terciles
ou la population pour améliorer un résultat. Tout écart sera consigné comme nouvelle expérience.
