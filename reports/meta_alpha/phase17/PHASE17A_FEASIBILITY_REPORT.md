# PHASE 17-A — RAPPORT DE FAISABILITÉ DU META-MODÈLE ÉCONOMIQUE M2

**Nature : faisabilité documentaire et numérique (effectifs et
disponibilités uniquement). Aucune étiquette économique nouvelle
n'a été construite hors du segment d'évaluation déjà traité en
Phase 14, aucun modèle n'a été entraîné, aucune performance
économique nouvelle n'est produite.**

## 1. Les huit questions de faisabilité

1. **Labels B08/B09 constructibles sur les populations IS ?**
   Oui. La machinerie exacte (entrée E0 au premier tick, barrières
   ATR ancrées au prix réel, franchissement au premier tick,
   statuts et censures) a été exécutée et gelée en Phase 14 sur les
   443 exposés d'évaluation ; les ticks IS et les barres
   nécessaires couvrent 2010–2020 (mêmes lots CI). L'extension aux
   segments apprentissage (1 143 filtrés) et calibration (360) est
   une ré-exécution du même code gelé, sans nouvelle méthode. Les
   étiquettes d'évaluation existent déjà (`PHASE14_TRIPLE_BARRIER_EVENTS.csv`).
2. **Cinq variables causales disponibles pour tous les segments ?**
   Oui : `PHASE12B_FEATURES.csv` les contient pour les 2 690
   événements F10-01 étiquetés (apprentissage, calibration,
   évaluation), sans aucune valeur manquante, avec borne temporelle
   vérifiée en Phase 12-B (données ≤ `t_decision` uniquement).
3. **ATR et spread de décision disponibles ?** Oui : ATR14_H1 déjà
   calculé pour l'évaluation (Phase 14) et reconstructible à
   l'identique pour les autres segments depuis les barres M1
   Bid/Ask committées (2010–2020 complets) ; spread de décision
   (minute se terminant à `t_decision`) présent dans les mêmes
   barres. Aucune donnée externe requise.
4. **Populations suffisantes ?** Au stade de la population :
   apprentissage filtré 1 143, calibration 360, évaluation 443 —
   très supérieurs aux planchers historiques du programme. La
   suffisance **par classe d'étiquette** (`Y_ECON` sous S2) ne
   pourra être constatée qu'à la construction des étiquettes en
   17-B ; les critères de rejet sont préenregistrés (n < 100 ou
   minorité < 50 par contrat et segment ⇒ `NON_EVALUABLE`), sans
   pooling ni assouplissement possibles.
5. **Incomplets et gaps traitables sans biais ?** Oui, par les
   conventions déjà gelées (14/14.1) : censurés et non-résolus
   jamais étiquetés 0/1, exclus du modèle mais comptés et publiés ;
   classification des barrières des trajectoires incomplètes
   seulement avant la première interruption ; limites de preuve
   des franchissements après trou inchangées et à republier.
6. **Séparation chronologique par grappe possible ?** Elle existe
   déjà : ensembles 12-B par grappe entière, 0 grappe partagée
   (revérifié en 17-A), purge des chevauchements d'horizon
   matérialisée avec motifs, intervalles d'étiquetage contenus
   dans les segments. Aucune nouvelle séparation n'est créée.
7. **Matrice M2 évaluable sans fuite ?** Oui sous les choix gelés :
   variables bornées à `t_decision` (audit au dictionnaire),
   `p_M1` **exclu** des variables faute de série hors échantillon
   pour l'apprentissage (il reste le filtre primaire, en amont),
   cible et dérivés futurs absents des variables, métriques contre
   `M0_ECON` calculé sur le seul apprentissage.
8. **Seuil économique calculable sur le seul apprentissage ?**
   Oui : gains/pertes moyens conditionnels des P&L d'apprentissage
   sous S2 ⇒ seuil `L/(G+L)` gelé avant évaluation ; non
   estimable ⇒ `NON_EVALUABLE` (règle préenregistrée).

## 2. Limites structurelles à ne pas oublier en 17-B

- Le filtre primaire appliqué à l'apprentissage utilise des
  probabilités **en échantillon** (M1 y a été ajusté) : la
  population d'apprentissage de M2 est donc sélectionnée par un
  filtre plus optimiste que celui, réellement hors échantillon,
  de la calibration et de l'évaluation. `M0_ECON`, le seuil et les
  coefficients de M2 hériteront de ce biais de sélection ; la
  calibration 2016–2017 (probabilités hors apprentissage) servira
  de contrôle chronologique, sans effacer la limite.
- L'évaluation 2018–2020 a déjà servi aux Phases 12-B à 16 : tout
  résultat M2 y sera **exploratoire**, jamais une confirmation
  indépendante. Le niveau 3 exigerait des données postérieures au
  gel de la Phase 17, sous décision distincte ; le holdout
  consommé est définitivement exclu.
- Les étiquettes dépendent du scénario de coûts primaire S2
  (slippage hypothétique) et excluent les commissions : même un
  M2 performant ne démontrerait pas une rentabilité nette
  complète.

## 3. Conclusion de faisabilité

Définitions des étiquettes, variables auditées, conventions de
coûts et de payoff, baseline `M0_ECON`, forme de modèle, seuil
économique, séparation par grappe purgée et critères de
non-évaluabilité sont établis et préenregistrés ; les effectifs
de population et la disponibilité des données sont constatés sur
artefacts. **Verdict : `PHASE17A_READY_FOR_ECONOMIC_META_MODEL`** —
sous les conditions consignées au préenregistrement (construction
des étiquettes apprentissage/calibration par le code gelé,
vérification des critères par classe avant tout entraînement,
double contrat B08/B09 rapporté intégralement sans sélection,
qualification exploratoire permanente des résultats IS). La
Phase 17-B restera soumise à une décision distincte.
