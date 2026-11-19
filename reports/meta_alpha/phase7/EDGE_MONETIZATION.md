# EDGE MONETIZATION — Phase 7 Axe 2 (simulation pure, 0 essai)

Modeles geles, aucune donnee nouvelle. Regles 2-Step Pro OWNER_CONFIG_V2; cout aller-retour deja inclus dans les flux nets simules (4,7 bp par trade suppose dans mu).

## F3 dans le challenge (flux synthetiques declares: bruit calibre sur la vol predite F3, esperance mu imposee)

| mu impose (bp/j) | P(passage P1) sans F3 | P(passage P1) avec sizing vol-cible F3 |
|---|---|---|
| mu_0bp | 0.417 | 0.416 |
| mu_2bp | 0.696 | 0.712 |
| mu_5bp | 0.780 | 0.794 |

Lecture: a esperance imposee egale, le sizing vol-cible F3 ne cree aucune esperance; il regularise le risque journalier (moins de jours extremes), ce qui deplace legerement la probabilite de passage/survie aux regles -4%/-10%. Sans strategie directionnelle a servir, mu=0 reste mu=0: la probabilite de passage a mu=0 est celle du hasard moins les couts.

## F7 en filtre d execution (carte des couts atlas)
```json
{
 "part_heures_saut": 0.018192419825072886,
 "spread_median_saut_bp": 2.65418351618605,
 "spread_median_calme_bp": 2.324825104742105,
 "spread_p95_saut_bp": 4.668346162197464,
 "F7_gele": "AUC OOF 0,684; lift 2,85x @ top 5% (F7_RESULTS.json, modele gele - aucun score recalcule ici)",
 "exces_spread_par_execution_evites_bp": 0.3293584114439452,
 "lecture": "en n'executant pas dans les fenetres flaggees (top 5% du score F7, qui concentrent 2,85x le taux de sauts), on evite en mediane l'exces de spread ci-dessus par execution reportee; c'est un cout evite, pas un gain: cela suppose un report d'execution acceptable pour la strategie servie."
}
```

## VERDICT HONNETE (exige par l ordre)
Sans instrument de volatilite dans notre univers (pas d options), F3 et F7 ne monetisent que via timing/sizing au service d'une strategie directionnelle - jamais seuls. F3 vaut une regularisation du risque (chiffree ci-dessus), F7 vaut un cout d'execution evite par trade reporte (ci-dessus). Aucun des deux ne produit d'esperance: ce sont des actifs de service, exactement comme le chassis. Toute strategie future (voie B proprietaire incluse) les consomme comme tels; aucun frais de challenge ne peut etre justifie par F3/F7 seuls.