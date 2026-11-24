# MA-EDGE-02 — PRÉENREGISTREMENT SECONDAIRE H17 (bras de gestion, jamais de sélection entre bras)

Enregistré au registre (seq412) avant l'observation du moindre événement prospectif.
Motivation historique (consommée, `EXPLORATORY_POST_HOC`) : EXP-08 montre que l'état Mid à
+60 min sépare fortement le PnL terminal des événements sélectionnés (ADVERSE −24,0 bp ;
PLAT −4,2 bp ; FAVORABLE +20,5 bp en moyenne, rejeu 2018-2019 uniquement). Ce bras teste si
cette information, **observable en temps réel**, a une valeur de gestion prospective.

**Bras H17 (secondaire, descriptif-confirmatoire séparé)** : même population, même entrée,
même modèle gelé que l'étude principale deadline. À t_decision + 60 min, si le rendement Mid
directionnel (clôture de la 4e barre M15 suivant la décision, base clôture de la barre de
décision) est **< −10 bp**, liquidation au premier prix exécutable ≤ 60 s ; sinon le bras suit
exactement la règle principale (deadline 120 min / référence 8 h). Comparaison préenregistrée :
différence appariée bras H17 − règle principale, bootstrap par grappes (graine 2129), même
population prospective postérieure au présent préenregistrement
(2026-11-24, horodatage du commit portant seq412 — la borne exacte est celle du commit Git).
**Interdictions** : choisir entre la règle principale et H17 selon leurs résultats respectifs
pour déclarer un vainqueur ; modifier le seuil −10 bp ou l'horizon 60 min ; utiliser ce bras
pour interrompre ou amender l'étude principale. Chaque bras rapporte ses propres critères ;
toute « meilleure » règle future exigera un nouveau préenregistrement et une nouvelle
population. Si l'exécution à +60 min est impossible (cotation absente ≤ 60 s), l'événement est
`EXIT_NONEXECUTABLE` dans ce bras et compté comme tel.
