# CAMPAGNE 0 — QUALITÉ ET DISPONIBILITÉ DES DONNÉES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

| Contrôle | Résultat |
|---|---|
| Partitions traitées | **282/282, 0 sautée** (run final 44713904881) ; corpus tick IS, borne 2020-01-20T09:36:27Z respectée |
| Journées distinctes | 3 097 journées avec barres ; 3 048 journées contribuant aux rendements M1 (≥ 5 barres/jour exigées par le moteur) |
| Barres produites | M1 : 3 537 724 · M5 : 709 189 · M15 : 234 208 · H1 : 56 331 (rendements intra-journée) |
| Couverture temporelle | Ères : 2010–2013 (1 432 902 barres M1), 2014–2016 (1 059 147), 2017–2020 (1 045 675) |
| Régime F3 | Jours classés par tercile de vol prédite (prévision ≤ j−1 par construction du modèle gelé) ; jours sans prédiction = NON_CLASSE, en global seulement |
| Données manquantes | Buckets vides jamais imputés ; journées < 5 barres exclues de l'accumulation (comptées dans l'écart 3 097 → 3 048) |
| Doublons | Ordre (timestamp, observation_id), patron historique des moteurs du programme |
| Prix | Barres sur **Mid** (déclaré au dictionnaire gelé) ; spread rapporté à part (V12) ; rien n'est un prix exécutable |
| Holdout | Non accédé, non téléchargé, non approché |
| Accès corpus | Kaggle du programme, repli miroir Drive du même corpus (patron F15/P11-A1) ; corpus brut jamais versé dans Git |

## Incidents d'exécution (consignés)

1. Premier run (44709555118) : échec de l'étape moteur sans diagnostic commité —
   corrigé en faisant commettre la sortie du moteur (`CI_LOG.txt`) par le workflow.
2. Run 44713153687 : le `STATE.json` persisté du run précédent a fait sauter les
   282 partitions (« déjà traitées ») et produit un CSV vide ; l'écrasement a été
   constaté, un garde-fou anti-écrasement ajouté, l'état réinitialisé et le calcul
   relancé intégralement (run 44713904881, succès, 288 cellules). Aucun chiffre du
   run vide n'a été utilisé.
3. Suspension 12.3 : le run annulé 44702531257 a poussé son commit final
   (`19a3e90`, comptages de configurations) avant l'effet de l'annulation ; artefact
   conservé tel quel sur ordre du propriétaire, **non consulté et non analysé**
   (consigné seq 154).

## Limites résiduelles

- Résolution : les barres M1 agrègent le tick ; toute microstructure intra-minute est
  hors de portée de cette campagne.
- La série F3 ne couvre pas les tout premiers jours de l'IS (amorçage du modèle) :
  régime NON_CLASSE en début de période.
- Les sessions sont des blocs UTC conventionnés (seq 144/146), pas des heures
  d'ouverture de places au sens réglementaire ; correspondance locale/DST documentée
  en seq 146.
- V6/V7 : statistiques poolées uniques (n = 1 dans le CSV par construction) — voir
  rapport §4.
