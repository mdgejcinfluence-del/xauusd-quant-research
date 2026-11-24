# PHASE 24-E — RAPPORT FINAL : POURQUOI LA PRÉDICTION NE SE CONVERTIT PAS

Statut : `EXPLORATORY_POST_HOC`. Aucune stratégie nouvelle n'est revendiquée.

## Le label se réalise tôt et il est capturable — quand il se réalise

Niveau de référence réconcilié à 16 054/16 054. Parmi les 1 124 sélectionnés, 719 réalisent le
label, avec un délai médian de **60 minutes** (P90 : 240 min). Liquidés au premier prix exécutable
après la clôture de confirmation (`FIRST_LABEL_PASSAGE_EXIT_DIAGNOSTIC`, jamais un prix au niveau
théorique), ces événements gagnent **+11,36 bp en S2 en moyenne (médiane +8,76 ; 94,3 % positifs)**,
après un chemin peu adverse (MAE médian avant passage : 8,6 bp).

## Mais sortir au premier passage n'améliore rien

Sur les mêmes 717 événements comparables, la liquidation fixe à 8 heures gagne **+12,50 bp** :
différence appariée −1,11 bp, IC95 par grappes [−4,72 ; +2,39]. Le gain n'est **pas restitué**
après réalisation — les excursions post-passage sont symétriques (≈ 21 bp dans chaque sens,
médianes). L'hypothèse « propriété de trajectoire qui disparaît avant la liquidation » est donc
réfutée pour les événements réalisés.

## La perte vient des faux positifs

Les 405 événements sélectionnés dont le label ne se réalise jamais perdent en moyenne
**−31,29 bp** à 8 heures. Le diagnostic complet (sortie au passage si réalisé, sinon à 8 h)
affiche −4,00 bp, moins bon que les −3,31 bp de la politique 24-D. Le Chauffeur prédit un
événement réel et tôt, mais avec une précision insuffisante : 36 % de sa sélection ne réalise
jamais l'événement, et ces échecs coûtent environ trois fois ce que les réussites rapportent à
la sortie fixe.

Verdicts : réalisation du label — **`LABEL_EVENT_EARLY_AND_ECONOMICALLY_CAPTUREABLE`** ;
conversion par la sortie au premier passage — **`NO_ECONOMIC_IMPROVEMENT_FROM_FIRST_PASSAGE_EXIT`**.
Toute architecture de risque future devra être préenregistrée séparément ; aucun passage en
démonstration ou en réel n'est autorisé.
