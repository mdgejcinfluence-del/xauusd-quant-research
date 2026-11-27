# ME-003.1 — CONTINUATION D'IMPULSION : RAPPORT

Protocole gelé seq490 : impulsion de 5 min ≥ 5/10/20 bp, trade dans
le sens du mouvement aux prix exécutables, sorties marquées à
15 min / 1 h / 4 h, coûts comptés une fois, refroidissement d'1 h.
5 128 épisodes, 5 partitions certifiées.

## Résultat

- **Continuation de trajectoire : réelle.** Dans les 1 h qui suivent,
  le prix prolonge le mouvement d'au moins la moitié de l'impulsion
  dans 60–89 % des cas ; excursion favorable médiane +8 à +14 bp.
- **Edge exécutable : RÉFUTÉ.** L'espérance nette est négative aux
  **trois horizons, trois seuils et deux groupes** (−1,6 à −8,6 bp),
  médianes négatives, 28–47 % de gagnants. L'extension est transitoire :
  elle se produit *à un moment* de l'heure qui suit, puis se résorbe ;
  aux instants fixes d'évaluation, acheter après l'impulsion revient à
  payer le spread pour chasser un mouvement déjà épuisé. Cela prolonge
  AESR-002 (retours forward faibles après entrées simulées).

## Lecture croisée ME-002 × ME-003 (la vraie découverte de la session)

Les deux exploitations naïves des excursions échouent, pour des
raisons opposées et complémentaires : le fade vers la médiane perd
parce que les écarts persistent avant de se résorber (queue des
continuations) ; la continuation perd parce que les extensions se
résorbent avant les horizons fixes (queue des retournements). Ce qui
survit à ce double tri, c'est la géométrie asymétrique de **ME-001** :
n'acheter que le creux après chute depuis un plus haut, viser le
retour complet à ce plus haut (gain potentiel multiple du seuil),
filtrer les contextes de volatilité excessive à l'entrée — et accepter
que la queue des non-récupérations reste le risque central, géré par
le budget et non par un stop. ME-001 reste la seule candidate ;
sa validation prospective (données postérieures au gel, règle
d'arrêt seq486) est le verrou scientifique restant.

## Verdict

ME-003 (continuation d'impulsion à horizons fixes) : **REJECTED**
sous cette forme. Aucun moteur créé.
