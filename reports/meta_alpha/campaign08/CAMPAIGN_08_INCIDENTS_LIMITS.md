# CAMPAGNE 8 — REGISTRE DES CENSURES, LIMITES ET INCIDENTS

## 1. Incidents techniques

**Aucun incident d'extraction** : run CI 44911859012 vert du premier
coup (282/282 partitions). La synthèse locale a nécessité trois
correctifs de code avant tout résultat publié (déballe d'un champ
d'appariement, clés JSON composites, nom de colonne interne incompatible
avec `itertuples`) : aucun n'a modifié une définition gelée ni un
chiffre d'extraction ; la synthèse a été relancée intégralement après
chaque correctif, et les lectures finales proviennent de la passe
complète corrigée. Une relance intermédiaire a été exécutée par erreur
en parallèle de l'écriture d'un correctif (ancienne version relue,
même échec) : aucun résultat n'en a été conservé.

## 2. Censures et inéligibilités (par construction gelée)

10 journées d'amorçage inéligibles à la détection ; 72 épisodes à
clôture indéterminée ; 43 épisodes clos non mixtes censurés à +60
minutes. Tous publiés et exclus selon le protocole, sans substitution.

## 3. Limites

- Le plancher de 10 bp est le seuil effectif la plupart des journées
  (médiane 10,04 bp) : « extrême » signifie donc le plus souvent
  « supérieur à 10 bp et au quantile causal », ce que les distributions
  publiées de I_ép (médiane 1,24) reflètent.
- FJ-05 est non évaluable sous le graphe gelé (composante géante à
  99,8 %, composition sensible par ère) : la question « le sillage
  après un choc diffère-t-il de celui d'instants calmes comparables »
  reste ouverte et ne pourra pas être rouverte sans nouveau protocole.
- Les épisodes regroupés sont plus fréquents dans les contextes agités
  (activité antérieure publiée) : FJ-02 décrit une association, pas un
  effet propre du regroupement.
- 1 322 épisodes mixtes (16,7 %) sont exclus des lectures
  directionnelles par construction ; leur sillage médian proche de
  zéro (−0,53 bp) est publié à titre descriptif.
- Tout le sillage est rétrospectif : l'épisode n'est identifiable qu'à
  t_der + 16 minutes et R₆₀ à t_der + 61 ; aucune disponibilité en
  temps réel n'est revendiquée, et aucun résultat de cette campagne ne
  constitue un signal.
