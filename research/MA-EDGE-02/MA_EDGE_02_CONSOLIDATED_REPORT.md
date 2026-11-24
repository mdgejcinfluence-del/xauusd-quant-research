# MA-EDGE-02 — RAPPORT CONSOLIDÉ DE RECHERCHE (seq409 → seq414)

Réponses aux quinze questions exigées avant présentation. Tout résultat historique est
`EXPLORATORY_POST_HOC` ; seul le dispositif prospectif peut un jour produire une validation.

**1. Nouvelles connaissances.** (a) Le blocage de flux est levé : Dukascopy public fournit des
ticks Bid/Ask XAUUSD vérifiés (43–50 k/heure, 0 violation, spread ≈ 1 bp) ; première heure
post-préenregistrement collectée (19:00 UTC, 32 375 ticks). Limitation découverte : le cron
GitHub ne s'exécute que depuis la branche par défaut — la collecte est relancée par dispatch à
chaque session de travail et reste à automatiser côté branche principale un jour.
(b) Après une impulsion M15, les excursions favorables et défavorables sont **quasi symétriques**
(EXP-11 : MFE+MAE médians entre −1,3 et +0,2 bp à tous horizons et terciles d'amplitude).
(c) La continuation d'impulsion existe comme régularité statistique faible (EXP-09 : +0,6/+1,2/
+1,3 bp Mid à 32 barres, signe cohérent sur trois périodes) mais elle est **inférieure aux
coûts** (scénarios 2–4 bp) : économiquement morte. (d) L'état de la position à +60 min sépare
fortement le destin terminal (EXP-08). (e) La géométrie potentiel/risque à la décision prédit
le label, pas l'argent (EXP-10).

**2. Mécanismes identifiés.** Le mécanisme de perte reste la **dérive après excursion favorable**
(EXP-07 : 265/405 faux positifs, −39 bp, MAE médian à 225 min). Le mécanisme de « gain » des
événements confirmés est une confirmation rapide (médiane 60 min). Entre les deux : une zone
plate (−4,2 bp) qui paie le spread sans décider.

**3. Hypothèses réfutées dans ce cycle.** Continuation/fade/confirmation locale/entrée différée
comme familles autonomes (EXP-09, majorants Mid sous les coûts, placebo non dépassé en
découverte pour la continuation 8 barres) ; asymétrie d'excursion exploitable post-impulsion
(EXP-11) ; géométrie du risque comme filtre économique (EXP-10, PnL non monotone, tout
négatif) ; GVZ et COT comme filtres (25-B, cycle précédent).

**4. Hypothèses qui méritent de continuer.** La deadline 120 min (prospectif en collecte, règle
gelée) ; H17 — gestion par état à +60 min — désormais **préenregistrée comme bras secondaire**
(seq412, seuil −10 bp figé, aucune sélection entre bras autorisée) ; H19 abstention par coût
(EXP-12 descriptif : spread de décision élevé ↔ PnL −6,1 vs −1,9 bp, à revoir en prospectif où
le spread est journalisé).

**5. Informations à vraie valeur ajoutée.** L'information **post-entrée observable en temps
réel** (trajectoire à 60 min) vaut plus que toutes les informations pré-entrée testées depuis
25 phases : c'est le premier renversement de perspective du programme — gérer la position
ouverte plutôt que mieux choisir l'entrée.

**6. Pourquoi certaines configurations gagnent.** Quand la confirmation survient tôt, le
mouvement paie +12,5 bp en moyenne avant que la dérive adverse ne s'installe ; la probabilité
de confirmation conditionnelle à un état favorable à 60 min atteint 0,94 (EXP-08).

**7. Pourquoi d'autres perdent lentement.** Après un MFE initial sans confirmation, le prix
reflue par paliers (MAE médian 46 bp atteint vers 277 min) : ni invalidation franche ni reprise
— une détérioration progressive qu'aucun stop structurel du contrat actuel ne coupe.

**8. Conditions pour éviter les opérations défavorables.** À ce jour, une seule est démontrée
descriptivement : être déjà adverse à +60 min prédit −24 bp terminal. Aucune condition
pré-entrée (score, GVZ, COT, régime, géométrie, spread) n'a séparé économiquement les gagnants.

**9. Meilleure combinaison d'informations.** Aucune combinaison pré-entrée ne survit aux coûts.
La combinaison justifiée est séquentielle : entrée par le modèle gelé (information prédictive
réelle mais insuffisante) + gestion post-entrée (deadline, et bras H17 en observation).

**10. Architecture la plus prometteuse.** Exactement celle en observation prospective :
M15_TIME_ONLY inchangé, sortie par deadline de non-réalisation 120 min, référence 8 h, bras
H17 secondaire. Aucune autre architecture n'a de justification supérieure.

**11. Résultats économiques démontrés.** Aucun positif. Le meilleur majorant nouveau
(continuation 32 barres, +1,3 bp Mid en rejeu) est détruit par 2–4 bp de coûts. Le PnL
sélectionné de référence reste −3,31 bp S2 (24-D).

**12. Coûts intégrés.** PnL historiques en comptabilité 19-B complète (spread réel tick, S0/S1/
S2) pour tout ce qui touche aux événements ; scénarios forfaitaires 0/2/4 bp, présentés comme
majorants, pour les familles nouvelles en barres Mid ; commissions toujours exclues et nommées.

**13. Risques restants.** Dépendance à un seul courtier de cotation (niveau B) ; retard de
publication Dukascopy ; échantillon prospectif à construire (≈ 350 événements, des mois) ;
risque que l'état à +60 min ne soit qu'un reflet du label plutôt qu'un levier (le bras H17 le
départagera prospectivement) ; queue de distribution toujours présente (−216 bp historique).

**14. Robustesse.** Les régularités retenues ont le même signe sur découverte/contrôle/rejeu ;
celles qui ne l'ont pas (confirmation locale, entrée différée) sont classées fragiles et closes.
Placebos systématiques sur les familles nouvelles.

**15. Validé vs exploratoire.** Validé indépendamment : **rien de nouveau**. Le seul chemin de
validation ouvert est le SHADOW (deadline + H17), dont la population compte à ce jour une heure
de cotations et zéro événement — la chauffe de 250 barres est en cours de collecte rétrospective
autorisée (contexte seul, décisions strictement postérieures au 2026-11-24T17:12:57Z).

## Décisions autonomes prises dans ce cycle

Flux Dukascopy retenu et branché ; clarifications du contrat sans toucher à la règle ; EXP-08 à
EXP-12 préenregistrées puis exécutées ; quatre familles closes ; bras H17 préenregistré ;
collecte étendue à la chauffe ; cron reconnu inopérant sur branche non par défaut (contourné par
dispatch, à régulariser si le fondateur fusionne un jour vers `main`).

## Suite (sans arbitrage requis)

Collecte quotidienne par dispatch à chaque session ; premier rapport descriptif à 25 événements
sélectionnés prospectifs ; préparation du connecteur MT5 démo (identité fondateur requise, rien
d'inventé) ; aucune conclusion économique avant la taille préenregistrée. Si H17 se confirme
prospectivement, une règle de gestion composée exigera son propre préenregistrement et sa propre
population — elle ne sera jamais rétro-optimisée sur les événements de la deadline.
