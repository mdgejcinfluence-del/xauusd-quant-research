# AUDIT FORENSIQUE DES 47 RÈGLES MA-ALPHA-GOLD-01

Recomptage indépendant depuis `EXPERIMENT_RESULTS.csv` (détail : `AUDIT_47_REGLES_DETAIL.csv`).
Distribution des règles selon le nombre de périodes à moyenne nette positive : **3 périodes : 2
règles ; 2 périodes : 19 ; 1 période : 9 ; 0 période : 18.**

**Correction à la conclusion GOLD-01** : l'affirmation « aucune règle positive sur les trois
périodes » doit être précisée. Deux règles le sont : (1) continuation après journée extrême H5
(+20,95/+21,63/+77,11 bp) ; (2) dérive longue du bloc H4 17-22h (+1,10/+0,13/+1,41 bp par barre)
— cette dernière est positive mais **inférieure au coût d'un aller-retour** et donc sans valeur
économique ; la formulation correcte est : « aucune règle *économiquement significative* et
cohérente, à l'exception fragile de la continuation après journée extrême ». La conclusion
économique de GOLD-01 est inchangée ; sa formulation est corrigée ici et au registre (seq421).

Populations et coûts rappelés : COT/GVZ/taux/momentum sur D1 (coût 2,30 bp), barrières sur
événements M15 (2 bp), sessions sur H4. Dépendances : les règles d'une même famille partagent
leurs événements (les 47 ne sont pas 47 essais indépendants) ; les périodes se chevauchent en
événements pour les horizons longs — les moyennes sont descriptives. **Contrôle holdout : les
trois périodes proviennent exclusivement des barsets 2010-2019 (PHASE20A/21A/24B, bornés au
2019-12-16) ; le holdout 2020-2026 n'a pas été touché.** Les 19 règles « 2 périodes sur 3 »
illustrent le risque de sélection : sans le critère des trois périodes, une dizaine de faux
edges auraient pu être présentés.
