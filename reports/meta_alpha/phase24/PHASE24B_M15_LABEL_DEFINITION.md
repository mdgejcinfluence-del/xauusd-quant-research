# PHASE 24-B — DÉFINITION M15 DE LA RÉINTÉGRATION ET DU LABEL (gelée seq392)

Adaptation M15 des définitions historiques 11-A/12-A, sens économique conservé, conversions
explicites :

- **Impulsion** : barre M15 complète dont |BODY_M15_BP| ≥ Q90 des |BODY| des 250 barres M15
  complètes précédentes (barre courante exclue) ; direction = signe du corps ; t0 = clôture de
  la barre ; P0 = Close Mid. (Historique H1 : seuil Q95 sur barres H1 — la présente phase applique
  la règle Q90/250 barres prescrite par son ordre de mission ; écart documenté, non dissimulé.)
- **Fenêtre d'observation** : 32 barres M15 = 8 heures nominales (conversion exacte de la fenêtre
  historique de 8 bougies H1).
- **Réintégration** : première clôture M15 strictement de l'autre côté de P0, postérieure à une
  clôture M15 confirmant le déplacement initial (clôture au-delà de P0 dans le sens initial).
  Unité de confirmation : la clôture M15 (historique : clôture M1) — conversion de résolution
  assumée et documentée. t_decision = clôture de la barre de réintégration.
- **`Y_RESUMPTION`** : 1 si une clôture M15 ultérieure dépasse le meilleur niveau de clôture
  favorable atteint avant la réintégration, avant la fin des 32 barres ; 0 sinon (dont
  invalidation préalable ou absence de dépassement). Population = événements réintégrés, comme
  en Phase 12.
- **Invalidation structurelle** : première clôture M15 au-delà de l'extrême adverse de la barre
  d'impulsion (bas pour un LONG, haut pour un SHORT) — origine de l'impulsion, sans buffer ni
  tolérance ajoutés. Temps jusqu'à invalidation et statut enregistrés.
- **Censure** : fenêtre de 32 barres incomplète (fin de barset) = `CENSURE_FENETRE` (1 cas) ;
  non-réintégrés (8 834) conservés au catalogue, hors population du label.

Aucun coefficient, seuil ou horizon du M1 n'est transposé. Le label est figé avant tout calcul
de performance future ; aucun entraînement n'a eu lieu dans cette phase.
