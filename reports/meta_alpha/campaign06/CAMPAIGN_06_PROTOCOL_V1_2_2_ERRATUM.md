# CAMPAGNE 6 — ERRATUM V1.2.2 (règle de priorité des statuts de journée)

**Statut : ERRATUM TRÈS COURT — GEL ET EXÉCUTION INTERDITS, AUCUN
CALCUL.** Relié à la V1.1 (`0fdb3920…`), à l'addendum V1.2 (`046df8d9…`)
et à l'erratum V1.2.1 (`78ef301f…`). Il ne modifie aucune définition ni
aucun seuil ; il fixe uniquement la priorité entre statuts lorsqu'une
journée satisfait les conditions de plusieurs d'entre eux. En cas de
tension, le présent erratum prévaut.

## Règle de priorité (un seul statut par journée, dans cet ordre)

1. **L = 0 et D = 0** : statut **PLATE OBSERVÉE**. ER et ρ sont
   indéfinies lorsque leurs dénominateurs sont nuls (publiées NaN,
   aucune valeur artificielle) ; S indéfinie si A = 0. Journée comptée
   et publiée, exclue de tout ratio.
2. **L = 0 et D > 0** : statut **INDÉTERMINÉE — DISCONTINUITÉS**,
   exclue des populations primaires de forme. ρ = D/(L+D) = 1 est
   définie et peut être **publiée comme mesure descriptive**, sans
   modifier le statut : le critère ρ > 0,5 ne s'applique pas à ce cas,
   la priorité 2 prime sur la priorité 3.
3. **L > 0 et ρ > 0,5** : statut **DOMINÉE PAR LES DISCONTINUITÉS
   OBSERVÉES**, exclue de l'analyse primaire (publiée séparément).
4. **Autres cas** : application des critères d'éligibilité (couverture
   cumulée, trou maximal) et des classifications déjà gelés
   (DÉPLACEMENT FAIBLE prioritaire, puis classes ER), sans changement.

Aucune autre définition, formule, constante ou seuil de la V1.1, de la
V1.2 ou de la V1.2.1 n'est modifié.

## Soumission

Dossier soumis pour validation du gel définitif : V1.1 (`0fdb3920…`) +
addendum V1.2 (`046df8d9…`) + erratum V1.2.1 (`78ef301f…`) + présent
erratum V1.2.2. Après validation seulement : gel chaîné des quatre
documents, puis ordre d'exécution séparé. Restrictions inchangées :
XAU/USD exclusivement, holdout scellé, aucun calcul ni extraction,
aucun backtest ni `challenge_sim`, aucun J2/J3 automatique, aucun
budget expérimental consommé, FRED suspendue, 36 cellules S12 gelées,
T0 séparé et inactif, aucune modification des fiches historiques.
