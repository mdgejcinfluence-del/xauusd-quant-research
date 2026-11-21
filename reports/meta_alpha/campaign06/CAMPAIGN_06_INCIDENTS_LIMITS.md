# CAMPAGNE 6 — REGISTRE DES INCIDENTS ET LIMITATIONS

## Incidents
- Aucun incident d'exécution : un seul run CI, extraction complète du
  premier coup (282/282), validation temporelle 15/15 verte avant
  calcul, chaîne vérifiée. Synthèse locale exécutée en ~13 minutes
  (bootstrap 2 000 réplicats × 5 comparaisons + contrôle par blocs),
  sans erreur.
- Note méthodologique (pas un incident) : les paires vendredi→lundi de
  C6-01 ne sont que 7, car la « journée présente précédente » du lundi
  est le plus souvent le dimanche de reprise de cotation, conformément
  à la règle gelée (jours présents successifs, sans chaînage à travers
  une censure). Publié tel quel, sans ajustement.

## Limitations (assumées au gel, rappelées)
- ER, S, PD, τ, AS décrivent les **clôtures M1** : le parcours
  intraminute est invisible (B13) ; sinuosité médiane ~15 à cette
  fréquence, efficiences mécaniquement basses.
- La classe DIRECTIONNELLE (ER ≥ 0,30) est quasi vide à fréquence
  minute (14 journées) : C6-01 non éligible. Toute autre granularité
  serait un nouveau protocole, hors campagne.
- ρ mesure les discontinuités **observées** dans le parcours mesuré,
  jamais la part réelle du mouvement non observé ; PLATE OBSERVÉE ne
  prouve aucune immobilité (0 cas observé sur le corpus).
- Couverture : les censures se concentrent en 2010–13 (halte
  indéterminée fréquente dans les données anciennes) ; les contrastes
  par ère sont publiés avec cet avertissement.
- Terciles d'amplitude de C6-02 contemporains et rétrospectifs : le
  contraste décrit des régimes d'activité du jour même, sans causalité.
- Grandeurs de journée complète rétrospectives (disponibles à la
  clôture) ; aucune lecture « à T0 ».

## Coûts et budgets
- Un run GitHub Actions + synthèse locale ; coût financier 0 FCFA ;
  aucun budget expérimental consommé (tick 148/150, panel 28/60,
  exo 6/60, P7 0/24, NR 0/24, P9 10/12 inchangés). Holdout scellé non
  accédé ; aucun secret exposé dans les livrables ; fiches historiques
  non modifiées.
