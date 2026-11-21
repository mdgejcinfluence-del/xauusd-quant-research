# CAMPAGNE 8 — RAPPORT SPÉCIFIQUE PSEUDO-ÉVÉNEMENTS (FJ-05)

**Protocole gelé V2 §6–§8. Lecture finale : NON ÉVALUABLE.**

## 1. Bassin et appariement

Bassin : première minute éligible par (journée éligible × session ×
bloc de 60 minutes depuis le début de session), sans choc dans les
60 minutes précédentes, activité antérieure A_avant complète, variation
non nulle et non extrême : **53 920 pseudo-événements**. Aucune
propriété de leur sillage futur n'a servi à les sélectionner ni à les
exclure ; un choc ultérieur y est publié (drapeau NOUVEAU_CHOC, taux
10,5 % dans le bassin).

Épisodes candidats (isolés, clos, non mixtes, A_avant défini) :
**5 191, tous appariés** (aucun motif de non-appariement : ni strate
vide ni distance de position > 60 minutes). Paires dont les deux R₆₀
sont définis : **5 126**. Terciles d'A_avant par session publiés dans
`CAMPAIGN_08_DETAILS.json`.

## 2. Pourquoi FJ-05 est non évaluable

Deux contrôles gelés, qui ne créent aucune p-value, se déclenchent :

- **Grappes insuffisantes et GRAPPE_DOMINANTE** : le graphe de
  dépendance du V2 (même journée, sillages chevauchants, sillage
  contenant un choc d'une autre unité, arête d'appariement, frontières
  journalières traversées) fusionne les 10 252 unités en **12
  composantes connexes**, la plus grande contenant **99,8 %** des
  unités des deux bras. L'éligibilité gelée exige ≥ 100 grappes par
  bras : elle n'est pas atteinte. Les arêtes d'appariement reliant des
  journées différentes sont le principal mécanisme de fusion
  inter-journalière.
- **COMPOSITION_SENSIBLE** : parts d'ère des paires — épisodes
  47,3 / 32,8 / 19,9 % contre pseudo-événements 65,7 / 22,3 / 12,0 %
  (écarts de 18,3, 10,3 et 7,9 points) : les pseudo-événements retenus
  par l'appariement chronologique proviennent disproportionnellement
  de 2010–2013, ère où le bassin est le plus dense relativement aux
  épisodes. Effectifs croisés ère × session publiés dans le fichier de
  détails.

## 3. Ce qui est publié à titre descriptif (sans lecture)

Différence brute de médianes de R₆₀ (épisodes − pseudo-événements) :
−4,28 bp, intervalle de bootstrap [−11,10 ; +13,95] à titre indicatif,
p 0,259 et q BY 0,739 publiées sans valeur inférentielle. Médianes de
session des pseudo-événements appariés : S1 −0,62, S2 −0,44, S3 −0,26,
S4 +1,64 (n 34). Taux de nouveau choc : 25,8 % chez les
pseudo-événements appariés contre 29,6 % chez les épisodes (fenêtres
comparables, lecture descriptive uniquement).

## 4. Portée

La non-évaluabilité est un résultat du protocole gelé, pas un échec
d'exécution : elle établit que, sous la définition de dépendance la
plus prudente (composantes connexes incluant les appariements), FJ-05
ne dispose pas de l'indépendance statistique requise pour être lue.
Aucun assouplissement (retrait d'arêtes, réutilisation de
pseudo-événements, élargissement de strates) n'a été appliqué ; toute
reprise de cette question exigerait un nouveau protocole soumis au
propriétaire.
