# CAMPAGNE 6 — RAPPORT SCIENTIFIQUE F-G « FORME DES TRAJECTOIRES JOURNALIÈRES »

**Statut : EXÉCUTION DESCRIPTIVE TERMINÉE** selon le protocole gelé
V1.1 (`0fdb3920…`) + addendum V1.2 (`046df8d9…`) + errata V1.2.1
(`78ef301f…`) et V1.2.2 (`b8e853db…`), prévalence V1.2.2 > V1.2.1 >
V1.2 > V1.1, gel seq239, autorisation d'exécution seq241, gel confirmé
avant extraction seq242. Aucune formule, seuil, population,
comparaison ou méthode n'a été modifié après le gel. Corpus IS
uniquement : 282/282 partitions, 3 540 993 barres M1, 3 097 journées
présentes.

## Population et statuts (publiés intégralement)

- Journées éligibles de forme : **2 772** ; censurées de forme
  (couverture cumulée du protocole : trou de session ≤15 min, cumul
  ≤30 min, taux ≥95 %) : **325**. Aucune journée PLATE OBSERVÉE,
  INDÉTERMINÉE — DISCONTINUITÉS, DOMINÉE PAR LES DISCONTINUITÉS
  OBSERVÉES ni INCOHÉRENTE sur le corpus (priorité V1.2.2 appliquée).
- Par ère (éligibles / présentes) : 2010–2013 : 990/1 245 ;
  2014–2016 : 884/932 ; 2017–2020 : 898/920. Les censures se
  concentrent en 2010–2013 (255), ère où la classe HALTE_INDÉTERMINÉE
  est aussi la plus fréquente (680 journées contre 94 et 76 ensuite).
- Classes de forme des journées éligibles : OSCILLANTE 2 292,
  DÉPLACEMENT FAIBLE 254, MIXTE 212, **DIRECTIONNELLE 14** seulement.
  À la fréquence minute gelée, le chemin L est long (médiane de S ≈
  15,3) et l'efficience médiane vaut 0,0297 (Q1–Q3 : 0,0135–0,0561) :
  le seuil gelé ER ≥ 0,30 n'est presque jamais atteint. C'est un fait
  descriptif central de la campagne : **à granularité minute, les
  journées XAU/USD sont massivement oscillantes au sens du protocole**,
  et la classe directionnelle est structurellement rare.
- ρ (part des discontinuités observées dans le parcours mesuré) :
  médiane 0,0013 ; aucune journée éligible au-dessus de 0,5.

## Résultats détaillés C6-01 à C6-05

Bootstrap par grappes (2 000 réplicats, graine 20261113) ; BY famille
de cinq à **m = 5 fixe** (H₅ = 2,283333) ; matérialité 0,05 d'ER /
30 minutes ; éligibilité ≥200 journées et ≥100 grappes par bras.

| ID | Comparaison | Effet (diff. de médianes) | IC 95 % | p | q BY (m=5) | n A/B | Lecture |
|---|---|---|---|---|---|---|---|
| C6-01 | ER_j selon j−1 directionnel vs oscillant | −0,0007 | [−0,0220 ; +0,0215] | 0,884 | 1,000 | **10** / 2 137 | **NON ÉLIGIBLE** |
| C6-02 | ER selon amplitude (tercile haut vs bas, rétrospectif) | +0,0208 | [+0,0169 ; +0,0241] | 0,0005 | 0,0057 | 924 / 924 | **SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL** |
| C6-03 | ER lundi vs vendredi | −0,0018 | [−0,0062 ; +0,0028] | 0,426 | 1,000 | 434 / 499 | NÉGATIF |
| C6-04 | τ selon signe de Δ_seg (+ vs −) | −4 min | [−10 ; +3] | 0,309 | 1,000 | 1 279 / 1 239 | NÉGATIF |
| C6-05 | ER 2010–13 vs 2017–20 | −0,0027 | [−0,0062 ; +0,0007] | 0,103 | 0,588 | 990 / 898 | NÉGATIF |

### C6-01 — NON ÉLIGIBLE (effectifs publiés, aucun assouplissement)
2 147 paires de jours de cotation successifs éligibles (dont 7 paires
vendredi→lundi marquées VEN_LUN, la journée présente précédant le plus
souvent le lundi étant le dimanche de reprise), 499 semaines. Le bras
« j−1 directionnel » ne compte que **10 paires** (14 journées
directionnelles en dix ans) contre 2 137 « j−1 oscillant » : sous les
seuils gelés (≥200/bras), la comparaison est déclarée **non éligible
telle quelle**. Médianes d'ER_j publiées à titre descriptif : 0,0292
(après directionnel) vs 0,0299 (après oscillant). Le contrôle par blocs
de deux semaines (498 blocs, 0 % de réplicats invalides, IC blocs
[−0,0227 ; +0,0247]) est classé FRAGILE_SIGNE selon la priorité gelée,
sans effet sur une lecture déjà non éligible ; aucun déclassement
supplémentaire, aucune p additionnelle.

### C6-02 — SIGNIFICATIVE SOUS LE SEUIL MATÉRIEL (pas une candidate)
L'efficience est plus élevée dans le tercile haut d'amplitude
(médianes ER : 0,0444 vs 0,0236 ; seuils de terciles décennaux
rétrospectifs : 83,4 et 134,5 bp), différence +0,0208 très
significative (q BY 0,0057) mais **inférieure au seuil matériel gelé de
0,05** : lecture fermée SIGNIFICATIVE_SOUS_LE_SEUIL_MATERIEL, aucune
fiche ANO. Décomposition descriptive publiée (S sans p ni q, règle
gelée) : |Δ_seg|/A médian 0,581 (haut) vs 0,334 (bas), ln-ratio
+0,553 ; S médian 12,70 vs 17,60, ln-ratio −0,326 (hors de l'intervalle
[−ln 1,15 ; +ln 1,15] : la sinuosité relative **diminue** quand
l'amplitude croît). Le contrôle de déclassement « forme → déplacement
relatif » n'est pas déclenché (sa condition |ΔER| ≥ 0,05 n'est pas
remplie) ; il est publié pour traçabilité. Lecture autorisée :
association contemporaine et rétrospective entre régime d'activité du
jour et géométrie mesurée, d'ampleur sous le seuil matériel — aucun
mécanisme, aucune lecture prédictive.

### C6-03, C6-04, C6-05 — NÉGATIFS (publiés)
- C6-03 : aucune différence d'efficience entre lundis et vendredis.
- C6-04 : le point médian de parcours survient à des heures quasi
  identiques selon le signe du déplacement net (médianes τ : 771 vs
  775 minutes, soit ~12:51 vs ~12:55 UTC) ; effet −4 min, très loin du
  seuil de 30 min. PD (secondaire, jamais testé) : médiane 0,506.
- C6-05 : aucune évolution d'efficience entre 2010–13 et 2017–20 au
  seuil gelé (médianes 0,0287 vs 0,0315).

## Conclusion descriptive

La dimension « forme » existe comme mesure (distribution d'ER très
concentrée sous 0,10, sinuosité médiane ~15), mais sur les cinq
contrastes gelés elle ne produit **aucune candidate J1** : un contraste
significatif sous le seuil matériel (C6-02), trois négatifs, et une
comparaison structurellement non éligible par rareté de la classe
directionnelle à fréquence minute (C6-01). Aucune promotion
automatique. Toute suite éventuelle (par exemple une autre granularité
d'observation) constituerait un **nouveau protocole**, hors de la
présente campagne, et exigerait un ordre distinct.
