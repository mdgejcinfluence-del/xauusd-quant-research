# PHASE 24-A — CONTRAT DE RECHERCHE (préenregistrement, aucun entraînement effectué)

Architecture conditionnelle envisagée, gelée : deux variantes séparées et non fusionnables,
`CHAUFFEUR_H1_H4_GATE` et `CHAUFFEUR_H1_D1_GATE` ; permissions du Directeur correspondant +
Horloge 08:00-16:00 UTC sur décision et entrée ; événements H1, 5 variables et cible RESUMPTION
de Phase 12 inchangés ; logistique de type M1 avec nouveaux identifiants et manifestes propres ;
coefficients M1 historiques gelés comme référence comparative (jamais modifiés) ; seuil =
probabilité majoritaire du train filtré, calculé et documenté avant tout examen d'évaluation ;
splits historiques 2010-2015 / 2016-2017 / 2018-2019 (l'évaluation historique se termine en 2019,
le holdout 2020-2026 restant fermé) ; comparaisons H4 vs D1 sur leur intersection temporelle
commune uniquement (`PHASE24A_COMMON_COHORT_AUDIT.csv`) ; aucun classement économique à cette
étape ; attribution Horloge / Directeur / combinaison / réentraînement uniquement sur cohortes
communes.

Condition d'activation : ce contrat ne peut passer en entraînement que si une future autorisation
constate des cohortes satisfaisant les minima (évaluation ≥ 100, minoritaire ≥ 50 ; train
minoritaire ≥ 20 par paramètre). En l'état des populations historiques, cette condition n'est
remplie pour aucune des deux variantes : le contrat est donc **préenregistré mais inactif**.
Aucune sélection de configuration par performance n'a eu lieu.
